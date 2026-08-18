# Final-report paper source map

Collected in **Phase L** (2026-08-18). These are the **only** papers approved for citation in the compiled report.

Markdown notes under [`docs/context/sfbds_literature_context_md/`](../sfbds_literature_context_md/) are **navigation aids**, not citation authority. Lecture notes are not bibliography entries.

**Do not add papers here unless the citation set is explicitly expanded.**

Locked set: six papers. Lippi 2012, Barker dissertation, Siag AIJ 2025, Shubi 2026, Zou 2026, and Pohl 1969 were **not** collected.

---

## hart1968astar

- **Canonical title:** A Formal Basis for the Heuristic Determination of Minimum Cost Paths
- **Authors:** Peter E. Hart, Nils J. Nilsson, Bertram Raphael
- **Year:** 1968
- **Venue:** IEEE Transactions on Systems Science and Cybernetics, Vol. 4, No. 2, pp. 100–107
- **DOI / official source URL:** https://doi.org/10.1109/TSSC.1968.300136
- **Bibliographic corroboration:** Nilsson’s publications list (http://ai.stanford.edu/~nilsson/publications.html) records the same title, authors, venue, and `SSC-4(2):100-107, 1968`. Barker and Korf (2015, this folder) cite Hart, Nilsson, and Raphael (1968) for A*.
- **Local PDF filename:** *none* (IEEE paywalled. An author’s copy exists at `https://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf`; it was not stored in this pass. Bibliographic verification is enough for the planned A* definition cite.)
- **Report section:** Background; Algorithms (A* sidecar)
- **Claim/formula we may cite (bib-level only):** A* is the standard unidirectional heuristic search with evaluation \(f = g + h\). We will **not** quote numbered theorems from this paper until a local PDF is verified.
- **Original PDF verified:** **no** (bibliographic record verified; PDF not local)
- **Planned BibTeX key:** `hart1968astar`
- **Identified by:** [`presentations_summary/02_SAI-3-4_Best-First-AStar_context.md`](../presentations_summary/02_SAI-3-4_Best-First-AStar_context.md) (not in the 10-note pack)

---

## felner2010sfbds

- **Canonical title:** Single-Frontier Bidirectional Search
- **Authors:** Ariel Felner, Carsten Moldenhauer, Nathan Sturtevant, Jonathan Schaeffer
- **Year:** 2010
- **Venue:** Proceedings of the Twenty-Fourth AAAI Conference on Artificial Intelligence (AAAI-10), pp. 59–64
- **DOI / official source URL:** https://doi.org/10.1609/aaai.v24i1.7555 — https://ojs.aaai.org/index.php/AAAI/article/view/7555
- **PDF URL used:** https://ojs.aaai.org/index.php/AAAI/article/download/7555/7416
- **Local PDF filename:** `papers/felner_et_al_2010_sfbds.pdf`
- **Report section:** Background; Algorithms
- **Claim/formula verified in PDF:**
  - A search node is a pair \(N(x,y)\); the task is the shortest path between \(x\) and \(y\) (pp. 59–60).
  - Expanding \(x\) generates \((x_i,y)\); expanding \(y\) generates \((x,y_j)\). Goal when \(x=y\) (p. 60).
  - A **jumping policy** chooses the side to expand. One listed feature is **branching factor**: expand the state with the smaller branching factor (p. 61). Our implementation’s BF direction policy is this family, not a claim that Felner et al. specified our exact code.
  - Pairwise heuristic \(h(x,y)\) is used on the pair node; Manhattan distance is given as a symmetric example (p. 61).
  - Best-first SFBDS can have up to \(V^2\) unique pair tasks (p. 60, Case 4).
- **Do not cite this PDF for:** our official F2E pair-bound formula (not in this paper); pair/result **caching** (not in the verified claims).
- **Note vs Markdown:** note `01` listed Moldenhauer first. Official AAAI cite and the PDF list **Felner first**. Use the official order.
- **Original PDF verified:** **yes**
- **Planned BibTeX key:** `felner2010sfbds`
- **Identified by:** [`sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md`](../sfbds_literature_context_md/01_single_frontier_bidirectional_search_2010.md)

---

## barker2015f2e

- **Canonical title:** Limitations of Front-To-End Bidirectional Heuristic Search
- **Authors:** Joseph K. Barker, Richard E. Korf
- **Year:** 2015
- **Venue:** Proceedings of the Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 1086–1092
- **DOI / official source URL:** https://doi.org/10.1609/aaai.v29i1.9374 — https://ojs.aaai.org/index.php/AAAI/article/view/9374
- **PDF URL used:** https://ojs.aaai.org/index.php/AAAI/article/download/9374/9233
- **Local PDF filename:** `papers/barker_korf_2015_f2e_limitations.pdf`
- **Report section:** Background
- **Claim/formula verified in PDF:**
  - Front-to-end: heuristic estimates cost only to the original start or goal; front-to-front evaluates against the opposite frontier (p. 1086).
  - Thesis (abstract and §3.1): any front-to-end BiHS algorithm will **likely** be dominated by unidirectional heuristic search **or** bidirectional brute-force search; a pathological counterexample exists, so it is not an impossibility theorem.
  - Mechanism (§3.1, p. 1087): a heuristic mainly prevents expansion of **high-\(g\)** nodes; those deep nodes are also the ones bidirectional brute-force already avoids past the midpoint. Weak \(h\) ⇒ BiHS does not beat Bi brute-force; strong \(h\) ⇒ unidirectional heuristic search expands fewer than BiHS.
- **Do not cite:** quantitative tables from this paper as if they were our grid results. Do not upgrade “likely dominated” to “never works.”
- **Original PDF verified:** **yes**
- **Planned BibTeX key:** `barker2015f2e`
- **Identified by:** [`sfbds_literature_context_md/03_limitations_front_to_end_2015.md`](../sfbds_literature_context_md/03_limitations_front_to_end_2015.md)

---

## chen2017nbs

- **Canonical title:** Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions
- **Authors:** Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant
- **Year:** 2017
- **Venue:** Proceedings of the Twenty-Sixth International Joint Conference on Artificial Intelligence (IJCAI-17), pp. 489–495
- **DOI / official source URL:** https://doi.org/10.24963/ijcai.2017/69 — https://www.ijcai.org/proceedings/2017/69
- **PDF URL used:** https://www.ijcai.org/proceedings/2017/0069.pdf
- **Local PDF filename:** `papers/chen_et_al_2017_nbs.pdf`
- **Report section:** Background; Algorithms (pair lower bound lineage)
- **Claim/formula verified in PDF (Definition 1, p. 490):**
  - On a **path pair** \((U,V)\): \(\mathrm{lb}(U,V)=\max\{f_F(U), f_B(V), c(U)+c(V)\}\).
  - This is a lower bound on a solution of the form \(U Z V^{-1}\).
  - Must-expand graph \(GMX(I)\); NBS expands both endpoints of a minimum-\(\mathrm{lb}\) pair and is at most \(2\cdot VC\) expansions (abstract, §5–6).
- **Do not write:** that Chen’s \(\mathrm{lb}\) already contains \(+1\) or \(\varepsilon\). Chen uses \(c(U)+c(V)\) without a cheapest-edge term. The unit-grid \(\varepsilon=1\) form is in Siag et al. 2023 (below).
- **Original PDF verified:** **yes**
- **Planned BibTeX key:** `chen2017nbs`
- **Identified by:** [`sfbds_literature_context_md/05_near_optimal_bidirectional_search_nbs_2017.md`](../sfbds_literature_context_md/05_near_optimal_bidirectional_search_nbs_2017.md)

---

## siag2023socs

- **Canonical title:** Comparing Front-to-Front and Front-to-End Heuristics in Bidirectional Search
- **Authors:** Lior Siag, Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant
- **Year:** 2023
- **Venue:** Proceedings of the Sixteenth International Symposium on Combinatorial Search (SoCS 2023), Vol. 16, pp. 158–162
- **DOI / official source URL:** https://doi.org/10.1609/socs.v16i1.27296 — https://ojs.aaai.org/index.php/SOCS/article/view/27296
- **PDF URL used:** https://ojs.aaai.org/index.php/SOCS/article/download/27296/27069/31340
- **Local PDF filename:** `papers/siag_et_al_2023_socs_f2f_f2e.pdf`
- **Report section:** Introduction; Background; Discussion
- **Claim/formula verified in PDF:**
  - F2E: \(h_F\) to goal, \(h_B\) from start. F2F: \(h:V\times V\to\mathbb{R}\) (pp. 158–159).
  - Two-frontier F2F uses \(h_F(u)=\min_{v\in\mathrm{Open}_B}h(u,v)\) (p. 159) — **this is not SFBDS**.
  - For \(I_{AD}/I_{CON}\), \(\mathrm{lb}_E(u,v)=\max\{f_F(u),f_B(v),g_F(u)+g_B(v)+\varepsilon\}\) and \(\mathrm{lb}_F(u,v)=g_F(u)+g_B(v)+\max(h(u,v),\varepsilon)\) (Eqs. 1–2, p. 159). \(\varepsilon\) is the cheapest edge cost.
  - F2F variants expand fewer nodes than F2E; F2F NBS incurs large runtime / data-structure overhead (Table 4; conclusions p. 162). Naive F2F evaluation is quadratic in \(|\mathrm{Open}|\) (p. 161).
  - Future work: when to use F2F while controlling computational overhead (p. 162).
- **Markdown correction:** note `06` infers an SFBDS “one eval per pair” connection. **This SoCS PDF does not mention SFBDS.** Do not cite `siag2023socs` for SFBDS. Cite `felner2010sfbds` for the pair frontier.
- **Do not copy:** pancake / STP / DAO expansion tables into our report as if they were our results.
- **Original PDF verified:** **yes**
- **Planned BibTeX key:** `siag2023socs`
- **Identified by:** [`sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md`](../sfbds_literature_context_md/06_comparing_f2f_and_f2e_2023.md)

---

## siag2023ijcai

- **Canonical title:** Front-to-End Bidirectional Heuristic Search with Consistent Heuristics: Enumerating and Evaluating Algorithms and Bounds
- **Authors:** Lior Siag, Shahaf Shperberg, Ariel Felner, Nathan Sturtevant
- **Year:** 2023
- **Venue:** Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence (IJCAI-23), pp. 5631–5638
- **DOI / official source URL:** https://doi.org/10.24963/ijcai.2023/625 — https://www.ijcai.org/proceedings/2023/625
- **PDF URL used:** https://www.ijcai.org/proceedings/2023/0625.pdf
- **Local PDF filename:** `papers/siag_et_al_2023_ijcai_f2e_bounds.pdf`
- **Report section:** Background; Algorithms (why the F2E bound must be specified)
- **Claim/formula verified in PDF:**
  - Cheapest-edge cost \(\varepsilon\) (0 if unknown) (p. 5632).
  - Eq. (1): \(\mathrm{lb}(u,v)=\max\{f_F(u), f_B(v), g_F(u)+g_B(v)+\varepsilon\}\). A pair is a MEP if this \(\mathrm{lb}<C^*\).
  - Unspecified bound / algorithm choices change which F2E method is being compared (unifying MEP vs search-bound view, §§1–3).
  - Tighter consistency-case bounds \(\mathrm{lb}_C\) exist (Eq. 2); we **do not** claim to implement \(\mathrm{lb}_C\).
- **How this supports our code (after this verification):** on 4-connected **unit** grids, \(\varepsilon=1\), so for \(u\neq v\) the implemented pair bound \(\max(g_F+\mathrm{MD}(u,G), g_B+\mathrm{MD}(S,v), g_F+g_B+1)\) matches Eq. (1) with Manhattan F2E heuristics. When \(u=v\), a feasible meeting costs \(g_F+g_B\) (no extra edge); that meeting case is our implementation, not a separate Siag equation.
- **Original PDF verified:** **yes**
- **Planned BibTeX key:** `siag2023ijcai`
- **Identified by:** [`sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md`](../sfbds_literature_context_md/07_enumerating_algorithms_and_bounds_2023.md)

---

## Not collected (locked skip)

| Paper | Reason |
| --- | --- |
| Lippi, Ernandes, Felner 2012 (eSBS) | Skipped. Pair-cache is unimplemented future work: do **not** cite Felner 2010 for caching (not in the verified claims above) and do not collect eSBS. |
| Barker 2015 dissertation | Redundant with `barker2015f2e` |
| Siag and Shperberg 2025 AIJ | Two-frontier theory–practice; we do not compare against SOTA F2E BiHS |
| Shubi et al. 2026 | Longest paths / MAX |
| Zou et al. 2026 F2A | Two-frontier attractors, not SFBDS |
| Pohl 1969 | Optional classic BiHS origin; not needed given Barker + Felner |

---

## Writing rules for later phases

1. Cite only keys in this file. This map is the **only** citation spec; do not follow plan §7 bullets if they ever disagree.
2. Copy formulas from the **PDF lines above**, not from the Markdown notes.
3. Do not mention SFBDS when citing `siag2023socs`.
4. Do not attribute \(\varepsilon=+1\) to Chen 2017. Never write “NBS \(+1\)” or “Chen instantiates with \(+1\) when \(u\neq v\).” Unit-grid \(\varepsilon=1\) is Siag (`siag2023socs` Eq. 1 / `siag2023ijcai` Eq. 1).
5. Do not cite `felner2010sfbds` for pair/result caching. Verified claims are pair nodes, jumping/BF, pairwise \(h\), and \(V^2\) tasks. If Conclusions mention a cache, say it was **not implemented**; no Felner cache sentence, no Lippi cite.
6. `references.bib` is filled in the bibliography phase from these records, using `aaai2027.bst` fields.
