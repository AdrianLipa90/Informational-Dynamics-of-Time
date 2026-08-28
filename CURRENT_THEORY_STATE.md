# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE`.

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

The residence layer persists exact segment lineage as a content-addressed chain. For each attractor \(i\), maximal contiguous residence episodes carry dwell

\[
T_{i,r}=\sum_{k\in I_{i,r}}\Delta\tau_k
\]

and winding

\[
W_{i,r}=\sum_{k\in I_{i,r}}\Delta W_k,
\]

with global elapsed-time accounting

\[
\sum_i\sum_rT_{i,r}=\sum_k\Delta\tau_k.
\]

The pinned PNCS v0.29 hierarchy binds sphere/entity structure onto nested temporal-memory attractor families. The pinned PNCS v0.27 observable layer retains three separately typed coordinates:

\[
\mathcal O_{\rm ORCH}=
\bigl(T,\mathcal R_\Omega,\{m_{\rm sem}(a_i)\}\bigr),
\]

where

\[
T\in[0,1],
\qquad
\mathcal R_\Omega:\;\mathrm{reduce\_ready}\iff\Omega\ge\Omega_{\rm crit},
\qquad
m_{\rm sem}(a_i)\ge0.
\]

For a verified residence lineage, the temporal semantic-mass aggregate is

\[
\boxed{
\bar m_{\rm sem}^{(\tau)}
=\frac{\sum_k\Delta\tau_k\,m_{\rm sem}(a_k)}{\sum_k\Delta\tau_k}.
}
\]

The typed-observable completion suite returned `475 passed in 11.91s` in GitHub Actions run `33196818703`, job `98935954122`. The combined ORCHORBITAL admission binding is `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

## Retrodiction active next gate

The Retrodiction stack already contains withheld-lineage inversion, local observability/rank gates, checkpoint selection, damped Gauss--Newton estimation, covariance/Fisher uncertainty geometry and covariance-preserving permutation nulls.

Its next dependency-compatible extension is

\[
\boxed{
\text{verified ORCHORBITAL residence/switch lineage}
\rightarrow
\text{Retrodiction conditioning}
\rightarrow
\text{identifiability comparison with retained basin labels}.
}
\]

This comparison remains inside the declared lineage firewall: estimator inputs and retained labels are committed before truth scoring.

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
