"""Experiment configuration loading and validation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import yaml

ALGORITHMS = frozenset({"astar", "sfbds_f2f", "sfbds_f2e"})
GENERATOR_KINDS = frozenset({"open", "random_obstacles", "corridor", "maze"})


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
    obstacle_densities: tuple[float, ...] = ()
    maze_braid: float = 0.0


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    name: str
    algorithms: tuple[str, ...]
    seed: int
    generator: GeneratorConfig
    queries: tuple[QuerySpec, ...]
    output_dir: str
    timeout_sec: Optional[float] = None
    min_manhattan: Optional[int] = None
    runtime_repeats: int = 1

    @property
    def algorithm(self) -> str:
        """First algorithm (compat for single-algo configs)."""
        return self.algorithms[0]


def _as_cell(value: Sequence[Any], *, label: str) -> tuple[int, int]:
    if len(value) != 2:
        raise ValueError(f"{label} must be [row, col]")
    return (int(value[0]), int(value[1]))


def sample_queries(
    *,
    height: int,
    width: int,
    count: int,
    min_manhattan: int,
    seed: int,
) -> tuple[QuerySpec, ...]:
    """Sample distinct in-bounds start/goal pairs with a Manhattan floor."""

    if count < 1:
        raise ValueError("query_sample count must be positive")
    if min_manhattan < 1:
        raise ValueError("min_manhattan must be at least 1")
    max_md = (height - 1) + (width - 1)
    if min_manhattan > max_md:
        raise ValueError(
            f"min_manhattan {min_manhattan} exceeds grid diameter {max_md}"
        )

    rng = random.Random(seed)
    seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    out: list[QuerySpec] = []
    attempts = 0
    limit = max(10_000, count * 200)
    while len(out) < count:
        attempts += 1
        if attempts > limit:
            raise ValueError(
                f"could not sample {count} queries with min_manhattan="
                f"{min_manhattan} on {height}x{width}"
            )
        start = (rng.randrange(height), rng.randrange(width))
        goal = (rng.randrange(height), rng.randrange(width))
        md = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        if md < min_manhattan:
            continue
        key = (start, goal) if start <= goal else (goal, start)
        if key in seen:
            continue
        seen.add(key)
        out.append(QuerySpec(start=start, goal=goal))
    return tuple(out)


def _parse_algorithms(data: Mapping[str, Any]) -> tuple[str, ...]:
    if "algorithms" in data and data["algorithms"] is not None:
        raw = list(data["algorithms"])
    elif "algorithm" in data:
        raw = [data["algorithm"]]
    else:
        raise ValueError("config must set algorithm or algorithms")
    if not raw:
        raise ValueError("algorithms must be non-empty")
    algos: list[str] = []
    for item in raw:
        name = str(item)
        if name not in ALGORITHMS:
            raise ValueError(f"unsupported algorithm: {name}")
        algos.append(name)
    return tuple(algos)


def _validate_queries(
    queries: tuple[QuerySpec, ...], generator: GeneratorConfig
) -> None:
    if generator.kind == "corridor" and generator.height != 1:
        raise ValueError("corridor generator requires height == 1")
    for q in queries:
        for label, cell in (("start", q.start), ("goal", q.goal)):
            r, c = cell
            if not (0 <= r < generator.height and 0 <= c < generator.width):
                raise ValueError(
                    f"{label} {cell} out of bounds for "
                    f"{generator.height}x{generator.width}"
                )


def config_from_dict(data: Mapping[str, Any]) -> ExperimentConfig:
    algorithms = _parse_algorithms(data)

    gen_raw = data["generator"]
    kind = str(gen_raw["kind"])
    if kind not in GENERATOR_KINDS:
        raise ValueError(f"unsupported generator kind: {kind}")
    height = int(gen_raw["height"])
    width = int(gen_raw["width"])
    if height < 1 or width < 1:
        raise ValueError("generator height/width must be positive")

    has_scalar = (
        "obstacle_density" in gen_raw and gen_raw["obstacle_density"] is not None
    )
    has_list = bool(gen_raw.get("obstacle_densities"))
    if has_scalar and has_list:
        raise ValueError("set obstacle_density or obstacle_densities, not both")

    densities: tuple[float, ...] = ()
    density = 0.0
    if has_list:
        if kind != "random_obstacles":
            raise ValueError("obstacle_densities requires kind random_obstacles")
        raw_list = list(gen_raw["obstacle_densities"])
        parsed = [float(x) for x in raw_list]
        if len(parsed) != len(set(parsed)):
            raise ValueError("obstacle_densities must be unique")
        for item in parsed:
            if not 0.0 <= item < 1.0:
                raise ValueError("obstacle_densities values must be in [0, 1)")
        densities = tuple(sorted(parsed))
    else:
        density = float(gen_raw.get("obstacle_density", 0.0))
        if not 0.0 <= density < 1.0:
            raise ValueError("obstacle_density must be in [0, 1)")

    maze_braid = float(gen_raw.get("maze_braid", 0.0))
    if maze_braid != 0.0 and kind != "maze":
        raise ValueError("maze_braid requires kind maze")
    if not 0.0 <= maze_braid < 1.0:
        raise ValueError("maze_braid must be in [0, 1)")

    generator = GeneratorConfig(
        kind=kind,
        height=height,
        width=width,
        obstacle_density=density,
        obstacle_densities=densities,
        maze_braid=maze_braid,
    )

    timeout = data.get("timeout_sec")
    timeout_sec = None if timeout is None else float(timeout)
    if timeout_sec is not None and timeout_sec <= 0:
        raise ValueError("timeout_sec must be positive when set")

    repeats_raw = data.get("runtime_repeats", 1)
    runtime_repeats = int(repeats_raw)
    if runtime_repeats < 1:
        raise ValueError("runtime_repeats must be at least 1")

    seed = int(data.get("seed", 0))
    queries_raw = data.get("queries") or []
    sample_raw = data.get("query_sample")
    min_manhattan: Optional[int] = None
    if queries_raw and sample_raw:
        raise ValueError("set queries or query_sample, not both")
    if sample_raw:
        if not isinstance(sample_raw, Mapping):
            raise ValueError("query_sample must be a mapping")
        if "count" not in sample_raw:
            raise ValueError("query_sample.count is required")
        min_manhattan = int(sample_raw.get("min_manhattan", 1))
        queries = sample_queries(
            height=height,
            width=width,
            count=int(sample_raw["count"]),
            min_manhattan=min_manhattan,
            seed=seed,
        )
    elif queries_raw:
        queries = tuple(
            QuerySpec(
                start=_as_cell(q["start"], label="start"),
                goal=_as_cell(q["goal"], label="goal"),
            )
            for q in queries_raw
        )
    else:
        raise ValueError("config must set queries or query_sample")
    _validate_queries(queries, generator)

    return ExperimentConfig(
        name=str(data.get("name", "run")),
        algorithms=algorithms,
        seed=seed,
        generator=generator,
        queries=queries,
        output_dir=str(data.get("output_dir", "results")),
        timeout_sec=timeout_sec,
        min_manhattan=min_manhattan,
        runtime_repeats=runtime_repeats,
    )


def load_config(path: str | Path) -> ExperimentConfig:
    text = Path(path).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, Mapping):
        raise ValueError("config root must be a mapping")
    return config_from_dict(data)
