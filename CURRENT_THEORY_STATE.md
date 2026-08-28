# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE / EVENT_AWARE_RESIDENCE_CONDITIONING_PASS / QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS / ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS / FIBER_LIFT_COMPOSITION_THEOREM_PASS / FINITE_DOMAIN_FIBER_LIFT_REFERENCE_PASS / POSITION_LINEAGE_LIFT_ACTIVE_NEXT_GATE / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

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

The event-aware bridge carries chronological event-to-smooth lineage and exact finite-precision elapsed-time binding. For the declared two-event reflection pair, the final retained base observation remains equivalent at tolerance \(10^{-10}\), while the latent separation exceeds \(0.9\). The active-attractor, next-attractor, switch and leak lineages also coincide.

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

## Quotient/fiber finite-domain Retrodiction

For a finite candidate-history domain \(\mathcal C\), base observation \(Y\), and separately typed fiber channels \(F_c\), define

\[
\widetilde Y(z)=\bigl(Y(z),F_1(z),\ldots,F_m(z)\bigr).
\]

07P establishes

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

The 07P binding is `formalism/07P_quotient_fiber_finite_injectivity.md` with receipt `validation/RETRODICTION_QUOTIENT_FIBER_FINITE_INJECTIVITY_V0_1.json`.

## Oriented winding as a fiber coordinate

07Q uses the already persisted signed residence winding

\[
\boxed{
\mathcal W(z)
=\bigl(\Delta W_1(z),\ldots,\Delta W_N(z)\bigr)
}
\]

as a concrete fiber candidate. The canonical storage is the exact binary64 `winding_increment_hex` carried by each residence receipt.

For the exact reflection pair, the base projection and active sequence remain equivalent while

\[
\boxed{
\|\mathcal W(\widetilde z)-\mathcal W(z)\|_2>10^{-12}.
}
\]

Feeding \(\mathcal W\) into 07P gives one base collision, one separated collision and zero unresolved collisions with the channel attributed to `oriented_winding`.

The 07Q binding is `formalism/07Q_oriented_winding_fiber_separator.md` with receipt `validation/RETRODICTION_ORIENTED_WINDING_FIBER_V0_1.json`.

## Fiber-lift composition theorem

07R introduces an injective reference carrier

\[
P:\mathcal Z\to\mathcal X
\]

and the augmented retained observation

\[
\boxed{A(z)=(Y(z),F(z)).}
\]

Assume a single-valued lift exists on the image of \(A\),

\[
L:A(\mathcal Z)\to\mathcal X,
\qquad
\boxed{P=L\circ A.}
\]

If \(P\) is injective, then \(A\) is injective. Indeed,

\[
A(z_1)=A(z_2)
\Longrightarrow
L(A(z_1))=L(A(z_2))
\Longrightarrow
P(z_1)=P(z_2)
\Longrightarrow
\boxed{z_1=z_2}.
\]

This is an exact composition theorem rather than an empirical extrapolation from finite tests.

### 07K carrier binding

The reference carrier is the ordered post-segment position lineage

\[
\boxed{
P(z)=(r_1(z),\ldots,r_N(z)).
}
\]

07K gives exact algebraic recovery of the event kick at each step,

\[
\boxed{
u_n=
\frac{r_n-r_{n-1}-\frac12A_n(r_{n-1})\Delta\tau_n^2}
{\Delta\tau_n}
-v_{n-1},}
\]

followed by

\[
\boxed{
v_n=v_{n-1}+u_n+
\frac12\left[A_n(r_{n-1})+A_n(r_n)\right]\Delta\tau_n.}
\]

Thus the active global closure problem is reduced to constructing

\[
\boxed{
L:(Y,F)\mapsto(r_1,\ldots,r_N)
}
\]

on the admitted Retrodiction domain.

### Finite reference audit

The executable 07R layer independently verifies the two theorem premises on finite candidate domains:

1. distinct latent candidates must remain distinct under the carrier \(P\);
2. an equal augmented observation cannot map to two distinct carrier values.

For the exact reflection pair, with sparse base observation plus `oriented_winding` and the 07K position carrier, the audit returns

```text
FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS
```

with zero carrier collisions, zero augmented collisions and zero lift conflicts. Replacing winding by an identical zero fiber returns

```text
FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN
```

because the colliding augmented record maps to two distinct position carriers.

The 07R binding is `formalism/07R_fiber_lift_composition_theorem.md` with receipt `validation/RETRODICTION_FIBER_LIFT_COMPOSITION_V0_1.json`. Hosted run `33202559485`, job `98955383447`, tested branch head `6abca4ad72c04cdca5d1128e690c17898b8650d7` and returned

```text
510 passed in 14.11s
```

on Python 3.12.14 / Ubuntu 24.04.4.

The active Retrodiction frontier is now `POSITION_LINEAGE_LIFT_ACTIVE_NEXT_GATE`: derive a domain-covering constructive lift from retained base observations and existing fiber channels to the ordered 07K position lineage. `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status until that lift or an equivalent domain-covering fiber-separation argument is receipted.

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
