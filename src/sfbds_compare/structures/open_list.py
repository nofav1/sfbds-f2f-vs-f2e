"""Priority OPEN abstractions, including lazy-heap implementation."""

from __future__ import annotations

import heapq
from typing import Callable, Generic, Hashable, Optional, Protocol, TypeVar

K = TypeVar("K", bound=Hashable)
N = TypeVar("N")
SortKey = tuple


class OpenList(Protocol[K, N]):
    """OPEN interface used by A* and SFBDS (no heapq details)."""

    def push(self, node: N) -> bool: ...

    def pop_min(self) -> Optional[N]: ...

    def contains(self, key: K) -> bool: ...

    def get_best(self, key: K) -> Optional[N]: ...

    def best_g(self, key: K) -> Optional[float]: ...

    def logical_size(self) -> int: ...

    def is_empty(self) -> bool: ...

    @property
    def stale_skipped(self) -> int: ...


class LazyHeapOpen(Generic[K, N]):
    """Lazy ``heapq`` OPEN: improved keys push a new entry; stale pops are skipped.

    Callers supply:
    - ``key_of(node)``: membership / duplicate key
    - ``g_of(node)``: path cost used for stale detection and ``best_g``
    - ``sort_key_of(node)``: total order for ``pop_min`` (e.g. TBh tuple)

    ``push`` is **improve-only**: if ``key`` already has a champion with
    ``g_new >= g_best``, the push is rejected (returns ``False``) and the
    champion is unchanged. Strictly better ``g`` updates the champion and
    inserts a new heap row (old row becomes stale).
    """

    def __init__(
        self,
        key_of: Callable[[N], K],
        g_of: Callable[[N], float],
        sort_key_of: Callable[[N], SortKey],
    ) -> None:
        self._key_of = key_of
        self._g_of = g_of
        self._sort_key_of = sort_key_of
        self._heap: list[tuple[SortKey, int, N]] = []
        self._best: dict[K, N] = {}
        self._seq = 0
        self._stale_skipped = 0

    @property
    def stale_skipped(self) -> int:
        return self._stale_skipped

    def push(self, node: N) -> bool:
        key = self._key_of(node)
        g = self._g_of(node)
        current = self._best.get(key)
        if current is not None and g >= self._g_of(current):
            return False
        self._best[key] = node
        heapq.heappush(self._heap, (self._sort_key_of(node), self._seq, node))
        self._seq += 1
        return True

    def pop_min(self) -> Optional[N]:
        while self._heap:
            _sort, _seq, node = heapq.heappop(self._heap)
            key = self._key_of(node)
            current = self._best.get(key)
            # Champion is updated by identity on push; older heap rows are stale.
            if current is node:
                del self._best[key]
                return node
            self._stale_skipped += 1
        return None

    def contains(self, key: K) -> bool:
        return key in self._best

    def get_best(self, key: K) -> Optional[N]:
        return self._best.get(key)

    def best_g(self, key: K) -> Optional[float]:
        node = self._best.get(key)
        if node is None:
            return None
        return self._g_of(node)

    def logical_size(self) -> int:
        return len(self._best)

    def is_empty(self) -> bool:
        return not self._best

    def clear(self) -> None:
        self._heap.clear()
        self._best.clear()
        self._seq = 0
        self._stale_skipped = 0

    def __len__(self) -> int:
        """Logical unique-key size (not raw heap length)."""

        return self.logical_size()
