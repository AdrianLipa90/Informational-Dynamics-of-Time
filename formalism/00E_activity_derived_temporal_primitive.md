# 00E — Activity-Derived Temporal Primitive

Status: `FORMAL_CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This layer derives an intrinsic positive duration weight from admitted relational transition kinetics. Its primitive input is directed relational traffic on a composable source--target relation; a global temporal order is supplied only downstream by 00F from relational composition plus the positive activity measure.

## 1. Pretime directed relation

Let an admitted relational edge be

\[
e:a\to b.
\]

The symbols \(a\) and \(b\) are source and target labels of the relation. Their source--target typing supplies composability with other relations and does not require a metric clock coordinate.

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

Let a candidate local duration density be a continuous map

\[
F:\mathbb R_{>0}^2\to\mathbb R_{>0},
\qquad
(W_+,W_-)\mapsto F(W_+,W_-).
\]

### 2.1 Independent-channel extensivity

For two independent transition channels on the same relational carrier, require

\[
\boxed{
F(u_++v_+,u_-+v_-)
=F(u_+,u_-)+F(v_+,v_-).
}
\]

Continuity and additivity on the positive cone give

\[
F(W_+,W_-)=c_+W_+ + c_-W_-.
\]

### 2.2 Orientation-even duration

Reversing the relation exchanges the directed weights. Duration is invariant under this exchange:

\[
\boxed{F(W_+,W_-)=F(W_-,W_+).}
\]

Hence

\[
c_+=c_-=:C>0
\]

and therefore

\[
\boxed{
F(W_+,W_-)=C(W_++W_-)=C\mathfrak a.
}
\]

Thus symmetric transition activity is the unique continuous local extensive orientation-even duration density up to one positive multiplicative scale.

## 3. Local parameter covariance and edge duration

Choose any admissible increasing local parameter \(\lambda_e\) along the directed relation. This parameter is a coordinate on the relation carrier, not a physical clock.

Under

\[
\lambda'_e=f(\lambda_e),
\qquad
\frac{d\lambda'_e}{d\lambda_e}>0,
\]

the directed traffic transforms as a one-density,

\[
W'_\pm
=W_\pm\frac{d\lambda_e}{d\lambda'_e}.
\]

Hence

\[
F'
=F\frac{d\lambda_e}{d\lambda'_e}
\]

and

\[
\boxed{F'd\lambda'_e=F d\lambda_e.}
\]

In intrinsic activity units choose \(C=1\). The invariant duration weight carried by one realized relation is

\[
\boxed{
\theta(e)
:=\int_e\mathfrak a\,d\lambda_e>0.
}
\]

For an infinitesimal relation segment,

\[
\boxed{d\Theta=\mathfrak a\,d\lambda_e.}
\]

The remaining overall scale is fixed only when a physical reference clock is calibrated.

## 4. Composition additivity

For two composable realized relations

\[
e_2\circ e_1,
\qquad
t(e_1)=s(e_2),
\]

define

\[
\boxed{
\theta(e_2\circ e_1)
:=\theta(e_1)+\theta(e_2).
}
\]

For a finite composable word

\[
P_n=e_n\circ\cdots\circ e_1,
\]

\[
\boxed{
\Theta(P_n)=\sum_{k=1}^{n}\theta(e_k).
}
\]

Positivity gives

\[
\Theta(P_{n+1})-\Theta(P_n)=\theta(e_{n+1})>0.
\]

00F uses this strict growth on relation prefixes to derive temporal precedence without taking an ordered temporal path as primitive input.

## 5. Temporal orientation

Define the normalized directed coordinate

\[
\boxed{
\chi
=\frac{\mathfrak j}{\mathfrak a}
=\tanh(A/2),
\qquad -1<\chi<1.
}
\]

Under edge reversal

\[
A\mapsto-A,
\]

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

Thus duration and directional affinity are distinct coordinates.

## 6. Shannon affinity form

00B supplies

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
=2M\cosh\!\left(\frac{\ln2}{2}\sigma\right)d\lambda_e,
}
\]

\[
\boxed{
\chi
=\tanh\!\left(\frac{\ln2}{2}\sigma\right).
}
\]

Using

\[
M_{ab}
=
\frac{\sqrt{\rho_R(a)\rho_R(b)}}
{\tfrac12[\eta_R(a)+\eta_R(b)]},
\]

\[
\boxed{
\frac{d\Theta}{d\lambda_e}
=
2\frac{\sqrt{\rho_R(a)\rho_R(b)}}
{\tfrac12[\eta_R(a)+\eta_R(b)]}
\cosh\!\left(\frac{\ln2}{2}\sigma_{ab}\right).
}
\]

Hence

\[
\boxed{
(\rho_R,\eta_R,\sigma)
\longmapsto
(d\Theta,\chi).
}
\]

The fixed information-phase normalization

\[
\boxed{\kappa=\frac{\ln2}{24\pi}}
\]

continues to govern the phase-link sector.

## 7. Relational lapse as a derived ratio

For two active subsystems \(x\) and \(r\) evaluated on a common relational comparison patch,

\[
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda.
\]

Then

\[
\boxed{
N_R(x|r)
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

For three clocks,

\[
\boxed{N_{x|s}=N_{x|r}N_{r|s}.}
\]

After reference calibration

\[
\boxed{dt=T_r\,d\Theta_r,}
\]

\[
\boxed{d\hat\tau_x=N_R(x|r)dt.}
\]

## 8. Temporal primitive handoff

The local derived pair is

\[
\boxed{
\mathbb T_e=(d\Theta_e,\chi_e).
}
\]

Its typed handoff is

```text
directed relation      : source -> target composability
local relation parameter: lambda_e [coordinate only]
directed traffic       : W_plus, W_minus
unique duration density: activity = W_plus + W_minus [up to clock scale]
invariant edge duration: theta(e) = integral activity d_lambda_e
orientation coordinate : chi = current/activity
composition accumulation: Theta(P_n) = sum theta(e_k)
derived precedence      : 00F prefix-order embedding
clock comparison        : N_R = dTheta_x/dTheta_ref
clock calibration       : dt = T_ref dTheta_ref
```

The derivational sequence is

\[
\boxed{
\text{DIRECTED RELATIONAL COMPOSABILITY}
\to
\text{EXTENSIVE EVEN ACTIVITY}
\to
(\theta,\chi)
\to
\text{00F DERIVED PRECEDENCE}
\to
N_R
\to
\text{CALIBRATED ELAPSED TIME}.
}
\]

## 9. GREMLIN candidate audit contract

GREMLIN remains candidate-only. The candidate relation is

```text
independent transition superposition -> extensive local density
orientation exchange                 -> even duration / odd direction
local parameter covariance           -> invariant edge duration
relation composition                 -> additive duration accumulation
positive edge duration               -> strict prefix growth in 00F
activity ratio                        -> relational lapse
reference calibration                -> physical clock reading
```

Promotion requires algebraic tests for positivity, channel extensivity, reparameterization invariance, composition additivity, orientation reversal, Shannon-affinity consistency, clock-ratio composition and fail-closed domain behavior.

Reference implementation: `src/idt/temporal_primitive_activity.py`.
Reference tests: `tests/reference/test_temporal_primitive_activity.py`.
Validation receipt: `validation/TEMPORAL_PRIMITIVE_ACTIVITY_V0_1.json`.
