# Pair-bound study CSVs

Official `sfbds_f2e` (`F2EPairLowerBound`). Study and follow-up YAML `output_dir` points here.

- Stems **without** `_opt` (`study_maze_127.csv`, …) are **NoReopen** pair-bound F2E (pre-fix). Do not overwrite them.
- Stems **with** `_opt` are reopen F2E (`official_f2e_searcher()`). The five official baselines must be analyzed together (not mixed with follow-up `*_opt`). Follow-up `_opt` stems need `--experiment` and `--allow-opt-subset`. Live follow-up YAMLs: `configs/followup/study_*_opt.yaml`. Non-`_opt` follow-ups are in [`../../configs/followup/retired/`](../../configs/followup/retired/).

Legacy gap CSVs stay in [`../legacy/`](../legacy/). Do not copy them into this folder.
