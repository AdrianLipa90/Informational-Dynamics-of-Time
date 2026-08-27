# 07L — Minimal Hybrid Sparse Checkpoint Rank Closure

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / HYBRID_SPARSE_LOCAL_RANK_CLOSURE_TARGETED_PASS`

This layer combines the 07J sparse checkpoint budget with the 07K exact position-lineage endpoint. The design goal is to add exactly the number of independent scalar channels required by the 07J dimensional deficit while using an already available ORCHORBITAL observable.

For `N` planar event kicks the latent dimension is

\[
\boxed{d_{\rm latent}=2N.}
\]

The 07J sparse schedule has

\[
\boxed{\operatorname{rank}J_{07J}\le N+3,}
\]

so for `N>=4` the minimum missing dimension is

\[
\boxed{\Delta d_{\min}=N-3.}
\]

## 1. Added orientation channel

For post-segment checkpoint `n`, let `a_n` be the persisted active attractor with centre `c_{a_n}`. Define the active-relative planar angular-momentum scalar

\[
\boxed{
h_n=(r_n-c_{a_n})_x v_{y,n}-(r_n-c_{a_n})_y v_{x,n}.
}
\]

This observable is already typed by the Memory/ORCHORBITAL phase state and the persisted active-attractor snapshot. No new gain or normalization constant is introduced.

The 07L hybrid schedule adds

\[
\boxed{m_N=\max(0,N-3)}
\]

such scalars, taken from the first `m_N` earlier checkpoints of the ordered lineage.

## 2. Hybrid schedule

The retained measurement consists of the 07J schedule:

1. final `(r_x,r_y,v_x)`;
2. final ORCHORBITAL basin-weight vector;
3. one declared basin weight at each of the `N-1` earlier checkpoints;

plus the `m_N` active-relative angular-momentum scalars.

For `N>=4`, the number of added channels equals the 07J lower bound exactly:

\[
\boxed{m_N=N-3=2N-(N+3).}
\]

Therefore a full-rank result would be minimal with respect to the number of scalar channels added to this declared schedule.

## 3. Fixed-regime Jacobian gate

Let the hybrid observation be `Y_H(z)` and

\[
J_H=\frac{\partial Y_H}{\partial z}.
\]

Finite differences are admitted only while the active-attractor sequence and bound-support pattern remain unchanged. Any perturbation crossing a switching, support-entry or `LEAK_MODE` boundary fails closed.

The local identifiability gate is

\[
\boxed{\operatorname{rank}J_H=2N.}
\]

## 4. Deterministic reference probe

A deterministic probe used the same three-attractor family as 07F–07K and 100 accepted cases for each `N=2,3,4,5,6`.

| `N` | 07J/base rank | added `h` scalars | hybrid rank | latent dim |
|---:|---:|---:|---:|---:|
| 2 | 4 | 0 | 4 | 4 |
| 3 | 6 | 0 | 6 | 6 |
| 4 | 7 | 1 | 8 | 8 |
| 5 | 8 | 2 | 10 | 10 |
| 6 | 9 | 3 | 12 | 12 |

For `N=4,5,6`, all 100/100 tested cases reached full local rank after adding exactly `N-3` orientation scalars. The minimum retained singular values in the tested samples were approximately

\[
4.13\times10^{-6},\quad 8.07\times10^{-6},\quad 5.15\times10^{-7}
\]

for `N=4,5,6`, respectively.

The targeted implementation suite adds deterministic exact cases for `N=3,4,5,6`, a randomized 30-case gate for each of `N=4,5,6`, and fail-closed input validation. It passes 6/6 locally.

## 5. Scope of the result

The result establishes a minimal scalar-count closure of the 07J local rank deficit for the tested reference regime:

\[
\boxed{
N-3\ \text{additional active-relative }h\text{ channels}
\Longrightarrow
\operatorname{rank}J_H=2N
}
\]

for the tested `N=4,5,6` cases.

Global injectivity remains a separate gate. A locally full-rank hybrid schedule must still be challenged by explicit null search, multistart reconstruction and, where possible, algebraic branch enumeration before a global uniqueness claim can advance.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The structural relation

`LATENT_DEFICIT -> ADDITIONAL_CHANNEL_SET -> FULL_RANK_GATE`

matched the tested hybrid schedule with `structurally_isomorphic=true`.

Three hypotheses returned `SUPPORTED_BY_DECLARED_TESTS`, each with `2/2` declared tests:

1. exactly `N-3` active-relative angular-momentum scalars restore full local rank for the tested `N=4,5,6` schedules;
2. the unaugmented measurement reproduces the 07J ranks `7,8,9` in the same tested cases;
3. the added channel count equals the dimensional lower bound while the hybrid rank reaches `2N`.

Probe artifact:
`/dev/shm/ciel_noema/gremlin/IDT_RETRODICTION_HYBRID_SPARSE_PROBE_20260827.json`

Probe SHA-256:
`03199842d731e0a2ba5c963f1b3e565a99919d20c25e32f1b2de9efe504bf3ba`

GREMLIN artifact:
`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_HYBRID_SPARSE_GATE_20260827.json`

GREMLIN SHA-256:
`482d36498c84d351ede9451d112f090c5ddce6a17d197b072653a16f589e3874`.

Reference implementation: `src/idt/retrodiction_hybrid_sparse_checkpoints.py`.
Reference tests: `tests/reference/test_retrodiction_hybrid_sparse_checkpoints.py`.
Validation receipt: `validation/RETRODICTION_HYBRID_SPARSE_CHECKPOINTS_V0_1.json`.
