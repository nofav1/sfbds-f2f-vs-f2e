"""Unit tests for F2F vs F2E pair-bound comparison helpers."""

from __future__ import annotations

import csv
import importlib.util
import random
import sys
from pathlib import Path

from sfbds_compare.domain.grid import GridProblem, GridState
from sfbds_compare.heuristics.f2f import F2FManhattanHeuristic
from sfbds_compare.heuristics.grid_distance import manhattan
from sfbds_compare.search.sfbds import SFBDSSearcher

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "heuristic_strength.py"
_SNAPSHOT = _ROOT / "results" / "analysis" / "pair-bound" / "2026-08-17-heuristic-strength"


def _load_mod():
    spec = importlib.util.spec_from_file_location("heuristic_strength", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["heuristic_strength"] = mod
    spec.loader.exec_module(mod)
    return mod


hs = _load_mod()


def test_meeting_pair_bounds_equal() -> None:
    problem = GridProblem(5, 5, GridState(0, 0), GridState(4, 4))
    m = GridState(2, 2)
    g_F, g_B = 4.0, 5.0
    assert hs.lb_f2f(m, m, g_F, g_B) == g_F + g_B
    assert hs.lb_f2e(m, m, problem, g_F, g_B) == g_F + g_B


def test_feasible_g_f2f_bound_dominates() -> None:
    problem = GridProblem(8, 8, GridState(0, 0), GridState(7, 7))
    s, g = problem.start_state, problem.goal_state
    for u_r in range(8):
        for u_c in range(8):
            u = GridState(u_r, u_c)
            g_F = manhattan(s, u)
            for v_r in range(8):
                for v_c in range(8):
                    v = GridState(v_r, v_c)
                    g_B = manhattan(v, g)
                    f2f = hs.lb_f2f(u, v, g_F, g_B)
                    f2e = hs.lb_f2e(u, v, problem, g_F, g_B)
                    assert f2f + 1e-9 >= f2e


def test_refuse_nonempty_out(tmp_path: Path) -> None:
    out = tmp_path / "slug"
    out.mkdir()
    (out / "stale.txt").write_text("x", encoding="utf-8")
    assert hs.refuse_out_dir(out, force=False) is not None
    assert hs.refuse_out_dir(out, force=True) is None
    empty = tmp_path / "empty"
    empty.mkdir()
    assert hs.refuse_out_dir(empty, force=False) is None


def test_recording_heuristic_on_tiny_search() -> None:
    problem = GridProblem(1, 6, GridState(0, 0), GridState(0, 5))
    stats = hs.BoundStats()
    recorder = hs.RecordingHeuristic(
        F2FManhattanHeuristic(),
        stats=stats,
        reservoir=hs.Reservoir(200, random.Random(0)),
        family="tiny",
        query_index=0,
        source="f2f",
    )
    result = SFBDSSearcher(recorder).search(problem)
    assert result.success
    assert stats.n == result.metrics.heuristic_evals
    assert stats.n_f2e_stronger == 0
    assert stats.n_meeting >= 1
    meetings = [
        item
        for item in recorder.reservoir.items
        if item["u_row"] == item["v_row"] and item["u_col"] == item["v_col"]
    ]
    assert meetings
    assert all(abs(float(item["diff"])) <= hs.EPS for item in meetings)


def test_frozen_expansion_splits_and_query_8() -> None:
    notes = hs.check_frozen_splits()
    assert any("nested_64_d45 q=8: expansion_diff=-1" in line for line in notes)
    n_f2f, n_f2e, n_tie, f2e_fewer = hs.frozen_expansion_counts(
        "study_random_64_dense_opt.csv", 1842
    )
    assert (n_f2f, n_f2e, n_tie) == (14, 1, 15)
    assert f2e_fewer == [8]


def test_check_only() -> None:
    assert hs.main(["--check-only"]) == 0


def test_snapshot_locks_query_8_bound_stats() -> None:
    path = _SNAPSHOT / "query_summary.csv"
    assert path.is_file(), "commit query_summary.csv for this slug"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    q8 = [
        r
        for r in rows
        if r["family"] == "nested_64_d45" and int(r["query_index"]) == 8
    ]
    assert len(q8) == 1
    assert int(q8[0]["expansion_diff"]) == -1
    assert float(q8[0]["pooled_median_diff"]) == 4.0
    assert abs(float(q8[0]["pooled_frac_f2f_stronger"]) - 0.737) < 0.01
    maze = [r for r in rows if r["family"] == "maze_127"]
    n_stronger = sum(int(r["pooled_n_f2f_stronger"]) for r in maze)
    n = sum(int(r["pooled_n"]) for r in maze)
    assert abs(n_stronger / n - 0.675) < 0.005
