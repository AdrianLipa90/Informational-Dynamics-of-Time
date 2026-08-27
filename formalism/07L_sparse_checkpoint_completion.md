# 07L — Rank-Minimal Sparse Position Completion

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / RANK_MINIMAL_POSITION_COMPLETION_TARGETED_PASS / LOCAL_CHECKPOINT_SUFFICIENCY_CONDITIONAL_PASS / GLOBAL_INJECTIVITY_OPEN`

This gate composes the 07J checkpoint-scaling bound with the 07K exact ordered-position lineage. Its purpose is to close the **local rank budget** of the declared sparse schedule using the minimum number of additional scalar position channels.

## 1. Inputs from 07J and 07K

For \(N\) planar event kicks,

\[
z=(u_1,\ldots,u_N)\in\mathbb R^{2N},
\qquad d_{\rm latent}=2N.
\]

The declared 07J schedule has sensitivity matrix \(J_S\) and satisfies

\[
\operatorname{rank}J_S\le N+3.
\]

When the reference family saturates that bound,

\[
\operatorname{rank}J_S=N+3,
\]

so the remaining first-order rank deficit is

\[
\boxed{2N-(N+3)=N-3.}
\]

The 07K ordered post-segment position bank supplies two scalar rows per event. Write its Jacobian as

\[
P=\frac{\partial(r_1,\ldots,r_N)}{\partial(u_1,\ldots,u_N)}
\in\mathbb R^{2N\times2N}.
\]

## 2. Exact full-rank certificate for the position bank

Conditional on the retained active-attractor sequence, one segment obeys

\[
r_{k+1}
=r_k+(v_k+u_k)\Delta\tau_k+\frac12 a_k\Delta\tau_k^2.
\]

Future kicks cannot affect earlier checkpoints. The derivative of the \(k\)-th post-segment position with respect to its own kick is exactly

\[
\boxed{
\frac{\partial r_{k+1}}{\partial u_k}
=\Delta\tau_k I_2.
}
\]

Therefore \(P\) is block lower triangular with diagonal blocks \(\Delta\tau_k I_2\). For finite positive segment durations,

\[
\det P
=\prod_{k=1}^{N}(\Delta\tau_k)^2>0,
\]

and hence

\[
\boxed{\operatorname{rank}P=2N.}
\]

The implementation stores the numerically safe certificate

\[
\log|\det P|=2\sum_{k=1}^{N}\log\Delta\tau_k.
\]

## 3. Minimal-completion theorem

Let

\[
r=\operatorname{rank}J_S.
\]

Because the rows of \(P\) span the complete \(2N\)-dimensional latent row space, rows from \(P\) can be appended until the stacked matrix reaches rank \(2N\). A single scalar row can increase rank by at most one. Consequently every completion requires at least

\[
2N-r
\]

additional scalar rows, while a rank-increment construction selects exactly that many.

Thus

\[
\boxed{
N_{\rm add}^{\min}=2N-\operatorname{rank}J_S.
}
\]

For the saturated 07J schedule,

\[
\boxed{
N_{\rm add}^{\min}=N-3.
}
\]

This matches the lower bound from 07J exactly.

## 4. Deterministic selector

The reference selector traverses the scalar position rows in declared order. A row is retained only when

\[
\operatorname{rank}
\begin{bmatrix}
J_{\rm current}\\ p_i
\end{bmatrix}
=
\operatorname{rank}J_{\rm current}+1.
\]

Selection terminates at rank \(2N\). The implementation fails closed when the position pool lacks full latent rank, the matrices are non-finite or dimensionally inconsistent, or the selected-row count differs from the measured rank deficit.

## 5. Targeted fixed-regime reference

The local reference suite passed `6/6` tests. It covers the exact block-triangular rank certificate, deterministic minimal completion, forty seeded fixed-regime cases, the already-full-rank case, rank-deficient position-pool rejection and input validation.

An extended deterministic probe evaluated ten accepted cases for each \(N=4,5,6,7,8,9,10\), for `70/70` accepted cases. Every case had

\[
\operatorname{rank}J_S=N+3,
\qquad
\operatorname{rank}[J_S;P_{\rm selected}]=2N,
\qquad
|P_{\rm selected}|=N-3.
\]

For this declared three-attractor fixed-regime family, the ordered greedy selector chose

\[
\boxed{r_{1x},r_{2x},\ldots,r_{(N-3)x}}
\]

in all `70/70` cases.

## 6. Conditioning audit

Rank sufficiency and numerical conditioning are recorded separately. Across the extended probe the smallest completed-Jacobian singular value remained positive, with the minimum approximately

\[
6.03\times10^{-6},
\]

while the largest observed condition number was approximately

\[
5.01\times10^5.
\]

The reference therefore retains singular-spectrum/conditioning diagnostics alongside the rank verdict. Conditioning quality remains an explicit numerical audit dimension for later estimator design.

## 7. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The explicit relation

`LATENT_DIMENSION -> RANK_DEFICIT -> REQUIRED_SCALAR_CHANNELS`

was compared with

`FULL_POSITION_SPAN -> MISSING_RANK -> SELECTED_POSITION_ROWS`

and returned `structurally_isomorphic=true`.

Three targeted hypotheses and the relational bridge were all `SUPPORTED_BY_DECLARED_TESTS`. GREMLIN supplies candidate/audit evidence only; admission remains controlled by repository tests and dependency gates.

## 8. Evidence boundary

This result establishes a conditional local checkpoint-sufficiency construction for the declared fixed-regime architecture. Parent Memory/ORCHORBITAL admission remains upstream. Sparse-schedule global injectivity and general global injectivity remain separate downstream gates before Retrodiction admission can advance.
