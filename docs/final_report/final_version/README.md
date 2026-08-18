# Final report (working copy)

AAAI’27 camera-ready course report for 237-2-5513. Do not edit [`../AuthorKit27`](../AuthorKit27) (that tree is gitignored). `aaai2027.sty` and `aaai2027.bst` in this folder are the locked copies used to compile the report.

## Build

PDFLaTeX only. From this directory:

```text
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

- `aaai2027.sty` already selects `aaai2027.bst`. Do not add `\bibliographystyle`.
- No `hyperref`, no `pgfplots`.
- `\nocopyright` is required by the course (overrides the kit’s publication warning).
- `\usepackage{aaai2027}` has no `[submission]` option (that option hides authors).
- End matter: `\bibliography{references}` then `\appendix` (keeps References unnumbered).

Draft uses `\input{sections/...}` for gated review (flatten later if required). Chapters follow the course four parts (§2): Introduction and Literature Review; Methodology; Experimental Results; Experimental Conclusions and Summary. `figures/` is empty until Phase 5 (`scripts/paper_figures.py`).

Build artifacts (`*.aux`, `*.log`, `main.pdf`, …) are gitignored. Compile locally with the commands above.

## Files

| Path | Role |
| --- | --- |
| `main.tex` | Camera-ready driver (`\input` of `sections/`) |
| `sections/*.tex` | One file per section (Phase 1 skeleton; later phases fill these) |
| `references.bib` | Empty until the bibliography phase; keys must match `PAPER_SOURCE_MAP.md` |
| `aaai2027.sty`, `aaai2027.bst` | Copied from AuthorKit; do not modify |
| `notes/source_map.md` | Internal. The only place excluded-era paths may be named. **Not compiled.** |

## Placeholders still needed

- Author names, emails
- Public code URL (`links` environment)
- Hardware/OS/Python string (methodology phase)
