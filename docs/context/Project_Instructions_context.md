# Search in Artificial Intelligence - Project Submission Instructions

## Source metadata

- **University:** Ben-Gurion University of the Negev
- **Faculty:** Faculty of Computer and Information Sciences
- **Course:** Search in Artificial Intelligence
- **Course number:** `237-2-5513`
- **Document type:** Project submission instructions
- **Original language:** Hebrew
- **Source file:** `instructions.pdf`
- **Source length:** 2 pages

---

## Purpose of this Markdown file

This file converts the official project instructions into a structured, Cursor-friendly reference. It should be treated as the authoritative source for:

- the project's academic purpose;
- the expected report structure;
- the grading emphasis for each report section;
- methodological and reproducibility expectations;
- report-format recommendations;
- acceptable project directions;
- project ideas explicitly suggested by the course staff;
- project types that may receive a low grade.

The explanations below reorganize the source content for clarity but do not add new course requirements.

---

# 1. General project requirements

## 1.1 Project purpose

The project is intended to be a **practical research project** in one of the subjects studied in the course.

Students are expected to:

1. choose a search-related research topic;
2. perform a practical implementation or empirical investigation;
3. run experiments;
4. analyze the results;
5. draw conclusions;
6. submit a laboratory report describing the research, results, and conclusions.

## 1.2 Team size

- The project may be submitted **in pairs only**.

## 1.3 Expected nature of the work

The project should not be only an implementation exercise. It should include a meaningful research or experimental component, such as:

- reproducing prior work;
- comparing approaches;
- adapting a method to a new domain;
- proposing and evaluating an algorithmic modification;
- performing a systematic empirical analysis.

## 1.4 Flexibility of report organization

The document describes a typical report structure, but the course explicitly allows flexibility.

- Students may use a different report structure when it presents their project more effectively.
- The alternative structure should still communicate the research question, methodology, results, and conclusions clearly.

---

# 2. Expected report structure

The standard report contains four central parts:

1. Introduction and literature review
2. Methodology
3. Experimental results
4. Experimental conclusions and summary

The report must also contain a link to the project code.

---

# 3. Introduction and literature review

## 3.1 Purpose of the section

This section should establish the scientific and technical context of the project.

It should:

- introduce the background of the topic;
- explain the motivation for choosing the topic;
- define the problem or research objective clearly;
- review relevant papers, methods, and prior work;
- compare existing approaches;
- explain the project's contribution, distinction, or unique angle.

## 3.2 Required content

A strong introduction and literature review should answer questions such as:

- What problem is being studied?
- Why is this problem important or interesting?
- What search algorithms or heuristic approaches are relevant?
- What has already been investigated in the literature?
- How do the relevant methods differ?
- What gap, extension, reproduction, or comparison does this project address?
- What exactly is the project's research objective?

## 3.3 Grading emphasis

This section is evaluated based on:

- the quality and scope of the literature review;
- the demonstrated understanding of the sources;
- the depth of analysis rather than merely listing papers;
- the clarity and strength of the motivation;
- correct and consistent citations;
- correct and consistent bibliography usage;
- logical organization;
- clarity of writing;
- proper academic writing style.

## 3.4 Implications for the SFBDS F2F-vs-F2E project

For the current project, this section should likely establish:

- what bidirectional search is;
- what Single-Frontier Bidirectional Search (SFBDS) is;
- what Front-to-End (F2E) and Front-to-Front (F2F) heuristics are;
- why F2F may be more informed but more computationally expensive;
- why comparing runtime alone is insufficient;
- why generated nodes, expanded nodes, memory, and solution quality are relevant metrics;
- what previous studies have said about bidirectional heuristic search.

These are project-specific applications of the official section requirements, not additional requirements stated verbatim in the source.

---

# 4. Methodology

## 4.1 Purpose of the section

This section should describe the work process and technical design in a clear, detailed, and reproducible manner.

It should explain:

- the research or development process;
- the selected algorithms;
- the technologies used;
- the data structures used;
- the working environment;
- the chosen evaluation and testing methods;
- the implementation stages;
- data collection or processing, when applicable;
- how the system's results are examined.

## 4.2 Required level of detail

The methodology should be detailed enough for another person to understand how the project was performed and, ideally, reproduce the experiments.

It should not merely state that an algorithm was implemented. It should explain important choices such as:

- which algorithmic variant was used;
- how OPEN and CLOSED were represented;
- how ties were broken;
- how duplicate states were handled;
- how the heuristic was computed;
- which domain instances were used;
- how experiments were repeated;
- which metrics were collected;
- how runtime and memory were measured;
- what hardware and software environment was used.

## 4.3 Grading emphasis

This section is evaluated based on:

- the detail and clarity of the methodology;
- the suitability of the methodology for the project's objectives;
- professional justification of technical choices;
- consistency of the workflow;
- reproducibility of the process.

## 4.4 Implications for the SFBDS F2F-vs-F2E project

For the current project, the methodology should likely document at least:

- the exact SFBDS algorithm implemented;
- the exact definitions of the F2E and F2F heuristic variants;
- whether both versions share the same implementation except for the heuristic;
- grid representation;
- move model and edge costs;
- obstacle generation or benchmark source;
- start and goal generation;
- admissibility and consistency assumptions;
- duplicate detection;
- priority-queue ordering and tie-breaking;
- stopping condition;
- solution reconstruction;
- experimental instance groups;
- runtime measurement procedure;
- generated-node count;
- expanded-node count;
- memory measurement;
- solution-cost verification;
- number of repetitions and random seeds.

Again, this subsection translates the official methodology expectations into the context of the selected project.

---

# 5. Experimental results

## 5.1 Purpose of the section

This section should present the findings of the project and the experiments clearly and systematically.

## 5.2 Expected forms of presentation

Results should be displayed using suitable forms such as:

- tables;
- graphs;
- charts;
- other relevant visualizations.

Every table or figure should be accompanied by explanation and analysis.

## 5.3 Required analysis

The report should explain:

- what the results show;
- what can be concluded from them;
- whether they support or contradict the project's objectives or hypotheses;
- how they relate to previous methods or prior work;
- under which conditions one method performs better;
- whether improvements in one metric create costs in another metric.

## 5.4 Grading emphasis

This section is evaluated based on:

- the quality of data presentation;
- the clarity of tables and graphs;
- the depth of the analysis;
- the quality of the discussion;
- the ability to draw evidence-based conclusions.

## 5.5 Implications for the SFBDS F2F-vs-F2E project

The experimental results should likely compare the two heuristic approaches across metrics such as:

- runtime;
- generated nodes;
- expanded nodes;
- maximum or average memory use;
- heuristic-computation overhead;
- solution cost;
- success or failure rate;
- scaling behavior with grid size, obstacle density, or path difficulty.

Useful analyses may include:

- cases where F2F reduces node expansions but still runs slower;
- cases where the additional F2F computation is worthwhile;
- cases where F2E is sufficient;
- the relationship between heuristic strength and total runtime;
- the break-even point between search reduction and heuristic overhead.

These are appropriate interpretations of the official result-analysis requirements for the selected topic.

---

# 6. Experimental conclusions and summary

## 6.1 Purpose of the section

This section should combine the findings into a coherent overall conclusion and relate them directly to the original project goals.

## 6.2 Required content

The section should:

- summarize the main work performed;
- emphasize the project's central contribution;
- state the conclusions derived from the experiments;
- determine whether the project goals were achieved;
- explain what can be learned from the results;
- discuss limitations discovered during the project;
- optionally propose future improvements or directions.

## 6.3 Grading emphasis

This section is evaluated based on:

- clarity of the conclusions;
- direct connection between conclusions and project objectives;
- depth of overall understanding;
- coherence of the final picture;
- critical reflection;
- quality of proposed future directions.

## 6.4 Expected length

- This section is generally expected to be **shorter than the other major sections**.

## 6.5 Implications for the SFBDS F2F-vs-F2E project

The conclusions should directly answer the project's central question:

> Under which grid and heuristic conditions does Front-to-Front provide enough search reduction to justify its additional computational cost compared with Front-to-End?

The conclusion should avoid a simplistic statement such as "F2F is better" or "F2E is faster." It should identify the conditions and trade-offs supported by the experiments.

---

# 7. Code availability requirement

The report must include:

- a link to the code used to run the experiments;
- the code used to prepare the project graphs.

For reproducibility, the repository should ideally contain:

- implementation source code;
- experiment-running scripts;
- configuration files;
- benchmark or instance-generation instructions;
- raw or processed result files;
- plotting scripts;
- a README explaining how to reproduce the reported results.

Only the requirement to include the code link is explicitly stated in the source. The repository-organization items above are practical recommendations that support the document's reproducibility criterion.

---

# 8. Report format

## 8.1 Recommended format

- The recommended format is **AAAI'27**.
- The intention is to prepare the report in a **camera-ready** style.
- Other formats are permitted.

## 8.2 Copyright footnote

The document recommends using:

```latex
\nocopyright
```

This command is intended to remove the copyright footnote from the first page.

## 8.3 Important interpretation

The AAAI format is recommended rather than mandatory. Regardless of template choice, the report should remain:

- academically written;
- clearly structured;
- consistently cited;
- visually readable;
- suitable for presenting experimental research.

---

# 9. Acceptable directions for selecting a project idea

A project may be based on one or more of the following directions.

## 9.1 Reproduction and adaptation of an existing paper

Possible structure:

1. reproduce an existing method or paper;
2. adapt it to a domain not examined in the original work;
3. evaluate its performance under conditions different from those in the original study.

The project should include more than merely copying the original experiment. The adaptation or new conditions should create a meaningful empirical question.

## 9.2 Modification, extension, or improvement of an existing algorithm

Examples mentioned by the instructions include changing:

- an evaluation function;
- an expansion strategy;
- a search mechanism.

The modification must satisfy two conditions:

- there is a clear motivation for the change;
- its contribution can be evaluated experimentally.

## 9.3 Testing existing heuristic-search algorithms in a new domain

Possible structure:

1. select a new domain;
2. implement or apply existing heuristic-search algorithms;
3. conduct extensive tests;
4. compare multiple methods;
5. analyze performance;
6. derive conclusions.

---

# 10. Project ideas explicitly suggested in the instructions

The list below is not exhaustive. Students may and are encouraged to propose additional ideas.

## 10.1 SFBDS with F2F versus F2E heuristics

- Compare Single-Frontier Bidirectional Search using a Front-to-Front heuristic against the corresponding Front-to-End heuristic.
- This is the selected project topic in the current repository.

## 10.2 Reproduction of the Explicit Estimation Search error model

- Reproduce the error model of Explicit Estimation Search.
- Reproduce the paper's results, specifically on the 15 Puzzle.

## 10.3 Best-First Search on Sorting Colored Balls in Colored Tubes

- Test different Best-First Search algorithms on the problem:
  - `Sorting Colored Balls in Colored Tubes`.

## 10.4 Correcting the PEA* + IDA* memory-bound analysis

- Correct the referenced work so that `CLOSED` is also considered when checking the memory bound.
- Compare the corrected analysis or implementation against the results reported in the paper.

## 10.5 Learning a heuristic function with a neural network

- Learn a heuristic function using a neural network.
- Possible learning paradigms mentioned:
  - supervised learning;
  - reinforcement learning.

## 10.6 Bidirectional search on 3D pathfinding voxel benchmarks

- Test bidirectional-search algorithms on:
  - `Voxel Benchmarks for 3D Pathfinding`.

## 10.7 Reproducing the WMM anomaly

- Reproduce the WMM anomaly on the domains studied in the paper.
- Extend the evaluation to additional domains.

## 10.8 Parallelizing algorithms without a parallel version

- Select existing search algorithms that do not yet have a parallel implementation.
- Design and evaluate a parallel version.

## 10.9 Vertex-priority functions in suboptimal search

- Test different vertex-priority functions in:
  - bounded suboptimal search;
  - unbounded suboptimal search.
- Study them both:
  - in a single-evaluation-function context;
  - inside a Focal Search structure.

## 10.10 Search-based agent for a strategy game

- Build a search-based agent for a strategy game.
- Compare it with a baseline such as:
  - a random agent;
  - a rule-based agent;
  - a human player;
  - another appropriate threshold or benchmark agent.

### Games to avoid

The instructions recommend avoiding very popular games such as:

- Chess;
- Checkers;
- Connect Four;
- Backgammon.

### Suggested game examples

The instructions mention:

- Ultimate Tic-Tac-Toe;
- Attax;
- Abalone;
- other suitable strategy games.

---

# 11. Project ideas that may receive a low grade

The instructions warn that several common project ideas may receive a low grade because they are:

- very common;
- relatively simple to implement;
- limited in uniqueness;
- limited in research novelty or interest.

The specifically discouraged comparisons are:

## 11.1 A* versus IDA* on common literature domains

A basic comparison of A* and IDA* on standard benchmark domains may be viewed as insufficiently original.

## 11.2 BFS versus DFS

A basic BFS-versus-DFS comparison is considered too simple and too common.

## 11.3 Minimax versus Alpha-Beta pruning

A basic comparison between Minimax and Alpha-Beta pruning is considered too standard and limited in novelty.

---

# 12. Authoritative checklist for the current project

The following checklist translates the official instructions into concrete project tasks.

## 12.1 Research framing

- [ ] Define SFBDS clearly.
- [ ] Define F2F clearly.
- [ ] Define F2E clearly.
- [ ] State the research question.
- [ ] Explain why the comparison is meaningful.
- [ ] Review and compare relevant literature.
- [ ] Identify the project's empirical contribution.

## 12.2 Implementation and methodology

- [ ] Implement a reproducible SFBDS baseline.
- [ ] Implement the F2E variant.
- [ ] Implement the F2F variant.
- [ ] Keep non-heuristic implementation choices controlled between variants.
- [ ] Document OPEN, CLOSED, duplicates, tie-breaking, and stopping conditions.
- [ ] Define grid domains and instance-generation rules.
- [ ] Record software and hardware environment.
- [ ] Fix or record random seeds.
- [ ] Define all evaluation metrics before running the final experiments.

## 12.3 Experiments

- [ ] Compare runtime.
- [ ] Compare generated nodes.
- [ ] Compare expanded nodes.
- [ ] Compare memory usage.
- [ ] Verify solution cost and correctness.
- [ ] Measure F2F heuristic overhead where possible.
- [ ] Test multiple grid sizes.
- [ ] Test multiple obstacle densities or difficulty levels.
- [ ] Repeat randomized experiments.
- [ ] Aggregate results systematically.

## 12.4 Results presentation

- [ ] Present clear tables.
- [ ] Present relevant graphs.
- [ ] Label axes, units, and experimental conditions.
- [ ] Explain every major result.
- [ ] Discuss both advantages and disadvantages.
- [ ] Relate findings to the literature.
- [ ] Avoid conclusions unsupported by the data.

## 12.5 Conclusions

- [ ] Answer the research question directly.
- [ ] State whether project goals were achieved.
- [ ] Explain when F2F is worthwhile.
- [ ] Explain when F2E is preferable.
- [ ] Document limitations.
- [ ] Propose meaningful future work.

## 12.6 Submission and reproducibility

- [ ] Include a link to the source-code repository in the report.
- [ ] Include experiment scripts.
- [ ] Include graph-generation scripts.
- [ ] Include instructions for reproducing results.
- [ ] Use AAAI'27 format or another clearly justified format.
- [ ] Use `\nocopyright` when appropriate in the AAAI template.

---

# 13. Recommended repository role for this file

A suitable location is:

```text
docs/context/project_submission_instructions.md
```

Cursor should use this file as the official requirements reference when:

- planning the project structure;
- drafting the report outline;
- deciding which metrics to log;
- reviewing experiment reproducibility;
- checking whether the report satisfies the course requirements;
- identifying missing sections before submission.

---

# 14. Source-faithfulness note

The following points are directly stated in the source document:

- the project is practical research;
- submission is in pairs only;
- the typical report sections and their grading emphases;
- the requirement to link the code used for experiments and graphs;
- the AAAI'27 format recommendation;
- the `\nocopyright` recommendation;
- the three general project-selection directions;
- the list of suggested project ideas;
- the list of project comparisons that may receive a low grade.

Project-specific checklists and SFBDS examples in this Markdown file are structured interpretations designed to apply those official requirements to the selected project. They should not be treated as additional formal requirements unless confirmed by the instructor.
