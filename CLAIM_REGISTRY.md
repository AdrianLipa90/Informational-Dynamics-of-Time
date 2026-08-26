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
| T014 | System-internal elapsed activity obeys \(d\tau_{\rm int}=(\mathfrak a/\mathfrak a_\star)d\lambda\) and is strictly monotone for positive admitted activity and increasing order parameter | T012 | formal candidate + theorem + reference tests | `FORMAL_CANDIDATE_WITH_PROVED_MONOTONICITY` | Ch. 7–8 |
| T015 | Under increasing reparameterization, activity transforms as a one-density so \(d\tau_{\rm int}\) is invariant | T014 | algebraic theorem + reference tests | `PROVED_STRUCTURAL_IDENTITY` | Ch. 7–8 |
| T016 | The provisional memory coordinate evolves in internal elapsed activity by \(d^2m/d\tau_{\rm int}^2=-\mu_M m/|m|^3\), \(\mu_M>0\) | T014–T015 + T009B | reference implementation + targeted tests | `PROVISIONAL_DOWNSTREAM_CANDIDATE_WITH_REFERENCE_IMPLEMENTATION` | Ch. 8 |
| T017 | For a smooth T016 segment, \(h_M=\operatorname{Im}[m^*dm/d\tau_{\rm int}]\) is conserved and \(d\mathcal A_M/d\tau_{\rm int}=h_M/2\) | T016 | central-force theorem + targeted tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 8 |
| T018 | T016 admits the Kepler conic law \(r_M=p_M/(1+e_M\cos\nu)\), \(p_M=h_M^2/\mu_M\), and on bound branches \(T_M^2=4\pi^2a_M^3/\mu_M\) | T016–T017 | classical central-force derivation + targeted tests | `PROVED_CONDITIONAL_IDENTITY` | Ch. 8 |
| T019 | A localized memory update exposes the typed impulse interface \(\mathbf v_M^+=\mathbf v_M^-+\Delta\mathbf v_M\); the event-imprint projection supplies a separate derivation target | T016 + bifurcation interface | formal interface + targeted tests | `PROVISIONAL_DOWNSTREAM_INTERFACE` | Ch. 8 |
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

A row may move from `CANDIDATE` or `PROVISIONAL_DOWNSTREAM_*` to a stronger status only through a recorded validation artifact and receipt consistent with the dependency graph.
