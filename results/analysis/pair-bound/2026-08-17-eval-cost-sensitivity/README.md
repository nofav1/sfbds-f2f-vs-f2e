# Offline heuristic-evaluation-cost sensitivity (Option 3A)

Secondary analysis only. Do not cite this folder as a main expansion-geography result. Authoritative pair-expansion numbers remain in [`2026-08-17-reopen-opt`](../2026-08-17-reopen-opt/) (maze 127, nested 64@30%) and [`2026-08-17-harder-opt`](../2026-08-17-harder-opt/) (maze 255).

Reproducible via `python scripts/eval_cost_sensitivity.py --force` (refuses a non-empty folder without `--force`). `--check-only` asserts 30 pairs, `rest ≥ 0`, and 0 F2E-fewer-eval maps without writing. That invariant is also locked in `tests/unit/test_eval_cost_sensitivity.py`. This folder is **not** produced by `python -m sfbds_compare.analysis`.

## Methodology

Offline rescaling of recorded reopen `*_opt` rows. Search is not re-run.

```text
rest = runtime_sec - heuristic_time_sec
T_beta = rest + beta * heuristic_evals
```

`beta` is a synthetic seconds-per-evaluation knob. `beta = 0` keeps only the non-heuristic residual. The observed Manhattan cost is the per-family median of `heuristic_time_sec / heuristic_evals` over F2F and F2E rows (~5–7×10⁻⁷ s/eval). The sweep is `0, 0.1×, 1×, 10×, …, 10⁶×` that observed median.

Preference is `T_F2F` vs `T_F2E` on each paired query. Headline series is the **median** of `T_F2F / T_F2E` (values `< 1` mean F2F cheaper). A crossover to F2E is defined as the first `beta ≥ 0` where that median exceeds 1 or F2E is cheaper on a majority of queries.

## Datasets

Official reopen F2E only. 30 F2F/F2E pairs each. No cost mismatches. No legacy gap-F2E.

| Family | Study CSV | Filter |
| --- | --- | --- |
| Maze 127 | `results/study/pair-bound/study_maze_127_opt.csv` | none (not `_timed`) |
| Maze 255 | `results/study/pair-bound/study_maze_255_opt.csv` | none |
| Nested 64 @ 30% | `results/study/pair-bound/study_random_64_opt.csv` | `obstacle_count == 1228` (seed 110; not `study_random_64_dense_opt`) |

Heuristic-eval counts on these pairs: maze 127 **22 / 0 / 8** F2F-fewer / F2E-fewer / tie; maze 255 **26 / 0 / 4**; nested 64@30% **13 / 0 / 17**. F2E never has fewer evals than F2F.

## Result

F2F remains preferable on the median `T` ratio throughout the tested range. There is **no crossover** where F2E becomes preferable.

| Family | Median T ratio at β=0 | at 1× observed | at 10⁶× | F2F cheaper at β=0 | at 10⁶× |
| --- | ---: | ---: | ---: | ---: | ---: |
| Maze 127 | 0.934 | 0.935 | 0.962 | 27/30 | 29/30 |
| Maze 255 | 0.915 | 0.917 | 0.962 | 26/30 | 29/30 |
| Nested 64 @ 30% | 0.950 | 0.951 | 1.000 | 21/30 | 22/30 |

As `beta` grows, the median ratio moves toward the per-query eval-count ratio. Mazes plateau near 0.96. Nested 64@30% approaches 1.0 because 17/30 queries have tied evals; the **total**-`T` ratio on that family stays about 0.37–0.41, because the 13 un-tied queries have large F2E eval counts. A few queries where F2E has a cheaper residual and equal evals stay F2E-cheaper at every `beta` (3→1 on maze 127, 4→1 on maze 255, 9→8 on nested). Those do not create a family-level crossover.

Figure: [`cost_ratio_vs_beta.png`](cost_ratio_vs_beta.png). Table: [`sensitivity.csv`](sensitivity.csv).

## Crossover

None. F2F stays at or below parity on the median ratio for every tested `beta ≥ 0` on all three families. Do not read the nested median approaching 1 as F2E becoming cheaper.

## Limitations

- Offline: `beta` rescales recorded evals; it does not change which pairs the search expands.
- `rest` is Python / OPEN / CLOSED / switching overhead from a **single** wall-clock sample, not a clean expansion-cost constant. Maze 127 `_timed` medians were not used.
- Recorded `heuristic_time_sec` is only about 3–7% of runtime (Manhattan is cheap). Subtracting it is a small correction.
- A real expensive heuristic could also change the expansion set, not only the cost per eval.
- Units of `beta` are seconds/eval on this machine’s recorded clock. The scientific claim is the **direction** of the sweep, not a portable constant.

## Report-ready sentences

On the recorded reopen `*_opt` searches, F2F never issued more heuristic evaluations than F2E on maze 127, maze 255, or nested 64@30%. An offline model that charges `beta` seconds per evaluation therefore cannot reverse the F2F cost advantage by making heuristics more expensive: the median `T_F2F / T_F2E` stays below 1 from `beta = 0` through a 10⁶× markup of the observed Manhattan eval cost. Mazes plateau near a 4% median saving; nested 64@30% approaches parity on the median because most queries tie on eval count, while the summed cost still favours F2F. This is a sensitivity check on cheap Manhattan, not a substitute for the pair-expansion geography result.

## How to cite

**Sensitivity / secondary only.** Include in an appendix or a short “heuristic-cost sensitivity” paragraph. Do not promote it to a co-primary result: the model is synthetic, the searches were not re-run under an expensive `h`, and the main claim remains pair-expansion counts under official reopen F2E.
