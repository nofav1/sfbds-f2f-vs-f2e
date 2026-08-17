"""Unit tests for experiment config loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from sfbds_compare.experiments.config import (
    config_from_dict,
    load_config,
    sample_queries,
)


def test_config_from_dict_minimal() -> None:
    cfg = config_from_dict(
        {
            "name": "t",
            "algorithm": "astar",
            "seed": 7,
            "generator": {"kind": "open", "height": 3, "width": 3},
            "queries": [{"start": [0, 0], "goal": [2, 2]}],
            "output_dir": "results",
        }
    )
    assert cfg.algorithms == ("astar",)
    assert cfg.algorithm == "astar"
    assert cfg.generator.kind == "open"
    assert cfg.queries[0].start == (0, 0)
    assert cfg.timeout_sec is None


def test_config_algorithms_list() -> None:
    cfg = config_from_dict(
        {
            "algorithms": ["astar", "sfbds_f2f", "sfbds_f2e"],
            "generator": {"kind": "open", "height": 2, "width": 2},
            "queries": [{"start": [0, 0], "goal": [1, 1]}],
        }
    )
    assert cfg.algorithms == ("astar", "sfbds_f2f", "sfbds_f2e")


def test_config_rejects_bad_algorithm() -> None:
    with pytest.raises(ValueError, match="unsupported algorithm"):
        config_from_dict(
            {
                "algorithm": "nbs",
                "generator": {"kind": "open", "height": 2, "width": 2},
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
            }
        )


def test_config_rejects_out_of_bounds_query() -> None:
    with pytest.raises(ValueError, match="out of bounds"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {"kind": "open", "height": 2, "width": 2},
                "queries": [{"start": [0, 0], "goal": [5, 5]}],
            }
        )


def test_config_rejects_corridor_bad_height() -> None:
    with pytest.raises(ValueError, match="height == 1"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {"kind": "corridor", "height": 2, "width": 4},
                "queries": [{"start": [0, 0], "goal": [0, 3]}],
            }
        )


def test_load_smoke_yaml() -> None:
    path = (
        Path(__file__).resolve().parents[2]
        / "configs"
        / "examples"
        / "smoke_astar.yaml"
    )
    cfg = load_config(path)
    assert cfg.name == "smoke_astar"
    assert cfg.algorithms == ("astar",)
    assert cfg.generator.kind == "corridor"
    assert cfg.queries[0].goal == (0, 3)


def test_sample_queries_respects_count_and_manhattan() -> None:
    queries = sample_queries(
        height=10, width=10, count=8, min_manhattan=6, seed=42
    )
    assert len(queries) == 8
    assert len(set((q.start, q.goal) for q in queries)) == 8
    for q in queries:
        md = abs(q.start[0] - q.goal[0]) + abs(q.start[1] - q.goal[1])
        assert md >= 6
        assert 0 <= q.start[0] < 10 and 0 <= q.start[1] < 10
        assert 0 <= q.goal[0] < 10 and 0 <= q.goal[1] < 10
    again = sample_queries(
        height=10, width=10, count=8, min_manhattan=6, seed=42
    )
    assert queries == again
    unordered = {tuple(sorted((q.start, q.goal))) for q in queries}
    assert len(unordered) == 8


def test_sample_queries_dedups_reversed_pairs() -> None:
    queries = sample_queries(
        height=4, width=4, count=20, min_manhattan=1, seed=1
    )
    unordered = [tuple(sorted((q.start, q.goal))) for q in queries]
    assert len(unordered) == len(set(unordered))


def test_config_query_sample_expands() -> None:
    cfg = config_from_dict(
        {
            "name": "sampled",
            "algorithms": ["astar"],
            "seed": 3,
            "generator": {"kind": "open", "height": 8, "width": 8},
            "query_sample": {"count": 5, "min_manhattan": 4},
        }
    )
    assert len(cfg.queries) == 5
    assert cfg.min_manhattan == 4
    for q in cfg.queries:
        md = abs(q.start[0] - q.goal[0]) + abs(q.start[1] - q.goal[1])
        assert md >= 4


def test_config_rejects_queries_and_sample_together() -> None:
    with pytest.raises(ValueError, match="not both"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {"kind": "open", "height": 4, "width": 4},
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
                "query_sample": {"count": 2},
            }
        )


def test_sample_queries_rejects_impossible_manhattan() -> None:
    with pytest.raises(ValueError, match="exceeds grid diameter"):
        sample_queries(
            height=3, width=3, count=1, min_manhattan=10, seed=0
        )


def test_sample_queries_exhaustion() -> None:
    with pytest.raises(ValueError, match="could not sample"):
        sample_queries(
            height=2, width=2, count=100, min_manhattan=2, seed=0
        )


def test_config_query_sample_requires_count() -> None:
    with pytest.raises(ValueError, match="query_sample.count is required"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {"kind": "open", "height": 4, "width": 4},
                "query_sample": {"min_manhattan": 10},
            }
        )


_STUDY_SPECS = {
    "study_open_128.yaml": {
        "kind": "open",
        "height": 128,
        "width": 128,
        "count": 30,
        "min_manhattan": 64,
        "obstacle_density": 0.0,
    },
    "study_random_64.yaml": {
        "kind": "random_obstacles",
        "height": 64,
        "width": 64,
        "count": 30,
        "min_manhattan": 24,
        "obstacle_densities": (0.10, 0.20, 0.30),
    },
    "study_random_128.yaml": {
        "kind": "random_obstacles",
        "height": 128,
        "width": 128,
        "count": 30,
        "min_manhattan": 48,
        "obstacle_densities": (0.10, 0.20, 0.30),
    },
    "study_maze_127.yaml": {
        "kind": "maze",
        "height": 127,
        "width": 127,
        "count": 30,
        "min_manhattan": 60,
        "obstacle_density": 0.0,
    },
    "study_corridor_512.yaml": {
        "kind": "corridor",
        "height": 1,
        "width": 512,
        "count": 30,
        "min_manhattan": 128,
        "obstacle_density": 0.0,
    },
}


def test_config_rejects_both_density_keys() -> None:
    with pytest.raises(ValueError, match="not both"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {
                    "kind": "random_obstacles",
                    "height": 8,
                    "width": 8,
                    "obstacle_density": 0.1,
                    "obstacle_densities": [0.1, 0.2],
                },
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
            }
        )


def test_load_study_yaml_configs() -> None:
    study_dir = (
        Path(__file__).resolve().parents[2] / "configs" / "study"
    )
    paths = sorted(study_dir.glob("study_*.yaml"))
    assert {p.name for p in paths} == set(_STUDY_SPECS)
    for path in paths:
        spec = _STUDY_SPECS[path.name]
        cfg = load_config(path)
        assert cfg.output_dir == "results/study/pair-bound"
        assert set(cfg.algorithms) == {"astar", "sfbds_f2f", "sfbds_f2e"}
        assert cfg.timeout_sec is not None
        assert cfg.generator.kind == spec["kind"]
        assert cfg.generator.height == spec["height"]
        assert cfg.generator.width == spec["width"]
        if "obstacle_densities" in spec:
            assert cfg.generator.obstacle_densities == spec["obstacle_densities"]
            assert cfg.generator.obstacle_density == 0.0
        else:
            assert cfg.generator.obstacle_density == spec["obstacle_density"]
            assert cfg.generator.obstacle_densities == ()
        assert cfg.min_manhattan == spec["min_manhattan"]
        assert len(cfg.queries) == spec["count"]
        unordered = {tuple(sorted((q.start, q.goal))) for q in cfg.queries}
        assert len(unordered) == spec["count"]
        for q in cfg.queries:
            md = abs(q.start[0] - q.goal[0]) + abs(q.start[1] - q.goal[1])
            assert md >= spec["min_manhattan"]


_FOLLOWUP_SPECS = {
    "study_maze_255.yaml": {
        "kind": "maze",
        "height": 255,
        "width": 255,
        "count": 30,
        "min_manhattan": 120,
        "runtime_repeats": 1,
    },
    "study_random_64_dense.yaml": {
        "kind": "random_obstacles",
        "height": 64,
        "width": 64,
        "count": 30,
        "min_manhattan": 24,
        "obstacle_densities": (0.30, 0.40, 0.45),
        "runtime_repeats": 1,
    },
    "study_maze_127_timed.yaml": {
        "kind": "maze",
        "height": 127,
        "width": 127,
        "count": 30,
        "min_manhattan": 60,
        "runtime_repeats": 5,
    },
    "study_maze_127_far.yaml": {
        "kind": "maze",
        "height": 127,
        "width": 127,
        "count": 30,
        "min_manhattan": 90,
        "runtime_repeats": 1,
    },
    "study_random_64_d50.yaml": {
        "kind": "random_obstacles",
        "height": 64,
        "width": 64,
        "count": 30,
        "min_manhattan": 24,
        "obstacle_densities": (0.40, 0.45, 0.50),
        "runtime_repeats": 1,
    },
    "study_random_128_dense.yaml": {
        "kind": "random_obstacles",
        "height": 128,
        "width": 128,
        "count": 30,
        "min_manhattan": 48,
        "obstacle_densities": (0.30, 0.40, 0.45),
        "runtime_repeats": 1,
    },
    "study_maze_127_braid.yaml": {
        "kind": "maze",
        "height": 127,
        "width": 127,
        "count": 30,
        "min_manhattan": 60,
        "maze_braid": 0.5,
        "runtime_repeats": 1,
    },
    "study_random_128_d45.yaml": {
        "kind": "random_obstacles",
        "height": 128,
        "width": 128,
        "count": 30,
        "min_manhattan": 28,
        "obstacle_densities": (0.45, 0.475, 0.50),
        "runtime_repeats": 1,
    },
    "study_random_64_d52.yaml": {
        "kind": "random_obstacles",
        "height": 64,
        "width": 64,
        "count": 30,
        "min_manhattan": 16,
        "obstacle_densities": (0.50, 0.51, 0.52),
        "runtime_repeats": 1,
    },
    "study_random_128_d45_md48.yaml": {
        "kind": "random_obstacles",
        "height": 128,
        "width": 128,
        "count": 30,
        "min_manhattan": 48,
        "obstacle_densities": (0.45, 0.475, 0.50),
        "runtime_repeats": 1,
        "skip_unconnected": True,
    },
    "study_maze_255_braid.yaml": {
        "kind": "maze",
        "height": 255,
        "width": 255,
        "count": 30,
        "min_manhattan": 120,
        "maze_braid": 0.5,
        "runtime_repeats": 1,
    },
}


def test_skip_unconnected_from_query_sample() -> None:
    cfg = config_from_dict(
        {
            "algorithm": "astar",
            "seed": 1,
            "generator": {"kind": "open", "height": 8, "width": 8},
            "query_sample": {
                "count": 3,
                "min_manhattan": 4,
                "skip_unconnected": True,
            },
        }
    )
    assert cfg.skip_unconnected is True
    assert cfg.min_manhattan == 4
    assert len(cfg.queries) == 3


def test_runtime_repeats_must_be_positive() -> None:
    with pytest.raises(ValueError, match="runtime_repeats"):
        config_from_dict(
            {
                "algorithm": "astar",
                "runtime_repeats": 0,
                "generator": {"kind": "open", "height": 2, "width": 2},
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
            }
        )


def test_maze_rejects_obstacle_density() -> None:
    with pytest.raises(ValueError, match="obstacle_density"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {
                    "kind": "maze",
                    "height": 5,
                    "width": 5,
                    "obstacle_density": 0.2,
                },
                "queries": [{"start": [0, 0], "goal": [4, 4]}],
            }
        )


def test_maze_braid_requires_maze_kind() -> None:
    with pytest.raises(ValueError, match="maze_braid"):
        config_from_dict(
            {
                "algorithm": "astar",
                "generator": {
                    "kind": "open",
                    "height": 4,
                    "width": 4,
                    "maze_braid": 0.5,
                },
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
            }
        )


def test_load_followup_yaml_configs() -> None:
    followup_dir = Path(__file__).resolve().parents[2] / "configs" / "followup"
    paths = sorted(followup_dir.glob("study_*.yaml"))
    assert {p.name for p in paths} == set(_FOLLOWUP_SPECS)
    for path in paths:
        spec = _FOLLOWUP_SPECS[path.name]
        cfg = load_config(path)
        assert cfg.output_dir == "results/study/pair-bound"
        assert set(cfg.algorithms) == {"astar", "sfbds_f2f", "sfbds_f2e"}
        assert cfg.generator.kind == spec["kind"]
        assert cfg.generator.height == spec["height"]
        assert cfg.generator.width == spec["width"]
        assert cfg.runtime_repeats == spec["runtime_repeats"]
        if "obstacle_densities" in spec:
            assert cfg.generator.obstacle_densities == spec["obstacle_densities"]
        assert cfg.generator.maze_braid == spec.get("maze_braid", 0.0)
        assert cfg.min_manhattan == spec["min_manhattan"]
        assert cfg.skip_unconnected == spec.get("skip_unconnected", False)
        assert len(cfg.queries) == spec["count"]


def test_refuses_frozen_legacy_output_dir() -> None:
    from sfbds_compare.experiments.config import refuse_frozen_legacy_output
    from sfbds_compare.experiments.runner import export_records

    refuse_frozen_legacy_output("results/pilot/pair-bound")
    refuse_frozen_legacy_output("results/study/pair-bound")
    with pytest.raises(ValueError, match="legacy"):
        refuse_frozen_legacy_output("results/pilot/legacy")
    with pytest.raises(ValueError, match="legacy"):
        refuse_frozen_legacy_output("results/study/legacy")
    with pytest.raises(ValueError, match="legacy"):
        config_from_dict(
            {
                "name": "t",
                "algorithm": "astar",
                "seed": 1,
                "generator": {"kind": "open", "height": 2, "width": 2},
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
                "output_dir": "results/pilot/legacy",
            }
        )
    cfg = config_from_dict(
        {
            "name": "t",
            "algorithm": "astar",
            "seed": 1,
            "generator": {"kind": "open", "height": 2, "width": 2},
            "queries": [{"start": [0, 0], "goal": [1, 1]}],
            "output_dir": "results/pilot/pair-bound",
        }
    )
    from dataclasses import replace

    with pytest.raises(ValueError, match="legacy"):
        export_records(replace(cfg, output_dir="results/study/legacy"), [])


def test_active_pilot_yamls_are_pair_bound_only() -> None:
    pilot_dir = Path(__file__).resolve().parents[2] / "configs" / "pilot"
    names = {p.name for p in pilot_dir.glob("*.yaml")}
    assert names == {
        "pilot_corridor_lb_f2e.yaml",
        "pilot_maze_lb_f2e.yaml",
        "pilot_open_lb_f2e.yaml",
        "pilot_random_lb_f2e.yaml",
    }
    for name in names:
        cfg = load_config(pilot_dir / name)
        assert cfg.output_dir == "results/pilot/pair-bound"
    retired = {
        p.name for p in (pilot_dir / "retired").glob("pilot_*.yaml")
    }
    assert retired == {
        "pilot_corridor.yaml",
        "pilot_maze.yaml",
        "pilot_open.yaml",
        "pilot_random.yaml",
    }
    for path in sorted((pilot_dir / "retired").glob("pilot_*.yaml")):
        with pytest.raises(ValueError, match="legacy"):
            load_config(path)


