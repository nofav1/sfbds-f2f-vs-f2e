"""Unit tests for SFBDSNode pair identity and path reconstruction."""

from __future__ import annotations

from sfbds_compare.domain.grid import GridState
from sfbds_compare.search.nodes import SFBDSNode, reconstruct_sfbds_path


def test_root_pair_costs_and_key() -> None:
    root = SFBDSNode(
        forward="S",
        backward="G",
        g_F=0.0,
        g_B=0.0,
        h_gap=3.0,
    )
    assert root.g == 0.0
    assert root.f == 3.0
    assert root.key == ("S", "G")
    assert root.pair_key == root.key


def test_meeting_start_equals_goal_reconstructs_singleton() -> None:
    meet = SFBDSNode(
        forward="S",
        backward="S",
        g_F=0.0,
        g_B=0.0,
        h_gap=0.0,
    )
    assert meet.forward == meet.backward
    assert reconstruct_sfbds_path(meet) == ["S"]


def test_ordered_pair_keys_are_directional() -> None:
    ab = SFBDSNode(forward="a", backward="b", g_F=0.0, g_B=0.0, h_gap=1.0)
    ba = SFBDSNode(forward="b", backward="a", g_F=0.0, g_B=0.0, h_gap=1.0)
    assert ab.key != ba.key
    assert ab.key == ("a", "b")
    assert ba.key == ("b", "a")


def test_f_set_at_construction_only() -> None:
    node = SFBDSNode(
        forward="x",
        backward="y",
        g_F=1.0,
        g_B=2.0,
        h_gap=4.0,
    )
    assert node.f == 7.0
    # Callers construct new nodes; mutating fields does not auto-refresh f.
    node.h_gap = 0.0
    assert node.f == 7.0
    refreshed = SFBDSNode(
        forward=node.forward,
        backward=node.backward,
        g_F=node.g_F,
        g_B=node.g_B,
        h_gap=0.0,
        parent_F=node.parent_F,
        parent_B=node.parent_B,
    )
    assert refreshed.f == 3.0


def test_hand_built_forward_then_backward_reconstruction() -> None:
    # Grid path S=(0,0) → (0,1) → (0,2)=m ← (1,2) ← G=(1,3)
    # When expanding one side, the other side's parent pointer is inherited.
    s = GridState(0, 0)
    a = GridState(0, 1)
    m = GridState(0, 2)
    b = GridState(1, 2)
    g = GridState(1, 3)

    root = SFBDSNode(forward=s, backward=g, g_F=0.0, g_B=0.0, h_gap=4.0)
    after_f1 = SFBDSNode(
        forward=a,
        backward=g,
        g_F=1.0,
        g_B=0.0,
        h_gap=3.0,
        parent_F=root,
        parent_B=root.parent_B,
    )
    after_f2 = SFBDSNode(
        forward=m,
        backward=g,
        g_F=2.0,
        g_B=0.0,
        h_gap=2.0,
        parent_F=after_f1,
        parent_B=after_f1.parent_B,
    )
    after_b1 = SFBDSNode(
        forward=m,
        backward=b,
        g_F=2.0,
        g_B=1.0,
        h_gap=1.0,
        parent_F=after_f2.parent_F,
        parent_B=after_f2,
    )
    meet = SFBDSNode(
        forward=m,
        backward=m,
        g_F=2.0,
        g_B=2.0,
        h_gap=0.0,
        parent_F=after_b1.parent_F,
        parent_B=after_b1,
    )

    assert meet.forward == meet.backward
    path = reconstruct_sfbds_path(meet)
    assert path == [s, a, m, b, g]
    assert meet.g == 4.0
    assert meet.g == len(path) - 1
