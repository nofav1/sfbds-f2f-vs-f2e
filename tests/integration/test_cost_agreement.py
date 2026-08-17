"""Integration: A* vs SFBDS-F2F vs SFBDS-F2E cost and path agreement."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any
from unittest.mock import patch

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import GeneratorConfig, QuerySpec, load_config
from sfbds_compare.experiments.generators import build_problem, map_fingerprint
from sfbds_compare.experiments.runner import _problems_for_query
from sfbds_compare.heuristics.f2e import F2EPairLowerBound
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.policies import default_policies, f2e_policies
from sfbds_compare.policies.types import DuplicateLocation, PathAction
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.nodes import SFBDSNode
from sfbds_compare.search.sfbds import SFBDSSearcher, official_f2e_searcher
from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import LazyHeapOpen

_Q20_ANCESTOR_KEY = (GridState(47, 35), GridState(57, 51))

# Pre-fix pair-bound cost_mismatch identities (not 12 query indexes).
FROZEN_COST_MISMATCH_ROWS: tuple[tuple[str, int, int, str], ...] = (
    ("study_random_128", 0, 4915, "b9a804c74171c449"),
    ("study_random_128", 8, 1638, "e64f85a15a867d66"),
    ("study_random_128", 8, 3276, "16c51c48e712f4ae"),
    ("study_random_128", 16, 3276, "e640a4ed25699ddc"),
    ("study_random_128", 23, 4915, "37c3b17c769dca9d"),
    ("study_random_128", 29, 4915, "51f66cb11ee8cf38"),
    ("study_random_64", 6, 819, "796c91331fd628f9"),
    ("study_random_64", 6, 1228, "36e0ac6e1f777935"),
    ("study_random_64", 9, 1228, "7740aa61f8e92fee"),
    ("study_random_64", 20, 819, "130ce1129eacbddc"),
    ("study_random_64", 20, 1228, "d604ed0b69115ce9"),
    ("study_random_64", 22, 1228, "aca0ecc8b3f56cfa"),
)


@dataclass
class _SFBDSTrace:
    generated: list[SFBDSNode[Any]] = field(default_factory=list)
    pushed: list[SFBDSNode[Any]] = field(default_factory=list)
    expanded: list[SFBDSNode[Any]] = field(default_factory=list)
    closed_better_g_discards: list[tuple[SFBDSNode[Any], SFBDSNode[Any]]] = field(
        default_factory=list
    )
    closed_better_g_reopens: list[tuple[SFBDSNode[Any], SFBDSNode[Any]]] = field(
        default_factory=list
    )
    meetings_generated: list[SFBDSNode[Any]] = field(default_factory=list)
    selected_meeting: SFBDSNode[Any] | None = None
    min_open_f_at_goal: float | None = None
    min_open_lb_at_goal: float | None = None
    remaining_open_at_goal: list[SFBDSNode[Any]] = field(default_factory=list)


class _TracingBetterPath:
    def __init__(self, inner: Any, trace: _SFBDSTrace) -> None:
        self._inner = inner
        self._trace = trace

    def decide(self, lookup: Any, candidate: SFBDSNode[Any], reopen: Any) -> PathAction:
        self._trace.generated.append(candidate)
        if candidate.forward == candidate.backward:
            self._trace.meetings_generated.append(candidate)
        action = self._inner.decide(lookup, candidate, reopen)
        if (
            action is PathAction.DISCARD
            and lookup.location is DuplicateLocation.CLOSED
            and lookup.existing is not None
            and candidate.g < lookup.existing.g
        ):
            self._trace.closed_better_g_discards.append((lookup.existing, candidate))
        if action is PathAction.REOPEN and lookup.existing is not None:
            self._trace.closed_better_g_reopens.append((lookup.existing, candidate))
        if action is not PathAction.DISCARD:
            self._trace.pushed.append(candidate)
        return action


def _trace_sfbds(problem: GridProblem, heuristic: Any, policies: Any):
    """Search with generated / pushed / expanded / CLOSED better-g traces."""

    trace = _SFBDSTrace()
    wrapped = replace(policies, better_path=_TracingBetterPath(policies.better_path, trace))

    class TracingClosed(ClosedSet):
        def add(self, key, node):  # type: ignore[no-untyped-def]
            trace.expanded.append(node)
            super().add(key, node)

    class TracingOpen(LazyHeapOpen):
        def pop_min(self):  # type: ignore[no-untyped-def]
            node = super().pop_min()
            if node is not None and node.forward == node.backward:
                trace.selected_meeting = node
                remaining = list(self._best.values())
                trace.remaining_open_at_goal = remaining
                if remaining:
                    trace.min_open_f_at_goal = min(n.f for n in remaining)
                    trace.min_open_lb_at_goal = min(n.g + n.h_gap for n in remaining)
            return node

    with (
        patch("sfbds_compare.search.sfbds.ClosedSet", TracingClosed),
        patch("sfbds_compare.search.sfbds.LazyHeapOpen", TracingOpen),
    ):
        result = SFBDSSearcher(heuristic, policies=wrapped).search(problem)
    return result, trace


def _late_stop_diagnostics(ident: tuple, astar_cost: float, result: Any, trace: _SFBDSTrace) -> str:
    generated_gs = sorted({n.g for n in trace.meetings_generated})
    cheaper_generated = [
        n.g
        for n in trace.meetings_generated
        if result.solution_cost is not None and n.g < result.solution_cost
    ]
    open_meetings = [n.g for n in trace.remaining_open_at_goal if n.forward == n.backward]
    selected_g = trace.selected_meeting.g if trace.selected_meeting is not None else None
    return (
        f"{ident}: F2E={result.solution_cost} A*={astar_cost}; "
        f"first selected meeting g={selected_g}; "
        f"generated meeting gs={generated_gs}; "
        f"cheaper generated meetings={cheaper_generated}; "
        f"min OPEN f at stop={trace.min_open_f_at_goal}; "
        f"min OPEN g+h_gap at stop={trace.min_open_lb_at_goal}; "
        f"OPEN meeting gs at stop={open_meetings}; "
        f"better-g reopens={len(trace.closed_better_g_reopens)}; "
        f"better-g CLOSED discards={len(trace.closed_better_g_discards)}"
    )


def _search_f2e(problem: GridProblem):
    return official_f2e_searcher().search(problem)


def _assert_unit_path(
    problem: GridProblem, path: list[GridState], cost: float
) -> None:
    assert path[0] == problem.start_state
    assert path[-1] == problem.goal_state
    assert cost == float(len(path) - 1)
    for a, b in zip(path, path[1:]):
        assert problem.transition_cost(a, b) == 1.0


def _assert_sfbds_h_evals(result) -> None:
    m = result.metrics
    assert m.heuristic_evals == 1 + (m.generated - m.duplicates_discarded)


def _run_three_way(problem: GridProblem) -> None:
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    f2f = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    f2e = _search_f2e(problem)

    assert astar.success and f2f.success and f2e.success
    assert astar.solution_cost == f2f.solution_cost == f2e.solution_cost
    assert astar.path is not None and f2f.path is not None and f2e.path is not None
    cost = astar.solution_cost
    assert cost is not None
    _assert_unit_path(problem, list(astar.path), cost)
    _assert_unit_path(problem, list(f2f.path), cost)
    _assert_unit_path(problem, list(f2e.path), cost)
    _assert_sfbds_h_evals(f2f)
    _assert_sfbds_h_evals(f2e)


@pytest.mark.parametrize(
    "problem",
    [
        GridProblem(1, 1, GridState(0, 0), GridState(0, 0)),
        GridProblem(1, 4, GridState(0, 0), GridState(0, 3)),
        GridProblem(5, 5, GridState(0, 0), GridState(4, 3)),
        GridProblem(3, 3, GridState(0, 0), GridState(2, 2)),
        GridProblem(
            height=2,
            width=3,
            start=GridState(0, 0),
            goal=GridState(0, 2),
            obstacles=[GridState(0, 1)],
        ),
        GridProblem(
            height=4,
            width=4,
            start=GridState(0, 0),
            goal=GridState(3, 3),
            obstacles=[GridState(1, 1), GridState(2, 2)],
        ),
    ],
    ids=[
        "start_eq_goal",
        "corridor",
        "open_5x5",
        "open_3x3",
        "obstacle_detour",
        "obstacle_diagonal_blocks",
    ],
)
def test_three_way_cost_and_path_agreement(problem: GridProblem) -> None:
    _run_three_way(problem)


def test_three_way_cost_agreement_on_small_maze() -> None:
    problem = build_problem(
        GeneratorConfig(kind="maze", height=7, width=7),
        QuerySpec(start=(0, 0), goal=(6, 6)),
        seed=11,
    )
    _run_three_way(problem)


def _study_random_64_q20_d1228() -> GridProblem:
    cfg = load_config("configs/study/study_random_64.yaml")
    problems = _problems_for_query(cfg, cfg.queries[20], 20)
    problem = next(p for p in problems if len(p.obstacles) == 1228)
    assert (
        map_fingerprint(problem, generator=cfg.generator, seed=cfg.seed)
        == "d604ed0b69115ce9"
    )
    return problem


def _problem_for_frozen_row(
    experiment: str, query_index: int, obstacle_count: int, map_hash: str
) -> GridProblem:
    cfg = load_config(f"configs/study/{experiment}.yaml")
    problems = _problems_for_query(cfg, cfg.queries[query_index], query_index)
    problem = next(p for p in problems if len(p.obstacles) == obstacle_count)
    assert (
        map_fingerprint(problem, generator=cfg.generator, seed=cfg.seed + query_index)
        == map_hash
    )
    return problem


def test_q20_noreopen_diagnosis_facts() -> None:
    """Replay q=20 under NoReopen: locks demonstrated duplicate-key facts.

    Do not lock F2E solution cost 57. Official F2E uses official_f2e_searcher().
    """

    problem = _study_random_64_q20_d1228()
    f2f_result, f2f_trace = _trace_sfbds(
        problem, F2FManhattanHeuristic(), default_policies()
    )
    f2e_result, f2e_trace = _trace_sfbds(
        problem, F2EPairLowerBound(), default_policies()
    )
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert astar.success and f2f_result.success and f2e_result.success
    assert astar.solution_cost == 53.0
    assert f2f_result.solution_cost == astar.solution_cost
    assert f2f_trace.closed_better_g_discards == []
    assert f2f_trace.closed_better_g_reopens == []

    ancestor_expands = [
        n.g for n in f2e_trace.expanded if n.pair_key == _Q20_ANCESTOR_KEY
    ]
    assert ancestor_expands
    assert ancestor_expands[0] == 29.0

    discards_27 = [
        (existing.g, cand.g)
        for existing, cand in f2e_trace.closed_better_g_discards
        if cand.pair_key == _Q20_ANCESTOR_KEY and cand.g == 27.0
    ]
    assert discards_27
    assert discards_27[0] == (29.0, 27.0)

    f2f_g = next(n.g for n in f2f_trace.expanded if n.pair_key == _Q20_ANCESTOR_KEY)
    assert f2f_g == 27.0
    assert discards_27[0][1] == f2f_g

    assert not any(
        n.forward == n.backward and n.g == 53.0 for n in f2e_trace.meetings_generated
    )


def test_f2f_q20_stays_noreopen() -> None:
    from sfbds_compare.policies.reopen import BetterGReopenPolicy, NoReopenPolicy

    problem = _study_random_64_q20_d1228()
    _result, trace = _trace_sfbds(problem, F2FManhattanHeuristic(), default_policies())
    assert trace.closed_better_g_discards == []
    assert trace.closed_better_g_reopens == []
    assert isinstance(default_policies().reopen, NoReopenPolicy)
    assert isinstance(f2e_policies().reopen, BetterGReopenPolicy)


def test_f2e_q20_reopens_and_expands_better_g() -> None:
    problem = _study_random_64_q20_d1228()
    result, trace = _trace_sfbds(problem, F2EPairLowerBound(), f2e_policies())
    reopened_27 = [
        (existing.g, cand.g)
        for existing, cand in trace.closed_better_g_reopens
        if cand.pair_key == _Q20_ANCESTOR_KEY and cand.g == 27.0
    ]
    assert reopened_27
    assert reopened_27[0][0] == 29.0
    assert any(
        n.pair_key == _Q20_ANCESTOR_KEY and n.g == 27.0 for n in trace.expanded
    )
    assert result.success
    assert result.solution_cost == 53.0
    assert result.metrics.meeting_g_F is not None
    assert result.metrics.meeting_g_B is not None
    assert (
        result.metrics.meeting_g_F + result.metrics.meeting_g_B == result.solution_cost
    )
    assert trace.selected_meeting is not None
    assert trace.selected_meeting.h_gap == 0.0


def test_f2e_matches_astar_on_study_random_64_q20_d1228() -> None:
    problem = _study_random_64_q20_d1228()
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    f2e = _search_f2e(problem)
    assert astar.success and f2e.success
    assert astar.solution_cost == 53.0
    assert f2e.solution_cost == astar.solution_cost


@pytest.mark.parametrize(
    ("experiment", "query_index", "obstacle_count", "map_hash"),
    FROZEN_COST_MISMATCH_ROWS,
    ids=[
        f"{exp}-q{q}-d{obs}-{h[:8]}"
        for exp, q, obs, h in FROZEN_COST_MISMATCH_ROWS
    ],
)
def test_f2e_matches_astar_on_frozen_mismatch_row(
    experiment: str, query_index: int, obstacle_count: int, map_hash: str
) -> None:
    ident = (experiment, query_index, obstacle_count, map_hash)
    problem = _problem_for_frozen_row(*ident)
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    result, trace = _trace_sfbds(problem, F2EPairLowerBound(), f2e_policies())
    assert astar.success and result.success
    if result.solution_cost != astar.solution_cost:
        pytest.fail(
            _late_stop_diagnostics(ident, astar.solution_cost or float("nan"), result, trace)
        )
