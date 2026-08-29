# 05F — Maximum-Entropy Positive-Rate Information Embedding

Status: `EXACT_SHANNON_MAXENT_RATE_EMBEDDING / 05E_REFINEMENT_LINEAGE_PASS / PHASE_RATE_INFORMATION_CARRIER_PASS / PHYSICAL_DWELL_LAW_OPTIONAL`

## 1. Purpose

05D introduced the exponential holding-time realization of the activity-derived clock ratio. 05E then proved that the corresponding continuous KL scalar is the refinement completion of finite 01C Shannon relative-information states and therefore has the 01K natural-log numerator type.

RF-E16 independently supplies another positive rate carrier: the gauge-covariant normal phase rate `r_n` and its directional ratio `R_s=r_n^(s)/r_0`.

05F derives a common Shannon information embedding for any positive rate coordinate without requiring the physical process itself to have an exponential dwell-time law.

## 2. Positive-rate coordinate

Let

\[
r>0.
\]

Associate to the rate the positive-time mean scale

\[
\boxed{\mu_r:=\frac1r.}
\]

Consider normalized probability densities `g(t)` on `t>=0` satisfying

\[
\int_0^\infty g(t)dt=1,
\qquad
\int_0^\infty t\,g(t)dt=\frac1r.
\]

Their differential Shannon entropy in nats is

\[
h[g]:=-\int_0^\infty g(t)\ln g(t)dt.
\]

## 3. Unique maximum-entropy representative

Define

\[
\boxed{f_r(t):=r e^{-rt},\qquad t\ge0.}
\]

For any admitted `g` with the same mean `1/r`, KL nonnegativity gives

\[
0\le D_{KL}(g\|f_r)
=\int g\ln g\,dt-\int g\ln f_r\,dt.
\]

Since

\[
\ln f_r(t)=\ln r-rt
\]

and `E_g[t]=1/r`,

\[
D_{KL}(g\|f_r)
=-h[g]-\ln r+1.
\]

Therefore

\[
\boxed{h[g]\le1-\ln r.}
\]

Equality holds exactly when `D_KL(g||f_r)=0`, hence when

\[
\boxed{g=f_r\quad\text{almost everywhere}.}
\]

Thus `f_r` is the unique maximum-Shannon-entropy positive-time representative of the rate coordinate when only normalization and mean `1/r` are retained.

Define the rate embedding

\[
\boxed{\mathfrak E:r\mapsto f_r.}
\]

This is an information-geometric representation theorem. A physical exponential waiting-time law is an additional realization, not a premise of the embedding theorem.

## 4. Scale covariance

Under common rate rescaling

\[
r\mapsto cr,
\qquad c>0,
\]

the representative satisfies

\[
\boxed{f_{cr}(t)=c f_r(ct).}
\]

Thus common rescaling changes the time unit while preserving relative rate information.

## 5. Relative information between positive rates

For two positive rates `a,b`,

\[
\begin{aligned}
\mathcal J_{rate}(a\|b)
&:=D_{KL}(f_a\|f_b)\\
&=\int_0^\infty a e^{-at}
\left[\ln\frac ab+(b-a)t\right]dt\\
&=\ln\frac ab+\frac ba-1.
\end{aligned}
\]

Hence

\[
\boxed{
\mathcal J_{rate}(a\|b)
=\Phi\!\left(\frac ba\right),
\qquad
\Phi(x)=x-1-\ln x.
}
\]

The scalar depends only on the rate ratio and is invariant under common positive rescaling:

\[
\boxed{\mathcal J_{rate}(ca\|cb)=\mathcal J_{rate}(a\|b).}
\]

05E supplies the finite-01C refinement lineage for every pair `f_a,f_b`, so `J_rate` has the completed 01C / 01K natural-log numerator type.

## 6. Recovery of the 05D activity-clock branch

For

\[
a=\mathfrak a_r,
\qquad
b=\mathfrak a_x,
\qquad
N_R=\frac{\mathfrak a_x}{\mathfrak a_r},
\]

one obtains

\[
\boxed{
\mathcal J_{rate}(\mathfrak a_r\|\mathfrak a_x)
=\Phi(N_R)
=N_R-1-\ln N_R.
}
\]

Thus 05D is the activity-clock specialization of the general positive-rate information embedding.

If the empirical dwell-time law is actually exponential, the maximum-entropy representative coincides with the physical holding-time distribution. Otherwise `f_r` remains the Shannon maximum-entropy information representative of the measured rate coordinate.

## 7. RF-E16 phase-rate specialization

RF-E16 supplies, on its admitted local directional phase sector,

\[
R_s:=\frac{r_n^{(s)}}{r_0}>0,
\qquad
x_s=R_s^{-1}=\frac{r_0}{r_n^{(s)}}.
\]

Choose the information orientation

\[
a=r_n^{(s)},
\qquad
b=r_0.
\]

Then 05F gives exactly

\[
\boxed{
\mathcal J_{phase}^{(s)}
:=\mathcal J_{rate}(r_n^{(s)}\|r_0)
=\Phi\!\left(\frac{r_0}{r_n^{(s)}}\right)
=\Phi(x_s).
}
\]

Therefore the RF-E14/RF-E16 directional information scalar has an explicit Shannon maximum-entropy positive-rate source representation. It does not require identification of the phase-rate ratio with the activity lapse `N_R`.

This closes the earlier rate-type seam:

```text
RF-E16 positive normal phase rates r_n^(s), r_0
 -> Shannon max-entropy embeddings f_{r_n}, f_{r_0}
 -> completed 01C relative information
 -> J_phase^(s)=Phi(r_0/r_n)=Phi(x_s)
 -> 01K natural-log numerator type
```

## 8. 01K information-curvature handoff

For any admitted positive relational area

\[
\mathcal A_{rel}>0,
\qquad [\mathcal A_{rel}]=L^2,
\]

define

\[
\boxed{
\Xi_{rate}(a\|b)
:=\frac{\mathcal J_{rate}(a\|b)}{\mathcal A_{rel}}.
}
\]

Then

\[
\boxed{[\Xi_{rate}]=L^{-2}.}
\]

For the RF-E16 directional phase-rate sector,

\[
\boxed{
\Xi_{phase}^{(s)}
=\frac{\Phi(x_s)}{\mathcal A_{rel}}.
}
\]

This is exactly the information-curvature form required by the RF-L3/RF-E17 action route, subject to the existing physical cell/area selection and cross-repository source pin.

## 9. Fisher metric

Parameterize the rate family by `rho=ln r`. Since `r=e^rho`,

\[
\mathcal J_{rate}(r\|r e^{d\rho})
=e^{d\rho}-1-d\rho
=\frac12(d\rho)^2+O((d\rho)^3).
\]

Thus the local Fisher line element in log-rate coordinate is

\[
\boxed{ds_F^2=(d\rho)^2.}
\]

In the rate coordinate itself,

\[
\boxed{ds_F^2=\frac{dr^2}{r^2}.}
\]

This agrees with the 05D one-dimensional Fisher metric and supplies the local Shannon-Fisher geometry used by the RFC information-curvature normalization.

## 10. Promotion boundary

05F establishes:

- unique Shannon maximum-entropy embedding of a positive rate when only its reciprocal mean scale is retained;
- exact KL/Burg potential between two embedded rates;
- common-scale invariance;
- recovery of 05D as the activity-rate specialization;
- direct RF-E16 phase-rate specialization producing `Phi(x_s)`;
- 05E finite-01C refinement lineage and 01K numerator typing;
- Fisher metric `dr^2/r^2`.

The physical exponential dwell-time law is optional at this theorem level. Physical selection of the relational area/cell, coupling into the RFC action, matter-flow domain, mass-scale calibration and observable assignment remain their existing downstream gates.

Reference implementation: `src/idt/maxent_positive_rate_embedding.py`.
Reference tests: `tests/reference/test_maxent_positive_rate_embedding.py`.
Validation receipt: `validation/MAXENT_POSITIVE_RATE_INFORMATION_EMBEDDING_V0_1.json`.
