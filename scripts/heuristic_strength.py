"""Replay official F2F / reopen F2E and compare pair lower bounds.

Does not change search, policies, or heuristic formulas. Rebuilds maps from
the same *_opt YAMLs, matches frozen CSV map_hash/expanded, then evaluates
both LBs on every pair that SFBDS actually evaluate()-s.

    LB_F2F = g_F + g_B + MD(u, v)
    LB_F2E = official F2EPairLowerBound.lower_bound

Outputs: results/analysis/pair-bound/2026-08-17-heuristic-strength/
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import load_config
from sfbds_compare.experiments.generators import map_fingerprint
from sfbds_compare.experiments.runner import _problems_for_query, run_query
from sfbds_compare.heuristics.f2e import F2EPairLowerBound
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.grid_distance import manhattan
from sfbds_compare.policies import f2e_policies
from sfbds_compare.search.sfbds import SFBDSSearcher

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "results" / "study" / "pair-bound"
OUT = ROOT / "results" / "analysis" / "pair-bound" / "2026-08-17-heuristic-strength"

EPS = 1e-9
SAMPLE_PER_SOURCE = 200
SAMPLE_RNG_SEED = 20260817

_F2E_BOUND = F2EPairLowerBound()

FAMILIES: list[tuple[str, str, str, int | None]] = [
    ("open_128", "configs/study/study_open_128_opt.yaml", "study_open_128_opt.csv", None),
    ("maze_127", "configs/study/study_maze_127_opt.yaml", "study_maze_127_opt.csv", None),
    ("maze_255", "configs/followup/study_maze_255_opt.yaml", "study_maze_255_opt.csv", None),
    (
        "maze_127_braid",
        "configs/followup/study_maze_127_braid_opt.yaml",
        "study_maze_127_braid_opt.csv",
        None,
    ),
    (
        "nested_64_d30",
        "configs/study/study_random_64_opt.yaml",
        "study_random_64_opt.csv",
        1228,
    ),
    (
        "nested_64_d45",
        "configs/followup/study_random_64_dense_opt.yaml",
        "study_random_64_dense_opt.csv",
        1842,
    ),
]

# Frozen expansion splits (F2F-fewer, F2E-fewer, tie). Locked against study CSVs.
EXPECTED_SPLITS: dict[str, tuple[int, int, int]] = {
    "open_128": (0, 0, 30),
    "maze_127": (22, 0, 8),
    "maze_255": (26, 0, 4),
    "maze_127_braid": (12, 0, 18),
    "nested_64_d30": (13, 0, 17),
    "nested_64_d45": (14, 1, 15),
}
NESTED_D45_F2E_FEWER_QUERY = 8


def lb_f2f(forward: GridState, backward: GridState, g_F: float, g_B: float) -> float:
    return g_F + g_B + manhattan(forward, backward)


def lb_f2e(
    forward: GridState,
    backward: GridState,
    problem: GridProblem,
    g_F: float,
    g_B: float,
) -> float:
    return _F2E_BOUND.lower_bound(forward, backward, problem, g_F, g_B)


class BoundStats:
    def __init__(self) -> None:
        self.n = 0
        self.n_f2f_stronger = 0
        self.n_equal = 0
        self.n_f2e_stronger = 0
        self.n_meeting = 0
        self.sum_diff = 0.0
        self.diffs: list[float] = []

    def add(self, diff: float) -> None:
        self.n += 1
        self.sum_diff += diff
        self.diffs.append(diff)
        if diff > EPS:
            self.n_f2f_stronger += 1
        elif diff < -EPS:
            self.n_f2e_stronger += 1
        else:
            self.n_equal += 1

    def mean_diff(self) -> float | None:
        return None if self.n == 0 else self.sum_diff / self.n

    def median_diff(self) -> float | None:
        return None if not self.diffs else float(statistics.median(self.diffs))

    def frac(self, count: int) -> float | None:
        return None if self.n == 0 else count / self.n


class Reservoir:
    def __init__(self, k: int, rng: random.Random) -> None:
        self.k = k
        self.rng = rng
        self.items: list[dict[str, Any]] = []
        self.seen = 0

    def add(self, item: dict[str, Any]) -> None:
        self.seen += 1
        if len(self.items) < self.k:
            self.items.append(item)
            return
        j = self.rng.randrange(self.seen)
        if j < self.k:
            self.items[j] = item


class RecordingHeuristic:
    """Delegates evaluate unchanged; records both LBs on the same (u,v,g)."""

    def __init__(
        self,
        inner: Any,
        *,
        stats: BoundStats,
        reservoir: Reservoir,
        family: str,
        query_index: int,
        source: str,
    ) -> None:
        self.inner = inner
        self.stats = stats
        self.reservoir = reservoir
        self.family = family
        self.query_index = query_index
        self.source = source

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: GridProblem,
        g_F: float = 0.0,
        g_B: float = 0.0,
    ) -> float:
        h = self.inner.evaluate(forward, backward, problem, g_F=g_F, g_B=g_B)
        f2f = lb_f2f(forward, backward, g_F, g_B)
        f2e = lb_f2e(forward, backward, problem, g_F, g_B)
        diff = f2f - f2e
        self.stats.add(diff)
        if forward == backward:
            self.stats.n_meeting += 1
        ratio = (f2f / f2e) if f2e > EPS else None
        self.reservoir.add(
            {
                "family": self.family,
                "query_index": self.query_index,
                "source": self.source,
                "u_row": forward.row,
                "u_col": forward.col,
                "v_row": backward.row,
                "v_col": backward.col,
                "g_F": g_F,
                "g_B": g_B,
                "lb_f2f": f2f,
                "lb_f2e": f2e,
                "diff": diff,
                "ratio": ratio,
            }
        )
        return h


def refuse_out_dir(path: Path, *, force: bool) -> str | None:
    if path.exists() and any(path.iterdir()) and not force:
        return (
            f"{path} already exists and is not empty; "
            "pick a new slug or pass --force"
        )
    return None


def _i(row: dict[str, str], key: str) -> int:
    return int(float(row[key]))


def load_frozen(
    csv_name: str, obstacle_count: int | None
) -> dict[tuple[int, str], dict[str, str]]:
    path = STUDY / csv_name
    by: dict[tuple[int, str], dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if obstacle_count is not None and _i(row, "obstacle_count") != obstacle_count:
                continue
            algo = row["algorithm"]
            if algo not in ("sfbds_f2f", "sfbds_f2e"):
                continue
            by[(_i(row, "query_index"), algo)] = row
    return by


def _pick_problem(problems: list[GridProblem], obstacle_count: int | None) -> GridProblem:
    if obstacle_count is None:
        if len(problems) != 1:
            raise ValueError(f"expected one problem, got {len(problems)}")
        return problems[0]
    matched = [p for p in problems if len(p.obstacles) == obstacle_count]
    if len(matched) != 1:
        raise ValueError(
            f"expected one problem with {obstacle_count} obstacles, got {len(matched)}"
        )
    return matched[0]


def _search(algorithm: str, recorder: RecordingHeuristic, problem: GridProblem, timeout: float | None):
    if algorithm == "sfbds_f2f":
        searcher = SFBDSSearcher(recorder)
    elif algorithm == "sfbds_f2e":
        searcher = SFBDSSearcher(recorder, policies=f2e_policies())
    else:
        raise ValueError(algorithm)

    def impl(p: GridProblem, should_stop):
        return searcher.search(p, should_stop=should_stop)

    return run_query(problem, algorithm, timeout_sec=timeout, search_impl=impl)


def _stats_row(prefix: str, stats: BoundStats) -> dict[str, Any]:
    return {
        f"{prefix}n": stats.n,
        f"{prefix}median_diff": stats.median_diff(),
        f"{prefix}mean_diff": stats.mean_diff(),
        f"{prefix}n_f2f_stronger": stats.n_f2f_stronger,
        f"{prefix}n_equal": stats.n_equal,
        f"{prefix}n_f2e_stronger": stats.n_f2e_stronger,
        f"{prefix}frac_f2f_stronger": stats.frac(stats.n_f2f_stronger),
        f"{prefix}frac_equal": stats.frac(stats.n_equal),
        f"{prefix}frac_f2e_stronger": stats.frac(stats.n_f2e_stronger),
    }


def replay_family(
    family: str,
    yaml_rel: str,
    csv_name: str,
    obstacle_count: int | None,
    rng: random.Random,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    config = load_config(ROOT / yaml_rel)
    frozen = load_frozen(csv_name, obstacle_count)
    query_rows: list[dict[str, Any]] = []
    reservoirs = {
        "f2f": Reservoir(SAMPLE_PER_SOURCE, rng),
        "f2e": Reservoir(SAMPLE_PER_SOURCE, rng),
    }
    n_ok = 0
    for idx, query in enumerate(config.queries):
        problems = _problems_for_query(config, query, idx)
        if not problems:
            continue
        problem = _pick_problem(problems, obstacle_count)
        fingerprint = map_fingerprint(
            problem, generator=config.generator, seed=config.seed + idx
        )
        f2f_row = frozen.get((idx, "sfbds_f2f"))
        f2e_row = frozen.get((idx, "sfbds_f2e"))
        if f2f_row is None or f2e_row is None:
            continue
        if f2f_row["map_hash"] != fingerprint or f2e_row["map_hash"] != fingerprint:
            raise ValueError(
                f"{family} q={idx}: map_hash mismatch "
                f"replay={fingerprint} frozen_f2f={f2f_row['map_hash']}"
            )

        pooled = BoundStats()
        source_stats: dict[str, BoundStats] = {}
        for algo, source, inner in (
            ("sfbds_f2f", "f2f", F2FManhattanHeuristic()),
            ("sfbds_f2e", "f2e", F2EPairLowerBound()),
        ):
            stats = BoundStats()
            recorder = RecordingHeuristic(
                inner,
                stats=stats,
                reservoir=reservoirs[source],
                family=family,
                query_index=idx,
                source=source,
            )
            result = _search(algo, recorder, problem, config.timeout_sec)
            frozen_row = f2f_row if algo == "sfbds_f2f" else f2e_row
            want = _i(frozen_row, "expanded")
            got = result.metrics.expanded
            if got != want:
                raise ValueError(
                    f"{family} q={idx} {algo}: expanded mismatch "
                    f"replay={got} frozen={want}"
                )
            want_evals = _i(frozen_row, "heuristic_evals")
            if stats.n != want_evals:
                raise ValueError(
                    f"{family} q={idx} {algo}: heuristic_evals mismatch "
                    f"replay={stats.n} frozen={want_evals}"
                )
            if stats.n != result.metrics.heuristic_evals:
                raise ValueError(
                    f"{family} q={idx} {algo}: recorded evals {stats.n} != "
                    f"metrics.heuristic_evals {result.metrics.heuristic_evals}"
                )
            want_cost = float(frozen_row["solution_cost"])
            got_cost = result.solution_cost
            if got_cost is None or abs(got_cost - want_cost) > EPS:
                raise ValueError(
                    f"{family} q={idx} {algo}: solution_cost mismatch "
                    f"replay={got_cost} frozen={want_cost}"
                )
            source_stats[source] = stats
            for d in stats.diffs:
                pooled.add(d)

        n_ok += 1
        f2f_exp = _i(f2f_row, "expanded")
        f2e_exp = _i(f2e_row, "expanded")
        row: dict[str, Any] = {
            "family": family,
            "query_index": idx,
            "map_hash": fingerprint,
            "obstacle_count": len(problem.obstacles),
            "seed": config.seed,
            "f2f_expanded": f2f_exp,
            "f2e_expanded": f2e_exp,
            "expansion_diff": f2e_exp - f2f_exp,
        }
        row.update(_stats_row("pooled_", pooled))
        row.update(_stats_row("f2f_source_", source_stats["f2f"]))
        row.update(_stats_row("f2e_source_", source_stats["f2e"]))
        query_rows.append(row)
        print(f"  {family} q={idx} expansion_diff={f2e_exp - f2f_exp} pooled_n={pooled.n}", flush=True)

    if n_ok != 30:
        raise ValueError(f"{family}: expected 30 matched queries, got {n_ok}")
    pair_rows = reservoirs["f2f"].items + reservoirs["f2e"].items
    return query_rows, pair_rows


def frozen_expansion_counts(
    csv_name: str, obstacle_count: int | None
) -> tuple[int, int, int, list[int]]:
    """F2F-fewer / F2E-fewer / tie plus query indexes where F2E expanded fewer."""
    frozen = load_frozen(csv_name, obstacle_count)
    n_f2f = n_f2e = n_tie = 0
    f2e_fewer: list[int] = []
    indexes = sorted({idx for idx, _algo in frozen})
    for idx in indexes:
        f2f = frozen.get((idx, "sfbds_f2f"))
        f2e = frozen.get((idx, "sfbds_f2e"))
        if f2f is None or f2e is None:
            continue
        diff = _i(f2e, "expanded") - _i(f2f, "expanded")
        if diff > 0:
            n_f2f += 1
        elif diff < 0:
            n_f2e += 1
            f2e_fewer.append(idx)
        else:
            n_tie += 1
    return n_f2f, n_f2e, n_tie, f2e_fewer


def check_frozen_splits() -> list[str]:
    """Return human-readable freeze checks (empty list = ok)."""
    notes: list[str] = []
    for family, _yaml, csv_name, obstacle_count in FAMILIES:
        n_f2f, n_f2e, n_tie, f2e_fewer = frozen_expansion_counts(csv_name, obstacle_count)
        expected = EXPECTED_SPLITS[family]
        got = (n_f2f, n_f2e, n_tie)
        if got != expected:
            raise ValueError(f"{family}: expansion split {got} != locked {expected}")
        notes.append(f"{family}: F2F-fewer/F2E-fewer/tie = {n_f2f}/{n_f2e}/{n_tie}")
        if family == "nested_64_d45":
            if f2e_fewer != [NESTED_D45_F2E_FEWER_QUERY]:
                raise ValueError(
                    f"nested_64_d45: F2E-fewer queries {f2e_fewer} != "
                    f"[{NESTED_D45_F2E_FEWER_QUERY}]"
                )
            f2f = load_frozen(csv_name, obstacle_count)[
                (NESTED_D45_F2E_FEWER_QUERY, "sfbds_f2f")
            ]
            f2e = load_frozen(csv_name, obstacle_count)[
                (NESTED_D45_F2E_FEWER_QUERY, "sfbds_f2e")
            ]
            diff = _i(f2e, "expanded") - _i(f2f, "expanded")
            if diff != -1:
                raise ValueError(
                    f"nested_64_d45 q={NESTED_D45_F2E_FEWER_QUERY}: "
                    f"expansion_diff {diff} != -1"
                )
            notes.append(
                f"nested_64_d45 q={NESTED_D45_F2E_FEWER_QUERY}: expansion_diff=-1"
            )
    return notes
    if len(xs) < 3:
        return None
    try:
        from scipy.stats import spearmanr

        corr, _p = spearmanr(xs, ys)
        return None if corr is None or math.isnan(float(corr)) else float(corr)
    except Exception:
        return None


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    if len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    try:
        from scipy.stats import spearmanr

        corr, _p = spearmanr(xs, ys)
        return None if corr is None or math.isnan(float(corr)) else float(corr)
    except Exception:
        return None


def family_summaries(query_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in query_rows:
        by[row["family"]].append(row)
    out: list[dict[str, Any]] = []
    for family, rows in by.items():
        exp_diffs = [int(r["expansion_diff"]) for r in rows]
        med_diffs = [float(r["pooled_median_diff"]) for r in rows]
        fracs = [float(r["pooled_frac_f2f_stronger"]) for r in rows]
        n_f2f_fewer = sum(1 for d in exp_diffs if d > 0)
        n_f2e_fewer = sum(1 for d in exp_diffs if d < 0)
        n_tie = sum(1 for d in exp_diffs if d == 0)
        pooled_n = sum(int(r["pooled_n"]) for r in rows)
        n_stronger = sum(int(r["pooled_n_f2f_stronger"]) for r in rows)
        n_equal = sum(int(r["pooled_n_equal"]) for r in rows)
        n_weaker = sum(int(r["pooled_n_f2e_stronger"]) for r in rows)
        untied_med = [m for m, d in zip(med_diffs, exp_diffs) if d != 0]
        untied_exp = [float(d) for d in exp_diffs if d != 0]
        untied_frac = [f for f, d in zip(fracs, exp_diffs) if d != 0]
        out.append(
            {
                "family": family,
                "n_queries": len(rows),
                "seed": rows[0]["seed"],
                "n_f2f_fewer_exp": n_f2f_fewer,
                "n_f2e_fewer_exp": n_f2e_fewer,
                "n_exp_tie": n_tie,
                "median_expansion_diff": float(statistics.median(exp_diffs)),
                "median_of_query_median_diff": float(statistics.median(med_diffs)),
                "mean_of_query_median_diff": float(statistics.mean(med_diffs)),
                "pooled_n": pooled_n,
                "pooled_frac_f2f_stronger": n_stronger / pooled_n if pooled_n else None,
                "pooled_frac_equal": n_equal / pooled_n if pooled_n else None,
                "pooled_frac_f2e_stronger": n_weaker / pooled_n if pooled_n else None,
                "spearman_untied_median_diff_vs_expansion_diff": _spearman(
                    untied_med, untied_exp
                ),
                "spearman_untied_frac_f2f_stronger_vs_expansion_diff": _spearman(
                    untied_frac, untied_exp
                ),
                "n_untied": len(untied_exp),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_plots(query_rows: list[dict[str, Any]], family_rows: list[dict[str, Any]], out: Path) -> None:
    import matplotlib.pyplot as plt

    labels = {
        "open_128": "Open 128",
        "maze_127": "Maze 127",
        "maze_255": "Maze 255",
        "maze_127_braid": "Maze 127 braid",
        "nested_64_d30": "Nested 64 @ 30%",
        "nested_64_d45": "Nested 64 @ 45%",
    }
    order = [r["family"] for r in family_rows]
    stronger = [100.0 * float(r["pooled_frac_f2f_stronger"] or 0) for r in family_rows]
    equal = [100.0 * float(r["pooled_frac_equal"] or 0) for r in family_rows]
    weaker = [100.0 * float(r["pooled_frac_f2e_stronger"] or 0) for r in family_rows]
    names = [labels.get(f, f) for f in order]

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    x = list(range(len(order)))
    ax.bar(x, stronger, label="F2F bound stronger")
    ax.bar(x, equal, bottom=stronger, label="equal")
    ax.bar(
        x,
        weaker,
        bottom=[s + e for s, e in zip(stronger, equal)],
        label="F2E bound stronger",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, ha="right")
    ax.set_ylabel("% of evaluate() pairs (pooled)")
    ax.set_title("Pair lower-bound comparison (same (u,v,g) under both LBs)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "bound_strength_share.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    for family in order:
        pts = [r for r in query_rows if r["family"] == family]
        ax.scatter(
            [float(r["pooled_median_diff"]) for r in pts],
            [int(r["expansion_diff"]) for r in pts],
            s=22,
            alpha=0.75,
            label=labels.get(family, family),
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Median LB_F2F − LB_F2E (evaluate() pairs, pooled)")
    ax.set_ylabel("F2E_expanded − F2F_expanded")
    ax.set_title("Bound advantage vs expansion saving")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "bound_vs_expansion.png", dpi=120)
    plt.close(fig)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="F2F vs F2E pair-bound strength replay")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Lock frozen expansion splits / query 8; do not replay or write.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing non-empty output folder.",
    )
    args = parser.parse_args(argv)

    try:
        notes = check_frozen_splits()
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.check_only:
        for line in notes:
            print(line)
        print("ok")
        return 0

    refused = refuse_out_dir(OUT, force=args.force)
    if refused:
        print(refused, file=sys.stderr)
        return 1

    rng = random.Random(SAMPLE_RNG_SEED)
    query_rows: list[dict[str, Any]] = []
    pair_rows: list[dict[str, Any]] = []
    try:
        for family, yaml_rel, csv_name, obstacle_count in FAMILIES:
            print(f"replaying {family} ...", flush=True)
            q, p = replay_family(family, yaml_rel, csv_name, obstacle_count, rng)
            query_rows.extend(q)
            pair_rows.extend(p)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    family_rows = family_summaries(query_rows)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "query_summary.csv", query_rows)
    write_csv(OUT / "pair_sample.csv", pair_rows)
    write_csv(OUT / "family_summary.csv", family_rows)
    write_plots(query_rows, family_rows, OUT)
    print(f"wrote {OUT}")
    for row in family_rows:
        print(
            f"{row['family']}: exp F2F-fewer/F2E-fewer/tie="
            f"{row['n_f2f_fewer_exp']}/{row['n_f2e_fewer_exp']}/{row['n_exp_tie']} "
            f"median_bound_diff={row['median_of_query_median_diff']:.4g} "
            f"frac_f2f_stronger={row['pooled_frac_f2f_stronger']:.3f} "
            f"frac_f2e_stronger={row['pooled_frac_f2e_stronger']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
