"""python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/<run-name>"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from sfbds_compare.analysis.load import load_raw_csvs
from sfbds_compare.analysis.pair import pair_rows
from sfbds_compare.analysis.plots import write_plots
from sfbds_compare.analysis.report import write_readme
from sfbds_compare.analysis.summarize import summarize

_ANALYSIS_INDEX_MARKER = "index of snapshots"

OFFICIAL_OPT_EXPERIMENTS = frozenset(
    {
        "study_corridor_512_opt",
        "study_maze_127_opt",
        "study_open_128_opt",
        "study_random_64_opt",
        "study_random_128_opt",
    }
)


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _is_analysis_index_dir(path: Path) -> bool:
    resolved = path.resolve()
    if resolved.name == "analysis" and resolved.parent.name == "results":
        return True
    readme = resolved / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8", errors="replace").lower()
        if _ANALYSIS_INDEX_MARKER in text:
            return True
    return False


def _mixed_opt_and_prefix(raw: Sequence[Mapping[str, Any]]) -> Optional[str]:
    """Refuse one analysis that mixes pre-fix pair-bound rows with ``*_opt``."""

    names = {r.get("experiment") for r in raw}
    opt = {n for n in names if isinstance(n, str) and n.endswith("_opt")}
    other = names - opt
    if opt and other:
        return (
            "refusing mixed pre-fix and *_opt experiments in one analysis; "
            "pass --experiment for all *_opt names (or only pre-fix names)"
        )
    return None


def _incomplete_official_opt(
    raw: Sequence[Mapping[str, Any]], *, allow_subset: bool
) -> Optional[str]:
    """Official reopen baseline is exactly the five ``*_opt`` stems.

    ``--allow-opt-subset`` permits a follow-up-only ``*_opt`` slice. It does not
    permit mixing those five with extras, or a partial official set plus a
    follow-up.
    """

    names = {r.get("experiment") for r in raw}
    opt = {n for n in names if isinstance(n, str) and n.endswith("_opt")}
    if not opt:
        return None
    official = opt & OFFICIAL_OPT_EXPERIMENTS
    if official and opt != OFFICIAL_OPT_EXPERIMENTS:
        return (
            "refusing mixed official *_opt baseline with a follow-up or partial "
            "official set; analyze the five official _opt stems alone, or pass "
            "--allow-opt-subset for a follow-up-only slice"
        )
    if opt == OFFICIAL_OPT_EXPERIMENTS:
        return None
    if not allow_subset:
        return (
            "refusing partial *_opt analysis of the official reopen baseline; "
            "pass --experiment for all five official _opt names, or --allow-opt-subset"
        )
    return None


def _refuse_out_dir(path: Path, *, force: bool) -> Optional[str]:
    if _is_analysis_index_dir(path):
        return (
            f"--out-dir {path} is the analysis index; use a dated slug "
            f"(results/analysis/pair-bound/YYYY-MM-DD-short-slug)"
        )
    if path.exists() and any(path.iterdir()) and not force:
        return (
            f"--out-dir {path} already exists and is not empty; "
            "pick a new slug or pass --force"
        )
    return None


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Paired F2F vs F2E analysis")
    parser.add_argument("--input-dir", required=True, help="Directory of raw study CSVs")
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Run folder for this analysis pass (e.g. results/analysis/pair-bound/YYYY-MM-DD-slug). Do not reuse a previous folder.",
    )
    parser.add_argument(
        "--experiment",
        action="append",
        dest="experiments",
        help="Only include this experiment name (repeatable). Default: all CSVs in --input-dir.",
    )
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument(
        "--allow-opt-subset",
        action="store_true",
        help=(
            "Allow a follow-up-only *_opt slice (not the five official stems). "
            "Does not allow mixing the official five with follow-up *_opt names."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing non-empty --out-dir (never the analysis index).",
    )
    args = parser.parse_args(argv)

    out = Path(args.out_dir)
    refused = _refuse_out_dir(out, force=args.force)
    if refused:
        print(refused, file=sys.stderr)
        return 1
    raw = load_raw_csvs(args.input_dir)
    if args.experiments:
        allow = set(args.experiments)
        raw = [r for r in raw if r.get("experiment") in allow]
    mixed = _mixed_opt_and_prefix(raw)
    if mixed:
        print(mixed, file=sys.stderr)
        return 1
    incomplete = _incomplete_official_opt(
        raw, allow_subset=args.allow_opt_subset
    )
    if incomplete:
        print(incomplete, file=sys.stderr)
        return 1
    if not raw:
        hint = f"no CSV rows in {args.input_dir}"
        root = Path(args.input_dir)
        if root.is_dir():
            subdirs = [p.name for p in sorted(root.iterdir()) if p.is_dir()]
            if subdirs:
                hint += (
                    f" (non-recursive glob; pass one subdirectory as --input-dir, "
                    f"not a mix: {', '.join(subdirs)})"
                )
        print(hint, file=sys.stderr)
        return 1
    paired = pair_rows(raw)
    summary = summarize(paired)
    paired_path = out / "paired.csv"
    summary_path = out / "summary.csv"
    stats_path = out / "stats.csv"
    _write_csv(paired_path, paired)
    _write_csv(summary_path, summary)
    _write_csv(stats_path, summary)
    print(f"wrote {paired_path} ({len(paired)} paired rows)")
    print(f"wrote {summary_path}")
    print(f"wrote {stats_path}")
    readme_path = write_readme(
        paired,
        summary,
        out,
        input_dir=args.input_dir,
        experiments=tuple(args.experiments) if args.experiments else None,
        allow_opt_subset=args.allow_opt_subset,
    )
    print(f"wrote {readme_path}")
    if not args.no_plots:
        for path in write_plots(paired, out):
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
