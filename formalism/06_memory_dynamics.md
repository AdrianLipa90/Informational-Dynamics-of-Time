# 06 — Event-Imprinted Memory Dynamics

Status: `MEMORY_FRONTIER_CANDIDATE`

This layer opens only after the Temporal Transport structural gate. It derives the first memory state directly from an admitted event rather than assuming an orbit as an upstream primitive.

## T016A — Gauge-invariant memory imprint decomposition

For pre/post event states define
\[
R_n^- = \Psi_n^- (\Psi_n^-)^\dagger,\qquad R_n^+ = \Psi_n^+ (\Psi_n^+)^\dagger.
\]
Retain the scalar contraction channel
\[
w_n^\pm=\operatorname{tr}R_n^\pm,\qquad \Delta w_n=w_n^+-w_n^-,
\]
and, for nonzero states, the projective channel
\[
\bar\rho_n^\pm=R_n^\pm/w_n^\pm,\qquad \boxed{\Delta M_n=\bar\rho_n^+-\bar\rho_n^-}.
\]
Then \(\Delta M_n\) is Hermitian, traceless and invariant under independent global phase changes of the pre/post states.

## T016B — Memory-plane projection

Let \(Q_M,P_M\) be declared Hermitian memory observables. Define
\[
\boxed{m=\operatorname{tr}(\rho Q_M)+i\operatorname{tr}(\rho P_M)},
\]
so an event imprint projects to
\[
\boxed{\delta m_n=\operatorname{tr}(\Delta M_nQ_M)+i\operatorname{tr}(\Delta M_nP_M)}.
\]

## T016 / T017 — Kepler–Newton smooth memory segment

The canonical smooth reference class remains
\[
\boxed{\ddot m=-\mu_M\frac{m}{|m|^3}},\qquad \mu_M>0,
\]
with signed angular momentum and areal law
\[
h_M=\operatorname{Im}(m^*\dot m),\qquad \boxed{\frac{d\mathcal A_M}{d\tau_{\rm int}}=\frac{h_M}{2}}.
\]
These are the already registered T016 and T017 claims.

## T019A — Memory action-area holonomy

The memory circulation identity
\[
\Gamma_M(C)=2\lambda_M\mathcal A_M(C)
\]
admits the continuous one-form
\[
\alpha_M=\lambda_M(x\,dy-y\,dx)=\lambda_Mr^2d\theta.
\]
With \(P_A=\lambda_Mr^2\) and \(Q_A=\theta\),
\[
\boxed{\Gamma_M(C)=\oint_C P_A\,dQ_A=\int_S dP_A\wedge dQ_A}.
\]
For constant \(\lambda_M\),
\[
\boxed{\frac{d\Gamma_M}{d\tau_{\rm int}}=\lambda_Mh_M}.
\]

## T019B — Berry-memory pullback candidate

In a stereographic patch of \(\mathbb{CP}^1\), with real Berry connection \(\mathcal A_B=P_Bd\phi\), set on \(|\lambda_M|r^2<1\)
\[
P_B=|\lambda_M|r^2,\qquad \phi=\operatorname{sgn}(\lambda_M)\theta,\qquad R^2=\frac{|\lambda_M|r^2}{1-|\lambda_M|r^2}.
\]
Then
\[
\boxed{\Phi^*\mathcal A_B=\alpha_M},\qquad \boxed{\Phi^*\mathcal F_B=d\alpha_M=2\lambda_M\,dx\wedge dy}.
\]
This supplies the explicit local pullback condition behind the action-area structural match.

## T019C — Event-driven orbital bifurcation candidate

For an admitted coupling \(\chi_M\),
\[
\Delta v_M=\chi_M\delta m_n.
\]
At fixed event position,
\[
\boxed{\Delta E_M=\operatorname{Re}(v_M^*\Delta v_M)+\frac12|\Delta v_M|^2},\qquad
\boxed{\Delta h_M=\operatorname{Im}(m^*\Delta v_M)}.
\]
The post-event invariants determine the next smooth Kepler-class orbit. The coupling and memory observables remain explicit model parameters for later derivation/evidence.

## GREMLIN result

GREMLIN compared Kepler swept area, two-dimensional symplectic action-area, Berry holonomy and memory circulation using a shared boundary-holonomy / curvature-flux spine. Pairwise structural comparisons matched 6/6. Structural salience has no claim-promotion authority; analytic identities and validation remain the admission route.
