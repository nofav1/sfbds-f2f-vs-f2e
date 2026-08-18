"""Paper figures must pair git study *_opt.csv, not gitignored analysis paired.csv."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "paper_figures.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("paper_figures", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pf = _load_mod()


def test_script_does_not_open_analysis_paired_csv() -> None:
    text = _SCRIPT.read_text(encoding="utf-8")
    assert "family_summary.csv" in text
    assert "/paired.csv" not in text
    assert "\\paired.csv" not in text


def test_maze_win_counts_from_study_opt_csv() -> None:
    from sfbds_compare.analysis.load import load_raw_csvs
    from sfbds_compare.analysis.pair import pair_rows

    raw = [
        r
        for r in load_raw_csvs(pf.STUDY)
        if r["experiment"] in {pf.MAZE_127, pf.MAZE_255}
    ]
    paired = pair_rows(raw)
    n_f2f, n_f2e, n_tie, n = pf.win_counts(pf.experiment_rows(paired, pf.MAZE_127))
    assert (n_f2f, n_f2e, n_tie, n) == (22, 0, 8, 30)
    n_f2f, n_f2e, n_tie, n = pf.win_counts(pf.experiment_rows(paired, pf.MAZE_255))
    assert (n_f2f, n_f2e, n_tie, n) == (26, 0, 4, 30)
    pf.assert_maze_sanity(paired)


def test_nested_64_d30_and_timed_from_study_opt_csv() -> None:
    from sfbds_compare.analysis.load import load_raw_csvs
    from sfbds_compare.analysis.pair import pair_rows

    raw = [
        r
        for r in load_raw_csvs(pf.STUDY)
        if r["experiment"] in {pf.NESTED_64_D30, "study_maze_127_timed_opt"}
    ]
    paired = pair_rows(raw)
    n_f2f, n_f2e, n_tie, n = pf.win_counts(
        pf.experiment_rows(
            paired, pf.NESTED_64_D30, obstacle_count=pf.NESTED_64_D30_OBS
        )
    )
    assert (n_f2f, n_f2e, n_tie, n) == (13, 0, 17, 30)
    timed = pf.table_timed(paired)[0]
    assert timed["n_expansion_untied"] == 22
    assert timed["n_f2f_faster"] == 22
    assert abs(float(timed["median_runtime_ratio"]) - 0.885) < 0.001


def test_maze_instance_rows_are_not_nested_densities() -> None:
    from sfbds_compare.analysis.load import load_raw_csvs
    from sfbds_compare.analysis.pair import pair_rows

    raw = [
        r
        for r in load_raw_csvs(pf.STUDY)
        if r["experiment"] in {pf.MAZE_127, pf.NESTED_64_D30}
    ]
    matrix = {r["experiment"]: r for r in pf.table_instance_matrix(pair_rows(raw))}
    assert matrix[pf.MAZE_127]["n_densities"] == 1
    assert matrix[pf.NESTED_64_D30]["n_densities"] == 3


def test_refuse_out_dir_requires_force(tmp_path: Path) -> None:
    (tmp_path / "stub.txt").write_text("x", encoding="utf-8")
    assert pf.refuse_out_dir(tmp_path, force=False)
    assert pf.refuse_out_dir(tmp_path, force=True) is None
