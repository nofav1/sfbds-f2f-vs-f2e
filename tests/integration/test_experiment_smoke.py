"""Integration smoke for experiment runner + timeout wrapper."""

from __future__ import annotations

import time
from pathlib import Path

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import ExperimentConfig, GeneratorConfig, QuerySpec
from sfbds_compare.experiments.export import write_csv
from sfbds_compare.experiments.runner import (
    export_records,
    run_experiment,
    run_query,
)
from sfbds_compare.search.result import TerminationReason


def test_smoke_astar_corridor_exports(tmp_path: Path) -> None:
    cfg = ExperimentConfig(
        name="smoke_test",
        algorithm="astar",
        seed=1,
        generator=GeneratorConfig(kind="corridor", height=1, width=4),
        queries=(QuerySpec(start=(0, 0), goal=(0, 3)),),
        output_dir=str(tmp_path),
        timeout_sec=5.0,
    )
    records = run_experiment(cfg)
    assert len(records) == 1
    assert records[0].success
    assert records[0].solution_cost == 3.0
    csv_path, json_path = export_records(cfg, records)
    assert csv_path.is_file()
    assert json_path.is_file()
    assert "solution_cost" in csv_path.read_text(encoding="utf-8")


def test_smoke_sfbds_f2f_and_f2e_corridor() -> None:
    for algo in ("sfbds_f2f", "sfbds_f2e"):
        cfg = ExperimentConfig(
            name=f"smoke_{algo}",
            algorithm=algo,
            seed=1,
            generator=GeneratorConfig(kind="corridor", height=1, width=4),
            queries=(QuerySpec(start=(0, 0), goal=(0, 3)),),
            output_dir="results",
            timeout_sec=5.0,
        )
        records = run_experiment(cfg)
        assert records[0].success
        assert records[0].solution_cost == 3.0


def test_timeout_with_slow_search_fn() -> None:
    problem = GridProblem(1, 2, GridState(0, 0), GridState(0, 1))

    def slow_search(_problem: SearchProblem[GridState]):
        time.sleep(1.0)
        raise AssertionError("should have timed out")

    result = run_query(problem, slow_search, timeout_sec=0.05)
    assert result.success is False
    assert result.termination_reason is TerminationReason.TIMEOUT
    assert result.metrics.timed_out is True


def test_write_csv_empty(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    write_csv(path, [])
    assert path.read_text(encoding="utf-8") == ""
