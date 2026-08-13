"""Generic search-problem abstractions (domain-independent)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, Hashable, Iterable, Optional, TypeVar

StateT = TypeVar("StateT", bound=Hashable)


@dataclass(frozen=True, slots=True)
class TransitionMeta:
    """Optional metadata for a generated transition.

    Domains may leave ``operator_id`` unset. Search algorithms must not assume
    grid-specific directions; parent suppression uses ``forbid_state`` instead.
    """

    operator_id: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Successor(Generic[StateT]):
    """One outgoing transition from a state."""

    state: StateT
    cost: float
    meta: TransitionMeta = TransitionMeta()


class SearchProblem(ABC, Generic[StateT]):
    """Abstract single-source / single-goal graph search problem.

    Implementations must provide hashable states. Parent-operator suppression is
    expressed by passing ``forbid_state`` into :meth:`successors` so branching
    factor and expansion agree without hard-coding reverse operators in search.
    """

    @property
    @abstractmethod
    def start_state(self) -> StateT:
        """Start state of the instance."""

    @property
    @abstractmethod
    def goal_state(self) -> StateT:
        """Goal state of the instance."""

    @abstractmethod
    def successors(
        self,
        state: StateT,
        *,
        forbid_state: Optional[StateT] = None,
    ) -> Iterable[Successor[StateT]]:
        """Yield legal successors of ``state``.

        If ``forbid_state`` is not ``None``, that neighbor must not be yielded.
        This is the generic parent-reversal suppression hook.
        """

    def predecessors(
        self,
        state: StateT,
        *,
        forbid_state: Optional[StateT] = None,
    ) -> Iterable[Successor[StateT]]:
        """Yield legal predecessors of ``state`` (incoming edges).

        Each yielded ``Successor`` uses ``state`` = predecessor and ``cost`` =
        cost(pred → ``state``). Default equals :meth:`successors` (undirected
        graphs). Directed domains must override.
        """

        return self.successors(state, forbid_state=forbid_state)

    @abstractmethod
    def transition_cost(self, from_state: StateT, to_state: StateT) -> float:
        """Nonnegative cost of the edge from ``from_state`` to ``to_state``.

        Raises ``ValueError`` if the transition is not a legal edge.
        """

    def is_goal(self, state: StateT) -> bool:
        """Return whether ``state`` is the goal (default: equality)."""

        return state == self.goal_state

    def branch_factor(
        self,
        state: StateT,
        *,
        forbid_state: Optional[StateT] = None,
    ) -> int:
        """Count legal successors after optional parent suppression."""

        return sum(1 for _ in self.successors(state, forbid_state=forbid_state))

    def predecessor_branch_factor(
        self,
        state: StateT,
        *,
        forbid_state: Optional[StateT] = None,
    ) -> int:
        """Count legal predecessors after optional parent suppression."""

        return sum(
            1 for _ in self.predecessors(state, forbid_state=forbid_state)
        )

    def describe(self) -> dict[str, Any]:
        """Optional metadata for experiment logging."""

        return {"problem_type": type(self).__name__}
