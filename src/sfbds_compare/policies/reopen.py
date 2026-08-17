"""Reopen policy for CLOSED duplicates."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.policies.types import PathAction
from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class ReopenPolicy(Protocol[StateT]):
    def decide_closed(
        self,
        existing: SFBDSNode[StateT],
        candidate: SFBDSNode[StateT],
    ) -> PathAction: ...


class NoReopenPolicy(Generic[StateT]):
    """Never reopen CLOSED nodes; always discard the candidate."""

    def decide_closed(
        self,
        existing: SFBDSNode[StateT],
        candidate: SFBDSNode[StateT],
    ) -> PathAction:
        return PathAction.DISCARD


class BetterGReopenPolicy(Generic[StateT]):
    """Reopen CLOSED pairs on strictly better g; discard equal or worse g."""

    def decide_closed(
        self,
        existing: SFBDSNode[StateT],
        candidate: SFBDSNode[StateT],
    ) -> PathAction:
        if candidate.g < existing.g:
            return PathAction.REOPEN
        return PathAction.DISCARD
