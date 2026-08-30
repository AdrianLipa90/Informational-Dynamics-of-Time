# TEMPORAL_TRACE_BINDING — Canonical Positive-Hermitian Lift v0.2

Status: **CANDIDATE / EXACT CANONICAL-LIFT THEOREM + PHYSICAL BINDING GATE**

Repository anchors inspected:
- TIR: `AdrianLipa90/The-Fundamental-Theory-of-Informational-Relations`
  @ `3f5a08ef04ec53c1a155263d23e8b10a96404370`
- IDT: `AdrianLipa90/Informational-Dynamics-of-Time`, current `main`
- RFC: `AdrianLipa90/Relational-Field-Closure`
  @ `63418a88d686021c2a6fe6ab159d6152db303c19`

## 1. Inputs already present upstream

TIR uses normalized binary quantum-point states

\[
\rho=\rho^\dagger,\qquad \rho\succeq0,\qquad \operatorname{Tr}\rho=1,
\]

with Bloch form

\[
\rho=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),
\qquad |\mathbf r|\le1.
\]

Its affine translation carrier is

\[
\operatorname{Herm}_0(2)\cong\mathbb R^3.
\]

IDT 00E derives an invariant positive elapsed quantity from relational activity:

\[
d\Theta=\mathfrak a\,d\lambda,
\qquad
\theta(e)=\int_e\mathfrak a\,d\lambda>0,
\]

with additive composition

\[
\Theta(P_n)=\sum_{k=1}^n\theta(e_k).
\]

After reference-clock calibration,

\[
dt=T_r\,d\Theta_r.
\]

Thus IDT supplies one positive scalar elapsed coordinate, while TIR supplies one
trace-one Hermitian state.

## 2. Canonical lift theorem

Let

\[
\ell>0
\]

be the calibrated or uncalibrated positive temporal scale, with physical choice
\(\ell=ct\) after clock calibration.

Seek a positive Hermitian lift \(X\) that recovers both inputs by

\[
\operatorname{Tr}X=\ell
\]

and

\[
\frac{X}{\operatorname{Tr}X}=\rho.
\]

Then necessarily

\[
\boxed{X=\ell\rho.}
\]

### Proof

The second recovery condition gives

\[
X=(\operatorname{Tr}X)\rho.
\]

Using the first gives

\[
X=\ell\rho.
\]

No second lift satisfies both recovery conditions. \(\square\)

Therefore the map

\[
\boxed{
\mathcal L:
\mathbb R_{>0}\times\mathcal D_2
\longrightarrow
\operatorname{Herm}_+(2),
\qquad
(\ell,\rho)\mapsto\ell\rho
}
\]

is the unique positive-Hermitian lift preserving both the IDT scalar and the TIR
trace-one state.

This is the sharpest current form of `TEMPORAL_TRACE_BINDING`.

## 3. Trace is the temporal coordinate

Using

\[
\rho=\frac12(I+\mathbf r\cdot\boldsymbol\sigma),
\]

the lift is

\[
X
=
\frac{\ell}{2}I
+
\frac{\ell}{2}\mathbf r\cdot\boldsymbol\sigma.
\]

Hence the decomposition

\[
\operatorname{Herm}(2)
=
\mathbb RI\oplus\operatorname{Herm}_0(2)
\]

is recovered explicitly as

\[
\boxed{
X=X_T+X_S
}
\]

with

\[
\boxed{
X_T=\frac{\ell}{2}I
}
\]

and

\[
\boxed{
X_S=\frac{\ell}{2}\mathbf r\cdot\boldsymbol\sigma
\in\operatorname{Herm}_0(2).
}
\]

Since

\[
\operatorname{Tr}X_S=0,
\qquad
\operatorname{Tr}X_T=\ell,
\]

the temporal scale is exactly the trace coordinate of the lift.

## 4. Rotational covariance becomes automatic

For a common spatial frame change

\[
\rho\mapsto U\rho U^\dagger,
\qquad U\in SU(2),
\]

define

\[
X\mapsto UXU^\dagger.
\]

Then

\[
\operatorname{Tr}(UXU^\dagger)=\operatorname{Tr}X=\ell.
\]

Therefore the temporal trace scale is invariant, while

\[
X_S\mapsto UX_SU^\dagger
\]

transforms in the spatial adjoint triplet.

The scalar/triplet split is therefore

\[
\boxed{
\mathbb RI\oplus\operatorname{Herm}_0(2)
=
\mathbf1\oplus\mathbf3.
}
\]

No separate assumption about the orientation of a fourth basis vector is required
after the lift has been chosen.

## 5. Positive cone and Lorentz quadratic form

Write

\[
X=x^0I+\mathbf x\cdot\boldsymbol\sigma
\]

with

\[
x^0=\frac{\ell}{2},
\qquad
\mathbf x=\frac{\ell}{2}\mathbf r.
\]

Then

\[
\boxed{
\det X=(x^0)^2-|\mathbf x|^2
=\frac{\ell^2}{4}(1-|\mathbf r|^2).
}
\]

Because \(|\mathbf r|\le1\),

\[
x^0\ge|\mathbf x|,
\qquad
x^0>0.
\]

Thus the positive-Hermitian cone is exactly the future causal cone of the
determinant quadratic form.

The boundary condition is

\[
\det X=0
\iff
|\mathbf r|=1.
\]

The interior condition is

\[
\det X>0
\iff
|\mathbf r|<1.
\]

Therefore:

\[
\boxed{
\text{pure trace-one qubit states}
\leftrightarrow
\text{boundary rays of the positive Hermitian cone}
}
\]

and

\[
\boxed{
\text{full-rank mixed qubit states}
\leftrightarrow
\text{interior rays of the positive Hermitian cone}.
}
\]

The algebraic statements are exact. A physical identification of these rays with
null/timelike spacetime events is a downstream TIR × IDT × RFC binding.

## 6. Why the cone does not restrict the full tangent carrier

One might object that positive Hermitian matrices cover only a cone rather than
all of \(\operatorname{Herm}(2)\). But every Hermitian matrix \(Y\) has spectral
positive/negative parts

\[
Y=Y_+-Y_-,
\qquad
Y_\pm\succeq0.
\]

Hence

\[
\boxed{
\operatorname{span}_{\mathbb R}\operatorname{Herm}_+(2)
=
\operatorname{Herm}(2).
}
\]

Equivalently, differences of admitted positive event carriers generate the full
four-real-dimensional relation/tangent carrier.

Thus event positivity and four-dimensional affine relation freedom coexist.

## 7. Dimension closure

The TIR trace-one slice supplies

\[
\dim\operatorname{Herm}_0(2)=3.
\]

The IDT elapsed scalar supplies the missing trace scale

\[
\dim\mathbb RI=1.
\]

The canonical lift reconstructs

\[
\boxed{
\operatorname{Herm}(2)
=
\mathbb RI\oplus\operatorname{Herm}_0(2)
}
\]

with

\[
\boxed{
\dim_{\mathbb R}\operatorname{Herm}(2)=4.
}
\]

Under the minimal-base rule — base dimensions require independent local
translation directions — the primitive two-level Hermitian completion contains
no fifth independent real Hermitian direction.

Therefore, once the positive elapsed scalar is admitted as the event trace scale,

\[
\boxed{
D_{\rm local\ base}=3+1=4.
}
\]

## 8. What changed relative to v0.1

v0.1 required a structural bridge

\[
\text{IDT temporal scalar}\leftrightarrow\mathbb RI.
\]

v0.2 replaces that free-looking identification by a unique recovery problem:

\[
(\ell,\rho)
\stackrel{?}{\longmapsto}X
\]

subject to

\[
\operatorname{Tr}X=\ell,
\qquad
X/\operatorname{Tr}X=\rho,
\qquad
X\succeq0.
\]

These conditions have the unique solution

\[
X=\ell\rho.
\]

Thus the remaining question is narrower: whether the IDT elapsed scalar is the
physical event-scale variable to be fed into this canonical lift. The algebraic
placement of any admitted positive scalar scale is no longer ambiguous.

## 9. Remaining physical gate

The remaining promotion gate is:

`IDT_ELAPSED_SCALAR_AS_EVENT_TRACE_SCALE`

It must establish, from the TIR/IDT/RFC dependency chain, that the elapsed scalar

\[
\ell \propto \Theta
\]

is the physical local event scale used in the Hermitian event carrier.

A sufficient test would bind:

\[
dt=T_r\,d\Theta_r
\]

to the RFC temporal coframe

\[
\mathcal E^0=N_Rc\,dt
\]

and show consistency with the independently derived spatial physicalization
without inserting a four-dimensional metric as a premise.

## 10. Status ledger

| Statement | Status |
|---|---|
| unique lift \(X=\ell\rho\) under trace + normalization recovery | EXACT |
| trace coordinate equals \(\ell\) | EXACT |
| traceless component lies in TIR spatial carrier | EXACT |
| common \(SU(2)\) conjugation preserves trace scale | EXACT |
| determinant gives signature-\((1,3)\) quadratic form | EXACT |
| positive Hermitian cone equals future cone of determinant form | STANDARD / EXACT ALGEBRA |
| pure states lie on determinant-zero cone | EXACT |
| full-rank mixed states lie in determinant-positive cone | EXACT |
| differences of positive Hermitian carriers span all `Herm(2)` | STANDARD / EXACT |
| local Hermitian carrier dimension is 4 | EXACT |
| IDT elapsed scalar is the physical event trace scale | OPEN PHYSICAL BINDING |
| resulting carrier is physical spacetime | CONDITIONAL on the binding above |

No canon promotion is performed by this candidate.
