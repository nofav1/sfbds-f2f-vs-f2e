"""Unit tests for experiment config loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from sfbds_compare.experiments.config import config_from_dict, load_config


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
    assert cfg.algorithm == "astar"
    assert cfg.generator.kind == "open"
    assert cfg.queries[0].start == (0, 0)
    assert cfg.timeout_sec is None


def test_config_rejects_bad_algorithm() -> None:
    with pytest.raises(ValueError, match="unsupported algorithm"):
        config_from_dict(
            {
                "algorithm": "nbs",
                "generator": {"kind": "open", "height": 2, "width": 2},
                "queries": [{"start": [0, 0], "goal": [1, 1]}],
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
    assert cfg.algorithm == "astar"
    assert cfg.generator.kind == "corridor"
    assert cfg.queries[0].goal == (0, 3)
