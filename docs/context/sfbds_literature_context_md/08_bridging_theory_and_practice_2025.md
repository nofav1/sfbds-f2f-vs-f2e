# Bridging Theory and Practice in Bidirectional Heuristic Search with Front-to-End Consistent Heuristics

**Bibliographic record:** Lior Siag, Shahaf S. Shperberg (2025), Artificial Intelligence 348, Article 104420.  
**Source:** https://www.sciencedirect.com/science/article/pii/S0004370225001390

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Scope

This journal paper extends the unifying approach to F2E bidirectional heuristic search. It connects must-expand-pair theory with practical algorithms that use lower bounds derived from consistent heuristics.

# Main objective

The paper asks how theoretical MEP information can be transformed into practical algorithm choices that work well across domains.

# Unified framework

Algorithms are described by combinations of:

- lower-bound components;
- node-pair or bucket selection;
- direction selection;
- expansion policy;
- termination test;
- assumptions about consistency.

Existing algorithms and newly generated variants can be expressed inside this shared framework.

# Consistency-aware bounds

Consistent heuristics offer stronger relationships between neighboring states and allow the search to maintain lower bounds unavailable in a purely admissible setting.

The paper reports that algorithms that fail to exploit consistency can perform substantially more expansions in some domains. The Towers of Hanoi results highlighted in the article description indicate differences on the order of roughly 1.8 to 5 times in certain comparisons.

# Theory-to-practice gap

The most theoretically informative bound is not necessarily the fastest. Practical performance depends on:

- frequency with which the bound changes decisions;
- cost of maintaining the bound;
- number and shape of search buckets;
- tie-breaking;
- memory overhead;
- domain-specific distributions of \(g\), \(h\), and optimal cost.

# Learning efficient bound combinations

A further contribution is a method for selecting or learning useful bounds from a subset of training instances and applying the learned choice to new instances in the same domain.

This turns algorithm configuration into an empirical selection problem.

# Relevance to the project

The paper provides a warning against presenting F2E as inherently primitive. Modern F2E search can use sophisticated cross-direction lower bounds and carefully designed stopping rules.

The current project should define its scope accurately:

> The project compares F2F and F2E heuristic guidance within a fixed SFBDS implementation, rather than claiming to compare F2F against every state-of-the-art F2E BiHS algorithm.

# Potential project extension

If time permits, the project could train or tune a small set of evaluation variants on development maps:

- F2E baseline;
- F2E with an added pair lower bound;
- F2F;
- max or hybrid combination.

The final test set must remain separate to avoid overfitting.

# Metrics

- expansions;
- generations;
- runtime;
- lower-bound update count;
- time spent updating bounds;
- number of termination checks;
- size of priority structures;
- generalization from development to test instances.

# Cursor context summary

This is a modern reference for the strongest F2E viewpoint. It connects MEP theory, consistency-derived bounds, practical algorithm design, and data-driven selection of bounds.
