# 05I — Regular Smooth Clock Extension Witness

Status: `EXACT_AFFINE_ATLAS_GLUE_THEOREM / DISCRETE_TO_SMOOTH_WITNESS_CERTIFIER / PRODUCTION_REGULAR_CLOCK_WITNESS_OPEN_INPUT`

Date: 2026-08-30

## 1. Purpose

05H reconstructs an exact scalar clock on a connected event complex when the positive elapsed one-cochain has zero period on every cycle. 05G proves that a regular smooth scalar clock produces the temporal foliation required by the relativistic join.

The remaining interface is therefore precise:

```text
05H exact discrete event clock
 -> regular smooth scalar extension witness
 -> 05G domain-wide temporal foliation
```

05I certifies a supplied continuum witness for that interface.

It does not infer a smooth continuum realization from graph exactness alone. The existence and coverage of the production spacetime realization remain explicit inputs.

## 2. Discrete parent

On the 05H exact sector there is a scalar

\[
t_V:V(K_1)\to\mathbb R
\]

such that every realized directed edge satisfies

\[
\boxed{t_V(v)-t_V(u)=\theta(u\to v)>0.}
\]

The scalar is unique up to one additive constant on a connected event complex.

This additive freedom must be preserved by the continuum bridge.

## 3. Finite smooth-clock witness format

Let the target continuum domain be represented by a supplied finite collection of smooth coordinate patches \(U_p\subset M\), each with coordinates

\[
x_p=(x_p^0,x_p^1,x_p^2,x_p^3).
\]

On patch \(p\), the witness supplies an affine representative

\[
\boxed{t_p(x_p)=a_{p\mu}x_p^\mu+b_p,}
\]

with

\[
\boxed{a_p\neq0.}
\]

Because the coefficients are constant, each \(t_p\) is \(C^\infty\), and

\[
\boxed{dt_p=a_{p\mu}dx_p^\mu\neq0}
\]

everywhere on that patch.

The affine representation is a certificate format for a regular scalar clock. By the standard submersion/constant-rank theorem, any regular smooth scalar admits local coordinates in which it is itself a coordinate, so an adapted affine local representative is available wherever a regular scalar witness has already been supplied.

This statement concerns representation of a supplied regular scalar; it does not supply the production scalar or prove coverage of the target domain.

## 4. Overlap compatibility

On an overlap \(U_p\cap U_q\), use the supplied affine coordinate transition

\[
\boxed{x_q=A_{q\leftarrow p}x_p+s_{q\leftarrow p},}
\]

with

\[
\det A_{q\leftarrow p}\neq0.
\]

For one scalar clock, the local representatives must obey

\[
\boxed{t_q\circ\phi_{q\leftarrow p}=t_p.}
\]

Substitution gives the exact coefficient conditions

\[
\boxed{a_qA_{q\leftarrow p}=a_p,}
\]

and

\[
\boxed{a_q\cdot s_{q\leftarrow p}+b_q=b_p.}
\]

When these hold on every overlap, the patchwise functions agree wherever both are defined and therefore glue to one smooth scalar on the represented union.

## 5. Regularity theorem

Since every local gradient is nonzero,

\[
dt|_{U_p}=dt_p\neq0.
\]

Overlap compatibility makes these covectors coordinate representatives of the same global one-form \(dt\). Hence on the supplied covered domain,

\[
\boxed{dt\neq0.}
\]

The glued scalar is a submersion there.

Consequently the 05G premises become available:

\[
\Theta_R=N_Rc\,dt,
\qquad N_R>0,
\]

and therefore

\[
\boxed{\Theta_R\wedge d\Theta_R=0.}
\]

The 05I output therefore feeds the already proved 05G foliation theorem rather than replacing it.

## 6. Event-clock alignment

Let an event \(v\in V(K_1)\) be embedded in patch \(p\) at coordinates \(X_{p,v}\).

Because the discrete 05H clock is defined only up to one additive constant, the continuum witness extends it exactly when there exists one \(C\in\mathbb R\) such that every supplied event embedding obeys

\[
\boxed{t_p(X_{p,v})=t_V(v)+C.}
\]

The same \(C\) must work for all events and all patches.

If the same event is represented in two overlapping patches, the coordinate embeddings must also satisfy the declared transition map:

\[
\boxed{X_{q,v}=A_{q\leftarrow p}X_{p,v}+s_{q\leftarrow p}.}
\]

This prevents a numerically aligned clock value from hiding an inconsistent event embedding.

## 7. Atlas cocycle

On a declared triple overlap \((p,q,r)\), coordinate consistency requires

\[
\boxed{A_{r\leftarrow p}=A_{r\leftarrow q}A_{q\leftarrow p}}
\]

and

\[
\boxed{
s_{r\leftarrow p}
=A_{r\leftarrow q}s_{q\leftarrow p}+s_{r\leftarrow q}.
}
\]

The certifier checks both identities on every declared triangle.

## 8. Domain-wide promotion firewall

Patch compatibility proves one regular smooth scalar on the union represented by the supplied witness.

A claim about the full target spacetime additionally requires a coverage witness establishing that the supplied patch collection covers that target domain.

Therefore the executable certificate separates

```text
regular compatible clock witness on supplied patches       PASS/FAIL
full target-domain coverage witness                         SUPPLIED/OPEN
production event/continuum data                             SUPPLIED/OPEN
```

Reference fixtures may set the coverage flag to exercise the theorem. That does not promote the production spacetime.

Production status remains

`PRODUCTION_REGULAR_CLOCK_WITNESS_OPEN_INPUT`.

## 9. Exact handoff to 05G and RFC

Once the production 05H event complex has passed, and a production 05I witness has passed with full target-domain coverage, the temporal chain is

```text
05H exact discrete scalar t_V
 -> 05I smooth regular scalar t on M, dt != 0
 -> 05G global regular temporal foliation
 -> RFC RF-E25 shared spacetime atlas/coframe certificate
 -> RFC RF-E24 local Einstein form on the assembled domain
```

This is FPDG coordinate `GSC-3`.

## 10. Falsification gates

05I fails closed if any of the following occurs:

1. a patch clock coefficient is non-finite;
2. a patch has \(a_p=0\), hence a vanishing clock differential;
3. an overlap map is singular;
4. two local clock representatives disagree under an overlap map;
5. the supplied patch overlap graph is disconnected for a connected-domain claim;
6. any 05H event lacks a continuum embedding;
7. event-clock values fail to match the continuum witness up to one common additive constant;
8. duplicate embeddings of the same event in the same patch occur;
9. repeated event embeddings disagree with the declared overlap coordinates;
10. a declared triple-overlap affine cocycle fails;
11. full-domain promotion is requested without an explicit domain-coverage witness.

## 11. Claim ledger

| Claim | Status |
|---|---|
| exact discrete event clock | `PARENT 05H` |
| 05H additive-constant freedom | `PARENT 05H` |
| affine patch clock is smooth | `EXACT` |
| nonzero affine gradient gives `dt != 0` on patch | `EXACT` |
| overlap coefficient equations imply scalar gluing | `EXACT` |
| affine transition triple-cocycle equations | `EXACT` |
| regular scalar admits local adapted coordinates | `STANDARD SUBMERSION/CONSTANT-RANK THEOREM` |
| one global event-to-continuum additive alignment | `EXACT WITNESS CONDITION` |
| executable regular smooth-clock witness certifier | `PASS TARGET` |
| production regular smooth-clock witness | `OPEN_INPUT` |
| production full-domain coverage | `OPEN_INPUT` |
| 05G global foliation after production 05I PASS | `CONDITIONAL PARENT THEOREM` |
| Cauchy/global hyperbolicity | `OPEN SEPARATE GATE` |

## 12. Validation authority

Reference implementation:

`src/idt/regular_smooth_clock_extension.py`

Reference tests:

`tests/reference/test_regular_smooth_clock_extension.py`

Static receipt:

`validation/REGULAR_SMOOTH_CLOCK_EXTENSION_V0_1.json`

Verdict target:

`PASS_IDT_REGULAR_SMOOTH_CLOCK_EXTENSION_CERTIFIER_WITH_PRODUCTION_INPUT_OPEN`.
