"""Unit tests for experiment map generators and connected sampling."""

from __future__ import annotations

import random

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.generators import (
    endpoints_connected,
    ensure_connected_query,
)


def test_ensure_connected_query_relocates_across_wall() -> None:
    obstacles = [GridState(0, 1), GridState(1, 1), GridState(2, 1)]
    problem = GridProblem(
        3, 3, GridState(0, 0), GridState(0, 2), obstacles=obstacles
    )
    assert not endpoints_connected(problem)
    fixed = ensure_connected_query(
        problem, min_manhattan=1, rng=random.Random(0)
    )
    assert endpoints_connected(fixed)
    assert fixed.obstacles == problem.obstacles
    assert fixed.start_state != fixed.goal_state


def test_ensure_connected_query_keeps_already_connected() -> None:
    problem = GridProblem(3, 3, GridState(0, 0), GridState(2, 2))
    assert endpoints_connected(problem)
    same = ensure_connected_query(
        problem, min_manhattan=2, rng=random.Random(1)
    )
    assert same is problem
