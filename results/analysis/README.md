# Analysis runs

This directory is an **index of snapshots**. Do not dump CSVs or plots at this level.

Living notes (what we concluded, what we locked, what to try next):

- Pair-bound: [`pair-bound/research_log.md`](pair-bound/research_log.md)
- Master log (legacy + pair-bound): [`docs/research_log.md`](../../docs/research_log.md)

**Do not mix F2E formulas.** Gap-heuristic study CSVs and analyses stay under `legacy/`. Official pair-bound output stays under `pair-bound/`. Analysis `--input-dir` is one folder of `*.csv` (non-recursive).

## Convention

```bash
# Official pair bound (new runs)
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/YYYY-MM-DD-short-slug

# Frozen gap F2E (do not cite as corrected F2E)
python -m sfbds_compare.analysis --input-dir results/study/legacy --out-dir results/analysis/legacy/YYYY-MM-DD-short-slug
```

- **New experiment or new analysis pass → new folder** under the matching formula directory. Never overwrite a previous slug.
- Follow-up maps or configs → new `*_opt` YAMLs under `configs/followup/` (copy seeds from [`configs/followup/retired/`](../../configs/followup/retired/) if needed), new CSVs under `results/study/pair-bound/` (keep `legacy/`), then a new analysis folder under `pair-bound/`. Use `--experiment` to select a subset; `--allow-opt-subset` is follow-up-only and does not mix the five official `*_opt` stems with extras.
- Update this table and [`docs/research_log.md`](../../docs/research_log.md) when you add a run.

## Runs (legacy gap F2E)

| Folder | Date | Input | What it is |
| --- | --- | --- | --- |
| [`legacy/2026-08-14-baseline-study`](legacy/2026-08-14-baseline-study/) | 2026-08-14 | all CSVs then in `results/study` (now `results/study/legacy`) | First paired F2F vs F2E analysis of the 64/128 grid study (open, maze, corridor, nested random, plus leftover independent random CSVs). |
| [`legacy/2026-08-14-harder-followup`](legacy/2026-08-14-harder-followup/) | 2026-08-14 | maze 63/127/255 + `study_random_64_dense` | Harder maze size rung and denser nested 64×64 random (30/40/45%). |
| [`legacy/2026-08-14-maze-runtime`](legacy/2026-08-14-maze-runtime/) | 2026-08-14 | `study_maze_127_timed` only | Maze 127 re-run with median of 5 wall-clock repeats; runtime slice on maps where expansions already differ. |
| [`legacy/2026-08-14-far-maze-and-dense-random`](legacy/2026-08-14-far-maze-and-dense-random/) | 2026-08-14 | maze 127 vs 127-far; nested 64@40/45/50% and 128@30/40/45% | Query-length maze contrast plus denser nested random. |
| [`legacy/2026-08-14-braid-and-denser-nested`](legacy/2026-08-14-braid-and-denser-nested/) | 2026-08-14 | maze 127 vs braid 0.5; nested 64@50–52% and 128@45–50% | Braided maze contrast and denser nested random (md lowered so connect-once succeeds). |
| [`legacy/2026-08-14-maze255-braid-and-128-md48`](legacy/2026-08-14-maze255-braid-and-128-md48/) | 2026-08-14 | maze 127/255 ± braid; nested 128@45–50% md 28 vs md 48 | Size×braid interaction and 45–50% nested random at the original Manhattan 48 (fewer connected queries). **Density tests in this README pool md-28 with md-48; use the next row.** |
| [`legacy/2026-08-14-density-by-experiment`](legacy/2026-08-14-density-by-experiment/) | 2026-08-14 | same experiments as the previous row | Re-analysis after density tests were keyed by experiment (stats-code fix; old snapshot kept). |

## Runs (pair-bound F2E)

Pre-fix snapshots (through `2026-08-17-cost-clean-plots`) use **NoReopen** pair-bound F2E. Reopen F2E is [`pair-bound/2026-08-17-reopen-opt`](pair-bound/2026-08-17-reopen-opt/). Do not mix the two in one analysis; the CLI refuses unless `--experiment` selects only one family of names.

| Folder | Date | Input | What it is |
| --- | --- | --- | --- |
| [`pair-bound/2026-08-17-baseline-study`](pair-bound/2026-08-17-baseline-study/) | 2026-08-17 | `configs/study/` CSVs in `results/study/pair-bound` | First paired F2F vs official pair-bound F2E analysis of the current study matrix (corridor 512, maze 127, open 128, nested random 64/128). Nested-random p-values in this README include cost mismatches; do not cite. |
| [`pair-bound/2026-08-17-cost-clean-tests`](pair-bound/2026-08-17-cost-clean-tests/) | 2026-08-17 | same CSVs | Re-analysis: expansion tests drop `cost_mismatch` / A* disagreement. Maze 22/30 stays; 64@30% `n_untied` is 9 → p null. **Plots in this folder still include the 12 mismatches.** |
| [`pair-bound/2026-08-17-cost-clean-plots`](pair-bound/2026-08-17-cost-clean-plots/) | 2026-08-17 | same CSVs | Same tables as cost-clean-tests; plots now omit `cost_mismatch` rows. Cite this folder for **NoReopen** figures. |
| [`pair-bound/2026-08-17-reopen-opt`](pair-bound/2026-08-17-reopen-opt/) | 2026-08-17 | `study_*_opt` CSVs (`--experiment` × 5) | Official reopen F2E on the same seeds/queries. 270/270 solved, **0** cost mismatches. Maze 22/30; nested 64@30% now cost-clean with 13 F2F-fewer. |
| [`pair-bound/2026-08-17-harder-opt`](pair-bound/2026-08-17-harder-opt/) | 2026-08-17 | maze 255 + nested 64/128 dense `_opt` (`--allow-opt-subset`) | Reopen F2E harder follow-up. 210/210 solved, **0** mismatches. Maze 255: 26/30 F2F-fewer. Nested 64@40/45% and 128@45% have `n_untied ≥ 10`. |
| [`pair-bound/2026-08-17-far-braid-opt`](pair-bound/2026-08-17-far-braid-opt/) | 2026-08-17 | far/braid/timed maze + denser nested `_opt` (`--allow-opt-subset`) | Mixed follow-up snapshot. 450/450 solved, **0** mismatches. Do **not** cite maze 60/120, size 127/128, or the runtime block. |
| [`pair-bound/2026-08-17-far-braid-by-experiment`](pair-bound/2026-08-17-far-braid-by-experiment/) | 2026-08-17 | same eight CSVs (stats-code fix) | Citable generated README: per-experiment maze, timed-only runtime, mixed size groups skip Wilcoxon. Density rows unchanged. |
| [`pair-bound/2026-08-17-eval-cost-sensitivity`](pair-bound/2026-08-17-eval-cost-sensitivity/) | 2026-08-17 | maze 127 / maze 255 / nested 64@30% `*_opt` rows (offline) | **Secondary.** Offline `T = rest + β·evals` sweep. No crossover to F2E. Do not cite as a main expansion result. |
