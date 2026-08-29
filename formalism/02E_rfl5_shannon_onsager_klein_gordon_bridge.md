# 02E — RF-L5 Shannon–Onsager → Klein–Gordon Bridge

Status: `01D_TO_02B_STIFFNESS_EXACT / CONSERVATIVE_HYPERBOLIC_LIFT_ADMITTED / RFC_MASS_TERM_COMPOSITION_EXACT / PREMETRIC_KG_PASS / METRIC_TIME_CALIBRATION_OPEN`

This interface records the IDT side of RFC RF-L5. It combines the exact 01D uniform-equilibrium Shannon–Onsager response/stiffness identity with the 02A–02C Temporal Wave line and the RF-L4A information-curvature mass term.

## 1. Exact 01D response/stiffness identity

For the zero-drive symmetric sector with `N_s` states and uniform stationary reference `u_a=1/N_s`, IDT 01D proves

\[
\boxed{
G_u^{(2)}(u)
=\frac{\ln2}{N_s}K_0,
}
\]

where 02B identifies

\[
\boxed{
K_0
=D^\top\operatorname{diag}(M_{ab})D
}
\]

as the untwisted relational-mobility Temporal Wave stiffness.

Therefore

\[
\boxed{
K_0=\frac{N_s}{\ln2}G_u^{(2)}(u).
}
\]

This identity is exact at the uniform stationary reference.

## 2. Conservative hyperbolic lift

02B supplies

\[
\ddot q+C_\eta\dot q+K_0q=0.
\]

The closed-system conservative projection is

\[
\boxed{C_\eta=0}
\]

and hence

\[
\boxed{
\ddot q+K_0q=0.
}
\]

The nonzero viscosity operator remains an admitted dissipative extension with energy balance

\[
\frac{d\mathcal H_T}{dt}
=-\dot q^\top C_\eta\dot q\le0.
\]

## 3. RFC information-curvature mass return

RFC RF-L4A returns the locally Fisher-normalized scalar coordinate and potential

\[
\phi_I=\sqrt{2\Xi_I},
\]

\[
U_I(\phi_I)=\frac12m_I^2\phi_I^2,
\qquad
\boxed{m_I^2=\frac{\alpha_I}{\kappa_E}.}
\]

Composing this potential with the 02B conservative stiffness gives

\[
\boxed{
\ddot\phi_I+(K_0+m_I^2I)\phi_I=0.
}
\]

Using the exact 01D identity,

\[
\boxed{
\ddot\phi_I
+\left[
\frac{N_s}{\ln2}G_u^{(2)}(u)
+m_I^2I
\right]\phi_I=0.
}
\]

Equivalently,

\[
\boxed{
\ddot\phi_I
+\left[
\frac{N_s}{\ln2}G_u^{(2)}(u)
+\frac{\alpha_I}{\kappa_E}I
\right]\phi_I=0.
}
\]

The symmetric information-response operator therefore supplies the relational stiffness, while the RFC information-curvature potential supplies the spectral gap.

## 4. Modal form

Let

\[
K_0v_r=\lambda_rv_r.
\]

Then each conservative mode satisfies

\[
\boxed{
\ddot a_r+(\lambda_r+m_I^2)a_r=0,
\qquad
\omega_r^2=\lambda_r+m_I^2.
}
\]

For the constant connected-graph mode,

\[
K_0\mathbf1=0,
\]

so

\[
\boxed{
\omega_0^2=m_I^2.
}
\]

The RFC scalar mass is thus the homogeneous conservative spectral gap of the composed IDT/RFC equation.

## 5. Premetric continuum bridge

02C gives

\[
\boxed{c_{eff}^2=M_{eff}}
\]

with the harmonic-mean mobility

\[
M_{eff}
=\left(\frac1N\sum_e\frac1{M_e}\right)^{-1}.
\]

The conservative long-wave equation becomes

\[
\boxed{
\partial_t^2\phi_I
-M_{eff}\partial_x^2\phi_I
+m_I^2\phi_I=0,
}
\]

with

\[
\boxed{
\omega^2=M_{eff}k^2+m_I^2.
}
\]

As in 02C, `M_eff` is a premetric wave coefficient with respect to the admitted ordering/coordinate normalization.

## 6. Metric-time interface

IDT 05C supplies the exact positive lapse ratio

\[
N_R=\frac{d\tau_x}{d\tau_{ref}}
\]

and the physical-time/coframe candidate

\[
\Theta_R=N_Rc\,dt.
\]

The remaining physical light-cone calibration is the comparison

\[
\boxed{
c_{eff}^2=M_{eff}
\stackrel{gate}{=}c^2
}
\]

in the common calibrated chart, or `M_eff=1` in natural units.

This gate is the current continuum metric-time normalization problem; the discrete Shannon-to-Klein–Gordon operator bridge is already explicit before that calibration.

## 7. Phase-clock scale target

IDT 01K carries a phase-clock frequency

\[
\ell_\phi=\frac{c}{|\omega_t|}.
\]

For the homogeneous physical-time Klein–Gordon mode,

\[
\omega_0^2=c^2m_I^2.
\]

A future common-clock spectral identification

\[
\boxed{\omega_0=|\omega_t|}
\]

would give

\[
\boxed{
m_I^2=\left(\frac{\omega_t}{c}\right)^2}
\]

and, using RF-L4A,

\[
\boxed{
\alpha_I
=\kappa_E\left(\frac{\omega_t}{c}\right)^2.
}
\]

The required spectral-line selection and common physical-time calibration are separate promotion gates.

## 8. Typed damping separation

The core RF-L5 action bridge uses `C_eta=0`. If the IDT viscosity operator is retained,

\[
\ddot\phi_I+C_\eta\dot\phi_I+(K_0+m_I^2I)\phi_I=0,
\]

then

\[
\frac{dE_I}{dt}
=-\dot\phi_I^\top C_\eta\dot\phi_I\le0.
\]

This remains the dissipative/open-system IDT branch and requires an explicit external/environmental energy ledger before coupling to a closed covariant Einstein source.

## 9. Advancement

```text
01D G_u^(2)(u) = (ln2/N_s) K0                    PASS EXACT
02B K0 temporal-wave stiffness                    ADMITTED
02B conservative C_eta=0 projection               PASS EXACT SUBSECTOR
RF-L4A local Fisher scalar normalization           RFC 543/543 PASS
RF-L4A m_I^2=alpha_I/kappa_E                      ADMITTED
finite-graph KG composition                        PASS EXACT CONSTRUCTION
Shannon-response KG representation                 PASS EXACT
homogeneous mass gap                               PASS EXACT
02C premetric continuum dispersion                 PASS STRUCTURAL
05C lapse/time interface                           ADMITTED CANDIDATE
M_eff -> c^2 metric-time calibration               OPEN
phase-clock homogeneous mass identification        OPEN
physical alpha_I / m_I scale                       OPEN
curved-spacetime continuum                         DOWNSTREAM RFC GATE
```
