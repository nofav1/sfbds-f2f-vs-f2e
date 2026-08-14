# Research log

Living document for **what we ran, what we locked, what we concluded, and what to try next**. Update it when a decision is locked or an analysis folder is added. Do not paste full tables here — those live in each generated analysis README.

- Analysis snapshots: [`results/analysis/README.md`](../results/analysis/README.md)
- Project definition (scope, Idea A/B): [`project_definition.md`](project_definition.md)
- Locked pairing/stats plan: [`.cursor/plans/paired_analysis_workflow.plan.md`](../.cursor/plans/paired_analysis_workflow.plan.md)

## How we keep results

| Kind | Where | Rule |
| --- | --- | --- |
| Raw study CSVs / JSON | `results/study/` | Keep old files. New configs get new stems. |
| Analysis pass | `results/analysis/YYYY-MM-DD-short-slug/` | **New pass → new folder.** Never overwrite. |
| This log | `docs/research_log.md` | Hand-edited. Record decisions and next questions. |
| Generated tables | `<run>/README.md` | Machine-written. Do not edit by hand. |

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/YYYY-MM-DD-short-slug
```

Follow-up experiments (new maps, densities, query lengths, cache settings) get **new YAML** under `configs/study/` (or a dated `configs/` subfolder), new CSVs, then a **new analysis folder**. Point `--input-dir` at all of `results/study` only if mixing old and new files is intentional.

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
- `ensure_connected_query` **once** on the densest map; reuse relocated S/G at lower densities.
- Skip ASCII visuals when `obstacle_densities` is set.
- Independent `*_d10/d20/d30` CSVs (old non-nested sampling) may still sit in `results/study/`. They pair F2F vs F2E but **must not** enter nested `obstacle_count` tests, `overall_random`, or `saving_by_density.png`.
- Optional YAML `maze_braid` in `[0, 1)` (maze only, default 0): after the perfect spanning tree, open that fraction of leftover inter-room walls. Same seed + queries as a `maze_braid: 0` run share endpoints; the braided map has extra openings.

**Pairing and stats**

- `family_id = experiment:generator_kind:h×w:seed:query_index`; `pair_id = family_id:map_hash`.
- Solved pair = both SFBDS success and not timed out. Timeouts stay in `paired.csv` with null ratios; win % / means / tests use solved only.
- Detour = solution cost / Manhattan, using **A* cost** when A* succeeded.
- Saving % = `(F2E − F2F) / F2E × 100`. Primary test: two-sided Wilcoxon on `expansion_diff`, `zero_method="wilcox"`, exact if `n_untied ≤ 25`, **p = null if `n_untied < 10`**.
- Do **not** stack nested densities as independent n. Wilcoxon for overall nested random = **one median `expansion_diff` per `family_id`**. Per-density tests stay uncollapsed.
- Confirmatory: sign/binomial (F2F-fewer vs F2E-fewer, ties dropped). Holm Wilcoxon and Holm sign in **separate** families. Detour buckets exploratory (raw p only).
- Rank-biserial from **T+/T−**, not scipy’s `statistic`. Positive ⇒ F2F fewer expansions.
- Runtime must not drive the claim.
- Optional YAML `runtime_repeats` (default 1): median `runtime_sec` and `heuristic_time_sec` across repeats; expansions/path from the first successful run. Skip ASCII visuals when repeats > 1, nested densities are set, or the grid is ≥ 200×200.

---

## Timeline

### 2026-08-14 — Baseline grid study (64 / 128)

**Folder:** [`results/analysis/2026-08-14-baseline-study/`](../results/analysis/2026-08-14-baseline-study/)  
**Input:** all CSVs then in `results/study/` (corridor 256/512, maze 63/127, open 64/128, nested random 64/128, plus leftover independent random `*_d10/d20/d30`).

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
- Expansions / density: [`results/analysis/2026-08-14-harder-followup/`](../results/analysis/2026-08-14-harder-followup/)
- Runtime protocol: [`results/analysis/2026-08-14-maze-runtime/`](../results/analysis/2026-08-14-maze-runtime/)

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

**Folder:** [`results/analysis/2026-08-14-far-maze-and-dense-random/`](../results/analysis/2026-08-14-far-maze-and-dense-random/)

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

**Folder:** [`results/analysis/2026-08-14-braid-and-denser-nested/`](../results/analysis/2026-08-14-braid-and-denser-nested/)

**Configs:** [`study_maze_127_braid.yaml`](../configs/followup/study_maze_127_braid.yaml) (`maze_braid: 0.5`, same seed/queries as `study_maze_127`), [`study_random_64_d52.yaml`](../configs/followup/study_random_64_d52.yaml), [`study_random_128_d45.yaml`](../configs/followup/study_random_128_d45.yaml).

**What we asked.** (1) At fixed 127×127 and the same endpoints, does opening 50% of leftover maze walls (braid) change the F2F expansion gap? (2) Nested 128 starting at 45% (drop 30/40%), and 64 just above 50%.

**Headline.** 240 paired rows, all solved, 0 timeouts.

- **Braid:** same 30 start/goal pairs as perfect maze 127. Obstacle count drops ~7936 → ~5952. F2F-fewer **21/30 → 11/30**; ties 9 → 19. No F2E-fewer. Loops made F2F and F2E agree more often, not less.
- **64×64 @ 50/51/52%** needed `min_manhattan` 16 (24 at ≥55% could not connect 30/30). All three densities stay too tied (`n_untied` 7). Going above 50% at 64 did not help.
- **128×128 @ 45/47.5/50%** needed `min_manhattan` 28 (48 at 50–55% could not connect). This is the strong slice: F2F-fewer **13 / 17 / 17** of 30; Holm p ≈ 2e-4 to 5e-5. No F2E-fewer.

**Decisions from this run.**

1. Perfect (unbraided) mazes are where F2F separates; braid toward open-with-loops **increases ties**. Do not expect braid to amplify the maze result.
2. Nested 128 **≥ 45%** (with a shorter Manhattan floor so connect-once succeeds) is the random density regime that actually unties. Tiny 64 steps above 50% are still mostly ties.
3. Connectivity, not timeout, is the limiter past ~50% obstacles at the old `min_manhattan` values.

---

## Next experiment (not started)

Cache stays off until instructor/scope lock. Nothing else is queued until we pick one of:

1. **Nested 128 @ 45–50% with the original `min_manhattan` 48** if we can connect (or accept fewer queries) — this pass lowered md to 28.
2. **Maze 255 braid** — size helped on perfect mazes; braid hurt at 127. Confirm the interaction.
3. **Cache ablation** — only after instructor/scope lock; strongest instance sets so far are perfect maze 255 and nested 128 @ 45–50%.

When we choose, add a YAML under `configs/followup/`, run into `results/study/` without deleting old CSVs, analyze into `results/analysis/YYYY-MM-DD-<slug>/` with `--experiment` filters, and add a row here plus in [`results/analysis/README.md`](../results/analysis/README.md).
