# Origin and Construction of Heuristic Functions — Complete Context

**Source deck:** `SAI-6-Heuristics.pptx`
**Number of slides:** 135
**Role in the project:** Heuristic-design deck: relaxed models, abstractions, pattern databases, additive heuristics, compression, differential heuristics, and related trade-offs.

## How to use this file with Cursor

This is a source-faithful, slide-by-slide context document. It preserves the terminology, equations, algorithm names, examples, experimental claims, and references appearing in the presentation. Use it as course context rather than as a replacement for checking visual diagrams in the original deck.

> Extraction note: text was recovered from the PowerPoint objects and, where useful, from a rendered PDF. Diagram geometry, arrows, colors, animations, and some image-only mathematical symbols cannot always be represented perfectly in Markdown. When a slide is primarily visual, the nearby text and labels are retained, but the original slide remains authoritative.

## Slide index

- Slide 1: Chapter 6
- Slide 2: Heuristic from Relaxed Models
- Slide 3: Example: Road navigation
- Slide 4: Example 2: - TSP problem
- Slide 5: Example 3- Tile Puzzle problem
- Slide 6: The STRIPS Problem formulation
- Slide 7: STRIPS - Eight Puzzle Example
- Slide 8: STRIPS - Eight Puzzle Example
- Slide 9: Admissibility and Consistency
- Slide 10: Method 2: pattern data base
- Slide 11: Homomorphic Abstractions
- Slide 12: Domains
- Slide 13: Domains
- Slide 14: (n,k) Pancake Puzzle
- Slide 15: (n,k) Top Spin Puzzle
- Slide 16: 4-peg Towers of Hanoi (TOH4)
- Slide 17: Better heuristics
- Slide 18: Subproblems-Abstractions
- Slide 19: Pattern Databases heuristics
- Slide 20: Example - 15 puzzle
- Slide 21: Example - 15 puzzle
- Slide 22: Non-additive pattern databases
- Slide 23: More than one PDBs
- Slide 24: Disjoint Additive PDBs (DADB)
- Slide 25: Disjoint Additive PDBs (DADB)
- Slide 26: DADB:Tile puzzles
- Slide 27: 4-peg towers of Hanoi
- Slide 28: Additive PDBS for TOH4
- Slide 29: TOH4: results
- Slide 30: General Additive PDBS
- Slide 31: Best Usage of Memory
- Slide 32: Compressing pattern database Sturtevant anf Felner 2017]]
- Slide 33: Compressing pattern database Felner et al AAAI-04, JAIR-2007]]
- Slide 34: Cliques in the pattern space
- Slide 35: Compressing cliques
- Slide 36: TOH4 results: 16 disks (14+2)
- Slide 37: TOH4: larger versions
- Slide 38: Tile Puzzles
- Slide 39: 15 puzzle results
- Slide 40: Dual lookups in pattern databases [Felner et al, IJCAI-05]
- Slide 41: Symmetries in PDBs
- Slide 42: Regular and dual representation
- Slide 43: Regular vs. Dual lookups in PDBs
- Slide 44: Regular and dual lookups
- Slide 45: Regular and dual in TopSpin
- Slide 46: Dual lookups
- Slide 47: 1) Inconsistent heuristics — [ Zahavi, et al. AAAI-2007,  — Zhang et al. IJCAI 2009, — Felner et al. AIJ-2011 ] —  — Joint work with Uzi Zahavi,  — Zhifu Zhang,  — Nathan Sturtevant, Robert Holte and  — Jonathan Schaeffer.
- Slide 48: Inconsistent heuristics — ]
- Slide 49: Consistent heuristics
- Slide 50: Inconsistent heuristics
- Slide 51: Reopening of nodes with A*
- Slide 52: In the context of A* inconsistency was considered a bad attribute
- Slide 53: Inconsistency in practical graphs
- Slide 54: Inconsistency and IDA*
- Slide 55: Pathmax
- Slide 56: Bidirectional pathmax (BPMX) — [Felner, Zahavi, Schaeffer, Holte IJCAI-2005]
- Slide 57: BPMX within A*
- Slide 58: Achieving inconsistent heuristics
- Slide 59: More than one heuristic
- Slide 60: 1) Randomizing a heuristic
- Slide 61: Achieving inconsistent heuristics
- Slide 62: Inconsistency of Dual lookups
- Slide 63: Compressing pattern database are inconsistent
- Slide 64: Consistent Vs. Inconsistent
- Slide 65: Heuristic value distribution
- Slide 66: Rubik’s cube results
- Slide 67: Tile puzzle results
- Slide 68: BPMX: Path finding results — random vs. max
- Slide 69: Summary: Inconsistent heuristics and BPMX
- Slide 70: Dual search
- Slide 71: Symmetries in PDBs
- Slide 72: Duality :definition 1
- Slide 73: Regular and dual representation
- Slide 74: Duality :definition 2
- Slide 75: Duality
- Slide 76: Using duality
- Slide 77: Dual Search
- Slide 78: Example
- Slide 79: When to jump
- Slide 80: Experimental results
- Slide 81: Experimental results
- Slide 82: Experimental results
- Slide 83: Experimental results
- Slide 84: Conclusions
- Slide 85: True distance Heuristics — New Form of  — Memory-based Heuristics
- Slide 86: A*
- Slide 87: Heuristic Functions: h(n)
- Slide 88: Different Domain Types
- Slide 89: Homomorphic Abstractions
- Slide 90: Abstractions – exponential domains
- Slide 91: Abstractions – polynomial domains
- Slide 92: Abstractions in Maps
- Slide 93: True Distance Heuristics
- Slide 94: True Distance Heuristics
- Slide 95: Abstracting APSP
- Slide 96: Differential heuristics
- Slide 97: Differential Heuristic
- Slide 98: Canonical heuristics
- Slide 99: All states
- Slide 100: Primary Data
- Slide 101: Primary & Secondary Data
- Slide 102: Extended secondary data
- Slide 103: Fix memory at 10N
- Slide 104: Example
- Slide 105: Slide 105
- Slide 106: Experimental Results
- Slide 107: Room-based Map
- Slide 108: Pathfinding (room maps)
- Slide 109: Diffrential against APSP
- Slide 110: Experimental Results - 10N memory
- Slide 111: Actuated Robotic Arm
- Slide 112: Robotic Arm Results
- Slide 113: The 8-puzzle
- Slide 114: Experimental Results – 8 puzzle
- Slide 115: Border Heuristics
- Slide 116: Border Heuristics
- Slide 117: Border Heuristics
- Slide 118: Border Heuristics
- Slide 119: Border Heuristic
- Slide 120: 4-peg Towers of Hanoi:
- Slide 121: Additive PDBS for TOH4
- Slide 122: Compressing Cliques
- Slide 123: Compressing PDBS
- Slide 124: Uncompressed PDB
- Slide 125: Compressed PDBs
- Slide 126: Border TDHs
- Slide 127: Border TDHs
- Slide 128: TOH4 results
- Slide 129: Summary
- Slide 130: Future (ongoing) work
- Slide 131: Different Domain Types
- Slide 132: Multi-agent path finding
- Slide 133: Motivation
- Slide 134: Multi-agent path finding
- Slide 135: Multi-agent path finding — N nodes, K agents

---

## Complete slide-by-slide content

### Slide 1 — Chapter 6

Chapter 6
Origin of Heuristic Functions

---

### Slide 2 — Heuristic from Relaxed Models

Heuristic from Relaxed Models

A heuristic function returns the exact cost of reaching a goal in a simplified or relaxed version of the original problem.
This means that we remove some of the constraints of the problem.
Removing constraints = adding edges

<number>

**Additional text recovered from rendered slide:**
A heuristic function returns the exact cost of
reaching a goal in a simplified or relaxed version
of the original problem.
This means that we remove some of the
constraints of the problem.

---

### Slide 3 — Example: Road navigation

Example: Road navigation

A good heuristic – the straight line.
We remove the constraint that we have to move along the roads
We are allowed to move in a straight line between two points.
We get a relaxation of the original problem.
In fact, we added edges of the complete graph

<number>

**Additional text recovered from rendered slide:**
We remove the constraint that we have to move along the
roads
We are allowed to move in a straight line between two
points.

---

### Slide 4 — Example 2: - TSP problem

Example 2: - TSP problem

We can describe the problem as a graph with 3 constraints:
1) Our sub-graph covers all the cities.
2) Every node has a degree two
an edge entering the node and
an edge leaving the node.
3) The graph is connected.
If we remove constraint 2 :
We get a spanning graph and the optimal solution to this problem is a MST (Minimum Spanning Tree).
If we remove constraint 3:
Now the graph isn’t connected and the optimal solution to this problem is the solution to the assignment problem.

<number>

**Additional text recovered from rendered slide:**
We get a spanning graph and the optimal solution to this
problem is a MST (Minimum Spanning Tree).
Now the graph isn’t connected and the optimal solution to
this problem is the solution to the assignment problem.

---

### Slide 5 — Example 3- Tile Puzzle problem

Example 3- Tile Puzzle problem

One of the constraints in this problem is that a tile can only slide into the position occupied by a blank.
If we remove this constraint we allow any tile to be moved horizontally or vertically position.
This is the Manhattan distance to its goal location.

<number>

**Additional text recovered from rendered slide:**
 One of the constraints in this problem is that a tile
can only slide into the position occupied by a
blank.
 If we remove this constraint we allow any tile to be
moved horizontally or vertically position.

---

### Slide 6 — The STRIPS Problem formulation

The STRIPS Problem formulation

We would like to derive such heuristics automatically.
In order to do that we need a formal description language that is richer than the problem space graph.
One such language is called STRIPS.
In this language we have predicates and operators.
Let’s see a STRIPS representation of the Eight Puzzle Problem

<number>

**Additional text recovered from rendered slide:**
• We would like to derive such heuristics
automatically.
• In order to do that we need a formal description
language that is richer than the problem space
graph.
• In this language we have predicates and
operators.
• Let’s see a STRIPS representation of the Eight
Puzzle Problem 6

---

### Slide 7 — STRIPS - Eight Puzzle Example

STRIPS - Eight Puzzle Example

On(x,y) = tile x is in location y.
Clear(z) = location z is clear.
Adj(y,z) = location y is adjacent to location z.
Move(x,y,z) = move tile x from location y to location z.
In the language we have:
A precondition list - for example to execute move(x,y,z) we
must have: On(x,y)
Clear(z)
Adj(y,z)
An add list - predicates that weren’t true before the operator and now after the operator was executed are true.
A delete list - a subset of the preconditions, that now after the
operator was executed aren’t true anymore.

<number>

**Additional text recovered from rendered slide:**
1) On(x,y) = tile x is in location y.
2) Clear(z) = location z is clear.
3) Adj(y,z) = location y is adjacent to location z.
4) Move(x,y,z) = move tile x from location y to location z.
An add list - predicates that weren’t true before the operator
and now after the operator was executed are true.
operator was executed aren’t true anymore. 7

---

### Slide 8 — STRIPS - Eight Puzzle Example

STRIPS - Eight Puzzle Example

Now in order to construct a simplified or relaxed problem we only have to remove some of the preconditions.
For example - by removing Clear(z) we allow tiles to move to adjacent locations.
In general, the hard part is to identify which relaxed problems have the property that their exact solution can be efficiently computed.

<number>

**Additional text recovered from rendered slide:**
• Now in order to construct a simplified or relaxed
problem we only have to remove some of the
preconditions.
• For example - by removing Clear(z) we allow tiles
to move to adjacent locations.
• In general, the hard part is to identify which relaxed
problems have the property that their exact solution
can be efficiently computed.

---

### Slide 9 — Admissibility and Consistency

Admissibility and Consistency

The heuristics that are derived by this method are both admissible and consistent.

Note : The cost of the simplified graph should be as close as possible to the original graph.

Admissibility means that the simplified graph has an equal or lower cost than the lowest - cost path in the original graph.

Consistency means that a heuristic h is consistent for every neighbor n’ of n,
when h(n) is the actual optimal cost of reaching a goal in the graph of the relaxed problem.

h(n)  c(n,n’)+h(n’)

<number>

**Additional text recovered from rendered slide:**
The heuristics that are derived by this method are both
admissible and consistent.
Note : The cost of the simplified graph should be as
close as possible to the original graph.
Admissibility means that the simplified graph has an
equal or lower cost than the lowest - cost path in the
original graph.
Consistency means that a heuristic h is consistent for
every neighbor n’ of n,
when h(n) is the actual optimal cost of reaching a
goal in the graph of the relaxed problem. 9

---

### Slide 10 — Method 2: pattern data base

Method 2: pattern data base

A different method for abstracting and relaxing to problem to get a simplified problem.
Invented in 1996 by Culberson & Schaeffer

<number>

**Additional text recovered from rendered slide:**
• A different method for abstracting and
relaxing to problem to get a simplified
problem.
• Invented in 1996 by Culberson &
Schaeffer

---

### Slide 11 — Homomorphic Abstractions

Homomorphic Abstractions

Many search spaces can be abstracted by merging nodes into abstract nodes
Distances from abstract spaces are lower bounds for the original problem

2

3

<number>

**Additional text recovered from rendered slide:**
• Many search spaces can be abstracted by
merging nodes into abstract nodes
2 3 2
• Distances from abstract spaces are lower
bounds for the original problem

---

### Slide 12 — Domains

Domains

15 puzzle
10^13 states
First solved by [Korf 85] with IDA* and Manhattan distance
Takes 53 seconds
24 puzzle
10^24 states
First solved by [Korf 96]
Takes two days

<number>

**Additional text recovered from rendered slide:**
1 2 3
4 5 6 7
8 9 1011
• First solved by [Korf 85] with
12131415
IDA* and Manhattan distance
1 2 3 4
24 puzzle 5 6 7 8 9
• 10^24 states 1011121314
• First solved by [Korf 96] 1516171819
• Takes two days 2021222324

---

### Slide 13 — Domains

Domains

Rubik’s cube
10^19 states
First solved by [Korf 97]
Takes 2 days to solve

<number>

---

### Slide 14 — (n,k) Pancake Puzzle

(n,k) Pancake Puzzle

An array of N tokens (Pancakes)
Operators: Any first k consecutive
tokens can be reversed.
The 17 version has 10^13 states
The 20 version has 10^18 states

<number>

**Additional text recovered from rendered slide:**
Pancake Puzzle )n,k(
1 2 3 4 5 N

---

### Slide 15 — (n,k) Top Spin Puzzle

(n,k) Top Spin Puzzle

n tokens arranged in a ring
States: any possible permutation of the tokens
Operators: Any k consecutive tokens can be reversed
The (17,4) version has 10^13 states
The (20,4) version has 10^18 states

<number>

**Additional text recovered from rendered slide:**
Top Spin Puzzle )n,k(
• Operators: Any k consecutive tokens can be
reversed

---

### Slide 16 — 4-peg Towers of Hanoi (TOH4)

4-peg Towers of Hanoi (TOH4)

Harder than the known 3-peg Towers of Hanoi
There is a conjecture about the length of optimal path but it was not proven.
Size 4^k

<number>

**Additional text recovered from rendered slide:**
peg Towers of Hanoi (TOH4)-4
• Harder than the known 3-peg Towers of
Hanoi
• There is a conjecture about the length of
optimal path but it was not proven.

---

### Slide 17 — Better heuristics

Better heuristics

In the 3rd Millennium we have very large memories.
We can build large tables.
For enhanced algorithms: large open-lists or transposition tables. They store nodes explicitly.
A more intelligent way is to store general knowledge. We can do this with heuristics

<number>

**Additional text recovered from rendered slide:**
• In the 3rd Millennium we have very large
memories.
• For enhanced algorithms: large open-lists or
transposition tables. They store nodes
explicitly.
• A more intelligent way is to store general
knowledge. We can do this with heuristics

---

### Slide 18 — Subproblems-Abstractions

Subproblems-Abstractions

Many problems can be abstracted into subproblems that must be also solved.
A solution to the subproblem is a lower bound on the entire problem.

Example: Rubik’s cube [Korf 97]
Problem: → 3x3x3 Rubik’s cube
Subproblem: → 2x2x2 Corner cubies.

<number>

**Additional text recovered from rendered slide:**
• Many problems can be abstracted into
subproblems that must be also solved.
• A solution to the subproblem is a lower
bound on the entire problem.

---

### Slide 19 — Pattern Databases heuristics

Pattern Databases heuristics

A pattern database (PDB) is a lookup table that stores solutions to all configurations of the sub-problem (patterns)
This PDB is used as a heuristic during the search

88 Million states

10^19 States

Search
space

#

h-value

Projection/
mapping

[Table]
| 1 | 18 |
| --- | --- |
| 2 | 20 |
| 3 | 18 |
| 4 | 17 |
| 5 | 19 |

Pattern
space

<number>

**Additional text recovered from rendered slide:**
• A pattern database (PDB) is a lookup table
that stores solutions to all configurations of the
sub-problem (patterns)
• This PDB is used as a heuristic during the
Search Projection/ Pattern 2 20
mapping space 3 18
5 19 19

---

### Slide 20 — Example - 15 puzzle

Example - 15 puzzle

1

1 4 5 10

4 5

8 11 9 12

2

13 15

8 9 10 11

3 6 7 14

12 13 14 15

How many moves do we need to move tiles 2,3,6,7 from locations 8,12,13,14 to their goal locations
The solution to this is located in
PDB[8][12][13][14]=18

<number>

**Additional text recovered from rendered slide:**
1 4 5 10 1 2 3
8 11 9 12 4 5 6 7
2 13 15 8 9 10 11
3 6 7 14 12 13 14 15
• How many moves do we need to move tiles
2,3,6,7 from locations 8,12,13,14 to their goal
locations
PDB[8][12][13][14]=18 20

---

### Slide 21 — Example - 15 puzzle

Example - 15 puzzle

2

3 6 7

How many moves do we need to move tiles 2,3,6,7 from locations 8,12,13,14 to their goal locations
The solution to this is located in
PDB[8][12][13][14]=18

<number>

**Additional text recovered from rendered slide:**
• How many moves do we need to move tiles
2,3,6,7 from locations 8,12,13,14 to their goal
locations
PDB[8][12][13][14]=18 21

---

### Slide 22 — Non-additive pattern databases

Non-additive pattern databases

Fringe pattern database [Culberson & Schaeffer 1996].
Has only 259 Million states.
Improvement of a factor of 100 over Manhattan Distance

<number>

**Additional text recovered from rendered slide:**
• Fringe pattern database
B x x 3
[Culberson & Schaeffer
1996]. x x x 7
x x x 11
• Has only 259 Million
12 13 14 15
states.
• Improvement of a factor 13 x B x
of 100 over Manhattan x 11 7 x
Distance 14 x 12 15
3 x x x

---

### Slide 23 — More than one PDBs

More than one PDBs

If you have k of admissible heuristics (e.g. PDBs), their max is also admissible,
h=max(h1,h2… hk)
What about h1+h2? Can this be admissible?

<number>

**Additional text recovered from rendered slide:**
• If you have k of admissible heuristics (e.g.
PDBs), their max is also admissible,

---

### Slide 24 — Disjoint Additive PDBs (DADB)

Disjoint Additive PDBs (DADB)

If you have many PDBS, take their maximum

Values of disjoint databases can be added and are still admissible [Korf & Felner: AIJ-02,
Felner, Korf & Hanan: JAIR-04]
Additivity can be applied if the cost of a subproblem is composed from costs of objects from corresponding pattern only

<number>

**Additional text recovered from rendered slide:**
1 2 3
4 5 6 7
8 9 10 11
12 13 14 15
• Values of disjoint databases can be added
and are still admissible [Korf & Felner: AIJ-02,
• Additivity can be applied if the cost of a
subproblem is composed from costs of objects
from corresponding pattern only 24

---

### Slide 25 — Disjoint Additive PDBs (DADB)

Disjoint Additive PDBs (DADB)

Consider the 7-tile subproblem (tiles 1-7) and the 8-tile sub problem (tiles 8-15).
They are disjoint: each operator belongs to one subproblem only

Values of disjoint databases can be added and are still admissible [Korf & Felner AIJ-02,
Felner, Korf & Hanan JAIR-04]

<number>

**Additional text recovered from rendered slide:**
•Consider the 7-tile subproblem (tiles 1-7) and
the 8-tile sub problem (tiles 8-15).
•They are disjoint: each operator belongs to
one subproblem only
1 2 3 1 2 3
4 5 6 7 4 5 6 7
8 9 10 11 8 9 10 11
12 13 14 15 12 13 14 15
• Values of disjoint databases can be added
and are still admissible [Korf & Felner AIJ-02,

---

### Slide 26 — DADB:Tile puzzles

DADB:Tile puzzles

5-5-5

6-6-3

7-8

6-6-6-6

[Korf, AAAI 2005]

[Table]
| Puzzle | Heuristic | Value | Nodes | Time | Memory |
| --- | --- | --- | --- | --- | --- |
| 15 | Breadth-FS | | 10^13 | 28 days | 3-tera-bytes |
| 15 | Manhattan | 36.942 | 401,189,630 | 53.424 | 0 |
| 15 | 5-5-5 | 41.562 | 3,090,405 | 0.541 | 3,145 |
| 15 | 6-6-3 | 42.924 | 617,555 | 0.163 | 33,554 |
| 15 | 7-8 | 45.632 | 36,710 | 0.034 | 576,575 |
| 24 | 6-6-6-6 | | 360,892,479,671 | 2 days | 242,000 |

<number>

**Additional text recovered from rendered slide:**
5-5-5 6-6-3 7-8 6-6-6-6
15 Breadth-FS 13^10 days 28 tera-bytes-3
360,892,479,67
24 6-6-6-6 1 days 2 242,000

---

### Slide 27 — 4-peg towers of Hanoi

4-peg towers of Hanoi

There is a conjecture about the length of optimal path but it was not proven.
Size 4^k
Infinite peg heuristic (INP): Each disk moves to its own temporary peg.
Additive pattern databases
[Felner, Korf & Hanan, JAIR-04]

<number>

**Additional text recovered from rendered slide:**
peg towers of Hanoi-4
• There is a conjecture about the length
of optimal path but it was not proven.
• Infinite peg heuristic (INP): Each disk
moves to its own temporary peg.

---

### Slide 28 — Additive PDBS for TOH4

Additive PDBS for TOH4

Partition the disks into disjoint sets
Store the cost of the complete pattern space of each set in a pattern database.
Add values from these PDBs for the heuristic value.
The n-disk problem contains 4^n states
The largest database that we stored was of 14 disks which needed 4^14=256MB.

6

10

<number>

**Additional text recovered from rendered slide:**
• Store the cost of the complete
pattern space of each set in a
pattern database. 6
• Add values from these PDBs for
the heuristic value.
• The n-disk problem contains 4^n
states 10
• The largest database that we
stored was of 14 disks which
needed 4^14=256MB.

---

### Slide 29 — TOH4: results

TOH4: results

[Table]
| | | | 16 disks | | |
| --- | --- | --- | --- | --- | --- |
| Heuristic | solution | h(s) | Avg h | Nodes | seconds |
| Infinite peg | | | | memory full | |
| Static 13-3 | 161 | 102 | 75.78 | 134,653,232 | 48 |
| Static 14-2 | 161 | 114 | 89.10 | 36,479,151 | 14 |
| Dynamic 14-2 | 161 | 114 | 95.52 | 12,872,732 | 21 |
| | | | 17 disks | | |
| Dynamic 14-3 | 183 | 116 | 97.05 | 238,561,590 | 2,501 |

The difference between static and dynamic is covered in [Felner, Korf & Hanan: JAIR-04]

<number>

**Additional text recovered from rendered slide:**
disks 16
disks 17
•The difference between static and dynamic is
covered in [Felner, Korf & Hanan: JAIR-04]

---

### Slide 30 — General Additive PDBS

General Additive PDBS

What about problems where each operator moves more than one object?
This was addressed by [Yang, Holte, Culberson, Zahavi, Felner JAIR 2008]
Cost splitting – split the costs among the different (non-disjoint) sub-problems.
Location based costs – we only charge the pattern that moved into a special location.
Additivity was also used in planning.

<number>

**Additional text recovered from rendered slide:**
• What about problems where each operator
moves more than one object?
• This was addressed by [Yang, Holte, Culberson,
Zahavi, Felner JAIR 2008]
• Cost splitting – split the costs among the
different (non-disjoint) sub-problems.
• Location based costs – we only charge
the pattern that moved into a special
location.

---

### Slide 31 — Best Usage of Memory

Best Usage of Memory

Given 1 giga byte of memory, how do we best use it with pattern databases?
[Holte, Newton, Felner, Meshulam and Furcy, ICAPS-2004] showed that it is better to use many small databases and take their maximum instead of one large database.
We will present a different (orthogonal) method [Felner, Mushlam & Holte: AAAI-04].

<number>

**Additional text recovered from rendered slide:**
• Given 1 giga byte of memory, how do we
best use it with pattern databases?
• [Holte, Newton, Felner, Meshulam and
Furcy, ICAPS-2004] showed that it is better
to use many small databases and take their
maximum instead of one large database.
• We will present a different (orthogonal)
method [Felner, Mushlam & Holte: AAAI-04].

---

### Slide 32 — Compressing pattern database Sturtevant anf Felner 2017]]

Compressing pattern database Sturtevant anf Felner 2017]]

Value compression:
When you have a large range of values partition them into disjoint regions.
Store a value for the entire region
For example for numbers 0…99
Partition to [0..9] [10..19] …. [90..99]
You save many bits
Combination of entry and value compression proved useful

<number>

**Additional text recovered from rendered slide:**
Compressing pattern database
]]Sturtevant anf Felner 2017
• When you have a large range of values partition them into
disjoint regions.

---

### Slide 33 — Compressing pattern database Felner et al AAAI-04, JAIR-2007]]

Compressing pattern database Felner et al AAAI-04, JAIR-2007]]

Entry Compression:
Nearby entries in PDBs are highly correlated !!
We propose to compress nearby entries by storing their minimum in one entry.
We show that → most of the knowledge is preserved
Consequences: Memory is saved, larger patterns can be used → speedup in search is obtained.

<number>

**Additional text recovered from rendered slide:**
Compressing pattern database
]]Felner et al AAAI-04, JAIR-2007
• Consequences: Memory is saved, larger patterns can be used → speedup in
search is obtained.

---

### Slide 34 — Cliques in the pattern space

Cliques in the pattern space

The values in a PDB for a clique are d or d+1
In permutation puzzles cliques exist when only one object moves to another location.

d

G

d+1

Usually they have nearby entries in the PDB
A[4][4][4][4][4]

A clique in TOH4

<number>

**Additional text recovered from rendered slide:**
• The values in a PDB for
a clique are d or d+1
• In permutation puzzles
cliques exist when only G d
one object moves to d+1
another location. d

---

### Slide 35 — Compressing cliques

Compressing cliques

Assume a clique of size K with values d or d+1
Store only one entry (instead of K) for the clique with the minimum d. Lose at most 1.
A[4][4][4][4][4] A[4][4][4][4][1]
Instead of 4^p we need only 4^(p-1) entries.
This can be generalized to a set of nodes with diameter D. (for cliques D=1)
A[4][4][4][4][4] A[4][4][4][1][1]
In general: compressing by k disks reduces memory requirements from 4^p to 4^(p-k)

<number>

**Additional text recovered from rendered slide:**
• Store only one entry (instead of K) for the
clique with the minimum d. Lose at most 1.
• This can be generalized to a set of nodes with
diameter D. (for cliques D=1)
• In general: compressing by k disks reduces
memory requirements from 4^p to 4^(p-k)

---

### Slide 36 — TOH4 results: 16 disks (14+2)

TOH4 results: 16 disks (14+2)

[Table]
| PDB | H(s) | Avg H | D | Nodes | Time | Mem MB |
| --- | --- | --- | --- | --- | --- | --- |
| 14/0 + 2 | 116 | 87.03 | 0 | 36,479,151 | 14.34 | 256 |
| 14/1 + 2 | 115 | 86.48 | 1 | 37,964,227 | 14.69 | 64 |
| 14/2 + 2 | 113 | 85.67 | 3 | 40,055,436 | 15.41 | 16 |
| 14/3 + 2 | 111 | 84.44 | 5 | 44,996,743 | 16.94 | 4 |
| 14/4 + 2 | 107 | 82.73 | 9 | 45,808,328 | 17.36 | 1 |
| 14/5 + 2 | 103 | 80.84 | 13 | 61,132,726 | 23.78 | 0.256 |

Memory was reduced by a factor of 1000!!! at a cost of only a factor of 2 in the search effort.

<number>

**Additional text recovered from rendered slide:**
2 + 14/0 116 87.03 0 36,479,151 14.34 256
2 + 14/1 115 86.48 1 37,964,227 14.69 64
2 + 14/2 113 85.67 3 40,055,436 15.41 16
2 + 14/3 111 84.44 5 44,996,743 16.94 4
2 + 14/4 107 82.73 9 45,808,328 17.36 1
2 + 14/5 103 80.84 13 61,132,726 23.78 0.256
• Memory was reduced by a factor of 1000!!!
at a cost of only a factor of 2 in the search
effort.

---

### Slide 37 — TOH4: larger versions

Memory was reduced by a factor of 1000!!! At a cost of only a factor of 2 in the search effort.
Lossless compressing is noe efficient in this domain.

TOH4: larger versions

[Table]
| size | PDB | Type | Avg H | Nodes | Time | Mem |
| --- | --- | --- | --- | --- | --- | --- |
| 17 | 14/0 + 3 | static | 81.5 | >393,887,923 | >421 | 256 |
| 17 | 14/0 + 3 | dynamic | 87.0 | 238,561,590 | 2,501 | 256 |
| 17 | 15/1 + 2 | static | 103.7 | 155,737,832 | 83 | 256 |
| 17 | 16/2 + 1 | static | 123.8 | 17,293,603 | 7 | 256 |
| 18 | 16/2 + 2 | static | 123.8 | 380,117,836 | 463 | 256 |

For the 17 disks problem a speed up of 3 orders of magnitude is obtained!!!
The 18 disks problem can be solved in 5 minutes!!

<number>

**Additional text recovered from rendered slide:**
17 3 + 14/0 static 81.5 393,887,923> 421> 256
17 3 + 14/0 dynamic 87.0 238,561,590 2,501 256
17 2 + 15/1 static 103.7 155,737,832 83 256
17 1 + 16/2 static 123.8 17,293,603 7 256
18 2 + 16/2 static 123.8 380,117,836 463 256
• For the 17 disks problem a speed up of
3 orders of magnitude is obtained!!!
• The 18 disks problem can be solved in 5
minutes!!

---

### Slide 38 — Tile Puzzles

Tile Puzzles

Goal State

Clique

Storing PDBs for the tile puzzle
(Simple mapping) A multi dimensional array →
A[16][16][16][16][16] size=1.04Mb
(Packed mapping) One dimensional array → A[16*15*14*13*12 ] size = 0.52Mb.
Time versus memory tradeoff !!

<number>

**Additional text recovered from rendered slide:**
A B Clique A B A B
C C DC
• (Packed mapping) One dimensional array →
A[16*15*14*13*12 ] size = 0.52Mb.

---

### Slide 39 — 15 puzzle results

15 puzzle results

A clique in the tile puzzle is of size 2.
We compressed the last index by two →
A[16][16][16][16][8]

[Table]
| PDB | Type | compress | Nodes | Time | Mem | Avg H |
| --- | --- | --- | --- | --- | --- | --- |
| 1 7-8 | packed | No | 136,288 | 0.081 | 576,575 | 44.75 |
| 1+ 7-8 | packed | No | 36,710 | 0.034 | 576,575 | 45.63 |
| 1 7-7-1 | packed | No | 464,977 | 0.232 | 57,657 | 43.64 |
| 1 7-7-1 | simple | No | 464,977 | 0.058 | 536,870 | 43.64 |
| 1 7-7-1 | simple | Yes | 565,881 | 0.069 | 268,435 | 43.02 |
| 2 7-7-1 | simple | Yes | 147,336 | 0.021 | 536,870 | 43.98 |
| 2+ 7-7-1 | simple | Yes | 66,692 | 0.016 | 536,870 | 44.92 |

<number>

**Additional text recovered from rendered slide:**
puzzle results 15
7-8 1 packed No 136,288 0.081 576,575 44.75
7-8 +1 packed No 36,710 0.034 576,575 45.63
7-7-1 1 packed No 464,977 0.232 57,657 43.64
7-7-1 1 simple No 464,977 0.058 536,870 43.64
7-7-1 1 simple Yes 565,881 0.069 268,435 43.02
7-7-1 2 simple Yes 147,336 0.021 536,870 43.98
7-7-1 +2 simple Yes 66,692 0.016 536,870 44.92

---

### Slide 40 — Dual lookups in pattern databases [Felner et al, IJCAI-05]

Dual lookups in pattern databases [Felner et al, IJCAI-05]

<number>

**Additional text recovered from rendered slide:**
• Dual lookups in pattern databases
[Felner et al, IJCAI-05]

---

### Slide 41 — Symmetries in PDBs

Symmetries in PDBs

Symmetric lookups were already performed by the first PDB paper of [Culberson & Schaeffer 96]
examples
Tile puzzles: reflect the tiles
about the main diagonal.
Rubik’s cube: rotate the cube
We can take the maximum among the different lookups
These are all geometrical symmetries
We suggest a new type of symmetry!!

7

8

<number>

**Additional text recovered from rendered slide:**
• Symmetric lookups were already
performed by the first PDB paper of
[Culberson & Schaeffer 96]
• examples 7
– Tile puzzles: reflect the tiles 8
• We can take the maximum among the 7 8
different lookups
• We suggest a new type of symmetry!! 41

---

### Slide 42 — Regular and dual representation

Regular and dual representation

Regular representation of a problem:
Variables – objects (tiles, cubies etc,)
Values – locations
Dual representation:
Variables – locations
Values – objects

<number>

---

### Slide 43 — Regular vs. Dual lookups in PDBs

Regular vs. Dual lookups in PDBs

Regular question:
Where are tiles {2,3,6,7} and how many moves are needed to gather them to their goal locations?
Dual question:
Who are the tiles in locations {2,3,6,7} and how many moves
are needed to distribute them to their goal locations?

<number>

**Additional text recovered from rendered slide:**
Where are tiles {2,3,6,7} and how
many moves are needed to gather
them to their goal locations? 2 3
• Dual question: 6 7
Who are the tiles in locations
{2,3,6,7} and how many moves
are needed to distribute them to
their goal locations?

---

### Slide 44 — Regular and dual lookups

Regular and dual lookups

Regular lookup: PDB[8,12,13,14]
Dual lookup: PDB[9,5,15,12]

<number>

**Additional text recovered from rendered slide:**
• Dual lookup: PDB[9,5,15,12] 44

---

### Slide 45 — Regular and dual in TopSpin

Regular and dual in TopSpin

Regular lookup for C : PDB[1,2,3,7,6]
Dual lookup for C: PDB[1,2,3,8,9]

<number>

---

### Slide 46 — Dual lookups

Dual lookups

Dual lookups are possible when there is a symmetry between locations and objects:
Each object is in only one location and each location occupies only one object.
Good examples: TopSpin, Rubik’s cube
Bad example: Towers of Hanoi
Problematic example: Tile Puzzles

<number>

**Additional text recovered from rendered slide:**
• Dual lookups are possible when there is a
symmetry between locations and objects:
– Each object is in only one location
and each location occupies only one
object.

---

### Slide 47 — 1) Inconsistent heuristics — [ Zahavi, et al. AAAI-2007,  — Zhang et al. IJCAI 2009, — Felner et al. AIJ-2011 ] —  — Joint work with Uzi Zahavi,  — Zhifu Zhang,  — Nathan Sturtevant, Robert Holte and  — Jonathan Schaeffer.

1) Inconsistent heuristics[ Zahavi, et al. AAAI-2007, Zhang et al. IJCAI 2009,Felner et al. AIJ-2011 ]Joint work with Uzi Zahavi, Zhifu Zhang, Nathan Sturtevant, Robert Holte and Jonathan Schaeffer.

<number>

**Additional text recovered from rendered slide:**
1) Inconsistent heuristics
[ Zahavi, et al. AAAI-2007,
Zhang et al. IJCAI 2009,
Felner et al. AIJ-2011 ]
Joint work with Uzi Zahavi,
Zhifu Zhang,
Nathan Sturtevant,
Robert Holte and
Jonathan Schaeffer .

---

### Slide 48 — Inconsistent heuristics — ]

Inconsistent heuristics]

Inconsistency sounds negative
“It is hard to concoct heuristics that are admissible but are inconsistent”
[AI book, Russel and Norvig 2005]
“Almost all admissible heuristics are consistent” [Korf, AAAI-2000]

<number>

**Additional text recovered from rendered slide:**
• “It is hard to concoct heuristics that
are admissible but are inconsistent”
• “Almost all admissible heuristics are
consistent” [Korf, AAAI-2000]

---

### Slide 49 — Consistent heuristics

Consistent heuristics

A heuristic is consistent if for every two nodes n and m
Intuition: h cannot change by more than the change of g

h(n)  c(n,m) + h(m)

h(m)  c(m,n) + h(n)

For undirected graphs: |h(n)-h(m)| ≤ c(n,m)

<number>

**Additional text recovered from rendered slide:**
• A heuristic is consistent if for every
two nodes n and m
h(n)  c(n,m) +
• Intuition: h cannot change by more
than the change of g

---

### Slide 50 — Inconsistent heuristics

Inconsistent heuristics

A heuristic is inconsistent if for some two nodes n and m

|h(n)-h(m)| > dist(n,m)

g=5
h=5
f=10

The child is inconsistent with its parent

1

g=6
h=2
f=8

<number>

**Additional text recovered from rendered slide:**
• A heuristic is inconsistent if for some
two nodes n and m
h=5 • The child is inconsistent
f=10 with its parent

---

### Slide 51 — Reopening of nodes with A*

Reopening of nodes with A*

c

a

0

f=2

f=1

d

5

I

G

f=8

f=7

f=0

f=3

b

f=6

Node d is expanded twice with A*!!

<number>

**Additional text recovered from rendered slide:**
a 0 c
0 f=2
I 0 d 0 5
G f=8
5 f=3
b f=6 f=2

---

### Slide 52 — In the context of A* inconsistency was considered a bad attribute

In the context of A* inconsistency was considered a bad attribute

Extreme case: exponential number of node expansions. n5(23), n1(11), n2(12), n1(10), n3(13), n1(9), n2(10),n1(8), n4(14), n1(7), n2(8), n1(6), n3(9), n1(5), n2(6), n1(4).

<number>

**Additional text recovered from rendered slide:**
• In the context of A* inconsistency
was considered a bad attribute
Extreme case: exponential number of
node expansions. n5(23), n1(11), n2(12), n1(10), n3(13),
n1(9), n2(10),n1(8), n4(14), n1(7), n2(8), n1(6), n3(9), n1(5), n2(6), n1(4). 52

---

### Slide 53 — Inconsistency in practical graphs

Inconsistency in practical graphs

<number>

---

### Slide 54 — Inconsistency and IDA*

Inconsistency and IDA*

In the context of A* inconsistency was considered a bad attribute
Node re-opening is not a problem with IDA* because each path to a node is examined anyway!!
No overhead for inconsistent heuristics

<number>

**Additional text recovered from rendered slide:**
• In the context of A* inconsistency was
considered a bad attribute
• Node re-opening is not a problem with
IDA* because each path to a node is
examined anyway!!

---

### Slide 55 — Pathmax

Pathmax

The pathmax (PMX) method corrects inconsistent heuristics. [Mero 84,Marteli 77]

g=5
h=5
f=10

The child inherits the f-value of the parent if it is larger

Pathmax ony corrects the current path to be consistent, not the entire graph [Holte, SoCS 2010]

1

g=6
h=2 →4
f=8→10

<number>

**Additional text recovered from rendered slide:**
• The pathmax (PMX) method corrects
inconsistent heuristics. [Mero 84,Marteli 77]
h=5 • The child inherits the f-value
Pathmax ony corrects
f=10 of thepath
the current parent
to beifconsistent,
it is larger
not the entire graph [Holte,
g=6 SoCS 2010]

---

### Slide 56 — Bidirectional pathmax (BPMX) — [Felner, Zahavi, Schaeffer, Holte IJCAI-2005]

Bidirectional pathmax (BPMX)[Felner, Zahavi, Schaeffer, Holte IJCAI-2005]

h-values

2

4

BPMX

5

1

3

Bidirectional pathmax: h-values are propagated in both directions decreasing by 1 in each edge.
If the IDA* threshold is 2 then with BPMX the right child will not even be generated!!

<number>

**Additional text recovered from rendered slide:**
Bidirectional pathmax (BPMX)
[Felner, Zahavi, Schaeffer, Holte IJCAI-2005]
5 1 5 3
• Bidirectional pathmax: h-values are
propagated in both directions
decreasing by 1 in each edge.
– If the IDA* threshold is 2 then with BPMX
the right child will not even be generated!! 56

---

### Slide 57 — BPMX within A*

BPMX within A*

BMPX(1)
We have a node p and its children n1, n2 … nk at hand.
Let h’ be the largest heuristic among the children
For each child n we set
h(n)=max(h(n), h’-2)
For the parent p we set
h(p)=max(h(n),h’-1)
Going deeper did not prove to be cost effective.
BPMX(∞) can be great or catastrophic. [See paper]

7

3

6

2

8

<number>

**Additional text recovered from rendered slide:**
– h(n)=max(h(n), h’-2) 3 7
– h(p)=max(h(n),h’-1) 8 2 7 8 6 7

---

### Slide 58 — Achieving inconsistent heuristics

Achieving inconsistent heuristics

Random selection of heuristics (out of K)
Dual evaluations [Zahavi et al AAAI-2006]
Compressed pattern databases [Felner et al. 2007]

<number>

**Additional text recovered from rendered slide:**
• Compressed pattern databases [Felner et al.
2007]

---

### Slide 59 — More than one heuristic

More than one heuristic

A munber of different PDBs
Symmetric lookups
Tile puzzles: reflect the tiles
about the main diagonal.
Rubik’s cube: rotate the cube

7

8

<number>

**Additional text recovered from rendered slide:**
• A munber of different PDBs 7
about the main diagonal. 7 8

---

### Slide 60 — 1) Randomizing a heuristic

1) Randomizing a heuristic

Taking the maximum of K heuristics is
Admissible
Consistent
Better than each of them
Drawbacks: Overhead of K heuristics lookups
diminishing return.
Alternatively, we can randomize which heuristic out of K to consult.
Admissible
Inconsistent
Benefits: Only one look up. BPMX can be activated.

<number>

**Additional text recovered from rendered slide:**
Randomizing a heuristic )1
Alternatively, we can randomize which
heuristic out of K to consult.

---

### Slide 61 — Achieving inconsistent heuristics

Achieving inconsistent heuristics

1) Random selection of heuristics (out of K)
Dual evaluations
are inconsistent
[Zahavi et al. AAAI-2006]
3) Compressed pattern databases
In general – any partial heuristic is inconsistent.

**Additional text recovered from rendered slide:**
2) Dual evaluations

**Speaker notes / hidden notes:**

<number>

---

### Slide 62 — Inconsistency of Dual lookups

Inconsistency of Dual lookups

Consistency of heuristics:
|h(a)-h(b)| <= c(a,b)

Example: Top-Spin
c(b,c)=1

Both lookups for B
PDB[1,2,3,4,5]=0
Regular lookup for C PDB[1,2,3,7,6]=1
Dual lookup for C PDB[1,2,3,8,9]=2

[Table]
| | Regular | Dual |
| --- | --- | --- |
| b | 0 | 0 |
| c | 1 | 2 |

<number>

**Additional text recovered from rendered slide:**
• Regular lookup for C Regular Dual
PDB[1,2,3,7,6]=1
• Dual lookup for C b 0 0
PDB[1,2,3,8,9]=2 c 1 2 62

---

### Slide 63 — Compressing pattern database are inconsistent

Compressing pattern database are inconsistent

3 and 5 are inconsistent

<number>

**Additional text recovered from rendered slide:**
Compressing pattern database
are inconsistent

---

### Slide 64 — Consistent Vs. Inconsistent

Consistent Vs. Inconsistent

Assume:
A threshold of 5
Similar distribution of heuristics at each level

consistent

inconsistent

<number>

**Additional text recovered from rendered slide:**
1)A threshold of 5
2)Similar distribution of heuristics at each level
consistent inconsistent

---

### Slide 65 — Heuristic value distribution

Heuristic value distribution

Notice that all these heuristics have the
same average value

<number>

---

### Slide 66 — Rubik’s cube results

Rubik’s cube results

[Table]
| No | Lookups | Nodes | Time |
| --- | --- | --- | --- |
| 1 | Regular | 90,930,662 | 28.18 |
| 1 | Dual | 19,653,386 | 7.38 |
| 1 | Dual+BPMX | 8,315,116 | 3.24 |
| 1 | Random | 9,652,138 | 3.30 |
| 1 | Random+BPMX | 3,828,138 | 1.25 |
| 2 | Regular | 13,380,154 | 7.85 |
| 4 | Regular | 10,574,180 | 11.60 |

7-edges PDB over 1000 instances of depth 14

<number>

**Additional text recovered from rendered slide:**
edges PDB over 1000 instances of depth 14 -7

---

### Slide 67 — Tile puzzle results

Tile puzzle results

[Table]
| No | Lookups | Nodes | Time |
| --- | --- | --- | --- |
| 1 | Regular | 136,289 | 0.081 |
| 1 | Dual+BPMX | 247,299 | 0.139 |
| 1 | Random+BPMX | 44,829 | 0.029 |
| 2 | Regular+reflected | 36,130 | 0.034 |
| 2 | 2 Random+BPMX | 26,862 | 0.025 |
| 3 | 3 Random+BPMX | 21,425 | 0.026 |
| 4 | All 4 | 18,601 | 0.022 |

7-8 additive PDB over 1000 instances

<number>

**Additional text recovered from rendered slide:**
additive PDB over 1000 instances 7-8

---

### Slide 68 — BPMX: Path finding results — random vs. max

BPMX: Path finding resultsrandom vs. max

<number>

**Additional text recovered from rendered slide:**
BPMX: Path finding results
random vs. max

---

### Slide 69 — Summary: Inconsistent heuristics and BPMX

Summary: Inconsistent heuristics and BPMX

Works great and natural for IDA* and for exponential domains
Has potential for A* and polynomial domains but you have to be careful
Node reopening
BPMX is tricky.

<number>

**Additional text recovered from rendered slide:**
• Works great and natural for IDA* and
for exponential domains
• Has potential for A* and polynomial
domains but you have to be careful

---

### Slide 70 — Dual search

Dual search
[Zahavi et al. AAAI-06,AIJ-2008]

<number>

---

### Slide 71 — Symmetries in PDBs

Symmetries in PDBs

Symmetric lookups
Tile puzzles: reflect the tiles
about the main diagonal.
Rubik’s cube: rotate the cube
We can take the maximum among the different lookups
These are all geometrical symmetries
We suggest a new type of symmetry!!

7

8

<number>

**Additional text recovered from rendered slide:**
• Symmetric lookups 7
• We can take the maximum 7 8
among the different lookups
• These are all geometrical
symmetries
• We suggest a new type of
symmetry!!

---

### Slide 72 — Duality :definition 1

Duality :definition 1

Let S be a state.
Let Π be a permutation such that Π(S)=G
Define: =Π(G)
consequences
Π ( )=G
The length of the optimal path from S to G and from S to G is identical

S

-1

d

An admissible heuristic for S is also admissible for S

<number>

**Additional text recovered from rendered slide:**
• Let Π be a permutation
such that Π(S)=G S
• Define: S d =Π(G) п
• Π-1(S d )=G п
• The length of the
optimal path from S to
d Sd
G and from S to G is
identical
An admissible heuristic for S is also admissible
for S 72

---

### Slide 73 — Regular and dual representation

Regular and dual representation

Regular representation of a problem:
Variables – objects (tiles, cubies etc,)
Values – locations
Dual representation:
Variables – locations
Values – objects

<number>

---

### Slide 74 — Duality :definition 2

Duality :definition 2

Definition 2: For a state S we flip the roles of variables and objects
Assume a vector <3,1,4,2>
Regular representation:
Dual representation:

3

1

4

2

<number>

**Additional text recovered from rendered slide:**
• Definition 2: For a state S we flip the
roles of variables and objects
• Regular representation: 3 1 4 2
2 4 1 3

---

### Slide 75 — Duality

Duality

Claim: Definition 1 and definition 2 are equivalent
Proof: Assume that in S, object j is in location i and that Π(i)=j.
Applying Π for the first time (on S) will move object j to location j.
Applying Π for the second time (on G) will move object i to location j

<number>

**Additional text recovered from rendered slide:**
• Claim: Definition 1 and definition 2 are
equivalent
• Proof: Assume that in S, object j is in location
i and that Π(i)=j.
• Applying Π for the first time (on S) will move
object j to location j.
• Applying Π for the second time (on G) will
move object i to location j

---

### Slide 76 — Using duality

Using duality

Dual lookup: We can take the heuristic of the dual state and use it for the regular state.
In particular we can perform a PDB lookup for the dual state
Dual Search:
This is a novel search algorithm which can be constructed for any known search algorithm

<number>

**Additional text recovered from rendered slide:**
• Dual lookup: We can take the heuristic of
the dual state and use it for the regular
state.
• In particular we can perform a PDB lookup
for the dual state
• This is a novel search algorithm which can
be constructed for any known search
algorithm

---

### Slide 77 — Dual Search

Dual Search

When the search arrives at a state S, we also look at its dual state S.
We might consider to JUMP and continue the search from S towards the goal.
This is a novel version of bidirectional search

d

<number>

**Additional text recovered from rendered slide:**
• When the search arrives at a state S,
we also look at its dual state S.d
• We might consider to JUMP and
continue the search from Sd towards the
goal.
• This is a novel version of bidirectional
search

---

### Slide 78 — Example

Example

S

п

G

(a) No Jumps

(b) One Jump

Traditional Search

Bidirectional Search

Construction of the solution path is possible by applying usual backtracking with some simple modifications.

<number>

**Additional text recovered from rendered slide:**
S d1
(a) No Jumps (b) One Jump
Bidirectional
Traditional
ConstructionSearch
ofSearch
the solution path is possible by
applying usual backtracking with some simple
.modifications 78

---

### Slide 79 — When to jump

When to jump

At every node, a decision should be made whether to continue the search from S or to jump to S
Jumping Policies:
JIL: Jump if larger
JOR: Jump only at the root
J15,J24: Special jumping policies for the 15 and 24 tile puzzles

d

<number>

**Additional text recovered from rendered slide:**
• At every node, a decision should be
made whether to continue the search
from S or to jump to Sd
• J15,J24: Special jumping policies for
the 15 and 24 tile puzzles

---

### Slide 80 — Experimental results

Experimental results

Rubik’s cube: 7-edges PDB. 1000 problem instances.

[Table]
| Heuristic | Search | Policy | Nodes | Time |
| --- | --- | --- | --- | --- |
| r | IDA* | - | 90,930,662 | 28.18 |
| d | IDA* | - | 8,315,116 | 3.24 |
| max(r,d) | IDA* | - | 2,997,539 | 1.34 |
| max(r,d) | DIDA* | JIL | 2,697,087 | 1.16 |
| max(r,d) | DIDA* | JOR | 2,464,685 | 1.02 |

<number>

**Additional text recovered from rendered slide:**
•Rubik’s cube:
7-edges PDB. 1000 problem instances.

---

### Slide 81 — Experimental results

Experimental results

16 Pancake problem 9-tiles PDB. 100 problem instances.

[Table]
| Heuristic | Search | Policy | Nodes | Time |
| --- | --- | --- | --- | --- |
| r | IDA* | - | 342,308,368,717 | 284,054 |
| d | IDA* | - | 14,387,002,121 | 12,485 |
| max(r,d) | IDA* | - | 2,478,269,076 | 3,086 |
| max(r,d) | DIDA* | JIL | 260,506,693 | 362 |

<number>

**Additional text recovered from rendered slide:**
• 16 Pancake problem
9-tiles PDB. 100 problem instances.

---

### Slide 82 — Experimental results

Experimental results

15 puzzle 7-8 tiles PDB. 1000 problem instances from [Korf & Felner 2002]

[Table]
| Heuristic | Search | Policy | Value | Nodes | Time |
| --- | --- | --- | --- | --- | --- |
| r | IDA* | - | 44.75 | 136,289 | 0.081 |
| Max(r,r*) | IDA* | - | 45.63 | 36,710 | 0.034 |
| max(r,r*,d,d*) | IDA* | - | 46.12 | 18,601 | 0.022 |
| max(r,r*,d,d*) | DIDA* | J15 | 46.12 | 13,687 | 0.018 |

<number>

**Additional text recovered from rendered slide:**
• 15 puzzle
7-8 tiles PDB. 1000 problem
instances from [Korf & Felner 2002]

---

### Slide 83 — Experimental results

Experimental results

24 puzzle 6-6-6-6 tiles PDB. 50 Problem instances from [Korf & Felner 2002]

[Table]
| Heuristic | Search | Policy | Nodes |
| --- | --- | --- | --- |
| max(r,r*) | IDA* | - | 43,454,810,045 |
| max(r,r*,d,d*) | IDA* | - | 13,549,943,868 |
| max(r,d*) | DIDA* | J24 | 8,248,769,713 |
| max(r,r*,d,d*) | DIDA* | J24 | 3,948,614,947 |

<number>

**Additional text recovered from rendered slide:**
• 24 puzzle
6-6-6-6 tiles PDB. 50 Problem
instances from [Korf & Felner 2002]

---

### Slide 84 — Conclusions

Conclusions

Duality in search spaces
Two way to use duality:
1) the dual heuristic
2) the dual search
Improvement in performance

<number>

---

### Slide 85 — True distance Heuristics — New Form of  — Memory-based Heuristics

True distance HeuristicsNew Form of Memory-based Heuristics

Ariel Felner Ben-Gurion University, Israel
Nathan Sturtevant University of Alberta, Canada
Jonathan Schaeffer University of Alberta, Canada
More will appear in [IJCAI-09]

<number>

**Additional text recovered from rendered slide:**
True distance Heuristics
New Form of
Memory-based Heuristics

---

### Slide 86 — A*

A*

A* is a best-first search algorithm that uses f(n)=g(n)+h(n) as its cost function.
g(n): Real distance from the initial state to n
h(n): The estimated remained distance from n to the goal state.
f(n): in A* is an estimation of the shortest path to the goal via n.

<number>

**Additional text recovered from rendered slide:**
• A* is a best-first search algorithm that uses
f(n)=g(n)+h(n) as its cost function.
• h(n): The estimated remained distance from n
to the goal state.
• f(n): in A* is an estimation of the shortest path
to the goal via n.

---

### Slide 87 — Heuristic Functions: h(n)

Heuristic Functions: h(n)

Better heuristics: more parts of the search tree will be pruned.
Memory-based heuristics:
Pattern Databases
True-Distance Heuristics

<number>

**Additional text recovered from rendered slide:**
• Better heuristics: more parts of the search tree
will be pruned.

---

### Slide 88 — Different Domain Types

Different Domain Types

[Table]
| | Exponential Domains | Polynomial (Quadratic) Domains |
| --- | --- | --- |
| Example | Permutation puzzles. | Path-finding in Maps, GPS / Sequence alignment |
| Space size N | N=O(bd) | N=O(d2) |
| # of states | 1015 | 1,000,000 |
| Solution | Optimal | Suboptimal |
| Search time | Days (optimal) | Real time (suboptimal) |
| Start-Goal | Goal specific | Any two states |

<number>

**Additional text recovered from rendered slide:**
Exponential Domains Polynomial (Quadratic)
Domains
Example .Permutation puzzles Path-finding in Maps, GPS
Sequence alignment

---

### Slide 89 — Homomorphic Abstractions

Homomorphic Abstractions

Many search spaces can be abstracted by merging nodes into abstract nodes
Distances from abstract spaces are lower bounds for the original problem

2

3

<number>

**Additional text recovered from rendered slide:**
• Many search spaces can be abstracted by
merging nodes into abstract nodes
2 3 2
• Distances from abstract spaces are lower
bounds for the original problem

---

### Slide 90 — Abstractions – exponential domains

Abstractions – exponential domains

Effective in exponential domains
b-branching factor d-depth/radius
Full problem size bd=N
Abstract state size = N/f w - new radius.
bw=bd/f
w=d-logb(f) (constant loss)
PDBs – are homomorphic abstractions

10^19 States

abstraction

10^8 states

Average distance 18

Average distance 11

<number>

**Additional text recovered from rendered slide:**
10^19 States 10^8 states
Average distance 18 Average distance 11

---

### Slide 91 — Abstractions – polynomial domains

Abstractions – polynomial domains

But, in polynomial domains
Spaces grows quadratically with d.
Full problem size d2=N
Abstract state size = N/f
w2=d2/f w=d/sqrt(f) (significant loss)

<number>

---

### Slide 92 — Abstractions in Maps

Abstractions in Maps

[Table]
| | |
| --- | --- |
| 11,614 states / Width: 157 | 3,455 states / Width: 80 |

2

3

<number>

**Additional text recovered from rendered slide:**
states 11,614 states 3,455
Width: 157 Width: 80
2 3 2

---

### Slide 93 — True Distance Heuristics

True Distance Heuristics

Useful in domains that fit in memory
Especially for polynomial domains
Useful where we need (optimal) solutions very fast. (e.g. real time games, GPS)
Some of these ideas were used before
[Bjornsson and Halldorsson, AIIDE 2006]
[Goldberg and Harrelson, SODA 2005]

<number>

**Additional text recovered from rendered slide:**
• Useful where we need (optimal) solutions
very fast. (e.g. real time games, GPS)

---

### Slide 94 — True Distance Heuristics

True Distance Heuristics

All-pairs Shortest Paths data (APSP)
Good for any two states
Time O(N3) (floyd-Warshal)
Memory - N2
Assume we have O(N) memory.
Let’s abstract this data too
True distance heuristic abstraction

[Table]
| | Boston | Chicago | NYC | LA |
| --- | --- | --- | --- | --- |
| Boston | 0 | 679 | 234 | 4565 |
| Chicago | 679 | 0 | 876 | 3879 |
| NYC | 234 | 876 | 0 | 4476 |
| LA | 4565 | 3879 | 4476 | 0 |

<number>

---

### Slide 95 — Abstracting APSP

Abstracting APSP

Differential heuristics
Canonical heuristics
Border heuristics

All pairs

Differential

Canonical/border

<number>

**Additional text recovered from rendered slide:**
All pairs Differential Canonical/border

---

### Slide 96 — Differential heuristics

Differential heuristics

Choose k pivot states
Store shortest paths to each of these states from all N states.
Memory: k*N
Time: k* N
hx(a, b) = | d(a, x) - d(b,x) |
Which x to use??? (max of all)

x

d(a, x)

a

d(b, x)

b

<number>

**Additional text recovered from rendered slide:**
• Store shortest paths to each of these
states from all N states. x
• Time: k* N a
Which x to use??? (max of all) 96

---

### Slide 97 — Differential Heuristic

Differential Heuristic

Placement strategies are discussed in [IJCAI-09]

<number>

---

### Slide 98 — Canonical heuristics

Canonical heuristics

Choose K (out of N) canonical states
Primary data: Store all pairs shortest paths
among all these K states
Secondary data: From every state (out of N) store distance to the closest canonical state
Memory: k2 (primary) + 2N (secondary)
Time: k* N
hx,y(a, b) = | d(x,y) - d(a,x)- d(b,y) |

d(x, y)

x

y

d(b, y)

d(a, x)

a

b

<number>

**Additional text recovered from rendered slide:**
• Secondary data: From every state (out of N) store
distance to the closest canonical state
d(a, x) d(b, y)

---

### Slide 99 — All states

All states

<number>

---

### Slide 100 — Primary Data

Primary Data

a

x

b

y

<number>

**Additional text recovered from rendered slide:**
100

---

### Slide 101 — Primary & Secondary Data

Primary & Secondary Data

h(a, b) = | d(x,y) - d(a,x)- d(b,y) |

a

x

b

y

<number>

**Additional text recovered from rendered slide:**
101

---

### Slide 102 — Extended secondary data

Extended secondary data

K = number of canonical states
d: For each state, store distance to d closest canonical states.
Memory: K^2 (primary)
+ 2d*N (secondary)
Time : K*N
h(a, b) = max{ all(x,y), | d(x,y) - d(a,x)-d(b,y) |}

<number>

**Additional text recovered from rendered slide:**
• d: For each state, store distance to d
closest canonical states.
102

---

### Slide 103 — Fix memory at 10N

Fix memory at 10N

[Table]
| | Total Memory | k (# states) | d (# distances) |
| --- | --- | --- | --- |
| Differential | 10N | 10 | 10 |
| Canonical | 10N | √(8N) | 1 |
| | 10N | √(6N) | 2 |
| | 10N | √(4N) | 3 |
| | 10N | √(2N) | 4 |

Total memory = k2 + 2dN

<number>

**Additional text recovered from rendered slide:**
Total
k (# states) d (# distances)
Memory
Differentia
10N 10 10
10N )8N(√ 1
Canonical 10N )6N(√ 2
Total memory = k2 + 2dN 103

---

### Slide 104 — Example

Example

Start

Goal

<number>

**Additional text recovered from rendered slide:**
104

---

### Slide 105 — Slide 105

<number>

**Additional text recovered from rendered slide:**
105

---

### Slide 106 — Experimental Results

Experimental Results

Pathfinding
8-puzzle
4-peg Towers of Hanoi

<number>

**Additional text recovered from rendered slide:**
106

---

### Slide 107 — Room-based Map

Room-based Map

<number>

**Additional text recovered from rendered slide:**
• Room-based Map 107

---

### Slide 108 — Pathfinding (room maps)

Pathfinding (room maps)

512x512 maps composed of 16x16 rooms
Path length 256 to 512
5 different maps
Average over 3200 problems (650 per map)
Search using A*
Default heuristic: Octile (8-connected grid)

<number>

**Additional text recovered from rendered slide:**
108

---

### Slide 109 — Diffrential against APSP

Diffrential against APSP

<number>

**Additional text recovered from rendered slide:**
109

---

### Slide 110 — Experimental Results - 10N memory

Experimental Results - 10N memory

[Table]
| d | k | Nodes | | Avg. h | Time |
| --- | --- | --- | --- | --- | --- |
| octile | | 21,354 | | 309 | 0.296 |
| Canonical | | | | | |
| 1 | 1448 | 8,698 | | 372 | 0.123 |
| 2 | 1254 | 6,011 | | 375 | 0.091 |
| 3 | 1042 | 5,472 | | 376 | 0.083 |
| 4 | 724 | 5,646 | | 373 | 0.092 |
| Differential | | | | | |
| 10 | 10 | 3,479 | | 370 | 0.054 |
| All pairs | | ~1,000 | | 385 | ? |

<number>

**Additional text recovered from rendered slide:**
110

---

### Slide 111 — Actuated Robotic Arm

Actuated Robotic Arm

Move arm configuration so that tip is on new x/y location
Most heuristics poor
Two ideas:
Reverse search
Use differential heuristic

<number>

**Additional text recovered from rendered slide:**
• Move arm configuration so that tip is on new
x/y location
Arm.mov
111

---

### Slide 112 — Robotic Arm Results

Robotic Arm Results

[Table]
| | Nodes | h-value | | Time (sec) | |
| --- | --- | --- | --- | --- | --- |
| Distance | 4.04M | 90.0 | | 278.3 | |
| Reverse | 1.98M | 209.9 | | 31.5 | |
| Differential (1) | 610k | 223.2 | | 10.3 | |
| Differential (2) | 214k | 226.7 | | 3.6 | |
| Differential (3) | 162k | 227.7 | | 2.9 | |
| Differential (4) | 140k | 228.0 | | 2.5 | |

564x faster when solving full problem set

<number>

**Additional text recovered from rendered slide:**
Time
Nodes h-value
(sec)
564x faster when solving full problem112set

**Speaker notes / hidden notes:**

<number>
4.3 million average over entire problem set for distance heuristic
40 hours total to solve
256 seconds for entire set vs. 144,501

---

### Slide 113 — The 8-puzzle

The 8-puzzle

Has N=181,440 states.
Normal PDBs are not effective for any pair of start and goal states
Neighborhoods According to blank’s position

<number>

**Additional text recovered from rendered slide:**
• Normal PDBs are not
effective for any pair of
start and goal states
• Neighborhoods According
to blank’s position
113

---

### Slide 114 — Experimental Results – 8 puzzle

Experimental Results – 8 puzzle

[Table]
| H | K | D | Nodes | | Avg. h | Mem |
| --- | --- | --- | --- | --- | --- | --- |
| MD | | | 3,000 | | 14.21 | None |
| DH | 1 | 1 | 2941 | | 14.26 | 1N |
| DH | 5 | 5 | 2784 | | 14.34 | 5N |
| DH | 10 | 10 | 2570 | | 14.41 | 10N |
| CH | 1024 | 1 | 2376 | | 14.50 | 10N |
| DH | 50 | 50 | 2184 | | 14.95 | 50N |
| DH | 200 | 200 | 832 | | 16.11 | 200N |
| CH | 20,160 | 1 | 345 | | 18.53 | 1120N |
| CH | 20,160 | 3 | 69 | | 19.83 | 1120N |

<number>

**Additional text recovered from rendered slide:**
114

---

### Slide 115 — Border Heuristics

Border Heuristics

Abstract the domain into K disjoint (canonical) regions
For example, divide the world into countries
A border state is a state at one region which has a neighbor at another region
The border heuristic keeps the shortest distance between borders of regions

<number>

**Additional text recovered from rendered slide:**
• Abstract the domain into K disjoint
(canonical) regions
• For example, divide the world into
countries
• A border state is a state at one region
which has a neighbor at another region
• The border heuristic keeps the
shortest distance between borders of
regions
115

---

### Slide 116 — Border Heuristics

Border Heuristics

Canonical Region X

Canonical Region Y

b

a

<number>

**Additional text recovered from rendered slide:**
Canonical Canonical
Region X Region Y
116

---

### Slide 117 — Border Heuristics

Border Heuristics

Canonical Region X

Canonical Region Y

d(X,Y)

b

a

<number>

**Additional text recovered from rendered slide:**
Canonical Canonical
Region X d(X,Y) Region Y
117

---

### Slide 118 — Border Heuristics

Border Heuristics

Canonical Region X

Canonical Region Y

d(X,Y)

b

a

bd(b)

bd(a)

h(a, b) = d(X,Y) + db(a)+ db(y)

<number>

**Additional text recovered from rendered slide:**
Canonical Canonical
Region X d(X,Y) Region Y
118

---

### Slide 119 — Border Heuristic

Border Heuristic

For each pair of regions store the minimum between border states
Memory : K2 (Primary)
+ N (secondary)
Time: K N
How to divide into regions?

<number>

**Additional text recovered from rendered slide:**
• For each pair of regions store the
minimum between border states
119

---

### Slide 120 — 4-peg Towers of Hanoi:

4-peg Towers of Hanoi:

Compressed PDBS are border heuristics

There is a conjecture about the length of optimal path but it was not proven.
Size 4^k
Additive pattern databases
[Felner, Korf & Hanan, JAIR-04]

<number>

**Additional text recovered from rendered slide:**
:peg Towers of Hanoi-4
• There is a conjecture about the length of
optimal path but it was not proven.
120

---

### Slide 121 — Additive PDBS for TOH4

Additive PDBS for TOH4

Consider the 10 larger disks
Store the cost configuration of
10 disks in a PDB.
Size 4^10
The largest database that we stored was of 14 disks which needed 4^14=256MB.
PDBs can be compressed
[Felner, Korf, Mehuslam and Holte JAIR-07]

6

10

<number>

**Additional text recovered from rendered slide:**
10 disks in a PDB. 6
• The largest database that we
stored was of 14 disks which
needed 4^14=256MB. 10
121

---

### Slide 122 — Compressing Cliques

Compressing Cliques

The values in a PDB for a clique are d or d+1

d

G

d+1

Usually they have nearby entries in the PDB
A[4][4][4][4][4] A[4][4][4][4][1]

A clique in TOH4

<number>

**Additional text recovered from rendered slide:**
• The values in a PDB for
a clique are d or d+1 d
122

---

### Slide 123 — Compressing PDBS

Compressing PDBS

This can be generalized to compressing any number of smallest disks
A[4][4][4][4][4] [4][4] A[4][4][4][4]

<number>

**Additional text recovered from rendered slide:**
• This can be generalized to compressing any
number of smallest disks
123

---

### Slide 124 — Uncompressed PDB

Uncompressed PDB

goal

a

PDB(a)

<number>

**Additional text recovered from rendered slide:**
a PDB(a)
124

---

### Slide 125 — Compressed PDBs

Compressed PDBs

goal

a

PDB_compressed[C(a)]

<number>

**Additional text recovered from rendered slide:**
a PDB_compressed[C(a)]
125

---

### Slide 126 — Border TDHs

Border TDHs

bd(a)

goal

a

TDH(goal,X)

Region X

<number>

**Additional text recovered from rendered slide:**
bd(a) goal
126

---

### Slide 127 — Border TDHs

Border TDHs

bd(a)

goal

a

TDH(goal,X)

Region X

The region: all states with fixed location of the “uncompressed” large disks
Border states: all state where one of the large disks can move

<number>

**Additional text recovered from rendered slide:**
bd(a) goal
• The region: all states with
fixed location of the
“uncompressed” large disks
• Border states: all state where
one of the large disks can move
127

---

### Slide 128 — TOH4 results

TOH4 results

<number>

**Additional text recovered from rendered slide:**
128

---

### Slide 129 — Summary

Summary

Previous work on memory-based heuristics was orientated towards exponential domains
New heuristics for domains that fit in memory
Differential Heuristics
Canonical Heuristics
Border Heuristic
Significant improvements in many domains

<number>

**Additional text recovered from rendered slide:**
• Previous work on memory-based heuristics
was orientated towards exponential domains
129

---

### Slide 130 — Future (ongoing) work

Future (ongoing) work

How many canonical states
Placement of canonical states
Deeper comparison of these heuristics
More variants
Fine-tuned algorithms (Unidirectional bidirectional search)
How do we compute the tables efficiently
Other domains

<number>

**Additional text recovered from rendered slide:**
130

---

### Slide 131 — Different Domain Types

Different Domain Types

[Table]
| | Exponential Domains | Polynomial (Quadratic) Domains |
| --- | --- | --- |
| Example | Permutation puzzles. Planning problems | Path-finding in Maps, GPS / Sequence alignment |
| Input | Implicitly given (large) | explicitly given (large) |
| Space size N | N=O(bd) | N=O(d2) |
| Typical #states | 1015 | 1,000,000 |
| Search time | Days (optimal) | Real time (suboptimal) |
| Algorithms | DFS based algorithms (IDA*) | BFS based algorithms (A*) |
| Memory-based heuristics | Pattern databases (PDBs) | True-distance heuristics (TDHs) |

<number>

**Additional text recovered from rendered slide:**
Exponential Domains Polynomial (Quadratic)
Domains
Example Permutation puzzles. Path-finding in Maps, GPS
Planning problems Sequence alignment
Memory-based Pattern databases (PDBs) True-distance heuristics
heuristics (TDHs)
131

---

### Slide 132 — Multi-agent path finding

Multi-agent path finding

A path for each agent, such that the different paths won’t overlap
Task: Minimize the total travel cost
Goal test: whether each agent is in its goal location.

<number>

**Additional text recovered from rendered slide:**
• A path for each agent, such that the
different paths won’t overlap
• Goal test: whether each agent is in its
goal location.
132

---

### Slide 133 — Motivation

Motivation

Robotics
Video games
Vehicle routing
Air/Train traffic control

<number>

**Additional text recovered from rendered slide:**
133

---

### Slide 134 — Multi-agent path finding

Multi-agent path finding

<number>

**Additional text recovered from rendered slide:**
134

---

### Slide 135 — Multi-agent path finding — N nodes, K agents

Multi-agent path findingN nodes, K agents

For k=1 (Explicit graphs and TDH)

For K=N-1 (Tile puzzle and PDBs)

What about 1 < K < N-1?

<number>

**Additional text recovered from rendered slide:**
Multi-agent path finding
N nodes, K agents
• For k=1 (Explicit For K=N-1 (Tile
graphs and TDH) puzzle and PDBs)
135

---
