"""Unit tests for MetricsCollector and SearchResult."""

from __future__ import annotations

from sfbds_compare.metrics.collector import MetricsCollector
from sfbds_compare.search.result import SearchResult, TerminationReason


def test_metrics_finish_snapshot() -> None:
    metrics = MetricsCollector()
    metrics.start()
    metrics.generated = 3
    metrics.expanded = 2
    metrics.note_open_size(4)
    metrics.note_open_size(2)
    metrics.note_closed_size(1)
    metrics.add_heuristic_time(0.01)
    snap = metrics.finish(success=False, solution_cost=None)
    assert snap.generated == 3
    assert snap.expanded == 2
    assert snap.peak_open == 4
    assert snap.peak_closed == 1
    assert snap.heuristic_evals == 1
    assert snap.success is False
    assert snap.runtime_sec >= 0.0
    assert snap.forward_expanded is None
    assert snap.backward_expanded is None
    assert snap.meeting_g_F is None
    assert snap.meeting_g_B is None
    assert snap.direction_switches is None


def test_search_result_failure_open_exhausted() -> None:
    metrics = MetricsCollector()
    metrics.start()
    snap = metrics.finish(success=False)
    result = SearchResult(
        success=False,
        termination_reason=TerminationReason.OPEN_EXHAUSTED,
        metrics=snap,
    )
    payload = result.to_dict()
    assert payload["success"] is False
    assert payload["termination_reason"] == "open_exhausted"
