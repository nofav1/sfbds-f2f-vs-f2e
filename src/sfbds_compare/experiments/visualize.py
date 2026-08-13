"""ASCII visuals of generated maps, queries, and solution paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import ExperimentConfig

_LEGEND = "S=start  G=goal  B=start+goal  #=obstacle  .=free  *=solution path"
_COORDS = "coords=(row,col), (0,0)=top-left  s/g/b=endpoint not on path"
_ROW_PREFIX = 5  # "Q12  " / indent for 1-row query stacking


@dataclass(frozen=True, slots=True)
class AlgoFrame:
    algorithm: str
    success: bool
    termination_reason: str
    solution_cost: Optional[float]
    expanded: int
    expanded_unit: str
    path: Optional[tuple[GridState, ...]]


@dataclass(frozen=True, slots=True)
class QueryFrame:
    query_index: int
    problem: GridProblem
    map_hash: str
    algorithms: tuple[AlgoFrame, ...]


def render_grid(
    problem: GridProblem,
    path: Optional[Sequence[GridState]] = None,
    *,
    show_endpoints: bool = True,
) -> str:
    """Render a grid: start/goal beat path marks; obstacles beat free cells.

    When ``path`` is provided, endpoints that are not on it render as ``s``/``g``
    (or ``b`` if start and goal coincide). Coincident start=goal is ``B``.
    """

    has_path = path is not None
    path_set = set(path or ())
    lines: list[str] = []
    for r in range(problem.height):
        row: list[str] = []
        for c in range(problem.width):
            row.append(
                _cell_char(
                    GridState(r, c),
                    problem,
                    path_set,
                    show_endpoints=show_endpoints,
                    has_path=has_path,
                )
            )
        lines.append("".join(row))
    return "\n".join(lines)


def col_ruler(width: int, *, indent: int = 0) -> list[str]:
    """Two-line column ruler aligned to a ``width``-character map row.

    Decade labels are written only when the full digit string fits. The last
    column index always wins, overwriting any overlapping decade tail.
    """

    pad = " " * indent
    if width < 1:
        return [pad, pad]

    nums = [" "] * width
    last = str(width - 1)
    last_start = max(0, width - len(last))
    last_span = range(last_start, width)

    for c in range(0, width, 10):
        label = str(c)
        end = c + len(label)
        if end > width:
            continue
        if any(i in last_span for i in range(c, end)):
            continue
        for i, ch in enumerate(label):
            nums[c + i] = ch
    for i, ch in enumerate(last):
        pos = last_start + i
        if pos < width:
            nums[pos] = ch

    ticks = "".join(
        "|" if c % 10 == 0 or c == width - 1 else "-" for c in range(width)
    )
    return [pad + "".join(nums), pad + ticks]


def format_experiment_visual(
    config: ExperimentConfig, frames: Sequence[QueryFrame]
) -> str:
    """Plain-text report: generated map, each query, each algorithm path."""

    gen = config.generator
    lines: list[str] = [
        config.name,
        (
            f"kind={gen.kind}  size={gen.height}x{gen.width}  "
            f"seed={config.seed}  queries={len(config.queries)}  "
            f"algorithms={','.join(config.algorithms)}"
        ),
        "",
        f"Legend: {_LEGEND}",
        f"        {_COORDS}",
        "",
    ]
    if frames:
        lines.extend(_format_overview(config, frames))
        lines.append("")
    for frame in frames:
        lines.extend(_format_query(frame))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_visual(
    path: str | Path,
    config: ExperimentConfig,
    frames: Sequence[QueryFrame],
) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(format_experiment_visual(config, frames), encoding="utf-8")
    return out


def _cell_char(
    state: GridState,
    problem: GridProblem,
    path_set: set[GridState],
    *,
    show_endpoints: bool,
    has_path: bool,
) -> str:
    is_start = state == problem.start_state
    is_goal = state == problem.goal_state
    on_path = state in path_set
    if show_endpoints and (is_start or is_goal):
        coinciding = is_start and is_goal
        if coinciding:
            mark = "B"
        elif is_start:
            mark = "S"
        else:
            mark = "G"
        if has_path and not on_path:
            return mark.lower()
        return mark
    if state in problem.obstacles:
        return "#"
    if on_path:
        return "*"
    return "."


def _query_label(index: int) -> str:
    return f"Q{index:<3} "


def _row_gutter(height: int) -> int:
    """Width of ``'{row:>w} '`` so map cells align under ``col_ruler``."""

    return len(str(max(height - 1, 0))) + 1


def _endpoint_pair(problem: GridProblem) -> str:
    s = problem.start_state
    g = problem.goal_state
    return f"({s.row},{s.col})->({g.row},{g.col})"


def _map_block(
    problem: GridProblem,
    path: Optional[Sequence[GridState]] = None,
    *,
    show_endpoints: bool = True,
    extra_indent: int = 0,
) -> list[str]:
    """Column ruler plus map rows; 2D rows are prefixed with the row index."""

    pad = " " * extra_indent
    body = render_grid(problem, path, show_endpoints=show_endpoints)
    if problem.height == 1:
        lines = col_ruler(problem.width, indent=extra_indent)
        for row in body.splitlines():
            lines.append(f"{pad}{row}")
        return lines

    gutter = _row_gutter(problem.height)
    lines = col_ruler(problem.width, indent=extra_indent + gutter)
    label_w = gutter - 1
    for r, row in enumerate(body.splitlines()):
        lines.append(f"{pad}{r:>{label_w}} {row}")
    return lines


def _format_overview(
    config: ExperimentConfig, frames: Sequence[QueryFrame]
) -> list[str]:
    first = frames[0].problem
    same_geom = all(
        f.problem.height == first.height
        and f.problem.width == first.width
        and f.problem.obstacles == first.obstacles
        for f in frames
    )
    title = f"== Generated {config.generator.kind} =="
    if not same_geom:
        return [
            title,
            (
                "Map geometry differs per query (see each query section). "
                f"First query: {first.height}x{first.width}, "
                f"{len(first.obstacles)} obstacles."
            ),
        ]

    lines = [
        title,
        (
            f"{first.height}x{first.width}, "
            f"{len(first.obstacles)} obstacles"
        ),
        "",
    ]
    if first.height == 1:
        lines.extend(col_ruler(first.width, indent=_ROW_PREFIX))
        for frame in frames:
            row = render_grid(frame.problem)
            lines.append(
                f"{_query_label(frame.query_index)}{row}  "
                f"{_endpoint_pair(frame.problem)}"
            )
        return lines

    lines.extend(_map_block(first, show_endpoints=False))
    lines.append("")
    lines.append("Queries on this geometry:")
    for frame in frames:
        lines.append(
            f"  {_query_label(frame.query_index).strip()}  "
            f"{_endpoint_pair(frame.problem)}"
        )
    return lines


def _format_query(frame: QueryFrame) -> list[str]:
    p = frame.problem
    start = (p.start_state.row, p.start_state.col)
    goal = (p.goal_state.row, p.goal_state.col)
    indent = 2 if p.height == 1 else 0
    lines = [
        (
            f"== Query {frame.query_index}  {start} -> {goal}  "
            f"hash={frame.map_hash} =="
        ),
        "",
        "map",
        *_map_block(p, extra_indent=indent),
        "",
    ]
    for algo in frame.algorithms:
        lines.extend(_format_algo(p, algo))
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    return lines


def _format_algo(problem: GridProblem, algo: AlgoFrame) -> list[str]:
    cost = "-" if algo.solution_cost is None else f"{algo.solution_cost:g}"
    if algo.success and algo.path is None:
        status = "ok (no path)"
    elif algo.success:
        status = "ok"
    else:
        status = algo.termination_reason
    header = (
        f"  {algo.algorithm:<10}  {status}  cost={cost}  "
        f"expanded={algo.expanded} {algo.expanded_unit}"
    )
    if algo.success and algo.path is None:
        return [header]
    if algo.success and algo.path is not None:
        path_set = set(algo.path)
        if (
            problem.start_state not in path_set
            or problem.goal_state not in path_set
        ):
            header += "  (path misses endpoints)"
        if (
            algo.solution_cost is not None
            and len(algo.path) != int(algo.solution_cost) + 1
        ):
            header += f"  path_len={len(algo.path)} != cost+1"
    indent = 2 if problem.height == 1 else 0
    return [header, *_map_block(problem, path=algo.path, extra_indent=indent)]
