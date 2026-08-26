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
is the Fubini–Study ray distance. Thus local phase choices cannot create or remove an event atom.

## Positive atomic event measure

Define
\[
\boxed{\mathcal K_T^+=\sum_e q_e\,\delta_{s_e},\qquad q_e\ge0.}
\]
Zero-weight atoms are omitted from the reduced measure. The canonical NOW candidate is
\[
\boxed{\mathcal N=\operatorname{supp}_{\rm at}\mathcal K_T^+.}
\]

Relational density and viscosity may rescale realization through the positive mobility
\[
M_{ab}=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}>0,
\]
so a realization-weighted event measure can be written as
\[
\boxed{\mathcal R_T=\sum_e M_{ab}q_e\,\delta_{s_e}.}
\]
Because \(M_{ab}>0\),
\[
\operatorname{supp}_{\rm at}\mathcal R_T
=\operatorname{supp}_{\rm at}\mathcal K_T^+
=\mathcal N.
\]
Density and viscosity can therefore change event pace/weight without changing which admitted transition signatures vanish.

## T023 — positive pushforward-support identity

For any map \(f\) defined on the atomic support,
\[
(f_*\mathcal K_T^+)(\{y\})
=\sum_{e:f(s_e)=y}q_e.
\]
Every non-empty fibre that intersects \(\mathcal N\) has strictly positive total mass, so
\[
\boxed{
\operatorname{supp}_{\rm at}(f_*\mathcal K_T^+)
=f(\mathcal N).
}
\]
No injectivity assumption is required for this positive measure. Strictly increasing reparameterizations are therefore an immediate special case.

## Separation from temporal activity

The symmetric kinetic activity
\[
\mathfrak a_e=W_{e,+}+W_{e,-}>0
\]
is a pace observable. It is not by itself the canonical event-existence criterion because a positive kinetic activity can exist even when the transition signature \(q_e\) vanishes. The project therefore keeps:

- \(q_e\): gauge-invariant transition/event signature;
- \(M_eq_e\): positive realization weight;
- \(\mathfrak a_e\): positive kinetic activity/pace;
- \(\mathfrak j_e\): signed directional current.

This typing is the input contract for the bifurcation layer.
