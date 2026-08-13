"""Late goal test for SFBDS pairs."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class GoalTestPolicy(Protocol[StateT]):
    def is_goal(self, node: SFBDSNode[StateT]) -> bool: ...


class GoalOnSelectPolicy(Generic[StateT]):
    """Late goal: pair is a goal iff forward == backward (meeting state)."""

    def is_goal(self, node: SFBDSNode[StateT]) -> bool:
        return node.forward == node.backward
