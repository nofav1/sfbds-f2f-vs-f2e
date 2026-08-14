# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/<run-name>
```

## Headline

- **Maze:** F2F expanded fewer pairs on 58/90 solved maps (64.4%); Holm p=3.51e-11.
- **Random (all files):** 90 solved pairs; 36 F2F-fewer, 1 F2E-fewer, 53 ties. Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {1638, 1842}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 90 maps from 30 families (median expansion_diff per family). Untied=14.

Coverage of this run: **180** paired instances, **180** solved, **0** timed out, **90** nested-density rows, map families maze, random. Cost mismatches (F2F vs F2E solution cost): **0**.

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
| study_maze_127 | 30 | maze | no |
| study_maze_255 | 30 | maze | no |
| study_maze_63 | 30 | maze | no |
| study_random_64_dense | 90 | random | yes (density-eligible) |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maze | 90 | 90 | 58 | 0 | 32 | 0.3% | 3.51e-11 | 1.00 | F2F fewer expansions; p=3.51e-11 |
| random | 90 | 30 | 36 | 1 | 53 | 0.0% | null | — | tests skipped (see note) |

Pooled `random` mixes nested and independent files, so tests are skipped there on purpose.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1228 obstacles (~0.30 on 64×64) | 30 | 30 | 6 | 0 | 24 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 1638 obstacles (~0.40 on 64×64) | 30 | 30 | 15 | 1 | 14 | 0.6% | 0.0001 | 0.97 | F2F fewer expansions; p=9.16e-05 |
| 1842 obstacles (~0.45 on 64×64) | 30 | 30 | 15 | 0 | 15 | 0.3% | 0.0001 | 1.00 | F2F fewer expansions; p=6.10e-05 |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 90 | 30 | 36 | 1 | 53 | 0.0% | 0.0001 | 1.00 | F2F fewer expansions; p=0.0001 |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 30 | 30 | 21 | 0 | 9 | 0.4% | 2.86e-06 | 1.00 | F2F fewer expansions; p=9.54e-07 |
| 255 | 30 | 30 | 26 | 0 | 4 | 0.9% | 1.19e-07 | 1.00 | F2F fewer expansions; p=2.98e-08 |
| 63 | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| 64 | 90 | 30 | 36 | 1 | 53 | 0.0% | 0.0002 | 1.00 | F2F fewer expansions; p=0.0001 |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).

- Untied maze pairs with both times: **58**
- F2F faster wall-clock: **42**; F2E faster: **16**; equal: **0**
- Median runtime_ratio: **0.956**; mean: **0.958**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 22 | 17 | 2 | 0 | 20 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [1.1, 1.5) | 49 | 26 | 19 | 1 | 29 | 0.0% | 0.0015 | 0.95 | F2F fewer expansions; p=0.0015 |
| [1.5, 2) | 18 | 13 | 13 | 0 | 5 | 13.9% | null | 1.00 | p null (too few untied pairs) |
| [2, inf) | 91 | 90 | 60 | 0 | 31 | 0.4% | 2.39e-11 | 1.00 | F2F fewer expansions; p=2.39e-11 |
