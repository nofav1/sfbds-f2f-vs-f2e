---
name: heuristic-strength-bounds
overview: Existing `*_opt` CSVs cannot reconstruct pair lower bounds. Replay official F2F and reopen F2E on six frozen families with a recording wrapper (no search-policy changes), compare both LBs on each evaluated `(u,v,g_F,g_B)`, and test whether F2F bound advantage tracks expansion savings.
todos:
  - id: script-replay
    content: "Write scripts/heuristic_strength.py: recording wrapper, YAML replay, hash/expanded match, on-the-fly stats + reservoir sample, --force"
    status: pending
  - id: run-six-families
    content: Replay open 128, maze 127, maze 255, maze 127 braid, nested 64@30% (seed 110), nested 64@45% (seed 210); abort on CSV mismatch
    status: pending
  - id: snapshot-writeup
    content: Write snapshot CSVs, two plots, README; update research logs and analysis index; copy plan to .cursor/plans/
    status: pending
  - id: verdict
    content: State whether bound strength explains / partially explains / does not explain the expansion result; do not commit
    status: pending
isProject: true
---

# Heuristic-strength analysis (F2F vs pair-bound F2E)

## 1. Existing data is **not** sufficient

Frozen [`results/study/pair-bound/*_opt.csv`](results/study/pair-bound/) rows have `expanded`, `heuristic_evals`, `runtime_sec`, and meeting `g`, but **no** `(u, v, g_F, g_B)` traces. Bound comparison cannot be reconstructed offline from those files.

Do **not** rerun the study matrix or overwrite `*_opt` CSVs. Replay F2F + official F2E only (skip A*), rebuild maps from the same YAMLs/seeds, and **assert `map_hash` and `expanded` match** the frozen CSV before using a query.

## 2. Algebraic fact (check, do not assume)

On 4-connected unit grids, official formulas are already in code:

- F2F: [`F2FManhattanHeuristic.evaluate`](src/sfbds_compare/heuristics/f2f.py) → `h_F2F = MD(u,v)`, so `LB_F2F = g_F + g_B + MD(u,v)`
- F2E: [`F2EPairLowerBound.lower_bound`](src/sfbds_compare/heuristics/f2e.py) as specified (`u==v` → `gsum`, else `max(f_F, f_B, gsum+1)`)

If `g_F ≥ MD(S,u)` and `g_B ≥ MD(v,G)` (true for tree path costs), then **`LB_F2F ≥ LB_F2E` on every pair**. The scientific question is the **size** of `LB_F2F − LB_F2E` and whether it tracks expansion savings — not whether F2E can beat F2F on a random feasible pair. Report any F2E-stronger observations as counterexamples (do not hide them).

## 3. Sampling / comparison method

**Population:** every pair on which SFBDS actually calls `evaluate` (insert/improve OPEN; same events as `heuristic_evals`). Not the union of unrelated pair-keys, and not a random grid sample.

For each recorded `(u, v, g_F, g_B, problem)` from **either** search, compute **both** LBs. That is the same pair-state under both formulas. Tag `source ∈ {f2f, f2e}`.

Report three views, labeled as such:

- F2F-search sample
- F2E-search sample
- pooled (source-tagged; **not** claimed as “pairs both algorithms expanded”)

Do **not** treat `(u,v)` key intersection as the primary comparison: `g` often differs, and intersection is a selected subset.

Per observation: `LB_F2F`, `LB_F2E`, `diff = LB_F2F − LB_F2E`, `ratio = LB_F2F / LB_F2E` when `LB_F2E > 0`.

Per query (from frozen `*_opt` expansions + replay diffs):

- `expansion_diff = F2E_expanded − F2F_expanded` (from frozen CSV, after replay match)
- median/mean `diff`, fraction F2F-stronger / equal / F2E-stronger

Then correlate query-level median `diff` vs `expansion_diff` (and vs F2F-stronger fraction). Do not force the maze/open/braid/dense story. On nested 64@45%, call out the single F2E-fewer expansion query: does it also show a weaker (or reversed) F2F bound advantage?

## 4. Families (official reopen `*_opt` only)

| Family | Config / CSV | Filter | Why |
| --- | --- | --- | --- |
| Open 128 | [`study_open_128_opt`](configs/study/study_open_128_opt.yaml) | none | expected ties |
| Maze 127 | [`study_maze_127_opt`](configs/study/study_maze_127_opt.yaml) | none | main maze result (22/30) |
| Maze 255 | [`study_maze_255_opt`](configs/followup/study_maze_255_opt.yaml) | none | stronger maze (26/30) |
| Maze 127 braid 0.5 | [`study_maze_127_braid_opt`](configs/followup/study_maze_127_braid_opt.yaml) | none | same seed 140 / endpoints as maze 127 |
| Nested 64 @ 30% | [`study_random_64_opt`](configs/study/study_random_64_opt.yaml) | `obstacle_count == 1228` | seed **110**; 13/30 F2F-fewer in [`2026-08-17-reopen-opt`](results/analysis/pair-bound/2026-08-17-reopen-opt/) |
| Nested 64 @ 45% | [`study_random_64_dense_opt`](configs/followup/study_random_64_dense_opt.yaml) | `obstacle_count == 1842` | seed **210**; 14 F2F-fewer and **1 F2E-fewer** in [`2026-08-17-harder-opt`](results/analysis/pair-bound/2026-08-17-harder-opt/) |

**Seeds differ.** Nested 64@30% (seed 110) and nested 64@45% (seed 210) are a **family-level contrast**, not a paired density progression on identical maps. Do not write “raising density from 30% to 45% on the same instances.” Same 64×64 size; different nested families. The 45% slice is useful because it has enough non-ties and a single F2E-fewer query as a bound-vs-expansion counterexample check.

No corridor (open covers the tie regime). No NoReopen / legacy CSVs. No new map sizes.

## 5. Instrumentation (minimum)

Do **not** change search, policies, or heuristic formulas.

Isolated script [`scripts/heuristic_strength.py`](scripts/heuristic_strength.py):

- Rebuild problems via existing [`runner._problems_for_query`](src/sfbds_compare/experiments/runner.py) / `load_config` (nested prefixes + connect-once stay correct).
- Wrap the official heuristic in a recorder that delegates `evaluate` unchanged and logs `(u,v,g_F,g_B)`.
- F2F searcher: `SFBDSSearcher(Recording(F2FManhattanHeuristic()))` (still default NoReopen).
- F2E searcher: `official_f2e_searcher()` with the bound wrapped the same way (still `f2e_policies()`).
- Compute both LBs in the script: `LB_F2F = gsum + MD(u,v)`, `LB_F2E = F2EPairLowerBound.lower_bound(...)`.
- Do not store every maze-255 pair (~30k evals × 30 × 2). Keep running counts/quantiles plus a **reservoir sample** (~200 pairs per family × source) for the pair CSV.
- Sanity: replay `expanded` and `map_hash` must match the frozen `*_opt` row; abort that family on mismatch.

Refuse a non-empty out-dir unless `--force` (same freeze-slug rule as eval-cost).

Tiny unit test: feasible random `(u,v,g)` on an open grid has `LB_F2F ≥ LB_F2E`; meeting pairs have `diff = 0`.

## 6. Expected runtime

Replay is F2F+F2E only (no A*, no visuals). Maze 255 dominates (~0.5–1 s/query/algo in the frozen CSVs → on the order of **1–3 minutes**). Other five families are smaller. Recorder overhead is small if we aggregate on the fly. **Budget ~10–15 minutes** wall-clock including plots; stop if a family mismatches the frozen CSV.

## 7. Outputs

New snapshot only: [`results/analysis/pair-bound/2026-08-17-heuristic-strength/`](results/analysis/pair-bound/2026-08-17-heuristic-strength/)

- `query_summary.csv` — one row per query × family (bound stats + frozen expansion_diff)
- `pair_sample.csv` — reservoir sample with source tag
- `family_summary.csv` / table in README
- Two plots: (1) per-family % F2F-stronger / equal / F2E-stronger; (2) scatter median bound-diff vs expansion_diff, colored by family
- Hand-written README: population definition, sampling, findings vs hypothesis, counterexamples (including the 64@45% F2E-fewer query), seed warning for 30% vs 45%, **explains / partially explains / does not explain** the expansion result
- Timeline entries in [`docs/research_log.md`](docs/research_log.md), [`results/analysis/pair-bound/research_log.md`](results/analysis/pair-bound/research_log.md), index row in [`results/analysis/README.md`](results/analysis/README.md)
- Repo plan copy: [`.cursor/plans/heuristic-strength-bounds.plan.md`](.cursor/plans/heuristic-strength-bounds.plan.md)

Cite expansions from `reopen-opt` / `harder-opt` / `far-braid-by-experiment`. This folder is a **mechanism** analysis, not a new co-primary result.

Do not commit until findings are reviewed.
