"""Unit tests for SFBDSSearcher with F2F / F2E heuristics."""

from __future__ import annotations

import pytest

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2e import F2EPairLowerBound
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.uni import UniManhattanHeuristic
from sfbds_compare.search.astar import AStarSearcher
from sfbds_compare.search.result import TerminationReason
from sfbds_compare.search.sfbds import SFBDSSearcher


def _assert_unit_path(
    problem: GridProblem, path: list[GridState], cost: float
) -> None:
    assert path[0] == problem.start_state
    assert path[-1] == problem.goal_state
    assert cost == len(path) - 1
    for a, b in zip(path, path[1:]):
        assert problem.transition_cost(a, b) == 1.0


def _assert_heuristic_eval_aligned(result) -> None:
    """h evals = root + non-discarded generations (A*-aligned accounting)."""
    m = result.metrics
    assert m.heuristic_evals == 1 + (m.generated - m.duplicates_discarded)


def _assert_sfbds_instrumentation(result) -> None:
    m = result.metrics
    assert m.forward_expanded is not None
    assert m.backward_expanded is not None
    assert m.direction_switches is not None
    assert m.forward_expanded + m.backward_expanded == m.expanded
    if result.success:
        assert m.meeting_g_F is not None
        assert m.meeting_g_B is not None
        assert result.solution_cost is not None
        assert m.meeting_g_F + m.meeting_g_B == result.solution_cost
    else:
        assert m.meeting_g_F is None
        assert m.meeting_g_B is None


def _assert_astar_sfbds_fields_na(result) -> None:
    m = result.metrics
    assert m.forward_expanded is None
    assert m.backward_expanded is None
    assert m.meeting_g_F is None
    assert m.meeting_g_B is None
    assert m.direction_switches is None


def test_sfbds_start_equals_goal() -> None:
    problem = GridProblem(1, 1, GridState(0, 0), GridState(0, 0))
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 0.0
    assert result.path == [GridState(0, 0)]
    assert result.termination_reason == TerminationReason.GOAL_FOUND
    assert result.metrics.expanded == 0
    assert result.metrics.forward_expanded == 0
    assert result.metrics.backward_expanded == 0
    assert result.metrics.direction_switches == 0
    assert result.metrics.meeting_g_F == 0.0
    assert result.metrics.meeting_g_B == 0.0
    assert result.metrics.heuristic_evals == 1
    _assert_sfbds_instrumentation(result)


def test_sfbds_straight_corridor() -> None:
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success
    assert result.solution_cost == 3.0
    assert result.path is not None
    _assert_unit_path(problem, list(result.path), result.solution_cost)
    _assert_heuristic_eval_aligned(result)
    _assert_sfbds_instrumentation(result)


def test_sfbds_obstacle_matches_astar() -> None:
    problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(0, 2),
        obstacles=[GridState(0, 1)],
    )
    sfbds = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert sfbds.success and astar.success
    assert sfbds.solution_cost == astar.solution_cost == 4.0
    assert sfbds.path is not None
    _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
    _assert_heuristic_eval_aligned(sfbds)
    _assert_sfbds_instrumentation(sfbds)
    _assert_astar_sfbds_fields_na(astar)


@pytest.mark.parametrize(
    ("height", "width", "start", "goal"),
    [
        (1, 4, GridState(0, 0), GridState(0, 3)),
        (5, 5, GridState(0, 0), GridState(4, 3)),
        (3, 3, GridState(0, 0), GridState(2, 2)),
        (2, 3, GridState(0, 0), GridState(0, 2)),
    ],
)
def test_sfbds_f2f_cost_agrees_with_astar_open_grids(
    height: int, width: int, start: GridState, goal: GridState
) -> None:
    problem = GridProblem(height, width, start, goal)
    sfbds = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
    assert sfbds.success and astar.success
    assert sfbds.solution_cost == astar.solution_cost
    assert sfbds.path is not None
    _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
    _assert_heuristic_eval_aligned(sfbds)
    _assert_sfbds_instrumentation(sfbds)
    _assert_astar_sfbds_fields_na(astar)


def test_sfbds_f2e_cost_agrees_with_astar_open_and_obstacle() -> None:
    open_problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 3))
    obstacle_problem = GridProblem(
        height=2,
        width=3,
        start=GridState(0, 0),
        goal=GridState(0, 2),
        obstacles=[GridState(0, 1)],
    )
    for problem in (open_problem, obstacle_problem):
        sfbds = SFBDSSearcher(F2EPairLowerBound()).search(problem)
        astar = AStarSearcher(UniManhattanHeuristic()).search(problem)
        assert sfbds.success and astar.success
        assert sfbds.solution_cost == astar.solution_cost
        assert sfbds.path is not None
        _assert_unit_path(problem, list(sfbds.path), sfbds.solution_cost)
        _assert_heuristic_eval_aligned(sfbds)
        _assert_sfbds_instrumentation(sfbds)
        _assert_astar_sfbds_fields_na(astar)


def test_sfbds_dead_end_goal_expands_backward() -> None:
    """Goal pocket has BF 1, start has BF 2: first expansion is Backward.

    After moving out of the pocket, BF ties and the policy returns Forward,
    so the trace must also record a direction switch.
    """

    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(0, 0),
        goal=GridState(2, 2),
        obstacles=[GridState(2, 1)],
    )
    for heuristic in (F2FManhattanHeuristic(), F2EPairLowerBound()):
        result = SFBDSSearcher(heuristic).search(problem)
        assert result.success
        _assert_sfbds_instrumentation(result)
        assert result.metrics.backward_expanded is not None
        assert result.metrics.direction_switches is not None
        assert result.metrics.backward_expanded >= 1
        assert result.metrics.direction_switches >= 1


def test_sfbds_unreachable_open_exhausted() -> None:
    problem = GridProblem(
        height=3,
        width=3,
        start=GridState(1, 0),
        goal=GridState(1, 2),
        obstacles=[GridState(0, 1), GridState(1, 1), GridState(2, 1)],
    )
    result = SFBDSSearcher(F2FManhattanHeuristic()).search(problem)
    assert result.success is False
    assert result.termination_reason == TerminationReason.OPEN_EXHAUSTED
    assert result.solution_cost is None
    assert result.metrics.expanded >= 1
    assert result.metrics.success is False
    _assert_heuristic_eval_aligned(result)
    _assert_sfbds_instrumentation(result)


class _RecordingPairHeuristic:
    """Spy: remaining cost 0; records g_F/g_B passed by SFBDSSearcher."""

    def __init__(self) -> None:
        self.calls: list[tuple[GridState, GridState, float, float]] = []

    def evaluate(
        self,
        forward: GridState,
        backward: GridState,
        problem: GridProblem,
        g_F: float = 0.0,
        g_B: float = 0.0,
    ) -> float:
        del problem
        self.calls.append((forward, backward, g_F, g_B))
        return 0.0


def test_sfbds_passes_child_g_to_pair_evaluate() -> None:
    """1×4 corridor: BF ties so first expansion is Forward; child's g is (1, 0).

    A swapped-kwargs call (g_F=provisional.g_B, g_B=provisional.g_F) still
    passes a nonzero-or check because one side stays 0 on this map.
    """
    problem = GridProblem(1, 4, GridState(0, 0), GridState(0, 3))
    spy = _RecordingPairHeuristic()
    result = SFBDSSearcher(spy).search(problem)
    assert result.success
    assert spy.calls
    assert spy.calls[0][2:] == (0.0, 0.0)
    assert spy.calls[1][2:] == (1.0, 0.0)
    child_gs = [(g_F, g_B) for _, _, g_F, g_B in spy.calls[1:]]
    assert child_gs
    assert all(g_F > 0.0 and g_B == 0.0 for g_F, g_B in child_gs)
