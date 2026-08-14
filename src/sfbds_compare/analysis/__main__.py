"""python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/<run-name>"""

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


def _refuse_out_dir(path: Path, *, force: bool) -> Optional[str]:
    if _is_analysis_index_dir(path):
        return (
            f"--out-dir {path} is the analysis index; use a dated slug "
            f"(results/analysis/YYYY-MM-DD-short-slug)"
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
        help="Run folder for this analysis pass (e.g. results/analysis/YYYY-MM-DD-slug). Do not reuse a previous folder.",
    )
    parser.add_argument(
        "--experiment",
        action="append",
        dest="experiments",
        help="Only include this experiment name (repeatable). Default: all CSVs in --input-dir.",
    )
    parser.add_argument("--no-plots", action="store_true")
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
    if not raw:
        print(f"no CSV rows in {args.input_dir}", file=sys.stderr)
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
    readme_path = write_readme(paired, summary, out)
    print(f"wrote {readme_path}")
    if not args.no_plots:
        for path in write_plots(paired, out):
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
