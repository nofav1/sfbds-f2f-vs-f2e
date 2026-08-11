"""Unidirectional Manhattan heuristic for grid problems."""

from __future__ import annotations

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridState


class UniManhattanHeuristic:
    """h(s) = Manhattan(s, goal) on a 4-connected unit grid."""

    def evaluate(self, state: GridState, problem: SearchProblem[GridState]) -> float:
        goal = problem.goal_state
        return float(abs(state.row - goal.row) + abs(state.col - goal.col))
