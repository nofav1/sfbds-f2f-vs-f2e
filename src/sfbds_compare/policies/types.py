"""Shared enums and result types for SFBDS policies."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, Hashable, Optional, TypeVar

from sfbds_compare.search.nodes import SFBDSNode

StateT = TypeVar("StateT", bound=Hashable)


class Side(Enum):
    """Which endpoint of a pair to expand."""

    FORWARD = auto()
    BACKWARD = auto()


class DuplicateLocation(Enum):
    """Where an ordered pair key was found."""

    UNSEEN = auto()
    OPEN = auto()
    CLOSED = auto()


class PathAction(Enum):
    """What the searcher should do with a generated child."""

    PUSH = auto()
    REPLACE_OPEN = auto()
    REOPEN = auto()
    DISCARD = auto()


@dataclass(frozen=True, slots=True)
class DuplicateLookup(Generic[StateT]):
    """Result of looking up a pair key in OPEN/CLOSED."""

    location: DuplicateLocation
    existing: Optional[SFBDSNode[StateT]] = None
