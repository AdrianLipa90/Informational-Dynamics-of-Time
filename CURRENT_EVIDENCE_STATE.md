# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE`.

## Temporal transport

Recorded structural evidence:

- prior full reference suite: `83 passed in 0.12s`;
- temporal-transport closure delta: `3/3 PASS` for spectral norm bound, algebraic invertibility/conditioning separation and exact cut factorization;
- receipt: `validation/TEMPORAL_TRANSPORT_CLOSURE_V0_2.json`.

## Memory

Memory reference evidence includes Kepler--Newton propagation, event-imprint kicks, conditional central-parameter identifiability, CP1 Kähler memory frames, append-only receipts, ledger-assisted recall and the integrated CP1 -> event kick -> Kepler -> persisted receipt -> recall path.

Hosted admission evidence:

- workflow: `Reference suite`;
- run: `33193861826` / run number `535`;
- job: `98925901636`;
- command: `python -m pytest -q tests/reference`;
- result: `431 passed in 7.08s`;
- receipt: `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

## ORCHORBITAL attractor organization

Base receipt: `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`.

The admitted promotion-branch component stack now contains:

- active-attractor binding, Shannon basin entropy/coherence, translated Kepler segments, winding, switch candidates, transition counts and phase-space closure diagnostics;
- append-only content-addressed residence receipts with exact binary64 state hashes and receipt hash chaining;
- strict residence schema controls and append-integrity controls;
- a real 101-segment dynamic residence profile with verified `A -> B` transition and global dwell-time accounting;
- generic hierarchy aggregation with Shannon chain-rule audit and transition coarse-graining;
- pinned PNCS v0.29 sphere/entity hierarchy binding with typed projection, canonical, hierarchy-lineage and mass-binding IDs;
- pinned PNCS v0.27 truth scalar, semantic mass and reduction-readiness carriers;
- residence-weighted semantic mass using verified temporal dwell lineage.

Component receipts:

- `validation/ORCHORBITAL_RESIDENCE_LEDGER_V0_1.json`;
- `validation/ORCHORBITAL_RESIDENCE_SCHEMA_HARDENING_V0_1.json`;
- `validation/ORCHORBITAL_PNCS_HIERARCHY_BINDING_V0_1.json`;
- `validation/ORCHORBITAL_TYPED_OBSERVABLES_V0_1.json`.

Hosted typed-observable completion evidence:

- workflow: `Reference suite`;
- run: `33196818703` / run number `557`;
- job: `98935954122`;
- command: `python -m pytest -q tests/reference`;
- result: `475 passed in 11.91s`;
- Python: `3.12.14`;
- runner: Ubuntu `24.04`;
- tested PR merge commit: `00057b9a7acb9874bc8cae3a47bd9bcf6877fe7f`;
- tested tree: `42b93983941098c02b350d9fb7bf18536ef4aeee`.

Combined admission receipt: `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

## Retrodiction active next gate

Existing Retrodiction evidence remains provisional and includes withheld-lineage inversion, local observability/rank admission, checkpoint selection, damped Gauss--Newton estimation, covariance/Fisher uncertainty geometry and covariance-preserving permutation nulls.

The active next experiment is to consume verified ORCHORBITAL residence/switch lineage and compare identifiability with and without retained basin labels under the existing information firewall.

## Canonical integration state

The promotion branch carries Memory and ORCHORBITAL admission receipts. Canonical `main` remains unchanged until explicit merge authorization.
