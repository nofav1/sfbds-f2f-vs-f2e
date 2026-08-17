# Retired gap-F2E pilot stems

These YAMLs record the frozen `pilot_corridor` / `pilot_open` / `pilot_maze` /
`pilot_random` runs (project-choice gap F2E). They are **not runnable**.

- `output_dir` is `results/pilot/legacy/`
- `load_config` / the runner **refuse** writes under `results/*/legacy/`
- Live pair-bound pilots: `configs/pilot/*_lb_f2e.yaml` → `results/pilot/pair-bound/`

Do not move them back next to the `*_lb_f2e` files (`--config-dir configs/pilot`
would pick them up).
