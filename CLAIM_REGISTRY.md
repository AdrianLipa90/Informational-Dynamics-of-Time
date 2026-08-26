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
| T010 | Temporal state admits ordered phase transport \(\Psi_{n+1}=U_n\Psi_n\) | T001 | formal candidate | `CANDIDATE` | Ch. 3–4 |
| T011 | For unitary phase-only transport, \(U_n=e^{-i\Omega_n}\) | T010 | algebraic derivation | `CANDIDATE` | Ch. 4 |
| T020 | Transition measure \(\mathcal K_T=\sum_n q_n\delta_{s_n}\) localizes discrete transition events | T010 | source-grounded structural candidate | `CANDIDATE` | Ch. 5 |
| T021 | \(\mathcal N=\operatorname{supp}_{\rm at}\mathcal K_T\) | T020 | GREMLIN + formal candidate | `CANDIDATE` | Ch. 5 |
| T022 | \(\Psi_T(s_n^+)=B(q_n)\Psi_T(s_n^-)\) | T021 | formal candidate | `CANDIDATE` | Ch. 6 |
| T023 | NOW-support is invariant under admissible monotone reparameterization | T021 | proof target | `OPEN_PROOF_TARGET` | Ch. 5 |
| T050 | \(\Delta\phi_t=-E\Delta t/\hbar\) calibrates phase order to metric clock time | T011 | later physical bridge | `DEFERRED` | Ch. 11–12 |
| T070 | Independently derived temporal and spatial branches admit spacetime closure | T050 | final closure | `DEFERRED` | Ch. 12 |

## Admission rule

A row may move from `CANDIDATE` to a stronger status only through a recorded validation artifact and receipt.
