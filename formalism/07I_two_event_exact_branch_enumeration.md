# 07I — Exact Two-Event Retrodiction by Finite Active-Branch Enumeration

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / TWO_EVENT_EXACT_BRANCH_ENUMERATION_TARGETED_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`

This layer uses the discrete velocity-Verlet Memory/ORCHORBITAL reference cell to replace local optimization by exact algebraic inversion for the two-event full-checkpoint problem.

## 1. Fixed active-attractor sequence

Let
\[
X_0=(r_0,v_0)
\]
be known, let the final full phase checkpoint
\[
X_2=(r_2,v_2)
\]
be retained, and let the two internal elapsed increments be
\[
\Delta\tau_1>0,\qquad \Delta\tau_2>0.
\]
For one declared ordered active-attractor pair
\[
(a_1,a_2),
\]
the second smooth ORCHORBITAL segment is algebraically invertible. Applying the existing centred velocity-Verlet inverse under \(a_2\) yields the state immediately after the second kick,
\[
\boxed{
(r_1,\tilde v_2)
=
\Phi_{a_2}^{-1}(\Delta\tau_2)X_2,
}
\]
where
\[
\tilde v_2=v_1+u_2.
\]

## 2. First kick from the intermediate position

For the first attractor define
\[
a_{1,0}=a_{a_1}(r_0),
\qquad
a_{1,1}=a_{a_1}(r_1).
\]
The velocity-Verlet position update is
\[
r_1
=r_0+(v_0+u_1)\Delta\tau_1
+\frac12a_{1,0}\Delta\tau_1^2.
\]
Therefore
\[
\boxed{
u_1
=
\frac{r_1-r_0-\tfrac12a_{1,0}\Delta\tau_1^2}
{\Delta\tau_1}
-v_0.
}
\]
For a fixed active sequence, the first kick is thus uniquely determined by the intermediate position.

The post-segment velocity is
\[
\boxed{
v_1
=v_0+u_1
+\frac12(a_{1,0}+a_{1,1})\Delta\tau_1.
}
\]
Hence the second kick is
\[
\boxed{
u_2=\tilde v_2-v_1.}
\]
Each declared active-attractor pair therefore produces at most one continuous kick pair.

## 3. Finite branch enumeration

For a finite attractor family
\[
\mathcal A=\{\mathfrak A_1,\ldots,\mathfrak A_M\},
\]
the two-event discrete mode space has exactly
\[
M^2
\]
ordered active sequences. The exact reference algorithm is:

1. enumerate every \((a_1,a_2)\in\mathcal A^2\);
2. invert the second smooth segment under \(a_2\);
3. reconstruct \(u_1,u_2\) algebraically;
4. replay the complete Memory→ORCHORBITAL lineage with the full attractor family;
5. retain the candidate only when replay selects the same active sequence and reproduces the final full checkpoint within the declared tolerance.

The resulting statuses are

- `NO_ADMISSIBLE_BRANCH`;
- `EXACT_UNIQUE_REFERENCE_BRANCH`;
- `FINITE_BRANCH_AMBIGUITY`.

Thus the two-event global inverse problem is converted into a finite discrete branch audit followed by exact continuous reconstruction inside each branch.

## 4. Reference probe

A deterministic 5000-case probe used the three-attractor reference family, random initial Memory states, two positive internal elapsed increments and two random event kicks.

- generated cases: `5000`;
- forward `LEAK_MODE` cases excluded by the existing admission boundary: `10`;
- admitted cases: `4990`;
- admitted cases with exactly one self-consistent branch: `4990`;
- admitted cases with multiple branches: `0`;
- admitted cases with no branch: `0`;
- maximum recovered latent-kick error: `3.230770417104829e-11`.

This supplies a targeted unique-reference result for the declared probe population. The formal structural result is the finite exact branch enumeration itself; general multi-event/global injectivity remains downstream.

## 5. Relation to the 07G/07H reflection null

The 07G reflection pair collides only after dropping the final signed \(v_y\) component. A full final phase checkpoint enters the 07I exact branch gate and selects the generating branch in the reference case. The 07H earlier-weight gate remains useful for partial-checkpoint Retrodiction, while 07I supplies the exact full-checkpoint reference closure for two events.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. It matched

`DISCRETE_MODE_SEQUENCE -> CONTINUOUS_CANDIDATE -> FORWARD_CONSISTENCY -> ADMITTED_BRANCH`

with the corresponding generic hybrid inverse-problem architecture and returned `structurally_isomorphic=true`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `2/2`, and `2/2`:

1. fixed-sequence algebraic reconstruction recovers the generating kick pair in the admitted probe;
2. finite enumeration returns one self-consistent branch for every admitted trajectory in the declared 4990-case sample;
3. forward `LEAK_MODE` cases remain outside the admitted branch-enumeration population.

GREMLIN artifact:

`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_TWO_EVENT_EXACT_BRANCH_ENUMERATION_20260827.json`

SHA-256:

`356fa50fb1a50e352c97248b70e380ef8d71b4e486532b28bc378c38e20832fa`.

Reference implementation: `src/idt/retrodiction_two_event_exact.py`.

Reference tests: `tests/reference/test_retrodiction_two_event_exact.py`.
