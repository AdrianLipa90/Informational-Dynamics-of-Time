# 05I — Regular Smooth Clock Extension on an Affine Atlas

Status: `EXACT_AFFINE_ATLAS_REGULAR_EXTENSION_THEOREM / EXECUTABLE_SMOOTH_CLOCK_WITNESS_CERTIFIER / 05H_EVENT_ANCHOR_BINDING_PASS_TARGET / PRODUCTION_ATLAS_AND_EVENT_ANCHOR_INPUT_OPEN / GENERAL_NONAFFINE_EXTENSION_OPEN`

Date: 2026-08-31

## 1. Purpose

05H closes the discrete exactness question for a supplied connected event complex. When its temporal one-cochain has zero period, it reconstructs one scalar event clock

\[
t_v:V(K_1)\to\mathbb R
\]

unique up to one additive constant.

05G requires the continuum input

\[
t\in C^2(M,\mathbb R),\qquad dt\neq0
\]

on the admitted spacetime domain. Gate 05I supplies a sufficient, fail-closed realization theorem and executable witness format between those two statements.

The dependency line becomes

```text
05H exact discrete event clock
 -> 05I regular affine-atlas clock extension certificate
 -> 05G temporal foliation
```

## 2. Affine-atlas witness

Let the admitted domain be covered by smooth coordinate charts `U_A` of one common real dimension `d`. On each chart provide a local affine clock

\[
\boxed{t_A(x_A)=b_A+g_A\cdot x_A}
\]

with constant covector

\[
\boxed{g_A\neq0.}
\]

On a declared overlap `U_A cap U_B`, let the admitted coordinate transition be affine and invertible,

\[
\boxed{x_B=A_{BA}x_A+c_{BA},\qquad A_{BA}\in GL(d,\mathbb R).}
\]

The transition data are part of the supplied atlas witness.

## 3. Exact overlap theorem

The two local clock expressions represent one scalar on the overlap exactly when

\[
t_B(A_{BA}x_A+c_{BA})=t_A(x_A)
\]

for every overlap coordinate `x_A`. Expanding gives

\[
g_BA_{BA}x_A+g_B\cdot c_{BA}+b_B
=g_Ax_A+b_A.
\]

Therefore the necessary and sufficient affine identities are

\[
\boxed{g_BA_{BA}=g_A}
\]

and

\[
\boxed{g_B\cdot c_{BA}+b_B=b_A.}
\]

These are finite-dimensional algebraic equalities and are directly executable.

## 4. Regularity theorem

On every chart,

\[
\boxed{dt_A=g_A.}
\]

Hence `g_A != 0` implies

\[
\boxed{dt_A\neq0}
\]

everywhere on that chart.

Because each transition Jacobian `A_BA` is invertible and the overlap identity gives

\[
g_A=g_BA_{BA},
\]

regularity is coordinate-compatible across the admitted atlas.

If all declared overlap identities pass, the local smooth functions agree on overlaps and therefore glue to one smooth scalar

\[
\boxed{t:M\to\mathbb R}
\]

on the admitted atlas domain. Its differential is nowhere zero on the certified domain:

\[
\boxed{dt\neq0.}
\]

Thus the supplied affine-atlas witness is sufficient for the global regular-clock input required by 05G.

## 5. Binding to the 05H discrete event clock

Let 05H reconstruct event potentials

\[
\boxed{t_v}
\]

from the production event complex. For each admitted anchor, provide an event `v`, chart `A`, and chart coordinate `x_A(v)`.

Since the 05H scalar is unique up to one additive constant, the continuum witness is compatible exactly when one constant `C` exists such that every anchor satisfies

\[
\boxed{t_A(x_A(v))-t_v=C.}
\]

The reference certifier reconstructs the first anchor's value of `C` and requires every remaining anchor to agree with it. For a global event-to-continuum binding claim, every 05H event must have at least one admitted continuum anchor.

Multiple anchors for the same event in different charts provide an additional overlap consistency check.

## 6. Connected-domain gate

For a connected-domain promotion, the undirected graph of declared chart overlaps must be connected. A disconnected atlas is retained only under an explicitly componentwise claim.

This gate certifies the supplied affine-atlas realization. General non-affine smooth extension remains a separately typed continuum route.

## 7. Reference witness

The reference positive control uses two four-dimensional affine charts:

\[
t_A(x)=x^0,
\]

\[
x_B=x_A+(1,0,0,0),
\qquad
t_B(x_B)=x_B^0-1.
\]

Thus

\[
t_B(x_B)=x_A^0=t_A(x_A),
\]

and both gradients are

\[
(1,0,0,0)\neq0.
\]

A two-event 05H chain with elapsed increment `2` is anchored at

\[
e_0\mapsto x_A^0=0,
\qquad
e_1\mapsto x_A^0=2,
\]

with a duplicate `e_1` anchor in chart `B` at `x_B^0=3`. All residuals vanish exactly in the reference fixture.

The fixture validates the certifier only. Production promotion requires source-owned event and atlas data.

## 8. Falsification rules

05I fails closed when any of the following occurs:

1. a chart clock gradient vanishes or falls below the declared numerical regularity floor;
2. chart dimensions disagree;
3. a declared overlap transition is singular;
4. the overlap gradient identity fails;
5. the overlap offset identity fails;
6. a connected-domain claim is made for a disconnected chart-overlap graph;
7. an anchor references an unknown chart or unknown 05H event;
8. event anchors require more than one additive calibration constant;
9. a global event-clock binding claim omits continuum anchors for admitted 05H events;
10. any supplied numerical value is non-finite.

## 9. Claim ledger

| Claim | Status |
|---|---|
| affine overlap identity iff coefficient identities hold | `EXACT` |
| nonzero affine clock gradient implies `dt != 0` on the chart | `EXACT` |
| invertible overlap transitions preserve regularity class | `EXACT` |
| compatible local affine clocks glue to one smooth scalar on the admitted atlas | `EXACT ON DECLARED AFFINE ATLAS` |
| one additive anchor offset binds the continuum scalar to the 05H event clock | `EXACT` |
| executable regular-clock witness certifier | `PASS TARGET` |
| reference affine-atlas fixture | `REFERENCE VALIDATION` |
| production event-complex + continuum-atlas witness | `OPEN INPUT` |
| general non-affine smooth extension route | `OPEN ROUTE` |

## 10. Validation authority

Reference implementation:

`src/idt/regular_smooth_clock_extension.py`

Reference tests:

`tests/reference/test_regular_smooth_clock_extension.py`

Static receipt:

`validation/REGULAR_SMOOTH_CLOCK_EXTENSION_V0_1.json`

Verdict target:

`PASS_IDT_05I_REGULAR_AFFINE_CLOCK_EXTENSION_CERTIFIER_WITH_PRODUCTION_INPUT_OPEN`.

## 11. Handoff

A production 05H PASS plus a production 05I PASS supplies the exact typed input consumed by 05G:

\[
\boxed{t\in C^\infty(M),\qquad dt\neq0.}
\]

05G may then apply its existing Frobenius and regular-level-set theorems on that same admitted domain. The stronger Cauchy/global-hyperbolicity promotion remains downstream in RFC L7.
