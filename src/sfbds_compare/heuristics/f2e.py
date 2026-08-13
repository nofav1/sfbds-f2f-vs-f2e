"""Front-to-end style pair heuristic (project choice for SFBDS-F2E)."""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridState
from sfbds_compare.heuristics.grid_distance import manhattan


class F2EFixedEndpointHeuristic:
    """Project-choice F2E gap using fixed start/goal endpoints.

    h(x, y) = max(|MD(x, G) - MD(y, G)|, |MD(S, x) - MD(S, y)|)

    This is **not** a canonical Felner/Lippi SFBDS-F2E formula; it is the
    team's locked MVP choice derived from fixed-endpoint F2E + consistency.
    """

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
    ) -> float:
        start = problem.start_state
        goal = problem.goal_state
        to_goal = abs(manhattan(forward, goal) - manhattan(backward, goal))
        from_start = abs(manhattan(start, forward) - manhattan(start, backward))
        return float(max(to_goal, from_start))
