# 02B — Temporal Wave Mobility–Viscosity Derivation Gate

Status: `BASELINE_CANDIDATE / DERIVATION_GATE_PASS_CANDIDATE`

This branch layer tests whether the free edge stiffness and scalar damping introduced in the first gauge-wave baseline can be reduced to already declared relational fields.

## D1 — mobility weight from the admitted zero-drive kinetics

The existing relational kinetics define
\[
M_{ab}=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\bar\eta_{ab}},
\qquad
\bar\eta_{ab}=\frac{\eta_R(a)+\eta_R(b)}{2},
\]
and
\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2}.
\]
At zero antisymmetric drive, \(A_{ab}=0\),
\[
\boxed{W_{a\to b}=W_{b\to a}=M_{ab}.}
\]
For the corresponding symmetric continuous-time generator \(G_0\), the real Dirichlet form is
\[
-\langle q,G_0q\rangle
=\sum_{\{a,b\}}M_{ab}|q_b-q_a|^2.
\]
Therefore the untwisted graph operator is exactly
\[
\boxed{K_0=-G_0=D^\dagger\operatorname{diag}(M_{ab})D.}
\]
The gauge-covariant lift keeps the already derived kinetic edge weight and replaces the ordinary edge difference by the admitted phase-covariant difference,
\[
(D_Lq)_{ab}=q_b-L_{ab}q_a,
\]
so the branch candidate becomes
\[
\boxed{K_M=D_L^\dagger\operatorname{diag}(M_{ab})D_L.}
\]
Thus \(w_{ab}=M_{ab}\) is fixed by the zero-drive symmetric kinetic sector rather than introduced as an independent branch coefficient.

## D2 — viscosity as an edge-local damping operator

The same pair viscosity already present in the mobility denominator supplies the tested damping weight
\[
\bar\eta_{ab}=\frac{\eta_R(a)+\eta_R(b)}{2}.
\]
Define
\[
\boxed{C_\eta=D_L^\dagger\operatorname{diag}(\bar\eta_{ab})D_L.}
\]
The operator-damped first-order system is
\[
\dot q=-p,
\qquad
\dot p=K_Mq-C_\eta p,
\]
equivalent to
\[
\boxed{\ddot q+C_\eta\dot q+K_Mq=0.}
\]
For
\[
\mathcal H_T=\frac12p^\dagger p+\frac12q^\dagger K_Mq,
\]
the exact branch identity is
\[
\boxed{\frac{d\mathcal H_T}{d\lambda}=-p^\dagger C_\eta p\le0.}
\]
Both \(K_M\) and \(C_\eta\) are Hermitian positive-semidefinite and transform by the same local \(U(1)\) conjugation.

## D3 — scalar damping factorization gate

The earlier scalar form \(C_\eta=\nu K_M\) is available when every declared edge shares one ratio
\[
\bar\eta_{ab}=\nu M_{ab}.
\]
Therefore each local candidate is
\[
\boxed{\nu_{ab}=\frac{\bar\eta_{ab}}{M_{ab}}
=\frac{\bar\eta_{ab}^2}{\sqrt{\rho_R(a)\rho_R(b)}}.}
\]
The reference implementation returns one scalar \(\nu\) only if these edge-local values agree within the declared numerical tolerance. Heterogeneous edge sets that do not factor to one scalar are retained as the operator \(C_\eta\), and an attempted scalar collapse fails closed.

For uniform fields
\[
\rho_R(a)=\rho_0,
\qquad
\eta_R(a)=\eta_0,
\]
we have
\[
M=\frac{\rho_0}{\eta_0},
\qquad
\boxed{\nu=\frac{\eta_0}{M}=\frac{\eta_0^2}{\rho_0}.}
\]
Under a common continuum geometric scaling, the small-mode structure is
\[
\operatorname{Re}\omega\sim\sqrt M\,|k|,
\qquad
\operatorname{Im}\omega\sim-\frac{\eta_0}{2}k^2.
\]
This remains a baseline bridge target rather than a variable identification with the earlier fluid-time model.

## Validation status

Exact branch-equivalent targeted suite after this layer: `18 passed in 0.92s`.

Additional deterministic derivation probe: 500 heterogeneous cases.

- zero-drive generator / mobility Dirichlet maximum defect: `0.0`;
- maximum gauge covariance defect for `K_M`: `2.0791723739534308e-14`;
- maximum gauge covariance defect for `C_eta`: `1.0658141036401503e-14`;
- maximum energy-balance defect: `1.4210854715202004e-13`;
- heterogeneous scalar-factorable cases at `1e-10` tolerance: `0 / 500`;
- smallest heterogeneous local-ratio spread observed: `0.08037424954165173`;
- uniform `nu=eta^2/rho` maximum error: `5.684341886080802e-14`.

GREMLIN v0.5 remained `CANDIDATE_ONLY`. Two relational comparisons were structurally isomorphic, and three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with test counts `2/2`, `3/3`, and `3/3`.

GitHub-hosted full-suite evidence remains a separate gate. The preceding two workflow attempts ended before checkout with `steps: []`, so their status remains `CI_INFRA_BLOCKED_BEFORE_STEPS`.

Reference implementation: `src/idt/temporal_wave_dissipation.py`.
Reference tests: `tests/reference/test_temporal_wave_mobility_viscosity.py`.
