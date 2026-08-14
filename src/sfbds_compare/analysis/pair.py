"""Pivot raw algorithm×query rows into one F2F/F2E pair per instance."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Optional

from sfbds_compare.analysis.metrics import (
    detour_bucket,
    detour_ratio,
    manhattan_distance,
    map_family,
    ratio,
    saving_pct,
)

_F2F = "sfbds_f2f"
_F2E = "sfbds_f2e"
_ASTAR = "astar"


def family_id(row: dict[str, Any]) -> str:
    return (
        f"{row['experiment']}:{row['generator_kind']}:"
        f"{row['height']}x{row['width']}:{row['seed']}:{row['query_index']}"
    )


def pair_id(row: dict[str, Any]) -> str:
    return f"{family_id(row)}:{row['map_hash']}"


def _solved_sfbds(row: dict[str, Any]) -> bool:
    return bool(row["success"]) and not bool(row["timed_out"])


def pair_rows(raw: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One paired row per map_hash × query (requires both SFBDS algorithms)."""

    by_key: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in raw:
        by_key[pair_id(row)][row["algorithm"]] = row

    out: list[dict[str, Any]] = []
    for pid, algos in by_key.items():
        f2f = algos.get(_F2F)
        f2e = algos.get(_F2E)
        if f2f is None or f2e is None:
            continue
        astar = algos.get(_ASTAR)
        out.append(_paired_record(pid, f2f, f2e, astar))
    _mark_nested_density(out)
    out.sort(key=lambda r: (r["experiment"], r["query_index"], r["obstacle_count"]))
    return out


def _mark_nested_density(paired: list[dict[str, Any]]) -> None:
    """Flag families that have more than one obstacle_count (nested prefixes).

    Independent ``*_d10/d20/d30`` experiments have one density per family_id
    and must not enter density-factor tests or plots.
    """

    counts_by_family: dict[str, set[int]] = defaultdict(set)
    for row in paired:
        if row.get("map_family") == "random":
            counts_by_family[row["family_id"]].add(int(row["obstacle_count"]))
    nested_families = {
        fid for fid, counts in counts_by_family.items() if len(counts) > 1
    }
    for row in paired:
        row["nested_density"] = row["family_id"] in nested_families


def _cost_for_detour(
    astar: Optional[dict[str, Any]],
    f2f: dict[str, Any],
    f2e: dict[str, Any],
) -> Optional[float]:
    if astar is not None and _solved_sfbds(astar) and astar["solution_cost"] is not None:
        return float(astar["solution_cost"])
    if _solved_sfbds(f2f) and f2f["solution_cost"] is not None:
        return float(f2f["solution_cost"])
    if _solved_sfbds(f2e) and f2e["solution_cost"] is not None:
        return float(f2e["solution_cost"])
    return None


def _paired_record(
    pid: str,
    f2f: dict[str, Any],
    f2e: dict[str, Any],
    astar: Optional[dict[str, Any]],
) -> dict[str, Any]:
    solved = _solved_sfbds(f2f) and _solved_sfbds(f2e)
    timed_out = bool(f2f["timed_out"] or f2e["timed_out"])
    md = manhattan_distance(
        f2f["start_row"], f2f["start_col"], f2f["goal_row"], f2f["goal_col"]
    )
    cost = _cost_for_detour(astar, f2f, f2e)
    detour = detour_ratio(cost, md)
    f2f_exp = int(f2f["expanded"]) if solved else None
    f2e_exp = int(f2e["expanded"]) if solved else None
    f2f_gen = int(f2f["generated"]) if solved else None
    f2e_gen = int(f2e["generated"]) if solved else None
    cost_mismatch = False
    if (
        _solved_sfbds(f2f)
        and _solved_sfbds(f2e)
        and f2f["solution_cost"] is not None
        and f2e["solution_cost"] is not None
        and float(f2f["solution_cost"]) != float(f2e["solution_cost"])
    ):
        cost_mismatch = True

    expansion_diff = None if not solved else f2e_exp - f2f_exp
    return {
        "pair_id": pid,
        "family_id": family_id(f2f),
        "experiment": f2f["experiment"],
        "map_family": map_family(f2f["generator_kind"]),
        "generator_kind": f2f["generator_kind"],
        "seed": f2f["seed"],
        "query_index": f2f["query_index"],
        "map_hash": f2f["map_hash"],
        "height": f2f["height"],
        "width": f2f["width"],
        "size": max(f2f["height"], f2f["width"]),
        "obstacle_count": f2f["obstacle_count"],
        "obstacle_density_label": round(
            f2f["obstacle_count"] / (f2f["height"] * f2f["width"]), 2
        ),
        "start_row": f2f["start_row"],
        "start_col": f2f["start_col"],
        "goal_row": f2f["goal_row"],
        "goal_col": f2f["goal_col"],
        "solution_cost": cost,
        "manhattan_distance": md,
        "detour_ratio": detour,
        "detour_bucket": detour_bucket(detour),
        "solved": solved,
        "timed_out": timed_out,
        "cost_mismatch": cost_mismatch,
        "f2f_expanded": f2f_exp,
        "f2e_expanded": f2e_exp,
        "f2f_generated": f2f_gen,
        "f2e_generated": f2e_gen,
        "f2f_runtime_sec": float(f2f["runtime_sec"]) if solved else None,
        "f2e_runtime_sec": float(f2e["runtime_sec"]) if solved else None,
        "f2f_heuristic_evals": int(f2f["heuristic_evals"]) if solved else None,
        "f2e_heuristic_evals": int(f2e["heuristic_evals"]) if solved else None,
        "f2f_heuristic_time_sec": float(f2f["heuristic_time_sec"]) if solved else None,
        "f2e_heuristic_time_sec": float(f2e["heuristic_time_sec"]) if solved else None,
        "f2f_peak_open": int(f2f["peak_open"]) if solved else None,
        "f2e_peak_open": int(f2e["peak_open"]) if solved else None,
        "f2f_forward_expanded": f2f["forward_expanded"] if solved else None,
        "f2f_backward_expanded": f2f["backward_expanded"] if solved else None,
        "f2e_forward_expanded": f2e["forward_expanded"] if solved else None,
        "f2e_backward_expanded": f2e["backward_expanded"] if solved else None,
        "f2f_meeting_g_F": f2f["meeting_g_F"] if solved else None,
        "f2f_meeting_g_B": f2f["meeting_g_B"] if solved else None,
        "f2e_meeting_g_F": f2e["meeting_g_F"] if solved else None,
        "f2e_meeting_g_B": f2e["meeting_g_B"] if solved else None,
        "expansion_diff": expansion_diff,
        "expansion_ratio": ratio(f2f_exp, f2e_exp),
        "expansion_saving_pct": saving_pct(f2e_exp, f2f_exp),
        "generation_saving_pct": saving_pct(f2e_gen, f2f_gen),
        "runtime_ratio": ratio(
            float(f2f["runtime_sec"]) if solved else None,
            float(f2e["runtime_sec"]) if solved else None,
        ),
        "heuristic_time_ratio": ratio(
            float(f2f["heuristic_time_sec"]) if solved else None,
            float(f2e["heuristic_time_sec"]) if solved else None,
        ),
        "astar_expanded": None if astar is None else int(astar["expanded"]),
        "astar_runtime_sec": None if astar is None else float(astar["runtime_sec"]),
        "astar_success": None if astar is None else bool(astar["success"]),
        "astar_timed_out": None if astar is None else bool(astar["timed_out"]),
        "astar_solution_cost": None
        if astar is None
        else astar["solution_cost"],
    }
