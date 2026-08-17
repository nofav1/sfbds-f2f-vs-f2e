"""Heuristic strategy interfaces."""

from __future__ import annotations

from typing import Hashable, Protocol, TypeVar

from sfbds_compare.domain.base import SearchProblem

StateT = TypeVar("StateT", bound=Hashable)


class UniHeuristic(Protocol[StateT]):
    """Unidirectional heuristic: estimate cost from a state to the goal."""

    def evaluate(self, state: StateT, problem: SearchProblem[StateT]) -> float: ...


class PairHeuristic(Protocol[StateT]):
    """Pair remaining-cost heuristic used by SFBDS OPEN (`h_gap`).

    ``g_F`` / ``g_B`` are the path costs already spent on each side. Gap
    heuristics may ignore them; pair lower-bound evaluators use them and
    return remaining cost ``max(0, lb − g_F − g_B)``.
    """

    def evaluate(
        self,
        forward: StateT,
        backward: StateT,
        problem: SearchProblem[StateT],
        g_F: float = 0.0,
        g_B: float = 0.0,
    ) -> float: ...


class PairLowerBound(Protocol[StateT]):
    """Lower bound on solution cost through a pair (not remaining cost)."""

    def lower_bound(
        self,
        forward: StateT,
        backward: StateT,
        problem: SearchProblem[StateT],
        g_F: float,
        g_B: float,
    ) -> float: ...
