# 07I — Two-Event Finite-Branch Global Retrodiction Gate

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / TWO_EVENT_FIXED_REGIME_GLOBAL_INJECTIVITY_CONDITIONAL_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`

This layer closes the explicit reflection ambiguity from 07G/07H for a declared two-event subclass by replacing multistart search with exhaustive finite branch reconstruction.

## 1. Scope

The gate assumes:

- known initial Memory state \(X_0=(r_0,v_0)\);
- two positive elapsed increments \(\Delta\tau_1,\Delta\tau_2\);
- persisted active-attractor snapshots for both smooth ORCHORBITAL cells;
- a fixed final basin-support regime with at least two positive weights;
- retained final \((r_{x,2},r_{y,2},v_{x,2})\) and final basin weights \(w_{i,2}\);
- one earlier basin weight \(w_{j,1}\).

General multi-event/global injectivity remains a separate Retrodiction gate.

## 2. Basin weights invert the final kinetic scalar

At fixed final position define

\[
u_i=\frac{\mu_i}{\|r_2-c_i\|},
\qquad
T_2=\frac12\|v_2\|^2.
\]

On a fixed positive support \(S\),

\[
b_i=u_i-T_2,
\qquad
w_i=\frac{u_i-T_2}{U_S-mT_2},
\qquad
U_S=\sum_{i\in S}u_i,
\quad m=|S|.
\]

For any supported pivot \(j\) with \(1-mw_j\neq0\),

\[
\boxed{
T_2=\frac{u_j-w_jU_S}{1-mw_j}.
}
\]

The implementation reconstructs all weights from the inferred \(T_2\) and requires the same support. Uniform supported weights are routed to `WEIGHT_KINETIC_CHANNEL_DEGENERATE`.

## 3. Finite hidden-velocity preimage

With retained \(v_{x,2}\),

\[
\boxed{
v_{y,2}=\pm\sqrt{2T_2-v_{x,2}^2}.
}
\]

Thus the regular final-state preimage contains at most two sign branches; at \(v_{y,2}=0\) it contains one.

Each branch is a complete final Memory state and can therefore be propagated backward through the persisted second active-centre Verlet cell.

## 4. Exact latent reconstruction per branch

Let inversion of the second cell return the kicked pre-segment state

\[
X_{1}^{+}=(r_1,v_1+u_2).
\]

For the first active attractor, the position part of the repository velocity-Verlet step is

\[
r_1=r_0+(v_0+u_1)\Delta\tau_1+\frac12a_0\Delta\tau_1^2.
\]

Hence the first latent kick is fixed by the recovered intermediate position:

\[
\boxed{
u_1=
\frac{r_1-r_0-\tfrac12a_0\Delta\tau_1^2}{\Delta\tau_1}-v_0.
}
\]

Forward replay of the first smooth cell then gives \(v_1\), and the second kick follows exactly from

\[
\boxed{
u_2=(v_1+u_2)-v_1.}
\]

Every final sign branch therefore maps to at most one latent two-kick history inside the persisted active-cell regime.

## 5. Earlier basin-weight selector

For every regular reconstructed branch, evaluate the declared earlier basin weight \(w_{j,1}\). Given equivalence tolerance \(arepsilon\):

- exactly one matching branch gives `UNIQUE_FIXED_REGIME_TWO_EVENT`;
- zero matching branches gives `INCONSISTENT_OBSERVATION`;
- more than one matching branch gives `GLOBAL_BRANCH_AMBIGUITY`.

This is an exhaustive branch gate for the declared subclass rather than a multistart-search verdict.

For the explicit 07H reflection pair the two branches recover

\[
w_{A,1}=0.5838364569736164
\]

and

\[
w_{A,1}=0.6030256253846111,
\]

with separation

\[
\boxed{|\Delta w_{A,1}|=0.01918916841099505.}
\]

The generating branch is therefore unique under the declared earlier-weight checkpoint.

## 6. Numerical gate

A deterministic 10,000-case probe in the same three-attractor reference family returned:

- admitted cases: `10000/10000`;
- unique branch after the earlier-weight selector: `10000/10000`;
- ambiguous cases: `0`;
- inconsistent cases: `0`;
- maximum latent reconstruction error: `2.2167990444174233e-11`;
- maximum kinetic-energy reconstruction error: `2.040034807748725e-15`;
- maximum basin-weight reconstruction error: `2.220446049250313e-16`;
- minimum two-branch earlier-weight separation: `2.6963444221816957e-07`;
- median two-branch earlier-weight separation: `0.02426143694524341`.

The targeted repository harness additionally passes the explicit 07H reflection pair, kinetic inversion, 500 nearby random recoveries, inconsistent-observation negative control and uniform-weight degeneracy control.

## 7. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The finite-preimage structure matched the generic inverse-problem chain

`PARTIAL_OBSERVATION -> FINITE_PREIMAGE_ENUMERATOR -> REGIME_FILTER -> AUXILIARY_CHECKPOINT_SELECTOR -> UNIQUE_CANDIDATE`

with `structurally_isomorphic=true`, comparison SHA-256
`4d658962abdeca2a4e8ae7d31730428cf6156def23dbbd2dff06d38237b690c0`.

Three declared hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `3/3`, and `2/2`.

GREMLIN artifact:

`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_FINITE_BRANCH_GLOBAL_GATE_20260827.json`

SHA-256:

`c50c25a37ab4f01f0c8286ce044c833206cba5d254f67c9a6cc2cacf937432bd`.

Reference implementation: `src/idt/retrodiction_finite_branch.py`.

Reference tests: `tests/reference/test_retrodiction_finite_branch.py`.
