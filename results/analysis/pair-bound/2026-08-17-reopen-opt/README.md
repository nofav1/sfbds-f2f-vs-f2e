# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/2026-08-17-reopen-opt --experiment study_corridor_512_opt --experiment study_maze_127_opt --experiment study_open_128_opt --experiment study_random_64_opt --experiment study_random_128_opt
```

## Headline

- **Corridor:** F2F and F2E tied on all 30 solved pairs (too few untied pairs for a Wilcoxon p-value).
- **Maze:** F2F expanded fewer pairs on 22/30 solved maps (73.3%); Holm p=4.77e-07.
- **Open:** F2F and F2E tied on all 30 solved pairs (too few untied pairs for a Wilcoxon p-value).
- **Random (all files):** 180 solved pairs; 8 F2F-fewer, 0 F2E-fewer, 52 ties (n_test=60). Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {study_random_64_opt: 1228 obstacles (~0.30 on 64×64)}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 180 maps from 60 families (median expansion_diff per family). Untied=8. Do not cite a pooled p here; use the per-experiment density table.

Coverage of this run: **270** paired instances, **270** solved, **0** timed out, **180** nested-density rows, map families corridor, maze, open, random. Cost mismatches (F2F / F2E / A* when A* succeeded): **0**.

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
| study_corridor_512_opt | 30 | corridor | no |
| study_maze_127_opt | 30 | maze | no |
| study_open_128_opt | 30 | open | no |
| study_random_128_opt | 90 | random | yes (density-eligible) |
| study_random_64_opt | 90 | random | yes (density-eligible) |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| corridor | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| maze | 30 | 30 | 22 | 0 | 8 | 3.8% | 4.77e-07 | 1.00 | F2F fewer expansions; p=4.77e-07 |
| open | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| random | 180 | 60 | 8 | 0 | 52 | 0.0% | null | — | tests skipped (see note) |

Pooled `random` collapses nested densities (`n_test` ≠ `n_solved`), so tests are skipped there on purpose; use the per-experiment density table.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| study_random_128_opt: 1638 obstacles (~0.10 on 128×128) | 30 | 30 | 1 | 0 | 29 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_128_opt: 3276 obstacles (~0.20 on 128×128) | 30 | 30 | 2 | 0 | 28 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_128_opt: 4915 obstacles (~0.30 on 128×128) | 30 | 30 | 7 | 0 | 23 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| study_random_64_opt: 1228 obstacles (~0.30 on 64×64) | 30 | 30 | 13 | 0 | 17 | 0.0% | 0.0002 | 1.00 | F2F fewer expansions; p=0.0002 |
| study_random_64_opt: 409 obstacles (~0.10 on 64×64) | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| study_random_64_opt: 819 obstacles (~0.20 on 64×64) | 30 | 30 | 6 | 0 | 24 | 0.0% | null | 1.00 | p null (too few untied pairs) |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 180 | 60 | 8 | 0 | 52 | 0.0% | null | — | tests skipped (see note) |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 30 | 30 | 22 | 0 | 8 | 3.8% | 4.77e-07 | 1.00 | F2F fewer expansions; p=4.77e-07 |
| 128 | 120 | 60 | 2 | 0 | 58 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 512 | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| 64 | 90 | 30 | 6 | 0 | 24 | 0.0% | null | 1.00 | p null (too few untied pairs) |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Maze runtime slice (exploratory)

Only maze pairs where F2F and F2E **already differ in expansions**. Do not treat this as a co-primary test.

These rows are **exploratory**. Expansions remain the primary claim; runtime is noisy. `runtime_ratio` is F2F / F2E (values **< 1** mean F2F was faster).

- Untied maze pairs with both times: **22**
- F2F faster wall-clock: **21**; F2E faster: **1**; equal: **0**
- Median runtime_ratio: **0.883**; mean: **0.896**

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 197 | 119 | 5 | 0 | 114 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [1.1, 1.5) | 39 | 33 | 11 | 0 | 22 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| [1.5, 2) | 4 | 4 | 3 | 0 | 1 | 22.5% | null | 1.00 | p null (too few untied pairs) |
| [2, inf) | 30 | 30 | 22 | 0 | 8 | 3.8% | 4.77e-07 | 1.00 | F2F fewer expansions; p=4.77e-07 |
