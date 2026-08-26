# 07E — Covariance-Weighted Retrodiction and Permutation Nulls

Status: `PROVISIONAL_DOWNSTREAM_REFERENCE_CONTRACT`

Dependency position:

\[
\mathrm{Memory}\rightarrow\mathrm{Retrodiction}\rightarrow\mathrm{Retrocausal\ Tests}.
\]

The canonical admitted frontier remains Memory until its parent admission gate is resolved. This file extends the staged Retrodiction inverse problem without promoting the node.

## 1. Covariance-weighted objective

For retained checkpoint observation vector \(Y_{\rm obs}\) with declared symmetric positive-definite covariance \(\Sigma_Y\), define

\[
r(z)=Y_{\rm obs}-Y(z),
\qquad
\boxed{Q(z)=r(z)^T\Sigma_Y^{-1}r(z)}.
\]

With Cholesky factorization

\[
\Sigma_Y=LL^T,
\]

use whitened residual and sensitivity

\[
r_W=L^{-1}r,
\qquad
J_W=L^{-1}J_R.
\]

The weighted observability gate remains

\[
\boxed{\operatorname{rank}J_W=\dim z}.
\]

## 2. Weighted damped Gauss--Newton step

For the currently admitted iterate \(z_k\), the reference proposal solves

\[
\boxed{
(J_W^TJ_W+\lambda I)\delta z_k=J_W^Tr_W,
\qquad \lambda\ge0.
}
\]

Only a line-search step \(z_k+\alpha\delta z_k\), \(\alpha=2^{-j}\), that strictly decreases \(Q\) is admitted. Loss of weighted full column rank, singular normal equations, invalid covariance, or failure to obtain descent is reported explicitly.

## 3. Checkpoint-order null ensemble

For \(K=|\mathcal C|\) retained four-component checkpoint blocks, let \(P_\pi\) be the block permutation matrix corresponding to \(\pi\in S_K\). A null member is constructed by jointly permuting observation and covariance:

\[
\boxed{
Y_\pi=P_\pi Y_{\rm obs},
\qquad
\Sigma_\pi=P_\pi\Sigma_YP_\pi^T.
}
\]

The same forward model, latent dimension, observability gate, damping rule, line search and estimator capacity are applied to every null member. This preserves the declared uncertainty assignment under the checkpoint relabeling.

The default finite reference ensemble contains all non-identity permutations when the total count is below the declared safety limit.

## 4. Reference diagnostics

Let \(Q_{\rm obs}\) be the weighted residual quadratic for the retained chronology and \(Q_\pi\) the fitted value for a null permutation. Record

\[
Q_{\rm null,min}=\min_{\pi\ne id}Q_\pi,
\]

\[
\boxed{\Delta Q_{\rm null}=Q_{\rm null,min}-Q_{\rm obs}},
\]

and the finite-ensemble rank diagnostic

\[
\boxed{
f_{\rm null}=\frac{\#\{\pi:Q_\pi\le Q_{\rm obs}\}}{N_{\rm null}}}.
\]

`f_null` is a finite computational reference-ensemble diagnostic. It is not registered as a p-value. Statistical-effect admission requires a later experiment-specific null calibration and the full evidence stack.

## 5. Evidence boundary

Reference implementation: `src/idt/retrodiction_weighted_nulls.py`.

Reference tests: `tests/reference/test_retrodiction_weighted_nulls.py`.

Validation receipt: `validation/RETRODICTION_WEIGHTED_NULLS_V0_1.json`.

Append-only E003 reference run: `experiments/E003_retrodiction/runs/E003_REFERENCE_0002.json`.

The implementation is a provisional downstream computational reference class. It does not advance the canonical dependency frontier and does not change physical claim status.
