"""Search result and termination reasons."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Optional, Sequence, TypeVar

from sfbds_compare.metrics.collector import MetricsSnapshot

StateT = TypeVar("StateT")


class TerminationReason(str, Enum):
    GOAL_FOUND = "goal_found"
    OPEN_EXHAUSTED = "open_exhausted"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class SearchResult(Generic[StateT]):
    """Structured outcome of a search run."""

    success: bool
    termination_reason: TerminationReason
    metrics: MetricsSnapshot
    solution_cost: Optional[float] = None
    path: Optional[Sequence[StateT]] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "termination_reason": self.termination_reason.value,
            "solution_cost": self.solution_cost,
            "path_length": None if self.path is None else len(self.path),
            "error_message": self.error_message,
            "metrics": self.metrics.to_dict(),
        }
