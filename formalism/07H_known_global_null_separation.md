# 07H — Known Global-Null Separation by an Earlier ORCHORBITAL Checkpoint

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / KNOWN_NULL_SEPARATION_TARGETED_PASS / GLOBAL_INJECTIVITY_OPEN`

The 07G gate exhibited two distinct latent histories that produce the same final retained partial checkpoint
\[
(r_x,r_y,v_x,w_A,w_B,w_C)_2.
\]
This layer asks whether an earlier persisted ORCHORBITAL scalar can separate that explicit collision while retaining the same downstream dependency discipline.

## 1. Pair-scoped null gate

Let two distinct latent histories be
\[
z,\tilde z\in\mathbb R^{2N},
\qquad
\|z-\tilde z\|_2>0.
\]
For a declared base observation map \(Y_B\), define
\[
\delta_B=\|Y_B(z)-Y_B(\tilde z)\|_2.
\]
For an added checkpoint map \(Y_A\), define the augmented vector
\[
Y_{B+A}=(Y_B,Y_A)
\]
and separation
\[
\delta_{B+A}
=\|Y_{B+A}(z)-Y_{B+A}(\tilde z)\|_2.
\]
Given an explicit equivalence tolerance \(\varepsilon>0\), the statuses are

- `NOT_A_BASE_NULL` when \(\delta_B>\varepsilon\);
- `KNOWN_NULL_PERSISTS` when \(\delta_B\le\varepsilon\) and \(\delta_{B+A}\le\varepsilon\);
- `KNOWN_NULL_SEPARATED` when \(\delta_B\le\varepsilon\) and \(\delta_{B+A}>\varepsilon\).

The gate is deliberately scoped to a declared candidate pair. Global injectivity remains the next Retrodiction gate.

## 2. Explicit reflection-null pair

The 07G reference histories are
\[
\begin{aligned}
u_1&=(0.034,-0.023),\\
u_2&=(-0.008,0.028),
\end{aligned}
\]
and
\[
\begin{aligned}
\tilde u_1&=(0.03399999999998063,0.34071654937113033),\\
\tilde u_2&=(-0.00802729491823317,-0.8206629500579328).
\end{aligned}
\]
Their latent separation is
\[
\boxed{\|\tilde z-z\|_2=0.9233193011263697.}
\]
For the final-only base checkpoint,
\[
Y_B=(r_x,r_y,v_x,w_A,w_B,w_C)_2,
\]
the independently replayed residual is
\[
\boxed{\delta_B=5.594315114139762\times10^{-17}.}
\]

## 3. One earlier basin weight

Add only the earlier weight of attractor \(A\),
\[
Y_A=w_{A,1}.
\]
The two histories give
\[
w_{A,1}(z)=0.5838364569736161,
\]
\[
w_{A,1}(\tilde z)=0.6030256253846112,
\]
so
\[
\boxed{
|\Delta w_{A,1}|
=0.01918916841099516.
}
\]
Therefore the declared reflection pair moves from an exact final-checkpoint collision to

`KNOWN_NULL_SEPARATED`.

The result uses one earlier ORCHORBITAL scalar and does not require exposing the hidden final \(v_y\) component.

## 4. Negative control

An added scalar is useful only when it separates the candidate pair. For the same histories,
\[
r_{x,1}(z)-r_{x,1}(\tilde z)
=1.1102230246251565\times10^{-16},
\]
which remains inside the declared numerical equivalence tolerance. The earlier \(r_x\) scalar therefore receives

`KNOWN_NULL_PERSISTS`.

This control distinguishes checkpoint cardinality from checkpoint information content.

## 5. Bounded multistart diagnostic

A separate numerical diagnostic searched the bounded latent box
\[
[-1.2,1.2]^4
\]
with 500 deterministic random initial seeds.

For the final-only 07G measurement:

- 495 starts reached residual below \(10^{-8}\);
- the recovered solutions formed two clusters;
- cluster counts were 317 and 178;
- the two cluster centres coincide with the reference and reflection-null branches to the declared numerical resolution.

After adding only \(w_{A,1}\):

- 286 starts reached residual below \(10^{-8}\);
- all successful fits formed one cluster around the generating branch.

This is retained as a bounded diagnostic supporting the known-null separation result. The formal admission level remains pair-scoped and the global-injectivity gate stays open.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. It matched the typed structure

`CANDIDATE_PAIR -> TERMINAL_PROJECTION -> COLLISION`

with

`CANDIDATE_PAIR -> AUXILIARY_CHECKPOINT -> SEPARATION`

against the generic inverse-problem architecture with `structurally_isomorphic=true`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `2/2`, and `3/3`:

1. the final-only measurement contains the declared distinct-history collision;
2. the earlier basin weight separates that collision;
3. the bounded multistart diagnostic resolves two recovered clusters to one after the added earlier basin weight.

GREMLIN artifact:

`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_KNOWN_NULL_SEPARATION_20260827.json`

SHA-256:

`fe49ff1f993379a90e106fbde0d39f4aa91e87fad7587eaa8c9ba2db12f0bd4c`.

Reference implementation: `src/idt/retrodiction_global_null_gate.py`.

Reference tests: `tests/reference/test_retrodiction_global_null_gate.py`.
