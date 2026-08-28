# 00E — Activity-Derived Temporal Primitive

Status: `FORMAL_CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This layer derives an intrinsic temporal measure from the already admitted relational transition kinetics. Its inputs are the ordered relational path, the positive transition weights of 00C, and the directed affinity of 00B. Physical clock calibration remains a later operation.

## 1. Ordered relational path

Let

\[
\Gamma:\lambda\mapsto s(\lambda)
\]

be an admitted relational path, with \(\lambda\) any strictly increasing label of the transition order.

For an active pair \(a\leftrightarrow b\), 00C supplies

\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2},
\qquad
M_{ab}>0.
\]

The symmetric activity and directed current are

\[
\boxed{
\mathfrak a_{ab}
=W_{a\to b}+W_{b\to a}
=2M_{ab}\cosh(A_{ab}/2)>0,
}
\]

\[
\boxed{
\mathfrak j_{ab}
=W_{a\to b}-W_{b\to a}
=2M_{ab}\sinh(A_{ab}/2).
}
\]

## 2. Intrinsic activity measure

Treat the directed transition weights as densities with respect to the ordering label. Under an increasing relabelling

\[
\lambda'=f(\lambda),
\qquad
\frac{d\lambda'}{d\lambda}>0,
\]

the weights transform as

\[
W'_{\pm}
=W_{\pm}\frac{d\lambda}{d\lambda'}.
\]

Hence the activity transforms identically,

\[
\mathfrak a'
=\mathfrak a\frac{d\lambda}{d\lambda'}.
\]

Define the activity-derived temporal increment

\[
\boxed{
d\Theta=\mathfrak a\,d\lambda.
}
\]

Then

\[
d\Theta'
=\mathfrak a' d\lambda'
=\mathfrak a d\lambda
=d\Theta.
\]

Therefore \(d\Theta\) is invariant under every admitted increasing reparameterization of the ordering label.

For an interval of relational history \(\Gamma_{12}\),

\[
\boxed{
\Theta[\Gamma_{12}]
=\int_{\Gamma_{12}}\mathfrak a\,d\lambda.
}
\]

Positivity of \(\mathfrak a\) gives positive accumulation on every active interval, and integration gives exact additivity under path concatenation,

\[
\Theta[\Gamma_{13}]
=
\Theta[\Gamma_{12}]
+
\Theta[\Gamma_{23}].
\]

This is the first derived temporal measure of the programme.

## 3. Temporal orientation

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

the two temporal coordinates transform as

\[
\boxed{
d\Theta\mapsto d\Theta,}
\qquad
\boxed{\chi\mapsto-\chi.}
\]

The construction therefore separates accumulated duration from transition orientation.

At the symmetric point \(A=0\),

\[
\mathfrak a=2M>0,
\qquad
\chi=0.
\]

The temporal measure continues to accumulate while the directed coordinate sits at its symmetry value.

## 4. Shannon affinity form

00B supplies the transition affinity in bits,

\[
\sigma
=\log_2\frac{W_+}{W_-},
\qquad
A=(\ln2)\sigma.
\]

Therefore the temporal primitive has the exact information-kinetic representation

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

This gives a direct bridge

\[
(\rho_R,\eta_R,\sigma)
\longmapsto
(d\Theta,\chi).
\]

The fixed information-phase normalization

\[
\kappa=\frac{\ln2}{24\pi}
\]

continues to govern the phase-link sector, while \(d\Theta\) supplies the derived activity measure used for clock comparison.

## 5. Relational lapse as a derived ratio

For two active subsystems \(x\) and \(r\) referred to the same ordering label,

\[
d\Theta_x=\mathfrak a_x d\lambda,
\qquad
d\Theta_r=\mathfrak a_r d\lambda.
\]

Their intrinsic clock ratio is therefore

\[
\boxed{
N_R(x|r)
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

The common ordering label cancels exactly. For three clocks,

\[
\boxed{
N_{x|s}=N_{x|r}N_{r|s}.
}
\]

After calibration of the reference clock by a scale \(T_r\),

\[
dt=T_r\,d\Theta_r,
\]

the local calibrated elapsed interval follows as

\[
\boxed{
d\hat\tau_x
=T_r\,d\Theta_x
=N_R(x|r)\,dt.
}
\]

Thus the existing relational-lapse formula is recovered downstream from the activity-derived temporal measure.

## 6. Temporal primitive

The derived local temporal primitive is the typed pair

\[
\boxed{
\mathbb T_{ab}
=\left(d\Theta_{ab},\chi_{ab}\right).
}
\]

Its components carry distinct roles:

```text
ordering relation     : lambda labels admitted precedence
activity measure      : dTheta = a d lambda
orientation coordinate: chi = j/a
clock comparison      : N_R = dTheta_x / dTheta_ref
clock calibration     : d tau_hat = T_ref dTheta
phase topology        : kappa-weighted Shannon/geometric link
```

This places the derivational sequence at

\[
\boxed{
\text{RELATIONAL TRANSITIONS}
\to
\text{ACTIVITY + CURRENT}
\to
(d\Theta,\chi)
\to
N_R
\to
\text{CALIBRATED ELAPSED TIME}.
}
\]

## 7. GREMLIN candidate audit contract

GREMLIN remains candidate-only. The relational-isomorphism candidate submitted by this gate is

```text
positive symmetric transition traffic -> additive path measure
antisymmetric transition traffic      -> orientation coordinate
ratio of path measures                 -> relational lapse
reference calibration                  -> elapsed clock reading
```

Promotion requires algebraic tests for positivity, additivity, reparameterization invariance, orientation reversal, Shannon-affinity consistency, and clock-ratio composition.

Reference implementation: `src/idt/temporal_primitive_activity.py`.
Reference tests: `tests/reference/test_temporal_primitive_activity.py`.
Validation receipt: `validation/TEMPORAL_PRIMITIVE_ACTIVITY_V0_1.json`.
