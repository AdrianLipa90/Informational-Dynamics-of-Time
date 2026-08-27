# 03B — Temporal Wave Activation of NOW

Status: `CANDIDATE / TEMPORAL_WAVE_DEPENDENCY_GATE_PASS`

This layer connects the admitted Temporal Wave candidate stack 02A–02D to the existing structural NOW carrier.

The structural transition signature remains
\[
q_e=
\sqrt{
 d_{FS}(a,b)^2+
 \kappa^2\Delta H_e^2+
 \kappa^2\sigma_e^2
}\ge0,
\]
with structural carrier
\[
\mathcal N_{\rm sig}
=\operatorname{supp}_{\rm at}
\left(\sum_e q_e\,\delta_{s_e}\right).
\]

## Kinetic invariant carried into Temporal Wave

For the directed kinetic pair
\[
W_{e,+}=M_e e^{A_e/2},
\qquad
W_{e,-}=M_e e^{-A_e/2},
\]
the symmetric activity and directed current are
\[
\mathfrak a_e=2M_e\cosh(A_e/2),
\qquad
\mathfrak j_e=2M_e\sinh(A_e/2).
\]
Therefore
\[
\boxed{
\mathfrak a_e^2-\mathfrak j_e^2=4M_e^2
}
\]
and the mobility entering the Temporal Wave stiffness is exactly reconstructible from the NOW auxiliary observables,
\[
\boxed{
M_e=\frac12\sqrt{\mathfrak a_e^2-\mathfrak j_e^2}.
}
\]
The stiffness coefficient used by the wave layer is therefore the hyperbolic invariant of the pace/current pair already available at the NOW boundary.

## Gauge-invariant wave activation

Let \(\Phi\) be the node amplitude of the Temporal Wave and
\[
(D_L\Phi)_e=\Phi_b-L_{ab}\Phi_a.
\]
Define the edge activation
\[
\boxed{
\epsilon_e^{(W)}
=M_e\,|(D_L\Phi)_e|^2
=\frac12
\sqrt{\mathfrak a_e^2-\mathfrak j_e^2}
\,|(D_L\Phi)_e|^2
\ge0.
}
\]
Under the local phase transformation
\[
\Phi_a\mapsto e^{i\chi_a}\Phi_a,
\qquad
L_{ab}\mapsto e^{i(\chi_b-\chi_a)}L_{ab},
\]
the covariant edge difference acquires only the target-node phase. Hence
\[
|(D_L\Phi)_e|^2
\]
and \(\epsilon_e^{(W)}\) are gauge invariant.

For a covariantly parallel state,
\[
(D_L\Phi)_e=0,
\]
so the corresponding edge activation vanishes exactly.

## Wave-active realization measure

The two positive local scalars \(q_e\) and \(\epsilon_e^{(W)}\) live on the same admitted transition carrier. Define
\[
\boxed{
\mathcal R_{\rm NOW}^{(W)}
=\sum_e
q_e\epsilon_e^{(W)}\,\delta_{s_e}.
}
\]
Its atomic support is
\[
\boxed{
\mathcal N_W
=\operatorname{supp}_{\rm at}\mathcal R_{\rm NOW}^{(W)}
=\mathcal N_{\rm sig}
\cap
\operatorname{supp}\{e:\epsilon_e^{(W)}>0\}.
}
\]
The equality follows from positivity: the product weight is strictly positive exactly on edges carrying both a structural transition signature and wave activation.

The structural carrier \(\mathcal N_{\rm sig}\) is retained for transition typing and lineage. The wave-active carrier \(\mathcal N_W\) supplies the dynamical realization candidate consumed by the next bifurcation gate.

## Total activation and holonomy gap

The total edge activation is the Temporal Wave quadratic form,
\[
\boxed{
\sum_e\epsilon_e^{(W)}
=\Phi^\dagger K_M\Phi,
\qquad
K_M=D_L^\dagger\operatorname{diag}(M_e)D_L.
}
\]
Whenever the lowest eigenvalue obeys \(\lambda_{\min}(K_M)>0\),
\[
\Phi^\dagger K_M\Phi
\ge
\lambda_{\min}(K_M)\|\Phi\|^2.
\]
The nontrivial-holonomy ring tested in 02A/02D supplies the exact gap
\[
\lambda_{\min}
=4M\sin^2\left(\frac{\phi}{2N}\right)>0
\]
for the principal branch \(|\phi|<\pi\) and \(\phi\ne0\). Thus every nonzero wave state on that tested ring carries positive total wave activation.

## GREMLIN relation gate

GREMLIN compared the existing structural-event architecture and the wave-activation architecture using the typed chain

`LOCAL_NONNEGATIVE_SCALAR -> POSITIVE_ATOMIC_MEASURE -> ATOMIC_SUPPORT`.

The comparison returned `structurally_isomorphic=true`, comparison SHA-256
`4291d8156d4028ec3c61112da03cd3a9f798b56bada0726b48be88299c726c65`.

Three explicit hypotheses were then evaluated in `CANDIDATE_ONLY` authority mode and returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `3/3`, and `1/1`.

Reference implementation: `src/idt/now_wave_activation.py`.
Reference tests: `tests/reference/test_now_wave_activation.py`.
