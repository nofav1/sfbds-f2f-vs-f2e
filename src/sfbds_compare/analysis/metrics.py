"""Locked pairing formulas (analysis layer only)."""

from __future__ import annotations

from typing import Optional


def manhattan_distance(
    start_row: int, start_col: int, goal_row: int, goal_col: int
) -> int:
    return abs(start_row - goal_row) + abs(start_col - goal_col)


def detour_ratio(
    solution_cost: Optional[float], manhattan: int
) -> Optional[float]:
    if manhattan == 0:
        if solution_cost == 0:
            return 1.0
        return None
    if solution_cost is None:
        return None
    return solution_cost / manhattan


def detour_bucket(ratio: Optional[float]) -> Optional[str]:
    if ratio is None:
        return None
    if ratio < 1.1:
        return "[1, 1.1)"
    if ratio < 1.5:
        return "[1.1, 1.5)"
    if ratio < 2.0:
        return "[1.5, 2)"
    return "[2, inf)"


def ratio(numer: Optional[float], denom: Optional[float]) -> Optional[float]:
    if numer is None or denom is None or denom == 0:
        return None
    return numer / denom


def saving_pct(
    baseline: Optional[float], challenger: Optional[float]
) -> Optional[float]:
    """Percent reduction of ``challenger`` vs ``baseline`` (F2E vs F2F)."""

    if baseline is None or challenger is None or baseline == 0:
        return None
    return (baseline - challenger) / baseline * 100.0


def map_family(generator_kind: str) -> str:
    if generator_kind == "random_obstacles":
        return "random"
    return generator_kind
