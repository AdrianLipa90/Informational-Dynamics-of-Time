# Provisional ORCHORBITAL Claim Registry

Status: `MEMORY_EXTENSION_STAGING_ONLY`

These IDs are reserved for the ORCHORBITAL temporal-memory extension while the parent Memory node remains pending its full repository reference-suite admission. Promotion into `CLAIM_REGISTRY.md` requires an explicit admission receipt and keeps the IDs below unchanged.

| ID | Statement | Depends on | Evidence class | Status | Monograph |
|---|---|---|---|---|---|
| T019O | For attractor \(\mathfrak A_i=(c_i,\mu_i)\), \(E_i=\tfrac12\|v_M\|^2-\mu_i/\|m-c_i\|\) and \(b_i=[-E_i]_+\) define the reference binding margin | T016–T019N | Kepler-energy identity + targeted reference tests | `PROVISIONAL_ORCHORBITAL_BINDING_CONTRACT` | Ch. 8F |
| T019P | For positive total binding \(B=\sum_i b_i\), \(w_i=b_i/B\) forms a normalized attractor distribution and the active reference basin is \(\arg\max_iw_i\); \(B=0\) gives `LEAK_MODE` | T019O | algebraic normalization + targeted positive/leak controls | `PROVISIONAL_ORCHORBITAL_ATTRACTOR_SELECTION_CONTRACT` | Ch. 8F |
| T019Q | ORCHORBITAL attractor weights carry Shannon entropy \(H_A=-\sum_iw_i\log_2w_i\) and normalized coherence \(C_A=1-H_A/\log_2N\) for \(N>1\) | T002 + T019P | Shannon identity + symmetric-basin control | `PROVISIONAL_ORCHORBITAL_SHANNON_BASIN_CONTRACT` | Ch. 8F |
| T019R | On one smooth segment with active attractor \(a\), memory evolves by \(\ddot m=-\mu_a(m-c_a)/\|m-c_a\|^3\) | T016 + T019P | translated Kepler reference implementation + covariance test | `PROVISIONAL_ORCHORBITAL_ACTIVE_CENTRE_DYNAMICS` | Ch. 8F |
| T019S | Active-attractor winding increments obey \(\Delta W_a=\operatorname{wrap}(\Delta\theta_a)/(2\pi)\), and post-segment field re-evaluation records a basin-switch candidate | T019R | branch-safe angle identity + targeted switch test | `PROVISIONAL_ORCHORBITAL_WINDING_SWITCH_CONTRACT` | Ch. 8F |
| T019T | With explicit positive scales \(r_*\) and \(v_*\), \(D_{\rm cl}=\sqrt{(\|m_f-m_i\|/r_*)^2+(\|v_f-v_i\|/v_*)^2}\) defines the reference phase-space closure defect | T019R–T019S | formal observable + zero-defect control | `PROVISIONAL_ORCHORBITAL_CLOSURE_DEFECT_CONTRACT` | Ch. 8F |
| T019U | For attractor \(i\), residence time \(T_i^{\rm res}=\sum_{n:a_n=i}\Delta\tau_n\) and total winding \(W_i^{\rm tot}=\sum_{n:a_n=i}\Delta W_{i,n}\) summarize its temporal occupancy | T014–T015 + T019S | ordered accumulation + targeted residence test | `PROVISIONAL_ORCHORBITAL_RESIDENCE_CONTRACT` | Ch. 8F |
| T019V | Adjacent segment labels define directed transition counts \(N_{i\to j}=\#\{n:a_n=i,a_{n+1}=j,i\neq j\}\), yielding the reference attractor-transition graph | T019S–T019U | ordered-label graph construction + targeted A-to-B test | `PROVISIONAL_ORCHORBITAL_TRANSITION_GRAPH_CONTRACT` | Ch. 8F |

## Admission rule

These rows remain provisional Memory-extension claims until the parent Memory gate and the ORCHORBITAL extension gate are explicitly admitted. The targeted receipt `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json` records the current reference evidence without independently advancing the canonical frontier.
