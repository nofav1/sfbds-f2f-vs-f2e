# Analysis results (F2F vs F2E)

This file is **generated** by `python -m sfbds_compare.analysis`. Re-run analysis to refresh it. Do not edit by hand.

```bash
python -m sfbds_compare.analysis --input-dir results/study/legacy --out-dir results/analysis/legacy/2026-08-14-baseline-study
```

## Headline

- **Corridor:** F2F and F2E tied on all 60 solved pairs (too few untied pairs for a Wilcoxon p-value).
- **Maze:** F2F expanded fewer pairs on 32/60 solved maps (53.3%); Holm p=4.66e-10.
- **Open:** F2F and F2E tied on all 60 solved pairs (too few untied pairs for a Wilcoxon p-value).
- **Random (all files):** 360 solved pairs; 40 F2F-fewer, 0 F2E-fewer, 320 ties. Wilcoxon is skipped on this pooled group; use nested density rows below.
- **Nested density tests with n_untied ≥ 10:** obstacle_count {1228}. Other density levels had too many ties for a p-value.
- **Overall nested random:** 180 maps from 60 families (median expansion_diff per family). Untied=8.

Coverage of this run: **540** paired instances, **540** solved, **0** timed out, **180** nested-density rows, map families corridor, maze, open, random. Cost mismatches (F2F vs F2E solution cost): **0**.

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
- **Nested density:** `study_random_64` and `study_random_128` share start/goal across 10/20/30% prefixes. Independent `*_d10/d20/d30` CSVs are kept for F2F vs F2E pairing but **do not** enter `obstacle_count` tests, `overall_random`, or `saving_by_density.png`.

## Experiments in this run

| experiment | paired rows | map family | nested density |
| --- | --- | --- | --- |
| study_corridor_256 | 30 | corridor | no |
| study_corridor_512 | 30 | corridor | no |
| study_maze_127 | 30 | maze | no |
| study_maze_63 | 30 | maze | no |
| study_open_128 | 30 | open | no |
| study_open_64 | 30 | open | no |
| study_random_128 | 90 | random | yes (density-eligible) |
| study_random_128_d10 | 30 | random | no |
| study_random_128_d20 | 30 | random | no |
| study_random_128_d30 | 30 | random | no |
| study_random_64 | 90 | random | yes (density-eligible) |
| study_random_d10 | 30 | random | no |
| study_random_d20 | 30 | random | no |
| study_random_d30 | 30 | random | no |

## Map family

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| corridor | 60 | 60 | 0 | 0 | 60 | 0.0% | null | — | p null (too few untied pairs) |
| maze | 60 | 60 | 32 | 0 | 28 | 0.2% | 4.66e-10 | 1.00 | F2F fewer expansions; p=4.66e-10 |
| open | 60 | 60 | 0 | 0 | 60 | 0.0% | null | — | p null (too few untied pairs) |
| random | 360 | 240 | 40 | 0 | 320 | 0.0% | null | — | tests skipped (see note) |

Pooled `random` mixes nested and independent files, so tests are skipped there on purpose.

## Nested density (eligible maps only)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1228 obstacles (~0.30 on 64×64) | 30 | 30 | 13 | 0 | 17 | 0.0% | 0.0002 | 1.00 | F2F fewer expansions; p=0.0002 |
| 1638 obstacles (~0.10 on 128×128) | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| 3276 obstacles (~0.20 on 128×128) | 30 | 30 | 2 | 0 | 28 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 409 obstacles (~0.10 on 64×64) | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| 4915 obstacles (~0.30 on 128×128) | 30 | 30 | 7 | 0 | 23 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 819 obstacles (~0.20 on 64×64) | 30 | 30 | 6 | 0 | 24 | 0.0% | null | 1.00 | p null (too few untied pairs) |

### Overall nested random (one median per family)

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nested random families | 180 | 60 | 28 | 0 | 152 | 0.0% | null | 1.00 | p null (too few untied pairs) |

## Size

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 127 | 30 | 30 | 21 | 0 | 9 | 0.4% | 2.86e-06 | 1.00 | F2F fewer expansions; p=9.54e-07 |
| 128 | 210 | 150 | 14 | 0 | 196 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| 256 | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| 512 | 30 | 30 | 0 | 0 | 30 | 0.0% | null | — | p null (too few untied pairs) |
| 63 | 30 | 30 | 11 | 0 | 19 | 0.0% | 0.0010 | 1.00 | F2F fewer expansions; p=0.0010 |
| 64 | 210 | 150 | 26 | 0 | 184 | 0.0% | 0.0005 | 1.00 | F2F fewer expansions; p=0.0002 |

Size groups that mix nested random maps collapse `family_id` before testing (`n_test` < `n_solved`).

## Detour buckets (exploratory)

Detour = solution cost / Manhattan (A* cost when A* succeeded). Not Holm-adjusted.

| group | n_solved | n_test | F2F fewer | F2E fewer | ties | median saving % | p (Holm if planned) | rank-biserial | read as |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1, 1.1) | 390 | 312 | 22 | 0 | 368 | 0.0% | 0.0002 | 1.00 | F2F fewer expansions; p=0.0002 |
| [1.1, 1.5) | 81 | 75 | 14 | 0 | 67 | 0.0% | 0.0001 | 1.00 | F2F fewer expansions; p=0.0001 |
| [1.5, 2) | 10 | 10 | 4 | 0 | 6 | 0.0% | null | 1.00 | p null (too few untied pairs) |
| [2, inf) | 59 | 59 | 32 | 0 | 27 | 0.2% | 4.66e-10 | 1.00 | F2F fewer expansions; p=4.66e-10 |
