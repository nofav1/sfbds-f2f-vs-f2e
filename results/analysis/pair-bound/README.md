# Pair-bound analysis snapshots

This directory is an **index of snapshots** of official `F2EPairLowerBound` study CSVs (`results/study/pair-bound`). Do not dump `paired.csv` here. Do not mix in [`../legacy/`](../legacy/) runs.

Living notes: [`research_log.md`](research_log.md). Each dated folder has a **generated** `README.md` with tables for that pass — do not edit those by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/YYYY-MM-DD-short-slug
```

## Runs

| Folder | Date | Input | What it is |
| --- | --- | --- | --- |
| [`2026-08-17-baseline-study`](2026-08-17-baseline-study/) | 2026-08-17 | `configs/study/` | First pair-bound F2F vs F2E analysis (corridor 512, maze 127, open 128, nested random 64/128). Nested-random p-values include cost mismatches; do not cite. |
| [`2026-08-17-cost-clean-tests`](2026-08-17-cost-clean-tests/) | 2026-08-17 | same CSVs | Expansion tests exclude cost mismatches. Maze 22/30 cost-clean; 64@30% `n_untied=9` → p null. Plots in this folder still include mismatches. |
| [`2026-08-17-cost-clean-plots`](2026-08-17-cost-clean-plots/) | 2026-08-17 | same CSVs | Same tables; plots omit `cost_mismatch` rows. Cite this folder for figures. |
