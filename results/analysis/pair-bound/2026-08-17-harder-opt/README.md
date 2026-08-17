# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/2026-08-17-harder-opt --experiment study_maze_255_opt --experiment study_random_64_dense_opt --experiment study_random_128_dense_opt --allow-opt-subset
```

## Headline

- **Maze:** F2F expanded fewer pairs on 26/30 solved maps (86.7%); Holm p=2.98e-08.
- **Random (all files):** 180 solved pairs; 22 F2F-fewer, 0 F2E-fewer, 38 ties (n_test=60). Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {study_random_128_dense_opt: 7372 obstacles (~0.45 on 128×128), study_random_64_dense_opt: 1638 obstacles (~0.40 on 64×64), study_random_64_dense_opt: 1842 obstacles (~0.45 on 64×64)}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 180 maps from 60 families (median expansion_diff per family). Untied=22. Do not cite a pooled p here; use the per-experiment density table.

Coverage of this run: **210** paired instances, **210** solved, **0** timed out, **180** nested-density rows, map families maze, random. Cost mismatches (F2F / F2E / A* when A* succeeded): **0**.

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

| experiment | paired rows | map family | nested density |
| --- | --- | --- | --- |
| study_maze_255_opt | 30 | maze | no |
| study_random_128_dense_opt | 90 | random | yes (density-eligible) |
| study_random_64_dense_opt | 90 | random | yes (density-eligible) |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maze | 30 | 30 | 26 | 0 | 4 | 3.8% | 2.98e-08 | 1.00 | F2F fewer expansions; p=2.98e-08 |
| random | 180 | 60 | 22 | 0 | 38 | 0.0% | null | — | tests skipped (see note) |

Pooled `random` collapses nested densities (`n_test` ≠ `n_solved`), so tests are skipped there on purpose; use the per-experiment density table.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| study_random_128_dense_opt: 4915 obstacles (~0.30 on 128×128) | 30 | 30 | 4 | 0 | 26 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_128_dense_opt: 6553 obstacles (~0.40 on 128×128) | 30 | 30 | 8 | 0 | 22 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_128_dense_opt: 7372 obstacles (~0.45 on 128×128) | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| study_random_64_dense_opt: 1228 obstacles (~0.30 on 64×64) | 30 | 30 | 6 | 0 | 24 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_64_dense_opt: 1638 obstacles (~0.40 on 64×64) | 30 | 30 | 16 | 0 | 14 | 4.9% | 6.10e-05 | 1.00 | F2F fewer expansions; p=3.05e-05 |
| study_random_64_dense_opt: 1842 obstacles (~0.45 on 64×64) | 30 | 30 | 14 | 1 | 15 | 0.0% | 0.0001 | 0.98 | F2F fewer expansions; p=0.0001 |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 180 | 60 | 22 | 0 | 38 | 0.0% | null | — | tests skipped (see note) |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 128 | 90 | 30 | 8 | 0 | 22 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 255 | 30 | 30 | 26 | 0 | 4 | 3.8% | 5.96e-08 | 1.00 | F2F fewer expansions; p=2.98e-08 |
| 64 | 90 | 30 | 14 | 0 | 16 | 0.0% | 0.0001 | 1.00 | F2F fewer expansions; p=0.0001 |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).

- Untied maze pairs with both times: **26**
- F2F faster wall-clock: **23**; F2E faster: **3**; equal: **0**
- Median runtime_ratio: **0.887**; mean: **0.872**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 59 | 40 | 8 | 0 | 32 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [1.1, 1.5) | 91 | 51 | 21 | 0 | 30 | 0.0% | 9.54e-07 | 1.00 | F2F fewer expansions; p=9.54e-07 |
| [1.5, 2) | 27 | 19 | 12 | 0 | 7 | 23.1% | 0.0005 | 1.00 | F2F fewer expansions; p=0.0005 |
| [2, inf) | 33 | 32 | 27 | 0 | 5 | 3.7% | 1.49e-08 | 1.00 | F2F fewer expansions; p=1.49e-08 |
