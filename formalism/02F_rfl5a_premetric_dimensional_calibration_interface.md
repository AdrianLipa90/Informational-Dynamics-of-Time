# 02F — RF-L5A Premetric Dimensional Calibration Interface

Status: `PREMETRIC_TO_PHYSICAL_AFFINE_MAP_EXACT / 05C_REFERENCE_CLOCK_FACTOR_EXACT / LIGHTCONE_RATIO_CONDITION_EXACT / RFC_MASS_FREQUENCY_MAP_EXACT / SPATIAL_CELL_BINDING_OPEN / VARIABLE_LAPSE_EXTENSION_OPEN`

This interface records the IDT side of RFC RF-L5A. It connects the 02B/02C ordering/cell-coordinate wave equation to a local physical clock/length chart while preserving the distinction between the premetric homogeneous gap `mu_lambda^2` and the RFC inverse-length scalar mass `m_I^2`.

## 1. Premetric input

02E carries

\[
\boxed{
\partial_\lambda^2\phi_I
-M_{eff}\partial_\xi^2\phi_I
+\mu_\lambda^2\phi_I=0.
}
\]

Here `lambda` is the IDT ordering coordinate and `xi` is the admitted premetric cell coordinate.

## 2. Local affine clock and length calibration

On one local patch define

\[
\boxed{
t-t_\star=\Gamma_t(\lambda-\lambda_\star),
\qquad
X-X_\star=\Gamma_x(\xi-\xi_\star),
}
\]

with `Gamma_t>0` and `Gamma_x>0`.

Then

\[
\boxed{
\partial_\lambda^2=\Gamma_t^2\partial_t^2,
\qquad
\partial_\xi^2=\Gamma_x^2\partial_X^2.
}
\]

Substitution gives

\[
\boxed{
\partial_t^2\phi_I
-M_{eff}\frac{\Gamma_x^2}{\Gamma_t^2}\partial_X^2\phi_I
+\frac{\mu_\lambda^2}{\Gamma_t^2}\phi_I=0.
}
\]

## 3. Physical coefficient map

Define

\[
\boxed{
c_{cal}^2
:=M_{eff}\frac{\Gamma_x^2}{\Gamma_t^2}}
\]

and

\[
\boxed{
\Omega_m^2
:=\frac{\mu_\lambda^2}{\Gamma_t^2}.}
\]

The local physical equation is

\[
\boxed{
\partial_t^2\phi_I
-c_{cal}^2\partial_X^2\phi_I
+\Omega_m^2\phi_I=0.
}
\]

## 4. 05C reference-clock factor

IDT 05C gives

\[
d\tau_{ref}=\phi_{ref}d\lambda
\]

and

\[
dt=T_{ref}d\tau_{ref}.
\]

Therefore, on a fixed-reference calibration patch,

\[
\boxed{
\Gamma_t
=\frac{dt}{d\lambda}
=T_{ref}\phi_{ref}>0.
}
\]

This is the exact IDT clock factor consumed by RF-L5A.

## 5. Light-cone condition

Matching the calibrated local equation to the physical Lorentzian scalar propagation coefficient gives

\[
\boxed{
M_{eff}\frac{\Gamma_x^2}{\Gamma_t^2}=c^2.
}
\]

Equivalently,

\[
\boxed{
\frac{\Gamma_x}{\Gamma_t}
=\frac{c}{\sqrt{M_{eff}}}.
}
\]

Thus `M_eff` and the physical light-cone coefficient are connected through the ratio of calibrated physical length to calibrated physical time per premetric coordinate unit.

## 6. Spatial cell calibration interface

If one premetric cell width `h` is assigned an independently calibrated physical width `L_h`, then

\[
\boxed{
\Gamma_x=\frac{L_h}{h}.
}
\]

Together with 05C,

\[
\boxed{
\frac{L_h}{hT_{ref}\phi_{ref}}
=\frac{c}{\sqrt{M_{eff}}}.
}
\]

IDT 01L supplies the exact phase-clock length carrier

\[
\ell_\varphi=\frac{c}{|\omega_t|}.
\]

A downstream cell-geometry gate may bind `L_h` to an admitted phase/projective length construction. The RF-L5A light-cone equation supplies the exact target that such a binding must satisfy.

## 7. RFC mass-frequency return

RFC RF-L4A supplies

\[
\boxed{
m_I^2=\frac{\alpha_I}{\kappa_E}.}
\]

Matching the calibrated homogeneous coefficient to the local Lorentzian Klein–Gordon equation requires

\[
\boxed{
\frac{\mu_\lambda^2}{\Gamma_t^2}
=c^2m_I^2.
}
\]

Therefore

\[
\boxed{
\mu_\lambda^2
=\Gamma_t^2c^2m_I^2
=\Gamma_t^2c^2\frac{\alpha_I}{\kappa_E}.
}
\]

Using 05C,

\[
\boxed{
\mu_\lambda^2
=(T_{ref}\phi_{ref})^2c^2\frac{\alpha_I}{\kappa_E}.
}
\]

## 8. Physical homogeneous frequency

The premetric homogeneous mode has

\[
\omega_{\lambda,0}^2=\mu_\lambda^2.
\]

The common physical clock gives

\[
\boxed{
\omega_t^{(KG)}
=\frac{\omega_{\lambda,0}}{\Gamma_t},
}
\]

so

\[
\boxed{
(\omega_t^{(KG)})^2
=c^2m_I^2
=c^2\frac{\alpha_I}{\kappa_E}.
}
\]

This is the frequency quantity that a downstream IDT phase-clock line must match if the scalar mass scale is to be fixed spectrally.

## 9. Unit-calibration specialization

For

\[
\Gamma_t=\Gamma_x=1,
\]

the general conditions reduce to

\[
\boxed{M_{eff}=c^2}
\]

and

\[
\boxed{\mu_\lambda^2=c^2m_I^2.}
\]

In natural units `c=1`, this further reduces to `M_eff=1` and `mu_lambda^2=m_I^2`.

## 10. Variable lapse frontier

IDT 05C exports the reparameterization-invariant local lapse ratio

\[
N_R=\frac{d\tau_x}{d\tau_{ref}}.
\]

RF-L5A/02F use a fixed-reference local affine patch. When `N_R`, `Gamma_t` or `Gamma_x` varies over spacetime, derivatives of the calibration fields contribute to the wave operator. The next covariant gate must carry those terms through the local coframe/metric construction rather than applying the constant-coefficient affine formula pointwise without derivatives.

## 11. Advancement

```text
02E premetric scalar equation                         ADMITTED
05C Gamma_t=T_ref phi_ref                            PASS EXACT GIVEN FIXED REFERENCE
local affine spatial factor Gamma_x                  TYPED
c_cal^2=M_eff Gamma_x^2/Gamma_t^2                  PASS EXACT
light-cone calibration ratio                         PASS EXACT
RFC m_I^2=alpha_I/kappa_E                            ADMITTED RETURN
mu_lambda^2=Gamma_t^2 c^2 m_I^2                    PASS EXACT CALIBRATION
physical KG homogeneous frequency                    PASS EXACT CALIBRATION
cell physical width L_h                              OPEN PHYSICAL BINDING
phase-clock spectral identification                  OPEN
variable-lapse derivative terms                      OPEN COVARIANT GATE
```
