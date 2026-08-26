# 07C — Retrodiction Noise and Local Uncertainty Geometry

Status: `PROVISIONAL_DOWNSTREAM_REFERENCE_CONTRACT`

Dependency position:

\[
\mathrm{Retrodiction\ Observability}
\rightarrow
\mathrm{Retrodiction\ Estimation}
\rightarrow
\mathrm{Uncertainty\ Geometry}.
\]

The canonical admitted frontier remains Memory pending its full-suite admission result. This layer supplies an explicit checkpoint-noise covariance and local uncertainty propagation around a committed Retrodiction estimate.

## 1. Observation-noise model

Let the retained checkpoint vector obey the local observation model
\[
Y_{\rm obs}=Y(z_\star)+\varepsilon,
\qquad
\mathbb E[\varepsilon]=0,
\qquad
\operatorname{Cov}(\varepsilon)=\Sigma_Y.
\]
The reference contract requires \(\Sigma_Y\) to be finite, symmetric and positive definite. Write its Cholesky factorization as
\[
\boxed{\Sigma_Y=LL^T.}
\]

## 2. Whitened sensitivity and weighted rank

For sensitivity matrix
\[
J_R=\frac{\partial Y}{\partial z},
\]
define the whitened sensitivity
\[
\boxed{J_W=L^{-1}J_R.}
\]
The weighted local-identifiability check is
\[
\boxed{\operatorname{rank}J_W=\dim z.}
\]
The singular spectrum of \(J_W\) defines the weighted local condition number
\[
\boxed{
\kappa_W=\frac{s_{\max}(J_W)}{s_{\min}(J_W)}.
}
\]
A protocol may supply an explicit maximum admitted \(\kappa_W\); the implementation records `WEIGHTED_ILL_CONDITIONED` when that threshold is exceeded.

## 3. Fisher information and latent covariance

Within the local Gaussian reference approximation, the latent Fisher information is
\[
\boxed{
F_z
=J_R^T\Sigma_Y^{-1}J_R
=J_W^TJ_W.
}
\]
For a full-column-rank weighted sensitivity,
\[
\boxed{
C_z\approx F_z^{-1},
\qquad
\sigma_{z_i}=\sqrt{(C_z)_{ii}}.
}
\]
This supplies a local uncertainty scale for each inferred kick coordinate.

For isotropic checkpoint noise
\[
\Sigma_Y=\sigma_Y^2 I,
\]
one obtains
\[
C_z
=\sigma_Y^2(J_R^TJ_R)^{-1},
\]
so doubling \(\sigma_Y\) multiplies \(C_z\) by four and the latent standard errors by two.

## 4. Weighted residual diagnostic

For committed residual
\[
r=Y_{\rm obs}-Y(\widehat z),
\]
define
\[
\boxed{
Q_W=r^T\Sigma_Y^{-1}r.
}
\]
When the retained observation dimension \(m\) exceeds latent dimension \(p\), the reference diagnostic also records
\[
\boxed{
\bar Q_W=\frac{Q_W}{m-p}.
}
\]
Its registered evidence class is `NOISE_MODEL_REFERENCE_DIAGNOSTIC`. Statistical calibration belongs to the later experiment-specific inference gate.

## 5. Reference validation target

The executable implementation is `src/idt/retrodiction_uncertainty.py`, with targeted tests in `tests/reference/test_retrodiction_uncertainty.py` and receipt `validation/RETRODICTION_UNCERTAINTY_V0_1.json`.

The first reference case uses isotropic checkpoint standard deviation \(10^{-5}\). Its weighted condition number is approximately \(4.076\), with six finite latent standard errors of order \(10^{-5}\). A seeded nonlinear Monte Carlo reference audit compares empirical kick-coordinate dispersion against the local Fisher prediction.

Physical-claim evaluation remains downstream of the preregistered statistical-effect and classical-channel audit stack.
