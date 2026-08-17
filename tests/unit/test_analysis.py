"""Unit tests for paired F2F/F2E analysis."""

from __future__ import annotations

from pathlib import Path

import pytest

from sfbds_compare.analysis.load import load_raw_csvs
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
    f2f_cost: float | None = None,
    f2e_cost: float | None = None,
    **kwargs,
) -> list[dict]:
    cost = kwargs.pop("cost", 10.0)
    ac = cost if astar_cost is None else astar_cost
    sc = cost if sfbds_cost is None else sfbds_cost
    fc = sc if f2f_cost is None else f2f_cost
    ec = sc if f2e_cost is None else f2e_cost
    return [
        _raw(algorithm="astar", query_index=query_index, expanded=f2e, cost=ac, **kwargs),
        _raw(algorithm="sfbds_f2f", query_index=query_index, expanded=f2f, cost=fc, **kwargs),
        _raw(algorithm="sfbds_f2e", query_index=query_index, expanded=f2e, cost=ec, **kwargs),
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


def test_independent_random_csvs_skip_density_claims() -> None:
    raw = []
    for experiment, count, seed in (
        ("study_random_128_d10", 1638, 110),
        ("study_random_128_d20", 3277, 120),
        ("study_random_128_d30", 4915, 130),
    ):
        for q in range(12):
            raw.extend(
                _triple(
                    q,
                    f2f=1,
                    f2e=2,
                    experiment=experiment,
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                    seed=seed,
                )
            )
    paired = pair_rows(raw)
    assert len(paired) == 36
    assert all(r["nested_density"] is False for r in paired)
    summary = summarize(paired)
    assert [r for r in summary if r["group_type"] == "obstacle_count"] == []
    assert [r for r in summary if r["group_type"] == "overall_random"] == []
    family = next(
        r for r in summary if r["group_type"] == "map_family" and r["group"] == "random"
    )
    assert family["n_solved"] == 36
    assert family["n_test"] == 36
    assert family["n_f2f_fewer"] == 36
    assert family["wilcoxon_p_raw"] is not None


def test_mixed_independent_and_nested_density_claims_only_nested() -> None:
    raw = []
    for q in range(12):
        raw.extend(
            _triple(
                q,
                f2f=1,
                f2e=2,
                experiment="study_random_128_d10",
                obstacle_count=1638,
                generator_kind="random_obstacles",
                seed=110,
            )
        )
        for count in (1638, 3277, 4915):
            raw.extend(
                _triple(
                    q,
                    f2f=3,
                    f2e=4,
                    experiment="study_random_128",
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                    seed=110,
                )
            )
    paired = pair_rows(raw)
    nested = [r for r in paired if r["experiment"] == "study_random_128"]
    independent = [r for r in paired if r["experiment"] == "study_random_128_d10"]
    assert all(r["nested_density"] is True for r in nested)
    assert all(r["nested_density"] is False for r in independent)
    summary = summarize(paired)
    dens = [r for r in summary if r["group_type"] == "obstacle_count"]
    assert {r["group"] for r in dens} == {
        "study_random_128::16x16::1638",
        "study_random_128::16x16::3277",
        "study_random_128::16x16::4915",
    }
    assert all(r["n_solved"] == 12 for r in dens)
    overall = next(r for r in summary if r["group_type"] == "overall_random")
    assert overall["n_solved"] == 36
    assert overall["n_test"] == 12


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
    assert overall["n_f2f_fewer"] == 12
    dens = [r for r in summary if r["group_type"] == "obstacle_count"]
    assert len(dens) == 3
    assert all(r["n_solved"] == 12 for r in dens)
    assert all(r["n_test"] == 12 for r in dens)
    assert all(r["nested_density"] is True for r in paired)


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
    readme = (out / "README.md").read_text(encoding="utf-8")
    assert "generated" in readme.lower()
    assert "F2F vs F2E" in readme
    assert list(out.glob("*.png")) == []


def test_cli_experiment_filter(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = []
    for rec in _triple(0, f2f=3, f2e=5, experiment="keep_me"):
        rows.append(rec)
    for rec in _triple(0, f2f=1, f2e=2, experiment="drop_me"):
        rows.append(rec)
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(out),
                "--no-plots",
                "--experiment",
                "keep_me",
            ]
        )
        == 0
    )
    paired = (out / "paired.csv").read_text(encoding="utf-8")
    assert "keep_me" in paired
    assert "drop_me" not in paired


def test_cli_refuses_mixed_opt_and_prefix(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = []
    rows.extend(_triple(0, f2f=3, f2e=5, experiment="study_maze_127"))
    rows.extend(_triple(0, f2f=3, f2e=5, experiment="study_maze_127_opt"))
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert main(["--input-dir", str(tmp_path), "--out-dir", str(out), "--no-plots"]) == 1
    assert not (out / "paired.csv").is_file()


def test_cli_opt_experiment_filter_drops_prefix(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = []
    rows.extend(_triple(0, f2f=3, f2e=5, experiment="study_maze_127"))
    rows.extend(_triple(0, f2f=4, f2e=6, experiment="study_maze_255_opt"))
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(out),
                "--no-plots",
                "--experiment",
                "study_maze_255_opt",
                "--allow-opt-subset",
            ]
        )
        == 0
    )
    import csv

    with (out / "paired.csv").open(encoding="utf-8", newline="") as fh:
        experiments = {row["experiment"] for row in csv.DictReader(fh)}
    assert experiments == {"study_maze_255_opt"}
    readme = (out / "README.md").read_text(encoding="utf-8")
    assert "--experiment study_maze_255_opt" in readme
    assert "--allow-opt-subset" in readme
    assert "--experiment study_maze_127\n" not in readme


def test_cli_refuses_partial_official_opt_without_subset_flag(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = _triple(0, f2f=3, f2e=5, experiment="study_maze_127_opt")
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(out),
                "--no-plots",
                "--experiment",
                "study_maze_127_opt",
            ]
        )
        == 1
    )
    assert not (out / "paired.csv").is_file()


def test_cli_refuses_partial_official_opt_even_with_subset_flag(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = _triple(0, f2f=3, f2e=5, experiment="study_maze_127_opt")
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(out),
                "--no-plots",
                "--experiment",
                "study_maze_127_opt",
                "--allow-opt-subset",
            ]
        )
        == 1
    )
    assert not (out / "paired.csv").is_file()


def test_cli_refuses_official_opt_mixed_with_followup_even_with_subset_flag(
    tmp_path: Path,
) -> None:
    from sfbds_compare.analysis.__main__ import OFFICIAL_OPT_EXPERIMENTS, main

    rows = []
    for name in sorted(OFFICIAL_OPT_EXPERIMENTS):
        rows.extend(_triple(0, f2f=3, f2e=5, experiment=name))
    rows.extend(_triple(0, f2f=3, f2e=5, experiment="study_maze_255_opt"))
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    argv = ["--input-dir", str(tmp_path), "--out-dir", str(out), "--no-plots"]
    for name in sorted(OFFICIAL_OPT_EXPERIMENTS):
        argv.extend(["--experiment", name])
    argv.extend(["--experiment", "study_maze_255_opt", "--allow-opt-subset"])
    assert main(argv) == 1
    assert not (out / "paired.csv").is_file()


def test_cli_accepts_all_five_official_opt(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import OFFICIAL_OPT_EXPERIMENTS, main

    rows = []
    for name in sorted(OFFICIAL_OPT_EXPERIMENTS):
        rows.extend(_triple(0, f2f=3, f2e=5, experiment=name))
    write_csv(tmp_path / "raw.csv", rows)
    out = tmp_path / "analysis"
    argv = ["--input-dir", str(tmp_path), "--out-dir", str(out), "--no-plots"]
    for name in sorted(OFFICIAL_OPT_EXPERIMENTS):
        argv.extend(["--experiment", name])
    assert main(argv) == 0
    readme = (out / "README.md").read_text(encoding="utf-8")
    for name in OFFICIAL_OPT_EXPERIMENTS:
        assert f"--experiment {name}" in readme
    assert "--allow-opt-subset" not in readme


def test_render_readme_includes_experiment_flags() -> None:
    from sfbds_compare.analysis.report import render_readme

    paired = pair_rows(_triple(0, f2f=3, f2e=5, experiment="study_maze_127_opt"))
    names = (
        "study_corridor_512_opt",
        "study_maze_127_opt",
        "study_open_128_opt",
        "study_random_64_opt",
        "study_random_128_opt",
    )
    text = render_readme(
        paired,
        summarize(paired),
        input_dir="results/study/pair-bound",
        out_dir="results/analysis/pair-bound/2026-08-17-reopen-opt",
        experiments=names,
    )
    assert "--experiment study_maze_127_opt" in text
    assert "--out-dir results/analysis/pair-bound/2026-08-17-reopen-opt" in text
    assert "--allow-opt-subset" not in text
    assert "the CLI refuses a mix" not in text


def test_render_readme_includes_allow_opt_subset_flag() -> None:
    from sfbds_compare.analysis.report import render_readme

    paired = pair_rows(_triple(0, f2f=3, f2e=5, experiment="study_maze_255_opt"))
    text = render_readme(
        paired,
        summarize(paired),
        input_dir="results/study/pair-bound",
        out_dir="results/analysis/pair-bound/2026-08-17-harder-opt",
        experiments=("study_maze_255_opt",),
        allow_opt_subset=True,
    )
    assert "--experiment study_maze_255_opt" in text
    assert "--allow-opt-subset" in text


def test_readme_skips_density_claims_for_independent_random() -> None:
    from sfbds_compare.analysis.report import render_readme

    raw = []
    for q in range(12):
        raw.extend(
            _triple(
                q,
                f2f=1,
                f2e=2,
                experiment="study_random_128_d10",
                obstacle_count=1638,
                generator_kind="random_obstacles",
                seed=110,
            )
        )
    paired = pair_rows(raw)
    text = render_readme(paired, summarize(paired))
    assert "study_random_128_d10" in text
    assert "No nested-density experiments" in text
    assert "density-eligible" not in text.split("study_random_128_d10")[1][:80]


def test_readme_includes_nested_density_groups() -> None:
    from sfbds_compare.analysis.report import render_readme

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
    text = render_readme(paired, summarize(paired))
    assert "10 obstacles" in text
    assert "nested random families" in text
    assert "Wilcoxon is skipped on this pooled group" in text
    assert "independent files" not in text
    assert "collapses nested densities" in text
    assert "and from plots" in text


def test_cli_refuses_analysis_index_and_nonempty_slug(tmp_path: Path) -> None:
    from sfbds_compare.analysis.__main__ import main

    rows = _triple(0, f2f=3, f2e=5)
    write_csv(tmp_path / "raw.csv", rows)
    index = tmp_path / "results" / "analysis"
    index.mkdir(parents=True)
    (index / "README.md").write_text(
        "This directory is an **index of snapshots**.\n", encoding="utf-8"
    )
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(index),
                "--no-plots",
            ]
        )
        == 1
    )
    assert not (index / "paired.csv").exists()
    slug = tmp_path / "2026-08-14-slug"
    slug.mkdir()
    (slug / "stale.txt").write_text("x", encoding="utf-8")
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(slug),
                "--no-plots",
            ]
        )
        == 1
    )
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(slug),
                "--no-plots",
                "--force",
            ]
        )
        == 0
    )
    assert (slug / "paired.csv").is_file()
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(index),
                "--no-plots",
                "--force",
            ]
        )
        == 1
    )


def test_cli_hints_when_input_dir_has_formula_subdirs(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from sfbds_compare.analysis.__main__ import main

    (tmp_path / "legacy").mkdir()
    (tmp_path / "pair-bound").mkdir()
    out = tmp_path / "out"
    assert (
        main(
            [
                "--input-dir",
                str(tmp_path),
                "--out-dir",
                str(out),
                "--no-plots",
            ]
        )
        == 1
    )
    err = capsys.readouterr().err
    assert "non-recursive" in err
    assert "legacy" in err
    assert "pair-bound" in err
    assert not (out / "paired.csv").exists()


def test_density_groups_do_not_pool_experiments() -> None:
    raw = []
    for experiment, seed in (("study_a", 1), ("study_b", 2)):
        for q in range(12):
            for count in (7372, 7781, 8191):
                raw.extend(
                    _triple(
                        q,
                        f2f=1,
                        f2e=2,
                        experiment=experiment,
                        obstacle_count=count,
                        generator_kind="random_obstacles",
                        seed=seed,
                        height=128,
                        width=128,
                    )
                )
    paired = pair_rows(raw)
    summary = summarize(paired)
    dens = [r for r in summary if r["group_type"] == "obstacle_count"]
    assert len(dens) == 6
    assert all(r["n_solved"] == 12 for r in dens)
    groups = {r["group"] for r in dens}
    assert "study_a::128x128::7372" in groups
    assert "study_b::128x128::7372" in groups
    a_p = [r["wilcoxon_p_holm"] for r in dens if r["group"].startswith("study_a::")]
    b_p = [r["wilcoxon_p_holm"] for r in dens if r["group"].startswith("study_b::")]
    assert None not in a_p and None not in b_p
    assert len(a_p) == 3 and len(b_p) == 3
    overall = next(r for r in summary if r["group_type"] == "overall_random")
    assert overall["n_test"] == 24
    assert overall["n_f2f_fewer"] == 24
    assert overall["wilcoxon_p_raw"] is None
    assert "multiple nested experiments" in overall["note"]


def test_load_raw_csvs_skips_analysis_stems(tmp_path: Path) -> None:
    rows = _triple(0, f2f=3, f2e=5)
    write_csv(tmp_path / "study_open.csv", rows)
    (tmp_path / "paired.csv").write_text(
        "pair_id,family_id,experiment\nx,y,z\n", encoding="utf-8"
    )
    (tmp_path / "summary.csv").write_text(
        "group_type,group\nmap_family,maze\n", encoding="utf-8"
    )
    (tmp_path / "stats.csv").write_text(
        "group_type,group\nmap_family,maze\n", encoding="utf-8"
    )
    loaded = load_raw_csvs(tmp_path)
    assert len(loaded) == 3
    assert {r["algorithm"] for r in loaded} == {"astar", "sfbds_f2f", "sfbds_f2e"}


def test_cost_mismatch_includes_astar_disagreement() -> None:
    f2f_vs_f2e = pair_rows(
        _triple(0, f2f=3, f2e=9, f2f_cost=10.0, f2e_cost=12.0, astar_cost=10.0)
    )
    assert f2f_vs_f2e[0]["cost_mismatch"] is True
    both_vs_astar = pair_rows(
        _triple(1, f2f=3, f2e=9, astar_cost=10.0, sfbds_cost=12.0)
    )
    assert both_vs_astar[0]["cost_mismatch"] is True
    clean = pair_rows(_triple(2, f2f=3, f2e=9, cost=10.0))
    assert clean[0]["cost_mismatch"] is False


def test_cost_mismatch_rows_do_not_enter_n_untied() -> None:
    raw = []
    for q in range(13):
        mismatch = q < 4
        for count in (10, 20, 30):
            raw.extend(
                _triple(
                    q,
                    f2f=1,
                    f2e=100 if mismatch and count == 30 else 2,
                    f2e_cost=12.0 if mismatch and count == 30 else 10.0,
                    astar_cost=10.0,
                    f2f_cost=10.0,
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                    experiment="study_random_64",
                    height=64,
                    width=64,
                )
            )
    paired = pair_rows(raw)
    summary = summarize(paired)
    dens = next(
        r
        for r in summary
        if r["group_type"] == "obstacle_count"
        and r["group"] == "study_random_64::64x64::30"
    )
    assert dens["n_solved"] == 13
    assert dens["n_untied"] == 9
    assert dens["n_f2f_fewer"] == 9
    assert dens["wilcoxon_p_raw"] is None
    assert "excluded 4 cost_mismatch" in dens["note"]


def test_plots_omit_cost_mismatch_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pytest.importorskip("matplotlib")
    import matplotlib.axes

    from sfbds_compare.analysis.plots import rows_for_plots, write_plots

    raw = _triple(0, f2f=3, f2e=9, cost=10.0) + _triple(
        1,
        f2f=450,
        f2e=2881,
        f2f_cost=53.0,
        f2e_cost=57.0,
        astar_cost=53.0,
    )
    paired = pair_rows(raw)
    drawn = rows_for_plots(paired)
    assert [r["query_index"] for r in drawn] == [0]
    assert [r["f2e_expanded"] for r in drawn] == [9]

    captured: list[tuple[list[object], list[object]]] = []
    original = matplotlib.axes.Axes.scatter

    def spy(self, x, y, *args, **kwargs):  # type: ignore[no-untyped-def]
        captured.append((list(x), list(y)))
        return original(self, x, y, *args, **kwargs)

    monkeypatch.setattr(matplotlib.axes.Axes, "scatter", spy)
    written = write_plots(paired, tmp_path)
    assert written
    assert captured
    f2e_x, f2f_y = captured[0]
    assert [int(v) for v in f2e_x] == [9]
    assert [int(v) for v in f2f_y] == [3]
    for xs, ys in captured:
        assert 2881 not in {int(v) for v in xs}
        assert 450 not in {int(v) for v in ys}


def test_load_raw_csvs_is_not_recursive(tmp_path: Path) -> None:
    write_csv(tmp_path / "study_open.csv", _triple(0, f2f=3, f2e=5))
    nested = tmp_path / "legacy"
    nested.mkdir()
    write_csv(nested / "hidden.csv", _triple(9, f2f=1, f2e=2))
    loaded = load_raw_csvs(tmp_path)
    assert {r["query_index"] for r in loaded} == {0}
    assert len(loaded) == 3


def test_readme_mentions_independent_mix_only_when_present() -> None:
    from sfbds_compare.analysis.report import render_readme

    raw = []
    for q in range(12):
        raw.extend(
            _triple(
                q,
                f2f=1,
                f2e=2,
                experiment="study_random_128_d10",
                obstacle_count=1638,
                generator_kind="random_obstacles",
                seed=110,
            )
        )
        for count in (1638, 3277, 4915):
            raw.extend(
                _triple(
                    q,
                    f2f=3,
                    f2e=4,
                    experiment="study_random_128",
                    obstacle_count=count,
                    generator_kind="random_obstacles",
                    seed=110,
                )
            )
    text = render_readme(pair_rows(raw), summarize(pair_rows(raw)))
    assert "mixes nested and independent files" in text
