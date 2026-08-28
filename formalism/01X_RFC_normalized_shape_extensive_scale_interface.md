# 01X-RFC — Normalized-Shape / Extensive-Scale Interface

Status: `SIMPLEX_SHAPE_EXPORT_PASS / SCALE_FIBER_INTERFACE_OPEN / RFC_CROSS_BINDING_OPEN`

This interface exports the normalized-state content of IDT 01D in a form suitable for the RFC conserved-carrier interface and for GREMLIN→PNV holonomy auditing. It is an explicit cross-repository interface gate rather than a new sequential Temporal Primitive admission node.

## 1. IDT simplex coordinate

IDT 01D evolves a strictly positive probability state

\[
p=(p_1,\dots,p_m),
\qquad
p_a>0,
\qquad
\sum_a p_a=1,
\]

under the exact Shannon–Onsager equation

\[
\boxed{
\dot p
=-G^{(2)}_\pi(p)\nabla_p\mathcal I_\pi[p].
}
\]

The active state therefore lies on the probability simplex and carries normalized distributional shape.

## 2. Positive extensive lift

Let an external positive carrier vector be

\[
Q=(Q_1,\dots,Q_m),
\qquad Q_a>0,
\]

with

\[
Q_\Sigma=\sum_aQ_a.
\]

Define

\[
\mathcal N(Q)=\frac{Q}{Q_\Sigma}=p
\]

and an explicit lift

\[
\mathcal L_s(p)=sp,
\qquad s>0.
\]

The round-trip transport is

\[
\boxed{
\mathcal H_s(Q)
=(\mathcal L_s\circ\mathcal N)(Q)
=\frac{s}{Q_\Sigma}Q.
}
\]

For the positive sector, the relative \(L^1\) holonomy defect is

\[
\boxed{
\Delta_{\rm ext}(Q;s)
=
\frac{\|Q-\mathcal H_s(Q)\|_1}{\|Q\|_1}
=
\left|1-\frac{s}{Q_\Sigma}\right|.
}
\]

The normalized state and the extensive lift coordinate therefore form two typed interface coordinates:

```text
simplex coordinate  p
scale coordinate    s
```

Exact inverse transport occurs at

\[
\boxed{s=Q_\Sigma.}
\]

## 3. Positive-scale invariance

For every \(\lambda>0\),

\[
\boxed{
\mathcal N(\lambda Q)=\mathcal N(Q).
}
\]

Thus the normalization map identifies the positive ray through \(Q\) with one simplex point. This is the exact structural feature used by the RFC RF-N1B2H holonomy probe.

A constructive pair is

\[
Q^{(1)}=(2,3,5),
\qquad
Q^{(2)}=(4,6,10),
\]

with common normalized state

\[
\boxed{p=(0.2,0.3,0.5).}
\]

The normalized-shape defect is zero, while a unit lift gives extensive defects

\[
\Delta_{\rm ext}(Q^{(1)};1)=0.90,
\qquad
\Delta_{\rm ext}(Q^{(2)};1)=0.95.
\]

## 4. RFC candidate cross-binding

RFC RF-N1B2 derives a positive normalized carrier profile

\[
p_a^{(Q)}=\frac{Q_a}{Q_\Sigma}.
\]

IDT therefore exports the following typed candidate interface:

\[
\boxed{
p_a^{\rm IDT}\stackrel{?}{\longleftrightarrow}p_a^{(Q)}}.
\]

The structural type compatibility is exact at the normalized finite-state level. Admission of the physical cross-binding remains `OPEN` until the two sides share an explicitly pinned state space, measure/cell partition, and compatible transport semantics.

## 5. Extensive source-mass coordinate

RFC's continuous carrier conversion uses an energy-per-carrier-charge coordinate \(\epsilon_Q\). For cell carrier amount \(Q_a\), define

\[
m_{Q,a}=\frac{\epsilon_Q}{c^2}Q_a.
\]

Combining this with

\[
Q_a=Q_\Sigma p_a^{(Q)}
\]

gives

\[
\boxed{
m_{Q,a}=M_Qp_a^{(Q)},}
\]

where

\[
\boxed{
M_Q:=\frac{\epsilon_QQ_\Sigma}{c^2}.
}
\]

Thus the candidate IDT↔RFC source interface factorizes into

\[
\boxed{
\text{normalized shape }p
\quad\times\quad
\text{extensive source-mass coordinate }M_Q.
}
\]

For physical cell volume \(V_a\), the RFC density coordinate becomes

\[
\boxed{
\rho_{Q,a}=\frac{M_Q}{V_a}p_a^{(Q)}.
}
\]

The source-mass coordinate \(M_Q\), its factorization into \(Q_\Sigma\) and \(\epsilon_Q\), and the physical carrier binding remain explicit downstream interface gates.

## 6. GREMLIN / PNV export contract

The invariant exported to GREMLIN is

```text
positive extensive state
  -> normalization
  -> simplex shape
  -> explicit scale lift
  -> exact round trip when scale coordinate is preserved
```

The PNV-facing objects are typed as

```text
SOURCE      extensive state Q
TRANSFORM   NORMALIZE
SOURCE      explicit lift scale
TRANSFORM   RESTORE_WITH_SCALE
IDENTITY    round-trip closure
DIFFERENCE  holonomy defect
```

Pinned PNCS bridge candidate:

```text
repository: AdrianLipa90/PhaseNav-Natural-Coding-System
branch: feat/gremlin-pnv-authoring-v0.2
head: 695223eff9373554c4c2aff1aca9c3e1e7dfecd4
bridge: PNCS_GREMLIN_NATIVE_PNV_BRIDGE_V0_2
```

Pinned RFC consumer branch:

```text
repository: AdrianLipa90/Relational-Field-Closure
branch: feat/rfc-gremlin-pnv-holonomy-v0.1
base: RF-N1B2 commit 66a6f9385a62dc473a0b2a02c0bfed26175b123a
consumer gate: RF-N1B2H
```

## 7. Advancement

01X-RFC exports:

```text
IDT normalized simplex shape                 PASS
positive-scale quotient theorem              PASS
analytic extensive holonomy defect           PASS
shape / scale coordinate separation          PASS
IDT p <-> RFC carrier p_Q                    OPEN
common state-space / cell-partition binding  OPEN
RFC source-mass coordinate M_Q               OPEN pending source binding
```

This narrows the coupled IDT↔RFC search: GREMLIN may search for transport-compatible realizations of the shape cross-binding, while the extensive source coordinate is audited independently through PNV holonomy.