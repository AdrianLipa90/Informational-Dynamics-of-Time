# 01AI — Horizon Spin-1/2 Thermal Antiperiodicity

Status: `EXACT_NEAR_HORIZON_SPIN_CONNECTION / EXACT_2PI_FRAME_HOLONOMY / SPIN_HALF_MINUS_SIGN_PASS / THERMAL_FERMION_COMPATIBILITY_PASS`

01AI refines 01AH by deriving the horizon one-form from the torsion-free spin connection of the Euclidean near-horizon plane and evaluating the same primitive `2π` winding in vector and spin-`1/2` representations.

## 1. Euclidean horizon coframe

Use the local two-dimensional near-horizon geometry

\[
 ds_E^2=d\rho^2+\rho^2d\Theta_H^2,
 \qquad
 \Theta_H=\kappa_H\tau_E.
\]

Choose the orthonormal coframe

\[
\boxed{
e^{\hat\rho}=d\rho,
\qquad
e^{\hat\theta}=\rho\,d\Theta_H.
}
\]

The torsion-free Cartan equation

\[
 de^{\hat a}+\omega^{\hat a}{}_{\hat b}\wedge e^{\hat b}=0
\]

gives, for the chosen orientation,

\[
\boxed{
\omega^{\hat\theta}{}_{\hat\rho}=d\Theta_H
=\kappa_Hd\tau_E.
}
\]

Thus the horizon one-form used in 01AH is the local Levi-Civita spin connection of the Euclidean polar frame.

## 2. Primitive frame holonomy

On the smooth thermal circle

\[
\beta_H=\frac{2\pi}{\kappa_H},
\]

one has

\[
\boxed{
\oint_{C_H}\omega^{\hat\theta}{}_{\hat\rho}
=\int_0^{\beta_H}\kappa_Hd\tau_E
=2\pi.
}
\]

The orthonormal frame therefore performs one primitive Euler rotation around the horizon cap.

## 3. Vector/bosonic representation

For integer-spin phase weight `m in Z`, the primitive rotation gives

\[
W_m=e^{i2\pi m}=1.
\]

In particular the scalar/vector thermal sector is periodic around the primitive Euclidean circle.

## 4. Spin-1/2 representation

For a spin-`1/2` representation, a spatial-frame rotation through angle `Theta` acts with half-angle phase. The primitive horizon winding therefore gives

\[
\boxed{
W_{1/2}
=e^{i(2\pi)/2}
=e^{i\pi}
=-1.
}
\]

Hence after one thermal-circle traversal,

\[
\boxed{
\psi(\tau_E+\beta_H)=-\psi(\tau_E).
}
\]

This is the fermionic antiperiodic thermal boundary condition.

## 5. Matsubara consequence

For a mode `exp(-i omega tau_E)`, periodicity gives

\[
\omega_n^{B}=\frac{2\pi n}{\beta_H}=n\kappa_H,
\]

while the spin-`1/2` minus sign gives

\[
\boxed{
\omega_n^{F}
=\frac{(2n+1)\pi}{\beta_H}
=\left(n+\frac12\right)\kappa_H.
}
\]

Thus the same horizon Euler winding distinguishes integer-spin and half-integer-spin thermal sectors by representation theory.

## 6. Relation to Aharonov–Bohm / Euler closure

01AH established the closed-loop `U(1)` structural map

\[
(q/\hbar)A\leftrightarrow\omega_H.
\]

01AI identifies

\[
\boxed{\omega_H=\omega^{\hat\theta}{}_{\hat\rho}}
\]

in the Euclidean near-horizon coframe. The AB-side and horizon-side connections remain separately typed while the common holonomy operator

\[
W=\exp(i\oint\omega)
\]

provides the relational isomorphism.

## 7. Evidential boundary

Exact at 01AI:

- torsion-free near-horizon spin connection;
- primitive `2π` frame holonomy;
- integer-spin periodic factor `+1`;
- spin-`1/2` factor `-1`;
- corresponding bosonic and fermionic Matsubara spacing.

The microscopic Hawking-emission mechanism remains a downstream physical binding. 01AI supplies its exact thermal spin/phase boundary condition.
