# Retired non-`_opt` follow-up stems

These YAMLs record the pre-reopen follow-up configs (same seeds/queries as
the matching `*_opt` files, names **without** `_opt`). They are **not
runnable**.

Official `sfbds_f2e` is reopen (`official_f2e_searcher()`). A live YAML named
`study_maze_255` would write `results/study/pair-bound/study_maze_255.csv`
and look like NoReopen to the analysis mix check.

- `load_config` refuses any `configs/followup/` path whose `name` does not
  end with `_opt`
- Live follow-ups: `configs/followup/study_*_opt.yaml` →
  `results/study/pair-bound/`
- Copy from here when adding a new reopen follow-up; give the copy an `_opt`
  name and keep this file retired

Do not move them back next to the `*_opt` files (`--config-dir configs/followup`
would pick them up).
