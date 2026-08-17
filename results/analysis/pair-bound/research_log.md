# Pair-bound research log

Living document for **official `F2EPairLowerBound` studies**: what we ran, what we locked, what we concluded, and what to try next. Update it when a decision is locked or an analysis folder is added. Do not paste full tables here — those live in each generated analysis README.

Legacy gap-F2E results are **not** recorded here. See [`docs/research_log.md`](../../../docs/research_log.md) for the master log (including the frozen gap timeline) and [`results/analysis/legacy/`](../legacy/).

- Pair-bound analysis index: [`README.md`](README.md)
- Project definition (scope, Idea A/B): [`docs/project_definition.md`](../../../docs/project_definition.md)
- Locked pairing/stats plan: [`.cursor/plans/paired_analysis_workflow.plan.md`](../../../.cursor/plans/paired_analysis_workflow.plan.md)

## How we keep results

| Kind | Where | Rule |
| --- | --- | --- |
| Raw study CSVs / JSON | `results/study/pair-bound/` | Keep old files. New configs get new stems. Never write into `results/study/legacy/`. |
| Analysis pass | `results/analysis/pair-bound/YYYY-MM-DD-short-slug/` | **New pass → new folder.** Never overwrite. Never mix `--input-dir` with `results/study/legacy`. |
| This log | `results/analysis/pair-bound/research_log.md` | Hand-edited. Record decisions and next questions. |
| Generated tables | `<run>/README.md` | Machine-written. Do not edit by hand. |

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/YYYY-MM-DD-short-slug
```

Follow-up experiments get **new `*_opt` YAML** under `configs/followup/` (copy seeds from [`configs/followup/retired/`](../../../configs/followup/retired/) if needed), new CSVs under `results/study/pair-bound/`, then a **new analysis folder** here. Use `--experiment` for a follow-up-only slice (`--allow-opt-subset`); do not mix with the five official stems.

---

## Locked methodology (do not silently change)

These are in force until we explicitly revise this section. Same locks as [`docs/research_log.md`](../../../docs/research_log.md).

**Search / export**

- Compare F2F vs F2E **inside one SFBDS**; A* is a sidecar (cost / success), not mixed into pair-expansion savings.
- SFBDS `expanded` is **pairs**; A* `expanded` is **states**. Never compare those units.
- Optional SFBDS fields: `forward_expanded`, `backward_expanded`, `meeting_g_F`, `meeting_g_B`, `direction_switches` (A* stays null). Count after `choose_by_branch_factors`, not at `expanded += 1`.
- Exported `obstacle_density` is realized `count / (h*w)`. YAML `obstacle_density` remains the sampler target.

**Nested random maps**

- `obstacle_density` XOR `obstacle_densities` (random only). Shuffle non-reserved cells once; prefix `round(d * n_candidates)` so `obs10 ⊆ obs20 ⊆ obs30`.
- `ensure_connected_query` **once** on the densest map; reuse relocated S/G at lower densities. If the current pair is already connected, that component is tried first; otherwise every free component is tried (largest first), not only the largest blob.
- Optional YAML `query_sample.skip_unconnected` (default false): if connect-once cannot place a pair at `min_manhattan`, skip that query instead of aborting. `query_index` may have gaps; realized n may be `< count`. Use only when the scientific plan is “accept fewer queries,” not as a silent default.
- Skip ASCII visuals when `obstacle_densities` is set.
- Independent `*_d10/d20/d30` CSVs belong to **legacy** sampling. They **must not** enter nested `obstacle_count` tests, `overall_random`, or `saving_by_density.png`.
- Optional YAML `maze_braid` in `[0, 1)` (maze only, default 0): after the perfect spanning tree, open that fraction of leftover inter-room walls. Same seed + queries as a `maze_braid: 0` run share endpoints; the braided map has extra openings.

**Pairing and stats**

- `family_id = experiment:generator_kind:h×w:seed:query_index`; `pair_id = family_id:map_hash`.
- Solved pair = both SFBDS success and not timed out. Timeouts stay in `paired.csv` with null ratios; win % / means / tests use solved only.
- **`cost_mismatch`** = F2F, F2E, or successful A* disagree on solution cost. Those rows stay in `paired.csv` but are excluded from Wilcoxon, sign, F2F-fewer / F2E-fewer / ties, expansion saving %, **and plots**.
- Detour = solution cost / Manhattan, using **A* cost** when A* succeeded.
- Saving % = `(F2E − F2F) / F2E × 100`. Primary test: two-sided Wilcoxon on `expansion_diff`, `zero_method="wilcox"`, exact if `n_untied ≤ 25`, **p = null if `n_untied < 10`**.
- Do **not** stack nested densities as independent n. Wilcoxon for overall nested random = **one median `expansion_diff` per `family_id`**. Per-density tests stay uncollapsed and are keyed by **experiment × grid size × `obstacle_count`**. Holm for density is within one nested config, not across experiments or sizes. Table F2F-fewer / F2E-fewer / ties match `n_test` (collapsed families when nested). Skip `overall_random` Wilcoxon when the run mixes more than one nested experiment; use the per-experiment density table.
- Confirmatory: sign/binomial (F2F-fewer vs F2E-fewer, ties dropped). Holm Wilcoxon and Holm sign in **separate** families. Detour buckets exploratory (raw p only).
- Rank-biserial from **T+/T−**, not scipy’s `statistic`. Positive ⇒ F2F fewer expansions.
- Runtime must not drive the claim.
- Optional YAML `runtime_repeats` (default 1): median `runtime_sec` and `heuristic_time_sec` across **successful** repeats; expansions/path from the first successful run. TIMEOUT only if every repeat times out. Skip ASCII visuals when repeats > 1, nested densities are set, or the grid is ≥ 200×200.

**SFBDS-F2E pair bound (locked 2026-08-17)**

- Official `sfbds_f2e` **bound** is `F2EPairLowerBound`: on unit grids, `lb = g_F+g_B` when `u=v`, else `lb = max(g_F+MD(u,G), g_B+MD(S,v), g_F+g_B+1)`. SFBDS still stores remaining cost via `h_gap = max(0, lb − g_F − g_B)`.
- Official `sfbds_f2e` **search** is `official_f2e_searcher()`: that bound plus `f2e_policies()` (`BetterGReopenPolicy`: strictly better CLOSED `g` → remove then push). `SFBDSSearcher(F2EPairLowerBound())` is MVP NoReopen and is **not** official F2E. F2F stays `default_policies()` / `NoReopenPolicy`. Reopen is the hypothesized repair for the demonstrated pair-key inconsistency; empirically accepted on the frozen mismatch-row gate. Not a general proof of Late-stop optimality.
- Pair-bound CSVs **without** `_opt` are **NoReopen** F2E. Stems **with** `_opt` are reopen F2E. Cite the 64/128 reopen baseline from [`2026-08-17-reopen-opt/`](2026-08-17-reopen-opt/). Cite maze 255 / dense nested (30/40/45%) from [`2026-08-17-harder-opt/`](2026-08-17-harder-opt/). Cite maze 127 far/braid/timed, maze 255 braid, and denser nested from [`2026-08-17-far-braid-by-experiment/`](2026-08-17-far-braid-by-experiment/). Do not cite pooled maze, size 127/128/64, or the runtime block in [`2026-08-17-far-braid-opt/`](2026-08-17-far-braid-opt/). Cite pre-fix maze figures from [`2026-08-17-cost-clean-plots/`](2026-08-17-cost-clean-plots/) only as NoReopen. Do not cite legacy gap maze 255. The analysis CLI refuses a mix. A run that includes any official `_opt` stem must be exactly the five official stems; `--allow-opt-subset` is for a follow-up-only `*_opt` slice and does not mix those five with extras. Live follow-up YAMLs are `configs/followup/study_*_opt.yaml`. Generated READMEs emit the `--experiment` flags used for that run (and `--allow-opt-subset` when it was passed).
- Do not cite `results/study/legacy/` or `results/analysis/legacy/` as corrected F2E.

---

## Timeline

### 2026-08-17 — Pair-bound baseline (corridor 512, maze 127, open 128, nested random 64/128)

**Folder:** [`2026-08-17-baseline-study/`](2026-08-17-baseline-study/)  
**Input:** [`configs/study/`](../../../configs/study/) written to [`results/study/pair-bound/`](../../../results/study/pair-bound/). Same seeds and queries as the matching legacy CSVs. Not the leftover smaller/independent files (`corridor_256`, `maze_63`, `open_64`, `*_d10/d20/d30`).

**What we asked.** With official pair-bound F2E, on these grids, does F2F expand fewer pairs than F2E, and does that depend on map family, nested obstacle density, size, or detour?

**Headline (see generated README for tables).**

- **270** paired instances, all solved, **0** timeouts.
- **Open and corridor:** F2F and F2E tied on every solved pair. Wilcoxon p is null (`n_untied < 10`).
- **Maze 127:** F2F fewer pairs on **22/30** maps (0 F2E-fewer). Holm p ≈ 4.8e-07, rank-biserial 1.00, median saving 3.4%. Costs agree with A* on all 30. Legacy gap F2E on the same config was 21/30 F2F-fewer.
- **Nested random:** the 64×64 @ ~30% row in this snapshot (13 F2F-fewer, Holm p ≈ 0.0002) **includes 4 cost-mismatch maps**. Do not cite that p-value. See the cost-clean re-analysis below.
- **12 cost mismatches**, all nested-random: F2E solution cost **above** A* and F2F (typically +2). Maze/open/corridor costs agree.

**Decisions from this run.**

1. Maze is still the regime where F2F separates on expansions under the pair bound, and that slice is cost-clean.
2. Do not cite nested-random p-values from this snapshot.
3. The 12 suboptimal F2E paths on random maps are a correctness question — not a reason to mix in `results/study/legacy/`.

**Open questions (answered in the next entry).**

- Why does pair-bound F2E return a longer path than A*/F2F on those 12 nested-random maps? → NoReopen + remaining-cost adapter (230 better-`g` CLOSED discards on q=20).
- Do maze 255 / denser nested random still separate once costs are required to match A*? → still open; wait until F2E matches A*.

---

### 2026-08-17 — Cost-clean expansion tests and F2E mismatch diagnosis

**Folder:** [`2026-08-17-cost-clean-tests/`](2026-08-17-cost-clean-tests/)  
**Input:** same `results/study/pair-bound/` CSVs (stats-code fix; previous snapshot kept).

**What changed.** Expansion Wilcoxon / sign / F2F-fewer drop `cost_mismatch` rows (F2F, F2E, or successful A* disagree). Generated README claims an independent-file mix only when that mix is present.

**Headline.**

- Maze 127 unchanged: **22/30** F2F-fewer, Holm p ≈ 4.8e-07.
- Nested 64 @ 30% cost-clean: **`n_untied = 9`** (9 F2F-fewer). p **null**. No density group has `n_untied ≥ 10`.
- Replay of `study_random_64` q=20 @ 1228 obstacles (hash `d604ed0b69115ce9`): A*/F2F cost 53, F2E 57. F2E discarded **230** better-`g` CLOSED pairs. That was the **hypothesis at the time**; demonstrated in the q=20 optimality-diagnosis entry.

**Decisions.** Keep maze. Do not cite nested-random expansion p-values until F2E matches A* or a cost-clean protocol with `n_untied ≥ 10` is pre-registered. Do not cite plots in this folder as mismatch-free.

---

### 2026-08-17 — Cost-clean plots, diagnosis test, and legacy write refuse

**Folder:** [`2026-08-17-cost-clean-plots/`](2026-08-17-cost-clean-plots/)  
**Input:** same `results/study/pair-bound/` CSVs (plot filter; previous snapshots kept).

**What changed.**

1. Plots use the same cost-clean rows as Wilcoxon. Cite this folder’s figures.
2. Diagnosis test no longer asserts F2E cost 57; the strict xfail remains the optimality lock.
3. Runner / `load_config` refuse `results/*/legacy/`. Old-stem pilots are in `configs/pilot/retired/`.

**Headline.** Tables unchanged: maze 22/30; nested 64@30% `n_untied=9` → p null.

---

### 2026-08-17 — F2E optimality diagnosis (q=20); fix not started

Same instance as the cost-clean xfail. **Demonstrated:** path-dependent F2E `h_gap` + NoReopen. F2E never generated `(m,m)` at g=53; same meeting cell as F2F at g=57 (`g_F` 45 vs 41). F2F: 0 CLOSED better-`g`. F2E: 230; 4 on F2F ancestor keys; one discarded `g` equals F2F’s `g`. Lipschitz 0 on generated edges; bound formula not the bug. **Hypothesized (not a proof):** reopen better CLOSED `g`. Forbidden: meeting `+1`.

---

### 2026-08-17 — F2E better-g reopen (Option C empirical gate)

Official F2E now uses `f2e_policies()` (better-`g` CLOSED remove-then-push). F2F stays NoReopen. Meeting `lb` unchanged. Late-on-first-meeting unchanged. Pre-fix pair-bound CSVs kept.

Reopen is the hypothesized repair for the demonstrated duplicate-key failure. It is empirically accepted only if all 12 frozen mismatches match A*. This is not yet a general proof of optimality.

**Gate passed.** All 12 frozen mismatch rows: F2E cost equals A*. q=20 is 53 with g=27 expanded. Pre-fix pair-bound CSVs kept. No `*_opt` studies in this pass.

---

### 2026-08-17 — Official F2E factory and citation lock

Official F2E is `official_f2e_searcher()`, not a bare bound searcher. On-disk `study_*.csv` (no `_opt`) remain NoReopen pair-bound F2E. Cite maze from `2026-08-17-cost-clean-plots` as pre-fix; do not cite nested-random p-values as reopen F2E.

---

### 2026-08-17 — Reopen F2E official baselines (`*_opt`)

**Folder:** [`2026-08-17-reopen-opt/`](2026-08-17-reopen-opt/)  
**Input:** five `study_*_opt` CSVs; `--experiment` for all five names. Pre-fix CSVs kept.

**Headline.** 270/270 solved, **0** cost mismatches. Maze 22/30 F2F-fewer, Holm p ≈ 4.77e-07. Nested 64@30% is now cost-clean with 13 F2F-fewer, Holm p ≈ 0.0002 (`n_untied ≥ 10`). Open/corridor still all ties.

---

### 2026-08-17 — Analysis README command and official `_opt` set

Generated READMEs emit the `--experiment` flags used for the run. Partial official `*_opt` analyses need `--allow-opt-subset`. Regenerated `2026-08-17-reopen-opt/README.md` in place (`--force`). Follow-ups: keep `_opt` plus `--experiment`, or a new stem; not `*_opt2`.

---

### 2026-08-17 — Maze 255 / denser nested random (`*_opt`)

**Folder:** [`2026-08-17-harder-opt/`](2026-08-17-harder-opt/)  
**Input:** `study_maze_255_opt`, `study_random_64_dense_opt`, `study_random_128_dense_opt`; `--experiment` × 3 and `--allow-opt-subset`. Same seeds as the matching follow-up YAMLs. Pre-fix and five-stem `*_opt` CSVs kept.

**Headline.** 210/210 solved, **0** cost mismatches. Maze 255: 26/30 F2F-fewer, Holm p ≈ 2.98e-08, median saving 3.8%. Nested density tests with `n_untied ≥ 10`: 64@40% (16/30), 64@45% (14 F2F-fewer, 1 F2E-fewer), 128@45% (11/30). Different seed than `study_random_64_opt`; do not pool.

---

### 2026-08-17 — Retire non-`_opt` follow-ups; official+follow-up mix refuse

Non-`_opt` follow-up YAMLs moved to [`configs/followup/retired/`](../../../configs/followup/retired/). `load_config` refuses them. `--allow-opt-subset` is follow-up-only and does not mix the official five with extras. Cite maze 127 / nested 64@30% from `2026-08-17-reopen-opt`; maze 255 / dense nested from this `2026-08-17-harder-opt` folder.

---

### 2026-08-17 — Far / braid / timed maze and denser nested (`*_opt`)

**Folder:** [`2026-08-17-far-braid-opt/`](2026-08-17-far-braid-opt/)  
**Input:** eight follow-up `*_opt` stems; `--allow-opt-subset`. Not mixed with the official five or the harder-opt three.

**Headline.** 450/450 solved, **0** cost mismatches. Do not cite pooled maze 60/120 (`timed` = maze 127 maps, 22/30). Far 15/30; 127-braid 12/30; 255-braid 11/30 (vs 26/30 perfect maze 255). Nested 64 d50 and 128 d45 (md 28) have `n_untied ≥ 10` at every density; 64 d52 and 128 d45 md 48 (n=20) p null. Do not pool md-28 with md-48. Do not cite this folder’s maze headline, size 127/128, or runtime slice.

---

### 2026-08-17 — Per-experiment follow-up README (stats-code fix)

**Folder:** [`2026-08-17-far-braid-by-experiment/`](2026-08-17-far-braid-by-experiment/)  
Same eight CSVs. Generated headline is per experiment; mixed maze/size skip Wilcoxon; runtime is `_timed` only (22/22, median ≈ 0.885). Cite this folder.

---

### 2026-08-17 — Offline eval-cost sensitivity (Option 3A)

**Folder:** [`2026-08-17-eval-cost-sensitivity/`](2026-08-17-eval-cost-sensitivity/)  
Existing `study_maze_127_opt`, `study_maze_255_opt`, and nested 64@30% rows from `study_random_64_opt` (`obstacle_count == 1228`). Offline `T_β = rest + β · heuristic_evals`. No new search.

**Headline.** No crossover to F2E. Median `T_F2F / T_F2E` stays `< 1` on all three families from `β = 0` through `10⁶×` observed Manhattan eval cost. Secondary only.

---

### 2026-08-17 — Heuristic-strength replay (F2F vs pair-bound F2E)

**Folder:** [`2026-08-17-heuristic-strength/`](2026-08-17-heuristic-strength/)  
Replay F2F + official F2E; both LBs on each `evaluate()` `(u,v,g)`. Nested 64@30% seed 110 vs 64@45% seed 210 (not paired maps).

**Headline.** F2E bound never strictly stronger. Open all-equal / all-tie. Maze bound advantage tracks maze wins; braid shrinks both. Nested 64@45% q=8 is F2E-fewer expansions despite F2F-stronger bounds. **Partially explains** the expansion result.

---

### 2026-08-17 — Heuristic-strength replay locks

Replay also matches frozen `heuristic_evals` and `solution_cost`. Spearman in the snapshot README is expansion-untied only. Pytest: mini `RecordingHeuristic` search, frozen splits, nested 64@45% q=8 `expansion_diff=-1`, snapshot query-8 bound stats. `query_summary.csv` / `family_summary.csv` are gitignore exceptions for this slug. `--check-only` does not write.

---

### 2026-08-17 — Eval-cost invariant test and `--force`

Script refuses a non-empty slug unless `--force`. Pytest locks 30 pairs × 3 families, `rest ≥ 0`, 0 F2E-fewer evals. Snapshot unchanged.

---

## Experiment freeze (2026-08-17)

Experimental phase is frozen for the report.

**Authoritative:** reopen `*_opt` only. Maze 127 / nested 64@30% → `2026-08-17-reopen-opt`. Maze 255 / dense nested → `2026-08-17-harder-opt`. Far/braid/timed/denser nested → `2026-08-17-far-braid-by-experiment`. This eval-cost folder is secondary.

**Main claims:** maze F2F-fewer expansions (127: 22/30; 255: 26/30), cost-clean; open/corridor ties; nested weaker and not pooled across seeds; braid reduces maze wins. Runtime is not co-primary. Late-stop remains Option C.

**Secondary:** eval-cost sweep (no crossover); maze 127 timed wall-clock; heuristic-strength replay (partial explanation).

**Future work (not done):** pair/result cache after instructor lock; Late-stop proof; incumbent stop; online expensive-`h` re-search.
