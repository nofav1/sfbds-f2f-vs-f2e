"""Unit tests for paired F2F/F2E analysis."""

from __future__ import annotations

from pathlib import Path

import pytest

from sfbds_compare.analysis.metrics import detour_ratio
from sfbds_compare.analysis.pair import pair_rows
from sfbds_compare.analysis.stats import holm_adjust, rank_biserial, sign_test_p, wilcoxon_signed_rank
from sfbds_compare.analysis.summarize import summarize
from sfbds_compare.experiments.export import write_csv


def _raw(
    *,
    experiment: str = "t",
    algorithm: str,
    query_index: int,
    expanded: int,
    generated: int | None = None,
    success: bool = True,
    timed_out: bool = False,
    cost: float = 10.0,
    start: tuple[int, int] = (0, 0),
    goal: tuple[int, int] = (0, 10),
    height: int = 16,
    width: int = 16,
    obstacle_count: int = 0,
    seed: int = 1,
    map_hash: str | None = None,
    generator_kind: str = "open",
) -> dict:
    return {
        "experiment": experiment,
        "algorithm": algorithm,
        "seed": seed,
        "query_index": query_index,
        "generator_kind": generator_kind,
        "height": height,
        "width": width,
        "obstacle_density": obstacle_count / (height * width),
        "obstacle_count": obstacle_count,
        "map_hash": map_hash or f"h{query_index}-{obstacle_count}",
        "start_row": start[0],
        "start_col": start[1],
        "goal_row": goal[0],
        "goal_col": goal[1],
        "success": success,
        "termination_reason": "timeout" if timed_out else "goal_found",
        "solution_cost": cost,
        "runtime_sec": 0.01,
        "generated": generated if generated is not None else expanded,
        "expanded": expanded,
        "expanded_unit": "state" if algorithm == "astar" else "pair",
        "forward_expanded": None if algorithm == "astar" else expanded,
        "backward_expanded": None if algorithm == "astar" else 0,
        "meeting_g_F": None if algorithm == "astar" else cost,
        "meeting_g_B": None if algorithm == "astar" else 0.0,
        "direction_switches": None if algorithm == "astar" else 0,
        "heuristic_evals": expanded,
        "heuristic_time_sec": 0.001,
        "peak_open": 2,
        "peak_closed": expanded,
        "timed_out": timed_out,
    }


def _triple(
    query_index: int,
    f2f: int,
    f2e: int,
    *,
    astar_cost: float | None = None,
    sfbds_cost: float | None = None,
    **kwargs,
) -> list[dict]:
    cost = kwargs.pop("cost", 10.0)
    ac = cost if astar_cost is None else astar_cost
    sc = cost if sfbds_cost is None else sfbds_cost
    return [
        _raw(algorithm="astar", query_index=query_index, expanded=f2e, cost=ac, **kwargs),
        _raw(algorithm="sfbds_f2f", query_index=query_index, expanded=f2f, cost=sc, **kwargs),
        _raw(algorithm="sfbds_f2e", query_index=query_index, expanded=f2e, cost=sc, **kwargs),
    ]


def test_pair_three_queries() -> None:
    raw = []
    for i in range(3):
        raw.extend(_triple(i, f2f=10, f2e=12))
    paired = pair_rows(raw)
    assert len(paired) == 3
    assert paired[0]["expansion_diff"] == 2
    assert paired[0]["astar_expanded"] == 12
    assert "astar_expanded" in paired[0]
    assert paired[0]["expansion_saving_pct"] == pytest.approx(100.0 * 2 / 12)


def test_pair_nested_densities_are_separate_rows() -> None:
    raw = []
    for q in range(3):
        for count in (10, 20, 30):
            raw.extend(
                _triple(
                    q,
                    f2f=5,
                    f2e=8,
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                )
            )
    paired = pair_rows(raw)
    assert len(paired) == 9
    fids = {r["family_id"] for r in paired}
    assert len(fids) == 3
    pids = {r["pair_id"] for r in paired}
    assert len(pids) == 9


def test_detour_uses_astar_cost_and_zero_manhattan() -> None:
    raw = _triple(
        0,
        f2f=4,
        f2e=4,
        astar_cost=20.0,
        sfbds_cost=10.0,
        start=(0, 0),
        goal=(0, 10),
    )
    paired = pair_rows(raw)
    assert paired[0]["manhattan_distance"] == 10
    assert paired[0]["astar_solution_cost"] == 20.0
    assert paired[0]["detour_ratio"] == pytest.approx(2.0)
    assert detour_ratio(0.0, 0) == 1.0
    assert detour_ratio(3.0, 0) is None


def test_zero_f2e_expanded_null_ratios() -> None:
    raw = _triple(0, f2f=0, f2e=0)
    paired = pair_rows(raw)
    assert paired[0]["expansion_ratio"] is None
    assert paired[0]["expansion_saving_pct"] is None


def test_timeout_excluded_from_win_and_means() -> None:
    raw = _triple(0, f2f=1, f2e=10)
    raw.extend(
        _triple(1, f2f=999, f2e=1, timed_out=True, success=False)
    )
    # timeout rows still have huge expanded; must not enter saving mean
    paired = pair_rows(raw)
    assert len(paired) == 2
    assert paired[1]["solved"] is False
    assert paired[1]["expansion_diff"] is None
    summary = summarize(paired)
    family = next(r for r in summary if r["group_type"] == "map_family")
    assert family["n_solved"] == 1
    assert family["n_timeout"] == 1
    assert family["n_f2f_fewer"] == 1
    assert family["mean_expansion_saving_pct"] == pytest.approx(90.0)


def test_paired_xy_does_not_shift_on_null_y() -> None:
    from sfbds_compare.analysis.plots import paired_xy

    rows = [
        {"detour_ratio": 1.0, "expansion_saving_pct": None},
        {"detour_ratio": 2.0, "expansion_saving_pct": 50.0},
    ]
    xs, ys = paired_xy(rows, "detour_ratio", "expansion_saving_pct")
    assert xs == [2.0]
    assert ys == [50.0]


def test_rank_biserial_all_positive() -> None:
    assert rank_biserial([1.0, 2.0, 3.0]) == pytest.approx(1.0)
    assert rank_biserial([0.0, 0.0]) is None


def test_wilcoxon_uses_exact_for_n12(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("scipy")

    class _Res:
        statistic = 0.0
        pvalue = 0.01

    captured: dict = {}

    def fake_wilcoxon(untied, **kwargs):  # type: ignore[no-untyped-def]
        captured.update(kwargs)
        return _Res()

    monkeypatch.setattr("scipy.stats.wilcoxon", fake_wilcoxon)
    diffs = [float(i) for i in range(1, 13)]
    wilcoxon_signed_rank(diffs)
    assert captured.get("method") == "exact"
    assert rank_biserial([1.0, 2.0, 3.0]) == pytest.approx(1.0)
    assert rank_biserial([0.0, 0.0]) is None


def test_holm_two_values() -> None:
    adj = holm_adjust([0.04, 0.01])
    assert adj[1] == pytest.approx(0.02)
    assert adj[0] == pytest.approx(0.04)


def test_n_untied_below_ten_null_p() -> None:
    diffs = [1.0] * 9
    stat, p, note = wilcoxon_signed_rank(diffs)
    assert stat is None and p is None
    assert "n_untied" in note


def test_wilcoxon_and_sign_when_f2f_smaller() -> None:
    scipy = pytest.importorskip("scipy")
    del scipy
    diffs = [float(i) for i in range(1, 13)]
    _stat, p, note = wilcoxon_signed_rank(diffs)
    assert note == ""
    assert p is not None and p < 0.05
    sp, snote = sign_test_p(diffs)
    assert snote == ""
    assert sp is not None and sp < 0.05


def test_all_ties_null_p() -> None:
    _stat, p, note = wilcoxon_signed_rank([0.0] * 20)
    assert p is None
    assert "n_untied=0" in note


def test_random_nested_not_stacked_in_map_family_test() -> None:
    raw = []
    for q in range(12):
        for count in (10, 20, 30):
            raw.extend(
                _triple(
                    q,
                    f2f=1,
                    f2e=2,
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                    seed=7,
                )
            )
    paired = pair_rows(raw)
    assert len(paired) == 36
    summary = summarize(paired)
    family = next(
        r for r in summary if r["group_type"] == "map_family" and r["group"] == "random"
    )
    assert family["n_solved"] == 36
    assert family["n_test"] == 12
    assert family["wilcoxon_p_raw"] is None
    assert "skipped on pooled nested random" in family["note"]
    overall = next(r for r in summary if r["group_type"] == "overall_random")
    assert overall["n_solved"] == 36
    assert overall["n_test"] == 12
    assert overall["n_untied"] == 12
    dens = [r for r in summary if r["group_type"] == "obstacle_count"]
    assert len(dens) == 3
    assert all(r["n_solved"] == 12 for r in dens)
    assert all(r["n_test"] == 12 for r in dens)


def test_cli_no_plots(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = []
    for rec in _triple(0, f2f=3, f2e=5):
        rows.append(rec)
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert main(["--input-dir", str(tmp_path), "--out-dir", str(out), "--no-plots"]) == 0
    assert (out / "paired.csv").is_file()
    assert (out / "summary.csv").is_file()
    assert (out / "stats.csv").is_file()
    assert list(out.glob("*.png")) == []
