# 02JL — Temporal Density Current and Continuity

Status: `FORMAL_CANDIDATE / COVARIANT_CONTINUITY_GATE`

02JK identifies the glued half-frame channel with the continuum density and the complementary seam-defect channel with the covariant gradient. This layer derives the exact density-current continuity law carried by the same phase-aware nearest-neighbour structure.

## 1. Covariant nearest-neighbour Hamiltonian

Let a path contain vertex amplitudes

\[
a=(a_1,\ldots,a_N)^T
\]

and edge links

\[
L_n=e^{i\varphi_n},
\qquad n=1,\ldots,N-1.
\]

Define the covariant edge difference

\[
(D_La)_n=a_{n+1}-L_na_n.
\]

For positive edge mobilities \(M_n>0\) and mesh spacing \(h>0\), define

\[
\boxed{
H_h
=\frac1{h^2}
D_L^\dagger\operatorname{diag}(M_n)D_L
+V,
}
\]

where \(V\) is any real diagonal vertex potential. The intrinsic unitary flow is

\[
\boxed{
i\frac{da}{d\Theta}=H_ha.}
\]

The Hamiltonian is Hermitian.

## 2. Exact discrete density continuity

Define the vertex occupation

\[
\boxed{p_n=|a_n|^2.}
\]

The oriented edge current is

\[
\boxed{
j_{n+1/2}^{(h)}
:=
\frac{2M_n}{h^2}
\operatorname{Im}
\left(a_n^*L_n^*a_{n+1}\right).
}
\]

Direct substitution of the Schrödinger flow gives, for every interior vertex,

\[
\boxed{
\frac{dp_n}{d\Theta}
=j_{n-1/2}^{(h)}-j_{n+1/2}^{(h)}.
}
\]

At open boundaries use

\[
j_{1/2}=j_{N+1/2}=0.
\]

Hence

\[
\boxed{
\frac{d}{d\Theta}\sum_n p_n=0.
}
\]

The diagonal real potential contributes only local phase rotation and leaves the continuity identity unchanged.

## 3. The same seam phase carries coherence and transport quadratures

Write

\[
a_n=r_ne^{i\alpha_n},
\qquad
a_{n+1}=r_{n+1}e^{i\alpha_{n+1}},
\]

and retain the gauge-invariant mismatch

\[
\boxed{
\delta_n
=\alpha_{n+1}-\alpha_n-\varphi_n.
}
\]

Define the pair scale

\[
C_n:=r_nr_{n+1}
\]

and the two seam quadratures

\[
\boxed{
\mathcal C_n=C_n\cos\delta_n,
\qquad
\mathcal Q_n=C_n\sin\delta_n.
}
\]

They satisfy the exact circle identity

\[
\boxed{
\mathcal C_n^2+\mathcal Q_n^2=C_n^2.
}
\]

The occupancy-sensitive fuzzy-interface mass of 02JJ is

\[
\boxed{
J_n=C_n+\mathcal C_n
=C_n(1+\cos\delta_n),
}
\]

while the transport current is

\[
\boxed{
j_{n+1/2}^{(h)}
=\frac{2M_n}{h^2}\mathcal Q_n.
}
\]

Thus the same gauge-invariant seam phase resolves into a coherence quadrature and a transport quadrature.

Equivalently,

\[
\boxed{
\left(J_n-C_n\right)^2
+\left(\frac{h^2j_{n+1/2}^{(h)}}{2M_n}\right)^2
=C_n^2.
}
\]

The controls are exact:

```text
delta = 0       : maximal constructive fuzzy seam, zero edge current
delta = +/-pi/2 : maximal transport quadrature magnitude for fixed pair scale
delta = pi      : interface-null seam, zero edge current
```

## 4. Gauge covariance

Under a local vertex rephasing

\[
a_n\mapsto e^{i\chi_n}a_n,
\]

with link transformation

\[
\varphi_n\mapsto
\varphi_n+\chi_{n+1}-\chi_n,
\]

we have

\[
\delta_n\mapsto\delta_n.
\]

Therefore

\[
\boxed{
J_n,\ \mathcal C_n,\ \mathcal Q_n,\ j_{n+1/2}^{(h)}
}
\]

are gauge invariant.

## 5. Continuum current

Use the 02JK sampling

\[
\boxed{
a_n^{(h)}=\sqrt h\,\Psi(x_n,\Theta)}
\]

and the edge connection phase

\[
\varphi_n^{(h)}
=\int_{x_n}^{x_{n+1}}A(x,\Theta)\,dx.
\]

Let

\[
D_A=\partial_x-iA.
\]

Then

\[
L_n^*\Psi(x_{n+1})
=\Psi(x_n)+hD_A\Psi(x_n)+O(h^2).
\]

Hence

\[
\boxed{
j_{n+1/2}^{(h)}
\longrightarrow
\mathcal J(x_{n+1/2},\Theta)
}
\]

with

\[
\boxed{
\mathcal J
=2M(x)\operatorname{Im}\left(\Psi^*D_A\Psi\right).
}
\]

Writing \(\Psi=Re^{i\alpha}\),

\[
\boxed{
\mathcal J
=2MR^2(\partial_x\alpha-A).
}
\]

At the same time,

\[
\rho_n^{(h)}:=\frac{|a_n|^2}{h}
\longrightarrow
|\Psi|^2.
\]

Dividing the discrete continuity equation by \(h\) and taking the smooth limit gives

\[
\boxed{
\partial_\Theta |\Psi|^2
+\partial_x\mathcal J
=0.
}
\]

This is the continuum temporal-density continuity law of the phase-aware half-frame carrier.

## 6. Relation to the half-frame fuzzy density

02JK gives

\[
\rho_{F,n}^{(h)}=\frac{J_n}{2h}
\longrightarrow|\Psi|^2.
\]

Therefore both the vertex occupation density \(|a_n|^2/h\) and the glued-interface density \(J_n/(2h)\) converge to the same smooth bulk density. Their finite-mesh difference carries the local half-frame structure, while their common continuum limit supplies the density transported by \(\mathcal J\).

## 7. Onsager phase flow and density transport

02JG supplies a phase-only Onsager tangent of the form

\[
\boxed{
\left.\frac{da_n}{d\Theta}\right|_D
=i\,\dot\alpha_n^{(D)}a_n,
\qquad
\dot\alpha_n^{(D)}\in\mathbb R.
}
\]

Therefore exactly

\[
\boxed{
\left.\frac{d|a_n|^2}{d\Theta}\right|_D=0.
}
\]

For the combined Schrödinger--Onsager vector field, the instantaneous vertex-density balance is therefore inherited from the unitary edge current,

\[
\boxed{
\frac{d|a_n|^2}{d\Theta}
=j_{n-1/2}^{(h)}-j_{n+1/2}^{(h)}.
}
\]

The Onsager sector acts on the seam coherence/current phase coordinate while the Schrödinger sector supplies the instantaneous redistribution of vertex occupation.

Together with the 02JH seam-energy balance,

\[
\frac{dV_{\rm seam}}{d\Theta}=P_H-D_\alpha,
\]

the temporal-wave microdynamics carries two complementary conservation/balance equations:

```text
vertex density : exact continuity through edge current
seam energy    : reversible power minus Onsager dissipation
```

## 8. Falsification gates

Reference tests require:

- exact finite-path continuity for arbitrary complex state, positive mobilities and seam phases;
- exact norm conservation from boundary-current telescoping;
- invariance of edge currents under local vertex gauge rephasing;
- exact seam-quadrature circle identity;
- exact control values at \(\delta=0,\pm\pi/2,\pi\);
- exact vanishing of the density derivative under an arbitrary real phase-only tangent;
- second-order midpoint convergence of the discrete edge current to \(2M\operatorname{Im}(\Psi^*D_A\Psi)\) for a smooth field;
- compatibility with the 02JK continuum density limit.

Reference implementation: `src/idt/temporal_density_current.py`.
Reference tests: `tests/reference/test_temporal_density_current.py`.
Validation receipt: `validation/TEMPORAL_DENSITY_CURRENT_V0_1.json`.
