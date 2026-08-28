# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE / EVENT_AWARE_RESIDENCE_CONDITIONING_PASS / QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS / ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

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

with signed winding increment

\[
\boxed{
\Delta W_a=\frac{1}{2\pi}\operatorname{wrap}(\theta_{n+1}-\theta_n).
}
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

The Retrodiction information channels remain distinctly typed as

\[
\boxed{
\text{discrete residence lineage}
\;\mid\;
\text{continuous ORCH observables}
\;\mid\;
\text{spatial/SOD coordinates}
\;\mid\;
\text{oriented winding/holonomy}
\;\mid\;
\text{provenance commitments}.
}
\]

The formal and evidence bindings are `formalism/07O_orchorbital_residence_conditioned_retrodiction.md` and `validation/RETRODICTION_ORCHORBITAL_RESIDENCE_CONDITIONING_V0_1.json`.

## Quotient/fiber finite-domain Retrodiction

Let

\[
\mathcal C=\{z_1,\ldots,z_n\}
\]

be a finite candidate-history domain, let \(Y\) be the retained base observation, and let \(F_c\) denote separately typed retained fiber channels. Define

\[
\widetilde Y(z)=\bigl(Y(z),F_1(z),\ldots,F_m(z)\bigr).
\]

On the finite domain the exact separation condition is

\[
\boxed{
\widetilde Y\text{ injective on }\mathcal C
\iff
\forall i\ne j:\
Y(z_i)=Y(z_j)
\Longrightarrow
\exists c:\ F_c(z_i)\ne F_c(z_j).
}
\]

The 07P binding is `formalism/07P_quotient_fiber_finite_injectivity.md` with receipt `validation/RETRODICTION_QUOTIENT_FIBER_FINITE_INJECTIVITY_V0_1.json`. Hosted run `33200684482`, job `98949092398`, returned `495 passed in 10.14s`.

## Oriented winding as a fiber coordinate

07Q uses the already persisted signed residence winding as a concrete fiber candidate. For an \(N\)-event history,

\[
\boxed{
\mathcal W(z)
=\bigl(\Delta W_1(z),\ldots,\Delta W_N(z)\bigr).
}
\]

The canonical storage is the exact binary64 `winding_increment_hex` carried by each residence receipt. Segment order is retained. Define

\[
\delta_W
=\|\mathcal W(\widetilde z)-\mathcal W(z)\|_2.
\]

For the exact 07G/07H reflection pair, the base projection remains equivalent and the active-attractor sequence remains equal, while hosted reference tests establish

\[
\boxed{
\delta_W>10^{-12}.
}
\]

Hence this pair receives

```text
BASE_NULL_SEPARATED_BY_ORIENTED_WINDING
```

without using provenance commitments as semantic coordinates.

Feeding \(\mathcal W\) directly into the 07P finite-domain gate gives, for the declared two-history candidate domain,

\[
\boxed{
N_{\rm collision}=1,
\quad
N_{\rm separated}=1,
\quad
N_{\rm unresolved}=0,
}
\]

and status

```text
FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER
```

with the separating channel attributed to `oriented_winding`.

This matches the repository's broader orientation-preservation pattern: the 01L temporal-holonomy carrier retains cycle orientation through the signed phase quadrature, while 07Q retains the signed segment-circulation lineage inside a Retrodiction collision fiber. GREMLIN treats that cross-layer relation as a structural candidate; repository evidence is governed by the explicit 07Q/07P tests.

The 07Q binding is `formalism/07Q_oriented_winding_fiber_separator.md` with receipt `validation/RETRODICTION_ORIENTED_WINDING_FIBER_V0_1.json`. Hosted run `33201861565`, job `98953023513`, tested branch head `1c124b7cb37a00ea9ce3e5e96cb3e66c5d7e0363` and returned

```text
502 passed in 8.09s
```

on Python 3.12.14 / Ubuntu 24.04.4.

The active Retrodiction frontier is now the characterization of complete base-collision fibers and a domain-covering separator theorem or constructive lift using ordered winding together with retained continuous ORCHORBITAL and SOD coordinates. `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status.

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
