# 07A — Multi-Event Retrodiction Observability

Status: `PROVISIONAL_DOWNSTREAM_BRANCH / FIRST_ORDER_OBSERVABILITY_REFERENCE_CANDIDATE`

This layer extends the single-missing-receipt inverse problem to several latent event kicks while preserving the parent gate: Memory remains the canonical frontier until its full repository reference-suite result is obtained.

## 1. Latent kick coordinates

For \(N\) event cells, write the two-component latent kick of event \(k\) as
\[
u_k=(\Delta v_{x,k},\Delta v_{y,k})\in\mathbb R^2,
\]
and collect
\[
\boxed{
z=(u_1,\ldots,u_N)\in\mathbb R^{2N}.
}
\]
The forward reference dynamics are the already-declared event kick followed by the smooth Kepler step,
\[
X_{k+1}=F_k(X_k,u_k)
=\Phi_K(\Delta\tau_k;\mu_M)\circ K_{u_k}(X_k).
\]

Retained memory checkpoints supply a measurement vector \(Y(z)\). In the current phase-plane reference each retained post-event checkpoint contributes
\[
(r_x,r_y,v_x,v_y)\in\mathbb R^4.
\]

## 2. T028 — first-order local observability matrix

At a nominal latent lineage \(z_0\), define the sensitivity matrix
\[
\boxed{
J_R(z_0)=\left.\frac{\partial Y}{\partial z}\right|_{z_0}.
}
\]
For the numerical reference, \(J_R\) is evaluated by centered finite differences of the exact repository forward cell.

The first-order local identifiability gate is
\[
\boxed{
\operatorname{rank}J_R=2N.
}
\]
Full column rank means that no nonzero infinitesimal latent-kick perturbation lies in the linearized measurement nullspace. This is a local regularity criterion; global uniqueness remains a separate problem.

The singular values of \(J_R\) are retained for conditioning audit. A full-rank system with a very small minimum singular value is distinguished from a well-conditioned reconstruction.

## 3. T029 — final-checkpoint dimensional bound

If only one final memory phase-state checkpoint is retained, then
\[
Y_f\in\mathbb R^4,
\qquad
J_R\in\mathbb R^{4\times 2N}.
\]
Therefore
\[
\boxed{
\operatorname{rank}J_R\le4.
}
\]
For \(N>2\),
\[
2N>4,
\]
so full column rank is impossible:
\[
\boxed{
N>2
\quad\Longrightarrow\quad
\text{several unknown two-component kicks cannot be locally identified from one final 4D checkpoint alone}.
}
\]
This obstruction is dimensional and precedes any optimizer or statistical estimator.

## 4. T030 — checkpoint augmentation

Additional retained checkpoints enlarge the measurement space. For checkpoint set \(\mathcal C\),
\[
Y_{\mathcal C}\in\mathbb R^{4|\mathcal C|},
\qquad
J_R\in\mathbb R^{4|\mathcal C|\times2N}.
\]
A necessary dimensional condition becomes
\[
4|\mathcal C|\ge2N.
\]
It is not sufficient by itself; the actual Jacobian must still have full column rank.

The current reference case with three unknown kicks has
\[
J_R^{\rm final}\in\mathbb R^{4\times6}
\]
and is necessarily underdetermined, whereas retaining all three post-event checkpoints gives
\[
J_R^{\rm all}\in\mathbb R^{12\times6}
\]
and the targeted reference calculation has rank six.

## 5. Fail-closed statuses

The implementation reports three distinct outcomes:

- `UNDERDETERMINED_DIMENSION` when the observation dimension is smaller than the latent dimension;
- `RANK_DEFICIENT` when sufficient measurement dimension exists but the numerical sensitivity matrix loses column rank;
- `LOCALLY_IDENTIFIABLE_REFERENCE` only when full column rank is obtained.

Invalid checkpoint duplication, checkpoint index zero, nonpositive step sizes and invalid numerical tolerances fail closed.

## 6. Role in the dependency graph

This is a Retrodiction design/audit layer, not a promotion of the canonical frontier. Its main methodological consequence is that future multi-event estimators must pass an observability/rank gate before optimization. This prevents an underdetermined inverse problem from being presented as a unique reconstruction.

Targeted controls are recorded in `validation/RETRODICTION_OBSERVABILITY_V0_1.json`.
