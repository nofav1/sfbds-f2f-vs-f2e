"""Direction selection for SFBDS pair expansion."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.policies.types import Side
from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class DirectionPolicy(Protocol[StateT]):
    def choose(
        self, node: SFBDSNode[StateT], problem: SearchProblem[StateT]
    ) -> Side: ...


class BranchingFactorDirectionPolicy(Generic[StateT]):
    """Expand the side with fewer legal successors after parent suppression.

    Tie → Forward.
    """

    def choose(
        self, node: SFBDSNode[StateT], problem: SearchProblem[StateT]
    ) -> Side:
        bf_f = problem.branch_factor(
            node.forward, forbid_state=node.forbid_forward
        )
        bf_b = problem.branch_factor(
            node.backward, forbid_state=node.forbid_backward
        )
        if bf_b < bf_f:
            return Side.BACKWARD
        return Side.FORWARD
