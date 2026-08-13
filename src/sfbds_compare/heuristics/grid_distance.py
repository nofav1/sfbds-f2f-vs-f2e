"""Manhattan distance on grid cells."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridState


def manhattan(a: GridState, b: GridState) -> float:
    """4-connected unit Manhattan distance between two cells."""

    return float(abs(a.row - b.row) + abs(a.col - b.col))
