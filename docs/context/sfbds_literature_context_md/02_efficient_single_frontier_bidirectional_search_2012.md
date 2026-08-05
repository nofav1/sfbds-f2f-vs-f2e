# Efficient Single Frontier Bidirectional Search

**Bibliographic record:** Marco Lippi, Marco Ernandes, Ariel Felner (2012; archive page republished 2021), SoCS.  
**Source:** https://ojs.aaai.org/index.php/SOCS/article/view/18248

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Purpose

This paper improves the original single-frontier framework. It calls the basic framework **SBS** and introduces an enhanced version, **eSBS**, using pruning and caching. It also proposes a hybrid between eSBS and IDA* to reduce memory.

# Starting point: SBS/SFBDS

In SBS, every search node contains a pair of states, one associated with each search direction. The pair represents an independent shortest-path subproblem.

The original framework naturally supports a front-to-front estimate because the two endpoint states are explicitly available:

\[
h_{\text{pair}}(u,v)
\]

The main difficulty is that the paired search tree can repeat equivalent subproblems and can consume substantial time and memory.

# Main contributions

## 1. Enhanced SBS (eSBS)

eSBS applies:

- pruning rules;
- caching of solved or partially solved subproblems;
- avoidance of redundant paired-state work;
- tighter handling of repeated pair configurations.

The intended effects are:

- fewer pair nodes generated;
- fewer pair nodes expanded;
- lower memory consumption;
- reuse of prior shortest-path information.

## 2. Hybrid eSBS and IDA*

The paper also combines eSBS ideas with iterative deepening. The hybrid is motivated by the contrast between:

- A*: strong duplicate detection, but high memory;
- IDA*: linear memory, but repeated iterations and many duplicate paths;
- eSBS: paired-state pruning and reusable information.

The hybrid is described as potentially using approximately the square root of the memory required by A* in favorable settings while pruning many nodes that a plain IDA* search would visit.

# Caching logic

A paired subproblem can recur through different sequences of forward and backward choices. Caching allows the algorithm to recognize that a distance or bound for a pair has already been computed.

Possible cache entries include:

- exact distance between a pair of states;
- lower or upper bounds;
- failure under a threshold;
- best-known continuation;
- direction choice statistics.

The cache must be keyed by a canonical representation of the pair.

# Pruning logic

Pruning removes pair nodes that cannot lead to an improved solution. Depending on the specific algorithm variant, useful conditions may include:

- current accumulated cost plus pair heuristic exceeds the incumbent;
- a cached result dominates the current pair;
- the same pair was previously reached with lower cost;
- path constraints make the partial solution infeasible;
- an iterative-deepening threshold is exceeded.

# Memory trade-off

The paper emphasizes that SFBDS is not automatically memory efficient merely because it has one frontier. A paired-state OPEN and cache can still grow rapidly.

The hybrid design treats memory as a tunable resource:

- more caching reduces repeated work but consumes memory;
- less caching approaches IDA*-like behavior;
- partial retention can provide an intermediate point.

# Experimental methodology

The algorithms are evaluated over several search domains. The reported comparison focuses on:

- runtime;
- memory;
- generated and expanded nodes;
- effectiveness of pruning;
- effectiveness of caching;
- comparison against A*, IDA*, and original SBS.

The reported results support the claim that pruning and caching substantially improve the original SBS framework.

# Project relevance

This paper is directly relevant for implementation quality. A naive SFBDS implementation can make F2F appear worse simply because it repeats pairwise computations unnecessarily.

For a fair F2F versus F2E experiment:

- both variants should use the same caching policy;
- both variants should use identical duplicate detection;
- heuristic caches should be measured separately;
- the cost of cache lookup must be included in runtime;
- cache hit rates should be reported;
- memory should include both OPEN/CLOSED and caches.

# Suggested metrics inspired by the paper

- number of unique pairs generated;
- total pair generations;
- duplicate pair ratio;
- cache hits and misses;
- exact-distance cache hits;
- heuristic cache hits;
- peak OPEN size;
- peak CLOSED size;
- peak cache entries;
- total memory estimate;
- expansions by forward versus backward direction.

# Threats to validity

- Caching can favor one heuristic if its values repeat more often.
- Different domains may have radically different pair redundancy.
- Python dictionary overhead can dominate small instances.
- An IDA* hybrid should not be compared directly to best-first variants without clearly separating memory and runtime objectives.
- Exact cache policies must be documented for reproducibility.

# Cursor context summary

- **eSBS = SBS + pruning + caching.**
- Repeated paired subproblems are a major efficiency issue.
- Memory usage must include all search and cache structures.
- The F2F/F2E comparison should not confound heuristic choice with different caching behavior.
