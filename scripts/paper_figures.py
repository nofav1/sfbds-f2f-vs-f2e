"""Camera-ready figures and tables from git study ``*_opt.csv``.

Does not read gitignored analysis ``paired.csv``. Pairing is in-memory via
``sfbds_compare.analysis``. Writes ``docs/final_report/final_version/figures/``.

Sanity: maze 127 is 22/30 F2F-fewer; maze 255 is 26/30.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sfbds_compare.analysis.load import load_raw_csvs
from sfbds_compare.analysis.pair import pair_rows
from sfbds_compare.analysis.stats import expansion_win_counts
from sfbds_compare.analysis.summarize import expansion_test_rows, summarize
STUDY = ROOT / "results" / "study" / "pair-bound"
FAMILY_SUMMARY = (
    ROOT
    / "results"
    / "analysis"
    / "pair-bound"
    / "2026-08-17-heuristic-strength"
    / "family_summary.csv"
)
OUT_DEFAULT = ROOT / "docs" / "final_report" / "final_version" / "figures"
EVAL_COST_SCRIPT = ROOT / "scripts" / "eval_cost_sensitivity.py"

MAZE_127 = "study_maze_127_opt"
MAZE_255 = "study_maze_255_opt"
NESTED_64_D30 = "study_random_64_opt"
NESTED_64_D30_OBS = 1228

GEOGRAPHY = (
    "study_open_128_opt",
    "study_corridor_512_opt",
    MAZE_127,
    NESTED_64_D30,
    "study_random_128_opt",
)
HARDER = (
    MAZE_255,
    "study_random_64_dense_opt",
    "study_random_128_dense_opt",
)
FACTORS = (
    "study_maze_127_far_opt",
    "study_maze_127_braid_opt",
    "study_maze_127_timed_opt",
    "study_maze_255_braid_opt",
    "study_random_64_d50_opt",
    "study_random_64_d52_opt",
    "study_random_128_d45_opt",
    "study_random_128_d45_md48_opt",
)

LABELS = {
    "study_open_128_opt": "Open 128",
    "study_corridor_512_opt": "Corridor 512",
    MAZE_127: "Maze 127",
    MAZE_255: "Maze 255",
    "study_maze_127_far_opt": "Maze 127 far",
    "study_maze_127_braid_opt": "Maze 127 braid",
    "study_maze_127_timed_opt": "Maze 127 timed",
    "study_maze_255_braid_opt": "Maze 255 braid",
    NESTED_64_D30: "Nested 64 (10/20/30%)",
    "study_random_128_opt": "Nested 128 (10/20/30%)",
    "study_random_64_dense_opt": "Nested 64 dense",
    "study_random_128_dense_opt": "Nested 128 dense",
    "study_random_64_d50_opt": "Nested 64 @ 40–50%",
    "study_random_64_d52_opt": "Nested 64 @ 50–52%",
    "study_random_128_d45_opt": "Nested 128 @ 45–50%",
    "study_random_128_d45_md48_opt": "Nested 128 md 48",
}

STRENGTH_LABELS = {
    "open_128": "Open 128",
    "maze_127": "Maze 127",
    "maze_255": "Maze 255",
    "maze_127_braid": "Maze 127 braid",
    "nested_64_d30": "Nested 64 @ 30%",
    "nested_64_d45": "Nested 64 @ 45%",
}


def _load_eval_cost():
    spec = importlib.util.spec_from_file_location("eval_cost_sensitivity", EVAL_COST_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {EVAL_COST_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def experiment_rows(
    paired: Sequence[dict[str, Any]], name: str, *, obstacle_count: Optional[int] = None
) -> list[dict[str, Any]]:
    rows = [r for r in paired if r["experiment"] == name]
    if obstacle_count is not None:
        rows = [r for r in rows if int(r["obstacle_count"]) == obstacle_count]
    return expansion_test_rows(rows)


def win_counts(rows: Sequence[dict[str, Any]]) -> tuple[int, int, int, int]:
    diffs = [float(r["expansion_diff"]) for r in rows if r.get("expansion_diff") is not None]
    n_f2f, n_f2e, n_tie = expansion_win_counts(diffs)
    return n_f2f, n_f2e, n_tie, len(diffs)


def assert_maze_sanity(paired: Sequence[dict[str, Any]]) -> None:
    n_f2f, n_f2e, n_tie, n = win_counts(experiment_rows(paired, MAZE_127))
    if (n_f2f, n_f2e, n_tie, n) != (22, 0, 8, 30):
        raise ValueError(f"maze 127 expected 22/0/8 of 30, got {n_f2f}/{n_f2e}/{n_tie} of {n}")
    n_f2f, n_f2e, n_tie, n = win_counts(experiment_rows(paired, MAZE_255))
    if (n_f2f, n_f2e, n_tie, n) != (26, 0, 4, 30):
        raise ValueError(f"maze 255 expected 26/0/4 of 30, got {n_f2f}/{n_f2e}/{n_tie} of {n}")


def _fmt_p(value: Any) -> str:
    if value is None or value == "":
        return ""
    p = float(value)
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def _write_csv(path: Path, rows: Sequence[MappingLike], fields: Sequence[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


MappingLike = dict[str, Any]


def _setup_mpl() -> Any:
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "legend.fontsize": 7,
            "pdf.fonttype": 42,
            "savefig.bbox": "tight",
            "savefig.dpi": 300,
        }
    )
    return plt


def save_fig(fig: Any, plt: Any, out: Path, stem: str) -> list[Path]:
    written: list[Path] = []
    for suffix in (".pdf", ".png"):
        path = out / f"{stem}{suffix}"
        fig.savefig(path)
        written.append(path)
    plt.close(fig)
    return written


def slice_paired(paired: Sequence[dict[str, Any]], names: Iterable[str]) -> list[dict[str, Any]]:
    allow = set(names)
    return [r for r in paired if r["experiment"] in allow]


def summary_by_experiment(paired: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in summarize(paired):
        if rec.get("group_type") == "experiment":
            out[str(rec["group"])] = rec
    return out


def density_rows(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        dict(rec)
        for rec in summarize(paired)
        if rec.get("group_type") == "obstacle_count" and int(rec.get("n_untied") or 0) >= 10
    ]
    rows.sort(key=lambda r: str(r["group"]))
    for rec in rows:
        rec["wilcoxon_p_holm"] = _fmt_p(rec.get("wilcoxon_p_holm"))
    return rows


def plot_headline(plt: Any, paired: Sequence[dict[str, Any]], out: Path) -> list[Path]:
    specs: list[tuple[str, str, Optional[int]]] = [
        ("study_open_128_opt", "Open 128", None),
        ("study_corridor_512_opt", "Corridor 512", None),
        (MAZE_127, "Maze 127", None),
        (MAZE_255, "Maze 255", None),
        (NESTED_64_D30, "Nested 64 @ 30%", NESTED_64_D30_OBS),
    ]
    labels, f2f, ties, f2e = [], [], [], []
    for name, label, obs in specs:
        n_f2f, n_f2e, n_tie, _n = win_counts(experiment_rows(paired, name, obstacle_count=obs))
        labels.append(label)
        f2f.append(n_f2f)
        ties.append(n_tie)
        f2e.append(n_f2e)
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    y = range(len(labels))
    ax.barh(y, f2f, color="#2c7bb6", label="F2F fewer")
    ax.barh(y, ties, left=f2f, color="#cccccc", label="tie")
    left2 = [a + b for a, b in zip(f2f, ties)]
    ax.barh(y, f2e, left=left2, color="#d7191c", label="F2E fewer")
    ax.set_yticks(list(y), labels)
    ax.set_xlabel("Queries (of 30)")
    ax.set_xlim(0, 30)
    ax.legend(loc="lower right")
    ax.invert_yaxis()
    return save_fig(fig, plt, out, "fig_headline_wins")


def plot_maze_scatter(plt: Any, paired: Sequence[dict[str, Any]], out: Path) -> list[Path]:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), sharex=False, sharey=False)
    for ax, name, title in (
        (axes[0], MAZE_127, "Maze 127"),
        (axes[1], MAZE_255, "Maze 255"),
    ):
        rows = experiment_rows(paired, name)
        x = [r["f2e_expanded"] for r in rows]
        y = [r["f2f_expanded"] for r in rows]
        ax.scatter(x, y, s=14, alpha=0.8, color="#2c7bb6", edgecolors="none")
        hi = max(max(x), max(y)) if x else 1
        ax.plot([0, hi], [0, hi], color="black", linewidth=0.8)
        ax.set_xlabel("F2E pair expansions")
        ax.set_ylabel("F2F pair expansions")
        ax.set_title(title)
        ax.set_aspect("equal", adjustable="box")
    return save_fig(fig, plt, out, "fig_maze_scatter")


def plot_maze_factors(plt: Any, paired: Sequence[dict[str, Any]], out: Path) -> list[Path]:
    specs = [
        (MAZE_127, "127"),
        ("study_maze_127_far_opt", "127 far"),
        ("study_maze_127_braid_opt", "127 braid"),
        (MAZE_255, "255"),
        ("study_maze_255_braid_opt", "255 braid"),
    ]
    labels, heights = [], []
    for name, label in specs:
        n_f2f, _n_f2e, _n_tie, n = win_counts(experiment_rows(paired, name))
        labels.append(f"{label}\n{n_f2f}/{n}")
        heights.append(n_f2f)
    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    ax.bar(range(len(labels)), heights, color="#2c7bb6")
    ax.set_xticks(range(len(labels)), labels)
    ax.set_ylabel("F2F-fewer queries")
    ax.set_ylim(0, 30)
    ax.axhline(0, color="black", linewidth=0.4)
    return save_fig(fig, plt, out, "fig_maze_factors")


def plot_heuristic_strength(plt: Any, out: Path) -> list[Path]:
    rows = list(csv.DictReader(FAMILY_SUMMARY.open(encoding="utf-8")))
    labels, f2f, equal, f2e = [], [], [], []
    for row in rows:
        key = row["family"]
        labels.append(STRENGTH_LABELS.get(key, key))
        f2f.append(100.0 * float(row["pooled_frac_f2f_stronger"]))
        equal.append(100.0 * float(row["pooled_frac_equal"]))
        f2e.append(100.0 * float(row["pooled_frac_f2e_stronger"]))
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    y = range(len(labels))
    ax.barh(y, f2f, color="#2c7bb6", label="F2F stronger")
    ax.barh(y, equal, left=f2f, color="#cccccc", label="equal")
    left2 = [a + b for a, b in zip(f2f, equal)]
    ax.barh(y, f2e, left=left2, color="#d7191c", label="F2E stronger")
    ax.set_yticks(list(y), labels)
    ax.set_xlabel("Share of evaluate() pairs (%)")
    ax.set_xlim(0, 100)
    ax.legend(loc="lower right")
    ax.invert_yaxis()
    return save_fig(fig, plt, out, "fig_heuristic_strength")


def plot_eval_cost(plt: Any, out: Path) -> tuple[list[Path], list[dict[str, Any]]]:
    ecs = _load_eval_cost()
    loaded = ecs.load_all_families()
    all_rows: list[dict[str, Any]] = []
    for family, pairs, _counts in loaded:
        betas = ecs.implied_betas(pairs)
        observed = ecs.median(betas)
        for multiplier in ecs.MULTIPLIERS:
            beta = 0.0 if multiplier == 0.0 else observed * multiplier
            all_rows.append(ecs.summarize_beta(family, pairs, beta, multiplier, observed))
    labels = {
        "maze_127": "Maze 127",
        "maze_255": "Maze 255",
        "nested_64_d30": "Nested 64 @ 30%",
    }
    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    for family, label in labels.items():
        fam = [r for r in all_rows if r["family"] == family]
        xs = [float(r["beta_sec_per_eval"]) for r in fam if float(r["beta_sec_per_eval"]) > 0]
        ys = [float(r["median_T_ratio"]) for r in fam if float(r["beta_sec_per_eval"]) > 0]
        ax.plot(xs, ys, marker="o", markersize=3.5, linewidth=1.2, label=label)
    ax.axhline(1.0, color="black", linewidth=0.8)
    ax.set_xscale("log")
    ax.set_xlabel(r"Assumed eval cost $\beta$ (s/eval); log $x$ omits $\beta=0$")
    ax.set_ylabel(r"Median $T_{\mathrm{F2F}}/T_{\mathrm{F2E}}$")
    ax.legend()
    ax.text(
        0.03,
        0.08,
        r"$\beta=0$ is in the table (secondary)",
        transform=ax.transAxes,
        fontsize=7,
    )
    written = save_fig(fig, plt, out, "fig_eval_cost")
    return written, all_rows


def table_headline(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    geo = summary_by_experiment(slice_paired(paired, GEOGRAPHY))
    harder = summary_by_experiment(slice_paired(paired, HARDER))
    nested_d30 = win_counts(
        experiment_rows(paired, NESTED_64_D30, obstacle_count=NESTED_64_D30_OBS)
    )
    rows: list[dict[str, Any]] = []
    for name, stats in (
        ("study_open_128_opt", geo.get("study_open_128_opt")),
        ("study_corridor_512_opt", geo.get("study_corridor_512_opt")),
        (MAZE_127, geo.get(MAZE_127)),
        (MAZE_255, harder.get(MAZE_255)),
    ):
        if stats is None:
            raise ValueError(f"missing experiment stats for {name}")
        rows.append(
            {
                "family": LABELS[name],
                "experiment": name,
                "n_test": stats["n_test"],
                "n_f2f_fewer": stats["n_f2f_fewer"],
                "n_f2e_fewer": stats["n_f2e_fewer"],
                "n_tie": stats["n_tie"],
                "median_saving_pct": stats["median_expansion_saving_pct"],
                "wilcoxon_p_holm": _fmt_p(stats.get("wilcoxon_p_holm")),
                "note": "30 maps",
            }
        )
    n_f2f, n_f2e, n_tie, n = nested_d30
    dens = [
        rec
        for rec in summarize(slice_paired(paired, GEOGRAPHY))
        if rec.get("group_type") == "obstacle_count"
        and str(rec["group"]).startswith(f"{NESTED_64_D30}::")
        and "1228" in str(rec["group"])
    ]
    p_holm = _fmt_p(dens[0].get("wilcoxon_p_holm")) if dens else ""
    rows.append(
        {
            "family": "Nested 64 @ 30%",
            "experiment": NESTED_64_D30,
            "n_test": n,
            "n_f2f_fewer": n_f2f,
            "n_f2e_fewer": n_f2e,
            "n_tie": n_tie,
            "median_saving_pct": median(
                [
                    float(r["expansion_saving_pct"])
                    for r in experiment_rows(
                        paired, NESTED_64_D30, obstacle_count=NESTED_64_D30_OBS
                    )
                    if r.get("expansion_saving_pct") is not None
                ]
            ),
            "wilcoxon_p_holm": p_holm,
            "note": "30 maps; one prefix of nested 64",
        }
    )
    return rows


def table_maze_factors(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    geo = summary_by_experiment(slice_paired(paired, GEOGRAPHY))
    harder = summary_by_experiment(slice_paired(paired, HARDER))
    fac = summary_by_experiment(slice_paired(paired, FACTORS))
    order = [
        (MAZE_127, geo),
        ("study_maze_127_far_opt", fac),
        ("study_maze_127_braid_opt", fac),
        (MAZE_255, harder),
        ("study_maze_255_braid_opt", fac),
    ]
    rows: list[dict[str, Any]] = []
    for name, src in order:
        stats = src[name]
        rows.append(
            {
                "family": LABELS[name],
                "experiment": name,
                "n_test": stats["n_test"],
                "n_f2f_fewer": stats["n_f2f_fewer"],
                "n_f2e_fewer": stats["n_f2e_fewer"],
                "n_tie": stats["n_tie"],
                "median_saving_pct": stats["median_expansion_saving_pct"],
                "wilcoxon_p_holm": _fmt_p(stats.get("wilcoxon_p_holm")),
            }
        )
    return rows


def table_generated_peak(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    names = (
        "study_open_128_opt",
        "study_corridor_512_opt",
        MAZE_127,
        MAZE_255,
        "study_maze_127_braid_opt",
        NESTED_64_D30,
    )
    rows: list[dict[str, Any]] = []
    for name in names:
        obs = NESTED_64_D30_OBS if name == NESTED_64_D30 else None
        test = experiment_rows(paired, name, obstacle_count=obs)
        if not test:
            continue
        rows.append(
            {
                "family": "Nested 64 @ 30%" if obs else LABELS[name],
                "experiment": name,
                "n": len(test),
                "median_f2f_generated": median(int(r["f2f_generated"]) for r in test),
                "median_f2e_generated": median(int(r["f2e_generated"]) for r in test),
                "median_f2f_peak_open": median(int(r["f2f_peak_open"]) for r in test),
                "median_f2e_peak_open": median(int(r["f2e_peak_open"]) for r in test),
            }
        )
    return rows


def table_timed(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = experiment_rows(paired, "study_maze_127_timed_opt")
    untied = [r for r in rows if r.get("expansion_diff") not in (None, 0)]
    faster = [
        r
        for r in untied
        if r.get("runtime_ratio") is not None and float(r["runtime_ratio"]) < 1.0
    ]
    ratios = [float(r["runtime_ratio"]) for r in untied if r.get("runtime_ratio") is not None]
    return [
        {
            "experiment": "study_maze_127_timed_opt",
            "n_expansion_untied": len(untied),
            "n_f2f_faster": len(faster),
            "median_runtime_ratio": median(ratios) if ratios else "",
            "note": "secondary; expansions from first successful repeat",
        }
    ]


def table_instance_matrix(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    by_exp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in paired:
        by_exp[str(row["experiment"])].append(row)
    rows: list[dict[str, Any]] = []
    for name in sorted(by_exp):
        group = by_exp[name]
        queries = {int(r["query_index"]) for r in group}
        sample = group[0]
        nested = any(bool(r.get("nested_density")) for r in group)
        n_densities = (
            len({int(r["obstacle_count"]) for r in group}) if nested else 1
        )
        rows.append(
            {
                "experiment": name,
                "family": LABELS.get(name, name),
                "height": sample["height"],
                "width": sample["width"],
                "seed": sample["seed"],
                "n_queries": len(queries),
                "n_maps": len(group),
                "n_densities": n_densities,
            }
        )
    return rows


def write_readme(
    out: Path,
    *,
    headline: Sequence[dict[str, Any]],
    written: Sequence[Path],
) -> None:
    lines = [
        "# Paper figures (generated)",
        "",
        "Produced by `python scripts/paper_figures.py`. Do not edit by hand.",
        "Inputs: `results/study/pair-bound/*_opt.csv` and committed",
        "`family_summary.csv`. Does **not** read gitignored analysis `paired.csv`.",
        "",
        "## Sanity",
        "",
        "- Maze 127 (`study_maze_127_opt`): **22/30** F2F-fewer.",
        "- Maze 255 (`study_maze_255_opt`): **26/30** F2F-fewer.",
        "",
        "## Headline win counts",
        "",
        "| Family | F2F fewer | F2E fewer | ties | Holm p |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in headline:
        lines.append(
            f"| {row['family']} | {row['n_f2f_fewer']} | {row['n_f2e_fewer']} | "
            f"{row['n_tie']} | {row['wilcoxon_p_holm'] or 'null'} |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
        ]
    )
    for path in written:
        lines.append(f"- `{path.name}`")
    lines.extend(
        [
            "",
            "Nested 64 @ 30% (seed 110) and nested 64 @ 45% (seed 210) in the",
            "heuristic-strength figure are different maps, not a paired density step.",
            "Do not cite Spearman from `family_summary.csv` as a savings ranking.",
            "",
            "`n_densities` is the nested prefix count. Maze/open/corridor rows are 1",
            "(unique wall counts from S/G carving are not densities).",
            "",
            "Eval-cost figure is **secondary**. The log-x curve omits beta=0;",
            "that point is in `table_eval_cost.csv`.",
            "",
        ]
    )
    (out / "README.md").write_text("\n".join(lines), encoding="utf-8")


def refuse_out_dir(path: Path, *, force: bool) -> Optional[str]:
    if path.exists() and any(path.iterdir()) and not force:
        return f"{path} is not empty; pass --force to overwrite"
    return None


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build final-report figures from git *_opt CSVs")
    parser.add_argument("--input-dir", default=str(STUDY))
    parser.add_argument("--out-dir", default=str(OUT_DEFAULT))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    out = Path(args.out_dir)
    refused = refuse_out_dir(out, force=args.force)
    if refused:
        print(refused, file=sys.stderr)
        return 1
    if not FAMILY_SUMMARY.is_file():
        print(f"missing {FAMILY_SUMMARY}", file=sys.stderr)
        return 1

    raw = load_raw_csvs(args.input_dir)
    raw = [r for r in raw if str(r.get("experiment", "")).endswith("_opt")]
    if not raw:
        print(f"no *_opt rows in {args.input_dir}", file=sys.stderr)
        return 1
    paired = pair_rows(raw)
    try:
        assert_maze_sanity(paired)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    out.mkdir(parents=True, exist_ok=True)
    plt = _setup_mpl()
    written: list[Path] = []
    written.extend(plot_headline(plt, paired, out))
    written.extend(plot_maze_scatter(plt, paired, out))
    written.extend(plot_maze_factors(plt, paired, out))
    written.extend(plot_heuristic_strength(plt, out))
    eval_paths, eval_rows = plot_eval_cost(plt, out)
    written.extend(eval_paths)

    headline = table_headline(paired)
    factors = table_maze_factors(paired)
    nested = density_rows(paired)
    generated = table_generated_peak(paired)
    timed = table_timed(paired)
    instances = table_instance_matrix(paired)

    table_specs: list[tuple[str, Sequence[dict[str, Any]], Sequence[str]]] = [
        (
            "table_headline.csv",
            headline,
            (
                "family",
                "experiment",
                "n_test",
                "n_f2f_fewer",
                "n_f2e_fewer",
                "n_tie",
                "median_saving_pct",
                "wilcoxon_p_holm",
                "note",
            ),
        ),
        (
            "table_maze_factors.csv",
            factors,
            (
                "family",
                "experiment",
                "n_test",
                "n_f2f_fewer",
                "n_f2e_fewer",
                "n_tie",
                "median_saving_pct",
                "wilcoxon_p_holm",
            ),
        ),
        (
            "table_nested_density.csv",
            nested,
            (
                "group",
                "n_solved",
                "n_test",
                "n_untied",
                "n_f2f_fewer",
                "n_f2e_fewer",
                "n_tie",
                "median_expansion_saving_pct",
                "wilcoxon_p_holm",
            ),
        ),
        (
            "table_generated_peak_open.csv",
            generated,
            (
                "family",
                "experiment",
                "n",
                "median_f2f_generated",
                "median_f2e_generated",
                "median_f2f_peak_open",
                "median_f2e_peak_open",
            ),
        ),
        (
            "table_timed_runtime.csv",
            timed,
            (
                "experiment",
                "n_expansion_untied",
                "n_f2f_faster",
                "median_runtime_ratio",
                "note",
            ),
        ),
        (
            "table_instance_matrix.csv",
            instances,
            (
                "experiment",
                "family",
                "height",
                "width",
                "seed",
                "n_queries",
                "n_maps",
                "n_densities",
            ),
        ),
        (
            "table_eval_cost.csv",
            eval_rows,
            (
                "family",
                "beta_sec_per_eval",
                "beta_over_observed",
                "median_T_ratio",
                "n_f2f_cheaper",
                "n_f2e_cheaper",
            ),
        ),
    ]
    for name, rows, fields in table_specs:
        path = out / name
        _write_csv(path, rows, fields)
        written.append(path)

    write_readme(out, headline=headline, written=written)
    written.append(out / "README.md")
    print("maze 127: 22/30 F2F-fewer")
    print("maze 255: 26/30 F2F-fewer")
    for path in written:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
