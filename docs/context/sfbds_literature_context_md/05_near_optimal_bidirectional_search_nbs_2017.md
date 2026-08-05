# Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions

**Bibliographic record:** Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant (2017), IJCAI.  
**Source:** https://www.ijcai.org/proceedings/2017/0069.pdf

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Main contribution

The paper introduces **Near-Optimal Bidirectional Search (NBS)** and gives a theoretical bound on its node expansions for front-to-end bidirectional search with consistent heuristics.

# Surely expanded pairs

For unidirectional A*, every state with:

\[
f(n)<C^*
\]

must be expanded under the relevant assumptions.

In bidirectional search there is no single state that must always be expanded, because the algorithm can choose either direction. Instead, theory identifies **pairs** \((u,v)\) for which at least one endpoint must be expanded.

For an optimal forward path \(U\) and backward path \(V\), define:

\[
lb(U,V)=\max\{f_F(U),f_B(V),c(U)+c(V)\}
\]

If:

\[
lb(U,V)<C^*
\]

then any admissible black-box F2E bidirectional algorithm must expand either the forward endpoint or the backward endpoint.

# Must-Expand Graph

The paper constructs a bipartite graph \(GMX(I)\):

- left vertices represent states in the forward direction;
- right vertices represent states in the backward direction;
- an edge connects \(u_F\) and \(v_B\) when \((u,v)\) is a surely expanded pair.

Any valid algorithm's expansion set must cover every edge. Therefore, the expansions correspond to a **vertex cover** of the must-expand graph.

The size of a minimum vertex cover, \(VC(I)\), is a lower bound on the number of expansions required by any admissible algorithm in the considered class.

# NBS algorithm

NBS adapts a greedy two-approximation idea for vertex cover.

At each iteration:

1. Consider candidate forward/backward pairs.
2. Compute the smallest pair lower bound.
3. Stop if this lower bound is at least the incumbent cost.
4. Select a pair attaining the minimum bound.
5. Expand both selected endpoints.
6. Update the incumbent when the searches connect.

# Theoretical guarantee

For consistent heuristics, NBS performs no more than:

\[
2VC(I)
\]

expansions to cover all surely expanded pairs.

The paper also proves that no admissible F2E algorithm can guarantee a better worst-case factor than 2 in the framework considered.

Thus, NBS is:

- within a factor of two of the per-instance lower bound;
- worst-case optimal with respect to this factor.

# Duplicate handling

The expansion routine:

- moves the selected path from OPEN to CLOSED;
- generates successors or predecessors;
- checks for a matching state in the opposite OPEN;
- updates incumbent solution cost;
- discards a generated path if an equal endpoint already has a cheaper path;
- replaces a worse duplicate when appropriate.

# Efficient implementation

Explicitly constructing the full Cartesian product of OPEN lists is too expensive. The practical implementation organizes paths into priority structures so that the minimum relevant pair can be selected without materializing all pairs.

This point is highly relevant to any F2F implementation: a mathematically pair-based rule can be computationally infeasible if implemented literally.

# Experiments

The paper compares NBS with existing BiHS methods and A* on standard domains. The key findings reported are:

- NBS is competitive with or better than prior bidirectional algorithms;
- it often outperforms A*;
- its advantage is strongest with weak heuristics or difficult instances;
- expansions with lower bound equal to \(C^*\) can still affect results beyond the strict must-expand lower bound.

# Relevance to F2F versus F2E

NBS represents the modern theoretical strength of the F2E side. Comparing F2F only against an outdated F2E baseline would understate what F2E can achieve.

The current project can use NBS in two ways:

- as related work showing that F2E has strong expansion guarantees;
- as an optional baseline if implementation scope permits.

# Important distinction

NBS optimizes node expansion relative to the must-expand theory. It does not guarantee minimum runtime.

Runtime also depends on:

- pair-selection data structures;
- heuristic evaluation;
- duplicate detection;
- memory locality;
- implementation language.

# Cursor context summary

- Must-expand pairs replace must-expand individual states.
- \(GMX\) is bipartite.
- Minimum vertex cover is an expansion lower bound.
- NBS expands at most \(2VC\) under consistency.
- The theoretical comparison concerns expansions, not necessarily wall-clock time.
