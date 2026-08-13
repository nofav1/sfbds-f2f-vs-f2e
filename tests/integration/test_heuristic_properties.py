"""Integration: F2F/F2E admissibility and pair-edge consistency on open grids."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2e import F2EFixedEndpointHeuristic
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.grid_distance import manhattan


def _free_cells(problem: GridProblem) -> list[GridState]:
    cells: list[GridState] = []
    for r in range(problem.height):
        for c in range(problem.width):
            s = GridState(r, c)
            if problem.is_free(s):
                cells.append(s)
    return cells


def _unit_neighbors(problem: GridProblem, state: GridState) -> list[GridState]:
    return [s.state for s in problem.successors(state)]


def test_f2f_f2e_nonnegative_and_zero_on_meeting() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2f = F2FManhattanHeuristic()
    f2e = F2EFixedEndpointHeuristic()
    for x in _free_cells(problem):
        assert f2f.evaluate(x, x, problem) == 0.0
        assert f2e.evaluate(x, x, problem) == 0.0
        for y in _free_cells(problem):
            assert f2f.evaluate(x, y, problem) >= 0.0
            assert f2e.evaluate(x, y, problem) >= 0.0


def test_f2f_equals_manhattan_on_open_grid() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2f = F2FManhattanHeuristic()
    for x in _free_cells(problem):
        for y in _free_cells(problem):
            assert f2f.evaluate(x, y, problem) == manhattan(x, y)


def test_f2e_admissible_vs_manhattan_on_open_grid() -> None:
    """On obstacle-free grids, F2E gap is at most MD(x, y)."""
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2e = F2EFixedEndpointHeuristic()
    for x in _free_cells(problem):
        for y in _free_cells(problem):
            assert f2e.evaluate(x, y, problem) <= manhattan(x, y)


def test_f2f_unit_step_lipschitz() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2f = F2FManhattanHeuristic()
    for x in _free_cells(problem):
        for y in _free_cells(problem):
            h0 = f2f.evaluate(x, y, problem)
            for xp in _unit_neighbors(problem, x):
                assert abs(f2f.evaluate(xp, y, problem) - h0) <= 1.0
            for yp in _unit_neighbors(problem, y):
                assert abs(f2f.evaluate(x, yp, problem) - h0) <= 1.0


def test_f2e_unit_step_lipschitz() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2e = F2EFixedEndpointHeuristic()
    for x in _free_cells(problem):
        for y in _free_cells(problem):
            h0 = f2e.evaluate(x, y, problem)
            for xp in _unit_neighbors(problem, x):
                assert abs(f2e.evaluate(xp, y, problem) - h0) <= 1.0
            for yp in _unit_neighbors(problem, y):
                assert abs(f2e.evaluate(x, yp, problem) - h0) <= 1.0
