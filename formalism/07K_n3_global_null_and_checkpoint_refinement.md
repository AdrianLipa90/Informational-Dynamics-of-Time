# 07K — N=3 Global Null and Checkpoint Refinement

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / N3_GLOBAL_NULL_EXPLICIT / SECOND_EARLIER_WEIGHT_KNOWN_NULL_SEPARATION_PASS / N3_GLOBAL_INJECTIVITY_OPEN`

The 07J rank budget makes \(N=3\) the last event count for which the declared sparse schedule can reach full first-order rank. This gate tests global uniqueness for that dimensionally sufficient case.

## 1. Declared N=3 schedule

For three unknown planar kicks, retain

\[
Y_3=
\left(
 w_{A,1},
 w_{A,2},
 r_{x,3},r_{y,3},v_{x,3},
 w_{A,3},w_{B,3},w_{C,3}
\right).
\]

Inside the tested fixed active/support regime its Jacobian reaches rank six for six latent coordinates, as recorded in 07J.

## 2. Explicit distinct-history collision

The generating history is

\[
\begin{aligned}
u_1&=(0.034,-0.023),\\
u_2&=(-0.008,0.028),\\
u_3&=(0.020,-0.015).
\end{aligned}
\]

A second fitted history is

\[
\begin{aligned}
\tilde u_1&=(0.02171604910786055,-0.01997647522522139),\\
\tilde u_2&=(0.02066339813510957,0.02094610600551937),\\
\tilde u_3&=(0.00362139881046886,-0.01096863363360488).
\end{aligned}
\]

Their latent separation is

\[
\boxed{
\|\tilde z-z\|_2=0.03627527334738057.
}
\]

Yet the complete declared observation agrees to

\[
\boxed{
\|Y_3(\tilde z)-Y_3(z)\|_2
=1.6939998869943826\times10^{-16}.
}
\]

Thus the dimensionally sufficient N=3 schedule has a distinct global branch in the declared reference system.

## 3. Why the collision survives

Earlier single basin weights constrain scalar binding/kinetic information while retaining directional freedom in the intermediate Memory phase state. The two histories exploit this freedom and merge into the same later checkpoint lineage while preserving the selected earlier \(w_A\) values.

For checkpoint 1,

\[
w_{A,1}(z)=w_{A,1}(\tilde z)=0.5838364569736161
\]

to the declared numerical resolution.

This gives a concrete global counterpart to the 07F distinction between local rank and global uniqueness.

## 4. One additional independent ORCHORBITAL scalar

At the same first checkpoint the second basin weight differs:

\[
w_{B,1}(z)=0.19430826752908295,
\]

\[
w_{B,1}(\tilde z)=0.19430761251872072.
\]

Hence

\[
\boxed{
|\Delta w_{B,1}|
=6.550103622271486\times10^{-7}.
}
\]

Adding \(w_{B,1}\) therefore changes the declared pair status to `KNOWN_NULL_SEPARATED`.

The first position component also differs by

\[
|\Delta r_{x,1}|=4.9135803568578496\times10^{-5},
\]

showing that the collision is tied to information discarded by the original sparse earlier checkpoint.

## 5. Bounded multistart diagnostic

A deterministic 300-start bounded search over the six-dimensional latent box used the same fixed-regime reference target.

For the original N=3 schedule:

- successful residuals below \(10^{-8}\): `91`;
- recovered clusters: `2`;
- cluster counts: `45`, `46`.

After adding only \(w_{B,1}\):

- successful residuals below \(10^{-8}\): `51`;
- recovered clusters: `1`.

This is a bounded diagnostic supporting separation of the explicit pair. N=3 global injectivity remains a separate gate.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. It matched

`DIMENSIONALLY_SUFFICIENT_MAP -> MAGNITUDE_ONLY_INTERMEDIATE_CHECKPOINT -> DISCRETE_GLOBAL_COLLISION -> ADDITIONAL_INDEPENDENT_SCALAR -> KNOWN_COLLISION_SEPARATION`

against the generic inverse-problem architecture with `structurally_isomorphic=true`, comparison SHA-256
`ffeed170561037dcfa635b4cad12b47f808d6db8d5a2af5b91a06c779d018958`.

Three declared hypotheses returned `SUPPORTED_BY_DECLARED_TESTS`.

Probe artifact:
`/dev/shm/ciel_noema/gremlin/IDT_RETRODICTION_N3_GLOBAL_NULL_PROBE_20260827.json`

SHA-256:
`b4ec7e55078bbb6d621087b19c354f1411f9843f212848958d9c357a75c1832b`

GREMLIN artifact:
`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_N3_GLOBAL_NULL_20260827.json`

SHA-256:
`d74407ba6b0de910ea639692ad49fadfd86d7bc77e298cb7f02e17baca984828`.

Reference tests use the existing generic sparse-observation/null-separation implementation in `src/idt/retrodiction_global_null_gate.py`.
