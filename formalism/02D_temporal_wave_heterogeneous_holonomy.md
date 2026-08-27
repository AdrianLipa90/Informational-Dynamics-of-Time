# 02D — Heterogeneous Temporal Wave with Holonomy

Status: `BASELINE_CANDIDATE / HETEROGENEOUS_HOLONOMY_GATE_PASS_CANDIDATE`

This layer composes the heterogeneous continuum gate with the already admitted U(1) temporal link structure. The purpose is to test whether non-zero closed-cycle holonomy changes the effective transport coefficients or enters as a gauge-invariant shift of the long-wave phase coordinate.

Let the periodic cell contain edge phases \(\alpha_e\) with total holonomy
\[
\phi=\operatorname{Arg}\prod_e e^{i\alpha_e}
=\operatorname{wrap}\!\left(\sum_e\alpha_e\right).
\]
For Bloch phase \(\theta\), the gauge-invariant cell mismatch is
\[
\boxed{\delta=\operatorname{wrap}(\theta-\phi).}
\]
With cell length \(L=Nh\), define
\[
\boxed{k_{\rm eff}=\frac{\delta}{L}.}
\]

The exact operators remain
\[
K_{M,\phi}(\theta)=D_{L,\theta}^\dagger\operatorname{diag}(M_e)D_{L,\theta},
\]
\[
C_{\eta,\phi}(\theta)=D_{L,\theta}^\dagger\operatorname{diag}(\eta_e)D_{L,\theta},
\]
where the internal link phases carry the closed-cycle holonomy and the boundary link carries the Bloch phase.

A local phase redistribution
\[
\alpha_e\mapsto\alpha_e+\chi_{e+1}-\chi_e
\]
preserves \(\phi\) and leaves the spectra of the two operators invariant.

The heterogeneous long-wave coefficients from 02C remain
\[
M_{\rm eff}=\left\langle M_e^{-1}\right\rangle^{-1},
\]
\[
\beta_{\rm eff}=M_{\rm eff}^2\left\langle\frac{\eta_e}{M_e^2}\right\rangle.
\]
The holonomy gate yields the acoustic branch
\[
\boxed{
\omega(k_{\rm eff})
=\sqrt{M_{\rm eff}}\,|k_{\rm eff}|
-i\frac{\beta_{\rm eff}}2k_{\rm eff}^2
+O(|k_{\rm eff}|^3).
}
\]
Thus the effective stiffness and damping are unchanged by redistribution of the same closed-cycle flux, while the phase coordinate is shifted by the total holonomy.

For a uniform ring this reduces to
\[
\lambda_m
=\frac{4M}{h^2}
\sin^2\!\left(\frac{2\pi m+\theta-\phi}{2N}\right),
\]
consistent with the earlier spectral-twist result.

## Falsification gate

The comparison candidate using the unshifted Bloch value \(k=\theta/L\) was tested separately. For non-zero \(\phi\), that candidate does not reproduce the acoustic branch. The tested invariant coordinate is \((\theta-\phi)/L\).

## Validation

A deterministic 500-cell heterogeneous stress ensemble used shifted cell phases `0.02`, `0.01`, `0.005`.

- maximum relative wave-speed error at the finest shift: `1.7891950205440555e-4`;
- maximum relative damping error: `1.367638979986604e-4`;
- median wave-speed convergence order: `2.0000736021939813`;
- median damping convergence order: `1.995918139258115`;
- maximum stiffness-spectrum drift under internal phase redistribution: `5.4569682106375694e-12`;
- median relative error of the rejected unshifted-wave-number candidate: `0.9999737410218146`;
- rejected unshifted candidate above 10% error: `500 / 500` cases.

Targeted branch-equivalent tests: `6 passed`.

GREMLIN v0.5 remained `CANDIDATE_ONLY`. Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `2/2`, and `2/2`.

Reference implementation: `src/idt/temporal_wave_holonomy_homogenization.py`.
Reference tests: `tests/reference/test_temporal_wave_holonomy_homogenization.py`.
