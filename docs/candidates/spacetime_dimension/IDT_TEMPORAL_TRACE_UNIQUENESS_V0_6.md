# IDT Temporal Scalar → Hermitian Trace Uniqueness v0.6

Status: **CANDIDATE / EXACT INVARIANT-EXTENSIVE FUNCTIONAL THEOREM**

## 1. Objective

The preceding temporal-trace candidate established the unique recovery lift

\[
X=\ell\rho,
\qquad
\operatorname{Tr}\rho=1,
\qquad
\operatorname{Tr}X=\ell.
\]

The remaining question was whether use of the trace as the temporal scalar is an arbitrary placement.

This gate answers the algebraic uniqueness part.

## 2. Admitted primitive carrier

Let the local event carrier be the real vector space

\[
V=\operatorname{Herm}(2)
=
\mathbb RI\oplus\operatorname{Herm}_0(2).
\]

Its positive cone is

\[
V_+=\operatorname{Herm}_+(2).
\]

Spatial frame changes act by

\[
X\mapsto UXU^\dagger,
\qquad
U\in SU(2).
\]

## 3. Temporal-scalar requirements

Let

\[
T:V\to\mathbb R
\]

be a real linear functional representing the local temporal magnitude after extensive positive-cone addition has been extended to the real span.

Require:

1. **additivity/extensivity**
   \[
   T(X+Y)=T(X)+T(Y);
   \]
2. **spatial-frame invariance**
   \[
   T(UXU^\dagger)=T(X)
   \quad\forall U\in SU(2);
   \]
3. **positive temporal orientation**
   \[
   X\succeq0,\ X\ne0
   \Longrightarrow
   T(X)>0
   \]
   after choosing the positive clock orientation.

These are the matrix-carrier analogues of the IDT 00E structural requirements: continuous extensive duration magnitude, orientation-even pace, and a later positive calibration scale.

## 4. Uniqueness theorem

Write

\[
X=x^0I+\mathbf x\cdot\boldsymbol\sigma.
\]

Every real linear functional has the form

\[
T(X)=a_0x^0+\mathbf a\cdot\mathbf x.
\]

Under \(SU(2)\) conjugation, \(x^0\) is invariant and the spatial coefficient vector transforms by the full \(SO(3)\) rotation action:

\[
\mathbf x\mapsto R\mathbf x.
\]

Therefore invariance requires

\[
\mathbf a\cdot R\mathbf x
=
\mathbf a\cdot\mathbf x
\qquad
\forall R\in SO(3),\ \forall\mathbf x.
\]

The only vector fixed by every rotation is the zero vector, hence

\[
\boxed{\mathbf a=0.}
\]

Thus

\[
T(X)=a_0x^0.
\]

Since

\[
\operatorname{Tr}X=2x^0,
\]

one obtains

\[
\boxed{
T(X)=\alpha\,\operatorname{Tr}X
}
\]

for one real constant \(\alpha=a_0/2\).

Positivity on nonzero positive-Hermitian carriers requires

\[
\boxed{\alpha>0.}
\]

Therefore the trace is the unique positive extensive \(SU(2)\)-invariant scalar functional on the primitive Hermitian carrier, up to the single positive clock calibration constant.

## 5. Relation to IDT 00E

IDT 00E independently proves that the local orientation-even extensive duration density is unique up to one positive multiplicative scale:

\[
F(W_+,W_-)=C(W_++W_-)=C\mathfrak a.
\]

The Hermitian-carrier theorem proves the corresponding uniqueness statement after the relational state is lifted to the primitive two-level observable carrier:

\[
\boxed{
\text{positive extensive rotational scalar}
\Longrightarrow
\text{trace, up to calibration}.
}
\]

Thus the temporal trace is selected by the same structural class of requirements; it is not one choice among several independent linear scalar readouts.

## 6. Calibrated binding

Let the IDT elapsed magnitude be calibrated to physical length units by

\[
\ell=c\,\hat\tau
\]

or locally

\[
d\ell=c\,d\hat\tau.
\]

The unique invariant-extensive carrier readout gives

\[
\ell
=
\alpha\,\operatorname{Tr}X.
\]

Choose the one remaining positive calibration constant so that the reference clock obeys

\[
\alpha=1
\]

in the declared carrier units. Then

\[
\boxed{
\ell=\operatorname{Tr}X.
}
\]

Changing physical units rescales \(\alpha\) but does not introduce another temporal direction.

## 7. Consequence for dimension closure

TIR supplies

\[
V_S=\operatorname{Herm}_0(2),
\qquad
\dim_{\mathbb R}V_S=3.
\]

This theorem selects the scalar complement

\[
V_T=\mathbb RI,
\qquad
\dim_{\mathbb R}V_T=1
\]

as the unique extensive rotational-scalar carrier.

Therefore

\[
\boxed{
V_T\oplus V_S
=
\operatorname{Herm}(2)
}
\]

and

\[
\boxed{
D_{\rm local\ carrier}=1+3=4.
}
\]

The trace/traceless dual theorem on the RFC candidate branch independently closes the premetric transversality of these four directions.

## 8. Scope firewall

The theorem proves uniqueness **within the primitive two-level Hermitian carrier** under the declared additive and rotational-invariance requirements.

Promotion of this carrier to physical spacetime additionally uses the TIR spatial physicalization and RFC spacetime soldering/field closure. The dimension count itself no longer requires choosing among multiple scalar directions inside `Herm(2)`: there is only the trace class up to calibration.

## 9. Executable validation

Reference implementation:

`src/idt/temporal_trace_uniqueness.py`

Reference tests:

`tests/reference/test_temporal_trace_uniqueness.py`

Local isolated result:

```text
7 passed in 0.08s
```

The symbolic coefficient constraints from three \(\pi\)-rotations give exactly

\[
\boxed{a_1=a_2=a_3=0}.
\]

No canon or `main` write is performed by this candidate.
