# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/2026-08-17-far-braid-by-experiment --experiment study_maze_127_far_opt --experiment study_maze_127_braid_opt --experiment study_maze_127_timed_opt --experiment study_maze_255_braid_opt --experiment study_random_64_d50_opt --experiment study_random_64_d52_opt --experiment study_random_128_d45_opt --experiment study_random_128_d45_md48_opt --allow-opt-subset
```

## Headline

- **study_maze_127_braid_opt:** F2F expanded fewer pairs on 12/30 solved maps (40.0%); Holm p=0.0010.
- **study_maze_127_far_opt:** F2F expanded fewer pairs on 15/30 solved maps (50.0%); Holm p=0.0002.
- **study_maze_127_timed_opt:** F2F expanded fewer pairs on 22/30 solved maps (73.3%); Holm p=1.91e-06.
- **study_maze_255_braid_opt:** F2F expanded fewer pairs on 11/30 solved maps (36.7%); Holm p=0.0010.
- Do not cite a pooled maze p-value; the per-experiment rows above are the maze claim (timed is the same maps as maze 127 when seeds match).
- **Random (all files):** 330 solved pairs; 45 F2F-fewer, 1 F2E-fewer, 64 ties (n_test=110). Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {study_random_128_d45_opt: 7372 obstacles (~0.45 on 128×128), study_random_128_d45_opt: 7781 obstacles (~0.47 on 128×128), study_random_128_d45_opt: 8191 obstacles (~0.50 on 128×128), study_random_64_d50_opt: 1638 obstacles (~0.40 on 64×64), study_random_64_d50_opt: 1842 obstacles (~0.45 on 64×64), study_random_64_d50_opt: 2047 obstacles (~0.50 on 64×64)}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 330 maps from 110 families (median expansion_diff per family). Untied=46. Do not cite a pooled p here; use the per-experiment density table.

Coverage of this run: **450** paired instances, **450** solved, **0** timed out, **330** nested-density rows, map families maze, random. Cost mismatches (F2F / F2E / A* when A* succeeded): **0**.

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
- **Holm** is within a planned family (map families together; maze experiments together; nested density groups within one experiment; size groups together). Mixed maze or size pools skip Wilcoxon. Detour buckets are exploratory: raw p only.
- **Nested density:** nested random experiments share start/goal across density prefixes. Independent `*_d10/d20/d30` CSVs are kept for F2F vs F2E pairing but **do not** enter `obstacle_count` tests, `overall_random`, or `saving_by_density.png`. Density tests are keyed by experiment, grid size, and `obstacle_count` so two configs that share a prefix count are not pooled.

## Experiments in this run

| experiment | paired rows | map family | nested density |
| --- | --- | --- | --- |
| study_maze_127_braid_opt | 30 | maze | no |
| study_maze_127_far_opt | 30 | maze | no |
| study_maze_127_timed_opt | 30 | maze | no |
| study_maze_255_braid_opt | 30 | maze | no |
| study_random_128_d45_md48_opt | 60 | random | yes (density-eligible) |
| study_random_128_d45_opt | 90 | random | yes (density-eligible) |
| study_random_64_d50_opt | 90 | random | yes (density-eligible) |
| study_random_64_d52_opt | 90 | random | yes (density-eligible) |

## Experiment

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| study_maze_127_braid_opt | 30 | 30 | 12 | 0 | 18 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0005 |
| study_maze_127_far_opt | 30 | 30 | 15 | 0 | 15 | 0.2% | 0.0002 | 1.00 | F2F fewer expansions; p=6.10e-05 |
| study_maze_127_timed_opt | 30 | 30 | 22 | 0 | 8 | 3.8% | 1.91e-06 | 1.00 | F2F fewer expansions; p=4.77e-07 |
| study_maze_255_braid_opt | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| study_random_128_d45_md48_opt | 60 | 20 | 8 | 1 | 11 | 0.0% | null | — | tests skipped (see note) |
| study_random_128_d45_opt | 90 | 30 | 17 | 0 | 13 | 6.1% | null | — | tests skipped (see note) |
| study_random_64_d50_opt | 90 | 30 | 13 | 0 | 17 | 0.0% | null | — | tests skipped (see note) |
| study_random_64_d52_opt | 90 | 30 | 7 | 0 | 23 | 0.0% | null | — | tests skipped (see note) |

Nested-random experiment totals skip Wilcoxon (use the density table). Maze experiments are tested here; do not cite a pooled maze row when that pool mixes timed / far / braid.

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maze | 120 | 120 | 60 | 0 | 60 | 0.2% | null | — | tests skipped (see note) |
| random | 330 | 110 | 45 | 1 | 64 | 0.0% | null | — | tests skipped (see note) |

Pooled `maze` mixes experiments (for example timed vs far vs braid), so tests are skipped there on purpose; use the per-experiment table.

Pooled `random` collapses nested densities (`n_test` ≠ `n_solved`), so tests are skipped there on purpose; use the per-experiment density table.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| study_random_128_d45_md48_opt: 7372 obstacles (~0.45 on 128×128) | 20 | 20 | 7 | 1 | 12 | 0.0% | null | 0.67 | p null (too few untied pairs) |
| study_random_128_d45_md48_opt: 7781 obstacles (~0.47 on 128×128) | 20 | 20 | 8 | 1 | 11 | 0.0% | null | 0.69 | p null (too few untied pairs) |
| study_random_128_d45_md48_opt: 8191 obstacles (~0.50 on 128×128) | 20 | 20 | 8 | 1 | 11 | 0.0% | null | 0.64 | p null (too few untied pairs) |
| study_random_128_d45_opt: 7372 obstacles (~0.45 on 128×128) | 30 | 30 | 13 | 0 | 17 | 0.0% | 0.0002 | 1.00 | F2F fewer expansions; p=0.0002 |
| study_random_128_d45_opt: 7781 obstacles (~0.47 on 128×128) | 30 | 30 | 17 | 0 | 13 | 6.3% | 4.58e-05 | 1.00 | F2F fewer expansions; p=1.53e-05 |
| study_random_128_d45_opt: 8191 obstacles (~0.50 on 128×128) | 30 | 30 | 17 | 0 | 13 | 6.3% | 4.58e-05 | 1.00 | F2F fewer expansions; p=1.53e-05 |
| study_random_64_d50_opt: 1638 obstacles (~0.40 on 64×64) | 30 | 30 | 12 | 0 | 18 | 0.0% | 0.0007 | 1.00 | F2F fewer expansions; p=0.0005 |
| study_random_64_d50_opt: 1842 obstacles (~0.45 on 64×64) | 30 | 30 | 13 | 0 | 17 | 0.0% | 0.0007 | 1.00 | F2F fewer expansions; p=0.0002 |
| study_random_64_d50_opt: 2047 obstacles (~0.50 on 64×64) | 30 | 30 | 13 | 0 | 17 | 0.0% | 0.0007 | 1.00 | F2F fewer expansions; p=0.0002 |
| study_random_64_d52_opt: 2047 obstacles (~0.50 on 64×64) | 30 | 30 | 7 | 0 | 23 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_64_d52_opt: 2088 obstacles (~0.51 on 64×64) | 30 | 30 | 7 | 0 | 23 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_64_d52_opt: 2129 obstacles (~0.52 on 64×64) | 30 | 30 | 8 | 0 | 22 | 0.0% | null | 1.00 | p null (too few untied pairs) |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 330 | 110 | 45 | 1 | 64 | 0.0% | null | — | tests skipped (see note) |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 90 | 90 | 49 | 0 | 41 | 1.5% | null | — | tests skipped (see note) |
| 128 | 150 | 50 | 25 | 1 | 24 | 0.0% | null | — | tests skipped (see note) |
| 255 | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| 64 | 180 | 60 | 20 | 0 | 40 | 0.0% | null | — | tests skipped (see note) |

Size groups that mix experiments (127, 128, 64) skip Wilcoxon; use the per-experiment table or nested density rows. Size groups that mix nested random maps also collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only **`_timed`** maze pairs where F2F and F2E **already differ in expansions** (median of `runtime_repeats`). Do not treat this as a co-primary test. Do not cite single-run maze clocks from this block.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster). Only `_timed` experiments (median of `runtime_repeats`).

- Untied maze pairs with both times: **22**
- F2F faster wall-clock: **22**; F2E faster: **0**; equal: **0**
- Median runtime_ratio: **0.885**; mean: **0.894**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 166 | 92 | 29 | 0 | 63 | 0.0% | 2.55e-06 | 1.00 | F2F fewer expansions; p=2.55e-06 |
| [1.1, 1.5) | 197 | 78 | 41 | 1 | 36 | 0.0% | 7.85e-08 | 0.95 | F2F fewer expansions; p=7.85e-08 |
| [1.5, 2) | 22 | 11 | 5 | 0 | 6 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [2, inf) | 65 | 62 | 37 | 0 | 25 | 1.6% | 1.14e-07 | 1.00 | F2F fewer expansions; p=1.14e-07 |
