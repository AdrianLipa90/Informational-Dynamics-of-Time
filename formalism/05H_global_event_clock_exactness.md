# 05H — Global Event-Clock Exactness and Temporal-Holonomy Certificate

Status: `EXACT_GRAPH_COHOMOLOGY_THEOREM / PATH_INDEPENDENCE_CERTIFIER_PASS / PREFIX_TREE_EXACTNESS_AUTOMATIC / PRODUCTION_EVENT_COMPLEX_INPUT_OPEN / SMOOTH_SPACETIME_EXTENSION_OPEN`

Date: 2026-08-30

## 1. Purpose

05G proves that the 05C temporal coframe

\[
\Theta_R=N_Rc\,dt
\]

is Frobenius-integrable wherever one regular calibrated clock scalar \(t\) exists. The remaining clock question is therefore an exactness question: when can the positive elapsed increments already derived by 00E/00F be represented by one scalar value on a connected event complex?

05H turns that question into an executable temporal-holonomy certificate.

## 2. Positive event-edge one-cochain

Let \(K_1\) be a connected event graph with oriented realized edges

\[
e:u\to v.
\]

00E supplies the positive elapsed weight

\[
\boxed{\theta(e)>0.}
\]

Treat these weights as a real one-cochain on the oriented edge set:

\[
\boxed{\vartheta_{uv}:=\theta(u\to v),\qquad \vartheta_{vu}:=-\vartheta_{uv}.}
\]

The target is a scalar event clock

\[
\boxed{t:V(K_1)\to\mathbb R}
\]

such that every admitted oriented edge satisfies

\[
\boxed{t(v)-t(u)=\vartheta_{uv}=\theta(u\to v)>0.}
\]

## 3. Exactness theorem

Choose one root vertex \(o\). For any path \(P:o\leadsto v\) in the underlying undirected graph, define the signed path integral

\[
I(P)=\sum_{e\in P}\operatorname{sgn}_P(e)\,\theta(e).
\]

A scalar potential exists if and only if the integral is path-independent. Equivalently, every closed undirected cycle \(C\) has zero signed period:

\[
\boxed{\oint_C\vartheta=0.}
\]

### Theorem — graph exactness

For a connected graph, the following are equivalent:

1. there exists \(t:V\to\mathbb R\) with \(t(v)-t(u)=\vartheta_{uv}\) on every edge;
2. every two paths with the same endpoints have the same signed elapsed integral;
3. every cycle has zero signed temporal period.

When these conditions hold, the scalar is unique up to one additive constant.

This is the discrete exact-one-form criterion

\[
\boxed{\vartheta=\delta t.}
\]

## 4. Temporal holonomy defect

For two paths \(P_1,P_2:u\leadsto v\), define

\[
\boxed{\Delta_T(P_1,P_2):=I(P_1)-I(P_2).}
\]

Equivalently, on the closed chain \(C=P_1-P_2\),

\[
\Delta_T=\oint_C\vartheta.
\]

The exact clock sector is

\[
\boxed{\Delta_T=0\quad\text{for every cycle}.}
\]

A nonzero value is retained as an explicit temporal-holonomy defect. The certifier fails closed on such a graph and reports the conflicting potential increment.

## 5. Relation to 00F prefix histories

00F labels a realized occurrence by its full prefix

\[
\nu_k=(P_k,x_k).
\]

On one prefix tree there is a unique path from the root to every occurrence. Therefore

\[
\Theta(P_k)=\sum_{r=1}^k\theta(e_r)
\]

already defines an exact scalar on that tree.

The new content of 05H appears when the event representation admits mergers or identifications between branches. A diamond

```text
      b
     / \
    a   d
     \ /
      c
```

has a common event clock at `d` exactly when

\[
\theta_{ab}+\theta_{bd}
=
\theta_{ac}+\theta_{cd}.
\]

Thus 05H is the quotient/merger compatibility gate downstream of the prefix construction.

## 6. Strict temporal precedence

On the exact sector,

\[
t(v)-t(u)=\theta(u\to v)>0
\]

for every realized directed edge. Hence

\[
\boxed{u\to v\Longrightarrow t(u)<t(v).}
\]

Any directed cycle would imply a positive total increase returning to the same scalar value and is therefore rejected automatically by the exactness condition.

The reconstructed event clock is consequently a strict scalar time function on the certified directed event graph.

## 7. Reference-clock covariance

05A/05C introduce a positive calibration of elapsed activity. A common positive global rescaling

\[
t\mapsto at+b,
\qquad a>0,
\]

preserves exactness and strict orientation.

02JL separately controls changes between admitted positive phase-clock references. Its multiplicative reference cocycle acts on clock coordinates/rates; 05H owns the additional path-independence condition required when multiple relational histories are identified inside one event complex.

## 8. Handoff to 05G

A certified connected event graph provides a global discrete scalar potential

\[
\boxed{t_v}
\]

unique up to one additive constant.

05G then requires a smooth spacetime realization whose scalar extension has

\[
dt\neq0
\]

on the target domain. Therefore the dependency line becomes

```text
00E positive edge durations
 -> 00F exact prefix-tree clock
 -> 05H event-merger / cycle exactness certificate
 -> global discrete event clock t_v
 -> smooth regular extension gate
 -> 05G global temporal foliation
```

The smooth extension remains a separately typed continuum interface.

## 9. Production-data promotion

The reference certifier proves the criterion and exercises positive and negative controls. Promotion for the physical/global IDT event complex requires the actual event incidence and elapsed-edge dataset to be supplied to the certifier.

Status:

`PRODUCTION_EVENT_COMPLEX_INPUT_OPEN`.

A PASS on that production input would promote a global discrete event-clock scalar. It would then feed the smooth-extension interface rather than bypass it.

## 10. Falsification rules

The certifier fails if:

1. an elapsed edge weight is non-positive or non-finite;
2. a declared event edge is a positive self-loop;
3. one connected event component receives inconsistent potential values through different paths;
4. any directed edge fails the reconstructed equation \(t(v)-t(u)=\theta(e)\);
5. a connected-domain claim is requested for disconnected event data.

## 11. Claim ledger

| Claim | Status |
|---|---|
| positive elapsed edge weights | `PARENT 00E` |
| prefix-tree cumulative scalar | `PARENT 00F` |
| zero cycle periods iff scalar potential exists | `EXACT GRAPH COHOMOLOGY THEOREM` |
| exact scalar unique up to additive constant per connected component | `EXACT` |
| positive exact edge increments imply strict directed time order | `EXACT` |
| temporal-holonomy defect is path-integral mismatch | `EXACT` |
| executable path-independence certifier | `PASS TARGET` |
| production global event-complex certificate | `OPEN_INPUT` |
| smooth regular scalar extension to spacetime | `OPEN_INTERFACE` |

## 12. Validation authority

Reference implementation:

`src/idt/global_event_clock_exactness.py`

Reference tests:

`tests/reference/test_global_event_clock_exactness.py`

Static receipt:

`validation/GLOBAL_EVENT_CLOCK_EXACTNESS_V0_1.json`

Verdict target:

`PASS_IDT_EVENT_CLOCK_EXACTNESS_CERTIFIER_WITH_PRODUCTION_INPUT_OPEN`.
