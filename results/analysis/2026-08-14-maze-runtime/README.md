# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/<run-name>
```

## Headline

- **Maze:** F2F expanded fewer pairs on 21/30 solved maps (70.0%); Holm p=9.54e-07.

Coverage of this run: **30** paired instances, **30** solved, **0** timed out, **0** nested-density rows, map families maze. Cost mismatches (F2F vs F2E solution cost): **0**.

## What the files are

| File | Role |
| --- | --- |
| `paired.csv` | One row per instance: F2F vs F2E on the same map (`pair_id` = family + `map_hash`). A* is a sidecar (cost / success), not mixed into expansion savings. |
| `summary.csv` / `stats.csv` | Same grouped table (descriptives + tests). Identical copies. |
| `expansions_scatter.png` | F2F pair expansions vs F2E (line of equality). |
| `saving_by_family.png` | Expansion saving % by map family. |
| `saving_by_density.png` | Expansion saving % by `obstacle_count` for **nested** random maps only. |
| `saving_vs_detour.png` | Saving % vs detour ratio. |
| `runtime_ratio.png` | Histogram of F2F/F2E runtime. |
| `forward_backward.png` | Forward vs backward pair expansions. |

## How to read the numbers

- **Pair expansions only.** A* `expanded` is states; SFBDS `expanded` is pairs. Saving % is `(F2E − F2F) / F2E × 100`. Positive means F2F expanded fewer pairs.
- **Solved pair** = both SFBDS succeeded and neither timed out. Timeouts stay in `paired.csv` with null diffs; they are excluded from means, win %, and tests.
- **`n_solved`** = descriptive sample. **`n_test`** = Wilcoxon sample after collapsing nested `family_id`s (median `expansion_diff` per family). If they differ, densities of the same query were not treated as independent n.
- **Primary test:** two-sided Wilcoxon on `expansion_diff = F2E − F2F`. **Confirmatory:** sign test on who expanded fewer, ties dropped. If `n_untied < 10`, p is **null** (not a missing file). That is expected when F2F and F2E almost always tie (open, corridor).
- **Rank-biserial** > 0 means F2F fewer expansions on the untied pairs.
- **Holm** is within a planned family (map families together; density counts together). Detour buckets are exploratory: raw p only.
- **Nested density:** nested random experiments share start/goal across density prefixes. Independent `*_d10/d20/d30` CSVs are kept for F2F vs F2E pairing but **do not** enter `obstacle_count` tests, `overall_random`, or `saving_by_density.png`.

## Experiments in this run

| experiment | paired rows | map family | nested density |
| --- | --- | --- | --- |
| study_maze_127_timed | 30 | maze | no |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maze | 30 | 30 | 21 | 0 | 9 | 0.4% | 9.54e-07 | 1.00 | F2F fewer expansions; p=9.54e-07 |

Pooled `random` mixes nested and independent files, so tests are skipped there on purpose.

## Nested density (eligible maps only)

_No nested-density experiments in this run, so there are no density-factor tests._

### Overall nested random (one median per family)

_No nested-density experiments in this run._

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 30 | 30 | 21 | 0 | 9 | 0.4% | 9.54e-07 | 1.00 | F2F fewer expansions; p=9.54e-07 |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).

- Untied maze pairs with both times: **21**
- F2F faster wall-clock: **21**; F2E faster: **0**; equal: **0**
- Median runtime_ratio: **0.941**; mean: **0.942**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [2, inf) | 30 | 30 | 21 | 0 | 9 | 0.4% | 9.54e-07 | 1.00 | F2F fewer expansions; p=9.54e-07 |
