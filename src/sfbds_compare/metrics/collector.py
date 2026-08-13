"""Metrics collection for search algorithms."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class MetricsSnapshot:
    """Immutable metrics taken at the end of a run."""

    runtime_sec: float
    generated: int
    expanded: int
    heuristic_evals: int
    heuristic_time_sec: float
    peak_open: int
    peak_closed: int
    stale_skipped: int
    duplicates_discarded: int
    success: bool
    solution_cost: Optional[float] = None
    timed_out: bool = False
    forward_expanded: Optional[int] = None
    backward_expanded: Optional[int] = None
    meeting_g_F: Optional[float] = None
    meeting_g_B: Optional[float] = None
    direction_switches: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MetricsCollector:
    """Mutable metrics accumulator shared by A* and SFBDS."""

    generated: int = 0
    expanded: int = 0
    heuristic_evals: int = 0
    heuristic_time_sec: float = 0.0
    peak_open: int = 0
    peak_closed: int = 0
    stale_skipped: int = 0
    duplicates_discarded: int = 0
    timed_out: bool = False
    forward_expanded: Optional[int] = None
    backward_expanded: Optional[int] = None
    meeting_g_F: Optional[float] = None
    meeting_g_B: Optional[float] = None
    direction_switches: Optional[int] = None
    _start_perf: float = field(default=0.0, repr=False)
    _finished: bool = field(default=False, repr=False)

    def start(self) -> None:
        self._start_perf = time.perf_counter()
        self._finished = False

    def note_open_size(self, size: int) -> None:
        if size > self.peak_open:
            self.peak_open = size

    def note_closed_size(self, size: int) -> None:
        if size > self.peak_closed:
            self.peak_closed = size

    def add_heuristic_time(self, seconds: float) -> None:
        self.heuristic_time_sec += seconds
        self.heuristic_evals += 1

    def finish(
        self,
        *,
        success: bool,
        solution_cost: Optional[float] = None,
    ) -> MetricsSnapshot:
        runtime = time.perf_counter() - self._start_perf if self._start_perf else 0.0
        self._finished = True
        return MetricsSnapshot(
            runtime_sec=runtime,
            generated=self.generated,
            expanded=self.expanded,
            heuristic_evals=self.heuristic_evals,
            heuristic_time_sec=self.heuristic_time_sec,
            peak_open=self.peak_open,
            peak_closed=self.peak_closed,
            stale_skipped=self.stale_skipped,
            duplicates_discarded=self.duplicates_discarded,
            success=success,
            solution_cost=solution_cost,
            timed_out=self.timed_out,
            forward_expanded=self.forward_expanded,
            backward_expanded=self.backward_expanded,
            meeting_g_F=self.meeting_g_F,
            meeting_g_B=self.meeting_g_B,
            direction_switches=self.direction_switches,
        )
