# Instructor confirmation brief — SFBDS F2F vs F2E

**Course:** Search in Artificial Intelligence (237-2-5513)  
**Purpose:** Get a yes/no on project scope **before any coding**.  
**Full definition:** [`project_definition.md`](project_definition.md)

---

## One-paragraph pitch (paste into email / office-hour ask)

We propose a controlled study inside a **fixed SFBDS** implementation on **4-connected grids**: compare admissible **F2E** vs **F2F**, while ablating a **shared eSBS-style pair/result (bound/subproblem) cache** and map structure (random vs maze). The question is when F2F’s expansion savings beat runtime cost, and whether that **pair cache** shifts the crossover—not a bare F2F-vs-F2E bake-off, and **not** memoizing \(O(1)\) Manhattan. MVP uses Manhattan + a light **eval-cost multiplier** sensitivity; baselines **A\*** + SFBDS-F2E/F2F. Backup if rejected: Idea A (structure crossover without cache as primary factor).

---

## Questions for the instructor

Record answers below (or tick in email reply).

| # | Question | Yes / No / Notes |
|---|----------|------------------|
| 1 | Is SFBDS + **pair/result-cache** ablation an acceptable “specific condition” beyond bare F2F vs F2E? | |
| 2 | Are **grids only** OK (no puzzle domains required for MVP)? | |
| 3 | Do **A\* + SFBDS-F2E + SFBDS-F2F** suffice as baselines (NBS / F2A **not** required)? | |
| 4 | Is **Manhattan** + pair-cache + light **eval-cost multiplier** OK for MVP (expensive \(h\) optional later)? | |
| 5 | Preferred report style / length (e.g. AAAI’27-like)? Code link required as in instructions? | |
| 6 | If Idea B is rejected, is **Idea A** (grid structure crossover, cache later) acceptable as primary? | |

---

## What we are *not* asking permission for yet

- Exact SFBDS pair-\(f\) / terminate / duplicate formulas (we will lock these from original PDFs next).
- Implementation language or full experimental matrix size.
- Claiming a new BiHS algorithm (this is an ablation / characterization study).

---

## Decision log (fill after the meeting)

- **Date:**  
- **Instructor:**  
- **Outcome:** Idea B approved / Idea A fallback / revise scope:  
- **Baseline set:**  
- **Any extra requirements:**  
- **Ok to start PDF locked-equations + coding plan?** Yes / No  

---

## After a clear Yes

1. Fill [`project_definition.md`](project_definition.md) locked-equations gate from Moldenhauer 2010 + Lippi 2012 (+ Siag SoCS as needed).  
2. Produce incremental implementation plan (SFBDS core → heuristics → pair-cache → experiments).  
3. Only then write code.
