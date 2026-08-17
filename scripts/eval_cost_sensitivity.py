"""Offline heuristic-eval cost sensitivity (Option 3A).

Uses existing reopen *_opt study CSVs only. Does not re-run search.

    T_beta = (runtime_sec - heuristic_time_sec) + beta * heuristic_evals

Outputs: results/analysis/pair-bound/2026-08-17-eval-cost-sensitivity/

Refuse a non-empty OUT unless --force. --check-only loads the three families
and asserts 30 pairs, rest >= 0, and 0 F2E-fewer-eval maps (no write).
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "results" / "study" / "pair-bound"
OUT = ROOT / "results" / "analysis" / "pair-bound" / "2026-08-17-eval-cost-sensitivity"

MULTIPLIERS = (0.0, 0.1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5, 1e6)

DATASETS: list[tuple[str, str, int | None]] = [
    ("maze_127", "study_maze_127_opt.csv", None),
    ("maze_255", "study_maze_255_opt.csv", None),
    ("nested_64_d30", "study_random_64_opt.csv", 1228),
]


def _f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def _i(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def load_pairs(path: Path, obstacle_count: int | None) -> list[tuple[dict[str, str], dict[str, str]]]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    by: dict[tuple[str, str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        if obstacle_count is not None and _i(row, "obstacle_count") != obstacle_count:
            continue
        algo = row["algorithm"]
        if algo not in ("sfbds_f2f", "sfbds_f2e"):
            continue
        key = (row["query_index"], row["obstacle_count"], row["map_hash"])
        by[key][algo] = row
    pairs: list[tuple[dict[str, str], dict[str, str]]] = []
    for grouped in by.values():
        if "sfbds_f2f" in grouped and "sfbds_f2e" in grouped:
            pairs.append((grouped["sfbds_f2f"], grouped["sfbds_f2e"]))
    return pairs


def eval_fewer_counts(
    pairs: list[tuple[dict[str, str], dict[str, str]]],
) -> tuple[int, int, int]:
    n_f2f = n_f2e = n_tie = 0
    for f2f, f2e in pairs:
        ef, ee = _i(f2f, "heuristic_evals"), _i(f2e, "heuristic_evals")
        if ef < ee:
            n_f2f += 1
        elif ee < ef:
            n_f2e += 1
        else:
            n_tie += 1
    return n_f2f, n_f2e, n_tie


def check_family(
    name: str, pairs: list[tuple[dict[str, str], dict[str, str]]]
) -> tuple[int, int, int]:
    """Lock the appendix premise: 30 pairs, rest >= 0, F2E never fewer evals."""
    if len(pairs) != 30:
        raise ValueError(f"{name}: expected 30 F2F/F2E pairs, got {len(pairs)}")
    for f2f, f2e in pairs:
        rest_and_evals(f2f)
        rest_and_evals(f2e)
    n_f2f, n_f2e, n_tie = eval_fewer_counts(pairs)
    if n_f2e != 0:
        raise ValueError(
            f"{name}: F2E-fewer heuristic evals = {n_f2e} (appendix assumes 0)"
        )
    return n_f2f, n_f2e, n_tie


def refuse_out_dir(path: Path, *, force: bool) -> str | None:
    if path.exists() and any(path.iterdir()) and not force:
        return (
            f"{path} already exists and is not empty; "
            "pick a new slug or pass --force"
        )
    return None


def rest_and_evals(row: dict[str, str]) -> tuple[float, int]:
    rest = _f(row, "runtime_sec") - _f(row, "heuristic_time_sec")
    if rest < 0:
        raise ValueError("negative non-heuristic residual")
    evals = _i(row, "heuristic_evals")
    if evals <= 0:
        raise ValueError("non-positive heuristic_evals")
    return rest, evals


def implied_betas(pairs: list[tuple[dict[str, str], dict[str, str]]]) -> list[float]:
    values: list[float] = []
    for f2f, f2e in pairs:
        for row in (f2f, f2e):
            evals = _i(row, "heuristic_evals")
            values.append(_f(row, "heuristic_time_sec") / evals)
    return values


def t_beta(row: dict[str, str], beta: float) -> float:
    rest, evals = rest_and_evals(row)
    return rest + beta * evals


def median(xs: list[float]) -> float:
    return float(statistics.median(xs))


def summarize_beta(
    family: str,
    pairs: list[tuple[dict[str, str], dict[str, str]]],
    beta: float,
    multiplier: float,
    observed_beta: float,
) -> dict[str, object]:
    ratios: list[float] = []
    n_f2f = n_f2e = n_tie = 0
    total_f2f = 0.0
    total_f2e = 0.0
    for f2f, f2e in pairs:
        tf = t_beta(f2f, beta)
        te = t_beta(f2e, beta)
        total_f2f += tf
        total_f2e += te
        if te == 0:
            raise ValueError("zero F2E T_beta")
        ratios.append(tf / te)
        if tf < te:
            n_f2f += 1
        elif te < tf:
            n_f2e += 1
        else:
            n_tie += 1
    return {
        "family": family,
        "beta_sec_per_eval": beta,
        "beta_over_observed": multiplier,
        "observed_beta_sec_per_eval": observed_beta,
        "n": len(pairs),
        "n_f2f_cheaper": n_f2f,
        "n_f2e_cheaper": n_f2e,
        "n_tie": n_tie,
        "median_T_ratio": median(ratios),
        "total_T_f2f": total_f2f,
        "total_T_f2e": total_f2e,
        "total_T_ratio": total_f2f / total_f2e,
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    fields = [
        "family",
        "beta_sec_per_eval",
        "beta_over_observed",
        "observed_beta_sec_per_eval",
        "n",
        "n_f2f_cheaper",
        "n_f2e_cheaper",
        "n_tie",
        "median_T_ratio",
        "total_T_f2f",
        "total_T_f2e",
        "total_T_ratio",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_figure(rows: list[dict[str, object]], path: Path) -> None:
    import matplotlib.pyplot as plt

    labels = {
        "maze_127": "Maze 127",
        "maze_255": "Maze 255",
        "nested_64_d30": "Nested 64 @ 30%",
    }
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for family, label in labels.items():
        fam_rows = [r for r in rows if r["family"] == family]
        # beta=0 cannot sit on a log axis; plot from the first positive beta.
        xs = [float(r["beta_sec_per_eval"]) for r in fam_rows if float(r["beta_sec_per_eval"]) > 0]
        ys = [float(r["median_T_ratio"]) for r in fam_rows if float(r["beta_sec_per_eval"]) > 0]
        ax.plot(xs, ys, marker="o", linewidth=1.6, label=label)
    ax.axhline(1.0, color="black", linewidth=0.9)
    ax.set_xscale("log")
    ax.set_xlabel("Assumed heuristic cost β (seconds / evaluation)")
    ax.set_ylabel("Median T_F2F / T_F2E")
    ax.set_title("Offline eval-cost sensitivity (reopen F2E)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def crossover_note(family: str, rows: list[dict[str, object]]) -> str:
    fam = [r for r in rows if r["family"] == family]
    for row in fam:
        if float(row["median_T_ratio"]) > 1.0 or int(row["n_f2e_cheaper"]) > int(row["n_f2f_cheaper"]):
            return (
                f"{family}: crossover at beta={row['beta_sec_per_eval']} "
                f"({row['beta_over_observed']}× observed)"
            )
    return f"{family}: no crossover to F2E for any tested beta >= 0"


def load_all_families() -> list[tuple[str, list[tuple[dict[str, str], dict[str, str]]], tuple[int, int, int]]]:
    loaded: list[
        tuple[str, list[tuple[dict[str, str], dict[str, str]]], tuple[int, int, int]]
    ] = []
    for family, filename, obstacle_count in DATASETS:
        pairs = load_pairs(STUDY / filename, obstacle_count)
        counts = check_family(family, pairs)
        loaded.append((family, pairs, counts))
    return loaded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline F2F vs F2E eval-cost sensitivity")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Assert 30 pairs, rest >= 0, 0 F2E-fewer evals; do not write.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing non-empty output folder.",
    )
    args = parser.parse_args(argv)

    try:
        loaded = load_all_families()
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.check_only:
        for family, _pairs, (n_f2f, n_f2e, n_tie) in loaded:
            print(f"{family}: evals F2F-fewer/F2E-fewer/tie = {n_f2f}/{n_f2e}/{n_tie}")
        print("ok")
        return 0

    refused = refuse_out_dir(OUT, force=args.force)
    if refused:
        print(refused, file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    all_rows: list[dict[str, object]] = []
    notes: list[str] = []
    for family, pairs, (n_f2f, n_f2e, n_tie) in loaded:
        betas = implied_betas(pairs)
        observed = median(betas)
        for multiplier in MULTIPLIERS:
            beta = 0.0 if multiplier == 0.0 else observed * multiplier
            all_rows.append(summarize_beta(family, pairs, beta, multiplier, observed))
        notes.append(crossover_note(family, all_rows))
        notes.append(
            f"{family}: evals F2F-fewer/F2E-fewer/tie = "
            f"{n_f2f}/{n_f2e}/{n_tie}; observed beta={observed:.6e}"
        )

    write_csv(all_rows, OUT / "sensitivity.csv")
    write_figure(all_rows, OUT / "cost_ratio_vs_beta.png")
    print(f"wrote {OUT}")
    for line in notes:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
