"""Run configured experiments and write result artifacts."""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Hashable, Optional, TypeVar

from sfbds_compare.domain.base import SearchProblem
from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.experiments.config import ExperimentConfig, load_config
from sfbds_compare.experiments.export import write_csv, write_json
from sfbds_compare.experiments.generators import build_problem
from sfbds_compare.heuristics.f2e import F2EFixedEndpointHeuristic
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.metrics.collector import MetricsCollector
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import SearchResult, TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher

StateT = TypeVar("StateT", bound=Hashable)
Searcher = Callable[[SearchProblem[StateT]], SearchResult[StateT]]


@dataclass(frozen=True, slots=True)
class RunRecord:
    """Flat record for one query run."""

    experiment: str
    algorithm: str
    seed: int
    query_index: int
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
    heuristic_evals: int
    heuristic_time_sec: float
    peak_open: int
    peak_closed: int
    stale_skipped: int
    duplicates_discarded: int
    timed_out: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_searcher(algorithm: str) -> Searcher[GridState]:
    if algorithm == "astar":
        searcher: Any = AStarSearcher(UniManhattanHeuristic())
        return searcher.search
    if algorithm == "sfbds_f2f":
        searcher = SFBDSSearcher(F2FManhattanHeuristic())
        return searcher.search
    if algorithm == "sfbds_f2e":
        searcher = SFBDSSearcher(F2EFixedEndpointHeuristic())
        return searcher.search
    raise ValueError(f"unsupported algorithm: {algorithm}")


def _timeout_result() -> SearchResult[GridState]:
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
    search_fn: Searcher[GridState],
    *,
    timeout_sec: Optional[float],
) -> SearchResult[GridState]:
    if timeout_sec is None:
        return search_fn(problem)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(search_fn, problem)
        try:
            return future.result(timeout=timeout_sec)
        except FuturesTimeout:
            return _timeout_result()


def run_experiment(config: ExperimentConfig) -> list[RunRecord]:
    search_fn = make_searcher(config.algorithm)
    records: list[RunRecord] = []
    for idx, query in enumerate(config.queries):
        # Per-query seed mix so obstacle layouts can vary across queries.
        problem = build_problem(
            config.generator, query, seed=config.seed + idx
        )
        result = run_query(
            problem, search_fn, timeout_sec=config.timeout_sec
        )
        m = result.metrics
        records.append(
            RunRecord(
                experiment=config.name,
                algorithm=config.algorithm,
                seed=config.seed,
                query_index=idx,
                start_row=query.start[0],
                start_col=query.start[1],
                goal_row=query.goal[0],
                goal_col=query.goal[1],
                success=result.success,
                termination_reason=result.termination_reason.value,
                solution_cost=result.solution_cost,
                runtime_sec=m.runtime_sec,
                generated=m.generated,
                expanded=m.expanded,
                heuristic_evals=m.heuristic_evals,
                heuristic_time_sec=m.heuristic_time_sec,
                peak_open=m.peak_open,
                peak_closed=m.peak_closed,
                stale_skipped=m.stale_skipped,
                duplicates_discarded=m.duplicates_discarded,
                timed_out=m.timed_out
                or result.termination_reason is TerminationReason.TIMEOUT,
            )
        )
    return records


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
    parser.add_argument(
        "--config",
        required=True,
        help="Path to experiment YAML config",
    )
    args = parser.parse_args(argv)
    config = load_config(args.config)
    records = run_experiment(config)
    csv_path, json_path = export_records(config, records)
    print(f"wrote {csv_path}")
    print(f"wrote {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
