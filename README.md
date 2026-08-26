# Informational Dynamics of Time

This repository develops temporal dynamics before spacetime closure. The project is maintained as three linked but distinct spines:

- `FORMALISM` — equations, typed contracts and dependency graph;
- `EVIDENCE` — tests, receipts, manifests and audits;
- `MONOGRAPH` — LaTeX view assembled from recorded formalism and evidence.

Canonical dependency graph:

\[
\boxed{\mathrm{TIR}\to\mathrm{Temporal\ Primitive}\to\mathrm{Temporal\ Wave}\to\mathrm{NOW}\to\mathrm{Bifurcation}\to\mathrm{Temporal\ Transport}\to\mathrm{Memory}\to\mathrm{Retrodiction}\to\mathrm{Retrocausal\ Tests}\to\mathrm{Einstein\ Closure}}
\]

The admitted frontier currently remains at `Memory`. Tested Retrodiction implementation may exist on `main` while remaining explicitly `PROVISIONAL_DOWNSTREAM`; merge status and theory-admission status are separate.

The current reference stack includes Shannon/phase transition primitives, positive temporal activity and NOW support, bifurcation and ordered temporal transport, internal elapsed activity, Kepler--Newton memory dynamics, CP1 Kähler memory geometry, append-only memory receipts and ledger-assisted recall.

The provisional Retrodiction layer contains:

- single-withheld-receipt inversion with explicit product-only ambiguity;
- multi-event observability and rank admission;
- minimal checkpoint selection with optional conditioning gate;
- damped Gauss--Newton estimation with information firewall and estimate commitment;
- declared checkpoint covariance, whitened sensitivity and local Fisher uncertainty geometry;
- covariance-weighted estimation and same-capacity checkpoint-permutation null ensembles.

Reference figures are generated from code. Raster outputs and compiled PDFs are local QA artifacts and are not committed; repository monograph source is LaTeX.

Reproduce figure sources with:

```text
PYTHONPATH=. python3 scripts/build_figures.py
```

Reference tests live under `tests/reference/`. GitHub Actions is configured to run the reference suite, but current hosted runs have repeatedly terminated before executing test steps; such runs are recorded as `CI_RESULT_NOT_OBTAINED`, not as repository-test failures.
