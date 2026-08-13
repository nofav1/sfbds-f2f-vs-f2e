# SFBDS / F2F / F2E — Project Definition

**Course:** Search in Artificial Intelligence (237-2-5513), Ben-Gurion University  
**Document type:** Team project definition (Stages 1–6)  
**Status:** Definition revised (MVP cache/direction/stop gates) — **no implementation until instructor confirms scope**  
**Sources:** [Project instructions](context/Project_Instructions_context.md), [literature notes](context/sfbds_literature_context_md/), [lecture notes](context/presentations_summary/)

Context notes are paraphrases. Formal claims, formulas, and cited numbers in the final report must be verified against original PDFs ([literature README](context/sfbds_literature_context_md/README.md)). Domains and numeric claims in notes are marked verify-in-PDF unless checked in originals.

---

## Executive summary

**Primary project (Idea B):** Fix one SFBDS implementation and compare admissible **F2E** vs **F2F** heuristics while systematically varying a **shared eSBS-style pair/subproblem (bound/result) cache** and grid structure. Ask when F2F’s expansion savings overcome evaluation and bookkeeping cost, and whether that **pair-result cache** shifts the runtime crossover.

This is **not** a bare F2F-vs-F2E bake-off, and it is **not** an ablation of memoizing \(O(1)\) Manhattan. Lippi et al. 2012 motivate caching of **paired subproblem distances/bounds** (and related reuse), not cheap coordinate arithmetic. Under Manhattan-only grids, an \(h\)-memo cache cannot credibly drive a runtime flip; the primary ablation object is therefore the **pair/result cache**. A small **eval-cost multiplier** (Idea D light) stays in the MVP as a sensitivity check when natural \(h\) is cheap.

This addresses the open “efficient F2F / SFBDS trade-off” question (Siag et al. 2023 SoCS) using caching as a controlled variable, without claiming a new BiHS paradigm.

**Backup (Idea A):** Same SFBDS framework; emphasize density/corridor/distance crossover; add cache later if time. If the instructor rejects pair-cache as the “specific condition,” promote Idea A (or require expensive \(h\) / stronger cost-multiplier in MVP).

---

## Stage 1: Literature mapping

### Paper-by-paper map

**1. Moldenhauer et al. 2010 — Single-Frontier Bidirectional Search** ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md))
- **Problem:** Traditional BiHS coordination often fails to deliver ~d/2 depth reduction.
- **Method:** SFBDS — one OPEN of paired nodes \(N=(s_N,g_N)\); expand start-side → \((s',g)\) or goal-side → \((s,g')\); **local** direction decision on the pair.
- **Focus:** SFBDS, natural F2F \(h(s_N,g_N)\), direction selection; caching suggested for pairwise work.
- **Open:** Pair-state explosion; domain-dependent direction policy; F2F can cut expansions but raise runtime; separate heuristic cost from search overhead.

**2. Lippi et al. 2012 — Efficient Single Frontier Bidirectional Search** ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md))
- **Problem:** SBS/SFBDS repeats equivalent pairs; high time/memory.
- **Method:** eSBS = SBS + pruning + **caching of solved/partial pair subproblems** (distance/bound reuse) + tighter repeated-pair handling; hybrid eSBS+IDA* for memory.
- **Open:** Cache can favor one heuristic; document cache policy; do not confound F2F/F2E with unequal caching. Lippi supports “caching helps SBS” and fairness warnings — **not** a proven preferential F2F runtime rescue on grids.

**3. Barker & Korf 2015 AAAI — Limitations of F2E BiHS** ([`03`](context/sfbds_literature_context_md/03_limitations_front_to_end_2015.md))
- **Problem:** Why F2E BiHS often fails to stack bidirectional + heuristic benefits.
- **Theory:** Bi brute-force and uni-heuristic both eliminate high-\(g\) nodes → overlapping, not additive, savings. Not an impossibility theorem.
- **Open:** Limitation of F2E fixed-endpoint guidance → motivates F2F/SFBDS.

**4. Barker 2015 dissertation** ([`04`](context/sfbds_literature_context_md/04_barker_dissertation_front_to_end_2015.md))
- Broader F2E survey/experiments; domain topology matters; exceptions exist (roads, peg solitaire). Avoid universal “BiHS never works” claims.

**5. Chen et al. 2017 — NBS** ([`05`](context/sfbds_literature_context_md/05_near_optimal_bidirectional_search_nbs_2017.md))
- Near-optimal expansions for F2E BiHS with consistent heuristics (≤2·VC). Optimizes expansions ≠ minimum runtime. Optional strong F2E baseline only if time remains.

**6. Siag et al. 2023 SoCS — Comparing F2F and F2E** ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md))
- Most direct prior work for this topic. F2F can greatly reduce expansions; **does not** establish that naive F2F is faster. SFBDS connection: one pairwise eval per pair. Efficient F2F / SFBDS trade-off left open — **our project target**.

**7. Siag et al. 2023 IJCAI — Enumerating algorithms and bounds** ([`07`](context/sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md))
- Unify F2E via MEP + consistent-heuristic bounds. Unspecified F2E formula/stopping can make “F2E vs F2F” compare frameworks, not heuristics → **fix SFBDS mechanics** when comparing heuristics.

**8. Siag & Shperberg 2025 AIJ** ([`08`](context/sfbds_literature_context_md/08_bridging_theory_and_practice_2025.md))
- Theory–practice gap for F2E bounds. Comparing inside fixed SFBDS ≠ claiming vs all SOTA F2E BiHS.

**9. Shubi et al. 2026 — Longest paths / BiXDFBnB** ([`09`](context/sfbds_literature_context_md/09_bidirectional_longest_paths_f2f_2026.md))
- F2F natural in paired MAX search; expansions drop more reliably than wall-clock. Do **not** transfer MAX/DFBnB results directly to shortest-path grids.

**10. Zou et al. 2026 — Front-to-Attractors** ([`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md))
- Intermediate between F2E and F2F in **two-frontier** BiHS (sparse attractor representatives — related cost idea, **different structure** from eSBS pair cache). Lesson: track expansions, pairwise heuristic evals, and runtime separately. F2A ≠ SFBDS.

### Lecture context (methodology)

| Note | Use for our project |
|------|---------------------|
| [Master-Class BDS](context/presentations_summary/01_Master-ClassBDS_context.md) | F2E vs F2F tradeoff; two-frontier side selection (Pohl); early vs late stopping language |
| [Best-First / A*](context/presentations_summary/02_SAI-3-4_Best-First-AStar_context.md) | Admissibility/consistency, OPEN/CLOSED, tie-breaking |
| [Heuristics](context/presentations_summary/03_SAI-6-Heuristics_context.md) | Manhattan / Octile; pairwise \(h(a,b)\) for F2F |
| [Early vs Late](context/presentations_summary/04_SAI-3.7_Early-vs-Late-AStar_context.md) | Background only. **MVP locks A\*-Late** (goal on select/pop) for uni A* and SFBDS pair goals — not Early+\(U\). |

Pohl cardinality (smaller OPEN) applies to **two** frontiers. SFBDS has **one** OPEN of pairs; direction is a **local** which-side-of-the-pair choice ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md)). Do not import Pohl as the SFBDS direction default.

### Comparison table

Domains and reported numbers: **verify in original PDFs** before the final report.

| Paper | Year | Main method | Search repr. | Heuristic | Domains (as in notes) | Main contribution | Main limitation | Relevance |
|-------|------|-------------|--------------|-----------|------------------------|-------------------|-----------------|-----------|
| Moldenhauer et al. | 2010 | SFBDS | Single frontier of pairs | F2F natural | Multiple (*verify*) | Paired-state BiHS + local direction | Pair explosion; policy/domain transfer | Core algorithm |
| Lippi et al. | 2012 | eSBS + cache/prune | Pair SBS | F2F pair | Several (*verify*) | Pair/subproblem caching + pruning | Cache confounds fairness | Ablation axis |
| Barker & Korf | 2015 | F2E analysis | Two-frontier | F2E | Hanoi + std (*verify*) | Overlap explanation | Not absolute theorem | Why F2E often fails |
| Barker diss. | 2015 | F2E survey/expts | Two-frontier | F2E | Hanoi, peg, roads (*verify*) | Nuanced exceptions | Scope breadth | Avoid overclaim |
| Chen et al. NBS | 2017 | NBS / MEP | Two-frontier F2E | F2E consistent | Std (*verify*) | ≤2·VC expansion theory | Expansions ≠ runtime | Optional baseline |
| Siag et al. SoCS | 2023 | F2F vs F2E compare | Mostly two-frontier; SFBDS noted | Both | Benchmarks (*verify*) | F2F informative but costly | Naive F2F not shown faster | Direct justification |
| Siag et al. IJCAI | 2023 | Bound/design space | Two-frontier F2E | F2E consistent | (*verify*) | Unify MEP + bounds | More bounds ≠ faster | Fix F2E definition |
| Siag & Shperberg AIJ | 2025 | Bound learning | Two-frontier F2E | F2E consistent | Hanoi + (*verify*) | Theory–practice gap | Scope ≠ SFBDS-F2F | Don’t strawman F2E |
| Shubi et al. | 2026 | BiXDFBnB | Paired SFBDS-like | F2F (MAX) | LSP, Snakes, Coil | F2F natural in pairs for MAX | Not shortest-path grids | Conceptual support only |
| Zou et al. F2A | 2026 | F2A attractors | Two-frontier | F2E/F2F/F2A | Grids, 15-puzzle, pancake (*verify*) | Middle ground on eval cost | Not SFBDS; different from pair cache | Metric design |

---

## Stage 2: Current state of knowledge

Labels: **[D]** directly supported · **[I]** reasonable inference · **[O]** still open in supplied literature.

### F2E
- **[D]** Fixed-endpoint \(h_F,h_B\) are cheap and independent ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)).
- **[D]** Often dominated by A* (strong \(h\)) or Bi brute-force (weak \(h\)) due to overlapping high-\(g\) pruning ([`03`](context/sfbds_literature_context_md/03_limitations_front_to_end_2015.md), [`04`](context/sfbds_literature_context_md/04_barker_dissertation_front_to_end_2015.md)).
- **[D]** Modern F2E with MEP/consistency can be near-optimal in expansions and practically strong ([`05`](context/sfbds_literature_context_md/05_near_optimal_bidirectional_search_nbs_2017.md), [`07`](context/sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md), [`08`](context/sfbds_literature_context_md/08_bridging_theory_and_practice_2025.md)).
- **[D]** Exceptions exist (roads, peg solitaire, pathological graphs).

### F2F
- **[D]** More informative LBs; can greatly reduce expansions ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md), [`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)).
- **[D]** Two-frontier naive F2F can cost ~\(O(|OPEN_F|·|OPEN_B|)\) ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)).
- **[D]** Full F2F can minimize expansions but incur huge pairwise eval counts ([`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)).

### Expansions vs runtime
- **[D]** Fewer expansions need not mean less runtime (SFBDS [`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md); Siag SoCS [`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md); F2A three-cost lesson [`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)).
- **[I]** Break-even depends on \(h\)-eval cost × call count vs expansion savings (and vs pair bookkeeping / cache overhead).

### Why SFBDS makes F2F natural
- **[D]** Nodes are already pairs; one \(h(u,v)\) per considered pair, avoiding full opposite-OPEN scan ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md), [`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)).

### Known SFBDS costs
- **[D]** Larger pair state space; harder duplicates; direction policy domain-dependent ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md)); repeated pairs need caching/pruning ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md)).

### Caching and related sparse ideas
- **[D]** eSBS: pruning + caching of pair subproblems substantially improve SBS ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md)).
- **[D]** Unequal caching can unfairly favor one heuristic ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md)).
- **[D]** F2A uses sparse representatives in **two-frontier** BiHS — related cost-reduction idea, **not** an eSBS pair/result cache and **not** SFBDS ([`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)).
- **[I]** Memoizing \(O(1)\) Manhattan is not a credible primary ablation for runtime crossover on grids.

### Heuristic strength, expansions, runtime, memory
- **[D]** Strong \(h\) favors A*; weak favors Bi ([`03`](context/sfbds_literature_context_md/03_limitations_front_to_end_2015.md), Master-Class).
- **[D]** More informative bounds can increase bookkeeping cost ([`07`](context/sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md), [`08`](context/sfbds_literature_context_md/08_bridging_theory_and_practice_2025.md)).
- **[D]** A* space ≈ expansions; eSBS hybrid trades memory ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md); lecture A*).

### What has already been compared experimentally
- SFBDS vs uni / conventional Bi ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md)).
- eSBS vs A*/IDA*/SBS — caching for **SBS efficiency**, not as F2F-vs-F2E crossover variable ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md)).
- F2E BiHS vs A*/Bi brute ([`03`](context/sfbds_literature_context_md/03_limitations_front_to_end_2015.md), [`04`](context/sfbds_literature_context_md/04_barker_dissertation_front_to_end_2015.md)).
- NBS vs BiHS/A* ([`05`](context/sfbds_literature_context_md/05_near_optimal_bidirectional_search_nbs_2017.md)).
- F2F vs F2E informativeness; SFBDS efficient-F2F trade-off left open ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)).
- F2E bound families ([`07`](context/sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md), [`08`](context/sfbds_literature_context_md/08_bridging_theory_and_practice_2025.md)).
- F2F in MAX paired search ([`09`](context/sfbds_literature_context_md/09_bidirectional_longest_paths_f2f_2026.md)).
- F2A vs A*/F2E/F2F/NBS on grids & puzzles — two-frontier, not SFBDS ([`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)).

### Insufficiently explored (in supplied pack)
- **[O]** Whether SFBDS makes F2F *practically* favorable vs F2E on **grid pathfinding** with controlled map structure.
- **[O]** How a **shared pair/result cache** shifts the F2F/F2E **runtime crossover** inside SFBDS (distinct from Lippi’s “caching helps SBS” and from F2A).
- **[O]** Direction-selection × heuristic-type interaction on grids.
- **[O]** Controlled injected \(h\)-cost / informativeness curves for SFBDS.

---

## Stage 3: Research gaps (course-feasible)

| Gap | Missing piece | Why interesting | Risk / mitigation |
|-----|---------------|-----------------|-------------------|
| **1** Grid F2F/F2E crossover + full cost metrics | When F2F justifies cost on grids | Matches course framing; conditional conclusions | Weak variables → bake-off; use density/corridor/distance + \(h\)-time |
| **2** Pair-cache × F2F/F2E runtime | Systematic **pair/result** cache × heuristic ablation in SFBDS | Mechanism for “efficient F2F” without inventing F2A; Lippi ≠ this crossover study | Low reuse; choose redundant maps; report hits; do not ablate \(O(1)\) Manhattan memo as primary |
| **3** Direction × F2F/F2E | Controlled **SFBDS-local** policy × heuristic on grids | SFBDS-unique knob | Null interaction still publishable as factorial |
| **4** Synthetic \(h\)-cost curves | Explicit break-even vs eval cost / informativeness | Isolates cost–benefit when natural \(h\) is cheap | Artificiality; pair with Manhattan vs exact distance |
| **5** Approximate F2F in SFBDS | F2A-style middle ground **inside** SFBDS | Bridges Siag + Zou | Harder; extension only |
| **6** SFBDS on DAO/maze with F2A-style metrics | Same grid style + pairwise evals | Valuable only with Gap 1–2 variables | Becomes another bake-off alone |

---

## Stage 4: Project ideas (short list)

| Idea | RQ (one line) | Difficulty (theory/impl/expt) | Role |
|------|---------------|-------------------------------|------|
| **A** Controlled grid crossover | Under which grid conditions does SFBDS-F2F justify \(h\)-cost vs F2E? | 2 / 3 / 3 | Backup |
| **B** Pair-cache crossover | Does a shared **pair/result** cache change which of F2F/F2E wins on runtime? | 2 / 3 / 4 | **Primary** |
| **C** Direction × heuristic | How do SFBDS-local direction policies interact with F2F vs F2E? | 2 / 3 / 3 | Optional |
| **D** Synthetic \(h\)-cost curves | Where is the F2F/F2E break-even as eval cost varies? | 2 / 2 / 3 | **MVP sensitivity** + extension |
| **E** Approximate F2F (landmarks) | Can cheap approximate pairwise \(h\) recover most F2F savings? | 3 / 4 / 3 | Extension |
| **F** F2A-in-SFBDS | Port attractor ideas into SFBDS | High | Avoid as primary |

---

## Stage 5: Ranking

| Idea | Originality | Feasibility | Impl | Expt clarity | Risk | Academic value | Rank |
|------|-------------|-------------|------|--------------|------|----------------|------|
| **B Pair-cache crossover** | High | High | Med | High | Low–med | High | **1 — primary** |
| **A Grid crossover** | Med | Very high | Med | High | Low | Med–high | **2 — backup** |
| D Cost curves | Med–high | High | Low–med | Very high | Low | Med–high | 3 (MVP light + extension) |
| C Direction × h | Med | High | Med | Med | Med | Med | 4 |
| E Approx F2F | High | Med | High | Med–high | Med | High | 5 (extension) |
| F F2A-in-SFBDS | High | Low–med | Very high | Med | High | High | 6 (avoid) |

Fits course preferences: meaningful RQ, ablations, not heavy math, pair scope, clear tables/plots even without a universal winner ([instructions](context/Project_Instructions_context.md)).

---

## Stage 6: Final recommendation

### Primary — Idea B

**Title:** Pair-Result Caching and the Front-to-Front / Front-to-End Runtime Crossover in Single-Frontier Bidirectional Search on Grids

**Gap addressed:** Literature shows (i) F2F is more informative but often not practically faster ([`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)), (ii) SFBDS makes pairwise \(h\) natural but has pair overhead ([`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md), [`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)), (iii) eSBS caching improves SBS efficiency ([`02`](context/sfbds_literature_context_md/02_efficient_single_frontier_bidirectional_search_2012.md)) but is **not** used as the controlled variable for F2F-vs-F2E **runtime crossover** on grids. F2A ([`10`](context/sfbds_literature_context_md/10_front_to_attractors_2026.md)) addresses two-frontier eval cost differently (attractors ≠ pair/result cache).

**Cache object (locked for Idea B):**
- **(A) Primary ablation — eSBS-style pair/result cache:** reuse of distance / bound / solved-subproblem results for canonical pairs (exact key and eviction: verify in Lippi PDF before coding). Shared policy for F2E and F2F; report hits/misses and peak entries.
- **(B) Not primary under Manhattan MVP — memoized \(h\):** only when \(h\) is expensive (exact distance oracle, PDB, or delayed cost). Do **not** treat memoizing \(O(1)\) Manhattan as the Idea B variable.
- **MVP sensitivity:** small **eval-cost multiplier** on heuristic calls (Idea D light) so runtime can still move when natural Manhattan is cheap.

**Main RQ:** Under which combinations of **pair/result cache** policy and grid structure does SFBDS-F2F achieve lower runtime than SFBDS-F2E, and when does it only reduce expansions?

**Hypotheses:**
1. **[I]** F2F expands fewer nodes than F2E (supported directionally by [`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md); not yet shown in *our* SFBDS+grid setup).
2. **[I]** Without pair/result caching, F2F often loses on runtime despite fewer expansions (SFBDS/F2F cost lessons [`01`](context/sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md), [`06`](context/sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)).
3. **[I] exploratory:** A **shared** pair/result cache *may* flip the runtime winner when F2F induces more repeated pairwise / pair-subproblem work than F2E (different pair visit patterns → higher reuse). Lippi **[D]** supports “caching helps SBS” and “unequal caching confounds fairness,” **not** that shared caching preferentially rescues F2F on grids. Equal help to both heuristics (no flip) is a publishable outcome.
4. **[I]** Open easy maps favor F2E; constrained mazes favor F2F more often (structure × informativeness).

**Algorithms:** A*; SFBDS-F2E; SFBDS-F2F; same **pair/result** cache module (off / unbounded / capped). NBS only if time remains (not required).

**Domains:** 4-connected unit-cost grids; random obstacle maps; maze/corridor maps; sizes e.g. 64²–256²; fixed seeds.

**Experimental matrix (MVP):**  
`{heuristic: F2E, F2F} × {pair-cache: off, unbounded} × {map family: random, maze} × {density or corridor width: 3 levels} × {≥30 queries/cell}` + A* on the same queries + a small **eval-cost multiplier** sweep (few levels) as sensitivity.

**Metrics:** runtime (repeated), expansions, generations, heuristic evaluations, heuristic CPU time, **pair-cache** hits/misses, peak OPEN/CLOSED/cache, solution cost, timeouts.

**Figures/tables (target):**
1. Expansions F2F vs F2E  
2. Runtime same  
3. Crossover heatmap pair-cache × density  
4. Cache hit rate vs map type  
5. Heuristic-time fraction of runtime (incl. cost-multiplier cells)  
6. Summary win-rate table  

**MVP:** shared SFBDS; Manhattan F2E/F2F; **pair/result** cache off vs on; eval-cost multiplier sensitivity; random+maze; A*; cost-agreement checks where termination is defined.  
**Extension:** cache-size sweep; expensive \(h\) (exact distance); landmark approximate F2F (Idea E).

**Why not mere repetition:** Lippi studies caching for SBS efficiency, not F2F-vs-F2E winner flip; Siag SoCS leaves the SFBDS trade-off open; Zou F2A is two-frontier / attractors, not SFBDS pair-cache. Originality depends on that distinction remaining explicit in the report.

### Backup — Idea A

Same SFBDS framework without pair-cache as the primary factor; emphasize density/corridor/distance crossover. Add pair-cache later if time. Promote to primary if instructor rejects Idea B’s cache object or Manhattan+pair-cache MVP.

---

## MVP methodology (partially locked; PDF gates remain)

| Topic | Status | Default / note |
|-------|--------|----------------|
| Framework | Locked | Shared SFBDS shell; vary heuristic (F2E vs F2F) and **pair/result** cache policy |
| Direction | Locked (SFBDS-native) | Expand the side of the **current pair** with **fewer legal operators**; documented deterministic tie-break (e.g. prefer start-side). **Not** Pohl smaller-OPEN (that needs two frontiers). Idea C out of MVP. |
| Stopping / termination | **Locked (MVP)** | **A\*-Late** for uni A* and SFBDS: goal test when a node/pair is **selected from OPEN**. SFBDS goal iff \(x=y\) (**coincide-only**; connectable out of MVP). No incumbent-\(U\) Early baseline. Goal selection is **not** counted in ``expanded``. Parent-operator suppression via ``forbid_state``. Backward expansion uses ``predecessors`` (defaults to successors on undirected grids). Heuristic evals occur only after duplicate/better-path (A*-aligned). |
| Ties | Locked | **TBh** (prefer smaller \(h\) / larger \(g\)), then deterministic pair/state id |
| Heuristic | Locked for MVP | **Manhattan** on 4-connected unit grids (admissible + consistent) |
| Reopening | Locked under consistent \(h\) | None required for MVP |
| Cache | Locked object; semantics gate | Shared **pair/result** cache for F2E and F2F; off / unbounded / capped; report hits/misses. Exact key/eviction from Lippi PDF. **Not** primary \(h\)-memo under Manhattan. |
| Eval-cost sensitivity | Locked in MVP | Small multiplier on heuristic wall time / artificial delay (Idea D light) |
| Metrics | Locked | Runtime, expansions, generations, heuristic evals + time, peak OPEN/CLOSED/cache, solution cost, timeouts |

### Still must verify in original PDFs (documentation / report gate)

MVP **implementation locks** already in code (not waiting on PDFs):

- Stopping: **Late** on select; SFBDS goal iff \(x=y\) (**coincide-only**).
- Domain assumption: **undirected** unit grids — ``predecessors`` defaults to ``successors``; directed graphs must override.
- Heuristic modules F2F/F2E and pair-\(f\) writeup still benefit from PDF cross-check before the report.

Historical PDF checklist (report / claims, not a coding blocker for the shell):

1. SFBDS pseudocode vs our Late/coincide MVP (note: connectable stopping **out of MVP**).
2. Exact F2E and F2F formulas on an SFBDS pair \((x,y)\) (pair \(f\)).
3. Pair-level duplicate detection / better-path replacement (duplicate key).
4. eSBS pair/result cache — **out of active project scope**.

Do **not** claim literature-faithful connectable termination or directed-graph SFBDS without implementing those variants.

### Confirm with instructor before coding

1. SFBDS + **pair/result-cache** ablation is an acceptable “specific condition” beyond bare F2F vs F2E (not an \(O(1)\) Manhattan memo toggle).
2. Grids-only OK (vs puzzles).
3. Whether NBS/F2A baselines are expected, or A* + SFBDS-F2E/F2F suffice.
4. Manhattan + pair-cache + light eval-cost multiplier OK for MVP (vs requiring expensive \(h\)).
5. Report language/format (e.g. AAAI’27 style) and code-link requirement.
6. Fallback: if Idea B’s cache object is rejected, run Idea A as primary.

### Methodology checklists (doc, not code)

**Cache-object checklist**
- [ ] Ablation object is pair/result cache (A), not Manhattan memo (B).
- [ ] Under Manhattan-only, expect **no** meaningful runtime change from \(h\)-memo alone; do not design MVP around that.
- [ ] Shared policy for F2E and F2F; hit rates and peak cache reported.
- [ ] Eval-cost multiplier cells included so cheap-\(h\) runs can still show cost sensitivity.

**Direction-policy checklist**
- [ ] Policy executable with a **single** pair OPEN (local side choice).
- [ ] Default = fewer legal operators + documented tie-break.
- [ ] Pohl used only if a two-frontier baseline is added later — not inside SFBDS shell.

**Claim-label audit**
- [ ] Every hypothesis tagged **[D]** / **[I]** / **[O]**.
- [ ] Hyp 3 remains **[I]** exploratory; Lippi not cited as proving an F2F-preferential flip.

**Locked-equations gate**
- [ ] One-page pair \(f\) (F2E vs F2F), stop, duplicate key, cache key — filled from PDFs.

---

## Intended implementation architecture (post-approval)

Thin entrypoints; logic in library modules.

```text
Grid instances → Experiment runner
                    ├─ A* (Late; same conventions as SFBDS)
                    └─ SFBDS core
                         ├─ Direction: fewer legal operators (local)
                         ├─ F2E heuristic ─┐
                         ├─ F2F heuristic ─┤
                         ├─ Pair/result cache (shared; off|unbounded|capped)
                         └─ Metrics logger → Tables / plots
```

**No code in this document.** Implementation plan (SFBDS core → heuristics → pair-cache → experiments) starts only after instructor OK **and** the locked-equations gate.

---

## Next actions for the team

1. **Instructor confirmation** — send [`instructor_confirmation_brief.md`](instructor_confirmation_brief.md); record answers in its decision log.
2. **Verify originals** — fill locked-equations sheet (pair \(f\), stop, duplicates, cache key). *No PDFs in this repo yet — add paper PDFs or paths before this step.*
3. **Then** produce an incremental coding plan and implement.
