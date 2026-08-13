"""Ordered-pair duplicate detection for SFBDS."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, TypeVar

from sfbds_compare.policies.types import DuplicateLocation, DuplicateLookup
from sfbds_compare.search.nodes import SFBDSNode
from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import OpenList

StateT = TypeVar("StateT", bound=Hashable)
PairKey = tuple[StateT, StateT]


class DuplicatePolicy(Protocol[StateT]):
    def lookup(
        self,
        key: PairKey,
        open_list: OpenList[PairKey, SFBDSNode[StateT]],
        closed: ClosedSet[PairKey, SFBDSNode[StateT]],
    ) -> DuplicateLookup[StateT]: ...


class OrderedPairDuplicatePolicy(Generic[StateT]):
    """Membership by ordered pair (x, y); OPEN checked before CLOSED."""

    def lookup(
        self,
        key: PairKey,
        open_list: OpenList[PairKey, SFBDSNode[StateT]],
        closed: ClosedSet[PairKey, SFBDSNode[StateT]],
    ) -> DuplicateLookup[StateT]:
        best = open_list.get_best(key)
        if best is not None:
            return DuplicateLookup(DuplicateLocation.OPEN, best)
        closed_node = closed.get(key)
        if closed_node is not None:
            return DuplicateLookup(DuplicateLocation.CLOSED, closed_node)
        return DuplicateLookup(DuplicateLocation.UNSEEN, None)
