"""Generic SFBDS over SearchProblem (Late goal, injectable policies)."""

from __future__ import annotations

import time
from typing import Callable, Generic, Hashable, Optional, TypeVar

from sfbds_compare.domain.base import SearchProblem, Successor
from sfbds_compare.heuristics.base import PairHeuristic
from sfbds_compare.metrics.collector import MetricsCollector
from sfbds_compare.policies import PolicyBundle, default_policies
from sfbds_compare.policies.types import PathAction, Side
from sfbds_compare.search.nodes import SFBDSNode, reconstruct_sfbds_path
from sfbds_compare.search.result import SearchResult, TerminationReason
from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import LazyHeapOpen

StateT = TypeVar("StateT", bound=Hashable)
PairKey = tuple[StateT, StateT]


class SFBDSSearcher(Generic[StateT]):
    """Single-frontier bidirectional search with injectable policies/heuristic.

    ``policies`` default is ``default_policies()`` (NoReopen). That is official
    F2F. Official F2E is :func:`official_f2e_searcher`, not
    ``SFBDSSearcher(F2EPairLowerBound())``.

    Metric conventions (aligned with A* MVP):
    - **Late:** goal when selected from OPEN (``forward == backward``); that
      selection is **not** counted in ``expanded``.
    - **Parent suppression:** children use ``forbid_forward`` / ``forbid_backward``.
    - **Heuristic evals:** ``h_gap`` is evaluated only when about to insert/improve
      OPEN (after duplicate / better-path), matching A*.
    - **Backward moves:** use ``problem.predecessors`` (defaults to successors on
      undirected domains such as MVP grids).
    """

    def __init__(
        self,
        heuristic: PairHeuristic[StateT],
        *,
        policies: Optional[PolicyBundle[StateT]] = None,
        metrics_factory: Optional[Callable[[], MetricsCollector]] = None,
    ) -> None:
        self._heuristic = heuristic
        self._policies: PolicyBundle[StateT] = policies or default_policies()  # type: ignore[assignment]
        self._metrics_factory = metrics_factory or MetricsCollector

    def search(
        self,
        problem: SearchProblem[StateT],
        *,
        should_stop: Optional[Callable[[], bool]] = None,
    ) -> SearchResult[StateT]:
        metrics = self._metrics_factory()
        metrics.start()
        metrics.forward_expanded = 0
        metrics.backward_expanded = 0
        metrics.direction_switches = 0
        last_side: Optional[Side] = None
        policies = self._policies

        open_list: LazyHeapOpen[PairKey, SFBDSNode[StateT]] = LazyHeapOpen(
            key_of=lambda n: n.pair_key,
            g_of=lambda n: n.g,
            sort_key_of=policies.tie_break.sort_key,
        )
        closed: ClosedSet[PairKey, SFBDSNode[StateT]] = ClosedSet()

        t0 = time.perf_counter()
        h0 = self._heuristic.evaluate(
            problem.start_state,
            problem.goal_state,
            problem,
            g_F=0.0,
            g_B=0.0,
        )
        metrics.add_heuristic_time(time.perf_counter() - t0)

        root = SFBDSNode(
            forward=problem.start_state,
            backward=problem.goal_state,
            g_F=0.0,
            g_B=0.0,
            h_gap=h0,
        )
        open_list.push(root)
        metrics.note_open_size(open_list.logical_size())

        while not open_list.is_empty():
            if should_stop is not None and should_stop():
                metrics.timed_out = True
                metrics.stale_skipped = open_list.stale_skipped
                snap = metrics.finish(success=False, solution_cost=None)
                return SearchResult(
                    success=False,
                    termination_reason=TerminationReason.TIMEOUT,
                    metrics=snap,
                )

            current = open_list.pop_min()
            if current is None:
                break
            metrics.stale_skipped = open_list.stale_skipped

            if policies.goal.is_goal(current):
                path = reconstruct_sfbds_path(current)
                cost = current.g
                metrics.meeting_g_F = current.g_F
                metrics.meeting_g_B = current.g_B
                snap = metrics.finish(success=True, solution_cost=cost)
                return SearchResult(
                    success=True,
                    termination_reason=TerminationReason.GOAL_FOUND,
                    metrics=snap,
                    solution_cost=cost,
                    path=path,
                )

            if closed.contains(current.pair_key):
                continue

            closed.add(current.pair_key, current)
            metrics.expanded += 1
            metrics.note_closed_size(len(closed))
            # Materialize each side once: BF choice + expansion share the lists.
            fwd_nbrs = list(
                problem.successors(
                    current.forward, forbid_state=current.forbid_forward
                )
            )
            bwd_nbrs = list(
                problem.predecessors(
                    current.backward, forbid_state=current.forbid_backward
                )
            )
            side = policies.direction.choose_by_branch_factors(
                len(fwd_nbrs), len(bwd_nbrs)
            )
            if side is Side.FORWARD:
                metrics.forward_expanded = (metrics.forward_expanded or 0) + 1
            else:
                metrics.backward_expanded = (metrics.backward_expanded or 0) + 1
            if last_side is not None and side is not last_side:
                metrics.direction_switches = (metrics.direction_switches or 0) + 1
            last_side = side
            neighbors = fwd_nbrs if side is Side.FORWARD else bwd_nbrs

            for edge in neighbors:
                metrics.generated += 1
                provisional = self._child_shell(current, side, edge)
                lookup = policies.duplicate.lookup(
                    provisional.pair_key, open_list, closed
                )
                action = policies.better_path.decide(
                    lookup, provisional, policies.reopen
                )
                if action is PathAction.DISCARD:
                    metrics.duplicates_discarded += 1
                    continue

                # PUSH, REPLACE_OPEN, and REOPEN all insert/improve OPEN (lazy).
                t1 = time.perf_counter()
                h_gap = self._heuristic.evaluate(
                    provisional.forward,
                    provisional.backward,
                    problem,
                    g_F=provisional.g_F,
                    g_B=provisional.g_B,
                )
                metrics.add_heuristic_time(time.perf_counter() - t1)
                child = SFBDSNode(
                    forward=provisional.forward,
                    backward=provisional.backward,
                    g_F=provisional.g_F,
                    g_B=provisional.g_B,
                    h_gap=h_gap,
                    parent_F=provisional.parent_F,
                    parent_B=provisional.parent_B,
                )
                self._insert_child(
                    action,
                    child,
                    closed=closed,
                    open_list=open_list,
                    metrics=metrics,
                )

        metrics.stale_skipped = open_list.stale_skipped
        snap = metrics.finish(success=False, solution_cost=None)
        return SearchResult(
            success=False,
            termination_reason=TerminationReason.OPEN_EXHAUSTED,
            metrics=snap,
        )

    def _insert_child(
        self,
        action: PathAction,
        child: SFBDSNode[StateT],
        *,
        closed: ClosedSet[PairKey, SFBDSNode[StateT]],
        open_list: LazyHeapOpen[PairKey, SFBDSNode[StateT]],
        metrics: MetricsCollector,
    ) -> None:
        """Push ``child``; on REOPEN, remove CLOSED first and restore if push fails."""

        closed_victim: Optional[SFBDSNode[StateT]] = None
        if action is PathAction.REOPEN:
            closed_victim = closed.remove(child.pair_key)
        if open_list.push(child):
            metrics.note_open_size(open_list.logical_size())
            return
        if closed_victim is not None:
            closed.add(child.pair_key, closed_victim)
            raise RuntimeError(
                f"REOPEN push rejected for pair {child.pair_key!r}; CLOSED restored"
            )
        metrics.duplicates_discarded += 1

    def _child_shell(
        self,
        node: SFBDSNode[StateT],
        side: Side,
        edge: Successor[StateT],
    ) -> SFBDSNode[StateT]:
        """Build a child with placeholder ``h_gap`` for duplicate / g checks."""

        if side is Side.FORWARD:
            return SFBDSNode(
                forward=edge.state,
                backward=node.backward,
                g_F=node.g_F + edge.cost,
                g_B=node.g_B,
                h_gap=0.0,
                parent_F=node,
                parent_B=node.parent_B,
            )
        return SFBDSNode(
            forward=node.forward,
            backward=edge.state,
            g_F=node.g_F,
            g_B=node.g_B + edge.cost,
            h_gap=0.0,
            parent_F=node.parent_F,
            parent_B=node,
        )


def official_f2e_searcher(
    *,
    metrics_factory: Optional[Callable[[], MetricsCollector]] = None,
) -> SFBDSSearcher:
    """Official SFBDS-F2E: pair lower bound plus better-g CLOSED reopen.

    ``SFBDSSearcher(F2EPairLowerBound())`` uses ``default_policies()``
    (NoReopen) and is **not** official F2E. F2F stays
    ``SFBDSSearcher(F2FManhattanHeuristic())``.
    """

    from sfbds_compare.heuristics.f2e import F2EPairLowerBound
    from sfbds_compare.policies import f2e_policies

    return SFBDSSearcher(
        F2EPairLowerBound(),
        policies=f2e_policies(),
        metrics_factory=metrics_factory,
    )
