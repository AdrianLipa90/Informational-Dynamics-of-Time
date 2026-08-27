# 07K — Arbitrary-N Exact Position-Lineage Retrodiction

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / POSITION_LINEAGE_EXACT_RETRODICTION_TARGETED_PASS`

This layer follows the 07J checkpoint-scaling gate. 07J establishes a rank budget for its declared sparse schedule. 07K studies a different, richer observation schedule: the ordered two-component post-segment Memory position after every event, together with the persisted active-attractor sequence and the already declared internal elapsed increments.

For `N` events, let

\[
X_0=(r_0,v_0),\qquad r_n\in\mathbb R^2,\qquad \Delta\tau_n>0,
\]

and let the active attractor used by segment `n` be

\[
\mathfrak A_n=(c_n,\mu_n).
\]

Define the active-centre acceleration at position `r` by

\[
\boxed{
A_n(r)=-\mu_n\frac{r-c_n}{\|r-c_n\|^3}.
}
\]

## 1. Exact kick recovery from the position update

The repository velocity-Verlet Memory/ORCHORBITAL segment begins with the event kick `u_n` and obeys

\[
r_n=r_{n-1}+(v_{n-1}+u_n)\Delta\tau_n
+\frac12 A_n(r_{n-1})\Delta\tau_n^2.
\]

Therefore the latent kick is recovered algebraically:

\[
\boxed{
u_n=
\frac{r_n-r_{n-1}-\frac12A_n(r_{n-1})\Delta\tau_n^2}
{\Delta\tau_n}
-v_{n-1}.
}
\]

The post-segment velocity is then

\[
\boxed{
v_n=v_{n-1}+u_n+
\frac12\left[A_n(r_{n-1})+A_n(r_n)\right]\Delta\tau_n.
}
\]

These two equations give a deterministic recursion from `n=1` through `N`.

## 2. Observation dimension

Each retained position contributes two real scalars. The ordered position lineage therefore has

\[
\boxed{\dim Y_{\rm pos}=2N.}
\]

The `N` two-component latent kicks also contain

\[
\boxed{\dim z=2N.}
\]

Thus this observation schedule exactly saturates the latent coordinate count. This complements 07J: its sparse schedule has the bound `rank <= N+3`, while 07K uses a different schedule carrying `2N` ordered position scalars.

## 3. Replay gate

The algebraic candidate is admitted only after replay through the existing Memory→ORCHORBITAL forward cells. The implementation fails closed if:

- a declared attractor name is absent;
- an elapsed increment is non-positive or non-finite;
- the position-lineage length differs from the event count;
- an active-centre singularity is encountered;
- replay enters `LEAK_MODE` or changes the persisted active-attractor sequence;
- replayed checkpoint positions exceed the declared tolerance.

A passing reconstruction receives `EXACT_POSITION_LINEAGE_RECOVERY`.

## 4. Reference probe

The deterministic probe generated 10,000 trajectories with event counts `N=1,...,6`. Thirteen forward-generated inputs entered the existing `LEAK_MODE` boundary and were excluded by that already declared gate. All 9,987 admitted trajectories were reconstructed.

Recorded maxima:

\[
\boxed{
\max\|u_{\rm recovered}-u_{\rm true}\|
=3.1342321523056973\times10^{-13}
}
\]

and

\[
\boxed{
\max\|v_{\rm reconstructed}-v_{\rm forward}\|
=9.849670420387302\times10^{-13}.
}
\]

GREMLIN remained `CANDIDATE_ONLY`; three declared hypotheses returned `SUPPORTED_BY_DECLARED_TESTS`, each with `2/2` tests.

## 5. Relation to the sparse frontier

07J and 07K now bracket the checkpoint-design problem:

\[
\boxed{
\text{sparse schedule of 07J}
\quad\longrightarrow\quad
\text{hybrid sparse design}
\quad\longrightarrow\quad
\text{exact }2N\text{-scalar position lineage of 07K}.
}
\]

The active frontier is to determine which position components can be replaced by already available ORCHORBITAL scalars — especially orientation/angular-momentum or basin observables — while preserving full local rank and then passing a separate global-null/injectivity gate.

Reference implementation: `src/idt/retrodiction_position_lineage_exact.py`.
Reference tests: `tests/reference/test_retrodiction_position_lineage_exact.py`.
Native declaration: `operators/retrodiction_position_lineage_exact_v01.pnv`.
Validation receipt: `validation/RETRODICTION_POSITION_LINEAGE_EXACT_V0_1.json`.
