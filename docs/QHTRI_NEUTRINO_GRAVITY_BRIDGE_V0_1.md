# QHTRI–Neutrino–Gravity Bridge v0.2

**Status:** PHYSICAL_TENSOR_KINEMATIC_CHAIN  
**Reference gates:** `01AJ`, `01AK`, `01AL`, `01AM`, `01AN`, `01AO`  
**Scope:** typed source chain from flavour-Hilbert dynamics through physical ultrarelativistic stress normalization, TT projection, integrated conservation, and SI-normalized leading far-zone linearized Einstein response.

## Typed chain

\[
\mathrm{QHTRI/Euler\ phase}
\rightarrow
\mathrm{neutrino\ flavour/Hilbert\ evolution}
\rightarrow
T_{\mu\nu}^{(\nu)}
\xrightarrow{\Pi_{\rm TT}}
T_{ij}^{\rm TT}
\rightarrow
h_{ij}^{\rm TT}.
\]

For a unit propagation direction \(n_i\),

\[
P_{ij}=\delta_{ij}-n_i n_j,
\qquad
T_{ij}^{\rm TT}
=
\left(P_i{}^k P_j{}^l-\frac12 P_{ij}P^{kl}\right)T_{kl}.
\]

## 01AJ — TT source gate

For propagation along \(z\), the phase-labelled spin-2 carrier

\[
Q(\phi)=A
\begin{pmatrix}
\cos 2\phi & \sin 2\phi & 0\\
\sin 2\phi & -\cos 2\phi & 0\\
0&0&0
\end{pmatrix}
\]

maps exactly to

\[
h_+\propto\cos 2\phi,
\qquad
h_\times\propto\sin 2\phi.
\]

The executable gate enforces tracelessness, transversality, nonzero TT norm, projection idempotence, and fail-closed direction validation.

## 01AK — flavour-tensor commutator gate

For a time-independent flavour-space tensor operator \(\hat T_{ij}\) and \(\hbar=1\),

\[
\frac{d}{dt}\langle \hat T_{ij}\rangle
=
i\langle[\hat H_\nu,\hat T_{ij}]\rangle.
\]

A flavour-central source \(\hat T_{ij}=c_{ij}\mathbb I\) is invariant under internal flavour rotation. Dynamic tensor modulation therefore requires a non-central Hermitian tensor component with

\[
[\hat H_\nu,\hat T_{ij}]\neq0.
\]

## 01AL — ultrarelativistic stream anisotropy gate

The normalized spatial stress shape for positive ultrarelativistic streams is

\[
S_{ij}
=
\frac{\sum_a w_a n_i^{(a)}n_j^{(a)}}{\sum_a w_a}.
\]

Equal tetrahedral streams yield \(S_{ij}=\delta_{ij}/3\) and zero TT projection. Pure internal flavour redistribution that preserves the total weight of every momentum direction leaves \(S_{ij}\) unchanged. Direction-correlated redistribution or a non-central tensor operator can change the TT source.

## 01AM — SI-normalized linearized Einstein response

For a localized source evaluated at one retarded source time,

\[
\mathcal T_{ij}(t_r)=\int T_{ij}(t_r,\mathbf x')\,d^3x',
\]

and the leading far-zone linearized response is

\[
\boxed{
h_{ij}^{\rm TT}(t,r)
=
\frac{4G}{c^4 r}
\mathcal T_{ij}^{\rm TT}(t_r)
}.
\]

`01AM` checks the SI prefactor, dimensionless strain, linear energy scaling, inverse-distance scaling, isotropic/tetrahedral null controls, and nonzero transverse response.

## 01AN — physical ultrarelativistic neutrino stress-energy

Using \(x^0=ct\), a massless directional packet with local energy density \(u_a\) and unit direction \(n_a\) carries

\[
k_a^\mu=(1,\mathbf n_a),
\qquad
T^{\mu\nu}_{(a)}=u_a k_a^\mu k_a^\nu.
\]

For a discrete source,

\[
T^{\mu\nu}_{\nu}(x,t)
=
\sum_a u_a(x,t)k_a^\mu k_a^\nu,
\]

and after volume integration,

\[
\mathcal T^{\mu\nu}_{\nu}
=
\sum_a E_a k_a^\mu k_a^\nu.
\]

Hence

\[
\mathcal T^{00}=\sum_aE_a,
\qquad
\mathcal T^{0i}=\sum_aE_a n_a^i,
\qquad
\mathcal T^{ij}=\sum_aE_a n_a^i n_a^j.
\]

The reference gate verifies the massless trace relation

\[
\mathcal T^{00}-\sum_i\mathcal T^{ii}=0,
\]

future-nonspacelike total four-momentum, tetrahedral isotropy, local energy-density normalization, and exact invariance under flavour redistribution that preserves every directional energy total.

## 01AO — conserved phase-quadrupole family

An explicit transverse eight-stream family provides a spin-2 phase carrier while preserving total energy and net momentum.  Define four opposite-pair energies

\[
W_x=\frac E4+A\cos2\phi,
\qquad
W_y=\frac E4-A\cos2\phi,
\]

\[
W_{d+}=\frac E4+A\sin2\phi,
\qquad
W_{d-}=\frac E4-A\sin2\phi,
\qquad
0\le A\le\frac E4.
\]

Each pair is split equally between opposite directions. Therefore, for every \(\phi\),

\[
\sum_aE_a=E,
\qquad
\sum_aE_a\mathbf n_a=0,
\]

while the TT coordinates are exactly

\[
\frac{\mathcal T_{xx}-\mathcal T_{yy}}2=A\cos2\phi,
\qquad
\mathcal T_{xy}=A\sin2\phi,
\]

and

\[
\|\mathcal T^{\rm TT}\|_F=\sqrt2 A.
\]

A phase change within this family has

\[
\frac{dP^\mu}{dt}=0
\]

at the integrated source level while the quadrupolar stress changes. Thus integrated energy-momentum conservation is compatible with a time-dependent TT source.

## Current dependency frontier

The next source-side theorem is the local transport law generating the directional redistribution:

\[
\boxed{
\mathrm{QHTRI/Euler}
\rightarrow
u\text{-phase-space transport}
\rightarrow
\partial_\mu T^{\mu\nu}_{(\nu)}=J^\nu_{\rm exchange}
}
\]

with the closed-sector limit \(J^\nu_{\rm exchange}=0\), causal propagation, and an explicit phase-to-directional-occupation operator. Once this local transport binding is closed, the resulting retarded stress history feeds directly through `01AM`.
