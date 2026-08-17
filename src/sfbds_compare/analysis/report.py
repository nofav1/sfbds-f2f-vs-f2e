"""Generate README.md inside an analysis run folder from paired rows and summary stats."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Sequence

from sfbds_compare.analysis.summarize import nested_density_group_key


def _fmt_int(value: Any) -> str:
    if value is None or value == "":
        return "—"
    return str(int(value))


def _fmt_pct(value: Any, digits: int = 1) -> str:
    if value is None or value == "":
        return "—"
    return f"{float(value):.{digits}f}%"


def _fmt_float(value: Any, digits: int = 3) -> str:
    if value is None or value == "":
        return "—"
    return f"{float(value):.{digits}f}"


def _fmt_p(value: Any) -> str:
    if value is None or value == "":
        return "null"
    p = float(value)
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    line = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([line, sep, *body])


def _groups(summary: Sequence[dict[str, Any]], group_type: str) -> list[dict[str, Any]]:
    return [r for r in summary if r.get("group_type") == group_type]


def _result_row(rec: dict[str, Any], group_label: str) -> list[str]:
    note = str(rec.get("note") or "")
    tested = rec.get("wilcoxon_p_raw") not in (None, "")
    skipped = "skipped" in note.lower()
    if skipped:
        claim = "tests skipped (see note)"
    elif not tested:
        claim = "p null (too few untied pairs)"
    else:
        p = float(rec["wilcoxon_p_raw"])
        rb = rec.get("rank_biserial")
        direction = "F2F fewer expansions" if rb is None or float(rb) > 0 else "F2E fewer expansions"
        claim = f"{direction}; p={_fmt_p(p)}"
    return [
        group_label,
        _fmt_int(rec.get("n_solved")),
        _fmt_int(rec.get("n_test")),
        _fmt_int(rec.get("n_f2f_fewer")),
        _fmt_int(rec.get("n_f2e_fewer")),
        _fmt_int(rec.get("n_tie")),
        _fmt_pct(rec.get("median_expansion_saving_pct")),
        _fmt_p(rec.get("wilcoxon_p_holm") if rec.get("wilcoxon_p_holm") not in (None, "") else rec.get("wilcoxon_p_raw")),
        _fmt_float(rec.get("rank_biserial"), 2),
        claim,
    ]


_RESULT_HEADERS = [
    "group",
    "n_solved",
    "n_test",
    "F2F fewer",
    "F2E fewer",
    "ties",
    "median saving %",
    "p (Holm if planned)",
    "rank-biserial",
    "read as",
]


def _experiment_counts(paired: Sequence[dict[str, Any]]) -> list[list[str]]:
    counts = Counter(str(r["experiment"]) for r in paired)
    meta: dict[str, tuple[str, bool]] = {}
    for row in paired:
        meta[str(row["experiment"])] = (
            str(row["map_family"]),
            _as_bool(row.get("nested_density")),
        )
    rows = []
    for name in sorted(counts):
        family, nested = meta[name]
        rows.append(
            [
                name,
                str(counts[name]),
                family,
                "yes (density-eligible)" if nested else "no",
            ]
        )
    return rows


def _maze_runtime_slice(paired: Sequence[dict[str, Any]]) -> str:
    """Wall-clock on maze pairs where expansions already differ (not a primary test)."""

    maze = [
        r
        for r in paired
        if r.get("map_family") == "maze"
        and _as_bool(r.get("solved"))
        and not _as_bool(r.get("cost_mismatch"))
        and r.get("expansion_diff") not in (None, 0, "0")
        and r.get("runtime_ratio") is not None
        and r.get("runtime_ratio") != ""
    ]
    if not maze:
        return "_No solved maze pairs with a nonzero expansion_diff in this run._"
    ratios = [float(r["runtime_ratio"]) for r in maze]
    n = len(ratios)
    n_f2f_faster = sum(1 for x in ratios if x < 1.0)
    n_f2e_faster = sum(1 for x in ratios if x > 1.0)
    n_tie = n - n_f2f_faster - n_f2e_faster
    srt = sorted(ratios)
    mid = srt[n // 2] if n % 2 else 0.5 * (srt[n // 2 - 1] + srt[n // 2])
    mean = sum(ratios) / n
    return "\n".join(
        [
            "These rows are **exploratory**. Expansions remain the primary claim; "
            "runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).",
            "",
            f"- Untied maze pairs with both times: **{n}**",
            f"- F2F faster wall-clock: **{n_f2f_faster}**; F2E faster: **{n_f2e_faster}**; "
            f"equal: **{n_tie}**",
            f"- Median runtime_ratio: **{_fmt_float(mid, 3)}**; mean: **{_fmt_float(mean, 3)}**",
        ]
    )


def _density_label(paired: Sequence[dict[str, Any]], group: str) -> str:
    matches = [
        r
        for r in paired
        if nested_density_group_key(r) == group
    ]
    if not matches:
        return group
    row = matches[0]
    count = int(row["obstacle_count"])
    label = row.get("obstacle_density_label")
    size = row.get("size")
    experiment = row.get("experiment")
    prefix = f"{experiment}: " if experiment else ""
    if label is None or size is None:
        return f"{prefix}{count} obstacles"
    return f"{prefix}{count} obstacles (~{float(label):.2f} on {size}×{size})"


def _headline(
    summary: Sequence[dict[str, Any]], paired: Sequence[dict[str, Any]]
) -> list[str]:
    bullets: list[str] = []
    for rec in _groups(summary, "map_family"):
        name = rec["group"]
        n_tie = int(rec.get("n_tie") or 0)
        n_solved = int(rec.get("n_solved") or 0)
        n_f2f = int(rec.get("n_f2f_fewer") or 0)
        n_f2e = int(rec.get("n_f2e_fewer") or 0)
        if name == "random":
            note = str(rec.get("note") or "")
            if "skipped" in note.lower():
                bullets.append(
                    f"**Random (all files):** {n_solved} solved pairs; "
                    f"{n_f2f} F2F-fewer, {n_f2e} F2E-fewer, {n_tie} ties "
                    f"(n_test={_fmt_int(rec.get('n_test'))}). "
                    "Wilcoxon is skipped on this pooled group; use nested density rows below."
                )
                continue
        if n_tie == n_solved and n_solved:
            bullets.append(
                f"**{name.capitalize()}:** F2F and F2E tied on all {n_solved} solved pairs "
                "(too few untied pairs for a Wilcoxon p-value)."
            )
        elif n_f2f and not n_f2e:
            bullets.append(
                f"**{name.capitalize()}:** F2F expanded fewer pairs on {n_f2f}/{n_solved} "
                f"solved maps ({_fmt_pct(rec.get('pct_f2f_fewer'))}); "
                f"Holm p={_fmt_p(rec.get('wilcoxon_p_holm'))}."
            )
        else:
            bullets.append(
                f"**{name.capitalize()}:** {n_f2f} F2F-fewer, {n_f2e} F2E-fewer, {n_tie} ties "
                f"(n_solved={n_solved})."
            )
    dens = _groups(summary, "obstacle_count")
    if dens:
        eligible = [r for r in dens if int(r.get("n_untied") or 0) >= 10]
        if eligible:
            names = ", ".join(
                _density_label(paired, str(r["group"])) for r in eligible
            )
            bullets.append(
                f"**Nested density tests with n_untied ≥ 10:** obstacle_count {{{names}}}. "
                "Other density levels had too many ties for a p-value."
            )
        else:
            bullets.append(
                "**Nested density:** no obstacle_count group had 10+ untied pairs, "
                "so Wilcoxon p-values are null; win counts and median saving % still apply."
            )
    overall = _groups(summary, "overall_random")
    if overall:
        rec = overall[0]
        bullets.append(
            f"**Overall nested random:** { _fmt_int(rec.get('n_solved')) } maps from "
            f"{ _fmt_int(rec.get('n_test')) } families (median expansion_diff per family). "
            f"Untied={_fmt_int(rec.get('n_untied'))}."
            + (
                " Do not cite a pooled p here; use the per-experiment density table."
                if "multiple nested experiments" in str(rec.get("note") or "")
                else ""
            )
        )
    return bullets


def _pooled_random_skip_sentence(summary: Sequence[dict[str, Any]]) -> str:
    recs = [
        r
        for r in summary
        if r.get("group_type") == "map_family" and r.get("group") == "random"
    ]
    if not recs:
        return ""
    note = str(recs[0].get("note") or "")
    if "mixes nested and independent" in note:
        return (
            "Pooled `random` mixes nested and independent files, "
            "so tests are skipped there on purpose."
        )
    if "skipped on pooled nested random" in note or "skipped on this pooled group" in note:
        return (
            "Pooled `random` collapses nested densities (`n_test` ≠ `n_solved`), "
            "so tests are skipped there on purpose; use the per-experiment density table."
        )
    return ""


def _cli_path(value: str | Path | None, default: str) -> str:
    if value is None:
        return default
    return Path(value).as_posix()


def format_analysis_command(
    *,
    input_dir: str | Path | None = None,
    out_dir: str | Path | None = None,
    experiments: Sequence[str] | None = None,
    allow_opt_subset: bool = False,
) -> str:
    """Reproduce the analysis CLI for this run."""

    parts = [
        "python -m sfbds_compare.analysis",
        f"--input-dir {_cli_path(input_dir, 'results/study/pair-bound')}",
        f"--out-dir {_cli_path(out_dir, 'results/analysis/pair-bound/<run-name>')}",
    ]
    if experiments:
        for name in experiments:
            parts.append(f"--experiment {name}")
    if allow_opt_subset:
        parts.append("--allow-opt-subset")
    return " ".join(parts)


def render_readme(
    paired: Sequence[dict[str, Any]],
    summary: Sequence[dict[str, Any]],
    *,
    input_dir: str | Path | None = None,
    out_dir: str | Path | None = None,
    experiments: Sequence[str] | None = None,
    allow_opt_subset: bool = False,
) -> str:
    """Markdown report for one analysis run."""

    n_paired = len(paired)
    n_solved = sum(1 for r in paired if _as_bool(r.get("solved")))
    n_timeout = sum(1 for r in paired if _as_bool(r.get("timed_out")))
    n_nested = sum(1 for r in paired if _as_bool(r.get("nested_density")))
    n_mismatch = sum(1 for r in paired if _as_bool(r.get("cost_mismatch")))
    families = sorted({str(r["map_family"]) for r in paired})
    bullets = "\n".join(f"- {b}" for b in _headline(summary, paired))

    family_table = _md_table(
        _RESULT_HEADERS,
        [_result_row(r, str(r["group"])) for r in _groups(summary, "map_family")],
    )
    size_table = _md_table(
        _RESULT_HEADERS,
        [_result_row(r, str(r["group"])) for r in _groups(summary, "size")],
    )
    dens_rows = _groups(summary, "obstacle_count")
    dens_table = (
        _md_table(
            _RESULT_HEADERS,
            [_result_row(r, _density_label(paired, str(r["group"]))) for r in dens_rows],
        )
        if dens_rows
        else "_No nested-density experiments in this run, so there are no density-factor tests._"
    )
    overall_rows = _groups(summary, "overall_random")
    overall_table = (
        _md_table(
            _RESULT_HEADERS,
            [_result_row(r, "nested random families") for r in overall_rows],
        )
        if overall_rows
        else "_No nested-density experiments in this run._"
    )
    detour_rows = _groups(summary, "detour_bucket")
    detour_table = (
        _md_table(
            _RESULT_HEADERS,
            [_result_row(r, str(r["group"])) for r in detour_rows],
        )
        if detour_rows
        else "_No detour buckets._"
    )
    exp_table = _md_table(
        ["experiment", "paired rows", "map family", "nested density"],
        _experiment_counts(paired),
    )
    maze_runtime = _maze_runtime_slice(paired)
    pooled_random_note = _pooled_random_skip_sentence(summary)
    pooled_random_block = f"\n{pooled_random_note}\n" if pooled_random_note else ""
    command = format_analysis_command(
        input_dir=input_dir,
        out_dir=out_dir,
        experiments=experiments,
        allow_opt_subset=allow_opt_subset,
    )
    mix_note = ""
    if not experiments:
        mix_note = (
            "\n\nIf `--input-dir` contains both pre-fix and `*_opt` CSVs, pass "
            "`--experiment` for only `*_opt` names or only pre-fix names "
            "(the CLI refuses a mix)."
        )

    return f"""# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
{command}
```{mix_note}

## Headline

{bullets}

Coverage of this run: **{n_paired}** paired instances, **{n_solved}** solved, **{n_timeout}** timed out, **{n_nested}** nested-density rows, map families {", ".join(families)}. Cost mismatches (F2F / F2E / A* when A* succeeded): **{n_mismatch}**.

## What the files are

| File | Role |
| --- | --- |
| `paired.csv` | One row per instance: F2F vs F2E on the same map (`pair_id` = family + `map_hash`). A* is a sidecar (cost / success), not mixed into expansion savings. |
| `summary.csv` / `stats.csv` | Same grouped table (descriptives + tests). Identical copies. |
| `expansions_scatter.png` | F2F pair expansions vs F2E (line of equality). Cost-clean solved rows only. |
| `saving_by_family.png` | Expansion saving % by map family. Cost-clean solved rows only. |
| `saving_by_density.png` | Expansion saving % by `obstacle_count` for **nested** random maps only. Cost-clean solved rows only. |
| `saving_vs_detour.png` | Saving % vs detour ratio. Cost-clean solved rows only. |
| `runtime_ratio.png` | Histogram of F2F/F2E runtime. Cost-clean solved rows only. |
| `forward_backward.png` | Forward vs backward pair expansions. Cost-clean solved rows only. |

## How to read the numbers

- **Pair expansions only.** A* `expanded` is states; SFBDS `expanded` is pairs. Saving % is `(F2E − F2F) / F2E × 100`. Positive means F2F expanded fewer pairs.
- **Solved pair** = both SFBDS succeeded and neither timed out. Timeouts stay in `paired.csv` with null diffs; they are excluded from means, win %, and tests.
- **`cost_mismatch`** = F2F, F2E, or successful A* disagree on solution cost. Those rows stay in `paired.csv` but are **excluded from expansion tests** (Wilcoxon, sign, F2F-fewer / F2E-fewer / ties, expansion saving %) **and from plots**.
- **`n_solved`** = descriptive sample. **`n_test`** = Wilcoxon sample after collapsing nested `family_id`s (median `expansion_diff` per family). If they differ, densities of the same query were not treated as independent n. **F2F fewer / F2E fewer / ties** in the tables are counted on the same units as `n_test` (families after collapse, maps otherwise).
- **Primary test:** two-sided Wilcoxon on `expansion_diff = F2E − F2F`. **Confirmatory:** sign test on who expanded fewer, ties dropped. If `n_untied < 10`, p is **null** (not a missing file). That is expected when F2F and F2E almost always tie (open, corridor).
- **Rank-biserial** > 0 means F2F fewer expansions on the untied pairs.
- **Holm** is within a planned family (map families together; nested density groups within one experiment; size groups together). Detour buckets are exploratory: raw p only.
- **Nested density:** nested random experiments share start/goal across density prefixes. Independent `*_d10/d20/d30` CSVs are kept for F2F vs F2E pairing but **do not** enter `obstacle_count` tests, `overall_random`, or `saving_by_density.png`. Density tests are keyed by experiment, grid size, and `obstacle_count` so two configs that share a prefix count are not pooled.

## Experiments in this run

{exp_table}

## Map family

{family_table}
{pooled_random_block}
## Nested density (eligible maps only)

{dens_table}

### Overall nested random (one median per family)

{overall_table}

## Size

{size_table}

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

{maze_runtime}

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

{detour_table}
"""


def write_readme(
    paired: Sequence[dict[str, Any]],
    summary: Sequence[dict[str, Any]],
    out_dir: str | Path,
    *,
    input_dir: str | Path | None = None,
    experiments: Sequence[str] | None = None,
    allow_opt_subset: bool = False,
) -> Path:
    path = Path(out_dir) / "README.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        render_readme(
            paired,
            summary,
            input_dir=input_dir,
            out_dir=out_dir,
            experiments=experiments,
            allow_opt_subset=allow_opt_subset,
        ),
        encoding="utf-8",
    )
    return path
