# 02E — RF-L5 Shannon–Onsager → Conservative Scalar Bridge

Status: `01D_TO_02B_STIFFNESS_EXACT / CONSERVATIVE_HYPERBOLIC_LIFT_ADMITTED / PREMETRIC_GAP_TYPED / RFC_PHYSICAL_MASS_BINDING_DEFERRED_TO_02F_RF_L5A`

This interface records the IDT side of RFC RF-L5. It combines the exact 01D uniform-equilibrium Shannon–Onsager response/stiffness identity with the 02A–02C Temporal Wave line on the IDT ordering coordinate `lambda`.

RFC RF-L4A separately supplies the physical inverse-length mass coordinate

\[
\boxed{m_I^2=\alpha_I/\kappa_E}.
\]

The 02F/RF-L5A calibration layer binds that physical coordinate to the premetric homogeneous spectral-gap slot introduced here.

## 1. Exact 01D response/stiffness identity

For the zero-drive symmetric sector with `N_s` states and uniform stationary reference `u_a=1/N_s`, IDT 01D proves

\[
\boxed{
G_u^{(2)}(u)=\frac{\ln2}{N_s}K_0,
\qquad
K_0=\frac{N_s}{\ln2}G_u^{(2)}(u).
}
\]

02B identifies

\[
\boxed{
K_0=D^\top\operatorname{diag}(M_{ab})D
}
\]

as the untwisted relational-mobility Temporal Wave stiffness.

## 2. Conservative hyperbolic lift on lambda

02B supplies

\[
\ddot q+C_\eta\dot q+K_0q=0
\]

with dots taken with respect to `lambda`, as its energy law explicitly uses `d/dlambda`.

The conservative projection is

\[
\boxed{C_\eta=0}
\]

and hence

\[
\boxed{
\frac{d^2q}{d\lambda^2}+K_0q=0.
}
\]

## 3. Premetric homogeneous gap

Introduce the nonnegative premetric spectral slot

\[
\boxed{\mu_\lambda^2\ge0}
\]

in the same ordering-coordinate normalization as `d^2/dlambda^2` and `K0`. The composed finite-graph equation is

\[
\boxed{
\frac{d^2\phi_I}{d\lambda^2}
+(K_0+\mu_\lambda^2I)\phi_I=0.
}
\]

Using 01D,

\[
\boxed{
\frac{d^2\phi_I}{d\lambda^2}
+\left[
\frac{N_s}{\ln2}G_u^{(2)}(u)
+\mu_\lambda^2I
\right]\phi_I=0.
}
\]

The symmetric information-response operator supplies the relational stiffness; `mu_lambda^2` is the separately typed homogeneous ordering-coordinate gap.

## 4. Modal form

For

\[
K_0v_r=\lambda_rv_r,
\]

each mode obeys

\[
\boxed{
a_r''+(\lambda_r+\mu_\lambda^2)a_r=0,
\qquad
\omega_{\lambda,r}^2=\lambda_r+\mu_\lambda^2.
}
\]

The connected-graph constant mode has

\[
\boxed{
\omega_{\lambda,0}^2=\mu_\lambda^2.
}
\]

## 5. Premetric continuum bridge

02C gives

\[
\boxed{c_{eff}^2=M_{eff}}
\]

in the ordering/cell-coordinate normalization. Writing the premetric cell coordinate as `xi`, the conservative long-wave equation is

\[
\boxed{
\partial_\lambda^2\phi_I
-M_{eff}\partial_\xi^2\phi_I
+\mu_\lambda^2\phi_I=0,
}
\]

with

\[
\boxed{
\omega_\lambda^2=M_{eff}k_\xi^2+\mu_\lambda^2.
}
\]

## 6. 02F / RF-L5A calibration interface

The downstream calibration introduces positive local affine factors

\[
t-t_\star=\Gamma_t(\lambda-\lambda_\star),
\qquad
X-X_\star=\Gamma_x(\xi-\xi_\star).
\]

It then maps

\[
\boxed{
c_{cal}^2=M_{eff}\Gamma_x^2/\Gamma_t^2}
\]

and

\[
\boxed{
\Omega_m^2=\mu_\lambda^2/\Gamma_t^2.
}
\]

Physical Lorentzian matching requires

\[
\boxed{
M_{eff}\frac{\Gamma_x^2}{\Gamma_t^2}=c^2
}
\]

and

\[
\boxed{
\mu_\lambda^2
=\Gamma_t^2c^2m_I^2
=\Gamma_t^2c^2\frac{\alpha_I}{\kappa_E}.
}
\]

## 7. Phase-clock scale target

After common physical clock calibration,

\[
\omega_t^{(KG)}
=\frac{\omega_{\lambda,0}}{\Gamma_t}
\]

and therefore

\[
\boxed{
(\omega_t^{(KG)})^2
=c^2m_I^2
=c^2\frac{\alpha_I}{\kappa_E}.
}
\]

IDT 01L carries independently calibrated phase-clock frequencies. A downstream spectral gate may compare an independently admitted line with `omega_t^(KG)` after common-clock calibration.

## 8. Typed damping separation

If the IDT viscosity operator is retained,

\[
\phi_I''+C_\eta\phi_I'+(K_0+\mu_\lambda^2I)\phi_I=0,
\]

then

\[
\frac{dE_\lambda}{d\lambda}
=-\phi_I'^\top C_\eta\phi_I'\le0.
\]

The dissipative sector keeps its explicit energy ledger while the conservative branch feeds the RFC action line.

## 9. Advancement

```text
01D G_u^(2)(u)=(ln2/N_s)K0                       PASS EXACT
02B K0 temporal-wave stiffness                    ADMITTED
02B derivative coordinate lambda                  EXPLICIT
conservative C_eta=0 projection                   PASS EXACT SUBSECTOR
premetric gap mu_lambda^2                         TYPED
finite-graph conservative scalar equation          PASS EXACT CONSTRUCTION
premetric continuum dispersion                    PASS STRUCTURAL
02F/RF-L5A affine clock/length calibration         DOWNSTREAM EXACT MAP
physical RFC m_I^2=alpha_I/kappa_E                ADMITTED RFC COORDINATE
common-clock phase spectral identification        OPEN
variable-lapse curved continuum                    OPEN
```
