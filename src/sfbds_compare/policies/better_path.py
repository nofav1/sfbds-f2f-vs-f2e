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

    Does not mutate OPEN/CLOSED. ``PUSH`` and ``REPLACE_OPEN`` are both
    applied as ``open_list.push`` (improve-only / lazy stale). ``REOPEN`` is
    for CLOSED only: the searcher must ``closed.remove`` then push. Do not
    return ``PUSH`` for a CLOSED duplicate (the searcher would skip the
    later pop while the key is still CLOSED).
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
