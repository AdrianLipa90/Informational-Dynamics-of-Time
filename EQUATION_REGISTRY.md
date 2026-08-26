# Equation Registry

Canonical equation IDs are stable across monograph revisions.

**EQ-T001 — informational normalization**
\[
\kappa=\frac{\ln2}{24\pi}.
\]

**EQ-T002 — Shannon relational state entropy**
\[
H_S(s)=-\sum_i p_i(s)\log_2 p_i(s).
\]

**EQ-T003 — exact entropy transition difference**
\[
\Delta H_e=H_S(b)-H_S(a),
\qquad
\sum_{e\in C}\Delta H_e=0.
\]

**EQ-T004 — normalized geometric phase link**
\[
G_{a\to b}=\frac{\langle\psi_a|\psi_b\rangle}{|\langle\psi_a|\psi_b\rangle|}.
\]

**EQ-T006 — Shannon--phase composite transition link**
\[
L_e=G_e\exp\!\left[i\kappa(\Delta H_e+\sigma_e)\right].
\]

**EQ-T007 — closed-cycle decomposition**
\[
\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=\gamma_B(C)+\kappa\sum_{e\in C}\sigma_e\pmod{2\pi}.
\]

**EQ-T008 — directed transition affinity**
\[
\sigma_{a\to b}=\log_2\frac{P(b\mid a)}{P(a\mid b)}.
\]

**EQ-T009 — closed-cycle affinity**
\[
\mathcal A_C
=\sum_{e\in C}\sigma_e
=\log_2\prod_{e\in C}\frac{P_{e,+}}{P_{e,-}}.
\]

**EQ-T009B — Shannon--phase cycle closure with path affinity**
\[
\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=\gamma_B(C)+\kappa\mathcal A_C\pmod{2\pi}.
\]

**EQ-T009C — relational pair mobility**
\[
M_{ab}
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
\]

**EQ-T009D — directed kinetic pair**
\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2}.
\]

**EQ-T009E — affinity from antisymmetric edge drive**
\[
\sigma_{a\to b}=\frac{A_{ab}}{\ln2}.
\]

**EQ-T009F — symmetric temporal activity**
\[
\mathfrak a_{ab}=W_{a\to b}+W_{b\to a}=2M_{ab}\cosh(A_{ab}/2)>0.
\]

**EQ-T009G — directed temporal current**
\[
\mathfrak j_{ab}=W_{a\to b}-W_{b\to a}=2M_{ab}\sinh(A_{ab}/2).
\]

**EQ-T009H — edge-drive reconstruction**
\[
A_{ab}=2\operatorname{artanh}\!\left(\frac{\mathfrak j_{ab}}{\mathfrak a_{ab}}\right),
\qquad
\sigma_{ab}=\frac{A_{ab}}{\ln2}.
\]

**EQ-T009M — oriented memory drive**
\[
A^{(M)}_{ab}=\lambda_M\operatorname{Im}[m(a)^*m(b)].
\]

**EQ-T009N — memory circulation / signed area**
\[
\sum_C A^{(M)}_e=2\lambda_M\mathcal A_M(C).
\]

**EQ-T010 — relational phase transport**
\[
\Psi_{n+1}=U_n\Psi_n.
\]

**EQ-T011 — phase-only transport candidate**
\[
\Psi_{n+1}=e^{-i\Omega_n}\Psi_n.
\]

**EQ-T014 — system-internal elapsed activity**
\[
d\tau_{\rm int}=\frac{\mathfrak a(\lambda)}{\mathfrak a_\star}\,d\lambda.
\]

**EQ-T014B — discrete internal elapsed activity**
\[
\tau_{{\rm int},N}=\sum_{n=0}^{N-1}\frac{\mathfrak a_n}{\mathfrak a_\star}\,\Delta\lambda_n,
\qquad \Delta\lambda_n>0.
\]

**EQ-T015 — activity one-density covariance**
\[
\mathfrak a'(\lambda')=\mathfrak a(\lambda)\frac{d\lambda}{d\lambda'},
\qquad
d\tau'_{\rm int}=d\tau_{\rm int}.
\]

**EQ-T016 — Newton memory dynamics in internal elapsed activity**
\[
\frac{d^2m}{d\tau_{\rm int}^2}
=-\mu_M\frac{m}{|m|^3},
\qquad \mu_M>0.
\]

**EQ-T016A — memory specific energy**
\[
\varepsilon_M
=\frac12\left|\frac{dm}{d\tau_{\rm int}}\right|^2
-\frac{\mu_M}{r_M}.
\]

**EQ-T016B — event memory imprint decomposition**
\[
R_n^\pm=\Psi_n^\pm(\Psi_n^\pm)^\dagger,
\qquad
\Delta w_n=\operatorname{tr}R_n^+-\operatorname{tr}R_n^-,
\]
\[
\bar\rho_n^\pm=\frac{R_n^\pm}{\operatorname{tr}R_n^\pm},
\qquad
\Delta M_n=\bar\rho_n^+-\bar\rho_n^-.
\]

**EQ-T016C — memory-plane projection**
\[
m=\operatorname{tr}(\rho Q_M)+i\operatorname{tr}(\rho P_M),
\]
\[
\delta m_n=\operatorname{tr}(\Delta M_nQ_M)+i\operatorname{tr}(\Delta M_nP_M).
\]

**EQ-T017 — signed memory angular momentum and areal law**
\[
h_M=\operatorname{Im}\!\left[m^*\frac{dm}{d\tau_{\rm int}}\right],
\qquad
\frac{d\mathcal A_M}{d\tau_{\rm int}}=\frac{h_M}{2}.
\]

**EQ-T017A — circulation rate on a smooth Kepler segment**
\[
\frac{d}{d\tau_{\rm int}}\left(\sum_C A_e^{(M)}\right)=\lambda_M h_M.
\]

**EQ-T018 — memory conic law and third law**
\[
r_M(\nu)=\frac{p_M}{1+e_M\cos\nu},
\qquad
p_M=\frac{h_M^2}{\mu_M},
\]
\[
a_M=-\frac{\mu_M}{2\varepsilon_M},
\qquad
T_M^2=\frac{4\pi^2}{\mu_M}a_M^3
\quad(\varepsilon_M<0).
\]

**EQ-T019 — bifurcation-to-memory impulse interface**
\[
\mathbf v_M^+=\mathbf v_M^-+\Delta\mathbf v_M.
\]

**EQ-T019A — temporal activity to memory propagation step**
\[
\Delta\tau_{\rm int}
=\frac{\mathfrak a}{\mathfrak a_\star}\Delta\lambda,
\qquad
(m,\dot m)_{n+1}=\Phi_{K}(\Delta\tau_{\rm int};\mu_M)(m,\dot m)_n.
\]

**EQ-T019B — memory action-area holonomy**
\[
\alpha_M=\lambda_Mr^2d\theta,
\qquad
P_A=\lambda_Mr^2,
\qquad Q_A=\theta,
\]
\[
\Gamma_M(C)=\oint_C P_A\,dQ_A=\int_S dP_A\wedge dQ_A.
\]
For constant \(\lambda_M\),
\[
\frac{d\Gamma_M}{d\tau_{\rm int}}=\lambda_Mh_M.
\]

**EQ-T019C — exact local Berry-memory pullback**
\[
P_B=|\lambda_M|r^2,
\qquad
\phi=\operatorname{sgn}(\lambda_M)\theta,
\qquad
R^2=\frac{|\lambda_M|r^2}{1-|\lambda_M|r^2},
\]
\[
\Phi^*\mathcal A_B=\alpha_M,
\qquad
\Phi^*\mathcal F_B=d\alpha_M=2\lambda_M\,dx\wedge dy,
\qquad
|\lambda_M|r^2<1.
\]

**EQ-T019D — general event-driven memory impulse family**
\[
\Delta v_M=\chi_M\delta m_n,
\]
\[
\Delta E_M=\operatorname{Re}(v_M^*\Delta v_M)+\frac12|\Delta v_M|^2,
\qquad
\Delta h_M=\operatorname{Im}(m^*\Delta v_M).
\]

**EQ-T019E — upstream-driven event action and derived kick**
\[
S_n^{(M)}(m)=q_n\operatorname{Re}(\delta m_n^*m),
\]
\[
L_M=\frac12|\dot m|^2+\frac{\mu_M}{|m|}+\sum_n\delta(\tau_{\rm int}-\tau_n)S_n^{(M)}(m),
\]
\[
\boxed{\Delta v_{M,n}=q_n\delta m_n.}
\]

**EQ-T019F — exact invariant changes under the derived kick**
\[
\Delta E_M
=q_n\operatorname{Re}(v_M^*\delta m_n)
+\frac12q_n^2|\delta m_n|^2,
\]
\[
\Delta h_M=q_n\operatorname{Im}(m^*\delta m_n).
\]

**EQ-T019G — central parameter from angular momentum and conic geometry**
\[
\boxed{\mu_M=\frac{h_M^2}{p_M}},
\qquad
p_M=\frac{2r_pr_a}{r_p+r_a}
=a_M(1-e_M^2).
\]

**EQ-T019H — central parameter from internal period**
\[
\boxed{\mu_M=\frac{4\pi^2a_M^3}{T_M^2}}.
\]

**EQ-T019I — central parameter from memory circulation**
\[
\boxed{
\mu_M
=\frac{1}{p_M}
\left(
\frac{1}{\lambda_M}
\frac{d\Gamma_M}{d\tau_{\rm int}}
\right)^2.
}
\]

**EQ-T019J — CP1 half-angle Fubini--Study logarithm**
\[
\theta_{ab}=\arccos(\mathbf n_a\cdot\mathbf n_b),
\qquad
d_{FS}(a,b)=\frac{\theta_{ab}}{2},
\]
\[
\boxed{
\xi^{FS}_{a\to b}
=\frac12\frac{\theta_{ab}}{\sin\theta_{ab}}
\left(\mathbf n_b-\cos\theta_{ab}\,\mathbf n_a\right),
\qquad
\|\xi^{FS}_{a\to b}\|=d_{FS}(a,b).
}
\]

**EQ-T019K — CP1 Kähler memory dyad and local displacement**
\[
\mathbf e_Q=\frac{\xi^{FS}}{\|\xi^{FS}\|},
\qquad
\mathbf e_P=\mathbf n\times\mathbf e_Q,
\]
\[
\boxed{
\delta m
=\xi^{FS}\cdot\mathbf e_Q
+i\,\xi^{FS}\cdot\mathbf e_P,
\qquad
|\delta m|=d_{FS}.
}
\]

**EQ-T019L — CP1 geodesic memory-frame transport**
\[
\boxed{
\mathbf e_Q^{(b)}=R_{b\leftarrow a}\mathbf e_Q^{(a)},
\qquad
\mathbf e_P^{(b)}=R_{b\leftarrow a}\mathbf e_P^{(a)},
}
\]
where \(R_{b\leftarrow a}\in SO(3)\) is the minimal non-antipodal Bloch-geodesic rotation, with
\[
\mathbf e_P^{(b)}=\mathbf n_b\times\mathbf e_Q^{(b)}.
\]

**EQ-T019M — persistent memory-event receipt and kick**
\[
\boxed{\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n)},
\qquad
\boxed{K_{\mathcal E_n}:v_M\mapsto v_M+q_n\delta m_n}.
\]

**EQ-T019N — reversible memory-lineage cell**
\[
\boxed{
\mathcal C_n
=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n},
}
\]
\[
\boxed{
\mathcal C_n^{-1}
=K_{\mathcal E_n}^{-1}\circ\Phi_K^{-1}(\Delta\tau_n;\mu_M).
}
\]
For the velocity--Verlet reference step,
\[
\boxed{r_0=r_1-v_1\Delta\tau+\frac12a_1\Delta\tau^2},
\qquad
\boxed{v_0=v_1-\frac12(a_0+a_1)\Delta\tau}.
\]

**EQ-T020 — atomic temporal transition measure**
\[
\mathcal K_T=\sum_n q_n\,\delta_{s_n}.
\]

**EQ-T020A — positive temporal activity measure**
\[
\mathcal A_T=\sum_n\mathfrak a_n\,\delta_{s_n},
\qquad \mathfrak a_n>0.
\]

**EQ-T021 — signed NOW support lineage**
\[
\mathcal N=\operatorname{supp}_{\rm at}\mathcal K_T.
\]

**EQ-T021A — active NOW support**
\[
\mathcal N=\operatorname{supp}_{\rm at}\mathcal A_T.
\]

**EQ-T022 — bifurcation transition law**
\[
\Psi_T(s_n^+)=B(q_n)\Psi_T(s_n^-).
\]

**EQ-T023A — positive pushforward-support identity**
\[
\operatorname{supp}_{\rm at}(f_*\mathcal A_T)
=f\!\left(\operatorname{supp}_{\rm at}\mathcal A_T\right).
\]

**EQ-T034 — ledger-assisted recall reconstruction**
\[
X_N=\mathcal C_{N-1}\cdots\mathcal C_1\mathcal C_0X_0,
\]
\[
\boxed{
\operatorname{RECALL}_{N\to0}
=\mathcal C_0^{-1}\mathcal C_1^{-1}\cdots\mathcal C_{N-1}^{-1},
}
\]
\[
\boxed{
\operatorname{RECALL}_{N\to0}(X_N;\{\mathcal E_n\},\mu_M)=X_0
}
\]
within the declared reversible reference class and complete persisted lineage.

**EQ-T050 — energy/clock calibration**
\[
\Delta\phi_t=-\frac{E\Delta t}{\hbar}.
\]
