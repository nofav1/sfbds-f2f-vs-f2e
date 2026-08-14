# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/<run-name>
```

## Headline

- **Maze:** F2F expanded fewer pairs on 33/60 solved maps (55.0%); Holm p=5.39e-07.
- **Random (all files):** 180 solved pairs; 57 F2F-fewer, 0 F2E-fewer, 123 ties. Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {1638, 1842, 2047, 7372}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 180 maps from 60 families (median expansion_diff per family). Untied=19.

Coverage of this run: **240** paired instances, **240** solved, **0** timed out, **180** nested-density rows, map families maze, random. Cost mismatches (F2F vs F2E solution cost): **0**.

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
| study_maze_127_far | 30 | maze | no |
| study_random_128_dense | 90 | random | yes (density-eligible) |
| study_random_64_d50 | 90 | random | yes (density-eligible) |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maze | 60 | 60 | 33 | 0 | 27 | 0.1% | 5.39e-07 | 1.00 | F2F fewer expansions; p=5.39e-07 |
| random | 180 | 60 | 57 | 0 | 123 | 0.0% | null | — | tests skipped (see note) |

Pooled `random` mixes nested and independent files, so tests are skipped there on purpose.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1638 obstacles (~0.40 on 64×64) | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0029 | 1.00 | F2F fewer expansions; p=0.0010 |
| 1842 obstacles (~0.45 on 64×64) | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0029 | 1.00 | F2F fewer expansions; p=0.0010 |
| 2047 obstacles (~0.50 on 64×64) | 30 | 30 | 12 | 0 | 18 | 0.0% | 0.0020 | 1.00 | F2F fewer expansions; p=0.0005 |
| 4915 obstacles (~0.30 on 128×128) | 30 | 30 | 4 | 0 | 26 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 6553 obstacles (~0.40 on 128×128) | 30 | 30 | 8 | 0 | 22 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 7372 obstacles (~0.45 on 128×128) | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0029 | 1.00 | F2F fewer expansions; p=0.0010 |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 180 | 60 | 57 | 0 | 123 | 0.0% | 3.81e-06 | 1.00 | F2F fewer expansions; p=3.81e-06 |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 60 | 60 | 33 | 0 | 27 | 0.1% | 1.08e-06 | 1.00 | F2F fewer expansions; p=5.39e-07 |
| 128 | 90 | 30 | 23 | 0 | 67 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 64 | 90 | 30 | 34 | 0 | 56 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).

- Untied maze pairs with both times: **33**
- F2F faster wall-clock: **27**; F2E faster: **6**; equal: **0**
- Median runtime_ratio: **0.951**; mean: **0.939**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 73 | 37 | 22 | 0 | 51 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| [1.1, 1.5) | 85 | 43 | 27 | 0 | 58 | 0.0% | 3.05e-05 | 1.00 | F2F fewer expansions; p=3.05e-05 |
| [1.5, 2) | 19 | 12 | 8 | 0 | 11 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [2, inf) | 63 | 62 | 33 | 0 | 30 | 0.1% | 5.39e-07 | 1.00 | F2F fewer expansions; p=5.39e-07 |
