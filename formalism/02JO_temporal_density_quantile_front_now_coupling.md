# 02JO — Temporal Density Quantile Front and NOW Coupling

Status: `FORMAL_CANDIDATE / THRESHOLD_FREE_MASS_FRONT_GATE`

This gate starts from the admitted continuum Temporal Wave continuity law and derives material-front kinematics without introducing an amplitude activation threshold. The logical NOW frontier remains carried by the realized-event order; this layer supplies a typed material coordinate that can be bound to that frontier by a downstream realization map.

## 1. Continuum Temporal Wave input

The preceding continuum gate supplies

\[
\boxed{\partial_\Theta\rho+\partial_xJ=0,}
\]

with

\[
\rho=|\Psi|^2>0,
\qquad
J=2M\rho q,
\qquad
q=\partial_x\alpha-A.
\]

On a finite interval \([x_L,x_R]\), define total temporal-wave mass

\[
\boxed{M_T=\int_{x_L}^{x_R}\rho(x,\Theta)\,dx.}
\]

For zero boundary flux, \(M_T\) is conserved exactly.

## 2. Cumulative mass coordinate

Define the normalized cumulative mass

\[
\boxed{
C(x,\Theta)
=\frac{1}{M_T}
\int_{x_L}^{x}\rho(y,\Theta)\,dy.
}
\]

For conserved \(M_T\), continuity gives

\[
\partial_\Theta C
=\frac{J(x_L,\Theta)-J(x,\Theta)}{M_T}.
\]

For the zero-left-flux reference condition,

\[
\boxed{
\partial_\Theta C(x,\Theta)
=-\frac{J(x,\Theta)}{M_T}.
}
\]

No pointwise amplitude threshold enters this coordinate.

## 3. Quantile front

For a fixed mass fraction

\[
q_m\in(0,1),
\]

define the material quantile front \(X_{q_m}(\Theta)\) by

\[
\boxed{C(X_{q_m}(\Theta),\Theta)=q_m.}
\]

When \(\rho(X_{q_m},\Theta)>0\), implicit differentiation gives

\[
0
=\partial_\Theta C
+\partial_xC\,\frac{dX_{q_m}}{d\Theta}.
\]

Since

\[
\partial_xC=\frac{\rho}{M_T},
\]

the exact kinematic law is

\[
\boxed{
\frac{dX_{q_m}}{d\Theta}
=\frac{J(X_{q_m},\Theta)-J(x_L,\Theta)}
{\rho(X_{q_m},\Theta)}.
}
\]

Under zero left-boundary flux,

\[
\boxed{
\frac{dX_{q_m}}{d\Theta}
=\frac{J}{\rho}\Big|_{X_{q_m}}
=u(X_{q_m},\Theta).
}
\]

Thus every admitted mass quantile is transported by the local Madelung velocity.

## 4. Symmetric half-mass marker

The TIR first-distinction theorem supplies the unique exchange-symmetric probability split \(1/2\). The corresponding temporal-wave mass marker is

\[
\boxed{X_{1/2}:\ C(X_{1/2},\Theta)=\frac12.}
\]

It obeys

\[
\boxed{
\frac{dX_{1/2}}{d\Theta}
=u(X_{1/2},\Theta)
}
\]

under the zero-flux reference condition.

This gives a typed crosslink

\[
\boxed{
\text{TIR symmetric }\frac12
\longrightarrow
\text{equal-mass Temporal Wave marker }X_{1/2}.
}
\]

The full family \(X_q\) remains available for shape-sensitive diagnostics.

## 5. Discrete cumulative transport

On the finite half-frame path, let \(p_n=|a_n|^2\) and let \(j_{n+1/2}\) be the exact gauge-covariant edge current from 02JL. The vertex continuity law is

\[
\dot p_n=j_{n-1/2}-j_{n+1/2}.
\]

For the cumulative mass through vertex \(m\),

\[
C_m=\sum_{n=0}^{m}p_n,
\]

telescoping gives

\[
\boxed{
\dot C_m
=j_{-1/2}-j_{m+1/2}.
}
\]

For the closed left boundary,

\[
\boxed{\dot C_m=-j_{m+1/2}.}
\]

Hence the same threshold-free cumulative-front construction exists before the continuum limit.

## 6. Center and width kinematics

For zero boundary flux define

\[
\bar x
=\frac1{M_T}\int x\rho\,dx.
\]

Integration by parts gives

\[
\boxed{
\frac{d\bar x}{d\Theta}
=\frac1{M_T}\int J\,dx
=\frac1{M_T}\int \rho u\,dx.
}
\]

For the variance

\[
\sigma_x^2
=\frac1{M_T}\int(x-\bar x)^2\rho\,dx,
\]

we obtain

\[
\boxed{
\frac{d\sigma_x^2}{d\Theta}
=\frac{2}{M_T}\int(x-\bar x)J\,dx.
}
\]

The quantile family, center and width therefore provide complementary threshold-free kinematic observables of Temporal Wave transport and fuzziness.

## 7. Typed relation to logical NOW

The logical NOW gate remains the maximal realized-event frontier

\[
\boxed{\mathcal N=\operatorname{Max}_{<_T}(D_q).}
\]

This layer exports material markers \(X_q(\Theta)\). A NOW/material identification is admitted only through an explicit realization-binding map

\[
\boxed{
\mathfrak B_{\rm NOW}:\mathcal N\to\{X_q\}.
}
\]

For a serial history with unique maximal realized event \(e_N\), a candidate binding has the form

\[
\boxed{x(e_N)=X_{q_*}(\Theta_N).}
\]

The symmetric candidate is \(q_*=1/2\). Other quantiles remain available as falsification controls.

For concurrent histories, \(\mathcal N\) is an antichain and the binding is branch-indexed,

\[
\boxed{e_{N,b}\mapsto X_{q_*,b}.}
\]

Thus the material wave marker and the logical realized-event frontier remain separately typed until the realization-binding gate is tested.

## 8. Immediate tests

Reference gates require:

- exact cumulative continuity from finite edge currents;
- quantile velocity equals local \(J/\rho\) in the zero-flux continuum reference;
- translating density/current control transports all tested quantiles at the declared velocity;
- \(X_{1/2}\) splits total mass equally;
- barycenter-rate identity;
- variance-rate identity;
- quantile coordinate invariance under common positive density rescaling;
- fail-closed behavior for non-positive local quantile density, non-monotone grids and invalid mass fractions.

Reference implementation: `src/idt/temporal_density_quantile_front.py`.
Reference tests: `tests/reference/test_temporal_density_quantile_front.py`.
Validation receipt: `validation/TEMPORAL_DENSITY_QUANTILE_FRONT_V0_1.json`.
