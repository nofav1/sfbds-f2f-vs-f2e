"""Unit tests for generic A* on small grids."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import TerminationReason


def _assert_unit_path(problem: GridProblem, path: list[GridState], cost: float) -> None:
    assert path[0] == problem.start_state
    assert path[-1] == problem.goal_state
    assert cost == len(path) - 1
    for a, b in zip(path, path[1:]):
        assert problem.transition_cost(a, b) == 1.0


def test_astar_start_equals_goal() -> None:
    problem = GridProblem(1, 1, GridState(0, 0), GridState(0, 0))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 0.0
    assert result.path == [GridState(0, 0)]
    assert result.termination_reason == TerminationReason.GOAL_FOUND
    # Late: selecting the goal is not counted as an expansion.
    assert result.metrics.expanded == 0
    assert result.metrics.generated == 0
    assert result.metrics.heuristic_evals == 1


def test_astar_straight_path() -> None:
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 3.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)


def test_astar_with_obstacle() -> None:
    problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(0, 2),
        obstacles=[GridState(0, 1)],
    )
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 4.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)


def test_astar_unreachable_returns_failure_with_metrics() -> None:
    # Vertical wall separates left column from right column.
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(1, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 1), GridState(1, 1), GridState(2, 1)],
    )
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success is False
    assert result.termination_reason == TerminationReason.OPEN_EXHAUSTED
    assert result.solution_cost is None
    # Reachable free cells on the start side: (0,0), (1,0), (2,0).
    assert result.metrics.expanded == 3
    assert result.metrics.success is False


def test_astar_matches_manhattan_on_open_grid() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 3))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 7.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)
