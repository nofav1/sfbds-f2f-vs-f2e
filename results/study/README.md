# Study CSVs

Do not write raw CSVs at this directory. Analysis loads `*.csv` only in the folder you pass as `--input-dir` (non-recursive), so pick one subdirectory:

| Folder | F2E formula | Write new runs? |
| --- | --- | --- |
| [`legacy/`](legacy/) | Frozen project-choice gap | No |
| [`pair-bound/`](pair-bound/) | Official `F2EPairLowerBound` | Yes |

```bash
python -m sfbds_compare.analysis --input-dir results/study/legacy --out-dir results/analysis/legacy/YYYY-MM-DD-short-slug
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/YYYY-MM-DD-short-slug
```
