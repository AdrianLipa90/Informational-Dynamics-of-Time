# 03 — NOW Localization

GREMLIN candidate lineage: `G-CAND-0001`, refined as positive gauge-invariant atomic-event support.

Status: `STRUCTURAL_PASS / PHYSICAL_IDENTIFICATION_OPEN`

## Gauge-invariant event weight

For an admitted transition edge \(e:a\to b\), retain the open oriented phase
\[
\vartheta_e=\operatorname{Arg}L_e
\]
as a gauge-covariant transport quantity. Event existence is localized by the non-negative scalar
\[
\boxed{
q_e=
\sqrt{
 d_{FS}(a,b)^2+
 \kappa^2\Delta H_e^2+
 \kappa^2\sigma_e^2
 }\ge 0.
}
\]
Here
\[
d_{FS}(a,b)=\arccos|\langle\psi_a|\psi_b\rangle|
\]
is the Fubini--Study ray distance. The scalar \(q_e\) is invariant under local phase re-expression of the same ray data.

## Positive atomic event measure

Define
\[
\boxed{\mathcal K_T^+=\sum_e q_e\,\delta_{s_e},\qquad q_e\ge0.}
\]
The reduced atomic support is
\[
\boxed{\mathcal N=\operatorname{supp}_{\rm at}\mathcal K_T^+.}
\]

Relational density and viscosity rescale realization through the positive mobility
\[
M_{ab}=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}>0,
\]
so the realization-weighted event measure is
\[
\boxed{\mathcal R_T=\sum_e M_{ab}q_e\,\delta_{s_e}.}
\]
Because \(M_{ab}>0\),
\[
\boxed{
\operatorname{supp}_{\rm at}\mathcal R_T
=\operatorname{supp}_{\rm at}\mathcal K_T^+
=\mathcal N.
}
\]
Density and viscosity therefore control event weighting while the positive atomic support is inherited from \(q_e\).

## T023 — positive pushforward-support identity

For any map \(f\) defined on the atomic support,
\[
(f_*\mathcal K_T^+)(\{y\})
=\sum_{e:f(s_e)=y}q_e.
\]
Every fibre intersecting \(\mathcal N\) carries positive total mass, so
\[
\boxed{
\operatorname{supp}_{\rm at}(f_*\mathcal K_T^+)
=f(\mathcal N).
}
\]
Strictly increasing reparameterizations are an immediate special case.

## Temporal typing

The upstream activity-derived primitive carries
\[
\boxed{d\Theta_e=\mathfrak a_e\,d\lambda,}
\qquad
\boxed{\chi_e=\mathfrak j_e/\mathfrak a_e.}
\]
The NOW gate carries the event-support coordinate \(q_e\) and its positive atomic measure. The four typed observables entering the bifurcation layer are therefore

```text
dTheta_e = activity_e d_lambda : accumulated intrinsic duration
chi_e = current_e/activity_e    : local temporal orientation
q_e                              : gauge-invariant event signature
M_e q_e                          : positive realization weight
```

This gives the dependency handoff
\[
\boxed{
\text{TEMPORAL MEASURE + ORIENTATION}
\to
\text{REALIZED EVENT SUPPORT (NOW)}
\to
\text{BIFURCATION}.
}
\]
