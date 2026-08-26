# 06B — Memory Central-Parameter Identifiability

Status: `MEMORY_FRONTIER_CANDIDATE / CONDITIONAL_IDENTIFIABILITY_DERIVATION`

The smooth memory reference class is
\[
\ddot m=-\mu_M\frac{m}{|m|^3},
\qquad \mu_M>0.
\]
This layer asks how \(\mu_M\) can be reconstructed from observables already carried by the Kepler memory branch.

## 1. T019G — identification from conic geometry and angular momentum

For a Kepler conic,
\[
p_M=\frac{h_M^2}{\mu_M}.
\]
Therefore
\[
\boxed{\mu_M=\frac{h_M^2}{p_M}}.
\]
For a bound ellipse with periapsis \(r_p\) and apoapsis \(r_a\),
\[
a_M=\frac{r_p+r_a}{2},
\qquad
e_M=\frac{r_a-r_p}{r_a+r_p},
\]
\[
\boxed{p_M=a_M(1-e_M^2)=\frac{2r_pr_a}{r_p+r_a}}.
\]
Thus the central parameter is identifiable from orbital geometry and signed angular momentum within the declared Kepler reference class.

## 2. T019H — identification from the third law

On a bound branch,
\[
T_M^2=\frac{4\pi^2}{\mu_M}a_M^3,
\]
so
\[
\boxed{
\mu_M=\frac{4\pi^2a_M^3}{T_M^2}.
}
\]
This provides an independent estimator from semi-major axis and internal-time orbital period.

## 3. T019I — identification from memory circulation

The admitted smooth memory circulation rate is
\[
\frac{d\Gamma_M}{d\tau_{\rm int}}=\lambda_Mh_M
\]
for constant \(\lambda_M\). Therefore
\[
h_M=\frac{1}{\lambda_M}\frac{d\Gamma_M}{d\tau_{\rm int}},
\]
and substitution into the conic relation gives
\[
\boxed{
\mu_M
=\frac{1}{p_M}
\left(
\frac{1}{\lambda_M}
\frac{d\Gamma_M}{d\tau_{\rm int}}
\right)^2.
}
\]
Orientation reversal changes the sign of \(h_M\) and of the corresponding circulation rate while leaving the identified \(\mu_M\) invariant.

## 4. Role in the dependency graph

These identities convert \(\mu_M\) from an unconstrained numerical input into an identifiable parameter once the required memory-orbit observables are available. A deeper origin law that predicts \(\mu_M\) directly from earlier relational primitives remains the next derivation layer.

Reference controls are recorded in `validation/MEMORY_MU_IDENTIFIABILITY_V0_1.json`.
