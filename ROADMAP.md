# Roadmap

The canonical dependency graph is maintained in `formalism/DEPENDENCY_GRAPH.md`.

\[
\boxed{\mathrm{TIR}\to\mathrm{Temporal\ Primitive}\to\mathrm{Temporal\ Wave}\to\mathrm{NOW}\to\mathrm{Bifurcation}\to\mathrm{Temporal\ Transport}\to\mathrm{Memory}\to\mathrm{ORCHORBITAL\ Attractors}\to\mathrm{Retrodiction}\to\mathrm{Retrocausal\ Tests}\to\mathrm{Einstein\ Closure}}
\]

## Phase A — Temporal core and transport

Status: `STRUCTURAL_REFERENCE_GATES_PASS`.

1. `PASS`: Shannon relational information primitives;
2. `PASS`: geometric phase-link primitives;
3. `PASS`: directed transition affinity and relational kinetic decomposition;
4. `PASS`: positive gauge-invariant NOW localization and pushforward-support identity;
5. `PASS_FORMAL_REFERENCE_CLASS`: reversible/contractive bifurcation operator contract;
6. `PASS_STRUCTURAL_REFERENCE_GATE`: ordered temporal transport, norm bound, conditioning separation and exact cut factorization.

## Phase B — Memory

Current promotion-branch status: `MEMORY_REFERENCE_GATE_ADMISSION_PASS / HOSTED_FULL_SUITE_PASS`.

1. `TARGETED_PASS`: Kepler--Newton memory propagation in \(\tau_{\rm int}\), signed areal law, conic elements and orbit classification;
2. `TARGETED_PASS`: event imprint projects to \(\delta m_n\) and the normalized event action yields \(\Delta v_{M,n}=q_n\delta m_n\);
3. `CONDITIONAL_IDENTIFIABILITY_PASS`: \(\mu_M\) recoverable from \((h_M,p_M)\), \((a_M,T_M)\), or memory-circulation rate plus conic geometry;
4. `CP1_REFERENCE_PASS`: Kähler-derived local memory frame with \(|\delta m|=d_{FS}\) and geodesic frame transport;
5. `TARGETED_PASS`: append-only memory receipt ledger and reversible lineage cell;
6. `TARGETED_PASS`: ledger-assisted `RECALL` reconstructs the recorded reference lineage;
7. `INTEGRATION_PASS`: CP1 geometry -> \(\delta m\) -> \(q\delta m\) -> Kepler lineage -> receipt -> recall passes the dedicated end-to-end controls;
8. `PASS_HOSTED_FULL_SUITE`: GitHub Actions run `33193861826`, job `98925901636`, executed `python -m pytest -q tests/reference` and returned `431 passed in 7.08s` on Python 3.12.14 / Ubuntu 24.04;
9. `ADMISSION_RECEIPT_ISSUED`: `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`;
10. `PARALLEL_OPEN_DERIVATION`: extend the geometry-derived frame beyond the CP1 reference subclass;
11. `PARALLEL_OPEN_DERIVATION`: predict \(\mu_M\) directly from earlier relational primitives.

Canonical `main` adopts this admission state when the promotion PR is merged.

## Phase B2 — ORCHORBITAL attractor organization

Current promotion-branch status: `ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / HOSTED_FULL_SUITE_PASS`.

1. `TARGETED_PASS`: define attractor-relative Kepler energy \(E_i\) and positive binding margin \(b_i=[-E_i]_+\);
2. `TARGETED_PASS`: normalize positive binding into replay-stable attractor weights \(w_i\) and select the maximum-binding basin;
3. `TARGETED_PASS`: expose `LEAK_MODE` when the total binding margin vanishes and fail closed before orbital propagation;
4. `TARGETED_PASS`: derive Shannon basin entropy \(H_A\) and normalized attractor coherence \(C_A\) from the weight distribution;
5. `TARGETED_PASS`: propagate each admitted smooth segment by the existing Kepler law translated to the active attractor centre;
6. `TARGETED_PASS`: accumulate branch-safe winding increments and re-evaluate the complete attractor field at every segment boundary;
7. `TARGETED_PASS`: record an attractor-switch candidate when the post-segment maximizing basin differs from the completed segment centre;
8. `TARGETED_PASS`: promote the changed basin on the following segment in multi-segment propagation;
9. `TARGETED_PASS`: accumulate per-attractor residence segment count, dwell time in \(\tau_{\rm int}\), winding and directed transition counts;
10. `TARGETED_PASS`: expose an explicitly normalized phase-space closure defect observable;
11. `REFERENCE_RESULT`: base ORCHORBITAL receipt `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`;
12. `HOSTED_SUITE_PASS`: ORCHORBITAL reference tests are included in successful repository-wide hosted suites;
13. `RESIDENCE_LEDGER_PASS`: append-only attractor-residence/switch receipts, strict schema, long-trajectory dwell distributions and transition lineage; receipts `validation/ORCHORBITAL_RESIDENCE_LEDGER_V0_1.json` and `validation/ORCHORBITAL_RESIDENCE_SCHEMA_HARDENING_V0_1.json`;
14. `PNCS_HIERARCHY_PASS`: pinned PNCS v0.29 sphere/entity hierarchy maps to nested IDT temporal-memory attractor families; receipt `validation/ORCHORBITAL_PNCS_HIERARCHY_BINDING_V0_1.json`;
15. `TYPED_OBSERVABLES_PASS`: pinned PNCS truth scalar, semantic mass and reduction readiness remain separately typed and residence-weightable where declared; receipt `validation/ORCHORBITAL_TYPED_OBSERVABLES_V0_1.json`;
16. `ADMISSION_RECEIPT_ISSUED`: `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`;
17. `PASS_HOSTED_FULL_SUITE`: run `33196818703`, job `98935954122`, returned `475 passed in 11.91s` for the typed-observable completion tree.

Canonical `main` adopts this admission state when the promotion PR is merged.

## Phase C — Retrodiction and retrocausal tests

Current promotion-branch status: `ACTIVE_NEXT_GATE / GATED_PENDING_ORCHORBITAL_PROMOTION_TO_MAIN`.

The tested Retrodiction implementation remains provisional downstream while its own admission work continues:

1. `PROVISIONAL_TARGETED_PASS`: reverse the known smooth Kepler segment and infer the missing kick \(\Delta v_{M,n}\);
2. `PROVISIONAL_CONDITIONAL_IDENTIFIABILITY`: infer \(q_n\) when nonzero \(\delta m_n\) is independently known;
3. `PROVISIONAL_CONDITIONAL_IDENTIFIABILITY`: infer \(\delta m_n\) when positive \(q_n\) is independently known;
4. `PROVED_REFERENCE_AMBIGUITY`: when both factors are withheld, only \(q_n\delta m_n\) is identifiable because positive reciprocal rescaling leaves the kick invariant;
5. `PROVISIONAL_OBSERVABILITY_GATE`: for \(N\) latent 2D kicks, build \(J_R=\partial Y/\partial z\) and require \(\operatorname{rank}J_R=2N\) before any estimator is admitted;
6. `PROVED_DIMENSIONAL_BOUND`: one final 4D memory checkpoint cannot locally identify more than two unknown 2D kicks, because \(\operatorname{rank}J_R\le4\);
7. `PROVISIONAL_CHECKPOINT_AUGMENTATION_PASS`: retained intermediate checkpoints enlarge the measurement space and produce full column rank in the targeted reference cases;
8. `PROVISIONAL_ESTIMATION_GATE_PASS`: gated damped Gauss--Newton reference estimation is implemented with strict residual-descent admission and fail-closed local-rank checks;
9. `PROVISIONAL_INFORMATION_FIREWALL_PASS`: estimator input excludes sealed truth and the estimate is content-committed before truth scoring;
10. `PROVISIONAL_UNCERTAINTY_GEOMETRY_PASS`: declared positive-definite checkpoint covariance yields whitened sensitivity, weighted rank/conditioning, local Fisher information and latent covariance;
11. `PROVISIONAL_PARTIAL_CHECKPOINT_SELECTION_PASS`: checkpoint cardinality is separated from rank and conditioning admission;
12. `PROVISIONAL_WEIGHTED_NULL_PASS`: covariance-weighted latent-kick estimation and the complete non-identity checkpoint-permutation reference ensemble pass the targeted layer;
13. `ACTIVE_NEXT`: condition Retrodiction on verified attractor-residence/switch histories and test whether basin labels improve identifiability under the declared lineage firewall;
14. `NEXT`: preregister experiment-specific null calibration before any `STATISTICAL_EFFECT` admission;
15. `LATER`: carry the admitted estimator into retrocausal-test protocols with statistical-effect and classical-channel audits.

Required later result stack:

`RAW_OBSERVATION -> STATISTICAL_EFFECT -> CLASSICAL_CHANNEL_AUDIT -> PHYSICAL_CLAIM_STATUS`.

`ANOMALY_DETECTED` and `RETROCAUSAL_CANDIDATE` remain distinct statuses.

## Phase D — spatial branch and Einstein closure

Spatial structure is introduced after the temporal branch has independently admitted state, transport, memory/ORCHORBITAL organization, retrodiction and clock-calibration structures. Einstein closure remains the final dependency gate.
