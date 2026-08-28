# 07R — Fiber-Lift Composition Theorem for Retrodiction

Status: `EXACT_COMPOSITION_THEOREM_PASS / FINITE_DOMAIN_REFERENCE_PASS / POSITION_LINEAGE_LIFT_ACTIVE_NEXT_GATE / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Purpose

07K supplies an exact arbitrary-event Retrodiction carrier when the ordered post-segment position lineage is retained. 07P supplies the quotient/fiber separation criterion, and 07Q demonstrates that ordered signed ORCHORBITAL winding can separate the exact known reflection fiber.

07R connects those results by an exact composition theorem. The theorem does not infer global injectivity from a finite test. It identifies the precise sufficient condition required to lift the compressed Retrodiction record back to the already injective 07K carrier.

Let

\[
\mathcal Z
\]

be an admitted latent-history domain. Let

\[
P:\mathcal Z\to\mathcal X
\]

be an injective carrier map. In the current Retrodiction architecture, the target carrier is the ordered position lineage

\[
\boxed{
P(z)=(r_1(z),\ldots,r_N(z)).
}
\]

Let

\[
Y:\mathcal Z\to\mathcal Y
\]

be the retained base observation and let

\[
F:\mathcal Z\to\mathcal H
\]

collect retained fiber coordinates, for example ordered winding, continuous ORCHORBITAL coordinates and SOD coordinates. Define

\[
\boxed{
A(z):=(Y(z),F(z)).
}
\]

as the augmented retained observation.

## 2. Fiber-lift composition theorem

Assume:

1. \(P\) is injective on \(\mathcal Z\);
2. there exists a single-valued lift
   \[
   L:A(\mathcal Z)\to\mathcal X
   \]
   satisfying
   \[
   \boxed{P=L\circ A.}
   \]

Then \(A\) is injective on \(\mathcal Z\).

### Proof

Take \(z_1,z_2\in\mathcal Z\) and assume

\[
A(z_1)=A(z_2).
\]

Applying \(L\) gives

\[
L(A(z_1))=L(A(z_2)).
\]

Using \(P=L\circ A\),

\[
P(z_1)=P(z_2).
\]

Since \(P\) is injective,

\[
\boxed{z_1=z_2.}
\]

Therefore \(A\) is injective. \(\square\)

## 3. Equivalent fiber condition

The existence of a single-valued lift on the image \(A(\mathcal Z)\) is equivalent to the consistency condition

\[
\boxed{
A(z_1)=A(z_2)
\Longrightarrow
P(z_1)=P(z_2).
}
\]

When \(P\) is injective, this immediately collapses to

\[
A(z_1)=A(z_2)
\Longrightarrow
z_1=z_2.
\]

Thus the global Retrodiction problem can be phrased as a carrier-lift problem rather than as an unconstrained search over latent histories.

## 4. Binding to 07K

07K proves an exact algebraic recursion for the event kicks from the ordered position lineage and persisted active-attractor sequence. For event \(n\),

\[
\boxed{
u_n=
\frac{r_n-r_{n-1}-\frac12A_n(r_{n-1})\Delta\tau_n^2}
{\Delta\tau_n}
-v_{n-1}}
\]

with

\[
\boxed{
v_n=v_{n-1}+u_n+
\frac12\bigl[A_n(r_{n-1})+A_n(r_n)\bigr]\Delta\tau_n.}
\]

Hence, on the admitted 07K domain with the declared active sequence and positive elapsed increments, the position-lineage carrier \(P\) is the injective reference carrier used by 07R.

The remaining constructive task is therefore to derive or verify a lift

\[
\boxed{
L:\bigl(Y,F\bigr)\mapsto(r_1,\ldots,r_N)
}
\]

from the retained compressed coordinates.

## 5. Relation to 07P and 07Q

07P states the finite-domain fiber-separation criterion directly in latent space. 07R supplies the complementary carrier formulation:

\[
\boxed{
\text{base/fiber record}
\xrightarrow{\ L\ }
\text{ordered position lineage}
\xrightarrow{\ 07K^{-1}\ }
\text{latent history}.
}
\]

07Q supplies one concrete fiber coordinate,

\[
\mathcal W(z)=(\Delta W_1,\ldots,\Delta W_N),
\]

and verifies that it separates the exact known reflection pair while the base observation and active-label class remain colliding.

For that pair, the 07R finite reference audit uses:

- the same sparse base observation as 07Q;
- `oriented_winding` as the declared fiber channel;
- the complete ordered post-segment position lineage as carrier \(P\).

The audit returns

```text
FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS
```

with zero carrier collisions, zero augmented collisions and zero lift conflicts.

A matched negative control replaces winding by an identical zero fiber. The base collision then maps to two distinct position carriers, and the audit returns

```text
FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN
```

as required.

## 6. Finite-domain executable audit

The reference implementation audits the theorem hypotheses on a declared finite candidate domain. For distinct latent candidates \(z_i,z_j\), it independently checks:

### Carrier injectivity

\[
\|P(z_i)-P(z_j)\|_2>\varepsilon_P.
\]

A violation emits

```text
CARRIER_INJECTIVITY_FAIL_ON_FINITE_DOMAIN
```

### Functional lift consistency

If the augmented record is equivalent,

\[
\|Y(z_i)-Y(z_j)\|_2\le\varepsilon_B
\]

and every declared fiber channel satisfies

\[
\|F_c(z_i)-F_c(z_j)\|_2\le\varepsilon_F,
\]

then the carrier must also be equivalent. An augmented collision with distinct carriers emits

```text
FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN
```

Only when the carrier is pairwise injective and no functional-lift conflict exists does the finite audit emit

```text
FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS
```

This executable status is finite-domain evidence for the theorem hypotheses; the theorem itself is the exact implication of Section 2.

## 7. Hosted reference evidence

Implementation:

- `src/idt/retrodiction_fiber_lift.py`.

Tests:

- `tests/reference/test_retrodiction_fiber_lift.py`.

The test layer covers:

1. an exact finite composition pattern;
2. explicit functional-lift conflict;
3. explicit carrier-injectivity failure;
4. identical-latent control;
5. the exact 07Q reflection pair with ordered winding and the 07K position carrier;
6. the same reflection pair with a non-separating zero-fiber control;
7. mismatched record-count rejection;
8. non-finite record rejection.

Hosted authority:

- workflow: `Reference suite`;
- run: `33202559485` / run number `621`;
- job: `98955383447`;
- tested branch head: `6abca4ad72c04cdca5d1128e690c17898b8650d7`;
- tested PR merge commit: `a58b0c382727435f0e16231085181b60651f7f98`;
- command: `python -m pytest -q tests/reference`;
- result: `510 passed in 14.11s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion: `success`.

## 8. Active frontier

The exact 07R theorem reduces the active global Retrodiction closure to construction of a domain-covering lift from retained coordinates to the 07K position-lineage carrier.

The active target is therefore

```text
POSITION_LINEAGE_LIFT_ACTIVE_NEXT_GATE
```

with candidate fiber inputs drawn from the already retained ordered winding, continuous ORCHORBITAL and SOD channels. The governing global status remains `GENERAL_GLOBAL_INJECTIVITY_OPEN` until a domain-covering lift or an equivalent fiber-separation argument is receipted.
