# 02JO — Temporal-Density Material Front and NOW Crosswalk

Status: `FORMAL_CANDIDATE / MATERIAL_FRONT_KINEMATICS_AND_NOW_SELECTOR_GATE`

This gate continues 02JL–02JN. The coordinate `x` is the smooth half-frame continuum coordinate, and `Theta` is the already-derived intrinsic temporal measure. The goal is to derive front kinematics directly from the temporal-density continuity law and then state the exact additional condition required to compare such a material front with the logical NOW frontier.

## 1. Temporal-density continuity

Let

\[
\boxed{
\partial_\Theta\rho(x,\Theta)
+\partial_x\mathcal J(x,\Theta)=0,
\qquad \rho>0,
}
\]

on an admitted interval `[a,b]`. Define the total temporal-density mass

\[
\boxed{
\mathcal M(\Theta)=\int_a^b\rho(x,\Theta)\,dx.
}
\]

Integration of continuity gives

\[
\boxed{
\dot{\mathcal M}=\mathcal J(a)-\mathcal J(b).
}
\]

For zero-flux boundaries,

\[
\boxed{
\mathcal J(a)=\mathcal J(b)=0
\quad\Longrightarrow\quad
\dot{\mathcal M}=0.
}
\]

## 2. Material quantile front

For `p in (0,1)`, define the cumulative temporal density

\[
F(x,\Theta)=\int_a^x\rho(y,\Theta)\,dy
\]

and let `X_p(Theta)` be the unique regular quantile satisfying

\[
\boxed{
F(X_p,\Theta)=p\,\mathcal M.
}
\]

Assume

\[
\rho(X_p,\Theta)>0.
\]

Differentiate the quantile identity while allowing the selector `p=p(Theta)` to vary:

\[
\mathcal J(a)-\mathcal J(X_p)
+\rho(X_p)\dot X_p
=
\dot p\,\mathcal M
+p[\mathcal J(a)-\mathcal J(b)].
\]

Therefore the exact front law is

\[
\boxed{
\dot X_p
=
\frac{
\mathcal J(X_p)
-(1-p)\mathcal J(a)
-p\mathcal J(b)
+\mathcal M\dot p
}{\rho(X_p)}.
}
\]

This relation is threshold-free: it follows from cumulative mass rather than a chosen local density threshold.

## 3. No-flux material-front theorem

For zero-flux boundaries,

\[
\boxed{
\dot X_p
=\frac{\mathcal J(X_p)}{\rho(X_p)}
+\frac{\mathcal M}{\rho(X_p)}\dot p.
}
\]

Define the local temporal-density transport velocity

\[
\boxed{
u(x,\Theta):=\frac{\mathcal J(x,\Theta)}{\rho(x,\Theta)}.}
\]

For a fixed material label `p`,

\[
\boxed{
\dot p=0
\quad\Longrightarrow\quad
\dot X_p=u(X_p,\Theta).
}
\]

Using the 02JN constant-`M` sector,

\[
\boxed{
u=2Mq.}
\]

Thus every regular fixed cumulative temporal-density label is transported by the same current velocity derived from the gauge-covariant phase gradient.

## 4. NOW selector crosswalk

The logical NOW layer is already defined upstream as the maximal realized-event frontier of the relational occurrence order. The present continuum density law supplies a family of material fronts `X_p`; it does not select one member of that family.

Introduce a typed NOW localization selector only when the event-realization layer supplies a cumulative coordinate

\[
\boxed{
p_{\rm NOW}(\Theta)\in(0,1)}
\]

such that the selected continuum representative satisfies

\[
\boxed{
F(X_{\rm NOW},\Theta)
=p_{\rm NOW}(\Theta)\mathcal M.
}
\]

Then, for zero-flux boundaries,

\[
\boxed{
\dot X_{\rm NOW}
=
u(X_{\rm NOW},\Theta)
+
\frac{\mathcal M}{\rho(X_{\rm NOW},\Theta)}
\dot p_{\rm NOW}.
}
\]

The two terms have distinct typed origins:

```text
u = J/rho                 : Temporal-Wave material transport
(M/rho) p_NOW_dot         : realized-front selector drift
```

If the event-realization rule carries a fixed material label over the comparison interval,

\[
\boxed{
\dot p_{\rm NOW}=0
\quad\Longrightarrow\quad
\dot X_{\rm NOW}=u(X_{\rm NOW},\Theta).
}
\]

If the realization rule changes its cumulative label, the second term remains explicitly present.

## 5. Gauge invariance

02JL–02JN give

\[
\rho\mapsto\rho,
\qquad
\mathcal J\mapsto\mathcal J
\]

under local phase re-expression. Hence

\[
F,\quad \mathcal M,\quad X_p,\quad \nu=\mathcal J/\rho
\]

and the material-front law are gauge invariant on the admitted chart.

## 6. Exact translating-density witness

A useful exact reference family is the normalized logistic density

\[
\boxed{
\rho(x,\Theta)
=\frac{1}{s}
\frac{e^{-z}}{(1+e^{-z})^2},
\qquad
z=\frac{x-v\Theta-x_0}{s},
\qquad s>0,
}
\]

with

\[
\boxed{\mathcal J=v\rho.}
\]

Its quantile is

\[
\boxed{
X_p(\Theta)
=x_0+v\Theta+s\ln\frac{p}{1-p}.
}
\]

For fixed `p`,

\[
\boxed{
\dot X_p=v=\frac{\mathcal J}{\rho}.
}
\]

For a differentiable dynamic selector `p(Theta)`,

\[
\boxed{
\dot X_p
=v+s\frac{\dot p}{p(1-p)}.
}
\]

At the quantile,

\[
\rho(X_p)=\frac{p(1-p)}{s},
\]

so this is exactly the no-flux selector law

\[
\dot X_p
=v+\frac{\mathcal M}{\rho(X_p)}\dot p
\]

with `M=1`.

## 7. Discrete half-frame correspondence

For finite half-frame support masses `m_j>=0`, define cumulative mass

\[
C_k=\sum_{j\le k}m_j.
\]

A continuum quantile front is the smooth limit of a cumulative support label, rather than a local occupancy threshold. This is compatible with the half-frame picture

\[
|1|\,|12|\,|23|\cdots|N|,
\]

where cumulative occupation can advance through overlapping supports while the logical serial NOW remains the maximal realized support supplied by the separate realization gate.

## 8. Phase-diffusion fuzziness corollary

In the constant sector `c=M rho>0`, 02JM gives

\[
\partial_\Theta q=2\mu c\,\partial_x^2q.
\]

For an impulsive initial phase-gradient packet, the Green kernel is

\[
\boxed{
G(x,\Delta\Theta)
=
\frac{1}{\sqrt{8\pi\mu c\Delta\Theta}}
\exp\left[-\frac{x^2}{8\mu c\Delta\Theta}\right],
\qquad \Delta\Theta>0.
}
\]

Its variance is

\[
\boxed{
\sigma_q^2=4\mu c\Delta\Theta,
\qquad
\sigma_q=2\sqrt{\mu c\Delta\Theta}.
}
\]

Thus the Gaussian phase-fuzziness profile appears as a derived Green function of the admitted phase-gradient dynamics rather than as an externally chosen smoothing kernel.

## 9. Evidence boundary and next gate

This gate establishes material-front kinematics and the exact decomposition of a NOW-selected front into transport plus selector drift. The logical NOW frontier remains supplied by the realized-event order; continuity alone supplies no distinguished value of `p_NOW`.

The next gate is to bind the finite half-frame realized-support measure to a continuum selector map and test whether a stable `p_NOW` emerges in declared reference families.

Reference implementation: `src/idt/temporal_material_front.py`.
Reference tests: `tests/reference/test_temporal_material_front.py`.
Validation receipt: `validation/TEMPORAL_MATERIAL_FRONT_V0_1.json`.
