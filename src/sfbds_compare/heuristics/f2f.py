"""Front-to-front Manhattan gap heuristic for SFBDS."""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridState
from sfbds_compare.heuristics.grid_distance import manhattan


class F2FManhattanHeuristic:
    """h_F2F(x, y) = Manhattan(x, y) on a 4-connected unit grid."""

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: SearchProblem[GridState],
    ) -> float:
        return manhattan(forward, backward)
