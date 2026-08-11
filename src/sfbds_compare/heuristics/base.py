"""Heuristic strategy interfaces."""

from __future__ import annotations

from typing import Hashable, Protocol, TypeVar

from sfbds_compare.domain.base import SearchProblem

StateT = TypeVar("StateT", bound=Hashable)


class UniHeuristic(Protocol[StateT]):
    """Unidirectional heuristic: estimate cost from a state to the goal."""

    def evaluate(self, state: StateT, problem: SearchProblem[StateT]) -> float: ...


class PairHeuristic(Protocol[StateT]):
    """Pair / gap heuristic used by SFBDS: estimate remaining cost between two states."""

    def evaluate(
        self,
        forward: StateT,
        backward: StateT,
        problem: SearchProblem[StateT],
    ) -> float: ...
