# 01K — Temporal Information Curvature Interface

Status: `TARGETED_TEMPORAL_INFORMATION_CURVATURE_INTERFACE_PASS_CANDIDATE / RELATIONAL_AREA_BINDING_PENDING`

## 1. Purpose

This gate types the dimensional bridge between the dimensionless Shannon-relative-information sector already admitted in 01C and the inverse-area scalar required by downstream geometric closure.

The central distinction is explicit:

- Shannon entropy and KL relative information are dimensionless information scalars once the logarithm base is fixed;
- an inverse-area quantity appears only after division by an admitted positive relational area carrying dimension `L^2`.

RFC owns the later binding of this inverse-area scalar into the dynamic `Lambda0` sector.

## 2. Information scalar

From 01C, let

\[
\mathcal I_\pi[p]
=D_{\rm KL}^{(2)}(p\|\pi)
=\sum_{a:p_a>0}p_a\log_2\frac{p_a}{\pi_a}.
\]

Convert bits to the natural-log information scalar

\[
\boxed{
\mathcal J_\pi[p]
=(\ln2)\,\mathcal I_\pi[p].
}
\]

Both `I_pi` and `J_pi` are dimensionless.

## 3. Relational areal normalization interface

Let

\[
\mathcal A_{\rm rel}>0,
\qquad
[\mathcal A_{\rm rel}]=L^2,
\]

be an admitted relational area supplied by the upstream geometric layer. Define

\[
\boxed{
\Xi_I
:=\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}}.
}
\]

Then exactly

\[
\boxed{[\Xi_I]=L^{-2}.}
\]

Under a physical length rescaling `ell -> s ell`, the area transforms as

\[
\mathcal A_{\rm rel}\to s^2\mathcal A_{\rm rel},
\]

so

\[
\boxed{\Xi_I\to s^{-2}\Xi_I.}
\]

This is the inverse-square information scalar exported by IDT.

## 4. Exact temporal differential

Along any admitted temporal evolution,

\[
\boxed{
 d\Xi_I
 =\frac{1}{\mathcal A_{\rm rel}}\,d\mathcal J_\pi
 -\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}^2}\,d\mathcal A_{\rm rel}.
}
\]

Using internal elapsed activity `tau_int`,

\[
\boxed{
\frac{d\Xi_I}{d\tau_{\rm int}}
=\frac{1}{\mathcal A_{\rm rel}}
\frac{d\mathcal J_\pi}{d\tau_{\rm int}}
-\frac{\Xi_I}{\mathcal A_{\rm rel}}
\frac{d\mathcal A_{\rm rel}}{d\tau_{\rm int}}.
}
\]

Therefore temporal change of the inverse-area information scalar receives two typed contributions:

1. information redistribution at fixed area;
2. relational-area evolution at fixed information.

For a fixed relational area, the 01C KL contraction transfers directly to `Xi_I`.

## 5. Clock calibration

For the admitted monotone empirical clock map

\[
t=t(\tau_{\rm int}),
\qquad
\frac{dt}{d\tau_{\rm int}}>0,
\]

the calibrated rate is

\[
\boxed{
\frac{d\Xi_I}{dt}
=
\frac{d\Xi_I/d\tau_{\rm int}}
{dt/d\tau_{\rm int}}.
}
\]

Thus the scalar itself is clock-coordinate independent, while its reported rate transforms by the usual chain rule.

## 6. TIR normalization crosslink

TIR fixes

\[
\kappa=\frac{\ln2}{24\pi}.
\]

Hence the numerator can equivalently be written

\[
\mathcal J_\pi
=24\pi\kappa\,\mathcal I_\pi,
\]

and therefore

\[
\boxed{
\Xi_I
=
\frac{24\pi\kappa}{\mathcal A_{\rm rel}}\,\mathcal I_\pi.
}
\]

This is an exact substitution once the independent TIR definition of `kappa` and the 01C bit-valued KL scalar are admitted.

## 7. Export contract

IDT exports to downstream field closure:

```text
information_scalar_bits        = I_pi
information_scalar_nats        = J_pi = ln(2) I_pi
relational_area                = A_rel > 0
temporal_information_curvature = Xi_I = J_pi / A_rel
internal_time_rate             = dXi_I / d tau_int
clock_calibration              = dt / d tau_int > 0
```

Required upstream receipt for physical `L^-2` typing: a TIR relational-area calibration contract.

## 8. Evidence boundary

Exact at this gate:

- bit-to-nat conversion;
- inverse-area scaling;
- quotient-rule temporal differential;
- chain-rule clock conversion;
- constant-area inheritance of 01C information contraction.

Downstream field binding:

- the coefficient coupling `Xi_I` into `Lambda0`;
- metric/area physical calibration;
- Einstein-Bianchi closure.
