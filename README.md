# sfbds-compare

Controlled comparison of SFBDS with F2F vs F2E heuristics on 4-connected grids.

## Setup

```bash
pip install -e ".[dev]"
pytest
```

Implementation proceeds phase by phase; see the project plan for scope and locked methodology.

## Analysis

Each analysis pass writes a **new folder**. Do not overwrite a previous run.

```bash
python -m sfbds_compare.analysis --input-dir results/study --out-dir results/analysis/YYYY-MM-DD-short-slug
```

Follow-up configs live under `configs/followup/`. Select a subset of CSVs with repeated `--experiment NAME`.

That writes a generated `README.md` plus `paired.csv`, `summary.csv`, `stats.csv`, and plots inside that folder. Re-run after new study CSVs into a **new** slug; do not edit a generated analysis README by hand.

Research progress and locked decisions live in [`docs/research_log.md`](docs/research_log.md). The list of analysis folders is [`results/analysis/README.md`](results/analysis/README.md).
