"""Paired Wilcoxon, sign test, rank-biserial, and Holm adjustment."""

from __future__ import annotations

from statistics import median
from typing import Optional, Sequence

_MIN_UNTIED = 10


def average_ranks(values: Sequence[float]) -> list[float]:
    """1-based average ranks (ties share the mean rank)."""

    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def rank_biserial(diffs: Sequence[float]) -> Optional[float]:
    """Matched-pairs rank-biserial; positive means F2F fewer expansions."""

    untied = [float(d) for d in diffs if d != 0]
    n = len(untied)
    if n == 0:
        return None
    ranks = average_ranks([abs(d) for d in untied])
    t_plus = sum(r for r, d in zip(ranks, untied) if d > 0)
    t_minus = sum(r for r, d in zip(ranks, untied) if d < 0)
    denom = n * (n + 1) / 2.0
    return (t_plus - t_minus) / denom


def holm_adjust(p_raw: Sequence[Optional[float]]) -> list[Optional[float]]:
    indexed = [(i, p) for i, p in enumerate(p_raw) if p is not None]
    m = len(indexed)
    out: list[Optional[float]] = [None] * len(p_raw)
    if m == 0:
        return out
    indexed.sort(key=lambda t: t[1])
    running = 0.0
    for rank, (i, p) in enumerate(indexed):
        val = min(1.0, (m - rank) * p)
        running = max(running, val)
        out[i] = running
    return out


def collapse_random_diffs(rows: Sequence[dict]) -> list[float]:
    """Median expansion_diff per family_id for random rows; others unchanged.

    Nested densities of the same query must not be stacked as independent n.
    """

    from collections import defaultdict

    rest: list[float] = []
    by_family: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        diff = row.get("expansion_diff")
        if diff is None or not row.get("solved"):
            continue
        if row.get("map_family") == "random":
            by_family[row["family_id"]].append(float(diff))
        else:
            rest.append(float(diff))
    collapsed = [median(vals) for vals in by_family.values()]
    return rest + collapsed


def expansion_win_counts(diffs: Sequence[float]) -> tuple[int, int, int]:
    """Return (f2f_fewer, f2e_fewer, ties) from expansion_diff values."""

    n_f2f = sum(1 for d in diffs if d > 0)
    n_f2e = sum(1 for d in diffs if d < 0)
    n_tie = sum(1 for d in diffs if d == 0)
    return n_f2f, n_f2e, n_tie


def wilcoxon_signed_rank(
    diffs: Sequence[float],
) -> tuple[Optional[float], Optional[float], str]:
    """Two-sided Wilcoxon on expansion_diff. Null p if n_untied < 10."""

    untied = [float(d) for d in diffs if d != 0]
    n_untied = len(untied)
    if n_untied < _MIN_UNTIED:
        return None, None, f"n_untied={n_untied} < {_MIN_UNTIED}"
    try:
        from scipy.stats import wilcoxon
    except ImportError:
        return None, None, "scipy not installed"
    method = "exact" if n_untied <= 25 else "auto"
    try:
        result = wilcoxon(
            untied,
            zero_method="wilcox",
            alternative="two-sided",
            method=method,
        )
    except TypeError:
        result = wilcoxon(
            untied,
            zero_method="wilcox",
            alternative="two-sided",
        )
    return float(result.statistic), float(result.pvalue), ""


def sign_test_p(diffs: Sequence[float]) -> tuple[Optional[float], str]:
    """Two-sided exact binomial on F2F-fewer vs F2E-fewer (ties dropped)."""

    n_f2f, n_f2e, _n_tie = expansion_win_counts(diffs)
    n = n_f2f + n_f2e
    if n < _MIN_UNTIED:
        return None, f"n_untied={n} < {_MIN_UNTIED}"
    try:
        from scipy.stats import binomtest
    except ImportError:
        return None, "scipy not installed"
    result = binomtest(n_f2f, n=n, p=0.5, alternative="two-sided")
    return float(result.pvalue), ""
