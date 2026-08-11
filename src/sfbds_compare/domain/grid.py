"""4-connected unit-cost grid search problem."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from sfbds_compare.domain.base import SearchProblem, Successor, TransitionMeta


@dataclass(frozen=True, slots=True, order=True)
class GridState:
    """Hashable grid cell ``(row, col)``."""

    row: int
    col: int


# Cardinal moves only (4-connected). Labels are domain-local, not used by SFBDS.
_CARDINAL_DELTAS: tuple[tuple[str, int, int], ...] = (
    ("N", -1, 0),
    ("S", 1, 0),
    ("W", 0, -1),
    ("E", 0, 1),
)


class GridProblem(SearchProblem[GridState]):
    """Unit-cost 4-connected grid with optional blocked cells.

    Coordinates use row-major indexing with ``(0, 0)`` at the top-left.
    Free cells are those inside bounds and not in ``obstacles``.
    """

    def __init__(
        self,
        height: int,
        width: int,
        start: GridState,
        goal: GridState,
        obstacles: Optional[Iterable[GridState]] = None,
    ) -> None:
        if height < 1 or width < 1:
            raise ValueError("height and width must be positive")
        self._height = height
        self._width = width
        self._obstacles = frozenset(obstacles or ())
        self._start = start
        self._goal = goal
        self._validate_endpoint(start, "start")
        self._validate_endpoint(goal, "goal")

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def obstacles(self) -> frozenset[GridState]:
        return self._obstacles

    @property
    def start_state(self) -> GridState:
        return self._start

    @property
    def goal_state(self) -> GridState:
        return self._goal

    def in_bounds(self, state: GridState) -> bool:
        return 0 <= state.row < self._height and 0 <= state.col < self._width

    def is_free(self, state: GridState) -> bool:
        return self.in_bounds(state) and state not in self._obstacles

    def successors(
        self,
        state: GridState,
        *,
        forbid_state: Optional[GridState] = None,
    ) -> Iterable[Successor[GridState]]:
        if not self.is_free(state):
            return
        for op_id, dr, dc in _CARDINAL_DELTAS:
            nxt = GridState(state.row + dr, state.col + dc)
            if not self.is_free(nxt):
                continue
            if forbid_state is not None and nxt == forbid_state:
                continue
            yield Successor(
                state=nxt,
                cost=1.0,
                meta=TransitionMeta(operator_id=op_id),
            )

    def transition_cost(self, from_state: GridState, to_state: GridState) -> float:
        if not self.is_free(from_state) or not self.is_free(to_state):
            raise ValueError("both endpoints must be free cells")
        manhattan = abs(from_state.row - to_state.row) + abs(
            from_state.col - to_state.col
        )
        if manhattan != 1:
            raise ValueError("cells are not 4-adjacent")
        return 1.0

    def describe(self) -> dict:
        return {
            "problem_type": "grid",
            "height": self._height,
            "width": self._width,
            "obstacle_count": len(self._obstacles),
            "start": (self._start.row, self._start.col),
            "goal": (self._goal.row, self._goal.col),
        }

    def _validate_endpoint(self, state: GridState, name: str) -> None:
        if not self.is_free(state):
            raise ValueError(f"{name} must be a free in-bounds cell: {state}")
