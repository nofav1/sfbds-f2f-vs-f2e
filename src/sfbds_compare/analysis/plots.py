"""Report plots for paired F2F vs F2E analysis."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Sequence

from sfbds_compare.analysis.summarize import expansion_test_rows, nested_density_group_key


def paired_xy(
    rows: Sequence[dict[str, Any]], x_key: str, y_key: str
) -> tuple[list[Any], list[Any]]:
    """Scatter coordinates from the same filtered rows (no index truncation)."""

    pts = [
        (r[x_key], r[y_key])
        for r in rows
        if r.get(x_key) is not None and r.get(y_key) is not None
    ]
    return [p[0] for p in pts], [p[1] for p in pts]


def rows_for_plots(paired: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rows every plot series is built from (cost-clean solved pairs)."""

    return expansion_test_rows(paired)


def write_plots(paired: Sequence[dict[str, Any]], out_dir: str | Path) -> list[Path]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plots", file=sys.stderr)
        return []

    root = Path(out_dir)
    root.mkdir(parents=True, exist_ok=True)
    drawn = rows_for_plots(paired)
    written: list[Path] = []

    def save(fig, name: str) -> None:
        path = root / name
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        written.append(path)

    fig, ax = plt.subplots()
    x = [r["f2e_expanded"] for r in drawn]
    y = [r["f2f_expanded"] for r in drawn]
    ax.scatter(x, y, s=18, alpha=0.7)
    if x and y:
        hi = max(max(x), max(y))
        ax.plot([0, hi], [0, hi], color="black", linewidth=1)
    ax.set_xlabel("F2E pair expansions")
    ax.set_ylabel("F2F pair expansions")
    ax.set_title("F2F vs F2E pair expansions")
    save(fig, "expansions_scatter.png")

    fig, ax = plt.subplots()
    families = sorted({r["map_family"] for r in drawn})
    data = [
        [r["expansion_saving_pct"] for r in drawn if r["map_family"] == fam
         and r.get("expansion_saving_pct") is not None]
        for fam in families
    ]
    if any(data):
        try:
            ax.boxplot(data, tick_labels=families)
        except TypeError:
            ax.boxplot(data, labels=families)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Expansion saving %")
    ax.set_title("Expansion saving % by map family")
    save(fig, "saving_by_family.png")

    random_rows = [
        r for r in drawn if r["map_family"] == "random" and r.get("nested_density")
    ]

    keys = sorted(
        {nested_density_group_key(r) for r in random_rows} - {None},
        key=str,
    )
    fig, ax = plt.subplots()
    data = [
        [
            r["expansion_saving_pct"]
            for r in random_rows
            if nested_density_group_key(r) == key
            and r.get("expansion_saving_pct") is not None
        ]
        for key in keys
    ]
    labels = [str(k).replace("::", "\n") for k in keys]
    if any(data):
        try:
            ax.boxplot(data, tick_labels=labels)
        except TypeError:
            ax.boxplot(data, labels=labels)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("experiment / size / obstacle_count")
    ax.set_ylabel("Expansion saving %")
    ax.set_title("Expansion saving % by nested density group")
    save(fig, "saving_by_density.png")

    fig, ax = plt.subplots()
    xs, ys = paired_xy(drawn, "detour_ratio", "expansion_saving_pct")
    ax.scatter(xs, ys, s=18, alpha=0.7)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("detour_ratio")
    ax.set_ylabel("Expansion saving %")
    ax.set_title("Expansion saving % vs detour ratio")
    save(fig, "saving_vs_detour.png")

    fig, ax = plt.subplots()
    ratios = [r["runtime_ratio"] for r in drawn if r.get("runtime_ratio") is not None]
    if ratios:
        ax.hist(ratios, bins=min(20, max(5, len(ratios) // 3)))
    ax.axvline(1.0, color="black", linewidth=0.8)
    ax.set_xlabel("runtime_ratio (F2F / F2E)")
    ax.set_title("Runtime ratio")
    save(fig, "runtime_ratio.png")

    fig, ax = plt.subplots()
    fx, fy = paired_xy(drawn, "f2f_forward_expanded", "f2f_backward_expanded")
    ax.scatter(fx, fy, s=18, alpha=0.7, label="F2F")
    ex, ey = paired_xy(drawn, "f2e_forward_expanded", "f2e_backward_expanded")
    ax.scatter(ex, ey, s=18, alpha=0.7, label="F2E", marker="x")
    ax.set_xlabel("forward_expanded")
    ax.set_ylabel("backward_expanded")
    ax.set_title("Forward vs backward pair expansions")
    ax.legend()
    save(fig, "forward_backward.png")
    return written
