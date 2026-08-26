# E003 — Retrodiction Withheld-Lineage Protocol v0.1

Status: `PREREGISTERED_PROVISIONAL_DOWNSTREAM`

Dependency gate: `Memory -> Retrodiction`.

This protocol is staged while Memory admission remains pending the full repository reference-suite result. It cannot promote a Retrodiction claim before the parent gate passes.

## Objective

Measure whether the declared Retrodiction operators reconstruct deliberately withheld lineage variables from the permitted memory checkpoints and model parameters, without access to sealed truth variables.

The experiment is a formal/reference-model validation. Physical claim status is outside this protocol.

## Forward reference generator

A run is generated from the declared event-driven Kepler memory cell

\[
X_{k+1}=\Phi_K(\Delta\tau_k;\mu_M)\circ K_{u_k}(X_k),
\qquad
u_k=q_k\delta m_k.
\]

The generator stores a sealed truth record containing the full event sequence and all intermediate states. The estimator receives only the explicitly declared observation package.

## Observation packages

### E003-A — single missing receipt factor

Retained:

- pre-event memory checkpoint \(X_n\);
- post-segment checkpoint \(X_{n+1}\);
- \(\mu_M\);
- \(\Delta\tau_n\);
- exactly one independently known factor: either \(q_n\) or \(\delta m_n\).

Withheld:

- the complementary receipt factor.

Primary reconstruction follows T024--T026.

### E003-B — product-only negative control

Retain the same two checkpoints, \(\mu_M\), and \(\Delta\tau_n\), but withhold both \(q_n\) and \(\delta m_n\).

Expected status: `PRODUCT_ONLY_AMBIGUITY`. Any estimator returning a unique factorization without an additional declared constraint fails this control.

### E003-C — multi-event observability

For \(N\) latent two-component kicks, retain a declared checkpoint subset \(\mathcal C\) and compute

\[
J_R=\frac{\partial Y_{\mathcal C}}{\partial z},
\qquad z\in\mathbb R^{2N}.
\]

No latent-lineage optimizer is admitted unless

\[
\operatorname{rank}J_R=2N.
\]

A final-only three-kick case is a mandatory underdetermined negative control.

## Information firewall

The estimator may read only:

- declared observed checkpoints;
- declared \(\Delta\tau_k\);
- declared \(\mu_M\);
- the public forward model;
- the single complementary receipt factor only in E003-A;
- numerical tolerances fixed in preregistration.

The estimator may not read:

- withheld \(q_k\) or \(\delta m_k\);
- hidden intermediate checkpoints;
- sealed truth kicks;
- the generator random seed;
- post-hoc tuning values derived from the hidden answer.

The scorer, not the estimator, may open the sealed truth record after the estimate has been committed.

## Baselines and null controls

`NULL_ZERO_KICK`: all withheld event kicks are set to zero.

`NULL_PRODUCT_FACTOR`: in E003-B, choose an arbitrary positive factorization of the recovered product. This control is expected to demonstrate non-uniqueness rather than score as a valid reconstruction.

`NULL_CHECKPOINT_SHUFFLE`: pair an observation package with a checkpoint from another run. The consistency residual must reject the mismatch.

## Metrics

For identifiable cases:

- kick error \(\|\widehat u-u\|_2\);
- scalar event-weight error when \(q\) is the target;
- complex imprint error when \(\delta m\) is the target;
- checkpoint reconstruction residual;
- sensitivity rank and singular spectrum;
- condition number for full-column-rank systems;
- improvement relative to `NULL_ZERO_KICK`.

For non-identifiable cases:

- correct ambiguity/underdetermined classification is the primary outcome.

## Predeclared exact-reference thresholds

For noiseless runs generated and inverted by the same declared reference equations:

- checkpoint consistency tolerance: \(10^{-10}\);
- factorization residual tolerance: \(10^{-10}\);
- relative rank tolerance: \(10^{-8}\);
- finite-difference sensitivity step: \(10^{-7}\).

Noisy-data thresholds require a separate preregistration.

## Result stack

Every run reports separately:

1. `RAW_OBSERVATION` — the estimator input package and committed estimate;
2. `STATISTICAL_EFFECT` — reconstruction metrics versus baselines when a repeated-run analysis is performed;
3. `CLASSICAL_CHANNEL_AUDIT` — information-firewall and leakage result;
4. `PHYSICAL_CLAIM_STATUS` — `NOT_EVALUATED` for this reference-model protocol.

Runs are append-only. A failed run is retained; corrections create a new run identifier.
