"""Load raw experiment CSV rows (one algorithm × query per row)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Optional


def _as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def _as_opt_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    return float(value)


def _as_opt_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    return int(float(value))


_ANALYSIS_CSV_STEMS = frozenset({"paired", "summary", "stats"})
_RAW_REQUIRED = frozenset(
    {
        "experiment",
        "algorithm",
        "seed",
        "query_index",
        "generator_kind",
        "height",
        "width",
        "obstacle_density",
        "obstacle_count",
        "map_hash",
        "start_row",
        "start_col",
        "goal_row",
        "goal_col",
        "success",
        "termination_reason",
        "runtime_sec",
        "generated",
        "expanded",
        "expanded_unit",
        "heuristic_evals",
        "heuristic_time_sec",
        "peak_open",
        "peak_closed",
        "timed_out",
    }
)


def _is_raw_study_csv(path: Path, fieldnames: Optional[list[str]]) -> bool:
    if path.stem.lower() in _ANALYSIS_CSV_STEMS:
        return False
    if not fieldnames:
        return False
    return _RAW_REQUIRED.issubset(fieldnames)


def coerce_raw_row(row: dict[str, str]) -> dict[str, Any]:
    """Parse exported CSV strings into typed fields used by pairing."""

    return {
        "experiment": row["experiment"],
        "algorithm": row["algorithm"],
        "seed": int(row["seed"]),
        "query_index": int(row["query_index"]),
        "generator_kind": row["generator_kind"],
        "height": int(row["height"]),
        "width": int(row["width"]),
        "obstacle_density": float(row["obstacle_density"]),
        "obstacle_count": int(row["obstacle_count"]),
        "map_hash": row["map_hash"],
        "start_row": int(row["start_row"]),
        "start_col": int(row["start_col"]),
        "goal_row": int(row["goal_row"]),
        "goal_col": int(row["goal_col"]),
        "success": _as_bool(row["success"]),
        "termination_reason": row["termination_reason"],
        "solution_cost": _as_opt_float(row.get("solution_cost")),
        "runtime_sec": float(row["runtime_sec"]),
        "generated": int(row["generated"]),
        "expanded": int(row["expanded"]),
        "expanded_unit": row["expanded_unit"],
        "forward_expanded": _as_opt_int(row.get("forward_expanded")),
        "backward_expanded": _as_opt_int(row.get("backward_expanded")),
        "meeting_g_F": _as_opt_float(row.get("meeting_g_F")),
        "meeting_g_B": _as_opt_float(row.get("meeting_g_B")),
        "direction_switches": _as_opt_int(row.get("direction_switches")),
        "heuristic_evals": int(row["heuristic_evals"]),
        "heuristic_time_sec": float(row["heuristic_time_sec"]),
        "peak_open": int(row["peak_open"]),
        "peak_closed": int(row["peak_closed"]),
        "timed_out": _as_bool(row["timed_out"]),
    }


def load_raw_csvs(input_dir: str | Path) -> list[dict[str, Any]]:
    """Read raw study ``*.csv`` files in ``input_dir`` (skips empty/analysis files).

    Non-recursive: pass ``results/study/pair-bound`` or ``results/study/legacy``,
    never the parent ``results/study`` folder.
    """

    root = Path(input_dir)
    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob("*.csv")):
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if not _is_raw_study_csv(path, reader.fieldnames):
                continue
            for raw in reader:
                rows.append(coerce_raw_row(raw))
    return rows
