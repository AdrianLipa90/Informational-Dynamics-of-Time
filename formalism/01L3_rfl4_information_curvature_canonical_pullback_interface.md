# 01L3 — RF-L4 Information-Curvature Canonical Pullback Interface

Status: `RFC_RF_L4_SQRT_PULLBACK_COMPANION / IDT_01K_EXPORT_PRESERVED / SHANNON_ONSAGER_KINETIC_MATCH_TARGET_OPEN`

This interface records the IDT side of the RF-L4 scalar-coordinate pullback while preserving the existing 01K information-curvature and 01L/01L2 holonomy lineages.

## 1. IDT scalar export

IDT 01K defines

\[
\boxed{
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}},
\qquad [\Xi_I]=L^{-2}.
}
\]

For an admitted constant reference state `Xi_star`, define

\[
\boxed{\bar\Xi_I=\Xi_I-\Xi_\star.}
\]

RF-L4 selects an admitted branch with `bar(Xi)_I >= 0` and introduces

\[
\boxed{
\phi_I=\beta_I\sqrt{\bar\Xi_I},
\qquad \beta_I>0.
}
\]

In four-dimensional natural units, `[phi_I]=L^-1`, matching the canonical scalar coordinate dimension used by the RFC action line.

## 2. Constant-background transfer

RFC RF-L3 has

\[
\Lambda_0=\Lambda_{ref}+\alpha_I\Xi_I.
\]

With

\[
\Lambda_\star=\Lambda_{ref}+\alpha_I\Xi_\star,
\]

RF-L4 gives

\[
\boxed{
\Lambda_0
=\Lambda_\star
+\frac{\alpha_I}{\beta_I^2}\phi_I^2.
}
\]

The IDT baseline scalar therefore maps to the constant reference coordinate, while the baseline-resolved curvature maps to the dynamic scalar coordinate.

## 3. Direct 01K phase-clock form

In the 01K constant-rate cell sector,

\[
\Xi_I
=\frac{\mathcal J_\pi}{a_{FS}}
\left(\frac{\omega}{c}\right)^2.
\]

For `Xi_star=0`,

\[
\boxed{
\phi_I
=\beta_I
\sqrt{\frac{\mathcal J_\pi}{a_{FS}}}
\frac{|\omega|}{c}.
}
\]

For the full CP1/Bloch sphere,

\[
\Xi_I
=24\kappa\mathcal I_\pi
\left(\frac{\omega}{c}\right)^2,
\qquad
\kappa=\frac{\ln2}{24\pi},
\]

so

\[
\boxed{
\phi_I^{(S^2)}
=\beta_I\sqrt{24\kappa\mathcal I_\pi}\,
\frac{|\omega|}{c}.
}
\]

This preserves the complete IDT scalar lineage

\[
(\mathcal I_\pi,\omega,a_{FS})
\rightarrow
\Xi_I
\rightarrow
\phi_I.
\]

## 4. Holonomy remains an independent oriented coordinate

The existing 01L/01L2 interface exports

\[
\tau_R=\operatorname{wrap}_\pi\Phi_T(C),
\qquad
h_R=e^{i\tau_R}.
\]

The RF-L4 square-root pullback acts on the scalar magnitude coordinate only. The paired state is therefore

\[
\boxed{
(\Xi_I,\tau_R)
\rightarrow
(\phi_I,\tau_R).
}
\]

The temporal orientation coordinate is carried unchanged through the canonical scalar map.

## 5. Differential pullback

For `Xi_I>Xi_star`,

\[
\boxed{
 d\phi_I
=\frac{\beta_I}{2\sqrt{\Xi_I-\Xi_\star}}d\Xi_I.
}
\]

Using the exact 01K quotient differential,

\[
 d\Xi_I
=\frac{1}{\mathcal A_{\rm rel}}d\mathcal J_\pi
-\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}^2}d\mathcal A_{\rm rel},
\]

gives

\[
\boxed{
 d\phi_I
=\frac{\beta_I}{2\sqrt{\Xi_I-\Xi_\star}}
\left(
\frac{d\mathcal J_\pi}{\mathcal A_{\rm rel}}
-\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}^2}d\mathcal A_{\rm rel}
\right).
}
\]

Thus information redistribution and phase-clock/area evolution both enter the canonical scalar differential through the already-admitted 01K channels.

## 6. Shannon–Onsager kinetic comparison target

IDT 01D supplies a positive tangent-space response metric on the mass-conserving probability-simplex sector. RFC RF-L4 induces the one-dimensional information-curvature coefficient

\[
\boxed{
Z_I^{RFC}(\Xi_I)
=\frac{\beta_I^2}{4(\Xi_I-\Xi_\star)}.
}
\]

The next IDT-side promotion coordinate is to reduce the 01D tangent metric along an admitted 01K trajectory and obtain the corresponding scalar coefficient `Z_I^IDT(Xi_I)`.

The cross-repository kinetic closure target is

\[
\boxed{
Z_I^{IDT}(\Xi_I)
=Z_I^{RFC}(\Xi_I).
}
\]

This comparison determines whether the RFC canonical scalar normalization is the induced normalization of the admitted Shannon–Onsager information dynamics and provides the gate for fixing `beta_I`.

## 7. RFC quadratic potential return

RF-L4 returns

\[
U_I(\phi_I)
=\frac{\alpha_I}{\kappa_E\beta_I^2}\phi_I^2
=\frac12m_I^2\phi_I^2
\]

with

\[
\boxed{
m_I^2=\frac{2\alpha_I}{\kappa_E\beta_I^2}.}
\]

The IDT-side calibration task therefore becomes a joint kinetic-normalization / carrier-scale problem rather than an unconstrained functional-potential problem.

## 8. Cross-repository advancement

```text
01K Xi_I inverse-area information curvature            ADMITTED
RF-L3 linear scalar displacement                       ADMITTED
baseline-resolved barXi_I                              PASS EXACT
phi_I = beta_I sqrt(barXi_I)                           PASS EXACT ON ADMITTED BRANCH
01K constant-cell/full-sphere export -> phi_I          PASS EXACT
01L/01L2 tau_R orientation transport                   PASS EXACT
01K quotient differential -> dphi_I                    PASS EXACT
01D tangent metric reduction to Xi_I trajectory         OPEN
Z_I^IDT = Z_I^RFC kinetic closure                      OPEN
beta_I physical normalization                          OPEN
```
