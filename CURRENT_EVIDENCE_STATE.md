# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_INTEGRATION_REFERENCE_PASS_CANDIDATE / ORCHORBITAL_TARGETED_REFERENCE_PASS / RETRODICTION_TARGETED_REFERENCE_PASS / FULL_SUITE_NOT_OBTAINED`

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

The integrated Memory path verifies

`CP1 geometry -> event kick -> Kepler propagation -> persisted receipt -> recall`,

including a tampered-receipt negative control and upstream global-phase invariance. The isolated integrated round-trip error in the recorded reference case is below `3.6e-16`.

## ORCHORBITAL attractor extension

Receipt: `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`.

Targeted exact-dependency reference result:

- `9 passed in 0.05s`;
- positive binding margins normalize to attractor weights;
- deterministic maximum-binding active-attractor selection: PASS;
- symmetric two-attractor state gives `H_A = 1 bit` and normalized attractor coherence `C_A = 0`: PASS;
- zero total binding produces explicit `LEAK_MODE`: PASS;
- active-centre Kepler propagation is translation-covariant: PASS;
- quarter-turn winding increment equals `1/4`: PASS;
- ORCHORBITAL smooth step advances `tau_internal` and records winding: PASS;
- a constructed boundary-crossing case records `A -> B` as an attractor-switch candidate: PASS;
- `LEAK_MODE` fails closed before orbital propagation: PASS;
- phase-space closure defect is zero for identical states: PASS.

Evidence class: `ORCHORBITAL_MEMORY_REFERENCE_DIAGNOSTIC`.

## Retrodiction downstream staging

Recorded provisional evidence includes:

- single missing receipt: `8/8 targeted PASS`, including 1000 randomized single-cell retrodictions with maximum errors at floating-point scale;
- multi-event observability: `7/7 targeted PASS`; the three-kick all-checkpoint reference Jacobian is `12 x 6` with rank 6;
- exact gated estimation: three-kick reference converges in two iterations at round-off residual; 50/50 seeded exact cases converge;
- uncertainty geometry: weighted condition number about `4.076`; seeded 500-case nonlinear audit gives empirical coordinate dispersions within about `4.4%` of local Fisher predictions;
- partial-checkpoint selection: two checkpoints can be information-sufficient but poorly conditioned; all three give condition about `4.067--4.076` in the recorded reference range;
- covariance-weighted permutation nulls: targeted file `5 passed`, final checkpoint-selection + weighted-null rerun `10 passed in 0.25s`; the retained chronology beats all five non-identity checkpoint permutations in E003 reference run 0002.

Retrodiction remains `PROVISIONAL_DOWNSTREAM` in the dependency graph.

## Hosted full-suite status

Observed GitHub Actions jobs for the integrated Memory/Retrodiction history terminate with conclusion `failure` but zero executed steps and unavailable logs. The recorded result class is therefore

`CI_RESULT_NOT_OBTAINED / RUNNER_OR_PRESTEP_INFRASTRUCTURE_FAILURE`.

No repository-test PASS or code/test FAIL is inferred from those hosted runs.

The canonical admitted frontier remains at Memory pending a real full repository reference-suite result. ORCHORBITAL has targeted reference PASS as a Memory extension; Retrodiction remains downstream staging behind the Memory -> ORCHORBITAL admission path.
