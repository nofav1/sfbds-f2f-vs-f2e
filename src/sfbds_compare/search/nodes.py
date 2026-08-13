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


@dataclass(slots=True)
class SFBDSNode(Generic[StateT]):
    """Single-frontier bidirectional pair node (x, y) with dual parent chains."""

    forward: StateT
    backward: StateT
    g_F: float
    g_B: float
    h_gap: float
    parent_F: Optional["SFBDSNode[StateT]"] = None
    parent_B: Optional["SFBDSNode[StateT]"] = None
    f: float = field(init=False)

    def __post_init__(self) -> None:
        self.f = self.g_F + self.g_B + self.h_gap

    @property
    def pair_key(self) -> tuple[StateT, StateT]:
        return (self.forward, self.backward)

    @property
    def key(self) -> tuple[StateT, StateT]:
        return self.pair_key

    @property
    def g(self) -> float:
        """Pair path cost g_F + g_B (for OPEN / TBh)."""
        return self.g_F + self.g_B


def reconstruct_sfbds_path(node: SFBDSNode[StateT]) -> list[StateT]:
    """Rebuild S→G path from dual parent chains (meeting state once).

    Walks ``parent_F`` collecting forward states (then reverses) and
    ``parent_B`` collecting backward states; concatenates with the meeting
    state included once. Caller owns the Late goal rule ``forward == backward``.
    """
    forward_states: list[StateT] = []
    cur_f: Optional[SFBDSNode[StateT]] = node
    while cur_f is not None:
        forward_states.append(cur_f.forward)
        cur_f = cur_f.parent_F
    forward_states.reverse()

    backward_states: list[StateT] = []
    cur_b: Optional[SFBDSNode[StateT]] = node
    while cur_b is not None:
        backward_states.append(cur_b.backward)
        cur_b = cur_b.parent_B

    return forward_states + backward_states[1:]
