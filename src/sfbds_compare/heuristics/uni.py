"""Unidirectional Manhattan heuristic for grid problems."""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridState
from sfbds_compare.heuristics.grid_distance import manhattan


class UniManhattanHeuristic:
    """h(s) = Manhattan(s, goal) on a 4-connected unit grid."""

    def evaluate(self, state: GridState, problem: SearchProblem[GridState]) -> float:
        return manhattan(state, problem.goal_state)
