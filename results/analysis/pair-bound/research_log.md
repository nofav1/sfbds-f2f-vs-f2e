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

Follow-up experiments get **new YAML** under `configs/followup/` (or `configs/study/`), new CSVs under `results/study/pair-bound/`, then a **new analysis folder** here. Use `--experiment` to select a subset.

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

- Official `sfbds_f2e` is `F2EPairLowerBound`: on unit grids, `lb = g_F+g_B` when `u=v`, else `lb = max(g_F+MD(u,G), g_B+MD(S,v), g_F+g_B+1)`. SFBDS still stores remaining cost via `h_gap = max(0, lb − g_F − g_B)`.
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
- Replay of `study_random_64` q=20 @ 1228 obstacles (hash `d604ed0b69115ce9`): A*/F2F cost 53, F2E 57. F2E discarded **230** better-`g` CLOSED pairs → **NoReopen + remaining-cost adapter**, not a bound-wiring bug.

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

## Next experiment (not started)

Nothing else is queued until we pick one of:

1. **Fix F2E suboptimality** (reopen on better CLOSED `g`, or a consistent remaining-cost mapping) so the xfail on q=20 can be removed.
2. **Maze 255 / denser nested random** under pair-bound, only after costs match A*.
3. **Cache ablation** — only after instructor/scope lock.

When we choose, add a YAML under `configs/followup/` if needed, run into `results/study/pair-bound/` without deleting old CSVs, analyze into `results/analysis/pair-bound/YYYY-MM-DD-<slug>/` with `--experiment` filters, and add a row here plus in [`../README.md`](../README.md) and [`docs/research_log.md`](../../../docs/research_log.md).
