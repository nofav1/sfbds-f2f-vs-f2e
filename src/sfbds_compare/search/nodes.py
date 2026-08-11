"""Search node types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Hashable, Optional, TypeVar

StateT = TypeVar("StateT", bound=Hashable)


@dataclass(slots=True)
class AStarNode(Generic[StateT]):
    """Unidirectional A* search node (domain state + search metadata)."""

    state: StateT
    g: float
    h: float
    parent: Optional["AStarNode[StateT]"] = None
    f: float = field(init=False)

    def __post_init__(self) -> None:
        self.f = self.g + self.h

    @property
    def key(self) -> StateT:
        return self.state
