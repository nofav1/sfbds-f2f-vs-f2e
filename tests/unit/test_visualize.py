"""Unit tests for ASCII experiment visuals."""

from __future__ import annotations

from pathlib import Path

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import (
    ExperimentConfig,
    GeneratorConfig,
    QuerySpec,
)
from sfbds_compare.experiments.visualize import (
    AlgoFrame,
    QueryFrame,
    col_ruler,
    format_experiment_visual,
    render_grid,
    write_visual,
)


def _corridor() -> GridProblem:
    return GridProblem(1, 8, GridState(0, 0), GridState(0, 7))


def _algo(
    algorithm: str = "astar",
    *,
    success: bool = True,
    termination_reason: str = "goal_found",
    solution_cost: float | None = 7.0,
    expanded: int = 7,
    expanded_unit: str = "state",
    path: tuple[GridState, ...] | None = None,
) -> AlgoFrame:
    return AlgoFrame(
        algorithm=algorithm,
        success=success,
        termination_reason=termination_reason,
        solution_cost=solution_cost,
        expanded=expanded,
        expanded_unit=expanded_unit,
        path=path,
    )


def _cfg(
    *,
    name: str = "viz",
    kind: str = "open",
    height: int = 3,
    width: int = 4,
    algorithms: tuple[str, ...] = ("astar",),
    n_queries: int = 1,
) -> ExperimentConfig:
    queries = tuple(
        QuerySpec(start=(0, 0), goal=(min(height - 1, 0), min(width - 1, 0)))
        for _ in range(n_queries)
    )
    return ExperimentConfig(
        name=name,
        algorithms=algorithms,
        seed=1,
        generator=GeneratorConfig(kind=kind, height=height, width=width),
        queries=queries,
        output_dir="results",
    )


def test_render_grid_marks_start_goal_path_and_obstacles() -> None:
    problem = GridProblem(
        3,
        3,
        GridState(0, 0),
        GridState(2, 2),
        obstacles=(GridState(1, 1),),
    )
    path = (
        GridState(0, 0),
        GridState(0, 1),
        GridState(0, 2),
        GridState(1, 2),
        GridState(2, 2),
    )
    text = render_grid(problem, path)
    assert text.splitlines() == ["S**", ".#*", "..G"]


def test_render_grid_can_hide_endpoints() -> None:
    problem = _corridor()
    assert render_grid(problem) == "S......G"
    assert render_grid(problem, show_endpoints=False) == "........"


def test_render_grid_start_equals_goal() -> None:
    problem = GridProblem(1, 5, GridState(0, 2), GridState(0, 2))
    assert render_grid(problem) == "..B.."
    assert render_grid(problem, path=(GridState(0, 2),)) == "..B.."


def test_render_grid_lowercase_when_path_misses_endpoints() -> None:
    problem = GridProblem(1, 5, GridState(0, 0), GridState(0, 4))
    text = render_grid(problem, path=(GridState(0, 2), GridState(0, 3)))
    assert text == "s.**g"


def test_col_ruler_exact_strings() -> None:
    assert col_ruler(11) == ["0        10", "|---------|"]
    assert col_ruler(12) == ["0         11", "|---------||"]
    assert col_ruler(13) == ["0          12", "|---------|-|"]

    nums_101, ticks_101 = col_ruler(101)
    expected_nums = [" "] * 101
    for c in range(0, 91, 10):
        label = str(c)
        expected_nums[c : c + len(label)] = list(label)
    expected_nums[98:101] = list("100")
    assert nums_101 == "".join(expected_nums)
    assert ticks_101 == "".join(
        "|" if c % 10 == 0 or c == 100 else "-" for c in range(101)
    )
    assert nums_101.endswith("100")
    assert " 10 " in f" {nums_101} "


def test_corridor_visual_shows_queries_and_algorithms() -> None:
    cfg = ExperimentConfig(
        name="pilot_corridor",
        algorithms=("astar", "sfbds_f2f"),
        seed=40,
        generator=GeneratorConfig(kind="corridor", height=1, width=8),
        queries=(
            QuerySpec(start=(0, 0), goal=(0, 7)),
            QuerySpec(start=(0, 2), goal=(0, 5)),
        ),
        output_dir="results",
    )
    path_q0 = tuple(GridState(0, c) for c in range(8))
    path_q1 = tuple(GridState(0, c) for c in range(2, 6))
    frames = [
        QueryFrame(
            query_index=0,
            problem=GridProblem(1, 8, GridState(0, 0), GridState(0, 7)),
            map_hash="abc",
            algorithms=(
                _algo(
                    "astar",
                    solution_cost=7.0,
                    expanded=7,
                    path=path_q0,
                ),
                _algo(
                    "sfbds_f2f",
                    solution_cost=7.0,
                    expanded=7,
                    expanded_unit="pair",
                    path=path_q0,
                ),
            ),
        ),
        QueryFrame(
            query_index=1,
            problem=GridProblem(1, 8, GridState(0, 2), GridState(0, 5)),
            map_hash="def",
            algorithms=(
                _algo(
                    "astar",
                    solution_cost=3.0,
                    expanded=3,
                    path=path_q1,
                ),
                _algo(
                    "sfbds_f2f",
                    solution_cost=3.0,
                    expanded=3,
                    expanded_unit="pair",
                    path=path_q1,
                ),
            ),
        ),
    ]
    text = format_experiment_visual(cfg, frames)
    assert "Generated corridor" in text
    assert "coords=(row,col), (0,0)=top-left" in text
    assert "Q0   S......G" in text
    assert "Q1   ..S..G.." in text
    assert "astar" in text and "sfbds_f2f" in text
    assert "S******G" in text
    assert "..S**G.." in text
    assert "Query 0" in text and "Query 1" in text
    assert "S*******G" not in text


def test_successful_path_length_matches_unit_cost() -> None:
    problem = GridProblem(1, 8, GridState(0, 0), GridState(0, 7))
    path = tuple(GridState(0, c) for c in range(8))
    cost = 7.0
    assert len(path) == int(cost) + 1
    overlay = render_grid(problem, path)
    assert overlay == "S******G"
    assert overlay.count("*") == max(int(cost) - 1, 0)


def test_overview_uses_framed_problem_not_config_index() -> None:
    cfg = _cfg(kind="corridor", height=1, width=5, n_queries=1)
    problem = GridProblem(1, 5, GridState(0, 1), GridState(0, 4))
    frames = [
        QueryFrame(
            query_index=9,
            problem=problem,
            map_hash="h",
            algorithms=(
                _algo(
                    path=tuple(GridState(0, c) for c in range(1, 5)),
                    solution_cost=3.0,
                    expanded=3,
                ),
            ),
        )
    ]
    text = format_experiment_visual(cfg, frames)
    assert "(0,1)->(0,4)" in text
    assert ".S..G" in text


def test_open_2d_visual_has_row_and_col_axes() -> None:
    cfg = _cfg(kind="open", height=3, width=4, n_queries=2)
    p0 = GridProblem(3, 4, GridState(0, 0), GridState(2, 3))
    p1 = GridProblem(3, 4, GridState(0, 3), GridState(2, 0))
    path0 = (
        GridState(0, 0),
        GridState(0, 1),
        GridState(0, 2),
        GridState(0, 3),
        GridState(1, 3),
        GridState(2, 3),
    )
    frames = [
        QueryFrame(
            query_index=0,
            problem=p0,
            map_hash="a",
            algorithms=(_algo(path=path0, solution_cost=5.0, expanded=5),),
        ),
        QueryFrame(
            query_index=1,
            problem=p1,
            map_hash="b",
            algorithms=(
                _algo(success=True, path=None, solution_cost=5.0, expanded=0),
            ),
        ),
    ]
    text = format_experiment_visual(cfg, frames)
    assert "Queries on this geometry:" in text
    assert "coords=(row,col), (0,0)=top-left" in text
    lines = text.splitlines()
    assert any(line.startswith("  0") and "3" in line for line in lines)
    assert any(line.startswith("  |") for line in lines)
    assert any(line.startswith("0 ") for line in lines)
    assert any(line.startswith("2 ") for line in lines)
    assert "(0,0)->(2,3)" in text
    assert "(0,3)->(2,0)" in text
    overlay = render_grid(p0, path0)
    assert overlay.count("*") == max(5 - 1, 0)
    assert len(path0) == 6
    assert "ok (no path)" in text


def test_differing_random_geometry_note() -> None:
    cfg = _cfg(kind="random_obstacles", height=3, width=3)
    p0 = GridProblem(
        3, 3, GridState(0, 0), GridState(2, 2), obstacles=(GridState(1, 1),)
    )
    p1 = GridProblem(
        3, 3, GridState(0, 0), GridState(2, 2), obstacles=(GridState(0, 2),)
    )
    frames = [
        QueryFrame(
            query_index=0,
            problem=p0,
            map_hash="a",
            algorithms=(
                _algo(
                    success=False,
                    termination_reason="open_exhausted",
                    solution_cost=None,
                    expanded=2,
                    path=None,
                ),
            ),
        ),
        QueryFrame(
            query_index=1,
            problem=p1,
            map_hash="b",
            algorithms=(
                _algo(
                    path=(
                        GridState(0, 0),
                        GridState(1, 0),
                        GridState(2, 0),
                        GridState(2, 1),
                        GridState(2, 2),
                    ),
                    solution_cost=4.0,
                    expanded=4,
                ),
            ),
        ),
    ]
    text = format_experiment_visual(cfg, frames)
    assert "Map geometry differs per query" in text
    assert "open_exhausted" in text
    assert "cost=-" in text


def test_success_without_path_is_not_a_normal_drawing() -> None:
    cfg = _cfg(kind="open", height=3, width=4)
    problem = GridProblem(3, 4, GridState(0, 0), GridState(2, 3))
    frames = [
        QueryFrame(
            query_index=0,
            problem=problem,
            map_hash="h",
            algorithms=(
                _algo(
                    success=True,
                    solution_cost=5.0,
                    expanded=4,
                    path=None,
                ),
            ),
        )
    ]
    text = format_experiment_visual(cfg, frames)
    assert "ok (no path)" in text
    assert "ok  cost=" not in text
    idx = next(
        i for i, ln in enumerate(text.splitlines()) if "ok (no path)" in ln
    )
    rest = [ln for ln in text.splitlines()[idx + 1 :] if ln.strip()]
    assert rest == []


def test_failed_run_status_without_requiring_absent_stars() -> None:
    cfg = _cfg(kind="open", height=3, width=3)
    problem = GridProblem(3, 3, GridState(0, 0), GridState(2, 2))
    frames = [
        QueryFrame(
            query_index=0,
            problem=problem,
            map_hash="h",
            algorithms=(
                _algo(
                    success=False,
                    termination_reason="open_exhausted",
                    solution_cost=None,
                    expanded=3,
                    path=None,
                ),
            ),
        )
    ]
    text = format_experiment_visual(cfg, frames)
    assert "open_exhausted" in text
    assert "cost=-" in text
    assert "ok (no path)" not in text
    assert "ok  cost=" not in text


def test_write_visual_creates_file(tmp_path: Path) -> None:
    cfg = ExperimentConfig(
        name="t",
        algorithms=("astar",),
        seed=1,
        generator=GeneratorConfig(kind="corridor", height=1, width=4),
        queries=(QuerySpec(start=(0, 0), goal=(0, 3)),),
        output_dir=str(tmp_path),
    )
    frames = [
        QueryFrame(
            query_index=0,
            problem=GridProblem(1, 4, GridState(0, 0), GridState(0, 3)),
            map_hash="h",
            algorithms=(
                _algo(
                    solution_cost=3.0,
                    expanded=3,
                    path=tuple(GridState(0, c) for c in range(4)),
                ),
            ),
        )
    ]
    path = write_visual(tmp_path / "t_visual.txt", cfg, frames)
    assert path.is_file()
    body = path.read_text(encoding="utf-8")
    assert "S**G" in body
    assert "S***G" not in body
