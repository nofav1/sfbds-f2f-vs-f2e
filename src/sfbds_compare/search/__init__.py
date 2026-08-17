"""Search algorithms and result types.

``SFBDSSearcher`` / ``AStarSearcher`` are lazy exports so policy modules can
import ``nodes`` without a circular import through the searcher.
"""

from sfbds_compare.search.nodes import AStarNode, SFBDSNode, reconstruct_sfbds_path
from sfbds_compare.search.result import SearchResult, TerminationReason

__all__ = [
    "AStarNode",
    "AStarSearcher",
    "SFBDSNode",
    "SFBDSSearcher",
    "official_f2e_searcher",
    "reconstruct_sfbds_path",
    "SearchResult",
    "TerminationReason",
]


def __getattr__(name: str):
    if name == "SFBDSSearcher":
        from sfbds_compare.search.sfbds import SFBDSSearcher

        return SFBDSSearcher
    if name == "official_f2e_searcher":
        from sfbds_compare.search.sfbds import official_f2e_searcher

        return official_f2e_searcher
    if name == "AStarSearcher":
        from sfbds_compare.search.astar import AStarSearcher

        return AStarSearcher
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
