---
name: eval-cost-sensitivity-3a
overview: Offline heuristic-cost sensitivity on existing reopen `*_opt` CSVs for maze 127, maze 255, and nested 64@30%. One isolated script, one CSV, one figure, a short summary, then an experiment freeze. No new searches or infrastructure.
todos:
  - id: script-and-run
    content: Write scripts/eval_cost_sensitivity.py and emit CSV + one figure + README under results/analysis/pair-bound/2026-08-17-eval-cost-sensitivity/
    status: completed
  - id: logs-and-index
    content: Update docs/research_log.md, pair-bound research_log.md, and results/analysis/README.md; copy plan to .cursor/plans/
    status: completed
  - id: freeze-and-stop
    content: Propose experiment freeze in chat; do not implement further; ask to commit
    status: completed
isProject: true
---

# Option 3A: offline eval-cost sensitivity

## Data available (already inspected)

All three target families are present under [`results/study/pair-bound/`](results/study/pair-bound/) with `expanded`, `heuristic_evals`, `runtime_sec`, and `heuristic_time_sec`. Pair F2F vs F2E on `(query_index, obstacle_count, map_hash)`. Do **not** use legacy gap CSVs or NoReopen non-`_opt` files.

| Family | Source | Filter | n pairs | Notes |
| --- | --- | --- | --- | --- |
| Maze 127 | [`study_maze_127_opt.csv`](results/study/pair-bound/study_maze_127_opt.csv) | none | 30 | Cite expansions from [`2026-08-17-reopen-opt`](results/analysis/pair-bound/2026-08-17-reopen-opt/). Use this CSV, not `_timed`. |
| Maze 255 | [`study_maze_255_opt.csv`](results/study/pair-bound/study_maze_255_opt.csv) | none | 30 | Cite expansions from [`2026-08-17-harder-opt`](results/analysis/pair-bound/2026-08-17-harder-opt/). |
| Nested 64 @ 30% | [`study_random_64_opt.csv`](results/study/pair-bound/study_random_64_opt.csv) | `obstacle_count == 1228` (seed 110) | 30 | Do **not** use `study_random_64_dense_opt` (seed 210). |

Sanity from the same files:

- `runtime_sec - heuristic_time_sec` is never negative.
- Recorded `heuristic_time_sec` is only ~3–7% of wall-clock (Manhattan is cheap).
- Observed per-eval cost is ~6.5e-7 s/eval.
- On these queries F2E **never** has fewer `heuristic_evals` than F2F (maze 127: 22/0/8; maze 255: 26/0/4; nested 30%: 13/0/17). So a high-`beta` crossover **to F2E** is not expected; do not manufacture one.

No missing-metric blocker. No new experiment.

## Cost model

Preferred model, supported by the data:

```text
rest = runtime_sec - heuristic_time_sec
T_beta = rest + beta * heuristic_evals
```

Compare `T_beta` of F2F vs F2E on each paired query.

- `beta` is a synthetic seconds-per-evaluation knob. `beta = 0` keeps only non-heuristic residual. The recorded Manhattan cost is approximately the observed median `heuristic_time_sec / heuristic_evals`.
- Sweep `beta` as multipliers of that observed median: `0, 0.1×, 1×, 10×, 100×, 1e3×, 1e4×, 1e5×, 1e6×` (covers current cheap `h` through extremely expensive evals). Also store absolute `beta` in seconds/eval.
- Per family, report: `n_f2f_cheaper`, `n_f2e_cheaper`, `n_tie`, median `T_F2F / T_F2E`, total-`T` ratio.
- Crossover: first `beta >= 0` where median ratio `> 1` or F2E cheaper on a majority. If none, say so.

**Limitations (must appear in the summary):** offline rescaling does not change search decisions; `rest` is Python/OPEN/CLOSED overhead, not a clean expansion-cost constant; single-shot runtime (not timed repeats); a real expensive heuristic could also change *which* nodes expand.

## Implementation (tiny, isolated)

Add [`scripts/eval_cost_sensitivity.py`](scripts/eval_cost_sensitivity.py) only. Do not touch search, heuristics, analysis CLI, or existing `*_opt` CSVs.

Write a **new** snapshot (never overwrite):

[`results/analysis/pair-bound/2026-08-17-eval-cost-sensitivity/`](results/analysis/pair-bound/2026-08-17-eval-cost-sensitivity/)

- `sensitivity.csv` — one row per family × `beta`
- `cost_ratio_vs_beta.png` — one figure: three lines (maze 127 / maze 255 / nested 64@30%), x = `beta` (log, seconds/eval), y = median `T_F2F / T_F2E`, horizontal line at 1
- `README.md` — hand-written report summary (this folder is not produced by `python -m sfbds_compare.analysis`, so it is not a generated README)

Then update [`docs/research_log.md`](docs/research_log.md), [`results/analysis/pair-bound/research_log.md`](results/analysis/pair-bound/research_log.md), and [`results/analysis/README.md`](results/analysis/README.md). Copy this plan to [`.cursor/plans/eval-cost-sensitivity-3a.plan.md`](.cursor/plans/eval-cost-sensitivity-3a.plan.md).

Do **not**: cache, incumbent stop, optimality proof, new map families, overwrite CSVs, change F2F/F2E, polish the analysis package.

## After the run (freeze, then stop)

In chat and in the research log, propose an **experiment freeze**:

- **Authoritative:** reopen `*_opt` only. Maze 127 / nested 64@30% from `2026-08-17-reopen-opt`; maze 255 / dense nested from `2026-08-17-harder-opt`; far/braid/timed/denser nested from `2026-08-17-far-braid-by-experiment`. This sensitivity folder is secondary.
- **Main claims:** expansion-geography F2F vs official reopen F2E (maze win counts, cost-clean, braid weakens, open/corridor ties). Runtime is not co-primary.
- **Secondary:** this eval-cost sweep; maze 127 timed wall-clock.
- **Future work (explicitly not done):** pair/result cache (instructor lock), Late-stop proof, incumbent stop, online expensive-`h` re-search.

Do not implement anything else. Ask before committing.
