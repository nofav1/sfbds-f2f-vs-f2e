# Research log

Living document for **what we ran, what we locked, what we concluded, and what to try next**. Update it when a decision is locked or an analysis folder is added. Do not paste full tables here — those live in each generated analysis README.

- Analysis snapshots: [`results/analysis/README.md`](../results/analysis/README.md)
- Pair-bound living notes: [`results/analysis/pair-bound/research_log.md`](../results/analysis/pair-bound/research_log.md)
- Project definition (scope, Idea A/B): [`project_definition.md`](project_definition.md)
- Locked pairing/stats plan: [`.cursor/plans/paired_analysis_workflow.plan.md`](../.cursor/plans/paired_analysis_workflow.plan.md)

## How we keep results

| Kind | Where | Rule |
| --- | --- | --- |
| Raw study CSVs / JSON | `results/study/pair-bound/` (new) or `results/study/legacy/` (frozen gap F2E) | Keep old files. New configs get new stems. Never write new runs into `legacy/`. |
| Analysis pass | `results/analysis/pair-bound/YYYY-MM-DD-short-slug/` (or `.../legacy/...` for gap re-analysis) | **New pass → new folder.** Never overwrite. Never mix formulas in one `--input-dir`. |
| This log | `docs/research_log.md` | Hand-edited master log. Pair-bound-only notes: [`results/analysis/pair-bound/research_log.md`](../results/analysis/pair-bound/research_log.md). |
| Generated tables | `<run>/README.md` | Machine-written. Do not edit by hand. |

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/YYYY-MM-DD-short-slug
```

Follow-up experiments (new maps, densities, query lengths, cache settings) get **new YAML** under `configs/study/` (or a dated `configs/` subfolder), new CSVs under `results/study/pair-bound/`, then a **new analysis folder** under `results/analysis/pair-bound/`. Point `--input-dir` at `results/study/legacy` only when re-analyzing the frozen gap CSVs. Do not pass the parent `results/study/` (the glob is non-recursive and would mix formulas if it were not).

---

## Locked methodology (do not silently change)

These are in force until we explicitly revise this section.

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
- Independent `*_d10/d20/d30` CSVs (old non-nested sampling) may still sit in `results/study/legacy/`. They pair F2F vs F2E but **must not** enter nested `obstacle_count` tests, `overall_random`, or `saving_by_density.png`.
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
- Pair-bound CSVs **without** `_opt` (`study_maze_127.csv`, …) are **NoReopen** F2E. Stems **with** `_opt` are reopen F2E. Cite reopen results from [`results/analysis/pair-bound/2026-08-17-reopen-opt/`](../results/analysis/pair-bound/2026-08-17-reopen-opt/). Cite pre-fix maze figures from [`2026-08-17-cost-clean-plots`](../results/analysis/pair-bound/2026-08-17-cost-clean-plots/) only as NoReopen. Analysis of `results/study/pair-bound/` must pass `--experiment` so the two are not mixed (the CLI refuses a mix). A run that includes any `*_opt` name must include all five official `_opt` stems unless `--allow-opt-subset`. Generated READMEs emit the `--experiment` flags used for that run.
- Every study CSV and analysis snapshot **before this lock** used the project-choice gap `max(|MD(x,G)−MD(y,G)|, |MD(S,x)−MD(S,y)|)` (now `LegacyFixedEndpointGapHeuristic`, tests only). Those results are **legacy F2E**, not the pair bound. They live under `results/study/legacy/`, `results/pilot/legacy/`, and `results/analysis/legacy/`. Do not cite them as corrected F2E. New pair-bound output goes to the matching `pair-bound/` folders. Regenerate study CSVs only after approval.

---

## Timeline

### 2026-08-14 — Baseline grid study (64 / 128)

**Folder:** [`results/analysis/legacy/2026-08-14-baseline-study/`](../results/analysis/legacy/2026-08-14-baseline-study/)  
**Input:** all CSVs then in `results/study/` (now `results/study/legacy/`; corridor 256/512, maze 63/127, open 64/128, nested random 64/128, plus leftover independent random `*_d10/d20/d30`).

**What we asked.** On these grids, does F2F expand fewer pairs than F2E, and does that depend on map family, nested obstacle density, size, or detour?

**Headline (see generated README for tables).**

- **540** paired instances, all solved, **0** timeouts, **0** F2F vs F2E cost mismatches.
- **Open and corridor:** F2F and F2E tied on every solved pair. Wilcoxon p is null (`n_untied < 10`). Expansion savings are not expected here at these sizes.
- **Maze:** F2F fewer pairs on 32/60 maps (0 F2E-fewer). Holm p ≈ 4.7e-10, rank-biserial 1.00. Strongest size slice is 127 (21/30 F2F-fewer).
- **Nested random:** only **64×64 at ~30%** (1228 obstacles) had enough untied pairs (13 F2F-fewer, 0 F2E-fewer, Holm p ≈ 0.0002). 10%/20% on 64 and all three densities on 128 were almost all ties. Overall nested random (median per family) had `n_untied = 8` → p null.
- **Detour [2, ∞)** matches the maze story (32 F2F-fewer). Low-detour buckets are huge and mostly ties.
- Pooled `map_family=random` mixes nested + independent files; tests are skipped there on purpose.

**Decisions from this run.**

1. Treat maze (and high detour) as the regime where F2F can separate on **expansions**. Do not over-read open/corridor ties as “F2F never helps.”
2. Random density on 128×128 at 10–30% is still too easy / too tied for a density-crossover claim. If we chase density, start from **64×64 ≥ 30%** or harder sampling — not another 128 @ 10%.
3. Do not claim a **runtime** win. This pass is expansion-only; runtime plots are diagnostic.
4. Keep old independent random CSVs on disk; do not feed them into nested-density tests (already enforced in analysis).
5. Next experimental work should be a **new config + new analysis folder**, not a silent overwrite of this snapshot.

**Open questions for the next experiment.**

- Does F2F’s maze advantage grow with maze size, braid, or query length (`min_manhattan`)?
- Can we get `n_untied ≥ 10` on nested random without stacking densities (higher density, smaller maps, or longer queries)?
- When expansions differ, does wall-clock still favor F2E (Siag et al. 2023 open trade-off)?
- Pair/result cache (Idea B in the project definition) is **not** in this baseline. Expansion gaps on maze are the place a cache ablation would matter, if we go there.

---

### 2026-08-14 — Harder maze, denser nested random, maze timing

**Folders:**
- Expansions / density: [`results/analysis/legacy/2026-08-14-harder-followup/`](../results/analysis/legacy/2026-08-14-harder-followup/)
- Runtime protocol: [`results/analysis/legacy/2026-08-14-maze-runtime/`](../results/analysis/legacy/2026-08-14-maze-runtime/)

**Configs (new stems; old CSVs kept):** [`configs/followup/`](../configs/followup/) — `study_maze_255.yaml`, `study_random_64_dense.yaml`, `study_maze_127_timed.yaml`.

**What we asked.** (1) Does the maze F2F expansion advantage grow at 255×255? (2) Can nested random on 64×64 at 30/40/45% produce `n_untied ≥ 10` per density? (3) On maze 127 maps where expansions already differ, does median-of-5 wall-clock still favor F2E?

**Headline (see generated READMEs for tables).**

- **Maze size:** F2F-fewer counts **11/30 (63) → 21/30 (127) → 26/30 (255)**. All three sizes have Wilcoxon p < 0.001. Median expansion saving stays small (~0–0.9%). No F2E-fewer maze pair in this set. 90/90 maze solved, 0 timeouts.
- **Nested 64 dense (seed 210, connect-once):** 270/270 success. **30%** (1228 obstacles) still too tied (`n_untied=6`, p null). **40%** (1638): 15 F2F-fewer, 1 F2E-fewer, Holm p ≈ 1.2e-4. **45%** (1842): 15 F2F-fewer, 0 F2E-fewer, Holm p ≈ 1.2e-4. Overall nested random: 14 untied families, p ≈ 1.2e-4.
- **Timed maze 127:** same queries as `study_maze_127` (seed 140), `runtime_repeats: 5`, median `runtime_sec`. Expansions still 21/30 F2F-fewer (matches the baseline maze 127 win count). On those 21 untied pairs, F2F was **faster on the clock in all 21** (median runtime_ratio ≈ 0.94). Heuristic-time ratio remains ~0.33 (F2F spends less time in `h`, as expected). This is **not** a runtime primary claim; it is the Siag-style check on the maps that already separate on expansions.

**Decisions from this run.**

1. Maze F2F expansion wins **scale with maze size** in this generator; 255 is the strongest size slice so far. Median % saving is still small because many “wins” are modest pair-count gaps relative to huge maze expansions.
2. Density claims on random maps should start at **64×64 ≥ 40%** (nested prefixes), not 128 @ 10–30%. 30% remains mostly ties even with a new seed.
3. On maze 127, after median-of-5 timing, wall-clock did **not** reverse the expansion result (F2E was not faster). Still do not promote runtime to the primary test; heuristic evals remain cheaper for F2F on Manhattan, so this is not yet the expensive-`h` trade-off.
4. Cache ablation is still **not** started. Maze 255 / 64@45% are the natural places if we add it later.

**Still not queued:** pair/result cache (item 4). Longer `min_manhattan` on a fixed maze size was not run (size was the maze factor this pass).

---

### 2026-08-14 — Longer maze-127 queries and denser nested random

**Folder:** [`results/analysis/legacy/2026-08-14-far-maze-and-dense-random/`](../results/analysis/legacy/2026-08-14-far-maze-and-dense-random/)

**Configs:** [`configs/followup/study_maze_127_far.yaml`](../configs/followup/study_maze_127_far.yaml), [`study_random_64_d50.yaml`](../configs/followup/study_random_64_d50.yaml), [`study_random_128_dense.yaml`](../configs/followup/study_random_128_dense.yaml). Compared against existing `study_maze_127` (min_manhattan 60). Cache still off.

**What we asked.** (1) At fixed 127×127 maze, does raising `min_manhattan` 60 → 90 increase F2F’s expansion advantage? (2) Do nested 64×64 prefixes at 40/45/50% and nested 128×128 at 30/40/45% yield `n_untied ≥ 10`?

**Headline (see generated README for tables).** 240 paired rows, all solved, 0 timeouts, 0 cost mismatches.

- **Maze query length:** `study_maze_127` (md ≥ 60): **21/30** F2F-fewer, 9 ties. `study_maze_127_far` (md ≥ 90, seed 141): **12/30** F2F-fewer, 18 ties. Longer queries did **not** raise the win rate; ties increased. Pooled maze 127 still F2F-fewer 33/60, Holm p ≈ 5.4e-7. No F2E-fewer maze pair.
- **Nested 64 @ 40/45/50%** (seed 211, connect-once, 270/270): all three densities have `n_untied` 11–12. F2F-fewer 11, 11, 12 / 30; Holm p ≈ 0.003–0.002. 50% connected for all 30 families (obstacle counts 1638 / 1842 / 2047).
- **Nested 128 @ 30/40/45%** (seed 220, 270/270): 30% and 40% still too tied (4 and 8 untied). **45%** reaches 11 F2F-fewer, Holm p ≈ 0.003. No F2E-fewer on this 128 dense set.

**Decisions from this run.**

1. Maze **size** (63→127→255) was the lever that increased F2F-fewer rate; **longer Manhattan at fixed 127** did not. Do not treat “harder query” as interchangeable with “larger maze.”
2. Nested random: 64×64 is testable from **40% upward** (including 50%). On 128×128, start density claims at **45%**, not 30/40%.
3. Cache still off.

---

### 2026-08-14 — Braided maze 127 and denser nested random

**Folder:** [`results/analysis/legacy/2026-08-14-braid-and-denser-nested/`](../results/analysis/legacy/2026-08-14-braid-and-denser-nested/)

**Configs:** [`study_maze_127_braid.yaml`](../configs/followup/study_maze_127_braid.yaml) (`maze_braid: 0.5`, same seed/queries as `study_maze_127`), [`study_random_64_d52.yaml`](../configs/followup/study_random_64_d52.yaml), [`study_random_128_d45.yaml`](../configs/followup/study_random_128_d45.yaml).

**What we asked.** (1) At fixed 127×127 and the same endpoints, does opening 50% of leftover maze walls (braid) change the F2F expansion gap? (2) Nested 128 starting at 45% (drop 30/40%), and 64 just above 50%.

**Headline.** 240 paired rows, all solved, 0 timeouts.

- **Braid:** same 30 start/goal pairs as perfect maze 127. Obstacle count drops ~7936 → ~5952. F2F-fewer **21/30 → 11/30**; ties 9 → 19. No F2E-fewer. Loops made F2F and F2E agree more often, not less.
- **64×64 @ 50/51/52%** needed `min_manhattan` 16 (24 at ≥55% could not connect 30/30). All three densities stay too tied (`n_untied` 7, 7, and **8** at 52% = 7 F2F-fewer + 1 F2E-fewer). Going above 50% at 64 did not help.
- **128×128 @ 45/47.5/50%** needed `min_manhattan` 28 (48 at 50–55% could not connect). This is the strong slice: F2F-fewer **13 / 17 / 17** of 30; Holm p ≈ 2e-4 to 5e-5. No F2E-fewer.

**Decisions from this run.**

1. Perfect (unbraided) mazes are where F2F separates; braid toward open-with-loops **increases ties**. Do not expect braid to amplify the maze result.
2. Nested 128 **≥ 45%** (with a shorter Manhattan floor so connect-once succeeds) is the random density regime that actually unties. Tiny 64 steps above 50% are still mostly ties.
3. Connectivity, not timeout, is the limiter past ~50% obstacles at the old `min_manhattan` values.

---

### 2026-08-14 — Maze 255 braid and nested 128 @ 45–50% with `min_manhattan` 48

**Folder:** [`results/analysis/legacy/2026-08-14-maze255-braid-and-128-md48/`](../results/analysis/legacy/2026-08-14-maze255-braid-and-128-md48/)

**Configs:** [`study_maze_255_braid.yaml`](../configs/followup/study_maze_255_braid.yaml) (`maze_braid: 0.5`, same seed/queries as `study_maze_255`), [`study_random_128_d45_md48.yaml`](../configs/followup/study_random_128_d45_md48.yaml) (same densities and seed 221 as `study_random_128_d45`, `min_manhattan` 48, `skip_unconnected: true`). Compared against existing maze 127 / 127-braid / 255 and nested 128 d45 (md 28). Cache still off.

**What we asked.** (1) Does braid still increase F2F/F2E ties at 255×255, where perfect-maze size had helped? (2) Does the nested 128 @ 45–50% expansion gap survive the original Manhattan floor of 48, if we accept fewer than 30 connected queries?

**Headline.** 261 paired rows, all solved, 0 timeouts. Read per-experiment counts below; the generated density table **pools** md-28 and md-48 rows that share `obstacle_count`, so it is not the md-48 confirmatory test.

- **Maze 255 braid:** same 30 start/goal pairs as perfect maze 255. Walls ~32256 → ~24192. F2F-fewer **26/30 → 11/30**; ties 4 → 19. No F2E-fewer. Same direction as 127 (**21/30 → 11/30**). Size does not protect the perfect-maze gap from braid.
- **Nested 128 @ 45/47.5/50%, md 48:** connect-once at 50% with md 48 cannot place 30/30 (probe: ~15–19 of 30 across seeds). This run skipped **13/30** queries; **17** families remain (51 paired rows). F2F-fewer **6 / 7 / 8** of 17; ties 11 / 10 / 9; no F2E-fewer. `n_untied` is 6–8 **< 10** at every density, so Wilcoxon p is null if this experiment is tested alone. Direction matches the md-28 pass (13 / 17 / 17 of 30) but this is underpowered, not a confirmation.
- Contrast md-28 on the same density targets (30/30 connected): still the strong slice. Raising md to 48 trades n for a longer floor; it does not reverse who wins on the maps that still connect.

**Decisions from this run.**

1. Braid × size: loops increase ties at **both** 127 and 255. The maze result to keep is **perfect** (unbraided) mazes; larger perfect mazes raise the F2F-fewer rate, braid knocks it back down.
2. Nested 128 @ 45–50% with md 48 is connectivity-limited. Accepting fewer queries is valid descriptively (no F2E-fewer) but does not meet the locked `n_untied ≥ 10` rule. Do not treat the pooled 47-row density tests in this snapshot as an md-48 result.
3. Cache still off. Strongest confirmatory sets remain perfect maze 255 and nested 128 @ 45–50% **with md 28** (full n=30).

---

### 2026-08-14 — Stats/protocol fixes (density grouping, connect-once, repeats)

**Folder:** [`results/analysis/legacy/2026-08-14-density-by-experiment/`](../results/analysis/legacy/2026-08-14-density-by-experiment/)  
**Input:** same experiment subset as [`2026-08-14-maze255-braid-and-128-md48`](../results/analysis/legacy/2026-08-14-maze255-braid-and-128-md48/) (old snapshot kept). No new study CSVs.

**What changed in code (locked methodology revised above).**

1. Nested `obstacle_count` tests are keyed by experiment × size × count; Holm is within one nested config. The previous snapshot’s density headline pooled md-28 (n=30) with md-48 (n=17) at the same prefix counts.
2. `ensure_connected_query` tries every free component (current first if already connected, then largest-first), not only the largest blob. Existing CSVs were **not** re-sampled; the 13/30 md-48 skips still reflect largest-only connect-once.
3. `runtime_repeats`: median times over successful repeats; TIMEOUT only if all repeats time out. Published `study_maze_127_timed` had 0 timeouts, so those numbers are unchanged.

**Headline after unpooling.** Maze 127/255 ± braid counts are unchanged. Nested 128 @ 45–50% **md 28** (30 families) still has `n_untied ≥ 10` at all three densities. Nested 128 **md 48** (17 families) stays `n_untied` 6–8 at every density → p null. That is the md-48 result; do not read a pooled n=47 test. The overall nested-random row in that README still stacks md-28 + md-48 families — do not cite its p-value.

Display/CLI leftovers from the same review (no new study CSVs, no new analysis slug): `map_family=random` Wilcoxon runs when the bucket is independent-only; table F2F-fewer counts follow `n_test`; `--out-dir` refuses the analysis index and a non-empty slug unless `--force`; maze YAML `obstacle_density` is rejected. Leftover `results/analysis/paired.csv` at the index root was removed. Read density from [`2026-08-14-density-by-experiment`](../results/analysis/legacy/2026-08-14-density-by-experiment/).

---

### 2026-08-17 — F2E audit (before pair-bound switch)

**Old official formula** (`F2EFixedEndpointHeuristic`, renamed `LegacyFixedEndpointGapHeuristic`):

```
h_gap(x,y) = max(|MD(x,G)−MD(y,G)|, |MD(S,x)−MD(S,y)|)
f = g_F + g_B + h_gap
```

`PairHeuristic.evaluate` and both SFBDS call sites (`sfbds.py` root insert and child insert) passed only `(forward, backward, problem)` — no `g`. Runner wired `sfbds_f2e` to that class. Numeric locks: `test_f2e_hand_formula`; Lipschitz / gap≤MD in `test_heuristic_properties.py`. Those properties belong to the gap, not to the pair lower bound.

**Decision.** Treat all existing `results/study/` F2E rows as legacy gap. Switch official `sfbds_f2e` to the NBS-style pair lower bound with a remaining-cost adapter. Do not overwrite study CSVs in this pass.

---

### 2026-08-17 — Official SFBDS-F2E is the pair lower bound

Code: `F2EPairLowerBound.lower_bound` is the source of truth; `evaluate` returns `max(0, lb − gsum)` so `SFBDSNode.f` is unchanged. Both SFBDS `evaluate` call sites pass `g_F`/`g_B`. Runner `sfbds_f2e` uses the new class. Spy test on the 1×4 Forward-tie corridor locks the first child to `(g_F, g_B) == (1.0, 0.0)` so swapped kwargs cannot stay green. Pytest: 161 passed.

**New-stem pilots** (old `pilot_*` filenames not overwritten): `pilot_corridor_lb_f2e`, `pilot_open_lb_f2e`, `pilot_maze_lb_f2e`, `pilot_random_lb_f2e`. All 9/9 success, 0 timeouts. A* / F2F / F2E **costs agree** on every query. Corridor/open/maze expansions tied F2F vs F2E on these small maps; random q=0 was 29 vs 35 pairs (F2F fewer). Study CSVs still legacy — regenerate only after approval.

---

### 2026-08-17 — Split legacy vs pair-bound result folders

Moved frozen gap-F2E artifacts so they cannot mix with official pair-bound output. Analysis `--input-dir` is non-recursive.

| Tree | Legacy (gap) | New (pair bound) |
| --- | --- | --- |
| Study CSVs | `results/study/legacy/` | `results/study/pair-bound/` |
| Pilots | `results/pilot/legacy/` | `results/pilot/pair-bound/` |
| Analysis | `results/analysis/legacy/<slug>/` | `results/analysis/pair-bound/<slug>/` |

Study / follow-up / pilot YAML `output_dir` now points at the pair-bound folders. Do not write new runs into `legacy/`. Do not pass `--input-dir results/study` (parent).

---

### 2026-08-17 — Pair-bound baseline study (64 / 128 matrix)

**Folder:** [`results/analysis/pair-bound/2026-08-17-baseline-study/`](../results/analysis/pair-bound/2026-08-17-baseline-study/)  
**Log:** [`results/analysis/pair-bound/research_log.md`](../results/analysis/pair-bound/research_log.md)  
**Input:** `configs/study/` → `results/study/pair-bound/` (`study_corridor_512`, `study_maze_127`, `study_open_128`, `study_random_64`, `study_random_128`). 810/810 success, 0 timeouts.

**What we asked.** Same question as the 2026-08-14 baseline, with official pair-bound F2E instead of the gap.

**Headline (see generated README for tables).**

- **270** paired instances, all solved, **0** timeouts. (Legacy baseline was 540 because it also loaded leftover smaller/independent CSVs.)
- **Open and corridor:** all ties.
- **Maze 127:** 22/30 F2F-fewer (0 F2E-fewer), Holm p ≈ 4.8e-07, rank-biserial 1.00. Costs agree with A*. Legacy gap on this config was 21/30.
- **Nested random:** the published 64×64 @ ~30% row in this snapshot (13 F2F-fewer, Holm p ≈ 0.0002) **includes 4 cost-mismatch maps**. Do not cite that p-value. See the cost-clean re-analysis below.
- **12 cost mismatches** on nested random: F2E cost above A* and F2F. Maze/open/corridor are clean.

**Decisions.** Maze expansion result is still the claim to keep, and it is cost-clean. Do not cite nested-random p-values from this snapshot. Do not cite legacy analysis READMEs as pair-bound results.

---

### 2026-08-17 — Cost-clean expansion tests and F2E mismatch diagnosis

**Folder:** [`results/analysis/pair-bound/2026-08-17-cost-clean-tests/`](../results/analysis/pair-bound/2026-08-17-cost-clean-tests/)  
**Input:** same `results/study/pair-bound/` CSVs (stats-code fix; old snapshot kept).

**What changed.** `cost_mismatch` is F2F / F2E / successful A* disagreement. Those rows stay in `paired.csv` but are dropped from Wilcoxon, sign, and F2F-fewer counts.

**Headline.**

- **Maze 127 unchanged:** 22/30 F2F-fewer, Holm p ≈ 4.8e-07, 0 mismatches.
- **Nested 64 @ 30% cost-clean:** `n_untied = 9` (was 13). p is **null**. 9 F2F-fewer among the cost-clean maps; do not treat this as a confirmatory density test.
- No nested-density group now has `n_untied ≥ 10`.
- Generated README skip sentence for pooled random is “collapses nested densities,” not a false independent-file mix.

**Diagnosis (study_random_64 q=20, 1228 obstacles, hash `d604ed0b69115ce9`).** A* and F2F cost 53; F2E cost 57 (450 vs 2881 pairs). F2E discarded **230** better-`g` CLOSED pairs. That sentence was the **hypothesis at the time**; the 2026-08-17 q=20 optimality-diagnosis entry demonstrated it. A strict xfail locked F2E=A* on this map until reopen landed.

**Decisions.** Keep maze. Do not cite nested-random expansion p-values until F2E is solution-optimal vs A* or we pre-register a cost-clean protocol with `n_untied ≥ 10`. Do not cite plots in this folder as mismatch-free.

---

### 2026-08-17 — Cost-clean plots, diagnosis test, and legacy write refuse

**Folder:** [`results/analysis/pair-bound/2026-08-17-cost-clean-plots/`](../results/analysis/pair-bound/2026-08-17-cost-clean-plots/)  
**Input:** same `results/study/pair-bound/` CSVs (plot filter; previous snapshots kept).

**What changed.**

1. Plots use the same cost-clean rows as Wilcoxon (`expansion_test_rows`). Cite this folder’s figures, not `2026-08-17-cost-clean-tests`.
2. Diagnosis test no longer asserts F2E cost 57; the strict xfail remains the optimality lock. A* cost 53, F2F matches A*, fingerprint, and better-`g` discard count stay.
3. Runner / `load_config` refuse `output_dir` under `results/*/legacy/`. Old-stem pilots live in `configs/pilot/retired/` and are not picked up by `--config-dir configs/pilot`.

**Headline.** Tables unchanged: maze 22/30; nested 64@30% `n_untied=9` → p null.

---

### 2026-08-17 — F2E optimality diagnosis (q=20); fix not started

**Instance:** `study_random_64` query 20, 1228 obstacles, hash `d604ed0b69115ce9`. A* 53, F2F 53 (450 pairs), F2E 57 (2881 pairs). Same Late-goal cell `(57,51)`; F2F `g_F+g_B = 41+12`, F2E `45+12`.

**Demonstrated (not assumed).**

- F2E never generated a meeting pair at g=53. The only meeting generated was `(m,m)` at g=57 (UNSEEN, PUSH), then Late-selected.
- F2F generated a meeting only at g=53. Same `NoReopenPolicy`: F2F had **0** CLOSED better-`g` discards; F2E had **230** (none of them meetings).
- Four of those 230 sit on F2F’s ancestor pair-keys (all with backward already at `m`). On `(47,35),(57,51)` F2E CLOSED at g=29 then discarded g=27, which **equals F2F’s g** on that key.
- Parent→child Lipschitz `h(n) ≤ c + h(n')` had **0** violations on every generated F2E (and F2F) edge, including the meeting step. The `lower_bound` formula (meeting `lb=gsum`, else `max(f_F,f_B,gsum+1)`) is not the demonstrated bug. Adapter `h_gap` **depends on `g_F`/`g_B`**, so the duplicate key `(u,v)` is not a consistent A* node: first select can freeze a suboptimal `g`.
- The “missing” F2F ancestor key is the root `(S,G)` (never a generated child).

**Root cause.** Path-dependent remaining-cost `h_gap` + NoReopen on pair keys: F2E expands/closes optimal-chain pairs at inflated `g_F`, then discards later better `g` (including F2F’s `g`). It never reaches `(m,m)` at `C*`.

**Smallest proposed correction (approved later the same day; see the reopen-gate entry).** Reopen on strictly better CLOSED `g`: remove the CLOSED key and push the candidate. **Forbidden:** meeting `lb=gsum+1`. **Not preferred:** `h_gap=1` off meeting. Pathmax on the current path does not resurrect a better branch after CLOSE.

**Do not treat this entry as a proof.** “Why reopen preserves optimality” was a hypothesis. Standard graph-search reopen is not a Late-stop proof. F2F (`h=MD(u,v)`) stays NoReopen.

**Do not implement** (status at this entry). No new studies yet.

---

### 2026-08-17 — F2E better-g reopen (Option C empirical gate)

**What changed.** Official F2E uses `f2e_policies()`: `BetterGReopenPolicy` + `ClosedSet.remove` + searcher remove-then-push. `default_policies()` / F2F stay `NoReopenPolicy`. Meeting lower bound unchanged (`u=v` ⇒ `lb = gsum`, `h_gap = 0`). Late-on-first-meeting unchanged. Pre-fix pair-bound CSVs kept.

**Demonstrated (q=20 tracer, NoReopen replay).** F2F CLOSED better-`g` discards = 0. F2E CLOSED `((47,35),(57,51))` at g=29 then discarded g=27, which equals F2F’s `g` on that key. F2E generated no `(x,x)` at g=53.

**Hypothesized repair.** Reopen that better-`g` pair (and others) so the optimal chain can be expanded. q=20 under reopen must expand g=27 on that key.

**Not proven.** Reopen is the hypothesized repair for the demonstrated duplicate-key failure. It is empirically accepted only if all 12 frozen mismatches match A*. This is not yet a general proof of optimality.

**Gate (passed).** Frozen identities from pre-fix `results/study/pair-bound/` (`experiment`, `query_index`, `obstacle_count`, `map_hash`), not 12 query indexes. All 12 match A*. q=20 under reopen: F2E=A*=53; g=27 on `((47,35),(57,51))` is reopened and expanded; meeting `h_gap` stays 0. Pre-fix pair-bound CSVs kept. No `*_opt` studies in this pass.

---

### 2026-08-17 — Official F2E factory and citation lock

**What changed.** Runner and tests construct official F2E via `official_f2e_searcher()` (bound + `f2e_policies()`). Bare `SFBDSSearcher(F2EPairLowerBound())` stays NoReopen on purpose. Failed REOPEN push restores the CLOSED node and raises. `docs/project_definition.md` reopen row matches the F2E exception.

**Cite.** On-disk `results/study/pair-bound/study_*.csv` (no `_opt`) remain NoReopen pair-bound F2E. Maze figures: `2026-08-17-cost-clean-plots` as pre-fix. Do not cite nested-random p-values. Do not cite those CSVs as reopen F2E.

---

### 2026-08-17 — Reopen F2E official baselines (`*_opt`)

**Folder:** [`results/analysis/pair-bound/2026-08-17-reopen-opt/`](../results/analysis/pair-bound/2026-08-17-reopen-opt/)  
**Input:** `study_*_opt` CSVs in `results/study/pair-bound/` (same seeds/queries as the pre-fix stems). Analysis used `--experiment` for all five `_opt` names. Pre-fix CSVs kept (q=20 still F2E=57 on `study_random_64`).

```bash
python -m sfbds_compare.analysis --input-dir results/study/pair-bound --out-dir results/analysis/pair-bound/2026-08-17-reopen-opt --experiment study_corridor_512_opt --experiment study_maze_127_opt --experiment study_open_128_opt --experiment study_random_64_opt --experiment study_random_128_opt
```

**What we asked.** With official reopen F2E, on the same 64/128 matrix, does F2F still expand fewer pairs, and do costs match A*?

**Headline.**

- **270** paired, **270** solved, **0** timeouts, **0** cost mismatches (the 12 pre-fix mismatches are gone on these maps).
- **Maze 127:** 22/30 F2F-fewer, Holm p ≈ 4.77e-07, median saving 3.8%. Same win count as pre-fix cost-clean; cite this folder for reopen F2E.
- **Open / corridor:** still all ties.
- **Nested 64 @ ~30%:** 13/30 F2F-fewer, 0 F2E-fewer, Holm p ≈ 0.0002, `n_untied ≥ 10`, cost-clean. Pre-fix cost-clean had `n_untied = 9` (p null) because mismatches were dropped. Do not cite the first pair-bound snapshot’s nested p-value.
- Other nested density rows still have too many ties (`n_untied < 10` → p null). Overall nested-random Wilcoxon stays skipped (two experiments).

**Decisions.** Maze remains the regime where F2F separates on expansions. Nested 64@30% is now a cost-clean density test with `n_untied ≥ 10` under reopen F2E. Late-stop is still Option C (empirical), not a general proof.

---

### 2026-08-17 — Analysis README command and official `_opt` set

Generated analysis READMEs now emit the `--experiment` flags actually used. The CLI refuses a partial official `*_opt` set unless `--allow-opt-subset`. Regenerated [`2026-08-17-reopen-opt/README.md`](../results/analysis/pair-bound/2026-08-17-reopen-opt/README.md) with `--force` (same slug; tables unchanged).

Follow-ups (maze 255 / denser random): keep the `_opt` suffix and pass `--experiment` (plus `--allow-opt-subset` if not the five-stem baseline), or use a new stem with an explicit `--experiment` list. `study_*_opt2` is not a third formula.

---

## Next experiment (not started)

Cache stays off. Pair-bound living notes: [`results/analysis/pair-bound/research_log.md`](../results/analysis/pair-bound/research_log.md).

1. **Maze 255 / denser nested random** under reopen F2E (`*_opt` or new follow-up stems), into `results/study/pair-bound/` without deleting existing CSVs. Analyze with `--experiment` (and `--allow-opt-subset` if not the five official `_opt` stems).
2. **Cache ablation** only after instructor/scope lock.
3. Option A Late-stop proof or Option B incumbent stop only after separate approval.
