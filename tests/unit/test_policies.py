"""Unit tests for locked SFBDS policies."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.policies.better_path import ReplaceBetterOpenPathPolicy
from sfbds_compare.policies.direction import BranchingFactorDirectionPolicy
from sfbds_compare.policies.duplicates import OrderedPairDuplicatePolicy
from sfbds_compare.policies.goal import GoalOnSelectPolicy
from sfbds_compare.policies.reopen import NoReopenPolicy
from sfbds_compare.policies.tie_break import TBhTieBreakingPolicy
from sfbds_compare.policies.types import (
    DuplicateLocation,
    DuplicateLookup,
    PathAction,
    Side,
)
from sfbds_compare.search.nodes import SFBDSNode
from sfbds_compare.structures.closed_set import ClosedSet
from sfbds_compare.structures.open_list import LazyHeapOpen


def _pair(
    forward: str,
    backward: str,
    *,
    g_F: float = 0.0,
    g_B: float = 0.0,
    h_gap: float = 0.0,
    parent_F: SFBDSNode[str] | None = None,
    parent_B: SFBDSNode[str] | None = None,
) -> SFBDSNode[str]:
    return SFBDSNode(
        forward=forward,
        backward=backward,
        g_F=g_F,
        g_B=g_B,
        h_gap=h_gap,
        parent_F=parent_F,
        parent_B=parent_B,
    )


def _make_open() -> LazyHeapOpen[tuple[str, str], SFBDSNode[str]]:
    tie = TBhTieBreakingPolicy[str]()
    return LazyHeapOpen(
        key_of=lambda n: n.pair_key,
        g_of=lambda n: n.g,
        sort_key_of=tie.sort_key,
    )


def test_bf_prefers_smaller_side() -> None:
    # Corridor: from (0,1) with parent (0,0) only East is free on forward;
    # backward endpoint (1,0) at left edge with no parent has N/S/E (3).
    problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 2)],
    )
    root = SFBDSNode(
        forward=GridState(0, 0),
        backward=GridState(1, 0),
        g_F=0.0,
        g_B=0.0,
        h_gap=1.0,
    )
    # Move forward once so forbid_forward suppresses parent.
    node = SFBDSNode(
        forward=GridState(0, 1),
        backward=GridState(1, 0),
        g_F=1.0,
        g_B=0.0,
        h_gap=1.0,
        parent_F=root,
        parent_B=None,
    )
    bf_f = problem.branch_factor(node.forward, forbid_state=node.forbid_forward)
    bf_b = problem.branch_factor(node.backward, forbid_state=node.forbid_backward)
    assert bf_f < bf_b
    assert BranchingFactorDirectionPolicy().choose(node, problem) is Side.FORWARD


def test_bf_tie_prefers_forward() -> None:
    problem = GridProblem(1, 3, GridState(0, 0), GridState(0, 2))
    # Endpoints are both corners with no parents → BF 1 each.
    node = SFBDSNode(
        forward=GridState(0, 0),
        backward=GridState(0, 2),
        g_F=0.0,
        g_B=0.0,
        h_gap=2.0,
    )
    assert problem.branch_factor(node.forward) == problem.branch_factor(node.backward)
    assert BranchingFactorDirectionPolicy().choose(node, problem) is Side.FORWARD


def test_goal_on_select_meeting_state() -> None:
    goal = GoalOnSelectPolicy[str]()
    assert goal.is_goal(_pair("m", "m")) is True
    assert goal.is_goal(_pair("x", "y")) is False


def test_ordered_pair_duplicate_lookup() -> None:
    dup = OrderedPairDuplicatePolicy[str]()
    open_list = _make_open()
    closed: ClosedSet[tuple[str, str], SFBDSNode[str]] = ClosedSet()

    ab = _pair("a", "b", g_F=1.0)
    ba = _pair("b", "a", g_F=1.0)
    open_list.push(ab)
    closed.add(ba.pair_key, ba)

    open_hit = dup.lookup(ab.pair_key, open_list, closed)
    assert open_hit.location is DuplicateLocation.OPEN
    assert open_hit.existing is ab

    closed_hit = dup.lookup(ba.pair_key, open_list, closed)
    assert closed_hit.location is DuplicateLocation.CLOSED
    assert closed_hit.existing is ba

    unseen = dup.lookup(("x", "y"), open_list, closed)
    assert unseen.location is DuplicateLocation.UNSEEN
    assert unseen.existing is None
    assert ab.pair_key != ba.pair_key


def test_better_path_replace_open_lazy_and_noreopen() -> None:
    better = ReplaceBetterOpenPathPolicy[str]()
    reopen = NoReopenPolicy[str]()
    open_list = _make_open()
    closed: ClosedSet[tuple[str, str], SFBDSNode[str]] = ClosedSet()

    first = _pair("p", "q", g_F=5.0, h_gap=1.0)
    assert (
        better.decide(
            DuplicateLookup(DuplicateLocation.UNSEEN), first, reopen
        )
        is PathAction.PUSH
    )
    assert open_list.push(first) is True

    worse = _pair("p", "q", g_F=6.0, h_gap=0.0)
    assert (
        better.decide(
            DuplicateLookup(DuplicateLocation.OPEN, first), worse, reopen
        )
        is PathAction.DISCARD
    )

    improved = _pair("p", "q", g_F=2.0, h_gap=1.0)
    assert (
        better.decide(
            DuplicateLookup(DuplicateLocation.OPEN, first), improved, reopen
        )
        is PathAction.REPLACE_OPEN
    )
    assert open_list.push(improved) is True
    popped = open_list.pop_min()
    assert popped is improved
    # Stale first entry discarded on further pop attempts.
    assert open_list.pop_min() is None
    assert open_list.stale_skipped >= 1

    closed_node = _pair("c", "d", g_F=1.0)
    closed.add(closed_node.pair_key, closed_node)
    candidate = _pair("c", "d", g_F=0.0)
    assert (
        better.decide(
            DuplicateLookup(DuplicateLocation.CLOSED, closed_node),
            candidate,
            reopen,
        )
        is PathAction.DISCARD
    )


def test_tbh_prefers_smaller_h_gap_on_equal_f() -> None:
    tie = TBhTieBreakingPolicy[str]()
    # f = 5 both: (g=2,h=3) vs (g=4,h=1) → prefer smaller h
    a = _pair("a", "z", g_F=2.0, h_gap=3.0)
    b = _pair("b", "z", g_F=4.0, h_gap=1.0)
    assert a.f == b.f == 5.0
    assert tie.sort_key(b) < tie.sort_key(a)

    open_list = _make_open()
    open_list.push(a)
    open_list.push(b)
    assert open_list.pop_min() is b
