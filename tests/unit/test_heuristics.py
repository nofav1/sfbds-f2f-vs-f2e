"""Unit tests for F2F / F2E / uni Manhattan heuristics."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2e import F2EFixedEndpointHeuristic
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.grid_distance import manhattan
from sfbds_compare.heuristics.uni import UniManhattanHeuristic


def test_manhattan_helper() -> None:
    assert manhattan(GridState(0, 0), GridState(0, 0)) == 0.0
    assert manhattan(GridState(0, 0), GridState(0, 3)) == 3.0
    assert manhattan(GridState(1, 2), GridState(4, 5)) == 6.0


def test_f2f_known_pairs() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    h = F2FManhattanHeuristic()
    a = GridState(1, 1)
    b = GridState(1, 4)
    c = GridState(3, 3)
    assert h.evaluate(a, a, problem) == 0.0
    assert h.evaluate(a, b, problem) == 3.0
    assert h.evaluate(a, c, problem) == 4.0


def test_f2e_hand_formula() -> None:
    # S=(0,0), G=(4,4); x=(1,0), y=(0,2)
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    x = GridState(1, 0)
    y = GridState(0, 2)
    # |MD(x,G)-MD(y,G)| = |7-6| = 1
    # |MD(S,x)-MD(S,y)| = |1-2| = 1
    assert F2EFixedEndpointHeuristic().evaluate(x, y, problem) == 1.0

    x2 = GridState(0, 3)
    y2 = GridState(3, 0)
    # |MD(x2,G)-MD(y2,G)| = |5-5| = 0
    # |MD(S,x2)-MD(S,y2)| = |3-3| = 0
    assert F2EFixedEndpointHeuristic().evaluate(x2, y2, problem) == 0.0

    x3 = GridState(4, 0)
    y3 = GridState(0, 0)
    # |MD(x3,G)-MD(y3,G)| = |4-8| = 4
    # |MD(S,x3)-MD(S,y3)| = |4-0| = 4
    assert F2EFixedEndpointHeuristic().evaluate(x3, y3, problem) == 4.0


def test_meeting_pair_gap_is_zero() -> None:
    problem = GridProblem(3, 3, GridState(0, 0), GridState(2, 2))
    m = GridState(1, 1)
    assert F2FManhattanHeuristic().evaluate(m, m, problem) == 0.0
    assert F2EFixedEndpointHeuristic().evaluate(m, m, problem) == 0.0


def test_pair_heuristics_nonnegative() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2f = F2FManhattanHeuristic()
    f2e = F2EFixedEndpointHeuristic()
    for r in range(4):
        for c in range(4):
            x = GridState(r, c)
            for r2 in range(4):
                for c2 in range(4):
                    y = GridState(r2, c2)
                    assert f2f.evaluate(x, y, problem) >= 0.0
                    assert f2e.evaluate(x, y, problem) >= 0.0
            assert f2f.evaluate(x, x, problem) == 0.0
            assert f2e.evaluate(x, x, problem) == 0.0


def test_uni_manhattan_uses_goal() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 2))
    assert UniManhattanHeuristic().evaluate(GridState(1, 2), problem) == 3.0
