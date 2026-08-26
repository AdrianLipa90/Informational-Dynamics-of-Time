# Claim Registry

| ID | Statement | Depends on | Evidence class | Status | Monograph |
|---|---|---|---|---|---|
| T001 | \(\kappa=\ln2/(24\pi)\) | TIR | inherited structural definition | `INHERITED_MODEL_POSTULATE` | Ch. 2 |
| T002 | Relational state entropy is \(H_S(s)=-\sum_i p_i(s)\log_2 p_i(s)\) | relational probability state | definition | `FORMAL_DEFINITION` | Ch. 1 |
| T003 | Exact Shannon differences telescope on every closed directed cycle: \(\sum_C \Delta H_e=0\) | T002 | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 1 |
| T004 | Normalized overlap \(G_e=\langle\psi_a|\psi_b\rangle/|\langle\psi_a|\psi_b\rangle|\) is an open gauge-covariant U(1) link; its closed product is gauge-invariant | complex relational state | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 1 |
| T006 | Candidate composite link \(L_e=G_e e^{i\kappa(\Delta H_e+\sigma_e)}\) yields closed-cycle phase \(\gamma_B+\kappa\sum_C\sigma_e\) | T001–T004 + edge quantity \(\sigma_e\) | conditional derivation + reference tests | `CANDIDATE_WITH_PROVED_CLOSURE` | Ch. 1 |
| T007 | Directed transition affinity is \(\sigma_{a\to b}=\log_2[P(b\mid a)/P(a\mid b)]\) and is antisymmetric under edge reversal | directed transition pair | algebraic theorem + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_IDENTITY` | Ch. 1 |
| T008 | If a positive relational weight \(\pi\) satisfies pairwise detailed balance, every closed-cycle affinity \(\mathcal A_C=\sum_C\sigma_e\) vanishes | T007 | algebraic theorem + reference tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 1 |
| T009 | Symmetric pair mobility \(M_{ab}=\sqrt{\rho_a\rho_b}/[(\eta_a+\eta_b)/2]\) controls pace and cancels from the forward/reverse affinity ratio | T007 + positive scalar fields | algebraic theorem + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_IDENTITY` | Ch. 1 |
| T009A | If \(A_{ab}=V_R(b)-V_R(a)\), then the closed-cycle drive and cycle affinity vanish | T009 | algebraic theorem + reference tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 1 |
| T009B | Memory-orbit drive \(A^{(M)}_{ab}=\lambda_M\operatorname{Im}[m(a)^*m(b)]\) is antisymmetric | T009 + oriented memory coordinate | algebraic theorem + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_IDENTITY` | Ch. 8 |
| T009C | Closed memory-orbit drive equals \(2\lambda_M\mathcal A_M(C)\), twice coupling times signed polygon area | T009B | shoelace identity + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 8 |
| T010 | Temporal state admits ordered phase transport \(\Psi_{n+1}=U_n\Psi_n\) | T001 | formal candidate | `CANDIDATE` | Ch. 3–4 |
| T011 | For unitary phase-only transport, \(U_n=e^{-i\Omega_n}\) | T010 | algebraic derivation | `CANDIDATE` | Ch. 4 |
| T012 | Directed rates decompose into positive activity \(\mathfrak a=W_++W_-\) and signed current \(\mathfrak j=W_+-W_-\) | T009 | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 5 |
| T013 | The edge drive is recoverable from \(A=2\operatorname{artanh}(\mathfrak j/\mathfrak a)\) for finite positive rates | T012 | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 5 |
| T014 | System-internal elapsed activity obeys \(d\tau_{\rm int}=(\mathfrak a/\mathfrak a_\star)d\lambda\) and is strictly monotone for positive admitted activity and increasing order parameter | T012 | formal candidate + theorem + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_MONOTONICITY` | Ch. 10 |
| T015 | Under increasing reparameterization, activity transforms as a one-density so \(d\tau_{\rm int}\) is invariant | T014 | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 10 |
| T016 | Event imprint decomposes into scalar weight change \(\Delta w_n\) and a Hermitian traceless projective imprint \(\Delta M_n=\bar\rho_n^+-\bar\rho_n^-\), invariant under independent global phases | Temporal Transport + polar bifurcation | algebraic identities + delta reference tests | `MEMORY_FRONTIER_CANDIDATE_WITH_PROVED_INVARIANTS` | Ch. 8 |
| T017 | Hermitian observables \(Q_M,P_M\) define the memory-plane projection \(m=\operatorname{tr}(\rho Q_M)+i\operatorname{tr}(\rho P_M)\) and project event imprints to \(\delta m\) | T016 | formal definition + delta reference tests | `MEMORY_FRONTIER_DEFINITION` | Ch. 8 |
| T018 | Smooth memory segments admit the effective central reference class \(\ddot m=-\mu_Mm/|m|^3\) with \(\mu_M>0\) | T017 | dynamical candidate + reference controls | `MEMORY_DYNAMICS_CANDIDATE` | Ch. 8 |
| T019 | The central memory reference class obeys \(d\mathcal A_M/d\tau_{\rm int}=h_M/2\), with \(h_M=\operatorname{Im}(m^*\dot m)\) | T018 | central-force identity + delta reference tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 8 |
| T019A | Memory circulation admits the action-area normal form \(\Gamma_M=\oint P_A dQ_A=\int dP_A\wedge dQ_A\), where \(P_A=\lambda_Mr^2\), \(Q_A=\theta\) | T009C + T019 | differential-form derivation + delta reference tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 8 |
| T019B | On the patch \(|\lambda_M|r^2<1\), the map \(R^2=|\lambda_M|r^2/(1-|\lambda_M|r^2)\), \(\phi=\operatorname{sgn}(\lambda_M)\theta\) pulls the CP1 Berry connection and curvature back exactly to the memory action-area connection and curvature | T004 + T019A | exact local pullback derivation + delta reference tests | `PROVED_LOCAL_PULLBACK_IDENTITY` | Ch. 8 |
| T019C | An admitted event-to-orbit coupling \(\Delta v_M=\chi_M\delta m_n\) updates \(E_M\) and \(h_M\) by the exact impulse formulas | T017–T019 | algebraic update identity + delta reference tests | `MEMORY_BIFURCATION_CANDIDATE` | Ch. 8 |
| T020 | Phase-bearing transition measure \(\mathcal K_T=\sum_n q_n\delta_{s_n}\) carries signed transition weights | T010 | source-grounded structural candidate | `CANDIDATE` | Ch. 5 |
| T020A | Positive temporal activity measure is \(\mathcal A_T=\sum_n\mathfrak a_n\delta_{s_n}\) with \(\mathfrak a_n>0\) | T012 | formal definition + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_POSITIVITY` | Ch. 5 |
| T021 | Signed-measure NOW lineage based on \(\operatorname{supp}_{\rm at}\mathcal K_T\) | T020 | GREMLIN + formal candidate | `REFINED_BY_T021A` | Ch. 5 |
| T021A | Active NOW candidate is \(\mathcal N=\operatorname{supp}_{\rm at}\mathcal A_T\) | T020A | positive-measure refinement + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_SUPPORT_PROPERTIES` | Ch. 5 |
| T022 | \(\Psi_T(s_n^+)=B(q_n)\Psi_T(s_n^-)\) | T021 | formal candidate | `CANDIDATE` | Ch. 6 |
| T023 | Injective pushforward-support lineage for signed atoms | T021 | proved lemma | `REFINED_BY_T023A` | Ch. 5 |
| T023A | Positive atomic activity support satisfies \(\operatorname{supp}_{\rm at}(f_*\mathcal A_T)=f(\operatorname{supp}_{\rm at}\mathcal A_T)\) for any map defined on the support | T020A–T021A | positive-measure theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 5 |
| T050 | \(\Delta\phi_t=-E\Delta t/\hbar\) calibrates phase order to metric clock time | T011 | later physical bridge | `DEFERRED` | Ch. 11–12 |
| T070 | Independently derived temporal and spatial branches admit spacetime closure | T050 | final closure | `DEFERRED` | Ch. 12 |

## Admission rule

A row may move from `CANDIDATE` to a stronger status only through a recorded validation artifact and receipt.
