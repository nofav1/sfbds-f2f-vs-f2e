"""Lock Option 3A premises: 30 pairs, rest >= 0, 0 F2E-fewer evals."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "eval_cost_sensitivity.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("eval_cost_sensitivity", _SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ecs = _load_mod()


def _row(*, evals: int, runtime: float = 0.1, h_time: float = 0.01) -> dict[str, str]:
    return {
        "heuristic_evals": str(evals),
        "runtime_sec": str(runtime),
        "heuristic_time_sec": str(h_time),
    }


@pytest.mark.parametrize("family, filename, obstacle_count", ecs.DATASETS)
def test_frozen_opt_families_have_no_f2e_fewer_evals(
    family: str, filename: str, obstacle_count: int | None
) -> None:
    path = ecs.STUDY / filename
    assert path.is_file(), f"missing {path}"
    pairs = ecs.load_pairs(path, obstacle_count)
    n_f2f, n_f2e, n_tie = ecs.check_family(family, pairs)
    assert n_f2f + n_f2e + n_tie == 30
    assert n_f2e == 0


def test_check_family_rejects_f2e_fewer_evals() -> None:
    pairs = [(_row(evals=10), _row(evals=9))] * 30
    with pytest.raises(ValueError, match="F2E-fewer"):
        ecs.check_family("toy", pairs)


def test_check_family_rejects_wrong_n() -> None:
    with pytest.raises(ValueError, match="expected 30"):
        ecs.check_family("toy", [(_row(evals=1), _row(evals=2))])


def test_check_only_does_not_write(capsys: pytest.CaptureFixture[str]) -> None:
    assert ecs.main(["--check-only"]) == 0
    out = capsys.readouterr().out
    assert "ok" in out
    assert "wrote" not in out


def test_main_refuses_nonempty_out_without_force(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "frozen"
    out.mkdir()
    stale = out / "sensitivity.csv"
    stale.write_text("stale", encoding="utf-8")
    monkeypatch.setattr(ecs, "OUT", out)
    assert ecs.main([]) == 1
    assert stale.read_text(encoding="utf-8") == "stale"


def test_main_force_allows_nonempty_out(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "frozen"
    out.mkdir()
    (out / "old.txt").write_text("x", encoding="utf-8")
    monkeypatch.setattr(ecs, "OUT", out)
    monkeypatch.setattr(ecs, "write_csv", lambda *args, **kwargs: None)
    monkeypatch.setattr(ecs, "write_figure", lambda *args, **kwargs: None)
    assert ecs.main(["--force"]) == 0
