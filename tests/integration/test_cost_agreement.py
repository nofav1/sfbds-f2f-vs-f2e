"""Integration: A* vs SFBDS-F2F vs SFBDS-F2E cost and path agreement."""

from __future__ import annotations

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import GeneratorConfig, QuerySpec
from sfbds_compare.experiments.generators import build_problem
from sfbds_compare.heuristics.f2e import F2EPairLowerBound
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.sfbds import SFBDSSearcher


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
    f2e = SFBDSSearcher(F2EPairLowerBound()).search(problem)

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
