# Provisional Retrodiction Claim Registry

Status: `DOWNSTREAM_STAGING_ONLY`

These claims belong to the Retrodiction branch and do not advance the canonical dependency frontier while Memory admission is pending.

| ID | Statement | Depends on | Evidence class | Status |
|---|---|---|---|---|
| T028 | For latent two-component event kicks \(z\in\mathbb R^{2N}\), the first-order Retrodiction observability matrix is \(J_R=\partial Y/\partial z\); full column rank \(\operatorname{rank}J_R=2N\) is the reference local-identifiability gate | T024–T027 + smooth Kepler forward cell | differential sensitivity criterion + targeted finite-difference controls | `PROVISIONAL_RETRODICTION_OBSERVABILITY_GATE` |
| T029 | With only one final memory phase-state checkpoint \(Y_f\in\mathbb R^4\), \(\operatorname{rank}J_R\le4\), so more than two unknown two-component kicks are dimensionally non-identifiable from that checkpoint alone | T028 | matrix-dimension theorem | `PROVED_PROVISIONAL_DIMENSIONAL_BOUND` |
| T030 | Retaining additional post-event checkpoints enlarges the measurement space to \(\mathbb R^{4|\mathcal C|}\); \(4|\mathcal C|\ge2N\) is necessary and full column rank remains the actual local-identifiability test | T028–T029 | dimensional condition + targeted reference-rank controls | `PROVISIONAL_CHECKPOINT_AUGMENTATION_CRITERION` |

The reference implementation distinguishes `UNDERDETERMINED_DIMENSION`, `RANK_DEFICIENT`, and `LOCALLY_IDENTIFIABLE_REFERENCE`. Global uniqueness and noisy statistical estimation are later layers.
