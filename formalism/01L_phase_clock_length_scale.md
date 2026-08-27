# 01L — Phase–Clock Length Scale

Status: `EXACT_PHASE_CLOCK_LENGTH_IDENTITY / RELATIONAL_AREA_BINDING_CANDIDATE`

## 1. Purpose

This gate supplies the length-typed carrier required by 01K using the already admitted temporal phase and clock-calibration structure. The construction is local and uses only the phase rate, the empirical clock map and the universal conversion speed `c`.

Let the internal elapsed activity be `tau_int`, let the measured clock coordinate be monotone,

\[
t=t(\tau_{\rm int}),
\qquad
\frac{dt}{d\tau_{\rm int}}>0,
\]

and let the local relational phase be

\[
\varphi=\varphi(\tau_{\rm int}).
\]

Define the calibrated angular phase rate

\[
\boxed{
\omega_t
:=\frac{d\varphi}{dt}
=\frac{d\varphi/d\tau_{\rm int}}{dt/d\tau_{\rm int}}.
}
\]

The admissible local patch for the present scale map satisfies

\[
|\omega_t|>0.
\]

## 2. Length per radian

Because phase is dimensionless and

\[
[\omega_t]=T^{-1},
\qquad
[c]=LT^{-1},
\]

the quantity

\[
\boxed{
\ell_\varphi
:=c\left|\frac{dt}{d\varphi}\right|
=\frac{c}{|\omega_t|}
}
\]

has exact dimension

\[
\boxed{[\ell_\varphi]=L.}
\]

Equivalently in internal-time variables,

\[
\boxed{
\ell_\varphi
=c\,
\frac{dt/d\tau_{\rm int}}
{|d\varphi/d\tau_{\rm int}|}.
}
\]

Thus the clock-calibrated phase flow supplies a local physical length per radian.

## 3. Energy representation

Using the admitted phase-energy calibration

\[
E=\hbar|\omega_t|,
\]

the same scale is

\[
\boxed{
\ell_\varphi=\frac{\hbar c}{E}.
}
\]

This is an exact re-expression of the phase-clock scale once the energy calibration is admitted.

The associated projective and spinorial cycle lengths are

\[
\boxed{
L_{2\pi}=2\pi\ell_\varphi
=\frac{hc}{E},
}
\]

\[
\boxed{
L_{4\pi}=4\pi\ell_\varphi
=\frac{2hc}{E},
}
\]

and therefore

\[
\boxed{
\frac{L_{2\pi}}{L_{4\pi}}=\frac12.
}
\]

The `2pi` projective/Berry cycle and `4pi` spinorial cycle remain separately typed.

## 4. Clock-coordinate covariance

Let `t -> t'(t)` be a monotone clock reparameterization. The reported angular rate transforms as

\[
\omega_{t'}
=\omega_t\frac{dt}{dt'},
\]

while the physical conversion one-form is

\[
c\,dt.
\]

The length associated with a fixed physical phase increment is

\[
\boxed{
 d\ell_\varphi^{\rm phys}
 =c|dt|
 =\ell_\varphi|d\varphi|.
}
\]

Hence the local scalar `ell_phi` is understood relative to the admitted physical clock calibration, while the interval assigned to a fixed phase increment is coordinate independent.

## 5. Dynamic scale law

For a smooth positive phase rate magnitude,

\[
\ell_\varphi=\frac{c}{|\omega_t|},
\]

so along internal elapsed activity

\[
\boxed{
\frac{1}{\ell_\varphi}
\frac{d\ell_\varphi}{d\tau_{\rm int}}
=-
\frac{1}{|\omega_t|}
\frac{d|\omega_t|}{d\tau_{\rm int}}.
}
\]

In the energy representation,

\[
\boxed{
\frac{1}{\ell_\varphi}
\frac{d\ell_\varphi}{d\tau_{\rm int}}
=-
\frac{1}{E}
\frac{dE}{d\tau_{\rm int}}.
}
\]

The relational length scale therefore evolves inversely with the calibrated local phase/energy scale.

## 6. Export to TIR area calibration

IDT exports the exact length carrier

```text
calibrated_phase_rate       = omega_t = (dphi/dtau_int)/(dt/dtau_int)
phase_length_per_radian     = ell_phi = c / |omega_t|
energy_form                 = ell_phi = hbar c / E
projective_cycle_length     = L_2pi = 2 pi ell_phi
spinorial_cycle_length      = L_4pi = 4 pi ell_phi
cycle_ratio                 = L_2pi / L_4pi = 1/2
```

TIR may use `ell_phi^2` to physicalize a dimensionless Fubini--Study area element. RFC owns the downstream curvature and `Lambda0` binding.

## 7. Evidence boundary

Exact at this gate:

- phase-clock chain rule;
- `ell_phi = c/|omega_t|` dimensional identity;
- `ell_phi = hbar c/E` under the admitted phase-energy calibration;
- `2pi/4pi` cycle-length ratio;
- inverse phase-rate scale evolution.

Downstream gates:

- selection of the projective/polyhedral area carrier receiving `ell_phi^2`;
- treatment of cells with spatially varying `omega_t`;
- physical field binding in RFC;
- empirical comparison of the resulting local scale.