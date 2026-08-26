# Informational-Dynamics-of-Time

Research program for deriving temporal dynamics from informational principles, starting from Kähler geometry, tensor--scalar temporal fields, and phase/information flow, and only later coupling the resulting temporal branch to space through Einstein closure.

## Current milestone

- Theory state: `v0.5.0-local`
- Evidence state: `v0.5.0-local`
- Native algorithm package: `src/idt/`
- Figure-generation pipeline: `scripts/build_figures.py`
- Monograph source: LaTeX only under `monograph/`
- Repository figures: generated SVG previews under `monograph/figures/`
- Compiled PDF is intentionally not tracked.

## Reproduce the figures

Run:

```bash
PYTHONPATH=. python3 scripts/build_figures.py
```

This regenerates local PNG assets used by LaTeX and SVG previews suitable for repository viewing.

## Build the monograph locally

After regenerating figures, compile `monograph/main.tex` locally. Compiled PDFs and LaTeX auxiliary files are ignored by Git.
