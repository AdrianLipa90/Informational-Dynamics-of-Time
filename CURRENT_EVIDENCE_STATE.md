# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_INTEGRATION_REFERENCE_PASS_CANDIDATE / RETRODICTION_TARGETED_ISOLATED_PASS / FULL_SUITE_NOT_OBTAINED`

Recorded transport evidence:

- prior full reference suite: `83 passed in 0.12s`;
- temporal-transport closure delta: `3/3 PASS` for the spectral norm bound, algebraic invertibility/conditioning separation and exact cut factorization;
- closure receipt: `validation/TEMPORAL_TRANSPORT_CLOSURE_V0_2.json`.

Recorded Memory-node targeted controls:

- Kepler--Newton memory suite: `11 passed in 0.46s`;
- event-imprint memory-kick suite: `7 passed in 0.08s`;
- memory central-parameter identifiability: `6 targeted checks PASS`;
- CP1 Kähler memory frame: `7 targeted checks PASS`;
- persistence / ledger-assisted recall: `8 passed in 0.13s` in the isolated targeted reference harness;
- integrated Memory admission path: `6/6 targeted integration checks PASS` in the isolated exact-formula integration harness.

The integrated Memory controls verify the CP1 geometry -> event kick -> Kepler propagation -> persisted receipt -> recall path, including a tampered-receipt negative control and upstream global-phase invariance. The isolated integrated round-trip error observed in the reference case was below `3.6e-16`.

Provisional single-missing-receipt Retrodiction evidence is recorded in `validation/RETRODICTION_SINGLE_MISSING_RECEIPT_V0_1.json`:

- `8/8` targeted exact-formula controls PASS in the isolated harness;
- reversing the known smooth segment recovers the missing event kick: PASS;
- known nonzero \(\delta m_n\) recovers \(q_n\): PASS;
- known positive \(q_n\) recovers \(\delta m_n\): PASS;
- withholding both factors fails closed as product-only ambiguity: PASS;
- wrong imprint direction fails the collinearity residual: PASS;
- zero-weight consistency and checkpoint-tampering controls: PASS;
- 1000 randomized single-cell retrodictions produced maximum absolute errors of about `4.0e-15` for \(q\), `2.6e-15` for \(\delta m\), and `1.2e-16` checkpoint residual.

Provisional multi-event observability evidence is recorded in `validation/RETRODICTION_OBSERVABILITY_V0_1.json`:

- `7/7` targeted exact-formula controls PASS in the isolated harness;
- one unknown 2D kick gives rank 2 from one final 4D phase-state checkpoint in the reference case;
- two unknown 2D kicks give rank 4 from one final 4D checkpoint in the generic reference case;
- three unknown 2D kicks are dimensionally underdetermined from one final 4D checkpoint because the Jacobian is `4 x 6`;
- retaining all three post-event checkpoints gives a `12 x 6` Jacobian with rank 6 in the targeted reference case;
- randomized audit: 200/200 two-kick final-checkpoint cases were full rank and 200/200 three-kick all-checkpoint cases were full rank in the recorded parameter range.

Provisional gated-estimation evidence is recorded in `validation/RETRODICTION_ESTIMATION_NULLS_V0_1.json` and append-only run `experiments/E003_retrodiction/runs/E003_REFERENCE_0001.json`:

- the three-kick reference case passes the `12 x 6`, rank-6 observability gate;
- damped Gauss--Newton converges in 2 iterations;
- estimator residual norm: about `1.04e-14`;
- maximum kick-coordinate error after estimate commitment and truth release: about `1.39e-14`;
- zero-kick reference residual: about `9.20e-2`;
- reversed-checkpoint, capacity-matched reference fit residual: about `9.57e-2`;
- 50/50 seeded three-kick exact-reference cases were full rank and converged, with maximum kick-coordinate error about `1.65e-14`;
- estimate-commitment mismatch is a fail-closed control.

Provisional noise/uncertainty evidence is recorded in `validation/RETRODICTION_UNCERTAINTY_V0_1.json`:

- isotropic checkpoint reference standard deviation: `1e-5`;
- weighted `12 x 6` sensitivity rank: `6`;
- weighted condition number: about `4.076`;
- six local Fisher kick-coordinate standard errors lie between about `9.98e-6` and `1.42e-5`;
- doubling the checkpoint standard deviation multiplies latent covariance by four and latent standard errors by two: PASS;
- Fisher information times the inferred local covariance returns the six-dimensional identity within numerical tolerance: PASS;
- a seeded 500-case nonlinear reference audit at checkpoint standard deviation `1e-5` produced zero fit failures;
- empirical coordinate standard deviations were within about `4.4%` of the local Fisher predictions in that recorded reference regime.

Provisional partial-checkpoint evidence is recorded in `validation/RETRODICTION_CHECKPOINT_SELECTION_V0_1.json`:

- for three latent 2D kicks, the necessary dimensional lower bound is two retained 4D checkpoints;
- subset `[1,2]` has rank 4 and is rejected for six latent coordinates;
- subset `[1,3]` has rank 6 with condition number about `66.30`;
- subset `[2,3]` has rank 6 with condition number about `72.16`;
- the minimal-cardinality reference selector therefore chooses `[1,3]`;
- retaining `[1,2,3]` gives condition number about `4.076`;
- with an explicit maximum admitted condition number `10`, the selector retains all three checkpoints;
- seeded 200-case three-event audit: every case had a full-rank two-checkpoint subset; the best two-checkpoint condition median was about `59.42`, while all-three-checkpoint condition median was about `4.067`.

Provisional covariance-weighted permutation-null evidence is recorded in `validation/RETRODICTION_WEIGHTED_NULLS_V0_1.json` and append-only run `experiments/E003_retrodiction/runs/E003_REFERENCE_0002.json`:

- exact weighted-null targeted test file: `5 passed in 0.19s`;
- final pre-merge combined checkpoint-selection plus weighted-null targeted rerun: `10 passed in 0.25s`;
- weighted three-kick estimator passes rank 6 and reconstructs the exact reference lineage in two iterations;
- weighted condition number: about `4.070`;
- retained chronology weighted residual quadratic: about `2.49e-24`;
- all five non-identity permutations of three complete checkpoint blocks are evaluated with the same latent dimension and jointly permuted covariance;
- permutation-null weighted residual quadratics range from about `1.80e5` to `8.19e5`, with median about `6.13e5`;
- no null member reaches a residual at or below the retained chronology in this finite reference ensemble;
- non-positive-definite covariance and a permutation count above the declared safety limit fail closed.

The registered evidence classes are `COMPUTATIONAL_REFERENCE_DIAGNOSTIC`, `NOISE_MODEL_REFERENCE_DIAGNOSTIC`, `PARTIAL_OBSERVATION_REFERENCE_DIAGNOSTIC` and `PERMUTATION_REFERENCE_DIAGNOSTIC`. Statistical-effect evaluation, experiment-specific uncertainty calibration, leakage/channel audit and physical-claim evaluation remain later gates.

Validation receipts include:

- `validation/TEMPORAL_TRANSPORT_CLOSURE_V0_2.json`;
- `validation/KEPLER_MEMORY_DYNAMICS_V0_1.json`;
- `validation/EVENT_MEMORY_KICK_V0_1.json`;
- `validation/MEMORY_MU_IDENTIFIABILITY_V0_1.json`;
- `validation/KAHLER_MEMORY_FRAME_CP1_V0_1.json`;
- `validation/MEMORY_PERSISTENCE_RECALL_V0_1.json`;
- `validation/MEMORY_ADMISSION_V0_1.json`;
- `validation/RETRODICTION_SINGLE_MISSING_RECEIPT_V0_1.json`;
- `validation/RETRODICTION_OBSERVABILITY_V0_1.json`;
- `validation/RETRODICTION_ESTIMATION_NULLS_V0_1.json`;
- `validation/RETRODICTION_UNCERTAINTY_V0_1.json`;
- `validation/RETRODICTION_CHECKPOINT_SELECTION_V0_1.json`;
- `validation/RETRODICTION_WEIGHTED_NULLS_V0_1.json`.

GitHub Actions infrastructure status: the integrated Memory admission attempts and the latest Retrodiction-branch workflow job end with conclusion `failure`, zero executed steps and unavailable job logs. The observable result class is `CI_RESULT_NOT_OBTAINED / RUNNER_OR_PRESTEP_INFRASTRUCTURE_FAILURE`; no repository-test outcome was produced by those runs.

Full repository suite status on the integrated Memory tree: `NOT_OBTAINED`.

The current evidence supports an integrated Memory reference-gate candidate and provisional downstream Retrodiction reference candidates through observability, estimation, null comparison, local uncertainty geometry, partial-checkpoint selection and covariance-preserving permutation-null comparison. Final Memory admission remains pending a real full repository reference-suite result; Retrodiction remains provisional until that dependency gate is explicitly promoted.
