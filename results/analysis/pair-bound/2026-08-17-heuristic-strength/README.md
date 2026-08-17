# Heuristic-strength analysis (F2F vs official pair-bound F2E)

Mechanism check, not a co-primary expansion result. Cite pair-expansion counts from [`2026-08-17-reopen-opt`](../2026-08-17-reopen-opt/) (maze 127, nested 64@30%), [`2026-08-17-harder-opt`](../2026-08-17-harder-opt/) (maze 255, nested 64@45%), and [`2026-08-17-far-braid-by-experiment`](../2026-08-17-far-braid-by-experiment/) (maze 127 braid). Replay matched those frozen `expanded` / `heuristic_evals` / `solution_cost` / `map_hash` values.

Reproducible via `python scripts/heuristic_strength.py --force`. Search policies and heuristic formulas were not changed.

## Methodology

Existing `*_opt` CSVs do not store `(u,v,g_F,g_B)`. This snapshot **replays** official F2F (`SFBDSSearcher(F2FManhattanHeuristic())`, NoReopen) and official F2E (`F2EPairLowerBound` + `f2e_policies()` / reopen) on the same YAML seeds. A* was not rerun. Study CSVs were not overwritten.

**Population.** Every pair on which SFBDS calls `evaluate` (insert/improve OPEN; same events as `heuristic_evals`). Not a random grid sample, and not “pairs both algorithms expanded.”

For each recorded `(u, v, g_F, g_B)` from **either** search, both lower bounds are computed:

```text
LB_F2F = g_F + g_B + MD(u, v)
LB_F2E = gsum                         if u == v
       = max(f_F(u), f_B(v), gsum+1)  otherwise
diff   = LB_F2F − LB_F2E
```

That is the same pair-state under both formulas. Rows are tagged `source ∈ {f2f, f2e}`. Pooled numbers mix those sources and **must not** be read as a shared expansion set. `(u,v)` key intersection is not the primary comparison (`g` often differs).

`pair_sample.csv` is a reservoir sample (~200 pairs per family × source), not the full evaluate() stream.

On feasible tree `g` (`g_F ≥ MD(S,u)`, `g_B ≥ MD(v,G)`), `LB_F2F ≥ LB_F2E` algebraically on unit grids. The question is the **size** of `diff` and whether it tracks expansion savings.

## Datasets

Official reopen `*_opt` only. 30 queries each. Replay matched frozen `map_hash`, `expanded`, `heuristic_evals`, and `solution_cost`.

| Family | Frozen CSV | Filter | Seed |
| --- | --- | --- | --- |
| Open 128 | `study_open_128_opt` | none | 100 |
| Maze 127 | `study_maze_127_opt` | none | 140 |
| Maze 255 | `study_maze_255_opt` | none | 150 |
| Maze 127 braid 0.5 | `study_maze_127_braid_opt` | none | 140 (same endpoints as maze 127) |
| Nested 64 @ 30% | `study_random_64_opt` | 1228 obstacles | **110** |
| Nested 64 @ 45% | `study_random_64_dense_opt` | 1842 obstacles | **210** |

**Seeds differ.** Nested 64@30% and 64@45% are a **family-level contrast**, not a paired density progression on identical maps. Do not write that raising density from 30% to 45% on the same instances did anything.

## Result

**F2E’s bound was never strictly stronger** on any recorded evaluate() pair (`pooled_frac_f2e_stronger = 0` on all six families). Open 128 is 100% equal. Mazes are where F2F’s bound is often strictly stronger.

| Family | Exp. F2F-fewer / F2E-fewer / tie | Median of per-query median `diff` | Pooled % F2F-stronger / equal | Spearman on **untied** queries (median `diff` vs expansion_diff) |
| --- | ---: | ---: | ---: | ---: |
| Open 128 | 0 / 0 / 30 | 0 | 0 / 100 | n/a (0 untied) |
| Maze 127 | 22 / 0 / 8 | 18.25 | 67.5 / 32.5 | 0.21 (n=22) |
| Maze 255 | 26 / 0 / 4 | 123.5 | 89.6 / 10.4 | 0.13 (n=26) |
| Maze 127 braid | 12 / 0 / 18 | 0 | 27.0 / 73.0 | 0.63 (n=12) |
| Nested 64 @ 30% | 13 / 0 / 17 | 0 | 59.3 / 40.7 | 0.86 (n=13) |
| Nested 64 @ 45% | 14 / 1 / 15 | 0 | 56.1 / 43.9 | 0.38 (n=15) |

Spearman is **expansion-untied queries only**. All-query Spearman is dominated by the tie cluster at `(median_diff=0, expansion_diff=0)` and is not a ranking of how much F2F saves. Maze 255’s 0.13 is the honest “does bound gap rank savings?” number (almost every query already has a large positive `diff`). Spearman of F2F-stronger **fraction** vs expansion_diff among untied queries is similar (maze 127 0.23, maze 255 0.12, nested 30% 0.81, nested 45% 0.41).

Expansion-tied maze 127 queries have **median `diff` = 0 and 0% F2F-stronger** (all eight). Queries where F2F expanded fewer have median `diff` ≈ 49 (maze 127) and ≈ 126 (maze 255). Braid winning queries only reach median `diff` ≈ 2.

Source-tagged (not pooled): on nested maps, F2E’s own evaluate() stream is where F2F’s bound is more often strictly stronger (64@30%: 71% of F2E-search pairs vs 30% of F2F-search pairs). F2E is visiting pair-states on which F2F would have posted a larger `f`. Maze 127/255 look similar across sources (~67–90% F2F-stronger either way).

## Hypothesis check

- **Open:** bounds equal → expansion ties. Supported.
- **Perfect maze:** F2F often stronger bound → fewer expansions. Supported in direction and in the tied-vs-untied split. Maze 255 has both a larger bound gap and a higher F2F-fewer count than maze 127.
- **Braid:** loops shrink F2F’s bound advantage → more expansion ties. Supported (27% F2F-stronger vs 68% on perfect maze 127; win count 12/30 vs 22/30).
- **Dense random:** F2F advantage only when obstacles make endpoint F2E less informative. **Only weakly supported as a 30% vs 45% story.** Both families have similar pooled F2F-stronger shares (59% vs 56%) and similar win counts (13 vs 14). They are different seeds; this is not a within-map density effect. Nested *does* show F2F-stronger bounds on a majority of F2E-search pairs, which is consistent with endpoint Manhattan being uninformative on some blocked queries.

## Counterexamples

- Nested 64@45% **query 8**: expansion_diff = **−1** (the single F2E-fewer map) but median `diff` = **+4** and 74% of evaluate() pairs have a strictly stronger F2F bound. Bound advantage did **not** produce an F2F expansion win here.
- Nested expansion savings can be huge (thousands of pairs) while the per-query median `diff` is only 2. Bound strength helps explain *whether* the searches separate, not the size of the expansion gap (reopen / tree shape still matter).
- Spearman among maze 255’s 26 untied queries is only 0.13: almost every query has a large F2F bound advantage, so bound `diff` does not rank expansion savings.

## Verdict

**Partially explains** the main expansion result.

F2F’s pair bound is everywhere at least as strong as official F2E’s on these evaluate() states, and it is *strictly* stronger on most maze pairs and on a large share of F2E’s nested-random pairs. That lines up with maze wins, open ties, and braid shrinking both the bound gap and the win count. It does **not** fully determine expansions: the 64@45% F2E-fewer query still had a stronger F2F bound, and nested expansion magnitudes dwarf the typical median `diff`.

## How to cite

Mechanism / appendix. Do not replace the expansion-geography claim with “F2F wins because the bound is stronger” as a complete explanation.

Figures: [`bound_strength_share.png`](bound_strength_share.png), [`bound_vs_expansion.png`](bound_vs_expansion.png). Tables: [`family_summary.csv`](family_summary.csv), [`query_summary.csv`](query_summary.csv).
