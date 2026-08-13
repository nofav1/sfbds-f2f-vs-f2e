"""Experiment configuration loading and validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import yaml

ALGORITHMS = frozenset({"astar", "sfbds_f2f", "sfbds_f2e"})
GENERATOR_KINDS = frozenset({"open", "random_obstacles", "corridor"})


@dataclass(frozen=True, slots=True)
class QuerySpec:
    start: tuple[int, int]
    goal: tuple[int, int]


@dataclass(frozen=True, slots=True)
class GeneratorConfig:
    kind: str
    height: int
    width: int
    obstacle_density: float = 0.0


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    name: str
    algorithm: str
    seed: int
    generator: GeneratorConfig
    queries: tuple[QuerySpec, ...]
    output_dir: str
    timeout_sec: Optional[float] = None


def _as_cell(value: Sequence[Any], *, label: str) -> tuple[int, int]:
    if len(value) != 2:
        raise ValueError(f"{label} must be [row, col]")
    return (int(value[0]), int(value[1]))


def config_from_dict(data: Mapping[str, Any]) -> ExperimentConfig:
    algorithm = str(data["algorithm"])
    if algorithm not in ALGORITHMS:
        raise ValueError(f"unsupported algorithm: {algorithm}")

    gen_raw = data["generator"]
    kind = str(gen_raw["kind"])
    if kind not in GENERATOR_KINDS:
        raise ValueError(f"unsupported generator kind: {kind}")
    height = int(gen_raw["height"])
    width = int(gen_raw["width"])
    if height < 1 or width < 1:
        raise ValueError("generator height/width must be positive")
    density = float(gen_raw.get("obstacle_density", 0.0))
    if not 0.0 <= density < 1.0:
        raise ValueError("obstacle_density must be in [0, 1)")

    queries_raw = data.get("queries") or []
    if not queries_raw:
        raise ValueError("queries must be a non-empty list")
    queries = tuple(
        QuerySpec(
            start=_as_cell(q["start"], label="start"),
            goal=_as_cell(q["goal"], label="goal"),
        )
        for q in queries_raw
    )

    timeout = data.get("timeout_sec")
    timeout_sec = None if timeout is None else float(timeout)
    if timeout_sec is not None and timeout_sec <= 0:
        raise ValueError("timeout_sec must be positive when set")

    return ExperimentConfig(
        name=str(data.get("name", "run")),
        algorithm=algorithm,
        seed=int(data.get("seed", 0)),
        generator=GeneratorConfig(
            kind=kind,
            height=height,
            width=width,
            obstacle_density=density,
        ),
        queries=queries,
        output_dir=str(data.get("output_dir", "results")),
        timeout_sec=timeout_sec,
    )


def load_config(path: str | Path) -> ExperimentConfig:
    text = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, Mapping):
        raise ValueError("config root must be a mapping")
    return config_from_dict(data)
