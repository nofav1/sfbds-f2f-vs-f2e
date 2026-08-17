"""Front-to-end pair evaluation for SFBDS.

Official ``sfbds_f2e`` is :class:`F2EPairLowerBound` (solution-cost bound
through the pair). :class:`LegacyFixedEndpointGapHeuristic` is the former
project-choice gap, kept for tests only.
"""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridState
from sfbds_compare.heuristics.grid_distance import manhattan

_EPSILON = 1.0


class LegacyFixedEndpointGapHeuristic:
    """Former project-choice F2E gap using fixed start/goal endpoints.

    h(x, y) = max(|MD(x, G) - MD(y, G)|, |MD(S, x) - MD(S, y)|)

    This is **not** the official SFBDS-F2E pair bound. Existing study CSVs
    used this formula; treat those rows as legacy.
    """

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
        g_F: float = 0.0,
        g_B: float = 0.0,
    ) -> float:
        del g_F, g_B
        start = problem.start_state
        goal = problem.goal_state
        to_goal = abs(manhattan(forward, goal) - manhattan(backward, goal))
        from_start = abs(manhattan(start, forward) - manhattan(start, backward))
        return float(max(to_goal, from_start))


class F2EPairLowerBound:
    """NBS-style pair lower bound for SFBDS-F2E on 4-connected unit grids.

    Front-to-end heuristics: ``h_F(u) = MD(u, goal)``, ``h_B(v) = MD(start, v)``.

    Source of truth (``lower_bound``), unit grids, ``epsilon = 1``:

        if u == v:  lb = g_F + g_B
        else:       lb = max(g_F + MD(u, G), g_B + MD(S, v), g_F + g_B + 1)

    ``evaluate`` is the remaining-cost adapter for ``SFBDSNode.f = g + h_gap``:

        h_gap = max(0, lb − g_F − g_B)
    """

    def lower_bound(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
        g_F: float,
        g_B: float,
    ) -> float:
        gsum = g_F + g_B
        if forward == backward:
            return float(gsum)
        start = problem.start_state
        goal = problem.goal_state
        f_F = g_F + manhattan(forward, goal)
        f_B = g_B + manhattan(start, backward)
        return float(max(f_F, f_B, gsum + _EPSILON))

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
        g_F: float = 0.0,
        g_B: float = 0.0,
    ) -> float:
        lb = self.lower_bound(forward, backward, problem, g_F, g_B)
        return max(0.0, lb - g_F - g_B)
