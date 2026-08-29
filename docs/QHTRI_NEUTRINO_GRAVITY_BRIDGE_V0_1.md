# QHTRI–Neutrino–Gravity Bridge v0.4

**Status:** ROTOR_LAMBDA_LOCAL_CONSERVATIVE_SOURCE_CHAIN  
**Reference gates:** `01AJ`, `01AK`, `01AL`, `01AM`, `01AN`, `01AO`, `01AP`, `01AQ`  
**Scope:** typed source chain from the QHTRI/Euler two-rotor state through Lambda-coupled relative neutrino oscillation phase, physical ultrarelativistic stress normalization, local conservative phase-space redistribution, TT projection, and SI-normalized leading far-zone linearized Einstein response.

## Typed chain

\[
(\theta_+,\theta_-)
\rightarrow
(\tau,\chi)_{\rm Minkowski\ spin}
\xrightarrow{\Lambda}
\phi_\nu
\rightarrow
C_a
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

The reference gate verifies

\[
\mathcal T^{00}-\sum_i\mathcal T^{ii}=0,
\]

future-nonspacelike total four-momentum, tetrahedral isotropy, local energy-density normalization, and exact invariance under flavour redistribution that preserves every directional energy total.

## 01AO — conserved phase-quadrupole family

Define four opposite-pair energies

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

Each pair is split equally between opposite directions. Therefore

\[
\sum_aE_a=E,
\qquad
\sum_aE_a\mathbf n_a=0,
\]

while

\[
\frac{\mathcal T_{xx}-\mathcal T_{yy}}2=A\cos2\phi,
\qquad
\mathcal T_{xy}=A\sin2\phi,
\qquad
\|\mathcal T^{\rm TT}\|_F=\sqrt2 A.
\]

A phase change within this family has

\[
\frac{dP^\mu}{dt}=0
\]

at the integrated source level while the quadrupolar stress changes.

## 01AP — local conservative phase-space transport

For fixed massless directions \(k_a^\mu=(1,\mathbf n_a)\), let the local stream energy densities obey

\[
(\partial_t+c\,\mathbf n_a\cdot\nabla)u_a=C_a.
\]

Then

\[
\partial_\mu T^{\mu\nu}
=
\frac1c\sum_a k_a^\nu C_a.
\]

A local redistribution is closed under energy-momentum conservation whenever

\[
\boxed{
\sum_a C_a=0,
\qquad
\sum_a C_a\mathbf n_a=0.
}
\]

For the `01AO` phase family,

\[
\dot W_x=-2A\sin2\phi\,\dot\phi,
\qquad
\dot W_y=+2A\sin2\phi\,\dot\phi,
\]

\[
\dot W_{d+}=+2A\cos2\phi\,\dot\phi,
\qquad
\dot W_{d-}=-2A\cos2\phi\,\dot\phi.
\]

Splitting each rate equally across its opposite pair gives, identically,

\[
\sum_a C_a=0,
\qquad
\sum_a C_a\mathbf n_a=0,
\qquad
\partial_\mu T^{\mu\nu}=0
\]

for the homogeneous local collision step. `01AP` also verifies free-streaming closure of the convective derivative and exposes any nonconserving collision as a nonzero exchange four-moment.

## 01AQ — two rotors, Lambda board, neutrino metronomes

The two cylinder/rotor phases are represented by \(\theta_+\) and \(\theta_-\). Their common and differential coordinates are

\[
\boxed{
\tau=\frac{\theta_++\theta_-}{2},
\qquad
\chi=\frac{\theta_+-\theta_-}{2}
}
\]

with the exact Minkowski-form identity

\[
\boxed{
\tau^2-\chi^2=\theta_+\theta_-.
}
\]

Counter-rotation \((\theta_+,\theta_-)\mapsto(\theta_++\delta,\theta_- -\delta)\) leaves \(\tau\) fixed and advances the spin coordinate \(\chi\mapsto\chi+\delta\).

The Lambda board binds this rotor state to the neutrino carrier by

\[
\boxed{
A=\Lambda\frac E4,
\qquad
0\le\Lambda\le1,
}
\]

\[
\boxed{
\phi=\phi_0+g_\tau\tau+g_\chi\chi,
\qquad
\dot\phi=g_\tau\dot\tau+g_\chi\dot\chi.
}
\]

The canonical pure-spin setting is \(g_\tau=0\), \(g_\chi=1\), hence \(\phi=\phi_0+\chi\). The three neutrino-metronome channels carry relative phase shifts

\[
\delta\varphi_f=q_f\phi,
\qquad
\sum_f q_f=0,
\]

so the drive lives in relative flavour phase rather than a common \(U(1)\) phase.

Substituting \((A,\phi,\dot\phi)\) into `01AO` and `01AP` gives the directional occupation and collision rates exactly:

\[
(\theta_+,\theta_-)
\rightarrow
(\tau,\chi)
\xrightarrow{\Lambda}
(A,\phi,\dot\phi)
\rightarrow
C_a.
\]

`01AQ` verifies the rotor identity, pure counter-rotation, traceless relative flavour drive, positivity bound \(A\le E/4\), exact numerical equality with the `01AO` source tensor, exact equality with the `01AP` transport rates, zero collision four-moment, and the spin-2 coordinates

\[
T_+^{TT}=A\cos2\chi,
\qquad
T_\times^{TT}=A\sin2\chi
\]

for the canonical pure-spin Lambda board.

## Current dependency frontier

The model-level source chain is now executable as

\[
\boxed{
(\theta_+,\theta_-)
\rightarrow
(\tau,\chi)_{\rm Minkowski\ spin}
\xrightarrow{\Lambda}
\delta\varphi_\nu
\rightarrow
C_a
\rightarrow
T_{\mu\nu}^{(\nu)}
\rightarrow
h_{ij}^{TT}.
}
\]

The next gate is the physical calibration of the Lambda operator and rotor variables against an experimentally identifiable neutrino interaction/observable, fixing \(\Lambda\), \(g_\tau\), \(g_\chi\), and the relative flavour gains from data rather than convention.

The repository may suggest controlled gravitational-wave emission from this source chain, yet does not state it as an established result until the Lambda/neutrino binding is experimentally supported.
