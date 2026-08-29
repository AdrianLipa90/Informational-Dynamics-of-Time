# 01L4 — RF-L4A Shannon–Fisher Local Normalization Interface

Status: `SHANNON_HESSIAN_EXACT / LOCAL_FISHER_RADIAL_NORMALIZATION_PASS / RFC_BETA_I_SQRT2_LOCAL / ORIENTED_HOLONOMY_PRESERVED / ONSAGER_TO_LORENTZIAN_DYNAMICAL_BRIDGE_OPEN`

This interface records the IDT-side local information-geometric normalization used by RFC RF-L4A. It consumes 01C relative information, 01D Shannon–Onsager response, 01K temporal information curvature and the 01L3 RF-L4 canonical pullback interface.

## 1. Natural-log relative information

IDT 01C defines

\[
\mathcal I_\pi[p]=D_{KL}^{(2)}(p\|\pi).
\]

The 01K natural-log scalar is

\[
\boxed{
\mathcal J_\pi[p]
=(\ln2)\mathcal I_\pi[p]
=\sum_a p_a\ln\frac{p_a}{\pi_a}.
}
\]

For a strictly positive stationary reference `pi`, let

\[
p_a=\pi_a+\delta p_a,
\qquad
\sum_a\delta p_a=0.
\]

At `p=pi`, the tangent first variation vanishes and the Hessian is

\[
\boxed{
H^F_{ab}(\pi)=\frac{\delta_{ab}}{\pi_a}.
}
\]

Thus the stationary-reference tangent geometry is the Fisher metric.

## 2. Local Fisher radial norm

Define

\[
\boxed{
s_F^2:=\sum_a\frac{(\delta p_a)^2}{\pi_a}.}
\]

Then the exact Taylor coefficient of the admitted relative-information scalar is

\[
\boxed{
\mathcal J_\pi
=\frac12s_F^2+O(\|\delta p\|^3).
}
\]

The coefficient `1/2` follows from the Hessian of `J_pi`; it is therefore fixed by the admitted Shannon geometry rather than selected as an RFC field convention.

## 3. Local 01K curvature reduction

IDT 01K defines

\[
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{rel}}.
\]

Let

\[
\mathcal A_{rel}=\mathcal A_\star+O(\|\delta p\|),
\qquad
\mathcal A_\star>0.
\]

Because `J_pi` begins at second order, smooth first-order area variation changes `Xi_I` first at third order. Hence

\[
\boxed{
\Xi_I
=\frac{s_F^2}{2\mathcal A_\star}
+O(\|\delta p\|^3).
}
\]

Define the local inverse-length Fisher radial coordinate

\[
\boxed{
\phi_F:=\frac{s_F}{\sqrt{\mathcal A_\star}}.
}
\]

Then

\[
\boxed{
\Xi_I=\frac12\phi_F^2+O(\|\delta p\|^3).
}
\]

## 4. RF-L4 normalization consequence

RF-L4 uses the zero-baseline local coordinate

\[
\phi_I=\beta_I\sqrt{\Xi_I}.
\]

Matching the leading Fisher radial coordinate gives

\[
\boxed{\beta_I=\sqrt2}
\]

in the local stationary-reference Fisher sector, and therefore

\[
\boxed{
\phi_I
=\sqrt{2\Xi_I}
=\phi_F+O(\|\delta p\|^2).
}
\]

The corresponding RFC one-dimensional information-curvature coefficient is

\[
\boxed{
Z_I^{RFC}(\Xi_I)=\frac{1}{2\Xi_I}.
}
\]

This fixes the RF-L4 field-coordinate normalization locally from IDT information geometry.

## 5. Full CP1/Bloch sphere specialization

IDT 01K gives

\[
\Xi_I^{(S^2)}
=24\kappa\mathcal I_\pi
\left(\frac{\omega}{c}\right)^2,
\qquad
\kappa=\frac{\ln2}{24\pi}.
\]

With the local Fisher normalization,

\[
\boxed{
\phi_I^{(S^2)}
=\sqrt{48\kappa\mathcal I_\pi}\,
\frac{|\omega|}{c}.
}
\]

Equivalently,

\[
\boxed{
\phi_I^{(S^2)}
=\sqrt{\frac{2\ln2}{\pi}\mathcal I_\pi}\,
\frac{|\omega|}{c}.
}
\]

## 6. Oriented holonomy transport

The 01L/01L2/01L3 line carries

\[
\tau_R=\operatorname{wrap}_\pi\Phi_T(C),
\qquad
h_R=e^{i\tau_R}.
\]

The Fisher normalization acts on the scalar magnitude chart only. The paired state therefore remains

\[
\boxed{
(\Xi_I,\tau_R)
\rightarrow
(\phi_I,\tau_R).
}
\]

The oriented temporal holonomy is preserved unchanged.

## 7. Relation to 01D dynamics

The Fisher Hessian fixes the local state-space geometry. IDT 01D separately gives the dynamical Onsager response

\[
\dot p=-G_\pi^{(2)}(p)\nabla_p\mathcal I_\pi.
\]

The next dynamical bridge must project this admitted response along an admitted Fisher-radial / 01K trajectory and compare the resulting scalar relaxation operator with the RFC Lorentzian scalar propagation law.

The remaining cross-repository targets are therefore

```text
local Fisher field normalization beta_I=sqrt(2)       PASS LOCAL
01K curvature -> Fisher radial scalar                  PASS LOCAL
smooth first-order area variation                      QUADRATIC COEFFICIENT PRESERVED
oriented tau_R transport                               PASS EXACT
01D response projection along admitted 01K trajectory OPEN
Onsager response -> Lorentzian propagation bridge      OPEN
alpha_I / m_I physical scale                           OPEN
finite-distance/global information-geodesic extension OPEN
```

## 8. RFC return

RF-L4A returns the locally normalized quadratic scalar potential

\[
U_I(\phi_I)=\frac{\alpha_I}{2\kappa_E}\phi_I^2
=\frac12m_I^2\phi_I^2
\]

with

\[
\boxed{m_I^2=\frac{\alpha_I}{\kappa_E}.}
\]

Thus after the local Shannon–Fisher normalization the remaining scalar calibration is one physical scale, expressible as `alpha_I` or equivalently `m_I`.
