"""Generic A* over SearchProblem (Late goal test, no reopen, lazy OPEN)."""

from __future__ import annotations

import time
from typing import Callable, Generic, Hashable, Optional, TypeVar

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.heuristics.base import UniHeuristic
from sfbds_compare.metrics.collector import MetricsCollector
from sfbds_compare.search.nodes import AStarNode
from sfbds_compare.search.result import SearchResult, TerminationReason
from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import LazyHeapOpen
from sfbds_compare.structures.ordering import tbh_sort_key

StateT = TypeVar("StateT", bound=Hashable)


def _reconstruct_path(node: AStarNode[StateT]) -> list[StateT]:
    path: list[StateT] = []
    cur: Optional[AStarNode[StateT]] = node
    while cur is not None:
        path.append(cur.state)
        cur = cur.parent
    path.reverse()
    return path


class AStarSearcher(Generic[StateT]):
    """A* with Late goal test, NoReopen, TBh ordering via lazy OPEN.

    Metric conventions (locked for MVP comparisons with SFBDS):
    - **Late:** goal is detected when selected from OPEN; that selection is
      **not** counted in ``expanded``.
    - **Parent suppression:** successors use ``forbid_state=parent``, matching
      the SFBDS BF/expansion convention. ``generated`` is therefore lower than
      textbook A* that re-generates the reverse parent edge (usually already CLOSED).
    """

    def __init__(
        self,
        heuristic: UniHeuristic[StateT],
        *,
        metrics_factory: Optional[Callable[[], MetricsCollector]] = None,
    ) -> None:
        self._heuristic = heuristic
        self._metrics_factory = metrics_factory or MetricsCollector

    def search(self, problem: SearchProblem[StateT]) -> SearchResult[StateT]:
        metrics = self._metrics_factory()
        metrics.start()

        def sort_key(node: AStarNode[StateT]):
            return tbh_sort_key(node.f, node.h, node.g, node.state)

        open_list: LazyHeapOpen[StateT, AStarNode[StateT]] = LazyHeapOpen(
            key_of=lambda n: n.state,
            g_of=lambda n: n.g,
            sort_key_of=sort_key,
        )
        closed: ClosedSet[StateT, AStarNode[StateT]] = ClosedSet()

        t0 = time.perf_counter()
        h0 = self._heuristic.evaluate(problem.start_state, problem)
        metrics.add_heuristic_time(time.perf_counter() - t0)

        start = AStarNode(state=problem.start_state, g=0.0, h=h0, parent=None)
        open_list.push(start)
        metrics.note_open_size(open_list.logical_size())

        while not open_list.is_empty():
            current = open_list.pop_min()
            if current is None:
                break
            metrics.stale_skipped = open_list.stale_skipped

            # Late goal test: when selected for expansion.
            if problem.is_goal(current.state):
                path = _reconstruct_path(current)
                snap = metrics.finish(success=True, solution_cost=current.g)
                return SearchResult(
                    success=True,
                    termination_reason=TerminationReason.GOAL_FOUND,
                    metrics=snap,
                    solution_cost=current.g,
                    path=path,
                )

            if closed.contains(current.state):
                # Should be rare with NoReopen + best-g discipline; skip safely.
                continue

            closed.add(current.state, current)
            metrics.expanded += 1
            metrics.note_closed_size(len(closed))

            parent_state = current.parent.state if current.parent is not None else None
            for succ in problem.successors(
                current.state, forbid_state=parent_state
            ):
                metrics.generated += 1
                new_g = current.g + succ.cost

                if closed.contains(succ.state):
                    metrics.duplicates_discarded += 1
                    continue

                best = open_list.get_best(succ.state)
                if best is not None and new_g >= best.g:
                    metrics.duplicates_discarded += 1
                    continue

                t1 = time.perf_counter()
                h = self._heuristic.evaluate(succ.state, problem)
                metrics.add_heuristic_time(time.perf_counter() - t1)

                child = AStarNode(
                    state=succ.state, g=new_g, h=h, parent=current
                )
                open_list.push(child)
                metrics.note_open_size(open_list.logical_size())

        metrics.stale_skipped = open_list.stale_skipped
        snap = metrics.finish(success=False, solution_cost=None)
        return SearchResult(
            success=False,
            termination_reason=TerminationReason.OPEN_EXHAUSTED,
            metrics=snap,
        )
