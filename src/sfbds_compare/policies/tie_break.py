"""Tie-breaking sort keys for SFBDS OPEN."""

from __future__ import annotations

from typing import Generic, Hashable, Protocol, Tuple, TypeVar

from sfbds_compare.search.nodes import SFBDSNode
from sfbds_compare.structures.ordering import tbh_sort_key

StateT = TypeVar("StateT", bound=Hashable)
SortKey = Tuple[float, float, float, str]


class TieBreakingPolicy(Protocol[StateT]):
    def sort_key(self, node: SFBDSNode[StateT]) -> SortKey: ...


class TBhTieBreakingPolicy(Generic[StateT]):
    """TBh: smaller f, smaller h_gap, larger g_pair, then deterministic pair id."""

    def sort_key(self, node: SFBDSNode[StateT]) -> SortKey:
        return tbh_sort_key(node.f, node.h_gap, node.g, node.pair_key)
