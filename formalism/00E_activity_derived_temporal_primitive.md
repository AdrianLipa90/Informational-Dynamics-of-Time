# 00E — Activity-Derived Temporal Primitive

Status: `FORMAL_CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This layer derives an intrinsic temporal measure from the admitted relational transition kinetics. Its inputs are an ordered relational path, the positive transition weights of 00C and the directed affinity of 00B. The derivation also identifies the unique local extensive orientation-even temporal density up to one positive clock-scale factor.

## 1. Ordered relational path

Let

\[
\Gamma:\lambda\mapsto s(\lambda)
\]

be an admitted relational path, with \(\lambda\) any strictly increasing label of transition order.

For an active pair \(a\leftrightarrow b\), 00C supplies

\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2},
\qquad
M_{ab}>0.
\]

Write

\[
W_+:=W_{a\to b},
\qquad
W_-:=W_{b\to a}.
\]

The symmetric activity and directed current are

\[
\boxed{
\mathfrak a
=W_++W_-
=2M\cosh(A/2)>0,
}
\]

\[
\boxed{
\mathfrak j
=W_+-W_-
=2M\sinh(A/2).
}
\]

## 2. Uniqueness of the local extensive duration density

Let a candidate local temporal density be a continuous map

\[
F:\mathbb R_{>0}^2\to\mathbb R_{>0},
\qquad
(W_+,W_-)\mapsto F(W_+,W_-).
\]

Impose the following structural requirements.

### 2.1 Independent-channel extensivity

For two independent transition channels on the same ordered patch, their directed traffic adds componentwise. The temporal density is required to add with that traffic:

\[
\boxed{
F(u_++v_+,u_-+v_-)
=F(u_+,u_-)+F(v_+,v_-).
}
\]

Continuity together with additivity on the positive cone gives a linear form

\[
F(W_+,W_-)=c_+W_+ + c_-W_-.
\]

### 2.2 Orientation-even duration

Reversing the local edge exchanges the two directed weights. Duration is invariant under this exchange:

\[
\boxed{F(W_+,W_-)=F(W_-,W_+).}
\]

Therefore

\[
c_+=c_-=:C.
\]

Positivity gives \(C>0\), and hence

\[
\boxed{
F(W_+,W_-)=C(W_++W_-)=C\mathfrak a.
}
\]

Thus the symmetric transition activity is the unique continuous local temporal density satisfying independent-channel extensivity and orientation-evenness, up to one positive multiplicative scale.

### 2.3 Reparameterization covariance

Treat directed transition weights as one-densities with respect to the ordering label. Under an increasing relabeling

\[
\lambda'=f(\lambda),
\qquad
\frac{d\lambda'}{d\lambda}>0,
\]

\[
W'_\pm
=W_\pm\frac{d\lambda}{d\lambda'}.
\]

The derived density therefore transforms as

\[
F'
=F\frac{d\lambda}{d\lambda'}.
\]

Hence

\[
\boxed{F'd\lambda'=F d\lambda.}
\]

The remaining constant \(C\) is a clock-unit scale. Intrinsic activity units choose \(C=1\); physical clock calibration supplies the later conversion factor.

## 3. Intrinsic temporal measure

With the intrinsic choice \(C=1\), define

\[
\boxed{
d\Theta=\mathfrak a\,d\lambda.}
\]

Then

\[
\boxed{d\Theta'=d\Theta.}
\]

For an interval of relational history \(\Gamma_{12}\),

\[
\boxed{
\Theta[\Gamma_{12}]
=\int_{\Gamma_{12}}\mathfrak a\,d\lambda.
}
\]

Positivity of \(\mathfrak a\) gives positive accumulation on every active interval. Integration gives exact path concatenation,

\[
\boxed{
\Theta[\Gamma_{13}]
=\Theta[\Gamma_{12}]
+\Theta[\Gamma_{23}].
}
\]

The intrinsic temporal coordinate is therefore an additive measure of realized relational activity.

## 4. Temporal orientation

Define the normalized directed coordinate

\[
\boxed{
\chi
=\frac{\mathfrak j}{\mathfrak a}
=\tanh(A/2),
\qquad -1<\chi<1.
}
\]

Under edge-orientation reversal

\[
A\mapsto-A,
\]

the temporal coordinates transform as

\[
\boxed{d\Theta\mapsto d\Theta,}
\qquad
\boxed{\chi\mapsto-\chi.}
\]

At the symmetric point \(A=0\),

\[
\boxed{
\mathfrak a=2M>0,
\qquad
\chi=0.
}
\]

Thus the duration measure remains active at the orientation-symmetric point. Duration and arrow/orientation are distinct coordinates of the temporal primitive.

## 5. Shannon affinity form

00B supplies the transition affinity in bits,

\[
\sigma
=\log_2\frac{W_+}{W_-},
\qquad
A=(\ln2)\sigma.
\]

Therefore

\[
\boxed{
d\Theta
=2M\cosh\!\left(\frac{\ln2}{2}\sigma\right)d\lambda,
}
\]

\[
\boxed{
\chi
=\tanh\!\left(\frac{\ln2}{2}\sigma\right).
}
\]

Using the 00C mobility,

\[
M_{ab}
=
\frac{\sqrt{\rho_R(a)\rho_R(b)}}
{\tfrac12[\eta_R(a)+\eta_R(b)]},
\]

the duration density becomes

\[
\boxed{
\frac{d\Theta}{d\lambda}
=
2\frac{\sqrt{\rho_R(a)\rho_R(b)}}
{\tfrac12[\eta_R(a)+\eta_R(b)]}
\cosh\!\left(\frac{\ln2}{2}\sigma_{ab}\right).
}
\]

This gives the direct relational-information map

\[
\boxed{
(\rho_R,\eta_R,\sigma)
\longmapsto
(d\Theta,\chi).
}
\]

The fixed information-phase normalization

\[
\boxed{
\kappa=\frac{\ln2}{24\pi}
}
\]

governs the phase-link sector, while \(d\Theta\) is the derived activity measure used for clock comparison.

## 6. Relational lapse as a derived ratio

For two active subsystems \(x\) and \(r\) referred to the same ordering label,

\[
d\Theta_x=\mathfrak a_x d\lambda,
\qquad
d\Theta_r=\mathfrak a_r d\lambda.
\]

Their intrinsic clock ratio is

\[
\boxed{
N_R(x|r)
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

The common ordering label cancels. For three clocks,

\[
\boxed{
N_{x|s}=N_{x|r}N_{r|s}.
}
\]

After calibration of the reference clock by \(T_r>0\),

\[
\boxed{dt=T_r\,d\Theta_r,}
\]

the local calibrated elapsed interval follows as

\[
\boxed{
d\hat\tau_x
=T_r\,d\Theta_x
=N_R(x|r)\,dt.
}
\]

The multiplicative scale left by the uniqueness theorem is therefore fixed at the clock-calibration layer.

## 7. Temporal primitive

The derived local temporal primitive is the typed pair

\[
\boxed{
\mathbb T_{ab}
=\left(d\Theta_{ab},\chi_{ab}\right).
}
\]

Its components carry distinct roles:

```text
ordering relation      : lambda labels admitted precedence
directed traffic       : W_plus, W_minus
unique duration density: activity = W_plus + W_minus [up to clock scale]
intrinsic duration     : dTheta = activity d_lambda
orientation coordinate : chi = current/activity
clock comparison       : N_R = dTheta_x/dTheta_ref
clock calibration      : dt = T_ref dTheta_ref
calibrated local time  : d tau_hat = N_R dt
phase topology         : kappa-weighted Shannon/geometric link
```

The derivational sequence is

\[
\boxed{
\text{RELATIONAL TRANSITIONS}
\to
\text{EXTENSIVE EVEN ACTIVITY MEASURE}
\to
(d\Theta,\chi)
\to
N_R
\to
\text{CALIBRATED ELAPSED TIME}.
}
\]

## 8. GREMLIN candidate audit contract

GREMLIN remains candidate-only. The relational-isomorphism candidate submitted by this gate is

```text
independent transition superposition -> extensive path density
orientation exchange                 -> even duration / odd direction
positive symmetric traffic           -> intrinsic duration measure
antisymmetric traffic                -> orientation coordinate
ratio of duration measures           -> relational lapse
reference calibration                -> elapsed clock reading
```

Promotion requires algebraic tests for positivity, independent-channel additivity, reparameterization invariance, orientation reversal, Shannon-affinity consistency, clock-ratio composition and fail-closed domain behavior.

Reference implementation: `src/idt/temporal_primitive_activity.py`.
Reference tests: `tests/reference/test_temporal_primitive_activity.py`.
Validation receipt: `validation/TEMPORAL_PRIMITIVE_ACTIVITY_V0_1.json`.
