# 02C — Heterogeneous Temporal-Wave Continuum Gate

Status: `BASELINE_CANDIDATE / HOMOGENIZATION_GATE_PASS_CANDIDATE`

This layer tests the long-wave limit of the mobility-stiffness and viscosity-damping operators introduced in 02A–02B for a one-dimensional periodic heterogeneous relational cell.

Let one periodic cell contain `N` edges of spacing `h`, with edge mobility and pair viscosity
\[
M_e>0,
\qquad
\eta_e>0.
\]
The exact Bloch operators at total cell phase \(\theta\) are
\[
K(\theta)=D_\theta^\dagger\operatorname{diag}(M_e)D_\theta,
\qquad
C(\theta)=D_\theta^\dagger\operatorname{diag}(\eta_e)D_\theta,
\]
with physical cell wave number
\[
k=\frac{\theta}{Nh}.
\]
The acoustic branch satisfies
\[
\ddot q+C(\theta)\dot q+K(\theta)q=0.
\]

## H1 — stiffness cell corrector

At long wavelength, let \(g_e\) denote the edge gradient carried by the acoustic mode. The cell problem minimizes
\[
\frac1N\sum_e M_e|g_e|^2
\]
subject to the imposed mean gradient
\[
\frac1N\sum_e g_e=ik.
\]
The constrained minimizer is
\[
\boxed{
g_e=ik\frac{M_{\rm eff}}{M_e}+O(k^2),
}
\]
where
\[
\boxed{
M_{\rm eff}
=\left(\frac1N\sum_e\frac1{M_e}\right)^{-1}.
}
\]
Thus the effective long-wave stiffness is the harmonic mean of the admitted relational edge mobility.

The leading acoustic wave coefficient is
\[
\boxed{c_{\rm eff}^2=M_{\rm eff}.}
\]

## H2 — viscosity evaluated on the stiffness corrector

The damping energy is evaluated on the same acoustic corrector,
\[
\frac1N\sum_e\eta_e|g_e|^2.
\]
Substitution of the stiffness minimizer gives
\[
\boxed{
\beta_{\rm eff}
=M_{\rm eff}^2
\left(\frac1N\sum_e\frac{\eta_e}{M_e^2}\right).
}
\]
Consequently the positive-frequency acoustic branch has the long-wave form
\[
\boxed{
\omega(k)
=\sqrt{M_{\rm eff}}\,|k|
-i\frac{\beta_{\rm eff}}{2}k^2
+O(|k|^3).
}
\]
Equivalently, for the time exponent \(s=-i\omega\),
\[
\operatorname{Im}s=\sqrt{M_{\rm eff}}\,k+O(k^3),
\qquad
\operatorname{Re}s=-\frac{\beta_{\rm eff}}2k^2+O(k^4).
\]

## H3 — substitution of the relational fields

For the already declared nearest-neighbour relational fields,
\[
\eta_e=\bar\eta_j
=\frac{\eta_R(j)+\eta_R(j+1)}2,
\]
\[
M_e
=\frac{\sqrt{\rho_R(j)\rho_R(j+1)}}{\bar\eta_j},
\]
the effective coefficients become
\[
\boxed{
M_{\rm eff}
=\left[
\frac1N\sum_j
\frac{\bar\eta_j}{\sqrt{\rho_R(j)\rho_R(j+1)}}
\right]^{-1},
}
\]
\[
\boxed{
\beta_{\rm eff}
=M_{\rm eff}^2
\frac1N\sum_j
\frac{\bar\eta_j^3}{\rho_R(j)\rho_R(j+1)}.
}
\]
No additional propagation coefficient is inserted into these expressions.

For uniform fields,
\[
\rho_R(j)=\rho_0,
\qquad
\eta_R(j)=\eta_0,
\]
this reduces exactly to
\[
M_{\rm eff}=\frac{\rho_0}{\eta_0},
\qquad
\beta_{\rm eff}=\eta_0,
\]
so
\[
\boxed{
\omega(k)
=\sqrt{\frac{\rho_0}{\eta_0}}\,|k|
-i\frac{\eta_0}{2}k^2+\cdots.
}
\]

Metric-time calibration remains downstream. The coefficient \(c_{\rm eff}\) here is the pre-metric acoustic coefficient with respect to the ordering parameter and the declared cell-coordinate normalization.

## Rejected simple attenuation candidate

The comparison candidate
\[
\beta_{\rm naive}
=\left(\frac1N\sum_e\frac1{\eta_e}\right)^{-1}
\]
was subjected to the same heterogeneous stress ensemble. The stiffness-corrected \(\beta_{\rm eff}\) is retained by the baseline gate; the simple harmonic-viscosity candidate is rejected by that test ensemble.

## Baseline bridge to the earlier fluid-time wave sector

The earlier fluid-time baseline supplies the long-wave form
\[
\omega^2=c_s^2k^2.
\]
The present derivation supplies the corresponding pre-metric coefficient slot
\[
\operatorname{Re}\omega^2=M_{\rm eff}k^2+O(k^4).
\]
The baseline bridge therefore tests the structural correspondence
\[
\boxed{c_s^2\;\longleftrightarrow\;M_{\rm eff}}
\]
while numerical and physical calibration remain downstream tasks.

## Validation

A deterministic ensemble of 500 heterogeneous periodic cells tested the exact Bloch quadratic eigenproblem against the two derived coefficients.

- maximum relative wave-speed error at the finest tested Bloch phase: `5.079114268253267e-05`;
- maximum relative damping-coefficient error: `7.451397791985819e-05`;
- median wave-speed convergence order: `2.000013138257951`;
- median damping convergence order: `2.0000917727223575`;
- median relative error of the rejected harmonic-viscosity candidate: `0.3404187453270899`;
- rejected candidate error above 1%: `499 / 500` cases;
- rejected candidate error above 5%: `486 / 500` cases.

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The structural homogenization comparison matched, and three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with declared counts `2/2`, `2/2`, and `3/3`.

Reference implementation: `src/idt/temporal_wave_homogenization.py`.
Reference tests: `tests/reference/test_temporal_wave_homogenization.py`.
