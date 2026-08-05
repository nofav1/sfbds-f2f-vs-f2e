# Front-to-Attractors: Modifying the Front-to-Front Heuristic in Bidirectional Search

**Bibliographic record:** Alvin Zou, Muhammad Suhail Saleem, Maxim Likhachev (2026), arXiv preprint 2606.07047.  
**Source:** https://arxiv.org/abs/2606.07047

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Research problem

F2F heuristics are informative but expensive because a state may need to be compared with every state in the opposite frontier.

The paper proposes **Front-to-Attractors (F2A)** as an intermediate approach between F2E and full F2F.

# Definitions

## F2E

\[
f_D(s)=g_D(s)+h_D(s)
\]

where the heuristic estimates from the state to the fixed target of direction \(D\).

## F2F

\[
f_D(s)=g_D(s)+\min_{s'\in OPEN_{OD}}\left(h(s,s')+g_{OD}(s')\right)
\]

where \(OD\) denotes the opposite direction.

## F2A

Replace the full opposite frontier with a small active attractor set:

\[
f_D(s)=g_D(s)+\min_{a\in Attrs_{OD}}\left(h(s,a)+g_{OD}(a)\right)
\]

# Attractors

Attractors are a sparse set of representative ancestor states. Frontier states are assigned to attractors. Parent links among attractors provide a compact structure that can support path reconstruction.

F2A uses active attractors associated with states currently in OPEN rather than all states in the opposite frontier.

# Algorithm outline

At each iteration:

1. Choose a search direction, using the smaller OPEN list in the reported implementation.
2. Pop the minimum-\(f\) state, using higher \(g\) for tie-breaking.
3. Generate successors.
4. Compute each new heuristic against opposite active attractors.
5. Update the incumbent if a state is present in both directions.
6. Update attractor assignments.
7. Remove attractors with no associated frontier states.
8. Update the global lower bound and test termination.

# Optimality

The pairwise heuristic must satisfy the required bi-consistency condition.

The proof argues that every opposite frontier state has an attractor lying on its discovered least-cost path. Consistency ensures that replacing the frontier state with its attractor does not invalidate the lower-bound argument.

The paper concludes that the algorithm is complete and optimal under its assumptions.

# Practical issue: degeneration to F2E

If the original goal remains an attractor for the backward direction, then the minimum can be dominated by the goal-based estimate. F2A may then become no more informative than F2E.

# Optimizations

## New Attractor (NA)

Create a new attractor when the \(g\)-distance between a state and its attractor exceeds a threshold \(\delta\). This keeps attractors closer to the frontier.

## Associated States (AS)

When an attractor is too far from assigned frontier states, use selected associated frontier states instead of the attractor for heuristic computation.

These methods trade additional representatives for stronger heuristic values.

# Domains

The paper evaluates:

- 2D grid pathfinding;
- 15-puzzle;
- 14-pancake puzzle.

For grids, it includes DAO and maze benchmarks with 4-connected unit-cost movement and Manhattan distance.

# Algorithms compared

The experiment includes variants of:

- A*;
- F2E bidirectional methods;
- full F2F methods;
- F2A with no optimization;
- F2A-NA;
- F2A-AS;
- NBS-style variants.

# Reported results

The abstract reports:

- up to 11.2x fewer pairwise evaluations than full F2F;
- about 4.8x fewer node expansions than F2E on average.

The detailed results show that no one F2A variant dominates every domain. Full F2F can minimize expansions but incur enormous heuristic-evaluation counts. F2A seeks a middle ground.

# Key experimental lesson

There are at least three separate costs:

1. number of expanded states;
2. number of pairwise heuristic evaluations;
3. total runtime.

A project that measures only expansions can rank the algorithms incorrectly for practical use.

# Direct relevance

This paper is highly relevant to the current project because it:

- includes grid pathfinding;
- directly studies F2E/F2F cost;
- formalizes the pairwise evaluation overhead;
- provides a modern compromise method;
- confirms that heuristic informativeness and runtime must be reported separately.

# Possible future extension

After the core SFBDS F2F-versus-F2E comparison, a small representative-set heuristic could be added:

- fixed landmarks;
- frontier centroids;
- sampled pair endpoints;
- attractor-like representatives.

Such an extension requires a proof or clear qualification concerning optimality.

# Cursor context summary

F2A approximates the opposite frontier with active attractors. It is designed to preserve much of F2F's guidance while reducing pairwise work. It provides a strong recent framing for the exact trade-off studied in the project.
