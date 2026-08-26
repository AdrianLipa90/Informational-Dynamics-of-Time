# 06 — Event-Imprinted Memory Dynamics

Status: `MEMORY_FRONTIER_CANDIDATE`

This layer opens only after the Temporal Transport structural gate. It derives the first memory state directly from an admitted event rather than assuming an orbit as an upstream primitive.

## T016 — Gauge-invariant memory imprint decomposition

For pre/post event states define the rank-one positive operators
\[
R_n^- = \Psi_n^- (\Psi_n^-)^\dagger,
\qquad
R_n^+ = \Psi_n^+ (\Psi_n^+)^\dagger.
\]
The raw event imprint is
\[
\boxed{\Delta R_n=R_n^+-R_n^-.}
\]
Because the polar bifurcation class may be contractive, retain the scalar weight
\[
w_n^\pm=\operatorname{tr}R_n^\pm=\|\Psi_n^\pm\|^2,
\qquad
\Delta w_n=w_n^+-w_n^-.
\]
For nonzero states define the projective operators
\[
\bar\rho_n^\pm=\frac{R_n^\pm}{w_n^\pm},
\qquad
\boxed{\Delta M_n=\bar\rho_n^+-\bar\rho_n^-.}
\]
Then \(\Delta M_n\) is Hermitian, traceless and invariant under independent global phase changes of \(\Psi_n^-\) and \(\Psi_n^+\). The pair \((\Delta w_n,\Delta M_n)\) separates scalar event contraction from projective state displacement.

## T017 — Memory-plane projection

Let \(Q_M,P_M\) be declared Hermitian memory observables. Define
\[
X_M(\rho)=\operatorname{tr}(\rho Q_M),
\qquad
Y_M(\rho)=\operatorname{tr}(\rho P_M),
\]
\[
\boxed{m=X_M+iY_M.}
\]
The event displacement is therefore
\[
\boxed{\delta m_n
=\operatorname{tr}(\Delta M_nQ_M)
+i\operatorname{tr}(\Delta M_nP_M).}
\]
This makes the memory plane a projection of the admitted state operator.

## T018 — Central memory dynamics candidate

On smooth memory segments introduce an effective central parameter \(\mu_M>0\) and
\[
\boxed{\ddot m=-\mu_M\frac{m}{|m|^3}.}
\]
For unit effective mass,
\[
E_M=\frac12|\dot m|^2-\frac{\mu_M}{|m|},
\qquad
h_M=\operatorname{Im}(m^*\dot m).
\]
The reference class conserves \(E_M\) and \(h_M\) on smooth segments.

## T019 — Memory areal law

For the central class,
\[
\boxed{\frac{d\mathcal A_M}{d\tau_{\rm int}}=\frac{h_M}{2}.}
\]
The statement follows from \(\dot{\mathcal A}_M=\tfrac12\operatorname{Im}(m^*\dot m)\) and zero central torque.

## T019A — Memory action-area holonomy

The earlier memory circulation identity is
\[
\Gamma_M(C)=\sum_{e\in C}A_e^{(M)}=2\lambda_M\mathcal A_M(C).
\]
For a smooth loop write \(m=re^{i\theta}\). The continuous connection one-form is
\[
\alpha_M=\lambda_M(x\,dy-y\,dx)=\lambda_M r^2d\theta.
\]
Defining
\[
P_A=\lambda_Mr^2,\qquad Q_A=\theta,
\]
gives the normal form
\[
\boxed{\Gamma_M(C)=\oint_C P_A\,dQ_A=\int_S dP_A\wedge dQ_A.}
\]
Hence for constant \(\lambda_M\),
\[
\boxed{\frac{d\Gamma_M}{d\tau_{\rm int}}=\lambda_Mh_M.}
\]
For dynamic coupling,
\[
\frac{d\Gamma_M}{d\tau_{\rm int}}
=\lambda_Mh_M+2\dot\lambda_M\mathcal A_M.
\]
The action-area form here is the symplectic form carried by the oriented memory plane. A Newtonian cotangent-bundle action is admitted into the same numerical identity only after an explicit symplectic reduction or coordinate identification.

## T019B — Berry-memory pullback candidate

In the standard stereographic patch of \(\mathbb{CP}^1\), use
\[
|\psi(z_B)\rangle=\frac{(1,z_B)^T}{\sqrt{1+|z_B|^2}},
\qquad z_B=Re^{i\phi}.
\]
With the real Berry connection convention
\[
\mathcal A_B=-i\langle\psi|d\psi\rangle
=P_B\,d\phi,
\qquad
P_B=\frac{R^2}{1+R^2},
\]
consider a memory region satisfying \(|\lambda_M|r^2<1\). For \(\lambda_M\ne0\) define
\[
P_B=|\lambda_M|r^2,
\qquad
\phi=\operatorname{sgn}(\lambda_M)\theta,
\]
or equivalently
\[
\boxed{R^2=\frac{|\lambda_M|r^2}{1-|\lambda_M|r^2}.}
\]
Then the pullback is exact:
\[
\boxed{\Phi^*\mathcal A_B=\alpha_M,}
\qquad
\boxed{\Phi^*\mathcal F_B=d\alpha_M=2\lambda_M\,dx\wedge dy.}
\]
Consequently every closed loop contained in the admitted patch satisfies
\[
\boxed{\gamma_B[\Phi(C)]=\Gamma_M(C)\pmod{2\pi}.}
\]
This is the explicit pullback condition required by the GREMLIN structural match.

## T019C — Event-driven orbital bifurcation candidate

Let an admitted coupling \(\chi_M\) map the projected event displacement to an orbital impulse,
\[
\Delta v_M=\chi_M\,\delta m_n.
\]
At fixed event position,
\[
\boxed{\Delta E_M
=\operatorname{Re}(v_M^*\Delta v_M)+\frac12|\Delta v_M|^2,}
\]
\[
\boxed{\Delta h_M=\operatorname{Im}(m^*\Delta v_M).}
\]
The post-event pair \((E_M^+,h_M^+)\) determines the next smooth Kepler-class orbit. The coupling \(\chi_M\) and the observables \(Q_M,P_M\) remain explicit model parameters for later derivation/evidence.

## GREMLIN result

GREMLIN compared Kepler swept area, two-dimensional symplectic action-area, Berry holonomy and memory circulation using the typed spine

`CLOSED_PATH -> SPANNING_SURFACE`, `ONE_FORM_CONNECTION -> TWO_FORM_CURVATURE`, boundary integral and surface flux.

All six pairwise structural comparisons matched. The resulting hypothesis is recorded in `validation/gremlin/ACTION_AREA_HOLONOMY_V0_1.json` and remains bounded to structural candidate generation; the equations above provide the independent analytic checks.
