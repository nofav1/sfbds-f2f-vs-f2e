# Comparing Front-to-Front and Front-to-End Heuristics in Bidirectional Search

**Bibliographic record:** Lior Siag, Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant (2023), SoCS.  
**Source:** https://ojs.aaai.org/index.php/SOCS/article/view/27296

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Purpose

This short paper directly compares the information available to front-to-front and front-to-end heuristics. It is the most direct prior work for the current project.

# F2E definition

F2E heuristics estimate distance to fixed endpoints:

\[
h_F(u)\le d(u,goal)
\]

\[
h_B(v)\le d(start,v)
\]

These estimates can be computed independently for each state.

# F2F definition

F2F heuristics estimate distance between arbitrary state pairs:

\[
h(u,v)\le d(u,v)
\]

In a traditional two-frontier algorithm, an F2F estimate for a forward state may use the opposite OPEN list:

\[
\min_{v\in OPEN_B}\left(g_F(u)+h(u,v)+g_B(v)\right)
\]

This uses current information about both searches.

# Informativeness

The central theoretical idea is that F2F has access to more relevant information. It can estimate the remaining gap between the actual active frontiers rather than treating the opposite search as if it were still located only at the original endpoint.

The paper demonstrates that F2F can provide substantially stronger lower bounds and has major potential to reduce expansions.

# Main challenge

The stronger information is expensive.

For every state in one frontier, a direct F2F implementation may compare against every state in the opposite frontier. This creates pairwise overhead approaching:

\[
O(|OPEN_F|\cdot|OPEN_B|)
\]

over relevant updates, depending on the algorithm.

The paper therefore distinguishes:

- theoretical heuristic advantage;
- practical algorithmic efficiency.

# Experimental approach

The paper compares F2E and F2F behavior empirically on benchmark search problems. The central measured quantity is the potential reduction in search effort.

The result is that F2F can be much more informative and can greatly reduce the number of expanded states. This supports further research into algorithms that can exploit F2F without paying the full pairwise cost.

# Interpretation

The paper does not establish that naive F2F is a faster practical solver. It establishes that:

- there is valuable information unavailable to F2E;
- this information can strongly reduce expansions;
- the remaining research challenge is efficient use of that information.

# Direct connection to SFBDS

SFBDS nodes already consist of pairs \((u,v)\). Therefore, SFBDS may avoid some of the full frontier-to-frontier evaluation overhead:

\[
h_{\text{SFBDS}}(u,v)
\]

is one pairwise evaluation for the pair being considered.

However, SFBDS has its own overhead because it searches over pair states. The current project tests whether this trade-off is favorable.

# Research hypotheses derived from the paper

1. F2F should expand fewer nodes than F2E.
2. F2F may still be slower due to evaluation overhead.
3. The advantage should increase as F2E becomes less informative.
4. Difficult maps with multiple misleading routes may benefit more from F2F.
5. Easy open maps may favor the cheaper heuristic.

# Experimental fairness requirements

- same SFBDS implementation;
- same direction rule;
- same tie-breaking;
- same duplicate detection;
- same stopping condition;
- same maps and queries;
- separate counters for heuristic calls and search expansions;
- repeated timing runs;
- timeout and memory-limit reporting.

# Cursor context summary

This paper is the direct justification for the project. Its central message is: **F2F has large potential because it is more informative, but efficient realization is the unsolved practical challenge.**
