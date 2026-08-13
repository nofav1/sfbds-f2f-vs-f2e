"""Unit tests for SFBDSSearcher with F2F / F2E heuristics."""

from __future__ import annotations

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2e import F2EFixedEndpointHeuristic
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher


def _assert_unit_path(
    problem: GridProblem, path: list[GridState], cost: float
) -> None:
    assert path[0] == problem.start_state
    assert path[-1] == problem.goal_state
    assert cost == len(path) - 1
    for a, b in zip(path, path[1:]):
        assert problem.transition_cost(a, b) == 1.0


def _assert_heuristic_eval_aligned(result) -> None:
    """h evals = root + non-discarded generations (A*-aligned accounting)."""
    m = result.metrics
    assert m.heuristic_evals == 1 + (m.generated - m.duplicates_discarded)


def _assert_sfbds_instrumentation(result) -> None:
    m = result.metrics
    assert m.forward_expanded is not None
    assert m.backward_expanded is not None
    assert m.direction_switches is not None
    assert m.forward_expanded + m.backward_expanded == m.expanded
    if result.success:
        assert m.meeting_g_F is not None
        assert m.meeting_g_B is not None
        assert result.solution_cost is not None
        assert m.meeting_g_F + m.meeting_g_B == result.solution_cost
    else:
        assert m.meeting_g_F is None
        assert m.meeting_g_B is None


def _assert_astar_sfbds_fields_na(result) -> None:
    m = result.metrics
    assert m.forward_expanded is None
    assert m.backward_expanded is None
    assert m.meeting_g_F is None
    assert m.meeting_g_B is None
    assert m.direction_switches is None


def test_sfbds_start_equals_goal() -> None:
    problem = GridProblem(1, 1, GridState(0, 0), GridState(0, 0))
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 0.0
    assert result.path == [GridState(0, 0)]
    assert result.termination_reason == TerminationReason.GOAL_FOUND
    assert result.metrics.expanded == 0
    assert result.metrics.heuristic_evals == 1
    _assert_sfbds_instrumentation(result)


def test_sfbds_straight_corridor() -> None:
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 3.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)
    _assert_heuristic_eval_aligned(result)
    _assert_sfbds_instrumentation(result)


def test_sfbds_obstacle_matches_astar() -> None:
    problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(0, 2),
        obstacles=[GridState(0, 1)],
    )
    sfbds = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert sfbds.success and astar.success
    assert sfbds.solution_cost == astar.solution_cost == 4.0
    assert sfbds.path is not None
    _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
    _assert_heuristic_eval_aligned(sfbds)
    _assert_sfbds_instrumentation(sfbds)
    _assert_astar_sfbds_fields_na(astar)


@pytest.mark.parametrize(
    ("height", "width", "start", "goal"),
    [
        (1, 4, GridState(0, 0), GridState(0, 3)),
        (5, 5, GridState(0, 0), GridState(4, 3)),
        (3, 3, GridState(0, 0), GridState(2, 2)),
        (2, 3, GridState(0, 0), GridState(0, 2)),
    ],
)
def test_sfbds_f2f_cost_agrees_with_astar_open_grids(
    height: int, width: int, start: GridState, goal: GridState
) -> None:
    problem = GridProblem(height, width, start, goal)
    sfbds = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert sfbds.success and astar.success
    assert sfbds.solution_cost == astar.solution_cost
    assert sfbds.path is not None
    _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
    _assert_heuristic_eval_aligned(sfbds)
    _assert_sfbds_instrumentation(sfbds)
    _assert_astar_sfbds_fields_na(astar)


def test_sfbds_f2e_cost_agrees_with_astar_open_and_obstacle() -> None:
    open_problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 3))
    obstacle_problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(0, 2),
        obstacles=[GridState(0, 1)],
    )
    for problem in (open_problem, obstacle_problem):
        sfbds = SFBDSSearcher(F2EFixedEndpointHeuristic()).search(problem)
        astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
        assert sfbds.success and astar.success
        assert sfbds.solution_cost == astar.solution_cost
        assert sfbds.path is not None
        _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
        _assert_heuristic_eval_aligned(sfbds)
        _assert_sfbds_instrumentation(sfbds)
        _assert_astar_sfbds_fields_na(astar)


def test_sfbds_unreachable_open_exhausted() -> None:
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(1, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 1), GridState(1, 1), GridState(2, 1)],
    )
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success is False
    assert result.termination_reason == TerminationReason.OPEN_EXHAUSTED
    assert result.solution_cost is None
    assert result.metrics.expanded >= 1
    assert result.metrics.success is False
    _assert_heuristic_eval_aligned(result)
    _assert_sfbds_instrumentation(result)
