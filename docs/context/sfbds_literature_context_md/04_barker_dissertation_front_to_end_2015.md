# Front-To-End Bidirectional Heuristic Search

**Bibliographic record:** Joseph Kelly Barker (2015), UCLA PhD dissertation; advisor Richard E. Korf.  
**Source:** https://escholarship.org/uc/item/5j34j5bj

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Scope

This dissertation provides a substantially broader treatment of front-to-end bidirectional heuristic search than the shorter AAAI paper. It develops historical background, formal definitions, explanatory theory, extensive experiments, counterexamples, and domain-specific solvers.

# Main thesis

Most F2E bidirectional heuristic-search algorithms are generally outperformed by either:

- unidirectional heuristic search; or
- bidirectional brute-force search.

The dissertation argues that these techniques tend to remove overlapping portions of the search space.

# Conceptual decomposition

The reasoning is developed in stages:

1. Explain how bidirectional brute force prevents expansion of nodes with high \(g\)-cost by meeting before either side reaches full solution depth.
2. Explain how unidirectional heuristic search also avoids many high-\(g\) nodes.
3. Show why adding a weak heuristic to bidirectional brute force often fails to reduce expansions meaningfully.
4. Show why, with a strong heuristic, unidirectional heuristic search becomes the stronger component and the bidirectional organization can add overhead.

# Search methods discussed

The dissertation places F2E BiHS in a larger family including:

- Dijkstra / uniform-cost search;
- A*;
- bidirectional breadth-first or uniform-cost search;
- BHPA;
- BS*;
- bidirectional iterative-deepening methods;
- disk-based search;
- pattern-database heuristic search.

# Formal issues

Important concerns include:

- forward and reverse operators;
- invertibility;
- additive and unit edge costs;
- admissibility;
- frontier intersection;
- incumbent solution cost;
- lower bounds for stopping;
- duplicate detection across directions;
- criteria for proving optimality.

# Meeting behavior

The dissertation analyzes where and when the searches meet. It challenges simplistic claims that poor BiHS performance is caused merely by frontiers missing one another or by meeting too early.

The key issue is the structure of the expanded region, not only the geometric meeting point.

# Counterexamples and exceptions

The author gives:

- a graph in which bidirectional heuristic search is genuinely superior;
- road-network cases showing that blanket impossibility claims are false;
- domains where bidirectional brute force is preferable;
- a peg-solitaire application using a bidirectional method with specially designed heuristics.

# Four-peg Towers of Hanoi

A major empirical case study considers arbitrary start and goal configurations. Pattern databases provide strong unidirectional heuristics, yet bidirectional brute-force methods can still perform better under the tested conditions.

This demonstrates that heuristic strength alone does not determine the winner; domain topology and the distribution of states by distance also matter.

# Peg solitaire

The dissertation develops a specialized bidirectional solver for peg solitaire. This part is important because it shows that a generally weak paradigm can still succeed when a domain has structural properties and heuristics tailored to the bidirectional formulation.

# Road navigation

Road-network examples are used to show cases in which bidirectional heuristic search can provide value. These examples prevent the theory from being interpreted as an unconditional theorem.

# Lessons for literature review

The dissertation supports a nuanced statement:

> F2E bidirectional heuristic search is generally ineffective on many standard heuristic-search benchmarks because its benefits overlap with those of unidirectional heuristic search, but domain structure can produce important exceptions.

# Relevance to the project

The current project should use this dissertation to justify:

- comparison over multiple map types;
- analysis by heuristic strength;
- analysis by obstacle density and corridor structure;
- inclusion of both search effort and runtime;
- avoidance of universal claims from a narrow benchmark.

# Recommended variables

- solution depth or optimal cost;
- forward/backward branching asymmetry;
- heuristic error;
- number of states with \(f<C^*\);
- meeting position;
- time of first optimal incumbent;
- time spent after first optimal incumbent;
- frontier sizes;
- number of cross-direction duplicate matches.

# Cursor context summary

This dissertation is the comprehensive source behind the 2015 limitations argument. Use it for history, motivation, exceptions, experimental design, and cautious wording. Do not reduce its thesis to “bidirectional heuristic search never works.”
