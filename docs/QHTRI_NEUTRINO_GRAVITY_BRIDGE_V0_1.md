# QHTRI–Neutrino–Gravity Bridge v0.1

**Status:** CANDIDATE_TT_SOURCE_CHAIN  
**Reference gates:** `01AJ`, `01AK`, `01AL`, `01AM`  
**Scope:** typed source admissibility from flavour-Hilbert dynamics through TT projection to a SI-normalized leading far-zone linearized Einstein response.

## Typed chain

\[
\mathrm{QHTRI/Euler\ phase}
\rightarrow
\mathrm{neutrino\ flavour/Hilbert\ evolution}
\rightarrow
\langle \hat T_{ij}^{(\nu)}\rangle
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

The executable gate enforces tracelessness, transversality, nonzero TT norm, projection idempotence, and fail-closed direction validation. For propagation along \(z\), the phase-labelled spin-2 carrier

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

`01AK` verifies an explicit non-central quadrupole reaching the `01AJ` gate.

## 01AL — ultrarelativistic stream anisotropy gate

The normalized spatial stress shape for positive ultrarelativistic streams is

\[
S_{ij}
=
\frac{\sum_a w_a n_i^{(a)}n_j^{(a)}}{\sum_a w_a}.
\]

Equal tetrahedral streams yield \(S_{ij}=\delta_{ij}/3\) and zero TT projection. Pure internal flavour redistribution that preserves the total weight of every momentum direction leaves \(S_{ij}\) unchanged. Direction-correlated redistribution or a non-central tensor operator can change the TT source.

## 01AM — SI-normalized linearized Einstein response

For a localized source evaluated at one retarded source time, define the integrated spatial stress

\[
\mathcal T_{ij}(t_r)=\int T_{ij}(t_r,\mathbf x')\,d^3x'.
\]

The leading far-zone linearized response used by the executable gate is

\[
\boxed{
h_{ij}^{\rm TT}(t,r)
=
\frac{4G}{c^4 r}
\mathcal T_{ij}^{\rm TT}(t_r)
}.
\]

`01AM` checks the exact SI prefactor, dimensionless strain, linear energy scaling, inverse-distance scaling, isotropic/tetrahedral null controls, and a nonzero response for a transverse ultrarelativistic stream.

## Current dependency frontier

The Einstein-response normalization is now executable once a physical integrated stress history is supplied. The remaining source-side dependency is

\[
\boxed{
\mathrm{DERIVE\_QHTRI\_NEUTRINO\_TIME\_DEPENDENT\_PHYSICAL\_}T_{\mu\nu}(x,t)
}
\]

with explicit local energy density, flavour/momentum coupling, conservation/exchange current and Bianchi closure. After that binding, the retarded source history can be propagated through `01AM` without an additional gravitational normalization parameter.
