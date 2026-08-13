"""Generic SFBDS over SearchProblem (Late goal, injectable policies)."""

from __future__ import annotations

import time
from typing import Callable, Generic, Hashable, Optional, TypeVar

from sfbds_compare.domain.base import SearchProblem
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

    Metric conventions (aligned with A* MVP):
    - **Late:** goal when selected from OPEN (``forward == backward``); that
      selection is **not** counted in ``expanded``.
    - **Parent suppression:** children use ``forbid_forward`` / ``forbid_backward``.
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

    def search(self, problem: SearchProblem[StateT]) -> SearchResult[StateT]:
        metrics = self._metrics_factory()
        metrics.start()
        policies = self._policies

        open_list: LazyHeapOpen[PairKey, SFBDSNode[StateT]] = LazyHeapOpen(
            key_of=lambda n: n.pair_key,
            g_of=lambda n: n.g,
            sort_key_of=policies.tie_break.sort_key,
        )
        closed: ClosedSet[PairKey, SFBDSNode[StateT]] = ClosedSet()

        t0 = time.perf_counter()
        h0 = self._heuristic.evaluate(
            problem.start_state, problem.goal_state, problem
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
            current = open_list.pop_min()
            if current is None:
                break
            metrics.stale_skipped = open_list.stale_skipped

            if policies.goal.is_goal(current):
                path = reconstruct_sfbds_path(current)
                cost = current.g
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

            side = policies.direction.choose(current, problem)
            for child in self._generate_children(current, side, problem, metrics):
                lookup = policies.duplicate.lookup(
                    child.pair_key, open_list, closed
                )
                action = policies.better_path.decide(
                    lookup, child, policies.reopen
                )
                if action is PathAction.DISCARD:
                    metrics.duplicates_discarded += 1
                    continue
                # PUSH and REPLACE_OPEN both improve-or-insert via lazy OPEN.
                if open_list.push(child):
                    metrics.note_open_size(open_list.logical_size())
                else:
                    metrics.duplicates_discarded += 1

        metrics.stale_skipped = open_list.stale_skipped
        snap = metrics.finish(success=False, solution_cost=None)
        return SearchResult(
            success=False,
            termination_reason=TerminationReason.OPEN_EXHAUSTED,
            metrics=snap,
        )

    def _generate_children(
        self,
        node: SFBDSNode[StateT],
        side: Side,
        problem: SearchProblem[StateT],
        metrics: MetricsCollector,
    ) -> list[SFBDSNode[StateT]]:
        children: list[SFBDSNode[StateT]] = []
        if side is Side.FORWARD:
            for succ in problem.successors(
                node.forward, forbid_state=node.forbid_forward
            ):
                metrics.generated += 1
                t1 = time.perf_counter()
                h_gap = self._heuristic.evaluate(
                    succ.state, node.backward, problem
                )
                metrics.add_heuristic_time(time.perf_counter() - t1)
                children.append(
                    SFBDSNode(
                        forward=succ.state,
                        backward=node.backward,
                        g_F=node.g_F + succ.cost,
                        g_B=node.g_B,
                        h_gap=h_gap,
                        parent_F=node,
                        parent_B=node.parent_B,
                    )
                )
        else:
            for succ in problem.successors(
                node.backward, forbid_state=node.forbid_backward
            ):
                metrics.generated += 1
                t1 = time.perf_counter()
                h_gap = self._heuristic.evaluate(
                    node.forward, succ.state, problem
                )
                metrics.add_heuristic_time(time.perf_counter() - t1)
                children.append(
                    SFBDSNode(
                        forward=node.forward,
                        backward=succ.state,
                        g_F=node.g_F,
                        g_B=node.g_B + succ.cost,
                        h_gap=h_gap,
                        parent_F=node.parent_F,
                        parent_B=node,
                    )
                )
        return children
