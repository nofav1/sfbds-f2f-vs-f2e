"""Integration smoke for experiment runner + timeout wrapper."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import (
    ExperimentConfig,
    GeneratorConfig,
    QuerySpec,
    config_from_dict,
)
from sfbds_compare.experiments.export import write_csv
from sfbds_compare.experiments.generators import (
    build_problem,
    endpoints_connected,
    map_fingerprint,
)
from sfbds_compare.experiments.runner import (
    _record_for,
    export_records,
    run_experiment,
    run_experiment_with_frames,
    run_query,
)
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.metrics.collector import MetricsSnapshot
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import SearchResult, TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher


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
    rec = records[0]
    assert rec.forward_expanded is None
    assert rec.backward_expanded is None
    assert rec.meeting_g_F is None
    assert rec.meeting_g_B is None
    assert rec.direction_switches is None
    row = next(csv.DictReader(csv_path.open(encoding="utf-8")))
    assert row["forward_expanded"] == ""
    assert row["backward_expanded"] == ""
    assert row["meeting_g_F"] == ""
    assert row["meeting_g_B"] == ""
    assert row["direction_switches"] == ""
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload[0]["forward_expanded"] is None
    assert payload[0]["meeting_g_F"] is None


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
        rec = records[0]
        assert rec.forward_expanded is not None
        assert rec.backward_expanded is not None
        assert rec.forward_expanded + rec.backward_expanded == rec.expanded
        assert rec.meeting_g_F is not None
        assert rec.meeting_g_B is not None
        assert rec.meeting_g_F + rec.meeting_g_B == rec.solution_cost


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
    assert result.metrics.meeting_g_F is None
    assert result.metrics.meeting_g_B is None


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
    assert result.metrics.meeting_g_F is None
    assert result.metrics.meeting_g_B is None


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


def test_maze_has_walls_and_detours() -> None:
    from sfbds_compare.heuristics.grid_distance import manhattan

    gen = GeneratorConfig(kind="maze", height=11, width=11)
    query = QuerySpec(start=(0, 0), goal=(10, 10))
    problem = build_problem(gen, query, seed=3)
    assert len(problem.obstacles) > 0
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost is not None
    assert result.solution_cost > manhattan(problem.start_state, problem.goal_state)


def test_maze_export_uses_realized_obstacle_density(tmp_path: Path) -> None:
    cfg = ExperimentConfig(
        name="maze_density",
        algorithms=("astar",),
        seed=3,
        generator=GeneratorConfig(kind="maze", height=11, width=11),
        queries=(QuerySpec(start=(0, 0), goal=(10, 10)),),
        output_dir=str(tmp_path),
        timeout_sec=5.0,
    )
    records = run_experiment(cfg)
    rec = records[0]
    assert rec.obstacle_count > 0
    expected = rec.obstacle_count / (rec.height * rec.width)
    assert rec.obstacle_density == expected
    assert rec.obstacle_density != 0.0
    assert cfg.generator.obstacle_density == 0.0


def test_exhausted_sfbds_export_enforces_side_sum() -> None:
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(1, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 1), GridState(1, 1), GridState(2, 1)],
    )
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success is False
    assert result.termination_reason is TerminationReason.OPEN_EXHAUSTED
    cfg = ExperimentConfig(
        name="exhausted",
        algorithms=("sfbds_f2f",),
        seed=0,
        generator=GeneratorConfig(kind="open", height=3, width=3),
        queries=(QuerySpec(start=(1, 0), goal=(1, 2)),),
        output_dir="results",
    )
    rec = _record_for(
        cfg,
        algorithm="sfbds_f2f",
        query_index=0,
        problem=problem,
        map_hash="x",
        result=result,
    )
    assert rec.forward_expanded is not None
    assert rec.backward_expanded is not None
    assert rec.forward_expanded + rec.backward_expanded == rec.expanded
    assert rec.meeting_g_F is None
    assert rec.meeting_g_B is None

    bad = SearchResult(
        success=False,
        termination_reason=TerminationReason.OPEN_EXHAUSTED,
        metrics=MetricsSnapshot(
            runtime_sec=0.0,
            generated=0,
            expanded=3,
            heuristic_evals=0,
            heuristic_time_sec=0.0,
            peak_open=0,
            peak_closed=0,
            stale_skipped=0,
            duplicates_discarded=0,
            success=False,
            forward_expanded=1,
            backward_expanded=0,
            direction_switches=0,
        ),
    )
    with pytest.raises(ValueError, match="forward_expanded"):
        _record_for(
            cfg,
            algorithm="sfbds_f2f",
            query_index=0,
            problem=problem,
            map_hash="x",
            result=bad,
        )


def test_open_and_empty_geometry_share_hash_ignoring_kind_label() -> None:
    open_gen = GeneratorConfig(kind="open", height=5, width=5)
    # Build an open map; fingerprint ignores kind label.
    query = QuerySpec(start=(0, 0), goal=(4, 4))
    open_p = build_problem(open_gen, query, seed=0)
    assert map_fingerprint(open_p, generator=open_gen, seed=0) == map_fingerprint(
        open_p, generator=GeneratorConfig(kind="maze", height=5, width=5), seed=99
    )


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
    viz = tmp_path / "cli_smoke_visual.txt"
    assert viz.is_file()
    viz_text = viz.read_text(encoding="utf-8")
    assert "Generated corridor" in viz_text
    assert "astar" in viz_text
    assert "S**G" in viz_text
    assert "S***G" not in viz_text


def test_cli_writes_2d_visual_with_axes(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main

    cfg_path = tmp_path / "cfg.yaml"
    cfg_path.write_text(
        "\n".join(
            [
                "name: cli_smoke_2d",
                "algorithm: astar",
                "seed: 1",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: open",
                "  height: 3",
                "  width: 4",
                "queries:",
                "  - start: [0, 0]",
                "    goal: [2, 3]",
            ]
        ),
        encoding="utf-8",
    )
    assert main(["--config", str(cfg_path)]) == 0
    viz = tmp_path / "cli_smoke_2d_visual.txt"
    assert viz.is_file()
    viz_text = viz.read_text(encoding="utf-8")
    assert "coords=(row,col), (0,0)=top-left" in viz_text
    assert "Generated open" in viz_text
    lines = viz_text.splitlines()
    assert any(line.startswith("0 ") for line in lines)
    assert any(line.startswith("  |") or line.startswith("  0") for line in lines)


def test_cli_config_dir_runs_sorted_yaml(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main

    def write_cfg(name: str) -> None:
        (tmp_path / f"{name}.yaml").write_text(
            "\n".join(
                [
                    f"name: {name}",
                    "algorithm: astar",
                    "seed: 1",
                    f"output_dir: {tmp_path.as_posix()}",
                    "generator:",
                    "  kind: corridor",
                    "  height: 1",
                    "  width: 4",
                    "query_sample:",
                    "  count: 2",
                    "  min_manhattan: 2",
                ]
            ),
            encoding="utf-8",
        )

    write_cfg("cli_dir_b")
    write_cfg("cli_dir_a")
    assert main(["--config-dir", str(tmp_path)]) == 0
    for name in ("cli_dir_a", "cli_dir_b"):
        csv_path = tmp_path / f"{name}.csv"
        assert csv_path.is_file()
        with csv_path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 2


def test_cli_config_dir_continues_after_bad_yaml(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main

    (tmp_path / "aaa_bad.yaml").write_text(
        "\n".join(
            [
                "name: aaa_bad",
                "algorithm: nbs",
                "seed: 1",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: open",
                "  height: 2",
                "  width: 2",
                "queries:",
                "  - start: [0, 0]",
                "    goal: [1, 1]",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "zzz_ok.yaml").write_text(
        "\n".join(
            [
                "name: zzz_ok",
                "algorithm: astar",
                "seed: 1",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: corridor",
                "  height: 1",
                "  width: 4",
                "query_sample:",
                "  count: 2",
                "  min_manhattan: 2",
            ]
        ),
        encoding="utf-8",
    )
    assert main(["--config-dir", str(tmp_path)]) == 1
    assert not (tmp_path / "aaa_bad.csv").is_file()
    ok_csv = tmp_path / "zzz_ok.csv"
    assert ok_csv.is_file()
    with ok_csv.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 2


def test_random_sampled_queries_are_connected() -> None:
    cfg = config_from_dict(
        {
            "name": "random_connected",
            "algorithms": ["astar"],
            "seed": 130,
            "timeout_sec": 5,
            "output_dir": "results",
            "generator": {
                "kind": "random_obstacles",
                "height": 12,
                "width": 12,
                "obstacle_density": 0.35,
            },
            "query_sample": {"count": 8, "min_manhattan": 6},
        }
    )
    records, frames = run_experiment_with_frames(cfg)
    assert len(frames) == 8
    for frame in frames:
        assert endpoints_connected(frame.problem)
        md = abs(
            frame.problem.start_state.row - frame.problem.goal_state.row
        ) + abs(
            frame.problem.start_state.col - frame.problem.goal_state.col
        )
        assert md >= 6
    assert all(r.success for r in records)


def test_sampled_open_run_cost_agreement() -> None:
    cfg = config_from_dict(
        {
            "name": "sampled_open",
            "algorithms": ["astar", "sfbds_f2f", "sfbds_f2e"],
            "seed": 9,
            "timeout_sec": 5,
            "output_dir": "results",
            "generator": {"kind": "open", "height": 8, "width": 8},
            "query_sample": {"count": 3, "min_manhattan": 4},
        }
    )
    records = run_experiment(cfg)
    assert len(records) == 9
    assert all(r.success for r in records)
    by_q: dict[int, set[float | None]] = {}
    for r in records:
        by_q.setdefault(r.query_index, set()).add(r.solution_cost)
    assert all(len(costs) == 1 for costs in by_q.values())


def test_write_csv_empty(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    write_csv(path, [])
    assert path.read_text(encoding="utf-8") == ""


def test_nested_densities_share_endpoints_and_hashes() -> None:
    from sfbds_compare.experiments.generators import endpoints_connected

    cfg = config_from_dict(
        {
            "name": "nested",
            "algorithms": ["astar", "sfbds_f2f", "sfbds_f2e"],
            "seed": 3,
            "timeout_sec": 5,
            "output_dir": "results",
            "generator": {
                "kind": "random_obstacles",
                "height": 8,
                "width": 8,
                "obstacle_densities": [0.10, 0.20, 0.30],
            },
            "query_sample": {"count": 2, "min_manhattan": 2},
        }
    )
    records, frames = run_experiment_with_frames(cfg)
    assert len(records) == 18
    for idx in (0, 1):
        qrows = [r for r in records if r.query_index == idx]
        counts = sorted({r.obstacle_count for r in qrows})
        assert len(counts) == 3
        assert counts[0] < counts[1] < counts[2]
        starts = {(r.start_row, r.start_col) for r in qrows}
        goals = {(r.goal_row, r.goal_col) for r in qrows}
        assert len(starts) == 1 and len(goals) == 1
        by_hash: dict[str, set[str]] = {}
        for r in qrows:
            by_hash.setdefault(r.map_hash, set()).add(r.algorithm)
        assert all(algos == {"astar", "sfbds_f2f", "sfbds_f2e"} for algos in by_hash.values())
        q_frames = [f for f in frames if f.query_index == idx]
        q_frames.sort(key=lambda f: len(f.problem.obstacles))
        assert len(q_frames) == 3
        obs = [set(f.problem.obstacles) for f in q_frames]
        assert obs[0] <= obs[1] <= obs[2]
    assert all(endpoints_connected(frame.problem) for frame in frames)


def test_nested_cli_skips_visual(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main

    cfg_path = tmp_path / "nested.yaml"
    cfg_path.write_text(
        "\n".join(
            [
                "name: nested_cli",
                "algorithm: astar",
                "seed: 1",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: random_obstacles",
                "  height: 8",
                "  width: 8",
                "  obstacle_densities: [0.10, 0.20, 0.30]",
                "query_sample:",
                "  count: 1",
                "  min_manhattan: 2",
            ]
        ),
        encoding="utf-8",
    )
    assert main(["--config", str(cfg_path)]) == 0
    assert (tmp_path / "nested_cli.csv").is_file()
    assert (tmp_path / "nested_cli.json").is_file()
    assert not (tmp_path / "nested_cli_visual.txt").is_file()


def test_runtime_repeats_keeps_expansions_and_skips_visual(tmp_path: Path) -> None:
    from sfbds_compare.experiments.runner import main, run_experiment

    cfg = config_from_dict(
        {
            "name": "timed_open",
            "algorithms": ["astar"],
            "seed": 1,
            "timeout_sec": 5,
            "runtime_repeats": 3,
            "output_dir": str(tmp_path),
            "generator": {"kind": "open", "height": 4, "width": 4},
            "queries": [{"start": [0, 0], "goal": [3, 3]}],
        }
    )
    once = config_from_dict(
        {
            "name": "once_open",
            "algorithms": ["astar"],
            "seed": 1,
            "timeout_sec": 5,
            "output_dir": str(tmp_path),
            "generator": {"kind": "open", "height": 4, "width": 4},
            "queries": [{"start": [0, 0], "goal": [3, 3]}],
        }
    )
    repeated = run_experiment(cfg)
    single = run_experiment(once)
    assert repeated[0].expanded == single[0].expanded
    assert repeated[0].success is True
    cfg_path = tmp_path / "timed.yaml"
    cfg_path.write_text(
        "\n".join(
            [
                "name: timed_cli",
                "algorithm: astar",
                "seed: 1",
                "runtime_repeats: 3",
                f"output_dir: {tmp_path.as_posix()}",
                "generator:",
                "  kind: open",
                "  height: 4",
                "  width: 4",
                "queries:",
                "  - start: [0, 0]",
                "    goal: [3, 3]",
            ]
        ),
        encoding="utf-8",
    )
    assert main(["--config", str(cfg_path)]) == 0
    assert (tmp_path / "timed_cli.csv").is_file()
    assert not (tmp_path / "timed_cli_visual.txt").is_file()


def test_runtime_repeats_median_of_successes_ignores_timeout(monkeypatch) -> None:
    from sfbds_compare.experiments import runner as runner_mod

    def _result(*, expanded: int, runtime: float, heuristic_time: float, timed_out: bool):
        return SearchResult(
            success=not timed_out,
            termination_reason=(
                TerminationReason.TIMEOUT if timed_out else TerminationReason.GOAL_FOUND
            ),
            solution_cost=None if timed_out else 6.0,
            metrics=MetricsSnapshot(
                runtime_sec=runtime,
                generated=expanded,
                expanded=expanded,
                heuristic_evals=expanded,
                heuristic_time_sec=heuristic_time,
                peak_open=1,
                peak_closed=expanded,
                stale_skipped=0,
                duplicates_discarded=0,
                success=not timed_out,
                timed_out=timed_out,
            ),
        )

    seq = [
        _result(expanded=10, runtime=1.0, heuristic_time=0.10, timed_out=False),
        _result(expanded=99, runtime=9.0, heuristic_time=0.90, timed_out=True),
        _result(expanded=20, runtime=3.0, heuristic_time=0.30, timed_out=False),
    ]
    calls = {"i": 0}

    def fake_run_query(problem, algorithm, timeout_sec=None, search_impl=None):
        i = calls["i"]
        calls["i"] += 1
        return seq[i]

    monkeypatch.setattr(runner_mod, "run_query", fake_run_query)
    cfg = ExperimentConfig(
        name="mix",
        algorithms=("astar",),
        seed=0,
        generator=GeneratorConfig(kind="open", height=4, width=4),
        queries=(QuerySpec(start=(0, 0), goal=(3, 3)),),
        output_dir="results",
        timeout_sec=1.0,
        runtime_repeats=3,
    )
    out = runner_mod._run_query_repeated(
        GridProblem(4, 4, GridState(0, 0), GridState(3, 3)),
        "astar",
        config=cfg,
    )
    assert out.success is True
    assert out.metrics.expanded == 10
    assert out.metrics.runtime_sec == 2.0
    assert out.metrics.heuristic_time_sec == pytest.approx(0.20)
    assert out.metrics.timed_out is False


def test_runtime_repeats_timeout_only_if_all_fail(monkeypatch) -> None:
    from sfbds_compare.experiments import runner as runner_mod

    timed = SearchResult(
        success=False,
        termination_reason=TerminationReason.TIMEOUT,
        metrics=MetricsSnapshot(
            runtime_sec=1.0,
            generated=1,
            expanded=1,
            heuristic_evals=1,
            heuristic_time_sec=0.1,
            peak_open=1,
            peak_closed=1,
            stale_skipped=0,
            duplicates_discarded=0,
            success=False,
            timed_out=True,
        ),
    )
    monkeypatch.setattr(
        runner_mod, "run_query", lambda *args, **kwargs: timed
    )
    cfg = ExperimentConfig(
        name="all_to",
        algorithms=("astar",),
        seed=0,
        generator=GeneratorConfig(kind="open", height=4, width=4),
        queries=(QuerySpec(start=(0, 0), goal=(3, 3)),),
        output_dir="results",
        timeout_sec=0.01,
        runtime_repeats=3,
    )
    out = runner_mod._run_query_repeated(
        GridProblem(4, 4, GridState(0, 0), GridState(3, 3)),
        "astar",
        config=cfg,
    )
    assert out.success is False
    assert out.metrics.timed_out is True
    assert out.termination_reason is TerminationReason.TIMEOUT

def test_skip_unconnected_drops_queries_without_a_far_pair() -> None:
    from sfbds_compare.experiments.runner import _connect_query

    isolated = GridProblem(
        3,
        3,
        GridState(0, 0),
        GridState(0, 2),
        obstacles=[
            GridState(0, 1),
            GridState(1, 0),
            GridState(1, 1),
            GridState(1, 2),
            GridState(2, 0),
            GridState(2, 1),
            GridState(2, 2),
        ],
    )
    skip_cfg = ExperimentConfig(
        name="skip",
        algorithms=("astar",),
        seed=0,
        generator=GeneratorConfig(kind="open", height=3, width=3),
        queries=(QuerySpec(start=(0, 0), goal=(0, 2)),),
        output_dir="results",
        min_manhattan=1,
        skip_unconnected=True,
    )
    raise_cfg = ExperimentConfig(
        name="raise",
        algorithms=("astar",),
        seed=0,
        generator=GeneratorConfig(kind="open", height=3, width=3),
        queries=(QuerySpec(start=(0, 0), goal=(0, 2)),),
        output_dir="results",
        min_manhattan=1,
        skip_unconnected=False,
    )
    assert _connect_query(skip_cfg, isolated, 0) is None
    with pytest.raises(ValueError, match="no connected free pair"):
        _connect_query(raise_cfg, isolated, 0)


def test_skip_unconnected_run_keeps_later_queries(tmp_path: Path) -> None:
    cfg = config_from_dict(
        {
            "name": "skip_run",
            "algorithm": "astar",
            "seed": 0,
            "timeout_sec": 5,
            "output_dir": str(tmp_path),
            "generator": {
                "kind": "random_obstacles",
                "height": 8,
                "width": 8,
                "obstacle_density": 0.55,
            },
            "query_sample": {
                "count": 8,
                "min_manhattan": 8,
                "skip_unconnected": True,
            },
        }
    )
    records = run_experiment(cfg)
    indices = {r.query_index for r in records}
    assert records
    assert indices <= set(range(8))
    assert all(r.success for r in records)

