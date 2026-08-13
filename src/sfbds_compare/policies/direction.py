"""Direction selection for SFBDS pair expansion."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.policies.types import Side
from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class DirectionPolicy(Protocol[StateT]):
    def choose_by_branch_factors(self, bf_f: int, bf_b: int) -> Side: ...

    def choose(
        self, node: SFBDSNode[StateT], problem: SearchProblem[StateT]
    ) -> Side: ...


class BranchingFactorDirectionPolicy(Generic[StateT]):
    """Expand the side with fewer legal operators after parent suppression.

    Forward uses successors; backward uses predecessors. Tie → Forward.
    """

    def choose_by_branch_factors(self, bf_f: int, bf_b: int) -> Side:
        if bf_b < bf_f:
            return Side.BACKWARD
        return Side.FORWARD

    def choose(
        self, node: SFBDSNode[StateT], problem: SearchProblem[StateT]
    ) -> Side:
        bf_f = problem.branch_factor(
            node.forward, forbid_state=node.forbid_forward
        )
        bf_b = problem.predecessor_branch_factor(
            node.backward, forbid_state=node.forbid_backward
        )
        return self.choose_by_branch_factors(bf_f, bf_b)
