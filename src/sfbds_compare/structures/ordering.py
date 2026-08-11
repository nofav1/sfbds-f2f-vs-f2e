"""Deterministic sort-key helpers for priority OPEN (TBh-compatible)."""

from __future__ import annotations

from typing import Hashable, Tuple


def tbh_sort_key(
    f: float,
    h: float,
    g: float,
    node_id: Hashable,
) -> Tuple[float, float, float, str]:
    """TBh hierarchy: smaller f, smaller h, larger g, then deterministic id.

    Suitable for ``heapq`` (min-heap): larger ``g`` is encoded as ``-g``.
    """

    return (f, h, -g, repr(node_id))
