"""Grid instance generators for experiments."""

from __future__ import annotations

import hashlib
import random
from typing import Iterable

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import GeneratorConfig, QuerySpec


def _cell(pair: tuple[int, int]) -> GridState:
    return GridState(pair[0], pair[1])


def map_fingerprint(
    problem: GridProblem,
    *,
    generator: GeneratorConfig,
    seed: int,
) -> str:
    """Deterministic identity for a resolved map instance."""

    obstacles = sorted((o.row, o.col) for o in problem.obstacles)
    payload = (
        f"{generator.kind}|{generator.height}x{generator.width}|"
        f"d={generator.obstacle_density}|seed={seed}|"
        f"S={problem.start_state.row},{problem.start_state.col}|"
        f"G={problem.goal_state.row},{problem.goal_state.col}|"
        f"obs={obstacles}"
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


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

    if kind == "maze":
        obstacles = _dfs_maze_obstacles(
            generator.height,
            generator.width,
            seed=seed,
            start=start,
            goal=goal,
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


def _neighbors(state: GridState, height: int, width: int) -> list[GridState]:
    out: list[GridState] = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nxt = GridState(state.row + dr, state.col + dc)
        if 0 <= nxt.row < height and 0 <= nxt.col < width:
            out.append(nxt)
    return out


def _dfs_maze_obstacles(
    height: int,
    width: int,
    *,
    seed: int,
    start: GridState,
    goal: GridState,
) -> list[GridState]:
    """Carve a seeded DFS spanning tree; remaining cells are obstacles."""

    rng = random.Random(seed)
    free: set[GridState] = {start}
    stack: list[GridState] = [start]
    while stack:
        cur = stack[-1]
        options = [n for n in _neighbors(cur, height, width) if n not in free]
        if not options:
            stack.pop()
            continue
        nxt = rng.choice(options)
        free.add(nxt)
        stack.append(nxt)

    if goal not in free:
        # Manhattan tunnel from goal until we hit the carved component.
        r, c = goal.row, goal.col
        while GridState(r, c) not in free:
            free.add(GridState(r, c))
            if r != start.row:
                r += 1 if start.row > r else -1
            elif c != start.col:
                c += 1 if start.col > c else -1
            else:
                break

    return [
        GridState(r, c)
        for r in range(height)
        for c in range(width)
        if GridState(r, c) not in free
    ]
