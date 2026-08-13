"""Grid instance generators for experiments."""

from __future__ import annotations

import hashlib
import random
from collections import deque
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
    """Deterministic identity for resolved map geometry (not generator label).

    Two configs that yield the same free/obstacle layout and endpoints share a
    hash even if ``generator.kind`` differs (e.g. empty maze vs open).
    """

    obstacles = sorted((o.row, o.col) for o in problem.obstacles)
    payload = (
        f"{problem.height}x{problem.width}|"
        f"S={problem.start_state.row},{problem.start_state.col}|"
        f"G={problem.goal_state.row},{problem.goal_state.col}|"
        f"obs={obstacles}"
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def realized_obstacle_density(problem: GridProblem) -> float:
    """Obstacle fraction of the generated grid: ``count / (height * width)``."""

    n_cells = problem.height * problem.width
    return len(problem.obstacles) / n_cells


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
        obstacles = _wall_passage_maze_obstacles(
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


def _manhattan(a: GridState, b: GridState) -> int:
    return abs(a.row - b.row) + abs(a.col - b.col)


def reachable_from(problem: GridProblem, origin: GridState) -> set[GridState]:
    """4-connected free cells reachable from ``origin`` (empty if blocked)."""

    if not problem.is_free(origin):
        return set()
    seen = {origin}
    queue: deque[GridState] = deque([origin])
    while queue:
        cur = queue.popleft()
        for suc in problem.successors(cur):
            if suc.state not in seen:
                seen.add(suc.state)
                queue.append(suc.state)
    return seen


def endpoints_connected(problem: GridProblem) -> bool:
    """True iff start and goal lie in the same free connected component."""

    return problem.goal_state in reachable_from(problem, problem.start_state)


def _largest_component(problem: GridProblem) -> list[GridState]:
    seen: set[GridState] = set()
    best: list[GridState] = []
    for r in range(problem.height):
        for c in range(problem.width):
            cell = GridState(r, c)
            if cell in seen or not problem.is_free(cell):
                continue
            comp = reachable_from(problem, cell)
            seen |= comp
            if len(comp) > len(best):
                best = sorted(comp, key=lambda s: (s.row, s.col))
    return best


def ensure_connected_query(
    problem: GridProblem,
    *,
    min_manhattan: int,
    rng: random.Random,
) -> GridProblem:
    """Keep obstacle geometry; move start/goal onto a connected free pair.

    Used after ``build_problem`` for ``query_sample`` so random-obstacle maps
    are not scored as solver failures when the sampled cells are separated.
    Explicit YAML queries are left unchanged (caller skips this helper).
    """

    if (
        endpoints_connected(problem)
        and _manhattan(problem.start_state, problem.goal_state) >= min_manhattan
    ):
        return problem

    cells = _largest_component(problem)
    pairs = [
        (a, b)
        for i, a in enumerate(cells)
        for b in cells[i + 1 :]
        if _manhattan(a, b) >= min_manhattan
    ]
    if not pairs:
        raise ValueError(
            f"no connected free pair with min_manhattan={min_manhattan} "
            f"on {problem.height}x{problem.width}"
        )
    start, goal = pairs[rng.randrange(len(pairs))]
    if rng.random() < 0.5:
        start, goal = goal, start
    return GridProblem(
        problem.height,
        problem.width,
        start,
        goal,
        obstacles=problem.obstacles,
    )


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


def _snap_to_room(state: GridState, height: int, width: int) -> GridState:
    """Nearest even-even room cell on the maze lattice (clamped in-bounds)."""

    r = state.row - (state.row % 2)
    c = state.col - (state.col % 2)
    max_r = height - 1 - ((height - 1) % 2)
    max_c = width - 1 - ((width - 1) % 2)
    return GridState(min(r, max_r), min(c, max_c))


def _carve_manhattan(
    free: set[GridState], a: GridState, b: GridState
) -> None:
    r, c = a.row, a.col
    free.add(GridState(r, c))
    while (r, c) != (b.row, b.col):
        if r != b.row:
            r += 1 if b.row > r else -1
        elif c != b.col:
            c += 1 if b.col > c else -1
        free.add(GridState(r, c))


def _wall_passage_maze_obstacles(
    height: int,
    width: int,
    *,
    seed: int,
    start: GridState,
    goal: GridState,
) -> list[GridState]:
    """Perfect maze: rooms on even lattice; walls stay blocked unless carved.

    DFS spans rooms at ``(2i, 2j)``. Moving between adjacent rooms carves the
    intervening wall cell. Remaining cells are obstacles. ``start``/``goal``
    are always free and connected to the nearest room by a short tunnel.
    """

    if height < 3 or width < 3:
        raise ValueError("maze generator requires height and width >= 3")

    rng = random.Random(seed)
    room_start = _snap_to_room(start, height, width)
    free: set[GridState] = {room_start}
    stack: list[GridState] = [room_start]
    visited_rooms: set[GridState] = {room_start}

    def room_neighbors(room: GridState) -> list[tuple[GridState, GridState]]:
        """Return (neighbor_room, wall_between) pairs."""
        out: list[tuple[GridState, GridState]] = []
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            nr, nc = room.row + dr, room.col + dc
            if 0 <= nr < height and 0 <= nc < width and nr % 2 == 0 and nc % 2 == 0:
                wall = GridState(room.row + dr // 2, room.col + dc // 2)
                out.append((GridState(nr, nc), wall))
        return out

    while stack:
        cur = stack[-1]
        options = [
            (nbr, wall)
            for nbr, wall in room_neighbors(cur)
            if nbr not in visited_rooms
        ]
        if not options:
            stack.pop()
            continue
        nbr, wall = rng.choice(options)
        free.add(wall)
        free.add(nbr)
        visited_rooms.add(nbr)
        stack.append(nbr)

    # Ensure start/goal are free and attached to the carved maze.
    free.add(start)
    free.add(goal)
    _carve_manhattan(free, start, room_start)
    room_goal = _snap_to_room(goal, height, width)
    if room_goal not in visited_rooms:
        # Connect room_goal into the maze by carving toward room_start.
        _carve_manhattan(free, room_goal, room_start)
        visited_rooms.add(room_goal)
    _carve_manhattan(free, goal, room_goal)

    return [
        GridState(r, c)
        for r in range(height)
        for c in range(width)
        if GridState(r, c) not in free
    ]
