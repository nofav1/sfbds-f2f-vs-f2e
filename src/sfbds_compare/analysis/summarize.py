"""Grouped descriptives plus planned paired tests."""

from __future__ import annotations

from collections import defaultdict
from statistics import mean, median
from typing import Any, Optional, Sequence

from sfbds_compare.analysis.stats import (
    collapse_random_diffs,
    expansion_win_counts,
    holm_adjust,
    rank_biserial,
    sign_test_p,
    wilcoxon_signed_rank,
)


def _finite(values: Sequence[Optional[float]]) -> list[float]:
    return [float(v) for v in values if v is not None]


def _mean(values: Sequence[Optional[float]]) -> Optional[float]:
    data = _finite(values)
    return mean(data) if data else None


def _median(values: Sequence[Optional[float]]) -> Optional[float]:
    data = _finite(values)
    return median(data) if data else None


def expansion_test_rows(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Solved pairs whose F2F / F2E / A* costs agree (when A* succeeded)."""

    return [
        r
        for r in rows
        if r.get("solved") and not r.get("cost_mismatch")
    ]


def nested_density_group_key(row: dict[str, Any]) -> Optional[str]:
    """Density test key: one nested experiment × grid size × obstacle_count."""

    if row.get("map_family") != "random" or not row.get("nested_density"):
        return None
    return (
        f"{row['experiment']}::{row['height']}x{row['width']}::"
        f"{int(row['obstacle_count'])}"
    )


def _group_key(row: dict[str, Any], group_type: str) -> Optional[str]:
    if group_type == "map_family":
        return str(row["map_family"])
    if group_type == "size":
        return str(row["size"])
    if group_type == "obstacle_count":
        return nested_density_group_key(row)
    if group_type == "detour_bucket":
        bucket = row.get("detour_bucket")
        return None if bucket is None else str(bucket)
    raise ValueError(f"unknown group_type: {group_type}")


def _pooled_random_skip_reason(rows: Sequence[dict[str, Any]]) -> Optional[str]:
    """Why map_family=random Wilcoxon is skipped, or None to test."""

    solved = [r for r in rows if r.get("solved")]
    flags = {bool(r.get("nested_density")) for r in solved}
    if flags == {True, False}:
        return (
            "Wilcoxon skipped: pooled random mixes nested and independent files; "
            "see overall_random and obstacle_count"
        )
    test_rows = expansion_test_rows(rows)
    n_maps = sum(1 for r in test_rows if r.get("expansion_diff") is not None)
    if len(collapse_random_diffs(test_rows)) != n_maps:
        return (
            "Wilcoxon skipped on pooled nested random; see overall_random and obstacle_count"
        )
    return None


def _describe(
    rows: Sequence[dict[str, Any]],
    *,
    exploratory: bool,
    skip_tests: bool = False,
    skip_reason: Optional[str] = None,
) -> dict[str, Any]:
    solved = [r for r in rows if r.get("solved")]
    n_timeout = sum(1 for r in rows if r.get("timed_out"))
    n_solved = len(solved)
    n_mismatch = sum(1 for r in solved if r.get("cost_mismatch"))
    test_rows = expansion_test_rows(rows)
    test_diffs = collapse_random_diffs(test_rows)
    n_test = len(test_diffs)
    n_f2f, n_f2e, n_tie = expansion_win_counts(test_diffs)
    n_untied = n_f2f + n_f2e
    n_for_pct = n_test if n_test else n_solved
    pct = lambda c: None if n_for_pct == 0 else 100.0 * c / n_for_pct
    notes: list[str] = []
    if n_mismatch:
        notes.append(
            f"excluded {n_mismatch} cost_mismatch rows from expansion tests"
        )
    if any(r.get("map_family") == "random" for r in test_rows) and n_test != len(
        test_rows
    ):
        notes.append(
            f"Wilcoxon n_test={n_test} collapsed family_ids; "
            f"descriptives n_solved={n_solved}"
        )
    if skip_tests:
        w_stat = w_p = s_p = None
        r_rb = None
        notes.append(
            skip_reason
            or "Wilcoxon skipped on pooled nested random; see overall_random and obstacle_count"
        )
    else:
        w_stat, w_p, w_note = wilcoxon_signed_rank(test_diffs)
        s_p, s_note = sign_test_p(test_diffs)
        r_rb = rank_biserial(test_diffs)
        notes.extend(n for n in (w_note, s_note) if n)
    return {
        "n_solved": n_solved,
        "n_timeout": n_timeout,
        "n_test": n_test,
        "n_untied": n_untied,
        "n_f2f_fewer": n_f2f,
        "n_f2e_fewer": n_f2e,
        "n_tie": n_tie,
        "pct_f2f_fewer": pct(n_f2f),
        "pct_f2e_fewer": pct(n_f2e),
        "pct_tie": pct(n_tie),
        "mean_expansion_saving_pct": _mean(
            [r.get("expansion_saving_pct") for r in test_rows]
        ),
        "median_expansion_saving_pct": _median(
            [r.get("expansion_saving_pct") for r in test_rows]
        ),
        "mean_generation_saving_pct": _mean(
            [r.get("generation_saving_pct") for r in test_rows]
        ),
        "median_generation_saving_pct": _median(
            [r.get("generation_saving_pct") for r in test_rows]
        ),
        "mean_runtime_ratio": _mean([r.get("runtime_ratio") for r in test_rows]),
        "median_runtime_ratio": _median([r.get("runtime_ratio") for r in test_rows]),
        "mean_heuristic_time_ratio": _mean(
            [r.get("heuristic_time_ratio") for r in test_rows]
        ),
        "median_heuristic_time_ratio": _median(
            [r.get("heuristic_time_ratio") for r in test_rows]
        ),
        "median_expansion_diff": _median(
            [r.get("expansion_diff") for r in test_rows]
        ),
        "wilcoxon_stat": w_stat,
        "wilcoxon_p_raw": w_p,
        "wilcoxon_p_holm": None,
        "rank_biserial": r_rb,
        "sign_p_raw": s_p,
        "sign_p_holm": None,
        "exploratory": exploratory,
        "note": "; ".join(notes),
    }


def _apply_holm(rows: list[dict[str, Any]]) -> None:
    planned = [r for r in rows if not r.get("exploratory")]
    w_adj = holm_adjust([r.get("wilcoxon_p_raw") for r in planned])
    s_adj = holm_adjust([r.get("sign_p_raw") for r in planned])
    for rec, wp, sp in zip(planned, w_adj, s_adj):
        rec["wilcoxon_p_holm"] = wp
        rec["sign_p_holm"] = sp


def summarize(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build summary+stats rows for planned and exploratory groupings."""

    out: list[dict[str, Any]] = []
    planned_families: list[list[dict[str, Any]]] = []

    def collect(group_type: str, *, exploratory: bool) -> list[dict[str, Any]]:
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in paired:
            key = _group_key(row, group_type)
            if key is None:
                continue
            buckets[key].append(row)
        family_rows: list[dict[str, Any]] = []
        for key in sorted(buckets, key=str):
            skip_reason = None
            if group_type == "map_family" and key == "random":
                skip_reason = _pooled_random_skip_reason(buckets[key])
            rec = {
                "group_type": group_type,
                "group": key,
                **_describe(
                    buckets[key],
                    exploratory=exploratory,
                    skip_tests=skip_reason is not None,
                    skip_reason=skip_reason,
                ),
            }
            family_rows.append(rec)
            out.append(rec)
        return family_rows

    planned_families.append(collect("map_family", exploratory=False))
    planned_families.append(collect("size", exploratory=False))
    density_rows = collect("obstacle_count", exploratory=False)
    density_by_experiment: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for rec in density_rows:
        experiment = str(rec["group"]).split("::", 1)[0]
        density_by_experiment[experiment].append(rec)
    for experiment in sorted(density_by_experiment):
        planned_families.append(density_by_experiment[experiment])
    random_rows = [
        r for r in paired if r.get("map_family") == "random" and r.get("nested_density")
    ]
    if random_rows:
        n_exps = len({str(r["experiment"]) for r in random_rows})
        overall = {
            "group_type": "overall_random",
            "group": "random",
            **_describe(
                random_rows,
                exploratory=False,
                skip_tests=n_exps > 1,
                skip_reason=(
                    "Wilcoxon skipped across multiple nested experiments; "
                    "use per-experiment density rows"
                    if n_exps > 1
                    else None
                ),
            ),
        }
        planned_families.append([overall])
        out.append(overall)
    collect("detour_bucket", exploratory=True)
    for family in planned_families:
        _apply_holm(family)
    return out
