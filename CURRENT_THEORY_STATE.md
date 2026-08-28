# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE / EVENT_AWARE_RESIDENCE_CONDITIONING_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

The proposed admitted frontier after merge of the current promotion branch is

\[
\boxed{\text{Temporal Primitive}\rightarrow\text{Temporal Wave}\rightarrow\text{NOW}\rightarrow\text{Bifurcation}\rightarrow\text{Temporal Transport}\rightarrow\text{Memory}\rightarrow\mathbf{ORCHORBITAL\ Attractors}}
\]

The active downstream dependency path is

\[
\boxed{\mathrm{Memory}\rightarrow\mathrm{ORCHORBITAL\ Attractors}\rightarrow\mathbf{Retrodiction}}.
\]

## Temporal-memory substrate

The Memory reference branch uses internal elapsed activity and event-driven Kepler dynamics,

\[
\Delta\tau_{\rm int}=\frac{\mathfrak a}{\mathfrak a_\star}\Delta\lambda,
\qquad
\ddot m=-\mu_M\frac{m}{|m|^3},
\qquad
\Delta v_{M,n}=q_n\delta m_n.
\]

For the pure-state \(\mathbb{CP}^1\) reference subclass,

\[
|\delta m|=d_{FS}.
\]

Memory persistence uses append-only event receipts and reversible Kepler/event cells. The repository-wide Memory gate is bound by `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

## ORCHORBITAL attractor organization

For attractor

\[
\mathfrak A_i=(c_i,\mu_i),
\qquad \mu_i>0,
\]

define

\[
E_i=\frac12\|v_M\|^2-\frac{\mu_i}{\|m-c_i\|},
\qquad
b_i=[-E_i]_+.
\]

For \(B=\sum_i b_i>0\),

\[
w_i=\frac{b_i}{B},
\qquad
a=\arg\max_iw_i,
\]

with Shannon organization

\[
H_A=-\sum_{i:w_i>0}w_i\log_2w_i,
\qquad
C_A=1-\frac{H_A}{\log_2N}\quad(N>1).
\]

Each admitted smooth segment follows the active-centre translated Kepler law

\[
\frac{d^2m}{d\tau_{\rm int}^2}
=-\mu_a\frac{m-c_a}{\|m-c_a\|^3},
\]

with winding increment

\[
\Delta W_a=\frac{1}{2\pi}\operatorname{wrap}(\theta_{n+1}-\theta_n).
\]

The residence layer persists exact segment lineage. For each attractor \(i\), maximal contiguous residence episodes carry

\[
T_{i,r}=\sum_{k\in I_{i,r}}\Delta\tau_k,
\qquad
W_{i,r}=\sum_{k\in I_{i,r}}\Delta W_k,
\]

with global elapsed-time accounting

\[
\sum_i\sum_rT_{i,r}=\sum_k\Delta\tau_k.
\]

The pinned PNCS hierarchy binds sphere/entity structure onto nested temporal-memory attractor families. The observable layer retains three separately typed coordinates,

\[
\mathcal O_{\rm ORCH}
=\bigl(T,\mathcal R_\Omega,\{m_{\rm sem}(a_i)\}\bigr),
\]

with

\[
T\in[0,1],
\qquad
\mathcal R_\Omega:\;\mathrm{reduce\_ready}\iff\Omega\ge\Omega_{\rm crit},
\qquad
m_{\rm sem}(a_i)\ge0.
\]

For a verified residence lineage,

\[
\boxed{
\bar m_{\rm sem}^{(\tau)}
=\frac{\sum_k\Delta\tau_k\,m_{\rm sem}(a_k)}{\sum_k\Delta\tau_k}.
}
\]

The combined ORCHORBITAL admission binding is `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

## Event-aware residence-conditioned Retrodiction

A Memory lineage places an event kick before each smooth ORCHORBITAL segment,

\[
X_k^-
\xrightarrow{\mathcal E_k}
X_k^K
\xrightarrow{\Phi_{a_k}(\Delta\tau_k)}
X_k^+.
\]

The event-aware bridge therefore carries the cell

\[
\mathcal B_k=
\left(
 k,\tau_k^-,\mathcal E_k,H(X_k^-),\mathcal R_k^{\rm smooth},h_{k-1}
\right),
\]

with chronological continuity

\[
H(X_{k-1}^+)=H(X_k^-)
\]

and event-to-smooth binding

\[
H(K_{\mathcal E_k}X_k^-)=H(X_{k,\rm smooth}^-).
\]

The exact finite-precision elapsed-time relation is

\[
\boxed{
\Delta\tau_k^R
=\operatorname{fl}\!\left(
\operatorname{fl}(\tau_k^-+\Delta\tau_k^E)-\tau_k^-
\right).
}
\]

For the declared two-event global reflection pair, the final retained base observation remains equivalent at tolerance \(10^{-10}\), while the latent separation exceeds \(0.9\). The retained discrete residence coordinates satisfy

\[
(a_k)_k=(\widetilde a_k)_k
\]

and the next-attractor, switch and leak lineages also coincide. The pair therefore remains in the same discrete residence-label equivalence class.

The earlier continuous ORCHORBITAL coordinate separates the pair,

\[
\boxed{
|w_{A,1}(z)-w_{A,1}(\widetilde z)|
=0.01918916841099516.
}
\]

The current Retrodiction information channels are therefore kept distinctly typed as

\[
\boxed{
\text{discrete residence lineage}
\;\mid\;
\text{continuous ORCH observables}
\;\mid\;
\text{provenance commitments}.
}
\]

The formal and evidence bindings are `formalism/07O_orchorbital_residence_conditioned_retrodiction.md` and `validation/RETRODICTION_ORCHORBITAL_RESIDENCE_CONDITIONING_V0_1.json`. The hardened hosted suite returned `486 passed in 8.89s` in run `33198069462`, job `98940226102`.

The active Retrodiction frontier is global branch separation using retained continuous ORCHORBITAL and spatial-offset/divergence channels. `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status.

## 01K temporal information curvature interface

The separate Einstein-interface branch starts from the exact 01C Shannon-relative-information scalar and internal elapsed-time/clock structure,

\[
\mathcal J_\pi=(\ln2)\mathcal I_\pi,
\qquad
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}},
\qquad
[\Xi_I]=L^{-2},
\]

with exact quotient-rule evolution

\[
\frac{d\Xi_I}{d\tau_{\rm int}}
=\frac{1}{\mathcal A_{\rm rel}}\frac{d\mathcal J_\pi}{d\tau_{\rm int}}
-\frac{\Xi_I}{\mathcal A_{\rm rel}}\frac{d\mathcal A_{\rm rel}}{d\tau_{\rm int}}.
\]

This interface remains a parallel downstream curvature-typed export while Retrodiction is the active sequential temporal gate.

Canonical `main` remains unchanged until explicit merge authorization.
