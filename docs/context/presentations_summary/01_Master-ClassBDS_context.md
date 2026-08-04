# Recent Advances in Bidirectional Search — Complete Context

**Source deck:** `Master-ClassBDS.pptx`
**Number of slides:** 90
**Role in the project:** Primary project deck: bidirectional heuristic search, Front-to-End and Front-to-Front heuristics, MM, must-expand theory, and modern bidirectional algorithms.

## How to use this file with Cursor

This is a source-faithful, slide-by-slide context document. It preserves the terminology, equations, algorithm names, examples, experimental claims, and references appearing in the presentation. Use it as course context rather than as a replacement for checking visual diagrams in the original deck.

> Extraction note: text was recovered from the PowerPoint objects and, where useful, from a rendered PDF. Diagram geometry, arrows, colors, animations, and some image-only mathematical symbols cannot always be represented perfectly in Markdown. When a slide is primarily visual, the nearby text and labels are retained, but the original slide remains authoritative.

## Slide index

- Slide 1: Recent Advances in Bidirectional Search
- Slide 2: 50 years on Bidirectional Search
- Slide 3: Outline
- Slide 4: Papers
- Slide 5: https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing
- Slide 6: 1 — Background — summary of 1969-2014
- Slide 7: Unidirectional search
- Slide 8: Bidirectional breadth-first search (BDS)
- Slide 9: Bidirectional search algorithms
- Slide 10: Challenges
- Slide 11: 1: The frontiers should meet
- Slide 12: 2: Guaranteeing Optimality
- Slide 13: 2: guaranteeing Optimality
- Slide 14: 3: Heuristics for BDS
- Slide 15: 3: Heuristics for BDS
- Slide 16: 4: Which side/node to expand
- Slide 17: 6: Stopping Condition
- Slide 18: 2 — Meet in the Middle
- Slide 19: New Theoretical Claims
- Slide 20: MM: The Meet in the Middle algorithm [Holte, Felner, Sharon and Sturtevant. AAAI-2016, AIJ-2017] (#2)
- Slide 21: How MM works
- Slide 22: Result: must meet in the middle
- Slide 23: MM0 = Brute-force MM
- Slide 24: Intermediate Summary
- Slide 25: Region-Based Analysis
- Slide 26: FF vs RM
- Slide 27: Our Conjectures
- Slide 28: Experiments: 10-Pancake Puzzle, C*=10
- Slide 29: Fractional MM – fMM(P) — [Shaham, Felner, Chen and Sturtevant . SoCS-2017}[(#3)
- Slide 30: Restrained Algorithm
- Slide 31: 4 — The Must-Expand Theory
- Slide 32: The Optimality of A*
- Slide 33: What about bidirectional search
- Slide 34: The conditions for bidirectional search  — [Eckerle, Chen, Sturtevant, Zilles and Holte, ICAPS-2017](#4)
- Slide 35: Must Expand Pairs
- Slide 36: Slide 36
- Slide 37: G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
- Slide 38: G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
- Slide 39: G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
- Slide 40: G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
- Slide 41: G_must-expand (GMX)
- Slide 42: What does MVC of GMX looks like?
- Slide 43: Properties of MVC of GMX — [Shaham, Felner, Chen, and Sturtevant. SoCS-2017][#3]
- Slide 44: Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]
- Slide 45: Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]
- Slide 46: Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]
- Slide 47: Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]
- Slide 48: fMM and MVC
- Slide 49: GMX for the pancake puzzle
- Slide 50: Problem
- Slide 51: Is MVC Uni- or Bi-directional? — Sturtevant, Shperberg, Felner, Chen, ICAPS-2020 [paper #6]
- Slide 52: 5 — Parametric algorithms
- Slide 53: FMM and GBFSH
- Slide 54: Algorithm: GBFHS — [Barley, Riddle, Linarez-Lopes, Pohl SoCS-2018] [#8]
- Slide 55: Non-Parametric
- Slide 56: NBS: The Near-optimal Bidirectional Search Algorithm
- Slide 57: NBS: The Near-optimal Bidirectional Search Algorithm
- Slide 58: NBS: The Near-optimal Bidirectional Search Algorithm
- Slide 59: NBS
- Slide 60: NBS: Main properties
- Slide 61: 3) Algorithm: Dynamic Vertex-cover  — Bidirectional Search (DVCBS) — [Shperberg , Felner, Shimony and Sturtevant. AAAI 2019][#7]
- Slide 62: DGMX: A dynamic graph
- Slide 63: Execution of DVCBS
- Slide 64: Execution of DVCBS
- Slide 65: Execution of DVCBS
- Slide 66: No upper bound for DVCBS
- Slide 67: All Algorithms: Nodes Expanded
- Slide 68: Summary
- Slide 69: 6 — Bound Propagations
- Slide 70: Bound propagation
- Slide 71: Using hlb
- Slide 72: Advanced assumptions on the heuristics
- Slide 73: Assumptions [Dechter & Pearl 85]
- Slide 74: Case 1: Knowing Epsilon
- Slide 75: Fractional MM – fMM(P)
- Slide 76: GMX vs GMXe
- Slide 77: Case 2: Assuming consistency
- Slide 78: Case 2: Assuming consistency
- Slide 79: What does MVC of GMX look like now?
- Slide 80: Slide 80
- Slide 81: New algorithm assuming consistency
- Slide 82: 8 — Memory bounded  — Bidirectional Search
- Slide 83: Memory bounded Bi-HS
- Slide 84: Iterative-Deepening Bi-HS
- Slide 85: Fixed memory Bi-HS
- Slide 86: 9 — Summary
- Slide 87: Summary
- Slide 88: Ongoing and Future Work
- Slide 89: Papers
- Slide 90: https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing

---

## Complete slide-by-slide content

### Slide 1 — Recent Advances in Bidirectional Search

Recent Advances in Bidirectional Search

Ariel Felner
ISE Department
Ben-Gurion University
ISRAEL
felner@bgu.ac.il

Jingwei Chen
Univ. of Alberta
Canada

Eyal Shimony
Ben-Gurion Univ.
Israel

Eshed Shaham
HUJI Israel

Robert C. Holte
Univ. of Alberta
Canada

Nathan Sturtevant
Univ. of Alberta
Canada

Ariel Felner
Ben-Gurion Univ.
Israel

Shahaf Shperberg
Ben-Gurion Univ.
Israel

Guni Sharon
Ben-Gurion Univ.
Israel

1

**Additional text recovered from rendered slide:**
Jingwei Chen Eyal Shimony ISRAEL
felner@bgu.ac.il Eshed Shaham
Robert C. Holte Nathan Sturtevant
Shahaf Shperberg Univ. of Alberta Ariel Felner Guni Sharon
Ben-Gurion Univ. Ben-Gurion Univ. Ben-Gurion Univ. Univ. of Alberta
Canada Canada
Israel Israel Israel

---

### Slide 2 — 50 years on Bidirectional Search

50 years on Bidirectional Search

No real success &
no real understanding

[Table]
| Bidirectional A* | Pohl | 1969 |
| --- | --- | --- |
| | de Champeaux | 1975 |
| BS* | Kwa | 1989 |
| Perimeter search | Dillenburg & Nelson, Manzini | 1994-96 |
| Variants of bidirectional search | Kaindl & Kainz | 1997 |
| Single-frontier bidirectional search | Felner, Sturtevant and Schaeffer | 2010 |
| Dynamic perimeter | Wilt & Ruml | 2013 |
| Theoretical claims | Barker & Korf | 2015 |
| The MM algorithm | Holte, Felner, Sharon & Sturtevant | 2016 |
| The must-expand Theory / The NBS Algorithm | Eckerle, Chen, Sturtevant, Zilles / Holte | 2017 |
| Fractional MM and MVC | Shaham, Felner, Chen, Sturtevant | 2017 |
| The DVCBS algorithm / Bound propagation | Shperberg, Felner, Sturtevant, / Shimony, Hayoun | 2019 |
| BAE*, DIBSS etc, | Alcazar et al. Sewell et al. | 2020 |

New line of work in 2015

2

**Additional text recovered from rendered slide:**
years on Bidirectional Search 50
*Bidirectional A Pohl
de Champeaux
1969
1975
Single-frontier bidirectional search
Dynamic perimeter
Felner, Sturtevant and Schaeffer
Wilt & Ruml
2010
2013
The must-expand Theory Zilles ,Sturtevant ,Chen ,Eckerle 2017
The NBS Algorithm Holte
The DVCBS algorithm Shperberg, Felner, Sturtevant, 2019
Bound propagation Shimony, Hayoun

---

### Slide 3 — Outline

Outline

(1969-2014)
Background
(2015-2022)
2) The MM Algorithm
3) The Must-Expand Theory
4) Various Algorithms
5) Assuming More Knowledge
6) Memory Bounded Bidirectional Search
7) Summary and Conclusions

3

**Additional text recovered from rendered slide:**
1) Background

---

### Slide 4 — Papers

Papers

Joseph Kelly Barker, Richard E. Korf: Limitations of Front-To-End Bidirectional Heuristic Search.  AAAI 2015: 1086-1092
Robert C. Holte, Ariel Felner, Guni Sharon, Nathan R. Sturtevant, Jingwei Chen: MM: A bidirectional search algorithm that is guaranteed to meet in the middle. Artif. Intell. 252: 232-266 (2017)
Eshed Shaham, Ariel Felner, Jingwei Chen, Nathan R. Sturtevant:The Minimal Set of States that Must Be Expanded in a Front-to-End Bidirectional Search. SOCS 2017: 82-90
Jürgen Eckerle, Jingwei Chen, Nathan R. Sturtevant, Sandra Zilles, Robert C. Holte:Sufficient Conditions for Node Expansion in Bidirectional Heuristic Search. ICAPS 2017: 79-87
Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant:Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions. IJCAI 2017: 489-495
Nathan R. Sturtevant, Shahaf S. Shperberg, Ariel Felner, Jingwei Chen:Predicting the Effectiveness of Bidirectional Heuristic Search. ICAPS 2020: 281-290
Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant, Solomon Eyal Shimony, Avi Hayoun:Enriching Non-Parametric Bidirectional Search Algorithms. AAAI 2019: 2379-2386
Michael W. Barley, Patricia J. Riddle, Carlos Linares López, Sean Dobson, Ira Pohl:GBFHS: A Generalized Breadth-First Heuristic Search Algorithm. SOCS 2018: 28-36
Shahaf S. Shperberg, Ariel Felner: On the Differences and Similarities of fMM and GBFHS. SOCS 2020: 66
Edward C. Sewell, Sheldon H. Jacobson: Dynamically improved bounds bidirectional search. Artif. Intell. 291: 103405 (2021)
Vidal Alcázar, Patricia J. Riddle, Mike Barley: A Unifying View on Individual Bounds and Heuristic Inaccuracies in Bidirectional Search. AAAI 2020: 2327-2334
Shahaf S. Shperberg, Ariel Felner, Solomon Eyal Shimony, Nathan R. Sturtevant, Avi Hayoun:Improving Bidirectional Heuristic Search by Bounds Propagation. SOCS 2019: 106-114
Shahaf S. Shperberg, Steven Danishevski, Ariel Felner, Nathan R. Sturtevant:Iterative-deepening Bidirectional Heuristic Search with Restricted Memory. ICAPS 2021: 331-33
Vidal Alcázar: The Consistent Case in Bidirectional Search and a Bucket-to-Bucket Algorithm as a Middle Ground between Front-to-End and Front-to-Front. ICAPS 2021: 7-1
Nathan R. Sturtevant, Ariel Felner: A Brief History and Recent Achievements in Bidirectional Search. AAAI 2018: 8000-8007

4

**Additional text recovered from rendered slide:**
1) Joseph Kelly Barker, Richard E. Korf: Limitations of Front-To-End Bidirectional Heuristic Search. AAAI 20
15: 1086-1092
2) Robert C. Holte, Ariel Felner, Guni Sharon, Nathan R. Sturtevant, Jingwei Chen: MM: A bidirectional search
algorithm that is guaranteed to meet in the middle. Artif. Intell. 252: 232-266 (2017)
3) Eshed Shaham, Ariel Felner, Jingwei Chen, Nathan R. Sturtevant:
The Minimal Set of States that Must Be Expanded in a Front-to-End Bidirectional Search. SOCS 2017
: 82-90
4) Jürgen Eckerle, Jingwei Chen, Nathan R. Sturtevant, Sandra Zilles, Robert C. Holte:
Sufficient Conditions for Node Expansion in Bidirectional Heuristic Search. ICAPS 2017: 79-87
5) Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant:
Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions. IJCAI 2017: 489-495
6) Nathan R. Sturtevant, Shahaf S. Shperberg, Ariel Felner, Jingwei Chen:
Predicting the Effectiveness of Bidirectional Heuristic Search. ICAPS 2020: 281-290
7) Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant, Solomon Eyal Shimony, Avi Hayoun:
Enriching Non-Parametric Bidirectional Search Algorithms. AAAI 2019: 2379-2386
8) Michael W. Barley, Patricia J. Riddle, Carlos Linares López, Sean Dobson, Ira Pohl:
GBFHS: A Generalized Breadth-First Heuristic Search Algorithm. SOCS 2018: 28-36
9) Shahaf S. Shperberg, Ariel Felner: On the Differences and Similarities of fMM and GBFHS. SOCS 2020: 66
10) Edward C. Sewell, Sheldon H. Jacobson: Dynamically improved bounds bidirectional search. Artif. Intell. 2
91: 103405 (2021)
11) Vidal Alcázar, Patricia J. Riddle, Mike Barley: A Unifying View on Individual Bounds and Heuristic
Inaccuracies in Bidirectional Search. AAAI 2020: 2327-2334
12) Shahaf S. Shperberg, Ariel Felner, Solomon Eyal Shimony, Nathan R. Sturtevant, Avi Hayoun:
Improving Bidirectional Heuristic Search by Bounds Propagation. SOCS 2019: 106-114
13) Shahaf S. Shperberg, Steven Danishevski, Ariel Felner, Nathan R. Sturtevant:
Iterative-deepening Bidirectional Heuristic Search with Restricted Memory. ICAPS 2021: 331-33
14) Vidal Alcázar: The Consistent Case in Bidirectional Search and a Bucket-to-Bucket Algorithm as a
Middle Ground between Front-to-End and Front-to-Front. ICAPS 2021: 7-1 4
15) Nathan R. Sturtevant, Ariel Felner: A Brief History and Recent Achievements in Bidirectional Search. AA

---

### Slide 5 — https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing

https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing

5

**Additional text recovered from rendered slide:**
https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMd
x7zEJceR84?usp=sharing

---

### Slide 6 — 1 — Background — summary of 1969-2014

1Backgroundsummary of 1969-2014

6

**Additional text recovered from rendered slide:**
Back ground
summary of 1969-2014

---

### Slide 7 — Unidirectional search

Unidirectional search

n

h(n)

g(n)

start

goal

Different costs functions:
f(n)=g(n) Breadth-First Search. AKA Dijkstra’s algorithm.
f(n)=g(n)+h(n) The A* algorithm (1968).

Adding heuristics to unidirectional search is very beneficial

Breadth
First
Search

A*

7

**Additional text recovered from rendered slide:**
start goal
Adding heuristics
f(n)=g(n)+h(n) to(1968).
The A* algorithm unidirectional
search is very beneficial

---

### Slide 8 — Bidirectional breadth-first search (BDS)

Bidirectional breadth-first search (BDS)

Main motivation for BDS: significant ponential reduction

start

goal

Improving search
Add heuristics
Run bidirectional search

Let’s combine both directions:
Bidirectional Heuristic Search

8

**Additional text recovered from rendered slide:**
Main motivation for BDS:
significant ponential reduction
start goal
1) Add heuristics
2) Let’s combine both directions:

---

### Slide 9 — Bidirectional search algorithms

Bidirectional search algorithms

9

---

### Slide 10 — Challenges

Challenges

1) Guarantee that the frontiers meet – they might cross each other.
2) Guarantee optimality (when applicable).
3) How do we add heuristics
4) Which side to expand next
5) Which node within the chosen side
6) Stopping condition (when do we halt)

10

---

### Slide 11 — 1: The frontiers should meet

1: The frontiers should meet

Siloam Tunnel
Jerusalem -800

City of David

Many Bi-HS algorithms are
guaranteed to meet!

Meeting point

Transcontinental railroad
USA 1869

Channel Tunnel
Europe 1994

11

**Additional text recovered from rendered slide:**
Transcontinental
railroad Meeting
point
Europe 1994 Meeting point

---

### Slide 12 — 2: Guaranteeing Optimality

2: Guaranteeing Optimality

goal

start

12

---

### Slide 13 — 2: guaranteeing Optimality

2: guaranteeing Optimality

goal

start

Many Bi-HS algorithms guarantee optimality- no open node below
U (incumbent solution)

13

**Additional text recovered from rendered slide:**
Many Bi-HS algorithms guarantee
optimality- no open node below

---

### Slide 14 — 3: Heuristics for BDS

3: Heuristics for BDS

Front-to-end Heuristics
Each node has a heuristic towards the opposite end

u

goal

start

v

14

**Additional text recovered from rendered slide:**
Heuristics for BDS :3
u goal

---

### Slide 15 — 3: Heuristics for BDS

3: Heuristics for BDS

n

m

goal

start

Front-to-front systems are more accurate but take more time to compute.

15

**Additional text recovered from rendered slide:**
Heuristics for BDS :3
m goal
Front-to-front systems are more accurate
but take more time to compute.

---

### Slide 16 — 4: Which side/node to expand

4: Which side/node to expand

Alternate sides
Select node within the smallest OPEN (Pohl’s cardinality criterion)
Select side/node with smallest f(n)
Select side/node with smallest g(n)
How to break ties?

16

**Additional text recovered from rendered slide:**
Which side/node to expand :4

---

### Slide 17 — 6: Stopping Condition

6: Stopping Condition

3) Stopping condition (when do we halt?)
Early stopping: U: the best known path.
Stop when no node is smaller than U
Late stopping: When a node in both sides is chosen for expansion.

A nice survey of all past methods appears in the MM journal paper (#2)

17

**Additional text recovered from rendered slide:**
Stopping Condition :6
A nice survey of all past methods
• Lateappears
stopping: in thea MM
When node injournal paper
both sides is (#2)
chosen for expansion.

---

### Slide 18 — 2 — Meet in the Middle

2Meet in the Middle

18

**Additional text recovered from rendered slide:**
Meet in the Middle

---

### Slide 19 — New Theoretical Claims

New Theoretical Claims
[Baker & Korf, AAAI 2015] (#1)

With a strong heuristic A* should be preferred
With a weak heuristic, bidirectional brute force search should be preferred
Hidden assumption: The frontiers meet in the middle

Meet in the middle ???

19

**Additional text recovered from rendered slide:**
)#1( ]Baker & Korf, AAAI 2015[
• With a weak heuristic, bidirectional brute force search
should be preferred

---

### Slide 20 — MM: The Meet in the Middle algorithm [Holte, Felner, Sharon and Sturtevant. AAAI-2016, AIJ-2017] (#2)

MM: The Meet in the Middle algorithm [Holte, Felner, Sharon and Sturtevant. AAAI-2016, AIJ-2017] (#2)

MM: the first bidirectional heuristic
search algorithm that is guaranteed to meet
exactly in the middle!

start

goal

C*/2

20

**Additional text recovered from rendered slide:**
MM: The Meet in the Middle algorithm
[Holte, Felner, Sharon and Sturtevant. AAAI-2016, AIJ-2017] (#2)
C*/2 C*/2
start goal

---

### Slide 21 — How MM works

How MM works

Nodes are ordered by priority:
Expand a node (on either sides) with minimal pr(n)
Remember the cheapest path found (cost = U).
When a node n is generated, check if n is in Open of the opposite side
MM stops when U ≤ LB
LB=max(C; fminF ; fminB; gminF +gminB +e)

g(n)+h(n) (case 1)

pr(n)=max

2×g(n) (case 2)

pr(n)=g(n)+max{g(n),h(n)}

21

---

### Slide 22 — Result: must meet in the middle

Result: must meet in the middle

Proof:
Let g(n)>C*/2
case 1: If g(n)<h(n) then pr(n)=g(n)+h(n) > C*
case 2: If g(n)>h(n) then pr(n)= 2g(n) > C*
OPEN always includes a node x on the optimal path with pr(x)≤C*

n

x

start

goal

**Additional text recovered from rendered slide:**
• OPEN always includes a node x on the optimal
path with pr(x)≤C*
start goal

---

### Slide 23 — MM0 = Brute-force MM

MM0 = Brute-force MM

MM0 = MM with a heuristic h(n)=0 for all n.

g(n)+0= g(n)

pr(n)=max ≡ g(n)

2×g(n)

23

---

### Slide 24 — Intermediate Summary

Intermediate Summary

BFS

MM0

start

A*

MM

goal

---

### Slide 25 — Region-Based Analysis

Region-Based Analysis

remote

far

FF

FN

RN

NF

Near
C*/2

start

goal

NN

**Additional text recovered from rendered slide:**
m ote
FF NF FN RN
start Near Near
C*/2 C*/2

---

### Slide 26 — FF vs RM

Only unidirectional search (A*) does work on FF
Only MM/MM0 does work on RN

FF vs RM

FF

RN

start

goal

If FF>RN
MM0 outperforms BFS

**Additional text recovered from rendered slide:**
FF RN
start goal

---

### Slide 27 — Our Conjectures

Our Conjectures

With a sufficiently accurate heuristic A* will expand fewer nodes than MM and MM0.
With a moderately accurate heuristic, MM can expand fewer nodes than A* and MM0 if FF > RN
With a sufficiently inaccurate heuristic, MM0 will expand fewer nodes than MM and A* if FF > RN.

The Barker and Korf claims
are generally correct under special circumstances

27

**Additional text recovered from rendered slide:**
1. With a sufficiently accurate heuristic A* will
expand fewer nodes than MM and MM0.
The
2. With Barker and
a moderately Korf heuristic,
accurate claims MM can
expand
are fewer nodes
generally thanunder
correct A* and special
MM0 if FF > RN
circumstances
3. With a sufficiently inaccurate heuristic, MM 0 will
expand fewer nodes than MM and A* if FF > RN.

---

### Slide 28 — Experiments: 10-Pancake Puzzle, C*=10

Experiments: 10-Pancake Puzzle, C*=10

[Table]
| | Better Heuristic Accuracy | | | |
| --- | --- | --- | --- | --- |
| Algorithm | GAP-3 | GAP-2 | GAP-1 | GAP |
| A* | 97,644 | 27,162 | 4,280 | 117 |
| MM | 7,507 | 6,723 | 2,448 | 165 |
| MM0 | 5,551 | 5,551 | 5,551 | 5,551 |

#states expanded

**Additional text recovered from rendered slide:**
Algorith
GAP-3 GAP-2 GAP-1 GAP
#states

---

### Slide 29 — Fractional MM – fMM(P) — [Shaham, Felner, Chen and Sturtevant . SoCS-2017}[(#3)

Fractional MM – fMM(P)[Shaham, Felner, Chen and Sturtevant . SoCS-2017}[(#3)

0≤P≤1

pr(n)=max

Forward side:

Backward side:

(1-P)C*

PC*

Will meet at
PC*,(1-P)C*

goal

start

29

**Additional text recovered from rendered slide:**
Fractional MM – fMM(P)
[Shaham, Felner, Chen and Sturtevant . SoCS-2017}[(#3)
Forward side: pr(n)=max
Backward side: pr(n)=max
PC*,(1-P)C* start goal

---

### Slide 30 — Restrained Algorithm

Restrained Algorithm

MM and fMM are restrained
A* and backward A* are restrained

(1-P)C*

PC*

Will meet at
PC*,(1-P)C*

goal

start

30

**Additional text recovered from rendered slide:**
PC*,(1-P)C* start goal

---

### Slide 31 — 4 — The Must-Expand Theory

4The Must-Expand Theory

31

**Additional text recovered from rendered slide:**
The Must-Expand Theory

---

### Slide 32 — The Optimality of A*

The Optimality of A*

All nodes with f(u)=g(u)+h(u) < C* must be expanded to prove a C* solution
Otherwise, there might be a shorter path from u to the goal
“Given an admissible heuristic, A* expands (up to tie breaking) the necessary and sufficient nodes to find an optimal solution and to prove that this solution is indeed optimal.” [Dechter and Pearl, 1985]

A* is optimally efficient!

32

**Additional text recovered from rendered slide:**
All nodes with f(u)=g(u)+h(u) < C* must be expanded to
prove a C* solution
“Given an admissible heuristic, A* expands (up to tie breaking) the
necessary and sufficient nodes to find an optimal solution and to
prove that this solution is indeed optimal.” [Dechter and Pearl, 1985]

---

### Slide 33 — What about bidirectional search

What about bidirectional search

What are the set of states that must be expanded by a bidirectional search?

In bidirectional search we have to talk about a pair (u,v)
of states

33

**Additional text recovered from rendered slide:**
What are the set of states
that must be expanded by a
bidirectional search?
In bidirectional search
we have to talk about
a pair (u,v)

---

### Slide 34 — The conditions for bidirectional search  — [Eckerle, Chen, Sturtevant, Zilles and Holte, ICAPS-2017](#4)

The conditions for bidirectional search [Eckerle, Chen, Sturtevant, Zilles and Holte, ICAPS-2017](#4)

+?

34

**Additional text recovered from rendered slide:**
The conditions for bidirectional search
[Eckerle, Chen, Sturtevant, Zilles and Holte, ICAPS-2017](#4)

---

### Slide 35 — Must Expand Pairs

Must Expand Pairs

No MEP

MEP

B

A

Y1

35

**Additional text recovered from rendered slide:**
MEP No MEP
A B Y1 B

---

### Slide 36 — Slide 36

_No extractable text; see the original slide for its visual content._

---

### Slide 37 — G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

G_must-expand (GMX) [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

Forward

s

A

X

B

C

D

37

**Additional text recovered from rendered slide:**
G_must-expand (GMX)
[Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

---

### Slide 38 — G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

G_must-expand (GMX) [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

Forward

Backward

s

A

D

X

C

B

g

38

**Additional text recovered from rendered slide:**
G_must-expand (GMX)
[Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
Forward Backward

---

### Slide 39 — G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

G_must-expand (GMX) [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

Forward

Backward

s

A

Edges exist between must-expand pairs

D

X

C

B

g

39

**Additional text recovered from rendered slide:**
G_must-expand (GMX)
[Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
Forward Backward
Edges exist between must-expand pairs A A

---

### Slide 40 — G_must-expand (GMX)  — [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

G_must-expand (GMX) [Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)

Forward

Backward

s

g=0

A

g=1

D

X

g=2

C

B

g

40

**Additional text recovered from rendered slide:**
G_must-expand (GMX)
[Chen, Holte, Zilles, Sturtevant IJCAI-2017] (#5)
Forward Backward
g=0 s
g=1 A A

---

### Slide 41 — G_must-expand (GMX)

G_must-expand (GMX)

GMX as clusters of nodes

6

Every admissible algorithm
must expand a VC of GMX

The Minimum Vertex Cover of GMX (MVC)
is a lower bound

---

### Slide 42 — What does MVC of GMX looks like?

What does MVC of GMX looks like?

Eshed Shaham

42

**Additional text recovered from rendered slide:**
What does MVC of GMX
looks like?

---

### Slide 43 — Properties of MVC of GMX — [Shaham, Felner, Chen, and Sturtevant. SoCS-2017][#3]

Properties of MVC of GMX[Shaham, Felner, Chen, and Sturtevant. SoCS-2017][#3]

Contiguous partition = VC

43

**Additional text recovered from rendered slide:**
Properties of MVC of GMX
[Shaham, Felner, Chen, and Sturtevant. SoCS-2017][#3]

---

### Slide 44 — Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Properties of MVC of GMX[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Contiguous partition = VC

44

**Additional text recovered from rendered slide:**
Properties of MVC of GMX
[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

---

### Slide 45 — Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Properties of MVC of GMX[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Contiguous partition = VC

45

**Additional text recovered from rendered slide:**
Properties of MVC of GMX
[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

---

### Slide 46 — Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Properties of MVC of GMX[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Contiguous partition = VC

46

**Additional text recovered from rendered slide:**
Properties of MVC of GMX
[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

---

### Slide 47 — Properties of MVC of GMX — [Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Properties of MVC of GMX[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]

Contiguous partition = VC

Theorem:
MVC is one of these contiguous partitions

MVC of GMX is Restrained

47

**Additional text recovered from rendered slide:**
Properties of MVC of GMX
[Shaham, Felner, Chen and Sturtevant. SoCS-2017][#3]
MVC is one of these
contiguous partitions

---

### Slide 48 — fMM and MVC

fMM and MVC

fMM is restrained
MVC is restrained

fMM(P*) is equivalent to A*

(1-P)C*

PC*

start

goal

Main result: There exists P* such that
fMM(P*) is optimally efficient

48

**Additional text recovered from rendered slide:**
start goal

---

### Slide 49 — GMX for the pancake puzzle

GMX for the pancake puzzle

C*=13

start

776,458

goal

49

**Additional text recovered from rendered slide:**
goal goal

---

### Slide 50 — Problem

Problem

GMX and C* are not known in advance →
P* cannot be known in advance either

Challenge: reason about GMX on the fly and try to expand a VC fast

The NBS algorithm [Chen et al. 2017] and
The DVCBS algorithm [Shperberg et al. 2019]
try to expand a VC fast

50

**Additional text recovered from rendered slide:**
Challenge: reason about GMX on the fly
and try to expand a VC fast
try to expand a VC fast 50

---

### Slide 51 — Is MVC Uni- or Bi-directional? — Sturtevant, Shperberg, Felner, Chen, ICAPS-2020 [paper #6]

Is MVC Uni- or Bi-directional?Sturtevant, Shperberg, Felner, Chen, ICAPS-2020 [paper #6]

51

**Additional text recovered from rendered slide:**
Is MVC Uni- or Bi-directional?
Sturtevant, Shperberg, Felner, Chen, ICAPS-2020 [paper #6]

---

### Slide 52 — 5 — Parametric algorithms

5Parametric algorithms

52

**Additional text recovered from rendered slide:**
Parametric algorithms

---

### Slide 53 — FMM and GBFSH

FMM and GBFSH

Two parametric algorithms which may expand exactly an MVC of GMX
fMM(p) [SoCs-2017] (fractional MM) meets at [pC*,(1-p)C*]
2. GBFHS [Barley et al., SoCS2018 #8] , requires a split function and expand nodes according to the split function.

(1-P)C*

PC*

start

goal

53

**Additional text recovered from rendered slide:**
Two parametric algorithms which may expand exactly an
MVC of GMX
1. fMM(p) [SoCs-2017] (fractional MM) meets at [pC*,(1-p)C*]
start goal
2. GBFHS [Barley et al., SoCS2018 #8] , requires a split function and
expand nodes according to the split function.

---

### Slide 54 — Algorithm: GBFHS — [Barley, Riddle, Linarez-Lopes, Pohl SoCS-2018] [#8]

Algorithm: GBFHS[Barley, Riddle, Linarez-Lopes, Pohl SoCS-2018] [#8]

The optimal parameters (p*, split) are instance dependent and are not known in advance

54

**Additional text recovered from rendered slide:**
Algorithm: GBFHS
[Barley, Riddle, Linarez-Lopes, Pohl SoCS-2018] [#8]
The optimal parameters (p*, split) are instance
dependent and are not known in advance

---

### Slide 55 — Non-Parametric

Non-Parametric
GMX-based
Algorithms

The NBS algorithm [Chen et al. 2017] and
The DVCBS algorithm [Shperberg et al. 2019]
try to expand a VC fast

55

---

### Slide 56 — NBS: The Near-optimal Bidirectional Search Algorithm

NBS: The Near-optimal Bidirectional Search Algorithm
[Chen, Holte, Zilles, Sturtevant, IJCAI-2017 #5]

56

**Additional text recovered from rendered slide:**
NBS: The Near-optimal Bidirectional
Search Algorithm

---

### Slide 57 — NBS: The Near-optimal Bidirectional Search Algorithm

NBS: The Near-optimal Bidirectional Search Algorithm
[Chen, Holte, Zilles, Sturtevant, IJCAI-2017 #5]

57

**Additional text recovered from rendered slide:**
NBS: The Near-optimal Bidirectional
Search Algorithm

---

### Slide 58 — NBS: The Near-optimal Bidirectional Search Algorithm

NBS: The Near-optimal Bidirectional Search Algorithm
[Chen, Holte, Zilles, Sturtevant, IJCAI-2017 #5]

58

**Additional text recovered from rendered slide:**
NBS: The Near-optimal Bidirectional
Search Algorithm

---

### Slide 59 — NBS

NBS

lb=1

X

s

g

lb=2

C

A

B

lb=3

D

Yi

59

**Additional text recovered from rendered slide:**
X Xs X
X X X X XA X
X XX X
Yi D

---

### Slide 60 — NBS: Main properties

NBS: Main properties

lb=1

X

s

g

1) NBS finds an optimal solution
2) NBS is at most twice than OPTIMAL
3) No other algorithm can have a better worst-case bound
4) NBS is robust

lb=2

C

A

B

lb=3

D

Yi

Why? Taking both vertices of disjoint edges is a VC ≤ 2 MVC

60

**Additional text recovered from rendered slide:**
NBS: Main properties lb=1
Xs X
1) NBS finds an optimal solution lb=2
2) NBS is at most twice than OPTIMAL XX X
Yi D
Why? Taking both vertices of B A
disjoint edges is a VC ≤ 2 MVC
3) No other algorithm can have a better
worst-case bound
4) NBS is robust 60

---

### Slide 61 — 3) Algorithm: Dynamic Vertex-cover  — Bidirectional Search (DVCBS) — [Shperberg , Felner, Shimony and Sturtevant. AAAI 2019][#7]

3) Algorithm: Dynamic Vertex-cover Bidirectional Search (DVCBS)[Shperberg , Felner, Shimony and Sturtevant. AAAI 2019][#7]

NBS expanded both nodes
DVCBS maintains dynamic GMX (DGMX) that uses the currently known information from Open nodes
Repeatedly find MVC of DGMX and expand it

Many variants exist

61

**Additional text recovered from rendered slide:**
3) Algorithm: Dynamic Vertex-cover
Bidirectional Search (DVCBS)
[Shperberg , Felner, Shimony and Sturtevant. AAAI 2019][#7]
• DVCBS maintains dynamic GMX (DGMX) that uses the currently
known information from Open nodes
Many variants exist 61

---

### Slide 62 — DGMX: A dynamic graph

DGMX: A dynamic graph

[Table]
| | GMX | DGMX |
| --- | --- | --- |
| Nodes | All nodes | All Open nodes |
| Edges | Pairs (u,v) S.T. lb(u,v)< C* | Pairs (u,v) S.T. lb(u,v)< LB |

Life cycle of DVCBS
1) Initialize DGMX,
2) Calculate MVC(),
3) Expand one cluster from the MVC, and
4) Update DGMX.

Many decisions/variants

62

**Additional text recovered from rendered slide:**
Execution of DVCBS
DGMX
lb=1

---

### Slide 63 — Execution of DVCBS

Execution of DVCBS

DGMX

X

s

g

lb=1

63

**Additional text recovered from rendered slide:**
X X X
lb=2

---

### Slide 64 — Execution of DVCBS

Execution of DVCBS

DGMX

X

g

2

A,X

lb=2

Yi

64

**Additional text recovered from rendered slide:**
X X X
A,X B, C

---

### Slide 65 — Execution of DVCBS

Execution of DVCBS

DGMX

X

6

B, C
D

A,X

lb=2

Yi

65

**Additional text recovered from rendered slide:**
No upper bound for DVCBS
DVCBS
MVC
• Optimal path s,x, g. Cost 2K-1.
• MVC is {X,Y,g}. NBS expans 6 nodes.
• DVCBS never expands Y.
• Generates (X,Y). This is a cluster of 2 nodes.
• It expands all the Vi nodes. K+1 nodes.

---

### Slide 66 — No upper bound for DVCBS

No upper bound for DVCBS

DVCBS

MVC

Optimal path s,x, g. Cost 2K-1.
MVC is {X,Y,g}. NBS expans 6 nodes.
DVCBS never expands Y.
Generates (X,Y). This is a cluster of 2 nodes.
It expands all the Vi nodes. K+1 nodes.

66

**Additional text recovered from rendered slide:**
All Algorithms: Nodes Expanded
First Ratio VC
solution VC/MVC
Pancake Puzzle-20
322,378 2.65 322,299 *A
209,723 1.71 208,648 NBSF
Gap-2
152,046 1.24 151,616 NBSA
141,669 1.16 141,111 DVSBSF
122,587 1.00 122,054 DVCBSA
peg Towers of Hanoi-4
3,268,093 4.75 3,239,287 *A
NBSF
234,165 1.91 234,165 6+6
232,268 1.89 232,268 NBSA
707,679 1.03 704,213 DVCBSF
691,159 1.01 690,389 DVCBSA
DVCBSA is the winner in all aspects, many time is exactly MVC

---

### Slide 67 — All Algorithms: Nodes Expanded

All Algorithms: Nodes Expanded

[Table]
| | | First / solution | Ratio VC/MVC | VC | | |
| --- | --- | --- | --- | --- | --- | --- |
| 20-Pancake Puzzle | | | | | | |
| | | 322,378 | 2.65 | 322,299 | A* | Gap-2 |
| | | 209,723 | 1.71 | 208,648 | NBSF | |
| | | 152,046 | 1.24 | 151,616 | NBSA | |
| | | 141,669 | 1.16 | 141,111 | DVSBSF | |
| | | 122,587 | 1.00 | 122,054 | DVCBSA | |
| 4-peg Towers of Hanoi | | | | | | |
| | | 3,268,093 | 4.75 | 3,239,287 | A* | |
| | | 234,165 | 1.91 | 234,165 | NBSF | 6+6 |
| | | 232,268 | 1.89 | 232,268 | NBSA | |
| | | 707,679 | 1.03 | 704,213 | DVCBSF | |
| | | 691,159 | 1.01 | 690,389 | DVCBSA | |

DVCBSA is the winner in all aspects, many time is exactly MVC

67

**Additional text recovered from rendered slide:**
Summary
• Non-parametric GMX-based algorithms
• NBS - worst case guarantee (2x)
• DVCBS - no guarantee but better
average-case performance

---

### Slide 68 — Summary

Summary

Non-parametric GMX-based algorithms
NBS - worst case guarantee (2x)
DVCBS - no guarantee but better
average-case performance

68

**Additional text recovered from rendered slide:**
Bound Propagations

---

### Slide 69 — 6 — Bound Propagations

6Bound Propagations

69

**Additional text recovered from rendered slide:**
Bound propagation
[Shperberg, Felner, Sturtevant, Shimony, Hayoun, SoCS-2019] (#12)
[Alcazar, Barley and Riddle (AAAI-2020](#11)
lb(u) can be plugged in to any algorithm

---

### Slide 70 — Bound propagation

Bound propagation
[Shperberg, Felner, Sturtevant, Shimony, Hayoun, SoCS-2019] (#12)
[Alcazar, Barley and Riddle (AAAI-2020](#11)

lb(u) can be plugged in to any algorithm

70

**Additional text recovered from rendered slide:**
Using hlb
Using hlb bestows good attributes such as
• Well-Behavedness
• Reasonable
MM_LB on Pancake (n=10)
No “Hump” in the middle
Stronger Weaker
Heuristic Heuristic 71

---

### Slide 71 — Using hlb

Using hlb

Using hlb bestows good attributes such as
Well-Behavedness
Reasonable

MM_LB on Pancake (n=10)

No “Hump” in the middle

Weaker
Heuristic

Stronger
Heuristic

71

**Additional text recovered from rendered slide:**
Advanced assumptions on the
heuristics

---

### Slide 72 — Advanced assumptions on the heuristics

7
Advanced assumptions on the heuristics

72

**Additional text recovered from rendered slide:**
Assumptions [Dechter & Pearl 85]
Traditionally, algorithms only assume
admissibility but not consistency
What if the algorithms
have more knowledge
on the instances?
[Shaham, Felner, Sturtevant and Rosenchein. SoCS-2018] [#9]

---

### Slide 73 — Assumptions [Dechter & Pearl 85]

Assumptions [Dechter & Pearl 85]

Traditionally, algorithms only assume
admissibility but not consistency

What if the algorithms have more knowledge
on the instances?

[Shaham, Felner, Sturtevant and Rosenchein. SoCS-2018] [#9]

73

**Additional text recovered from rendered slide:**
Case 1: Knowing Epsilon

---

### Slide 74 — Case 1: Knowing Epsilon

Case 1: Knowing Epsilon
[Shaham, Felner, Sturtevant and Rosenchein. SoCS-2018] [#9]

+ε

74

**Additional text recovered from rendered slide:**
Fractional MM – fMM(P)
0≤P≤1
Forward side: pr(n)=max
Backward side: pr(n)=max +ε
(1-P)C*
Will meet at
PC*,(1-P)C* start goal

---

### Slide 75 — Fractional MM – fMM(P)

Fractional MM – fMM(P)

0≤P≤1

pr(n)=max

Forward side:

+ε

Backward side:

(1-P)C*

PC*

Will meet at
PC*,(1-P)C*

goal

start

75

**Additional text recovered from rendered slide:**
GMX vs GMXe
No knowledge on ε
Assuming ε=1

---

### Slide 76 — GMX vs GMXe

GMX vs GMXe

No knowledge on ε

Assuming ε=1

**Additional text recovered from rendered slide:**
Case 2: Assuming consistency
h(u,v)=5
start u v goal

---

### Slide 77 — Case 2: Assuming consistency

Case 2: Assuming consistency

h(u,v)=5

u

v

goal

start

77

**Additional text recovered from rendered slide:**
start u v goal

---

### Slide 78 — Case 2: Assuming consistency

Case 2: Assuming consistency

h(u,v)=5

u

v

goal

start

78

**Additional text recovered from rendered slide:**
What does MVC of
GMX look like now?
It is not restrained
We have a counter example
Here we do not have one 1/3 1/2 1/2
fraction f* for MVC but a 1/4 2/5 3/7
matrix of fractions F*
7/8 2/7 1/2

---

### Slide 79 — What does MVC of GMX look like now?

What does MVC of GMX look like now?

It is not restrained
We have a counter example

Here we do not have one fraction f* for MVC but a matrix of fractions F*

79

---

### Slide 80 — Slide 80

80

**Additional text recovered from rendered slide:**
New algorithm assuming consistency
)#10( ]DIBBS: Sewel and Jacobson AIJ[
BAE*: Alcazar, Barley and Riddle, AAAI-2020 (#11) [
• Very impressive experimental results
• Up to x10 reduction over v Bi-HS algorithms
other
goal
start

---

### Slide 81 — New algorithm assuming consistency

New algorithm assuming consistency
[DIBBS: Sewel and Jacobson AIJ] (#10)
[BAE*: Alcazar, Barley and Riddle, AAAI-2020 (#11)

Very impressive experimental results
Up to x10 reduction over other Bi-HS algorithms

v

u

goal

start

81

**Additional text recovered from rendered slide:**
Memory bounded
Bidirectional Search

---

### Slide 82 — 8 — Memory bounded  — Bidirectional Search

8Memory bounded Bidirectional Search

82

**Additional text recovered from rendered slide:**
Memory bounded Bi-HS
)#13( ]Shperberg, Danishevski, Felner and Sturtevant, ICAPS 2021[ )1
• All Bi-HS algorithms store the frontier in memory
• We worked on two new memory restrictions:
• 1) Linear memory: IDA* style
• 2) Fixed amount of memory M

---

### Slide 83 — Memory bounded Bi-HS

Memory bounded Bi-HS
[Shperberg, Danishevski, Felner and Sturtevant, ICAPS 2021] (#13)

All Bi-HS algorithms store the frontier in memory
We worked on two new memory restrictions:
1) Linear memory: IDA* style
2) Fixed amount of memory M

83

**Additional text recovered from rendered slide:**
Iterative-Deepening Bi-HS

---

### Slide 84 — Iterative-Deepening Bi-HS

Iterative-Deepening Bi-HS

84

**Additional text recovered from rendered slide:**
Fixed memory Bi-HS
Only M bytes allowed
Store partial frontier Store a Bloom Filter

---

### Slide 85 — Fixed memory Bi-HS

Fixed memory Bi-HS

Only M bytes allowed

Store partial frontier

Store a Bloom Filter

85

**Additional text recovered from rendered slide:**
Summary

---

### Slide 86 — 9 — Summary

9Summary

86

**Additional text recovered from rendered slide:**
Summary
2) The MM algorithm
3) The Must-Expand Theory
4) Various Algorithms
5) Assuming more knowledge
6) Memory bounded bidirectional search

---

### Slide 87 — Summary

Summary

2) The MM algorithm
3) The Must-Expand Theory
4) Various Algorithms
5) Assuming more knowledge
6) Memory bounded bidirectional search

87

**Additional text recovered from rendered slide:**
Ongoing and Future Work
1) Further improve the MEP theory
2) Front-to-Front Systems [Alcazar, ICAPS 2021] (#14)
3) Specific Heuristics for Bi-HS
4) Suboptimal algorithms
5) Finding killer apps.

---

### Slide 88 — Ongoing and Future Work

Ongoing and Future Work

Further improve the MEP theory
Front-to-Front Systems [Alcazar, ICAPS 2021] (#14)
Specific Heuristics for Bi-HS
Suboptimal algorithms
Finding killer apps.

88

**Additional text recovered from rendered slide:**
Papers
1) Joseph Kelly Barker, Richard E. Korf: Limitations of Front-To-End Bidirectional Heuristic Search. AAAI 20
15: 1086-1092
2) Robert C. Holte, Ariel Felner, Guni Sharon, Nathan R. Sturtevant, Jingwei Chen: MM: A bidirectional search
algorithm that is guaranteed to meet in the middle. Artif. Intell. 252: 232-266 (2017)
3) Eshed Shaham, Ariel Felner, Jingwei Chen, Nathan R. Sturtevant:
The Minimal Set of States that Must Be Expanded in a Front-to-End Bidirectional Search. SOCS 2017
: 82-90
4) Jürgen Eckerle, Jingwei Chen, Nathan R. Sturtevant, Sandra Zilles, Robert C. Holte:
Sufficient Conditions for Node Expansion in Bidirectional Heuristic Search. ICAPS 2017: 79-87
5) Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant:
16) Recent Advancements in
Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions. IJCAI 2017: 489-495
6) Nathan R. Sturtevant, Shahaf S. Shperberg, Ariel Felner, Jingwei Chen:
Predicting the Effectiveness of Bidirectional Heuristic Search. ICAPS 2020: 281-290
Bidirectional Search - Survey
7) Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant, Solomon Eyal Shimony, Avi Hayoun:
Enriching Non-Parametric Bidirectional Search Algorithms. AAAI 2019: 2379-2386
8) Michael W. Barley, Patricia J. Riddle, Carlos Linares López, Sean Dobson, Ira Pohl:
GBFHS: A Generalized Breadth-First Heuristic Search Algorithm. SOCS 2018: 28-36
9) Shahaf S. Shperberg, Ariel Felner: On the Differences and Similarities of fMM and GBFHS. SOCS 2020: 66
10) Edward C. Sewell, Sheldon H. Jacobson: Dynamically improved bounds bidirectional search. Artif. Intell. 2
91: 103405 (2021)
11) Vidal Alcázar, Patricia J. Riddle, Mike Barley: A Unifying View on Individual Bounds and Heuristic
Inaccuracies in Bidirectional Search. AAAI 2020: 2327-2334
12) Shahaf S. Shperberg, Ariel Felner, Solomon Eyal Shimony, Nathan R. Sturtevant, Avi Hayoun:
Improving Bidirectional Heuristic Search by Bounds Propagation. SOCS 2019: 106-114
13) Shahaf S. Shperberg, Steven Danishevski, Ariel Felner, Nathan R. Sturtevant:
Iterative-deepening Bidirectional Heuristic Search with Restricted Memory. ICAPS 2021: 331-33
14) Vidal Alcázar: The Consistent Case in Bidirectional Search and a Bucket-to-Bucket Algorithm as a
Middle Ground between Front-to-End and Front-to-Front. ICAPS 2021: 7-1
15) Nathan R. Sturtevant, Ariel Felner: A Brief History and Recent Achievements in Bidirectional Search. AA 89

---

### Slide 89 — Papers

Papers

Joseph Kelly Barker, Richard E. Korf: Limitations of Front-To-End Bidirectional Heuristic Search.  AAAI 2015: 1086-1092
Robert C. Holte, Ariel Felner, Guni Sharon, Nathan R. Sturtevant, Jingwei Chen: MM: A bidirectional search algorithm that is guaranteed to meet in the middle. Artif. Intell. 252: 232-266 (2017)
Eshed Shaham, Ariel Felner, Jingwei Chen, Nathan R. Sturtevant:The Minimal Set of States that Must Be Expanded in a Front-to-End Bidirectional Search. SOCS 2017: 82-90
Jürgen Eckerle, Jingwei Chen, Nathan R. Sturtevant, Sandra Zilles, Robert C. Holte:Sufficient Conditions for Node Expansion in Bidirectional Heuristic Search. ICAPS 2017: 79-87
Jingwei Chen, Robert C. Holte, Sandra Zilles, Nathan R. Sturtevant:Front-to-End Bidirectional Heuristic Search with Near-Optimal Node Expansions. IJCAI 2017: 489-495
Nathan R. Sturtevant, Shahaf S. Shperberg, Ariel Felner, Jingwei Chen:Predicting the Effectiveness of Bidirectional Heuristic Search. ICAPS 2020: 281-290
Shahaf S. Shperberg, Ariel Felner, Nathan R. Sturtevant, Solomon Eyal Shimony, Avi Hayoun:Enriching Non-Parametric Bidirectional Search Algorithms. AAAI 2019: 2379-2386
Michael W. Barley, Patricia J. Riddle, Carlos Linares López, Sean Dobson, Ira Pohl:GBFHS: A Generalized Breadth-First Heuristic Search Algorithm. SOCS 2018: 28-36
Shahaf S. Shperberg, Ariel Felner: On the Differences and Similarities of fMM and GBFHS. SOCS 2020: 66
Edward C. Sewell, Sheldon H. Jacobson: Dynamically improved bounds bidirectional search. Artif. Intell. 291: 103405 (2021)
Vidal Alcázar, Patricia J. Riddle, Mike Barley: A Unifying View on Individual Bounds and Heuristic Inaccuracies in Bidirectional Search. AAAI 2020: 2327-2334
Shahaf S. Shperberg, Ariel Felner, Solomon Eyal Shimony, Nathan R. Sturtevant, Avi Hayoun:Improving Bidirectional Heuristic Search by Bounds Propagation. SOCS 2019: 106-114
Shahaf S. Shperberg, Steven Danishevski, Ariel Felner, Nathan R. Sturtevant:Iterative-deepening Bidirectional Heuristic Search with Restricted Memory. ICAPS 2021: 331-33
Vidal Alcázar: The Consistent Case in Bidirectional Search and a Bucket-to-Bucket Algorithm as a Middle Ground between Front-to-End and Front-to-Front. ICAPS 2021: 7-1
Nathan R. Sturtevant, Ariel Felner: A Brief History and Recent Achievements in Bidirectional Search. AAAI 2018: 8000-8007

16) Recent Advancements in Bidirectional Search - Survey

89

**Additional text recovered from rendered slide:**
https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829R
x7zEJceR84?usp=sharing
Thank you!
Questions?

---

### Slide 90 — https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing

https://drive.google.com/drive/folders/1n_V_XJ-UEgrRf8Cr829RMdx7zEJceR84?usp=sharing

Thank you!
Questions?

90

---
