"""Unit tests for GridProblem and parent-state suppression."""

from __future__ import annotations

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState


def _open_3x3() -> GridProblem:
    return GridProblem(
        height=3,
        width=3,
        start=GridState(0, 0),
        goal=GridState(2, 2),
        obstacles=(),
    )


def test_grid_state_is_hashable_and_ordered() -> None:
    a = GridState(1, 2)
    b = GridState(1, 2)
    c = GridState(0, 0)
    assert a == b
    assert hash(a) == hash(b)
    assert {a, b, c} == {a, c}
    assert c < a


def test_corner_has_two_successors() -> None:
    problem = _open_3x3()
    start = problem.start_state
    succs = list(problem.successors(start))
    assert {s.state for s in succs} == {GridState(0, 1), GridState(1, 0)}
    assert all(s.cost == 1.0 for s in succs)
    assert problem.branch_factor(start) == 2


def test_center_has_four_successors() -> None:
    problem = _open_3x3()
    center = GridState(1, 1)
    succs = list(problem.successors(center))
    assert len(succs) == 4
    assert problem.branch_factor(center) == 4


def test_obstacles_block_successors() -> None:
    blocked = GridState(0, 1)
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(0, 0),
        goal=GridState(2, 2),
        obstacles=[blocked],
    )
    succs = list(problem.successors(GridState(0, 0)))
    assert {s.state for s in succs} == {GridState(1, 0)}
    assert problem.branch_factor(GridState(0, 0)) == 1


def test_forbid_state_suppresses_parent() -> None:
    problem = _open_3x3()
    current = GridState(1, 0)
    parent = GridState(0, 0)
    without = {s.state for s in problem.successors(current)}
    with_forbid = {
        s.state for s in problem.successors(current, forbid_state=parent)
    }
    assert parent in without
    assert parent not in with_forbid
    assert problem.branch_factor(current, forbid_state=parent) == len(with_forbid)
    assert problem.branch_factor(current, forbid_state=parent) == (
        problem.branch_factor(current) - 1
    )


def test_forbid_state_matches_expansion_for_bf() -> None:
    """BF must count the same set expansion would generate."""
    problem = _open_3x3()
    state = GridState(1, 1)
    parent = GridState(1, 0)
    generated = list(problem.successors(state, forbid_state=parent))
    assert problem.branch_factor(state, forbid_state=parent) == len(generated)
    assert all(s.state != parent for s in generated)


def test_transition_cost_unit_adjacent() -> None:
    problem = _open_3x3()
    assert problem.transition_cost(GridState(0, 0), GridState(0, 1)) == 1.0


def test_transition_cost_rejects_non_adjacent() -> None:
    problem = _open_3x3()
    with pytest.raises(ValueError):
        problem.transition_cost(GridState(0, 0), GridState(1, 1))


def test_invalid_start_raises() -> None:
    with pytest.raises(ValueError):
        GridProblem(
            height=2,
            width=2,
            start=GridState(0, 0),
            goal=GridState(1, 1),
            obstacles=[GridState(0, 0)],
        )


def test_is_goal() -> None:
    problem = _open_3x3()
    assert problem.is_goal(GridState(2, 2))
    assert not problem.is_goal(GridState(0, 0))


def test_describe_metadata() -> None:
    problem = _open_3x3()
    meta = problem.describe()
    assert meta["problem_type"] == "grid"
    assert meta["height"] == 3
    assert meta["width"] == 3
