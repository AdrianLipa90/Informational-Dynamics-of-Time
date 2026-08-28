# 01K — Temporal Information Curvature Interface

Status: `TARGETED_TEMPORAL_INFORMATION_CURVATURE_INTERFACE_PASS_CANDIDATE / PHASE_CLOCK_AREA_BINDING_CANDIDATE`

## 1. Purpose

This gate types the dimensional bridge between the dimensionless Shannon-relative-information sector already admitted in 01C and the inverse-area scalar required by downstream geometric closure.

The central distinction is explicit:

- Shannon entropy and KL relative information are dimensionless information scalars once the logarithm base is fixed;
- an inverse-area quantity appears after division by an admitted positive relational area carrying dimension `L^2`;
- 01L supplies a local `L`-typed phase-clock carrier from the calibrated temporal phase flow.

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

### 3A. Phase-clock length carrier from 01L

For the calibrated phase rate

\[
\omega_t
=\frac{d\varphi/d\tau_{\rm int}}{dt/d\tau_{\rm int}},
\qquad |\omega_t|>0,
\]

01L gives

\[
\boxed{
\ell_\varphi=\frac{c}{|\omega_t|}
=\frac{\hbar c}{E}.
}
\]

Let `da_FS` denote a dimensionless Fubini--Study area element imported from the projective geometry layer. The local phase-clock area candidate is

\[
\boxed{
 d\mathcal A_{\rm rel}
 :=\ell_\varphi^2\,da_{FS}
 =\frac{c^2}{\omega_t^2}\,da_{FS}.
}
\]

For a cell `P` with constant calibrated phase-rate magnitude,

\[
\boxed{
\mathcal A_{\rm rel}^{(P)}
=\frac{c^2}{\omega_P^2}\,a_{FS}^{(P)}.
}
\]

Therefore

\[
\boxed{
\Xi_I^{(P)}
=\frac{\mathcal J_\pi}{a_{FS}^{(P)}}
\left(\frac{\omega_P}{c}\right)^2
}
\]

and, using `E_P = hbar |omega_P|`,

\[
\boxed{
\Xi_I^{(P)}
=\frac{\mathcal J_\pi}{a_{FS}^{(P)}}
\left(\frac{E_P}{\hbar c}\right)^2.
}
\]

For a spatially varying nonzero phase rate,

\[
\boxed{
\mathcal A_{\rm rel}^{(P)}
=\int_P\frac{c^2}{\omega_t(x)^2}\,da_{FS}(x).
}
\]

The constant-rate formula is the exact reduction of this integral when `omega_t` is constant on the cell.

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

For the constant-dimensionless-area and constant-over-cell phase-rate sector,

\[
\Xi_I
=\frac{\mathcal J_\pi}{a_{FS}}
\frac{\omega_t^2}{c^2},
\]

hence

\[
\boxed{
\frac{d\Xi_I}{d\tau_{\rm int}}
=
\frac{\omega_t^2}{c^2a_{FS}}
\frac{d\mathcal J_\pi}{d\tau_{\rm int}}
+
\frac{2\mathcal J_\pi\omega_t}{c^2a_{FS}}
\frac{d\omega_t}{d\tau_{\rm int}}.
}
\]

Temporal change therefore contains an information-redistribution channel and a phase-rate/scale channel.

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

The scalar itself is carried by the admitted physical phase-clock map, while its reported temporal rate follows the usual chain rule.

## 6. TIR normalization crosslink

TIR fixes

\[
\kappa=\frac{\ln2}{24\pi}.
\]

Hence

\[
\mathcal J_\pi
=24\pi\kappa\,\mathcal I_\pi,
\]

and in the constant-rate cell sector

\[
\boxed{
\Xi_I^{(P)}
=
\frac{24\pi\kappa}{a_{FS}^{(P)}}
\mathcal I_\pi
\left(\frac{\omega_P}{c}\right)^2.
}
\]

For the full CP1/Bloch sphere, `a_FS = pi`, so

\[
\boxed{
\Xi_I^{(S^2)}
=24\kappa\,\mathcal I_\pi
\left(\frac{\omega}{c}\right)^2.
}
\]

## 7. Export contract

IDT exports to downstream field closure:

```text
information_scalar_bits        = I_pi
information_scalar_nats        = J_pi = ln(2) I_pi
calibrated_phase_rate           = omega_t
phase_length_per_radian         = ell_phi = c / |omega_t| = hbar c / E
phase_clock_area_element        = dA_rel = ell_phi^2 da_FS
temporal_information_curvature = Xi_I = J_pi / A_rel
constant_cell_form              = Xi_I = (J_pi / a_FS) (omega/c)^2
internal_time_rate              = dXi_I / d tau_int
clock_calibration               = dt / d tau_int > 0
```

Required upstream geometric receipt: the TIR projective/polyhedral area carrier and refinement rule.

## 8. Evidence boundary

Exact at this gate:

- bit-to-nat conversion;
- inverse-area scaling;
- 01L phase-clock length identity;
- constant-rate area and curvature reduction;
- quotient-rule temporal differential;
- constant-area phase-rate derivative;
- chain-rule clock conversion.

Downstream field binding:

- selection/refinement of the physical projective cell;
- treatment of phase-rate zeros and nonuniform cells;
- the coefficient coupling `Xi_I` into `Lambda0`;
- Einstein-Bianchi closure.
