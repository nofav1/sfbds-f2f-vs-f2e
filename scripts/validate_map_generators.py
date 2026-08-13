"""One-off map-generator validation (artifacts under results/pilot/map_validation)."""

from __future__ import annotations

import json
from pathlib import Path

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import GeneratorConfig, QuerySpec
from sfbds_compare.experiments.generators import build_problem, map_fingerprint
from sfbds_compare.heuristics.grid_distance import manhattan
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher

OUT = Path("results/pilot/map_validation")
OUT.mkdir(parents=True, exist_ok=True)

CASES: list[tuple[str, GeneratorConfig, QuerySpec, int]] = [
    ("open", GeneratorConfig("open", 15, 15), QuerySpec((0, 0), (14, 14)), 10),
    ("open", GeneratorConfig("open", 15, 15), QuerySpec((0, 0), (14, 14)), 99),
    (
        "random",
        GeneratorConfig("random_obstacles", 12, 12, 0.15),
        QuerySpec((0, 0), (11, 11)),
        20,
    ),
    (
        "random",
        GeneratorConfig("random_obstacles", 12, 12, 0.15),
        QuerySpec((0, 0), (11, 11)),
        21,
    ),
    (
        "random",
        GeneratorConfig("random_obstacles", 12, 12, 0.15),
        QuerySpec((0, 5), (11, 5)),
        21,
    ),
    ("corridor", GeneratorConfig("corridor", 1, 40), QuerySpec((0, 0), (0, 39)), 40),
    ("corridor", GeneratorConfig("corridor", 1, 20), QuerySpec((0, 0), (0, 19)), 1),
    ("maze", GeneratorConfig("maze", 15, 15), QuerySpec((0, 0), (14, 14)), 30),
    ("maze", GeneratorConfig("maze", 15, 15), QuerySpec((0, 0), (14, 14)), 31),
    ("maze", GeneratorConfig("maze", 15, 15), QuerySpec((0, 0), (0, 14)), 30),
    ("maze", GeneratorConfig("maze", 11, 11), QuerySpec((0, 0), (10, 10)), 3),
]


def render(problem: GridProblem, path: list[GridState] | None = None) -> str:
    path_set = set(path or [])
    obs = set(problem.obstacles)
    lines: list[str] = []
    for r in range(problem.height):
        row: list[str] = []
        for c in range(problem.width):
            s = GridState(r, c)
            if s == problem.start_state:
                ch = "S"
            elif s == problem.goal_state:
                ch = "G"
            elif s in obs:
                ch = "#"
            elif s in path_set:
                ch = "*"
            else:
                ch = "."
            row.append(ch)
        lines.append("".join(row))
    return "\n".join(lines)


def avg_branch(problem: GridProblem) -> float:
    free = [
        GridState(r, c)
        for r in range(problem.height)
        for c in range(problem.width)
        if problem.is_free(GridState(r, c))
    ]
    if not free:
        return 0.0
    return sum(problem.branch_factor(s) for s in free) / len(free)


def analyze(
    label: str, gen: GeneratorConfig, query: QuerySpec, seed: int
) -> dict:
    problem = build_problem(gen, query, seed=seed)
    md = manhattan(problem.start_state, problem.goal_state)
    result = AStarSearcher(UniManhattanHeuristic()).search(problem)
    n_cells = problem.height * problem.width
    n_obs = len(problem.obstacles)
    cost = result.solution_cost
    path = list(result.path) if result.path else None
    ascii_map = render(problem, path)
    fp = map_fingerprint(problem, generator=gen, seed=seed)
    fp_other = map_fingerprint(
        problem,
        generator=GeneratorConfig("open", gen.height, gen.width),
        seed=999,
    )
    stats = {
        "label": label,
        "kind": gen.kind,
        "seed": seed,
        "height": problem.height,
        "width": problem.width,
        "obstacle_count": n_obs,
        "obstacle_ratio": round(n_obs / n_cells, 4),
        "free_count": n_cells - n_obs,
        "start": [problem.start_state.row, problem.start_state.col],
        "goal": [problem.goal_state.row, problem.goal_state.col],
        "manhattan": md,
        "optimal_cost": cost,
        "detour": None if cost is None else cost - md,
        "solvable": result.success,
        "avg_branch_factor_free": round(avg_branch(problem), 3),
        "map_hash": fp,
        "map_hash_ignores_kind_label": fp == fp_other,
        "density_config": gen.obstacle_density,
    }
    stem = (
        f"{label}_h{problem.height}w{problem.width}_s{seed}"
        f"_S{query.start[0]}-{query.start[1]}_G{query.goal[0]}-{query.goal[1]}"
    )
    (OUT / f"{stem}.txt").write_text(
        json.dumps(stats, indent=2) + "\n\n" + ascii_map + "\n",
        encoding="utf-8",
    )
    (OUT / f"{stem}.map.txt").write_text(ascii_map + "\n", encoding="utf-8")
    return stats


def main() -> None:
    rows = [analyze(*case) for case in CASES]

    open_p = build_problem(
        GeneratorConfig("open", 15, 15), QuerySpec((0, 0), (14, 14)), seed=10
    )
    maze_p = build_problem(
        GeneratorConfig("maze", 15, 15), QuerySpec((0, 0), (14, 14)), seed=30
    )
    identical_geom = set(open_p.obstacles) == set(maze_p.obstacles) and (
        open_p.height,
        open_p.width,
    ) == (maze_p.height, maze_p.width)

    random_rows = [r for r in rows if r["label"] == "random"]
    corridor_rows = [r for r in rows if r["label"] == "corridor"]

    summary = {
        "cases": rows,
        "hash_notes": {
            "map_hash_is_geometry_only": True,
            "open_15_vs_maze_15_identical_geometry": identical_geom,
            "open_hash": map_fingerprint(
                open_p, generator=GeneratorConfig("open", 15, 15), seed=10
            ),
            "maze_hash": map_fingerprint(
                maze_p, generator=GeneratorConfig("maze", 15, 15), seed=30
            ),
        },
        "random_obstacle_counts": [
            (r["seed"], r["obstacle_count"], r["obstacle_ratio"])
            for r in random_rows
        ],
        "corridor_heights": [
            (r["seed"], r["height"], r["width"]) for r in corridor_rows
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md: list[str] = [
        "# Map generator validation",
        "",
        "Legend: `S` start, `G` goal, `#` obstacle, `.` free, `*` optimal path.",
        "",
    ]
    for r in rows:
        md.append(
            f"## {r['label']} | seed={r['seed']} | {r['height']}x{r['width']}"
        )
        md.append("")
        md.append(
            f"- obstacles={r['obstacle_count']} ({r['obstacle_ratio']:.1%}), "
            f"free={r['free_count']}, MD={r['manhattan']}, "
            f"cost={r['optimal_cost']}, detour={r['detour']}, "
            f"solvable={r['solvable']}, avgBF={r['avg_branch_factor_free']}, "
            f"hash={r['map_hash']}"
        )
        md.append("")
        stem = (
            f"{r['label']}_h{r['height']}w{r['width']}_s{r['seed']}"
            f"_S{r['start'][0]}-{r['start'][1]}_G{r['goal'][0]}-{r['goal'][1]}"
        )
        md.append("```")
        md.append((OUT / f"{stem}.map.txt").read_text(encoding="utf-8").rstrip())
        md.append("```")
        md.append("")

    (OUT / "REPORT.md").write_text("\n".join(md), encoding="utf-8")
    print(
        json.dumps(
            {k: summary[k] for k in ("hash_notes", "random_obstacle_counts")},
            indent=2,
        )
    )
    print("wrote", OUT.resolve())


if __name__ == "__main__":
    main()
