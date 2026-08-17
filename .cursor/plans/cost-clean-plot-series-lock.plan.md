---
name: Cost-clean plot series lock
overview: Lock write_plots against drawing cost_mismatch rows by asserting the series it actually passes to matplotlib. Leave F2E discard causation in the research log; the strict xfail remains the optimality spec.
todos:
  - id: plot-drawn-rows
    content: Extract the row list write_plots draws from; test captured scatter/boxplot series omit the mismatch (length 1, query_index 0)
    status: completed
  - id: diagnosis-causation
    content: Do not add an F2F discard-count CI lock; keep xfail as the optimality spec and leave causation in the log
    status: completed
isProject: true
---

# Cost-clean plot series lock

Cite maze tables and [`results/analysis/pair-bound/2026-08-17-cost-clean-plots/`](results/analysis/pair-bound/2026-08-17-cost-clean-plots/) figures. Do not cite nested-random p-values. Do not cite plots under `2026-08-17-cost-clean-tests`.

No new analysis slug. This is a test/code-path lock, not a stats-code change that would rewrite tables.

## Finding 1 (do this)

[`test_plots_omit_cost_mismatch_rows`](tests/unit/test_analysis.py) currently checks `expansion_test_rows(paired)` and that `"expansion_test_rows"` appears in `inspect.getsource(write_plots)`. That stays green if `write_plots` calls the helper and then scatters from `paired`.

**Change**

1. In [`plots.py`](src/sfbds_compare/analysis/plots.py), add a small helper that returns the rows every series is built from, e.g. `rows_for_plots(paired) -> expansion_test_rows(paired)`.
2. `write_plots` uses that list once (`drawn = rows_for_plots(paired)`). Nested-density boxplots filter `drawn`, not `paired`. No later `for r in paired`.
3. Replace the source-string test with an assertion on **drawn coordinates**:
   - Same two-row fixture (query 0 cost-clean 3 vs 9 expansions; query 1 mismatch 450 vs 2881).
   - Prefer capturing what `write_plots` passes to matplotlib (`Axes.scatter` x/y for `expansions_scatter`, `importorskip` matplotlib) **or** returning the numeric series from a helper that `write_plots` unpacks with no other row source.
   - Require `len == 1`, `query_index == 0`, and F2E expansions `== 9` (not 2881).

A helper-only test of `rows_for_plots` is not enough unless `write_plots` has no other path to `paired`. The captured scatter (or unpacked series) is the lock.

Do not re-run analysis. Existing `2026-08-17-cost-clean-plots` PNGs already used `expansion_test_rows`; this only stops a later regression.

## Finding 2 (do not change CI)

[`test_f2e_discards_better_g_closed_pairs_on_mismatch_instance`](tests/integration/test_cost_agreement.py) showing `counter.better > 0` on F2E does not prove discards caused cost 57. F2F uses the same NoReopen policy and matches A* (53).

- Keep the test as an observation (fingerprint, A* 53, F2F matches A*, F2E better-g visits happen).
- Keep [`test_f2e_matches_astar_on_study_random_64_q20_d1228`](tests/integration/test_cost_agreement.py) as the **only** optimality spec (strict xfail).
- Leave the causal sentence in [`docs/research_log.md`](docs/research_log.md) / the pair-bound log. Do not assert F2E cost 57. Do not add an F2F discard-count comparison unless we later want a diagnostic, not a spec.

## Out of scope

- Reopen / consistent adapter
- Maze 255 / denser nested random under pair-bound
- Overwriting `2026-08-17-cost-clean-tests` or `2026-08-17-cost-clean-plots`
