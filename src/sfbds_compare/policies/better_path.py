"""Better-path decisions for generated SFBDS children."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.policies.reopen import ReopenPolicy
from sfbds_compare.policies.types import DuplicateLocation, DuplicateLookup, PathAction
from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class BetterPathPolicy(Protocol[StateT]):
    def decide(
        self,
        lookup: DuplicateLookup[StateT],
        candidate: SFBDSNode[StateT],
        reopen: ReopenPolicy[StateT],
    ) -> PathAction: ...


class ReplaceBetterOpenPathPolicy(Generic[StateT]):
    """Push unseen; replace OPEN on strictly better g; CLOSED → ReopenPolicy.

    Does not mutate OPEN/CLOSED; the searcher applies PUSH / REPLACE_OPEN via
    ``open_list.push`` (improve-only / lazy stale).
    """

    def decide(
        self,
        lookup: DuplicateLookup[StateT],
        candidate: SFBDSNode[StateT],
        reopen: ReopenPolicy[StateT],
    ) -> PathAction:
        if lookup.location is DuplicateLocation.UNSEEN:
            return PathAction.PUSH
        if lookup.location is DuplicateLocation.CLOSED:
            assert lookup.existing is not None
            return reopen.decide_closed(lookup.existing, candidate)
        # OPEN
        assert lookup.existing is not None
        if candidate.g < lookup.existing.g:
            return PathAction.REPLACE_OPEN
        return PathAction.DISCARD
