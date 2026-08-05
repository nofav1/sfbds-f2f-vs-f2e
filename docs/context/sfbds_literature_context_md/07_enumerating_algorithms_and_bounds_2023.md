# Front-to-End Bidirectional Heuristic Search with Consistent Heuristics: Enumerating and Evaluating Algorithms and Bounds

**Bibliographic record:** Lior Siag, Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant (2023), IJCAI.  
**Source:** https://www.ijcai.org/proceedings/2023/0625.pdf

> This file is a detailed, source-grounded research context note. It is a structured paraphrase and analysis, not a verbatim reproduction of the copyrighted paper. Verify equations, pseudocode details, numerical tables, and citation metadata against the original PDF before using them in the final report.

# Purpose

This paper unifies two lines of modern F2E bidirectional-search research:

- must-expand-pairs theory;
- practical lower bounds derived from consistent heuristics.

It shows how existing and new BiHS algorithms can be understood as choices over lower bounds, expansion rules, direction selection, and stopping conditions.

# Consistent front-to-end heuristics

For forward and backward directions, consistency provides triangle-inequality-like relations. This allows lower bounds to be updated and combined safely during search.

The standard quantities include:

\[
g_F(u),\quad h_F(u),\quad f_F(u)=g_F(u)+h_F(u)
\]

\[
g_B(v),\quad h_B(v),\quad f_B(v)=g_B(v)+h_B(v)
\]

# Pair lower bounds

A pair \((u,v)\) can be associated with multiple lower-bound components. The classic MEP expression includes:

\[
\max\{f_F(u),f_B(v),g_F(u)+g_B(v)\}
\]

The paper develops a larger family of valid bounds using consistency relationships and cross-direction information.

# MEP interpretation

A must-expand pair represents an unresolved possibility of an optimal path. At least one endpoint must be expanded to rule out or resolve that possibility.

Different algorithms can be viewed as different ways of selecting endpoints to cover these pairs.

# Algorithm enumeration

Instead of treating every named algorithm as unrelated, the paper describes an algorithm design space:

- which valid lower bounds are included;
- how the global lower bound is computed;
- which pair or bucket is selected;
- whether one or both directions are expanded;
- how ties are broken;
- what stopping test is used.

This creates both known and novel algorithm variants.

# Evaluation of bounds

A lower bound can be:

- theoretically valid but rarely decisive;
- expensive to maintain;
- redundant with stronger bounds;
- useful only on certain domains;
- especially helpful under consistent heuristics.

The experiments evaluate each bound by its marginal contribution to search efficiency.

# Main lesson

More valid bounds do not automatically produce a faster algorithm. A bound is useful only if the reduction in expansions or earlier stopping compensates for:

- update cost;
- priority-queue overhead;
- additional bookkeeping;
- cache or bucket complexity.

# Relationship to the current project

The project compares heuristic types, but an F2E implementation is not fully defined by the heuristic alone. Lower bounds and stopping conditions can strongly influence performance.

Therefore, the report must specify:

- exact F2E evaluation formula;
- exact global lower bound;
- exact termination condition;
- consistency assumptions;
- whether cross-direction bounds are enabled.

Otherwise, “F2E versus F2F” may accidentally compare two different algorithm frameworks rather than two heuristics.

# Recommended baseline strategy

For a limited course project:

1. Implement a minimal SFBDS framework.
2. Hold all non-heuristic logic fixed.
3. Compare a clearly documented F2E pair evaluation with F2F.
4. Treat advanced MEP-based algorithms as related work rather than reproduce the full enumeration.
5. Optionally add one stronger F2E lower-bound variant as an ablation.

# Cursor context summary

- Modern F2E BiHS is a family of algorithms, not one fixed method.
- MEP theory provides a unifying lens.
- Consistency enables additional safe bounds.
- Extra bounds must be evaluated by runtime as well as expansions.
- Exact stopping and lower-bound choices are required for reproducibility.
