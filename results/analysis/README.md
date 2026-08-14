# Analysis runs

This directory is an **index of snapshots**. Do not dump CSVs or plots at this level.

Living notes (what we concluded, what we locked, what to try next) are in [`docs/research_log.md`](../../docs/research_log.md). Each folder below has a **generated** `README.md` with tables for that pass — do not edit those by hand.

## Convention

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/YYYY-MM-DD-short-slug
```

- **New experiment or new analysis pass → new folder.** Never overwrite a previous slug.
- Same study CSVs after a code/stats fix → new slug (for example `2026-08-15-baseline-study-rerun`).
- Follow-up maps or configs → new YAMLs under `configs/followup/` (or `configs/study/`), new CSVs under `results/study/` (keep old files), then a new analysis folder. Use `--experiment` to select a subset instead of mixing the whole `results/study` tree.
- Update this table and [`docs/research_log.md`](../../docs/research_log.md) when you add a run.

## Runs

| Folder | Date | Input | What it is |
| --- | --- | --- | --- |
| [`2026-08-14-baseline-study`](2026-08-14-baseline-study/) | 2026-08-14 | all CSVs then in `results/study` | First paired F2F vs F2E analysis of the 64/128 grid study (open, maze, corridor, nested random, plus leftover independent random CSVs). |
| [`2026-08-14-harder-followup`](2026-08-14-harder-followup/) | 2026-08-14 | maze 63/127/255 + `study_random_64_dense` | Harder maze size rung and denser nested 64×64 random (30/40/45%). |
| [`2026-08-14-maze-runtime`](2026-08-14-maze-runtime/) | 2026-08-14 | `study_maze_127_timed` only | Maze 127 re-run with median of 5 wall-clock repeats; runtime slice on maps where expansions already differ. |
| [`2026-08-14-far-maze-and-dense-random`](2026-08-14-far-maze-and-dense-random/) | 2026-08-14 | maze 127 vs 127-far; nested 64@40/45/50% and 128@30/40/45% | Query-length maze contrast plus denser nested random. |
| [`2026-08-14-braid-and-denser-nested`](2026-08-14-braid-and-denser-nested/) | 2026-08-14 | maze 127 vs braid 0.5; nested 64@50–52% and 128@45–50% | Braided maze contrast and denser nested random (md lowered so connect-once succeeds). |
| [`2026-08-14-maze255-braid-and-128-md48`](2026-08-14-maze255-braid-and-128-md48/) | 2026-08-14 | maze 127/255 ± braid; nested 128@45–50% md 28 vs md 48 | Size×braid interaction and 45–50% nested random at the original Manhattan 48 (fewer connected queries). |
