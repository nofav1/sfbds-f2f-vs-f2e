# Paper figures (generated)

Produced by `python scripts/paper_figures.py`. Do not edit by hand.
Inputs: `results/study/pair-bound/*_opt.csv` and committed
`family_summary.csv`. Does **not** read gitignored analysis `paired.csv`.

## Sanity

- Maze 127 (`study_maze_127_opt`): **22/30** F2F-fewer.
- Maze 255 (`study_maze_255_opt`): **26/30** F2F-fewer.

## Headline win counts

| Family | F2F fewer | F2E fewer | ties | Holm p |
| --- | ---: | ---: | ---: | --- |
| Open 128 | 0 | 0 | 30 | null |
| Corridor 512 | 0 | 0 | 30 | null |
| Maze 127 | 22 | 0 | 8 | 4.77e-07 |
| Maze 255 | 26 | 0 | 4 | 2.98e-08 |
| Nested 64 @ 30% | 13 | 0 | 17 | 0.0002 |

## Files

- `fig_headline_wins.pdf`
- `fig_headline_wins.png`
- `fig_maze_scatter.pdf`
- `fig_maze_scatter.png`
- `fig_maze_factors.pdf`
- `fig_maze_factors.png`
- `fig_heuristic_strength.pdf`
- `fig_heuristic_strength.png`
- `fig_eval_cost.pdf`
- `fig_eval_cost.png`
- `table_headline.csv`
- `table_maze_factors.csv`
- `table_nested_density.csv`
- `table_generated_peak_open.csv`
- `table_timed_runtime.csv`
- `table_instance_matrix.csv`
- `table_eval_cost.csv`

Nested 64 @ 30% (seed 110) and nested 64 @ 45% (seed 210) in the
heuristic-strength figure are different maps, not a paired density step.
Do not cite Spearman from `family_summary.csv` as a savings ranking.

`n_densities` is the nested prefix count. Maze/open/corridor rows are 1
(unique wall counts from S/G carving are not densities).

Eval-cost figure is **secondary**. The log-x curve omits beta=0;
that point is in `table_eval_cost.csv`.
