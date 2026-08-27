# 02A — Gauge-Covariant Temporal Wave Baseline

Status: `BASELINE_CANDIDATE / BRANCH_VALIDATION`

This branch instantiates the Temporal Wave test baseline from the already declared Shannon/phase links and relational mobility primitives.

For every admitted oriented edge `e:a→b`, let
\[
L_{ab}\in U(1),
\qquad
w_{ab}>0.
\]
Define the covariant edge difference
\[
\boxed{(D_L q)_{ab}=q_b-L_{ab}q_a.}
\]
The quadratic edge energy is
\[
\mathcal E_{ab}=w_{ab}|q_b-L_{ab}q_a|^2.
\]
Summing over edges gives the Hermitian positive-semidefinite operator
\[
\boxed{K_L=D_L^\dagger W D_L.}
\]

The baseline branch supplies the candidate identification
\[
\boxed{w_{ab}=M_{ab}}
\]
through the existing symmetric relational mobility primitive
\[
M_{ab}
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
\]
Its admission is evaluated separately from the structural properties of \(K_L\).

Under a local phase change
\[
q_a\mapsto e^{i\chi_a}q_a,
\qquad
L_{ab}\mapsto e^{i(\chi_b-\chi_a)}L_{ab},
\]
the operator transforms covariantly,
\[
K_L\mapsto U K_L U^\dagger,
\]
so its spectrum is invariant.

For conjugate state variables \((q,p)\), the tested first-order candidate is
\[
\dot q=-p,
\qquad
\dot p=K_Lq-\nu K_Lp,
\qquad \nu\ge0,
\]
equivalent to
\[
\boxed{\ddot q+\nu K_L\dot q+K_Lq=0.}
\]
With
\[
\mathcal H_T=\frac12 p^\dagger p+\frac12 q^\dagger K_Lq,
\]
the declared energy balance is
\[
\boxed{\frac{d\mathcal H_T}{d\lambda}=-\nu p^\dagger K_Lp\le0.}
\]

For a uniform \(N\)-cycle of unit circumference, diffusivity scale \(D>0\), and total link holonomy \(e^{i\phi}\), the branch uses edge weights \(DN^2\). The analytic spectrum is
\[
\boxed{
\lambda_m=4DN^2\sin^2\left(\frac{2\pi m-\phi}{2N}\right).
}
\]
Thus the continuum target is
\[
\lambda_m\to D(2\pi m-\phi)^2.
\]
For \(|\phi|<\pi\), the lowest mode approaches the holonomy gap
\[
\lambda_0\to D\phi^2.
\]

The positive-frequency modal branch for \(K_Lv_r=\lambda_rv_r\) is
\[
\boxed{
\omega_r
=\sqrt{\lambda_r-\frac{\nu^2\lambda_r^2}{4}}
-i\frac{\nu\lambda_r}{2}.
}
\]
For a continuum eigenvalue \(\lambda=Dk^2\) and small \(|k|\),
\[
\operatorname{Re}\omega=\sqrt D\,|k|+O(|k|^3),
\qquad
\operatorname{Im}\omega=-\frac{\nu D}{2}k^2+O(k^4).
\]

Reference implementation: `src/idt/temporal_wave.py`.
Targeted tests: `tests/reference/test_temporal_wave_gauge_laplacian.py`.
