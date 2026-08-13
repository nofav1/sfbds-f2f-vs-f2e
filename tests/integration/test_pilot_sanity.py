"""Pilot matrix sanity: cost agreement and finite metrics across map families."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pytest

from sfbds_compare.domain.grid import GridState
from sfbds_compare.experiments.config import load_config
from sfbds_compare.experiments.runner import export_records, run_experiment
from sfbds_compare.heuristics.grid_distance import manhattan

_PILOT_DIR = Path(__file__).resolve().parents[2] / "configs" / "pilot"


def _pilot_configs() -> list[Path]:
    return sorted(_PILOT_DIR.glob("pilot_*.yaml"))


@pytest.mark.parametrize("config_path", _pilot_configs(), ids=lambda p: p.stem)
def test_pilot_config_cost_agreement_and_metrics(
    config_path: Path, tmp_path: Path
) -> None:
    cfg = load_config(config_path)
    # Redirect artifacts away from the real results/ tree during tests.
    cfg = type(cfg)(
        name=cfg.name,
        algorithms=cfg.algorithms,
        seed=cfg.seed,
        generator=cfg.generator,
        queries=cfg.queries,
        output_dir=str(tmp_path),
        timeout_sec=cfg.timeout_sec,
    )

    records = run_experiment(cfg)
    assert records, f"no records for {config_path.name}"
    assert len(records) == len(cfg.queries) * len(cfg.algorithms)

    by_query: dict[int, list] = defaultdict(list)
    for rec in records:
        by_query[rec.query_index].append(rec)
        assert not rec.timed_out, f"unexpected timeout in {config_path.name}"
        assert rec.runtime_sec >= 0.0
        assert rec.expanded >= 0
        assert rec.generated >= 0
        assert rec.peak_open >= 0
        assert rec.peak_closed >= 0
        assert rec.map_hash
        assert rec.generator_kind == cfg.generator.kind
        assert rec.expanded_unit in ("state", "pair")
        if cfg.generator.kind == "maze":
            assert rec.obstacle_count > 0
            n_cells = rec.height * rec.width
            assert rec.obstacle_density == rec.obstacle_count / n_cells
            assert rec.obstacle_density != 0.0

    for q_idx, group in by_query.items():
        assert len(group) == len(cfg.algorithms)
        assert len({r.map_hash for r in group}) == 1
        successes = [r for r in group if r.success]
        failures = [r for r in group if not r.success]
        # All solvers must agree on success/failure for the same instance.
        assert len(successes) in (0, len(group)), (
            f"mixed success on query {q_idx} in {config_path.name}: "
            f"{[(r.algorithm, r.termination_reason) for r in group]}"
        )
        if successes:
            costs = {r.solution_cost for r in successes}
            assert len(costs) == 1, (
                f"cost mismatch on query {q_idx} in {config_path.name}: {costs}"
            )
            assert next(iter(costs)) is not None
            assert next(iter(costs)) >= 0.0
        else:
            assert all(
                r.termination_reason == "open_exhausted" for r in failures
            )

    if cfg.generator.kind == "maze":
        detoured = False
        for group in by_query.values():
            ok = [r for r in group if r.success and r.solution_cost is not None]
            if not ok:
                continue
            r0 = ok[0]
            md = manhattan(
                GridState(r0.start_row, r0.start_col),
                GridState(r0.goal_row, r0.goal_col),
            )
            if r0.solution_cost > md:
                detoured = True
                break
        assert detoured, "maze pilot should force a detour on some query"

    csv_path, json_path = export_records(cfg, records)
    assert csv_path.is_file() and json_path.is_file()
