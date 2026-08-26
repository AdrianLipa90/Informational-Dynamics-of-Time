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

**EQ-T050 — energy/clock calibration**
\[
\Delta\phi_t=-\frac{E\Delta t}{\hbar}.
\]
