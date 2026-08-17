"""CLOSED-set abstraction for search algorithms."""

from __future__ import annotations

from typing import Generic, Hashable, Iterator, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
N = TypeVar("N")


class ClosedSet(Generic[K, N]):
    """Hash-based CLOSED membership and node lookup."""

    def __init__(self) -> None:
        self._nodes: dict[K, N] = {}

    def add(self, key: K, node: N) -> None:
        self._nodes[key] = node

    def contains(self, key: K) -> bool:
        return key in self._nodes

    def get(self, key: K) -> Optional[N]:
        return self._nodes.get(key)

    def remove(self, key: K) -> N:
        return self._nodes.pop(key)

    def __len__(self) -> int:
        return len(self._nodes)

    def __iter__(self) -> Iterator[K]:
        return iter(self._nodes)

    def clear(self) -> None:
        self._nodes.clear()
