"""Integration smoke for experiment runner + timeout wrapper."""

from __future__ import annotations

import time
from pathlib import Path

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import (
    ExperimentConfig,
    GeneratorConfig,
    QuerySpec,
)
from sfbds_compare.experiments.export import write_csv
from sfbds_compare.experiments.generators import build_problem, map_fingerprint
from sfbds_compare.experiments.runner import (
    export_records,
    run_experiment,
    run_query,
)
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import TerminationReason


def test_smoke_astar_corridor_exports(tmp_path: Path) -> None:
    cfg = ExperimentConfig(
        name="smoke_test",
        algorithms=("astar",),
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
    assert records[0].generator_kind == "corridor"
    assert records[0].map_hash
    csv_path, json_path = export_records(cfg, records)
    assert csv_path.is_file()
    assert json_path.is_file()
    text = csv_path.read_text(encoding="utf-8")
    assert "solution_cost" in text
    assert "map_hash" in text


def test_smoke_sfbds_f2f_and_f2e_corridor() -> None:
    for algo in ("sfbds_f2f", "sfbds_f2e"):
        cfg = ExperimentConfig(
            name=f"smoke_{algo}",
            algorithms=(algo,),
            seed=1,
            generator=GeneratorConfig(kind="corridor", height=1, width=4),
            queries=(QuerySpec(start=(0, 0), goal=(0, 3)),),
            output_dir="results",
            timeout_sec=5.0,
        )
        records = run_experiment(cfg)
        assert records[0].success
        assert records[0].solution_cost == 3.0


def test_multi_algo_same_instance_cost_agreement() -> None:
    cfg = ExperimentConfig(
        name="compare",
        algorithms=("astar", "sfbds_f2f", "sfbds_f2e"),
        seed=2,
        generator=GeneratorConfig(kind="open", height=5, width=5),
        queries=(QuerySpec(start=(0, 0), goal=(4, 3)),),
        output_dir="results",
        timeout_sec=5.0,
    )
    records = run_experiment(cfg)
    assert len(records) == 3
    assert len({r.map_hash for r in records}) == 1
    costs = {r.solution_cost for r in records}
    assert costs == {7.0}
    assert all(r.success for r in records)


def test_timeout_wall_clock_bound() -> None:
    """Cooperative stop must return well before a long search body finishes."""

    from sfbds_compare.metrics.collector import MetricsCollector
    from sfbds_compare.search.result import SearchResult

    problem = GridProblem(2, 2, GridState(0, 0), GridState(0, 1))

    def slow_impl(_problem: GridProblem, should_stop):
        steps = 0
        while steps < 200:
            if should_stop():
                metrics = MetricsCollector()
                metrics.start()
                metrics.expanded = max(steps, 1)
                metrics.timed_out = True
                return SearchResult(
                    success=False,
                    termination_reason=TerminationReason.TIMEOUT,
                    metrics=metrics.finish(success=False),
                )
            time.sleep(0.05)
            steps += 1
        raise AssertionError("should have been stopped")

    t0 = time.perf_counter()
    result = run_query(
        problem, "astar", timeout_sec=0.12, search_impl=slow_impl
    )
    elapsed = time.perf_counter() - t0
    assert result.termination_reason is TerminationReason.TIMEOUT
    assert result.metrics.timed_out is True
    assert result.metrics.expanded >= 1
    assert elapsed < 1.0


def test_timeout_cooperative_preserves_metrics() -> None:
    problem = GridProblem(2, 2, GridState(0, 0), GridState(1, 1))

    def slow_impl(_problem: GridProblem, should_stop):
        from sfbds_compare.metrics.collector import MetricsCollector
        from sfbds_compare.search.result import SearchResult

        steps = 0
        while True:
            if should_stop():
                metrics = MetricsCollector()
                metrics.start()
                metrics.expanded = max(steps, 1)
                metrics.generated = steps * 2
                metrics.timed_out = True
                return SearchResult(
                    success=False,
                    termination_reason=TerminationReason.TIMEOUT,
                    metrics=metrics.finish(success=False),
                )
            time.sleep(0.05)
            steps += 1

    result = run_query(
        problem, "astar", timeout_sec=0.1, search_impl=slow_impl
    )
    assert result.termination_reason is TerminationReason.TIMEOUT
    assert result.metrics.expanded >= 1
    assert result.metrics.generated >= 1


def test_random_obstacles_reproducible_hash() -> None:
    gen = GeneratorConfig(
        kind="random_obstacles", height=8, width=8, obstacle_density=0.2
    )
    query = QuerySpec(start=(0, 0), goal=(7, 7))
    a = build_problem(gen, query, seed=42)
    b = build_problem(gen, query, seed=42)
    assert set(a.obstacles) == set(b.obstacles)
    assert map_fingerprint(a, generator=gen, seed=42) == map_fingerprint(
        b, generator=gen, seed=42
    )


def test_maze_solvable() -> None:
    gen = GeneratorConfig(kind="maze", height=11, width=11)
    query = QuerySpec(start=(0, 0), goal=(10, 10))
    problem = build_problem(gen, query, seed=3)
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success


def test_cli_writes_artifacts(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main

    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(
        "\n".join(
            [
                "name: cli_smoke",
                "algorithm: astar",
                "seed: 1",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: corridor",
                "  height: 1",
                "  width: 4",
                "queries:",
                "  - start: [0, 0]",
                "    goal: [0, 3]",
            ]
        ),
        encoding="utf-8",
    )
    assert main(["--config", str(cfg_path)]) == 0
    assert (tmp_path / "cli_smoke.csv").is_file()
    assert (tmp_path / "cli_smoke.json").is_file()


def test_write_csv_empty(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    write_csv(path, [])
    assert path.read_text(encoding="utf-8") == ""
