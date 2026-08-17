"""Injectable SFBDS policies (locked MVP defaults)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Hashable, TypeVar

from sfbds_compare.policies.better_path import (
    BetterPathPolicy,
    ReplaceBetterOpenPathPolicy,
)
from sfbds_compare.policies.direction import (
    BranchingFactorDirectionPolicy,
    DirectionPolicy,
)
from sfbds_compare.policies.duplicates import (
    DuplicatePolicy,
    OrderedPairDuplicatePolicy,
)
from sfbds_compare.policies.goal import GoalOnSelectPolicy, GoalTestPolicy
from sfbds_compare.policies.reopen import (
    BetterGReopenPolicy,
    NoReopenPolicy,
    ReopenPolicy,
)
from sfbds_compare.policies.tie_break import TBhTieBreakingPolicy, TieBreakingPolicy
from sfbds_compare.policies.types import (
    DuplicateLocation,
    DuplicateLookup,
    PathAction,
    Side,
)

StateT = TypeVar("StateT", bound=Hashable)


@dataclass(slots=True)
class PolicyBundle(Generic[StateT]):
    """Six policies injected into SFBDSSearcher."""

    direction: DirectionPolicy[StateT]
    goal: GoalTestPolicy[StateT]
    duplicate: DuplicatePolicy[StateT]
    better_path: BetterPathPolicy[StateT]
    reopen: ReopenPolicy[StateT]
    tie_break: TieBreakingPolicy[StateT]


def default_policies() -> PolicyBundle[Hashable]:
    """Locked MVP policy set (F2F and generic SFBDS). Stays NoReopen."""

    return PolicyBundle(
        direction=BranchingFactorDirectionPolicy(),
        goal=GoalOnSelectPolicy(),
        duplicate=OrderedPairDuplicatePolicy(),
        better_path=ReplaceBetterOpenPathPolicy(),
        reopen=NoReopenPolicy(),
        tie_break=TBhTieBreakingPolicy(),
    )


def f2e_policies() -> PolicyBundle[Hashable]:
    """Official F2E bundle: same as default except better-g CLOSED reopen.

    Remaining-cost ``h_gap`` is not consistent on the pair key ``(u, v)``.
    Use ``official_f2e_searcher()`` rather than
    ``SFBDSSearcher(F2EPairLowerBound())``. F2F keeps ``default_policies()``.
    """

    return PolicyBundle(
        direction=BranchingFactorDirectionPolicy(),
        goal=GoalOnSelectPolicy(),
        duplicate=OrderedPairDuplicatePolicy(),
        better_path=ReplaceBetterOpenPathPolicy(),
        reopen=BetterGReopenPolicy(),
        tie_break=TBhTieBreakingPolicy(),
    )


__all__ = [
    "BetterGReopenPolicy",
    "BetterPathPolicy",
    "BranchingFactorDirectionPolicy",
    "DirectionPolicy",
    "DuplicateLocation",
    "DuplicateLookup",
    "DuplicatePolicy",
    "GoalOnSelectPolicy",
    "GoalTestPolicy",
    "NoReopenPolicy",
    "OrderedPairDuplicatePolicy",
    "PathAction",
    "PolicyBundle",
    "ReplaceBetterOpenPathPolicy",
    "ReopenPolicy",
    "Side",
    "TBhTieBreakingPolicy",
    "TieBreakingPolicy",
    "default_policies",
    "f2e_policies",
]
