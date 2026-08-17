"""Unit tests for F2F / F2E / uni Manhattan heuristics."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2e import F2EPairLowerBound, LegacyFixedEndpointGapHeuristic
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


def test_legacy_f2e_hand_formula() -> None:
    # S=(0,0), G=(4,4); x=(1,0), y=(0,2)
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    x = GridState(1, 0)
    y = GridState(0, 2)
    # |MD(x,G)-MD(y,G)| = |7-6| = 1
    # |MD(S,x)-MD(S,y)| = |1-2| = 1
    assert LegacyFixedEndpointGapHeuristic().evaluate(x, y, problem) == 1.0

    x2 = GridState(0, 3)
    y2 = GridState(3, 0)
    # |MD(x2,G)-MD(y2,G)| = |5-5| = 0
    # |MD(S,x2)-MD(S,y2)| = |3-3| = 0
    assert LegacyFixedEndpointGapHeuristic().evaluate(x2, y2, problem) == 0.0

    x3 = GridState(4, 0)
    y3 = GridState(0, 0)
    # |MD(x3,G)-MD(y3,G)| = |4-8| = 4
    # |MD(S,x3)-MD(S,y3)| = |4-0| = 4
    assert LegacyFixedEndpointGapHeuristic().evaluate(x3, y3, problem) == 4.0


def test_meeting_pair_gap_is_zero() -> None:
    problem = GridProblem(3, 3, GridState(0, 0), GridState(2, 2))
    m = GridState(1, 1)
    g_F, g_B = 2.0, 3.0
    bound = F2EPairLowerBound()
    assert F2FManhattanHeuristic().evaluate(m, m, problem) == 0.0
    assert LegacyFixedEndpointGapHeuristic().evaluate(m, m, problem) == 0.0
    assert bound.lower_bound(m, m, problem, g_F, g_B) == g_F + g_B
    assert bound.evaluate(m, m, problem, g_F=g_F, g_B=g_B) == 0.0


def test_pair_heuristics_nonnegative() -> None:
    problem = GridProblem(4, 4, GridState(0, 0), GridState(3, 3))
    f2f = F2FManhattanHeuristic()
    legacy = LegacyFixedEndpointGapHeuristic()
    official = F2EPairLowerBound()
    for r in range(4):
        for c in range(4):
            x = GridState(r, c)
            for r2 in range(4):
                for c2 in range(4):
                    y = GridState(r2, c2)
                    assert f2f.evaluate(x, y, problem) >= 0.0
                    assert legacy.evaluate(x, y, problem) >= 0.0
                    assert official.evaluate(x, y, problem, g_F=1.0, g_B=2.0) >= 0.0
            assert f2f.evaluate(x, x, problem) == 0.0
            assert legacy.evaluate(x, x, problem) == 0.0
            assert official.evaluate(x, x, problem, g_F=1.0, g_B=2.0) == 0.0


def test_uni_manhattan_uses_goal() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 2))
    assert UniManhattanHeuristic().evaluate(GridState(1, 2), problem) == 3.0


def test_f2e_pair_lower_bound_f_f_dominates() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    u = GridState(0, 0)
    v = GridState(1, 0)
    g_F, g_B = 3.0, 0.0
    f_F = g_F + manhattan(u, problem.goal_state)  # 11
    f_B = g_B + manhattan(problem.start_state, v)  # 1
    gsum_eps = g_F + g_B + 1.0  # 4
    assert f_F > f_B and f_F > gsum_eps
    bound = F2EPairLowerBound()
    lb = bound.lower_bound(u, v, problem, g_F, g_B)
    assert lb == f_F
    assert bound.evaluate(u, v, problem, g_F=g_F, g_B=g_B) == lb - g_F - g_B


def test_f2e_pair_lower_bound_f_b_dominates() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    u = GridState(1, 0)
    v = GridState(4, 4)
    g_F, g_B = 0.0, 3.0
    f_F = g_F + manhattan(u, problem.goal_state)  # 7
    f_B = g_B + manhattan(problem.start_state, v)  # 11
    gsum_eps = g_F + g_B + 1.0  # 4
    assert f_B > f_F and f_B > gsum_eps
    bound = F2EPairLowerBound()
    lb = bound.lower_bound(u, v, problem, g_F, g_B)
    assert lb == f_B
    assert bound.evaluate(u, v, problem, g_F=g_F, g_B=g_B) == lb - g_F - g_B


def test_f2e_pair_lower_bound_gsum_epsilon_dominates() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    u = GridState(4, 3)
    v = GridState(0, 1)
    g_F, g_B = 5.0, 5.0
    f_F = g_F + manhattan(u, problem.goal_state)  # 6
    f_B = g_B + manhattan(problem.start_state, v)  # 6
    gsum_eps = g_F + g_B + 1.0  # 11
    assert gsum_eps > f_F and gsum_eps > f_B
    bound = F2EPairLowerBound()
    lb = bound.lower_bound(u, v, problem, g_F, g_B)
    assert lb == gsum_eps
    assert bound.evaluate(u, v, problem, g_F=g_F, g_B=g_B) == 1.0


def test_f2e_pair_lower_bound_meeting_skips_epsilon() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    m = GridState(2, 2)
    g_F, g_B = 4.0, 4.0
    bound = F2EPairLowerBound()
    assert bound.lower_bound(m, m, problem, g_F, g_B) == g_F + g_B
    assert bound.evaluate(m, m, problem, g_F=g_F, g_B=g_B) == 0.0
