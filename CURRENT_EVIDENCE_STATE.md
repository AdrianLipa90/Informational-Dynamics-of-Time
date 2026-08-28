# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_HOSTED_FULL_SUITE_PASS_PROMOTION_READY / ORCHORBITAL_TARGETED_REFERENCE_PASS / RETRODICTION_TARGETED_REFERENCE_PASS`

## Temporal transport

Recorded structural evidence:

- prior full reference suite: `83 passed in 0.12s`;
- temporal-transport closure delta: `3/3 PASS` for spectral norm bound, algebraic invertibility/conditioning separation and exact cut factorization;
- receipt: `validation/TEMPORAL_TRANSPORT_CLOSURE_V0_2.json`.

## Memory

Recorded targeted controls:

- Kepler--Newton memory: `11 passed in 0.46s`;
- event-imprint memory kick: `7 passed in 0.08s`;
- central-parameter identifiability: `6 targeted checks PASS`;
- CP1 Kähler memory frame: `7 targeted checks PASS`;
- persistence / ledger-assisted recall: `8 passed in 0.13s`;
- integrated Memory path: `6/6 targeted integration checks PASS`.

The integrated Memory path verifies `CP1 geometry -> event kick -> Kepler propagation -> persisted receipt -> recall`, including a tampered-receipt negative control and upstream global-phase invariance. The isolated integrated round-trip error in the recorded reference case is below `3.6e-16`.

The previously outstanding repository-wide admission condition has now been executed by GitHub Actions. Run `33193861826`, job `98925901636`, executed `python -m pytest -q tests/reference` on Python 3.12.14 / Ubuntu 24.04 and returned `431 passed in 7.08s`. The workflow conclusion is `success`.

The tested PR merge commit is `e0b1cdc491a1a501adce93b8d62ade063e167500`, tree `92302498f3c9131b163d5d0ccbbeab1db935d29f`. The append-only evidence binding is `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

Memory is therefore promotion-ready on the evidence branch. Canonical `main` remains unchanged until PR #21 is merged.

## ORCHORBITAL attractor extension

Receipt: `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`.

Targeted exact-dependency reference result:

- `11 passed in 0.07s`;
- positive binding margins normalize to attractor weights;
- deterministic maximum-binding active-attractor selection: PASS;
- symmetric two-attractor state gives `H_A = 1 bit` and normalized attractor coherence `C_A = 0`: PASS;
- zero total binding produces explicit `LEAK_MODE`: PASS;
- active-centre Kepler propagation is translation-covariant: PASS;
- quarter-turn winding increment equals `1/4`: PASS;
- ORCHORBITAL smooth step advances `tau_internal` and records winding: PASS;
- a constructed boundary-crossing case records `A -> B` as an attractor-switch candidate: PASS;
- multi-segment propagation uses `A` on the completed segment and `B` on the following segment: PASS;
- directed transition graph counts the reference `A -> B` transition exactly once: PASS;
- residence summary accumulates segment count, dwell time in `tau_internal` and winding: PASS;
- `LEAK_MODE` fails closed before orbital propagation: PASS;
- phase-space closure defect is zero for identical states: PASS.

These ORCHORBITAL tests are also contained in the successful 431-test repository suite. This closes the hosted-execution uncertainty for the existing implementation, but does not by itself satisfy the remaining ORCHORBITAL admission work on long-trajectory residence/switch provenance, hierarchical attractor families and typed observables.

Evidence class: `ORCHORBITAL_MEMORY_REFERENCE_DIAGNOSTIC`.

## Retrodiction downstream staging

Recorded provisional evidence includes:

- single missing receipt: `8/8 targeted PASS`, including 1000 randomized single-cell retrodictions with maximum errors at floating-point scale;
- multi-event observability: `7/7 targeted PASS`; the three-kick all-checkpoint reference Jacobian is `12 x 6` with rank 6;
- exact gated estimation: three-kick reference converges in two iterations at round-off residual; 50/50 seeded exact cases converge;
- uncertainty geometry: weighted condition number about `4.076`; seeded 500-case nonlinear audit gives empirical coordinate dispersions within about `4.4%` of local Fisher predictions;
- partial-checkpoint selection: two checkpoints can be information-sufficient but poorly conditioned; all three give condition about `4.067--4.076` in the recorded reference range;
- covariance-weighted permutation nulls: targeted file `5 passed`, final checkpoint-selection + weighted-null rerun `10 passed in 0.25s`; the retained chronology beats all five non-identity checkpoint permutations in E003 reference run 0002.

Retrodiction remains `PROVISIONAL_DOWNSTREAM` in the dependency graph and is gated by ORCHORBITAL admission.

## Hosted full-suite status

Current hosted result: `PASS`.

- workflow: `Reference suite`;
- run: `33193861826` / run number `535`;
- job: `98925901636`;
- test step executed: yes;
- command: `python -m pytest -q tests/reference`;
- result: `431 passed in 7.08s`;
- job/workflow conclusion: `success`.

Earlier zero-step infrastructure failures remain historical evidence and are not reclassified as code-test failures. The fresh executed run supersedes them for the current integrated Memory evidence gate.

The next admission dependency is now ORCHORBITAL Attractors. Retrodiction remains downstream staging behind `Memory -> ORCHORBITAL`.
