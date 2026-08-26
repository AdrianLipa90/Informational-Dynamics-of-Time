# CURRENT THEORY STATE

Status: `SHANNON_PHASE_CORE_V0_2`

The temporal programme now has an explicit upstream directed-transition core:

\[
\text{relational state}
\to (H_S,\psi)
\to (\Delta H_e,G_e)
\to \sigma_e
\to L_e
\to q_e
\to \mathcal K_T.
\]

The first candidate microscopic closure of the non-exact edge increment is
\[
\sigma_{a\to b}=\log_2\frac{P(b\mid a)}{P(a\mid b)}.
\]
It is antisymmetric and produces the cycle affinity
\[
\mathcal A_C=\sum_{e\in C}\sigma_e.
\]
Under a pairwise detailed-balance representation, \(\mathcal A_C=0\). Otherwise the candidate composite cycle phase is
\[
\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=\gamma_B(C)+\kappa\mathcal A_C\pmod{2\pi}.
\]

Immediate derivational target: derive the forward/reverse transition weights from relational density \(\rho_R\) and viscosity \(\eta_R\), rather than supplying them externally.
