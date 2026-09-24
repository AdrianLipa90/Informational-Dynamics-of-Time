# IDT Temporal Trace / Physical Clock Calibration Closure v0.1

Status: CANDIDATE_ONLY / EXACT_AFTER_REFERENCE_CLOCK_CALIBRATION / SINGLE_POSITIVE_SCALE_FREEDOM / LOCAL_LAPSE_PROPAGATION_EXACT / UNIVERSAL_PHYSICAL_ADEQUACY_OPEN / CANON_ALLOWED_FALSE

Date: 2026-09-19

## 1. Purpose

IDT already supplies three ingredients:

1. a positive additive intrinsic elapsed measure;
2. a physical reference-clock calibration protocol;
3. an exact uniqueness theorem stating that the only positive extensive SU(2)-invariant scalar on the primitive Hermitian carrier is the trace, up to one positive multiplicative constant.

This note closes the remaining algebraic/calibration seam between these ingredients.

It does not claim that a particular physical clock realization is universally adequate in every regime. It proves that once one admitted reference clock fixes the unit scale, no additional functional freedom remains in the temporal trace binding.

## 2. Intrinsic elapsed measure

IDT 00E supplies

\[
d\Theta=\mathfrak a\,d\lambda,
\qquad
\mathfrak a>0,
\]

with additive elapsed composition.

For a local subsystem x and reference subsystem r,

\[
d\Theta_x=\mathfrak a_x\,d\lambda,
\qquad
d\Theta_r=\mathfrak a_r\,d\lambda.
\]

The exact relational lapse is

\[
\boxed{
N_R(x|r)
=
\frac{d\Theta_x}{d\Theta_r}
=
\frac{\mathfrak a_x}{\mathfrak a_r}
>0.
}
\]

## 3. Physical reference-clock calibration

IDT 05C calibrates the reference measure to a physical clock coordinate t by

\[
\boxed{
dt=T_r\,d\Theta_r,
\qquad
T_r>0.
}
\]

The local calibrated elapsed interval is then

\[
\boxed{
d\hat\tau_x=N_R(x|r)\,dt.
}
\]

The corresponding length-valued temporal one-form exported to the relativistic bridge is

\[
\boxed{
\Theta_R
=
N_R c\,dt
=
c\,d\hat\tau_x.
}
\]

Define the calibrated local event-length scale

\[
\boxed{
d\ell_x:=\Theta_R.
}
\]

Thus

\[
\boxed{
d\ell_x
=
N_R c\,dt
=
c\,d\hat\tau_x
>0.
}
\]

No Hermitian carrier has been used yet.

## 4. Unique invariant extensive scalar on Herm(2)

IDT Temporal Trace Uniqueness v0.6 proves:

if

\[
T:\operatorname{Herm}(2)\to\mathbb R
\]

is real-linear, additive/extensive, invariant under common SU(2) spatial-frame conjugation, and positive on nonzero positive-Hermitian carriers, then

\[
\boxed{
T(X)=\alpha\,\operatorname{Tr}X,
\qquad
\alpha>0.
}
\]

Therefore the carrier has one and only one admissible temporal scalar class, up to one positive calibration constant.

## 5. Reference calibration fixes the remaining constant

At a selected reference calibration event, require the Hermitian temporal readout to equal the calibrated clock length:

\[
T(X_\star)=d\ell_\star.
\]

Using

\[
T(X)=\alpha\,\operatorname{Tr}X,
\]

this fixes

\[
\boxed{
\alpha
=
\frac{d\ell_\star}{\operatorname{Tr}X_\star}.
}
\]

Equivalently, one may choose carrier units so that

\[
\boxed{\alpha=1.}
\]

Then

\[
\boxed{
\operatorname{Tr}X_\star=d\ell_\star.
}
\]

Because alpha is one global calibration constant rather than a function of state, position or orientation, no further temporal-scalar freedom remains.

## 6. Local propagation through the relational lapse

For every local clock x, 05C supplies

\[
d\ell_x=N_R(x|r)c\,dt.
\]

Use the canonical positive-Hermitian lift

\[
\boxed{
X_x=d\ell_x\,\rho_x,
}
\]

where

\[
\rho_x\succeq0,
\qquad
\operatorname{Tr}\rho_x=1.
\]

Then automatically

\[
\boxed{
\operatorname{Tr}X_x=d\ell_x
=
N_R(x|r)c\,dt
=
c\,d\hat\tau_x.
}
\]

Thus the reference-clock calibration propagates locally through the exact lapse field without introducing a second temporal coordinate or a state-dependent calibration function.

## 7. Reparameterization invariance

The lapse ratio is invariant under a common increasing reparameterization of the underlying IDT parameter.

Therefore

\[
N_R'=N_R.
\]

Once the reference physical clock coordinate t is calibrated, the local event-length scale

\[
d\ell_x=N_R c\,dt
\]

is independent of the arbitrary internal parameterization used to compute the activity ratio.

The trace binding inherits that invariance:

\[
\boxed{
\operatorname{Tr}X_x=N_R c\,dt.
}
\]

## 8. Clock-network consistency

IDT 05E proves that, on a connected clock graph satisfying cycle closure,

\[
N_{x|y}
=
\frac{\mathfrak a_x}{\mathfrak a_y}
\]

arises from one positive global rate potential, unique up to common positive scale.

Therefore the same single reference calibration propagates consistently around every closed clock cycle.

There is no independent holonomy in the scalar calibration when

\[
\prod_{e\in C}N_e=1.
\]

Hence the trace-scale binding is globally path-independent on every admitted cycle-closed clock network.

## 9. Composition

For sequential local elapsed packets,

\[
d\ell_1=c\,d\hat\tau_1,
\qquad
d\ell_2=c\,d\hat\tau_2,
\]

additivity gives

\[
\boxed{
d\ell_{12}=d\ell_1+d\ell_2.
}
\]

For the Hermitian packets

\[
X_1=d\ell_1\rho_1,
\qquad
X_2=d\ell_2\rho_2,
\]

the positive elapsed-state cone theorem gives

\[
X_1+X_2
=
(d\ell_1+d\ell_2)\rho_{12},
\]

with

\[
\rho_{12}
=
\frac{
d\ell_1\rho_1+d\ell_2\rho_2
}{
d\ell_1+d\ell_2
}.
\]

Taking the trace,

\[
\boxed{
\operatorname{Tr}(X_1+X_2)
=
d\ell_1+d\ell_2
=
c(d\hat\tau_1+d\hat\tau_2).
}
\]

Thus clock additivity and Hermitian-cone additivity are the same scalar composition law after one reference calibration.

## 10. Consequence for the 3+1 causal carrier

With

\[
X
=
d\ell\,\rho
=
\frac{d\ell}{2}
\left(
I+\mathbf r\cdot\boldsymbol\sigma
\right),
\]

one has

\[
x^0=\frac{d\ell}{2}
=
\frac{c\,d\hat\tau}{2},
\]

and

\[
\mathbf x
=
\frac{d\ell}{2}\mathbf r.
\]

Therefore

\[
\boxed{
\det X
=
\frac{c^2d\hat\tau^2}{4}
\left(
1-|\mathbf r|^2
\right).
}
\]

The scalar temporal direction is now the calibrated physical-clock length coordinate of the already-derived Hermitian causal carrier.

No second time direction is introduced.

## 11. What is and is not closed

Closed exactly after one declared reference-clock calibration:

- temporal scalar class is trace up to one positive constant;
- reference calibration fixes that constant;
- local lapse propagates the calibration;
- cycle-closed clock networks preserve path independence;
- calibrated local event scale satisfies
  \[
  \operatorname{Tr}X=c\,d\hat\tau;
  \]
- composition of clock intervals equals composition of trace scales.

Still physical / empirical:

- whether the selected reference clock is an adequate physical realization in the target regime;
- whether every physical local forward event displacement is represented by the admitted elapsed-state Hermitian packet;
- global spacetime / Einstein identification downstream.

## 12. Main closure statement

Under the already-declared IDT 05C reference-clock calibration,

\[
dt=T_r\,d\Theta_r,
\]

and the exact relational lapse,

\[
d\hat\tau_x=N_R(x|r)\,dt,
\]

the unique invariant-extensive temporal scalar on the primitive Hermitian carrier can be calibrated once so that

\[
\boxed{
\operatorname{Tr}X_x
=
c\,d\hat\tau_x
=
N_R(x|r)c\,dt.
}
\]

The remaining freedom is only the conventional positive choice of physical units/reference normalization.

There is no additional dynamical or functional temporal degree of freedom hidden in the trace binding.
