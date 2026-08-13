"""Grid instance generators for experiments."""

from __future__ import annotations

import random
from typing import Iterable

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import GeneratorConfig, QuerySpec


def _cell(pair: tuple[int, int]) -> GridState:
    return GridState(pair[0], pair[1])


def build_problem(
    generator: GeneratorConfig,
    query: QuerySpec,
    *,
    seed: int,
) -> GridProblem:
    """Build a GridProblem for one query under the generator settings."""

    start = _cell(query.start)
    goal = _cell(query.goal)
    kind = generator.kind

    if kind == "corridor":
        if generator.height != 1:
            raise ValueError("corridor generator requires height == 1")
        return GridProblem(1, generator.width, start, goal)

    if kind == "open":
        return GridProblem(generator.height, generator.width, start, goal)

    if kind == "random_obstacles":
        obstacles = _sample_obstacles(
            generator.height,
            generator.width,
            generator.obstacle_density,
            seed=seed,
            reserved=(start, goal),
        )
        return GridProblem(
            generator.height,
            generator.width,
            start,
            goal,
            obstacles=obstacles,
        )

    raise ValueError(f"unknown generator kind: {kind}")


def _sample_obstacles(
    height: int,
    width: int,
    density: float,
    *,
    seed: int,
    reserved: Iterable[GridState],
) -> list[GridState]:
    reserved_set = set(reserved)
    candidates = [
        GridState(r, c)
        for r in range(height)
        for c in range(width)
        if GridState(r, c) not in reserved_set
    ]
    rng = random.Random(seed)
    k = int(round(density * len(candidates)))
    if k <= 0:
        return []
    return rng.sample(candidates, k=min(k, len(candidates)))
