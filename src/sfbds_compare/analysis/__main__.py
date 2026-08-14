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
    args = parser.parse_args(argv)

    raw = load_raw_csvs(args.input_dir)
    if args.experiments:
        allow = set(args.experiments)
        raw = [r for r in raw if r.get("experiment") in allow]
    if not raw:
        print(f"no CSV rows in {args.input_dir}", file=sys.stderr)
        return 1
    paired = pair_rows(raw)
    summary = summarize(paired)
    out = Path(args.out_dir)
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
