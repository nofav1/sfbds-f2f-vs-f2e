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
    "study_open_32.yaml": {
        "kind": "open",
        "height": 32,
        "width": 32,
        "count": 12,
        "min_manhattan": 16,
        "obstacle_density": 0.0,
    },
    "study_random_d10.yaml": {
        "kind": "random_obstacles",
        "height": 24,
        "width": 24,
        "count": 12,
        "min_manhattan": 12,
        "obstacle_density": 0.10,
    },
    "study_random_d20.yaml": {
        "kind": "random_obstacles",
        "height": 24,
        "width": 24,
        "count": 12,
        "min_manhattan": 12,
        "obstacle_density": 0.20,
    },
    "study_random_d30.yaml": {
        "kind": "random_obstacles",
        "height": 24,
        "width": 24,
        "count": 12,
        "min_manhattan": 12,
        "obstacle_density": 0.30,
    },
    "study_maze_21.yaml": {
        "kind": "maze",
        "height": 21,
        "width": 21,
        "count": 10,
        "min_manhattan": 10,
        "obstacle_density": 0.0,
    },
    "study_corridor_80.yaml": {
        "kind": "corridor",
        "height": 1,
        "width": 80,
        "count": 8,
        "min_manhattan": 20,
        "obstacle_density": 0.0,
    },
}


def test_load_study_yaml_configs() -> None:
    study_dir = (
        Path(__file__).resolve().parents[2] / "configs" / "study"
    )
    paths = sorted(study_dir.glob("study_*.yaml"))
    assert {p.name for p in paths} == set(_STUDY_SPECS)
    for path in paths:
        spec = _STUDY_SPECS[path.name]
        cfg = load_config(path)
        assert cfg.output_dir == "results/study"
        assert set(cfg.algorithms) == {"astar", "sfbds_f2f", "sfbds_f2e"}
        assert cfg.timeout_sec is not None
        assert cfg.generator.kind == spec["kind"]
        assert cfg.generator.height == spec["height"]
        assert cfg.generator.width == spec["width"]
        assert cfg.generator.obstacle_density == spec["obstacle_density"]
        assert cfg.min_manhattan == spec["min_manhattan"]
        assert len(cfg.queries) == spec["count"]
        unordered = {tuple(sorted((q.start, q.goal))) for q in cfg.queries}
        assert len(unordered) == spec["count"]
        for q in cfg.queries:
            md = abs(q.start[0] - q.goal[0]) + abs(q.start[1] - q.goal[1])
            assert md >= spec["min_manhattan"]

