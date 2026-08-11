"""Unit tests for generic A* on small grids."""

from __future__ import annotations

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import TerminationReason


def test_astar_start_equals_goal() -> None:
    problem = GridProblem(1, 1, GridState(0, 0), GridState(0, 0))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 0.0
    assert result.path == [GridState(0, 0)]
    assert result.termination_reason == TerminationReason.GOAL_FOUND


def test_astar_straight_path() -> None:
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 3.0
    assert result.path is not None
    assert result.path[0] == GridState(0, 0)
    assert result.path[-1] == GridState(0, 3)


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
    assert result.metrics.expanded >= 1
    assert result.metrics.success is False


def test_astar_matches_manhattan_on_open_grid() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 3))
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 7.0
