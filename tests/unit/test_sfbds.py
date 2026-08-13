"""Smoke unit tests for SFBDSSearcher (test-local pair heuristic)."""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.search.result import TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher


class _ManhattanGapHeuristic:
    """Test-local F2F-style gap: Manhattan between pair endpoints."""

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
    ) -> float:
        return float(
            abs(forward.row - backward.row) + abs(forward.col - backward.col)
        )


def _assert_unit_path(
    problem: GridProblem, path: list[GridState], cost: float
) -> None:
    assert path[0] == problem.start_state
    assert path[-1] == problem.goal_state
    assert cost == len(path) - 1
    for a, b in zip(path, path[1:]):
        assert problem.transition_cost(a, b) == 1.0


def test_sfbds_start_equals_goal() -> None:
    problem = GridProblem(1, 1, GridState(0, 0), GridState(0, 0))
    result = SFBDSSearcher(_ManhattanGapHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 0.0
    assert result.path == [GridState(0, 0)]
    assert result.termination_reason == TerminationReason.GOAL_FOUND
    assert result.metrics.expanded == 0


def test_sfbds_straight_corridor() -> None:
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    result = SFBDSSearcher(_ManhattanGapHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 3.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)


def test_sfbds_unreachable_open_exhausted() -> None:
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(1, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 1), GridState(1, 1), GridState(2, 1)],
    )
    result = SFBDSSearcher(_ManhattanGapHeuristic()).search(problem)
    assert result.success is False
    assert result.termination_reason == TerminationReason.OPEN_EXHAUSTED
    assert result.solution_cost is None
    assert result.metrics.expanded >= 1
    assert result.metrics.success is False
