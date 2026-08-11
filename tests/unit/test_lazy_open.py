"""Unit tests for LazyHeapOpen stale-entry behavior and CLOSED."""

from __future__ import annotations

from dataclasses import dataclass

from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import LazyHeapOpen
from sfbds_compare.structures.ordering import tbh_sort_key


@dataclass(slots=True)
class _Node:
    key: str
    g: float
    h: float = 0.0

    @property
    def f(self) -> float:
        return self.g + self.h


def _make_open() -> LazyHeapOpen[str, _Node]:
    return LazyHeapOpen(
        key_of=lambda n: n.key,
        g_of=lambda n: n.g,
        sort_key_of=lambda n: tbh_sort_key(n.f, n.h, n.g, n.key),
    )


def test_pop_min_returns_lowest_f() -> None:
    open_list = _make_open()
    open_list.push(_Node("a", g=5, h=1))
    open_list.push(_Node("b", g=1, h=1))
    first = open_list.pop_min()
    assert first is not None
    assert first.key == "b"
    assert open_list.logical_size() == 1


def test_improved_entry_makes_old_stale() -> None:
    open_list = _make_open()
    stale = _Node("x", g=10, h=0)
    better = _Node("x", g=4, h=0)
    open_list.push(stale)
    open_list.push(better)
    assert open_list.logical_size() == 1
    assert open_list.best_g("x") == 4.0

    got = open_list.pop_min()
    assert got is better
    # Stale heap row is discarded on the next pop attempt.
    assert open_list.pop_min() is None
    assert open_list.stale_skipped >= 1
    assert open_list.is_empty()


def test_contains_and_get_best_track_champion() -> None:
    open_list = _make_open()
    open_list.push(_Node("p", g=3))
    open_list.push(_Node("p", g=2))
    assert open_list.contains("p")
    best = open_list.get_best("p")
    assert best is not None
    assert best.g == 2


def test_tbh_prefers_smaller_h_on_equal_f() -> None:
    open_list = _make_open()
    # f=5 both; prefer smaller h (larger g)
    a = _Node("a", g=2, h=3)
    b = _Node("b", g=4, h=1)
    open_list.push(a)
    open_list.push(b)
    assert open_list.pop_min() is b


def test_closed_set_roundtrip() -> None:
    closed: ClosedSet[str, _Node] = ClosedSet()
    node = _Node("c", g=1)
    closed.add("c", node)
    assert closed.contains("c")
    assert closed.get("c") is node
    assert len(closed) == 1
