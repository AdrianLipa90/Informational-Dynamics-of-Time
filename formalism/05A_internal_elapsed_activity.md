# 05A — System-Internal Elapsed Activity

Status: `ACTIVITY_DERIVED_ELAPSED_MEASURE_CANDIDATE`

00E supplies the intrinsic positive temporal measure directly from relational transition activity. This layer carries that measure into the Temporal Transport clock interface and introduces clock normalization only as a downstream comparison/calibration operation.

## 1. Activity-derived elapsed measure

Let \(\lambda\) be an admissible increasing ordering label. From the directed relational kinetics,

\[
W_+=Me^{A/2},
\qquad
W_-=Me^{-A/2},
\]

with \(M>0\), define

\[
\boxed{
\mathfrak a=W_++W_-=2M\cosh(A/2)>0.
}
\]

The intrinsic elapsed increment is

\[
\boxed{
d\Theta=\mathfrak a\,d\lambda.
}
\]

For an ordered discrete path,

\[
\boxed{
\Theta_N
=\sum_{n=0}^{N-1}
\mathfrak a_n\,\Delta\lambda_n,
\qquad
\Delta\lambda_n>0.
}
\]

Positive activity gives positive accumulation along every active realized interval. Concatenation of ordered intervals gives exact additivity.

## 2. Reparameterization invariance

For an increasing relabeling \(\lambda'=f(\lambda)\), transition weights transform as one-densities,

\[
W'_\pm(\lambda')
=W_\pm(\lambda)\frac{d\lambda}{d\lambda'}.
\]

Therefore

\[
\mathfrak a'(\lambda')
=\mathfrak a(\lambda)\frac{d\lambda}{d\lambda'}
\]

and

\[
\boxed{
\mathfrak a'(\lambda')d\lambda'
=\mathfrak a(\lambda)d\lambda
=d\Theta.
}
\]

The accumulated elapsed measure is therefore intrinsic to the admitted relational path and its transition activity.

## 3. Duration and orientation

The directed current is

\[
\mathfrak j=W_+-W_-=2M\sinh(A/2).
\]

The normalized orientation coordinate is

\[
\boxed{
\chi=\frac{\mathfrak j}{\mathfrak a}=\tanh(A/2).
}
\]

Under edge reversal \(A\mapsto-A\),

\[
\boxed{d\Theta\mapsto d\Theta,}
\qquad
\boxed{\chi\mapsto-\chi.}
\]

At the symmetric point \(A=0\),

\[
\mathfrak a=2M>0,
\qquad
\chi=0.
\]

Thus accumulated elapsed activity and transition orientation are carried as separate coordinates.

## 4. Density, viscosity and Shannon affinity

The relational mobility is

\[
\boxed{
M
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
}
\]

00B gives

\[
A=(\ln2)\sigma,
\]

so the elapsed density is

\[
\boxed{
\frac{d\Theta}{d\lambda}
=
2\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}
\cosh\!\left(\frac{\ln2}{2}\sigma\right).
}
\]

and the orientation coordinate is

\[
\boxed{
\chi
=\tanh\!\left(\frac{\ln2}{2}\sigma\right).
}
\]

This gives the typed map

\[
\boxed{
(\rho_R,\eta_R,\sigma)
\longmapsto
(d\Theta,\chi).
}
\]

## 5. Clock comparison and calibration

For a local subsystem \(x\) and reference subsystem \(r\) on the same ordered patch,

\[
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda.
\]

Their intrinsic relative clock rate is

\[
\boxed{
N_R(x|r)
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

A reference clock calibration supplies a conversion scale \(T_r>0\),

\[
\boxed{dt=T_r\,d\Theta_r.}
\]

The local calibrated elapsed increment is then

\[
\boxed{
d\hat\tau_x=N_R(x|r)\,dt.}
\]

The sequence is therefore

\[
\boxed{
\text{relational activity}
\to d\Theta
\to N_R
\to d\hat\tau.
}
\]

Physical clock comparison supplies the calibration of \(T_r\); the activity-derived measure and clock ratio retain their algebraic definitions upstream.
