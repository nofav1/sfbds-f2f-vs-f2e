# Internal source map (not compiled)

This file is **not** part of the report PDF. It records what later phases may cite, and what must never appear in compiled `.tex`.

**EXCLUDED FROM FINAL REPORT — never use as evidence** (paths and claims below).

Citation spec for compiled files: [`docs/context/final_report_papers/PAPER_SOURCE_MAP.md`](../../../context/final_report_papers/PAPER_SOURCE_MAP.md).

---

## PRIMARY (paper evidence)

- Course contract: `docs/context/Project_Instructions_context.md`
- Locked science: `docs/research_log.md`, `results/analysis/pair-bound/research_log.md`, `results/analysis/README.md` — numbers from official snapshots; do not copy historical-era sentences into the paper
- Implementation: `official_f2e_searcher`, `F2EPairLowerBound`, `F2FManhattanHeuristic`, policies, A*, generators, metrics
- Official configs: `configs/study/study_*_opt.yaml`; live `configs/followup/study_*_opt.yaml`
- Official CSVs: `results/study/pair-bound/*_opt.csv` only
- Citable snapshot READMEs:
  - `results/analysis/pair-bound/2026-08-17-reopen-opt/`
  - `results/analysis/pair-bound/2026-08-17-harder-opt/`
  - `results/analysis/pair-bound/2026-08-17-far-braid-by-experiment/`
- Secondary snapshots: `2026-08-17-heuristic-strength/`, `2026-08-17-eval-cost-sensitivity/`
- Committed heuristic-strength tables: `query_summary.csv`, `family_summary.csv`
- Verified papers: `docs/context/final_report_papers/` (map is the only citation spec)

Paper figures (Phase 5): rebuild from git `*_opt.csv` + `family_summary.csv` via `scripts/paper_figures.py` into `figures/`. Do not require gitignored analysis `paired.csv`.

---

## SECONDARY (supporting, not citation authority)

- Literature Markdown notes under `docs/context/sfbds_literature_context_md/` — navigation only
- Lecture summaries under `docs/context/presentations_summary/` — methodology language only; not bibliography
- `docs/project_definition.md` — topic map; Idea B cache was **not** implemented
- Analysis PNGs under `results/analysis/` — gitignored; not figure inputs

---

## EXCLUDED FROM FINAL REPORT — never use as evidence

- `results/study/legacy/`, `results/analysis/legacy/`, `results/pilot/legacy/`
- `LegacyFixedEndpointGapHeuristic` and all gap-F2E numbers/figures
- Pair-bound CSVs **without** `_opt` (NoReopen)
- Snapshots: `2026-08-17-baseline-study`, `cost-clean-tests`, `cost-clean-plots`
- `2026-08-17-far-braid-opt` pooled README (use `far-braid-by-experiment`)
- Non-`_opt` follow-up YAMLs / `configs/followup/retired/`
- Pooled nested-random / pooled maze-across-experiments
- All-query Spearman, and nested 64@30% Spearman **0.86 (n=13)** as a savings ranking
- “F2F is faster” as a general claim
- Bug-fix / two-era / 12-mismatch narrative
- Felner 2010 as a cache citation; Lippi 2012; Barker dissertation; Siag AIJ 2025; Shubi 2026; Zou 2026 F2A; Pohl 1969
- Hart 1968 numbered theorems (bib-only; no local PDF)
- Chen 2017 “NBS +1”; `siag2023socs` next to SFBDS

Allowed `\cite` keys: `hart1968astar`, `felner2010sfbds`, `barker2015f2e`, `chen2017nbs`, `siag2023socs`, `siag2023ijcai`.
