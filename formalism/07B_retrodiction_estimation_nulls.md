# 07B — Retrodiction Estimation and Null Comparison

Status: `PROVISIONAL_DOWNSTREAM_REFERENCE_CONTRACT`

Dependency position:

\[
\mathrm{Memory}\rightarrow\mathrm{Retrodiction}\rightarrow\mathrm{Retrocausal\ Tests}.
\]

The canonical admitted frontier remains Memory until the parent full-suite admission result is obtained. This file specifies the estimator layer downstream of the already staged Retrodiction observability gate.

## 1. Estimation is gated by observability

Let the latent direct event-kick vector be
\[
z=(\Delta v_{x,1},\Delta v_{y,1},\ldots,\Delta v_{x,N},\Delta v_{y,N})\in\mathbb R^{2N},
\]
and let the retained checkpoint observation map be
\[
Y(z)\in\mathbb R^{4|\mathcal C|}.
\]
The sensitivity matrix is
\[
J_R(z)=\frac{\partial Y}{\partial z}.
\]
Optimization is admitted only when the staged observability gate satisfies
\[
\boxed{\operatorname{rank}J_R(z_0)=2N.}
\]
Dimensionally underdetermined or rank-deficient cases fail closed before estimation.

## 2. Reference estimator

The provisional reference objective is the unweighted checkpoint residual
\[
\boxed{
\widehat z
=\arg\min_z
\frac12\|Y_{\rm obs}-Y(z)\|_2^2.
}
\]
At iteration \(k\), with
\[
r_k=Y_{\rm obs}-Y(z_k),
\qquad J_k=J_R(z_k),
\]
the damped Gauss--Newton proposal satisfies
\[
\boxed{
(J_k^T J_k+\lambda I)\,\delta z_k
=J_k^T r_k,
\qquad \lambda\ge0.
}
\]
The implementation accepts only a step length \(\alpha=2^{-j}\) for which
\[
\|Y_{\rm obs}-Y(z_k+\alpha\delta z_k)\|_2
<\|r_k\|_2.
\]
If no declared line-search step decreases the residual, the reference estimator returns `STALLED_NO_DESCENT` rather than fabricating a solution. If the local sensitivity loses full column rank during iteration, estimation fails closed.

## 3. Information firewall and estimate commitment

Hidden truth is absent from the estimator API. The estimator may consume only the preregistered retained checkpoints, \(\Delta\tau\), \(\mu_M\), the public forward model and predeclared numerical tolerances.

Before sealed truth is released to a scorer, the estimate is frozen by a content commitment
\[
\boxed{
C_{\rm est}=\operatorname{SHA256}(\widehat z\,\|\,\widehat Y\,\|\,r\,\|\,\mathrm{metadata}).
}
\]
The scorer verifies the commitment before evaluating reconstruction error. A commitment mismatch fails closed.

## 4. Reference nulls

### Zero-kick null

The first dynamical null fixes
\[
z_0=0
\]
and records
\[
r_0=\|Y_{\rm obs}-Y(0)\|_2.
\]

### Checkpoint-shuffle null

For at least two retained checkpoints, the observation is partitioned into four-component phase-state blocks and their order is permuted by a preregistered permutation \(\pi\). The same estimator capacity and the same observability gate are then applied to
\[
Y_{\rm obs}^{(\pi)}.
\]
Its fitted residual is denoted
\[
r_{\rm shuf}.
\]
The reference implementation uses reversal of the checkpoint-block order as the deterministic first null permutation.

### Product-factor ambiguity control

The single-event factorization control remains
\[
(q,\delta m)\mapsto(cq,\delta m/c),\qquad c>0,
\]
which preserves \(q\delta m\). It is therefore a structural non-identifiability control rather than an optimizer baseline.

## 5. Residual-reduction diagnostics

The reference diagnostics are
\[
\boxed{
R_0=1-\frac{r_{\rm est}}{r_0},
\qquad
R_{\rm shuf}=1-\frac{r_{\rm est}}{r_{\rm shuf}}.
}
\]
These quantities are computational reference diagnostics. They are not p-values and do not establish a physical effect.

## 6. Evidence boundary

The estimator contract is downstream staging. Its reference implementation is `src/idt/retrodiction_estimation.py`; targeted tests are `tests/reference/test_retrodiction_estimation.py`. The associated receipt is `validation/RETRODICTION_ESTIMATION_NULLS_V0_1.json`.

Later experimental inference must add a declared noise model, uncertainty propagation, independent baselines, leakage audits and the existing result stack

`RAW_OBSERVATION -> STATISTICAL_EFFECT -> CLASSICAL_CHANNEL_AUDIT -> PHYSICAL_CLAIM_STATUS`.
