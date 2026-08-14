"""Run configured experiments and write result artifacts."""

from __future__ import annotations

import argparse
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import asdict, dataclass, replace
from statistics import median
from pathlib import Path
from typing import Any, Callable, Optional

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import ExperimentConfig, load_config
from sfbds_compare.experiments.export import write_csv, write_json
from sfbds_compare.experiments.generators import (
    build_problem,
    ensure_connected_query,
    map_fingerprint,
    prefix_obstacles,
    ranked_obstacle_cells,
    realized_obstacle_density,
)
from sfbds_compare.experiments.visualize import (
    AlgoFrame,
    QueryFrame,
    write_visual,
)
from sfbds_compare.heuristics.f2e import F2EFixedEndpointHeuristic
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.metrics.collector import MetricsCollector
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import SearchResult, TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher

# Grace period after signaling should_stop for the loop to return real metrics.
_TIMEOUT_GRACE_SEC = 2.0


@dataclass(frozen=True, slots=True)
class RunRecord:
    """Flat record for one algorithm × query run.

    ``expanded`` / ``generated`` count **states** for ``astar`` and **pairs**
    for ``sfbds_*`` (see ``expanded_unit``). Do not compare those columns
    across algorithm families without converting units.

    ``forward_expanded`` / ``backward_expanded`` are SFBDS **pair** expansions
    on that side, not A* state expansions. ``direction_switches`` counts
    consecutive expansion-side flips in the search trace, not along the
    solution path. ``obstacle_density`` is ``obstacle_count / (height * width)``
    from generated geometry, not the YAML sampler setting.
    """

    experiment: str
    algorithm: str
    seed: int
    query_index: int
    generator_kind: str
    height: int
    width: int
    obstacle_density: float
    obstacle_count: int
    map_hash: str
    start_row: int
    start_col: int
    goal_row: int
    goal_col: int
    success: bool
    termination_reason: str
    solution_cost: Optional[float]
    runtime_sec: float
    generated: int
    expanded: int
    expanded_unit: str
    forward_expanded: Optional[int]
    backward_expanded: Optional[int]
    meeting_g_F: Optional[float]
    meeting_g_B: Optional[float]
    direction_switches: Optional[int]
    heuristic_evals: int
    heuristic_time_sec: float
    peak_open: int
    peak_closed: int
    stale_skipped: int
    duplicates_discarded: int
    timed_out: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _expanded_unit(algorithm: str) -> str:
    return "state" if algorithm == "astar" else "pair"


def _search_with_stop(
    algorithm: str,
    problem: GridProblem,
    should_stop: Callable[[], bool],
) -> SearchResult[GridState]:
    if algorithm == "astar":
        return AStarSearcher(UniManhattanHeuristic()).search(
            problem, should_stop=should_stop
        )
    if algorithm == "sfbds_f2f":
        return SFBDSSearcher(F2FManhattanHeuristic()).search(
            problem, should_stop=should_stop
        )
    if algorithm == "sfbds_f2e":
        return SFBDSSearcher(F2EFixedEndpointHeuristic()).search(
            problem, should_stop=should_stop
        )
    raise ValueError(f"unsupported algorithm: {algorithm}")


def _timeout_result() -> SearchResult[GridState]:
    """Last-resort synthetic timeout if cooperative stop does not return."""
    metrics = MetricsCollector()
    metrics.start()
    metrics.timed_out = True
    snap = metrics.finish(success=False, solution_cost=None)
    return SearchResult(
        success=False,
        termination_reason=TerminationReason.TIMEOUT,
        metrics=snap,
    )


def run_query(
    problem: GridProblem,
    algorithm: str,
    *,
    timeout_sec: Optional[float],
    search_impl: Optional[
        Callable[[GridProblem, Callable[[], bool]], SearchResult[GridState]]
    ] = None,
) -> SearchResult[GridState]:
    """Run one search, optionally with a wall-clock timeout.

    On timeout the cooperative ``should_stop`` flag is set and the searcher
    returns a real TIMEOUT result with metrics so far. The pool is shut down
    with ``wait=False`` so the caller does not block on a stuck worker.
    """

    def default_impl(
        p: GridProblem, should_stop: Callable[[], bool]
    ) -> SearchResult[GridState]:
        return _search_with_stop(algorithm, p, should_stop)

    impl = search_impl or default_impl

    if timeout_sec is None:
        return impl(problem, lambda: False)

    stop = threading.Event()

    def work() -> SearchResult[GridState]:
        return impl(problem, stop.is_set)

    pool = ThreadPoolExecutor(max_workers=1)
    try:
        future = pool.submit(work)
        try:
            return future.result(timeout=timeout_sec)
        except FuturesTimeout:
            stop.set()
            try:
                return future.result(timeout=_TIMEOUT_GRACE_SEC)
            except FuturesTimeout:
                return _timeout_result()
    finally:
        pool.shutdown(wait=False)


def _write_visuals(config: ExperimentConfig) -> bool:
    if config.generator.obstacle_densities:
        return False
    if config.runtime_repeats > 1:
        return False
    return config.generator.height * config.generator.width < 200 * 200


def _is_timeout_result(result: SearchResult[GridState]) -> bool:
    return (
        result.metrics.timed_out
        or result.termination_reason is TerminationReason.TIMEOUT
    )


def _run_query_repeated(
    problem: GridProblem,
    algorithm: str,
    *,
    config: ExperimentConfig,
) -> SearchResult[GridState]:
    """Run ``runtime_repeats`` times; keep first success, median of success times.

    TIMEOUT is returned only when every repeat timed out.
    """

    n = config.runtime_repeats
    results = [
        run_query(problem, algorithm, timeout_sec=config.timeout_sec)
        for _ in range(n)
    ]
    ok = [r for r in results if not _is_timeout_result(r)]
    if not ok:
        return next(r for r in results if _is_timeout_result(r))
    first = ok[0]
    if len(ok) == 1:
        return first
    metrics = replace(
        first.metrics,
        runtime_sec=float(median([r.metrics.runtime_sec for r in ok])),
        heuristic_time_sec=float(
            median([r.metrics.heuristic_time_sec for r in ok])
        ),
    )
    return replace(first, metrics=metrics)


def _validate_sfbds_metrics(result: SearchResult[GridState]) -> None:
    """Export-time checks for SFBDS rows with recorded side counts."""

    m = result.metrics
    if m.forward_expanded is None:
        return
    if m.backward_expanded is None:
        raise ValueError("SFBDS run has forward_expanded but missing backward_expanded")
    if m.forward_expanded + m.backward_expanded != m.expanded:
        raise ValueError(
            f"forward_expanded + backward_expanded != expanded "
            f"({m.forward_expanded} + {m.backward_expanded} != {m.expanded})"
        )
    if not result.success:
        return
    if m.meeting_g_F is None or m.meeting_g_B is None:
        raise ValueError("successful SFBDS run missing meeting costs")
    if result.solution_cost is None:
        raise ValueError("successful SFBDS run missing solution_cost")
    if m.meeting_g_F + m.meeting_g_B != result.solution_cost:
        raise ValueError(
            f"meeting_g_F + meeting_g_B != solution_cost "
            f"({m.meeting_g_F} + {m.meeting_g_B} != {result.solution_cost})"
        )


def _record_for(
    config: ExperimentConfig,
    *,
    algorithm: str,
    query_index: int,
    problem: GridProblem,
    map_hash: str,
    result: SearchResult[GridState],
) -> RunRecord:
    m = result.metrics
    if algorithm.startswith("sfbds"):
        _validate_sfbds_metrics(result)
    return RunRecord(
        experiment=config.name,
        algorithm=algorithm,
        seed=config.seed,
        query_index=query_index,
        generator_kind=config.generator.kind,
        height=config.generator.height,
        width=config.generator.width,
        obstacle_density=realized_obstacle_density(problem),
        obstacle_count=len(problem.obstacles),
        map_hash=map_hash,
        start_row=problem.start_state.row,
        start_col=problem.start_state.col,
        goal_row=problem.goal_state.row,
        goal_col=problem.goal_state.col,
        success=result.success,
        termination_reason=result.termination_reason.value,
        solution_cost=result.solution_cost,
        runtime_sec=m.runtime_sec,
        generated=m.generated,
        expanded=m.expanded,
        expanded_unit=_expanded_unit(algorithm),
        heuristic_evals=m.heuristic_evals,
        heuristic_time_sec=m.heuristic_time_sec,
        peak_open=m.peak_open,
        peak_closed=m.peak_closed,
        stale_skipped=m.stale_skipped,
        duplicates_discarded=m.duplicates_discarded,
        timed_out=m.timed_out
        or result.termination_reason is TerminationReason.TIMEOUT,
        forward_expanded=m.forward_expanded,
        backward_expanded=m.backward_expanded,
        meeting_g_F=m.meeting_g_F,
        meeting_g_B=m.meeting_g_B,
        direction_switches=m.direction_switches,
    )


def _connect_query(
    config: ExperimentConfig,
    problem: GridProblem,
    idx: int,
) -> Optional[GridProblem]:
    """Relocate endpoints onto a connected pair, or skip when allowed."""

    if config.min_manhattan is None:
        return problem
    try:
        return ensure_connected_query(
            problem,
            min_manhattan=config.min_manhattan,
            rng=random.Random(config.seed + idx + 1_000_003),
        )
    except ValueError:
        if config.skip_unconnected:
            return None
        raise


def _problems_for_query(
    config: ExperimentConfig,
    query,
    idx: int,
) -> list[GridProblem]:
    """One problem, or nested-density problems sharing endpoints."""

    gen = config.generator
    levels = gen.obstacle_densities
    if not levels:
        problem = build_problem(gen, query, seed=config.seed + idx)
        problem = _connect_query(config, problem, idx)
        return [] if problem is None else [problem]

    start = GridState(query.start[0], query.start[1])
    goal = GridState(query.goal[0], query.goal[1])
    ranked = ranked_obstacle_cells(
        gen.height,
        gen.width,
        seed=config.seed + idx,
        reserved=(start, goal),
    )
    densest = max(levels)
    dense = GridProblem(
        gen.height,
        gen.width,
        start,
        goal,
        obstacles=prefix_obstacles(ranked, densest),
    )
    dense = _connect_query(config, dense, idx)
    if dense is None:
        return []
    start, goal = dense.start_state, dense.goal_state
    return [
        GridProblem(
            gen.height,
            gen.width,
            start,
            goal,
            obstacles=prefix_obstacles(ranked, density),
        )
        for density in levels
    ]


def run_experiment(config: ExperimentConfig) -> list[RunRecord]:
    """Run all algorithms on each query's resolved map (same instance)."""

    records, _frames = run_experiment_with_frames(config)
    return records


def run_experiment_with_frames(
    config: ExperimentConfig,
) -> tuple[list[RunRecord], list[QueryFrame]]:
    """Same as ``run_experiment``, plus per-query frames for ASCII visuals."""

    records: list[RunRecord] = []
    frames: list[QueryFrame] = []
    n_skipped = 0
    for idx, query in enumerate(config.queries):
        problems = _problems_for_query(config, query, idx)
        if not problems:
            n_skipped += 1
            continue
        for problem in problems:
            fingerprint = map_fingerprint(
                problem, generator=config.generator, seed=config.seed + idx
            )
            algo_frames: list[AlgoFrame] = []
            for algorithm in config.algorithms:
                result = _run_query_repeated(
                    problem, algorithm, config=config
                )
                records.append(
                    _record_for(
                        config,
                        algorithm=algorithm,
                        query_index=idx,
                        problem=problem,
                        map_hash=fingerprint,
                        result=result,
                    )
                )
                path = tuple(result.path) if result.path is not None else None
                algo_frames.append(
                    AlgoFrame(
                        algorithm=algorithm,
                        success=result.success,
                        termination_reason=result.termination_reason.value,
                        solution_cost=result.solution_cost,
                        expanded=result.metrics.expanded,
                        expanded_unit=_expanded_unit(algorithm),
                        path=path,
                    )
                )
            frames.append(
                QueryFrame(
                    query_index=idx,
                    problem=problem,
                    map_hash=fingerprint,
                    algorithms=tuple(algo_frames),
                )
            )
    if not records:
        raise ValueError(
            f"{config.name}: all {len(config.queries)} queries skipped "
            f"(no connected pair with min_manhattan={config.min_manhattan})"
        )
    if n_skipped:
        print(
            f"{config.name}: skipped {n_skipped}/{len(config.queries)} "
            "queries with no connected pair at min_manhattan="
            f"{config.min_manhattan}",
            file=sys.stderr,
        )
    return records, frames


def export_records(
    config: ExperimentConfig, records: list[RunRecord]
) -> tuple[Path, Path]:
    out_dir = Path(config.output_dir)
    stem = config.name
    rows = [r.to_dict() for r in records]
    csv_path = out_dir / f"{stem}.csv"
    json_path = out_dir / f"{stem}.json"
    write_csv(csv_path, rows)
    write_json(json_path, rows)
    return csv_path, json_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run SFBDS comparison experiment")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="Path to one experiment YAML config")
    group.add_argument(
        "--config-dir",
        help="Directory of YAML configs (sorted *.yaml)",
    )
    args = parser.parse_args(argv)
    if args.config_dir:
        paths = sorted(Path(args.config_dir).glob("*.yaml"))
        if not paths:
            raise ValueError(f"no YAML configs in {args.config_dir}")
    else:
        paths = [Path(args.config)]
    failed = 0
    for path in paths:
        try:
            config = load_config(path)
            records, frames = run_experiment_with_frames(config)
            csv_path, json_path = export_records(config, records)
            n_ok = sum(1 for r in records if r.success)
            n_to = sum(1 for r in records if r.timed_out)
            print(f"wrote {csv_path}")
            print(f"wrote {json_path}")
            if _write_visuals(config):
                viz_path = write_visual(
                    Path(config.output_dir) / f"{config.name}_visual.txt",
                    config,
                    frames,
                )
                print(f"wrote {viz_path}")
            print(
                f"{config.name}: {n_ok}/{len(records)} success, "
                f"{n_to} timed out"
            )
        except Exception as exc:
            failed += 1
            print(f"{path}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
