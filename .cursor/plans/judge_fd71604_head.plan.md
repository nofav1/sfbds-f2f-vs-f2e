---
name: Judge fd71604 HEAD
overview: Independent review of commits fd71604 through 7217852. The four medium findings are implemented (load skip, runtime_repeats, density grouping, connect-once components).
todos:
  - id: skip-analysis-csvs
    content: Skip paired/summary/stats.csv in load_raw_csvs; add mixed-dir test
    status: completed
  - id: runtime-repeats-timeout
    content: Aggregate runtime_repeats as median of successes; TIMEOUT only if all fail
    status: completed
  - id: density-group-by-experiment
    content: Do not pool obstacle_count across experiments or grid sizes in Holm
    status: completed
  - id: connect-all-components
    content: "ensure_connected_query: search more than the largest component"
    status: completed
isProject: true
---

# Judge: fd71604 through HEAD

Review range: `fd71604` (`feat(analysis): pair F2F vs F2E and nest random densities`) through `7217852` (maze-255 braid + nested 128 at Manhattan 48). Tests: **65 passed** (`test_analysis`, `test_experiment_config`, `test_generators`, `test_experiment_smoke`). Treat that as evidence, not proof.

## Reconstruction

**Intended behavior.** Post-hoc F2F vs F2E pairing with Wilcoxon/sign tests; nested random densities as shuffle-prefixes with connect-once; append-only analysis folders; follow-ups (harder maze, braid, denser random, `runtime_repeats`, `skip_unconnected`).

**Architecture.** Raw CSVs in [`results/study/`](results/study/) → [`python -m sfbds_compare.analysis`](src/sfbds_compare/analysis/__main__.py) with `--experiment` filters → snapshot under [`results/analysis/<slug>/`](results/analysis/README.md). Generator/runner in [`config.py`](src/sfbds_compare/experiments/config.py), [`generators.py`](src/sfbds_compare/experiments/generators.py), [`runner.py`](src/sfbds_compare/experiments/runner.py).

**Invariants.** Pair expansions only; no stacked nested n; A* detour; timeouts excluded from tests; `obs10 ⊆ obs20 ⊆ …`; visuals skipped for nested / repeats / ≥200×200; new analysis pass → new folder.

## Prior judge items (from the uncommitted analysis review)

- **Fixed:** plot `paired_xy` alignment ([`plots.py`](src/sfbds_compare/analysis/plots.py)); A* vs SFBDS detour test; nested obstacle-set inclusion smoke test; nested CLI skip-visuals; pooled `map_family=random` Wilcoxon skipped (with `n_test`).
- **Still open:** [`load.py`](src/sfbds_compare/analysis/load.py) still globs every `*.csv`.

## Findings

### 1. Medium — `load_raw_csvs` will ingest analysis CSVs

**Where:** [`src/sfbds_compare/analysis/load.py`](src/sfbds_compare/analysis/load.py) lines 64–75.

**Why.** `root.glob("*.csv")` then `coerce_raw_row` with no stem/schema allowlist.

**Failure.** `--input-dir` pointing at an analysis run (or `results/study` after someone copies `paired.csv` there) raises `KeyError: 'algorithm'`, or silently mixes rows if columns overlap. Leftover [`results/analysis/paired.csv`](results/analysis/paired.csv) makes `--input-dir results/analysis` especially easy to get wrong.

**Fix.** Skip `paired.csv` / `summary.csv` / `stats.csv`; require raw columns before coerce; unit-test a mixed directory.

### 2. Medium — `runtime_repeats` treats any timeout as the whole result

**Where:** [`src/sfbds_compare/experiments/runner.py`](src/sfbds_compare/experiments/runner.py) lines 187–208.

**Why.** Locked log: median times, expansions from the first **successful** run. Code: if any repeat timed out, return that timeout and drop successful repeats.

**Failure.** `study_maze_127_timed` (`runtime_repeats: 5`): one slow repeat marks the query timed out even if 4/5 solved. Published timed maze CSV had 0 timeouts, so those numbers are probably fine; the protocol is still wrong.

**Fix.** Median over non-timeout repeats; keep first success; TIMEOUT only if all repeats time out. Test mixed success/timeout.

`test_runtime_repeats_keeps_expansions_and_skips_visual` only covers a 4×4 open map that never times out — same-way-wrong with the implementation.

### 3. Medium — `obstacle_count` tests pool distinct experiments

**Where:** [`src/sfbds_compare/analysis/summarize.py`](src/sfbds_compare/analysis/summarize.py) lines 38–41 and 163; headline in [`results/analysis/2026-08-14-maze255-braid-and-128-md48/README.md`](results/analysis/2026-08-14-maze255-braid-and-128-md48/README.md).

**Why.** Density groups are only `str(obstacle_count)`. Same 128×128 prefix `k` from `study_random_128_d45` (md 28, n=30) and `study_random_128_d45_md48` (md 48, n=17) merge. Holm `m` also spans every density key in the run (64 and 128 together).

**Failure.** Latest snapshot headline claims nested tests with `n_untied ≥ 10` at counts `{7372, 7781, 8191}` on **47** families — that is md-28 + md-48 stacked. The research log warns; the generated README does not. A reader of the snapshot README will take the pooled Holm p as an md-48 confirmation.

**Fix.** Group density as `experiment` or `{h}x{w}:{obstacle_count}:{experiment}`. Holm within one nested config, not across sizes. Keep `--experiment` filters as the operational guard until then.

### 4. Medium — `ensure_connected_query` only searches the largest component

**Where:** [`src/sfbds_compare/experiments/generators.py`](src/sfbds_compare/experiments/generators.py) lines 144–180.

**Why.** After a failed current pair, sampling is only in `_largest_component`. At ~45–50% obstacles a smaller component can still have Manhattan ≥ `min_manhattan`.

**Failure.** `study_random_128_d45_md48` skipped 13/30. Some skips may be “largest blob is compact,” not “no connected pair exists.” Connectivity-limit claims in the log can be overstated.

**Fix.** Try components (prefer current if connected, then largest) until a pair meets `min_manhattan`. Test a map where only a smaller component has enough span.

### 5. Low — Collapsed win counts computed then discarded

**Where:** [`summarize.py`](src/sfbds_compare/analysis/summarize.py) lines 56–87.

**Why.** `n_f2f_t, n_f2e_t, n_tie_t` from `collapse_random_diffs` are unused. Tables show uncollapsed F2F-fewer beside collapsed `n_test`.

**Failure.** `overall_random` with 12 families × 3 densities all F2F-better: F2F fewer = 36 next to `n_test=12`.

**Fix.** Report collapsed win counts beside `n_test` (or extra columns).

### 6. Low — Pooled `map_family=random` always skips tests

**Where:** [`summarize.py`](src/sfbds_compare/analysis/summarize.py) line 147.

**Why.** Skip is unconditional. `overall_random` exists only when some rows have `nested_density`.

**Failure.** Independent-only random input: no density tests, no `overall_random`, and pooled random Wilcoxon also skipped.

**Fix.** Skip only when the bucket mixes nested + independent (or `n_test != n_solved`).

### 7. Low — CLI does not enforce append-only `--out-dir`

**Where:** [`__main__.py`](src/sfbds_compare/analysis/__main__.py) lines 34–38, 57–63.

**Failure.** `--out-dir results/analysis` or reusing a slug overwrites `README.md` / CSVs. Cursor rules say not to; the program still will.

**Fix.** Refuse the analysis parent; refuse a non-empty existing dir unless `--force`.

### 8. Low — Maze `obstacle_density` is stored and ignored

**Where:** [`config.py`](src/sfbds_compare/experiments/config.py) (scalar density parsed for every kind); maze `build_problem` never uses it.

**Fix.** Reject non-zero `obstacle_density` unless `kind == "random_obstacles"`.

## Requirements apparently satisfied

- Nested shuffle-prefix + connect-once + shared endpoints; XOR densities; skip visuals for nested / repeats / large grids
- `pair_id` / `family_id`; A* detour (now actually tested); timeouts excluded from means; T+/T− rank-biserial; `n_untied < 10` → null p; nested not stacked in Wilcoxon
- `maze_braid` leftover-wall fraction; braid configs reuse maze seeds
- `skip_unconnected` drops queries and continues; `query_index` gaps allowed
- Append-only analysis folders, research log, `--experiment` filter
- Follow-up YAMLs match `_FOLLOWUP_SPECS` tests

## Requirements not demonstrated

- Detour plot / load glob robustness against analysis CSVs
- `runtime_repeats` mixed timeout (locked protocol)
- Connect-once on a non-largest component
- Density Holm stratified by experiment / size (latest snapshot README is pooled)
- Distinct prefix `k` for close density floats
- CLI refusal to overwrite a previous analysis slug

## Tests to add

1. `load_raw_csvs` ignores `paired.csv` beside a raw study CSV
2. `runtime_repeats`: 2 successes + 1 timeout → success + median of successes
3. `ensure_connected_query` succeeds when only a smaller component meets `min_manhattan`
4. Two nested experiments with the same `obstacle_count` do not share one density test row
5. `--out-dir` equal to `results/analysis` (or an existing non-empty slug) fails without `--force`

## Do you need to rerun?

**No solver rerun for the published expansion claims.** Maze, braid, nested 64, nested 128 @ md 28, and timed maze CSVs stay valid. Fix code first if you want; then new stems / new analysis folders — never overwrite.

**Do not rerun**

- Baseline study, maze 63/127/255, braid, nested random that already connected 30/30
- `study_maze_127_timed` — 0 timeouts, so the buggy “any timeout wins” path did not fire
- Anything just because `load_raw_csvs` or `--out-dir` are weakly guarded

**Optional and cheap (analysis CLI only, existing CSVs)**

- Re-analyze `study_random_128_d45_md48` **alone** into a new `results/analysis/<slug>/` so the generated README is not pooled with md 28. The research log already has the correct 17-family numbers; this only cleans the snapshot headline.
- Delete leftover `results/analysis/paired.csv` (locked copy at the analysis root). Not a rerun.

**Rerun searches only after a code fix, and only these**

- `ensure_connected_query` searches all components → **only** high-density + high-md configs that skipped queries (`study_random_128_d45_md48`). New stem; keep the old 17 families. Other nested runs that placed 30/30 do not change.
- `runtime_repeats` timeout aggregation → timed maze **only if** a later run actually mixes success and timeout. Not needed for the current timed CSV.

**Bottom line.** The analysis/stats core and nested generation match the locked plan; five of six earlier review items were fixed. Do not trust mixed-input `obstacle_count` Holm in the latest snapshot README (the log is right; the generated headline is not). Fix timeout aggregation and connect-once before treating high-density skip rates or median-of-5 timing as protocol-correct. Do not rerun the full study matrix.
