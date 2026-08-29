# QHTRI–Neutrino–Gravity Bridge v0.1

**Status:** CANDIDATE_TT_SOURCE_GATE  
**Reference gate:** `01AJ`  
**Scope:** algebraic source admissibility for the gravitational transverse-traceless sector.

## Typed chain

The bridge is represented as

\[
\mathrm{QHTRI/Euler\ phase}
\rightarrow
\mathrm{neutrino\ flavour/Hilbert\ evolution}
\rightarrow
T_{ij}^{(\nu,\,candidate)}
\xrightarrow{\Pi_{\rm TT}}
T_{ij}^{\rm TT}.
\]

The repository already carries the neutrino flavour/AUX superposition and subsequent flavour-Hamiltonian gates. This module adds the next typed operation: projection of a supplied symmetric spatial tensor into the radiative TT sector.

For a unit propagation direction \(n_i\),

\[
P_{ij}=\delta_{ij}-n_i n_j,
\]

and

\[
T_{ij}^{\rm TT}
=
\left(P_i{}^k P_j{}^l-\frac12 P_{ij}P^{kl}\right)T_{kl}.
\]

The executable gate requires

\[
\operatorname{tr}T^{\rm TT}=0,
\qquad
T_{ij}^{\rm TT}n^j=0,
\qquad
\lVert T^{\rm TT}\rVert_F>0.
\]

## Spin-2 phase carrier

For propagation along \(z\), the minimal phase-labelled quadrupole is

\[
Q(\phi)=A
\begin{pmatrix}
\cos 2\phi & \sin 2\phi & 0\\
\sin 2\phi & -\cos 2\phi & 0\\
0&0&0
\end{pmatrix}.
\]

It is already transverse and traceless, therefore

\[
\Pi_{\rm TT}Q(\phi)=Q(\phi),
\]

with polarization coordinates

\[
h_+\propto \cos 2\phi,
\qquad
h_\times\propto \sin 2\phi.
\]

## Reference tests

`tests/reference/test_01AJ_qhtri_neutrino_tt_source_gate.py` checks:

1. isotropic source rejection;
2. longitudinal source rejection;
3. plus-polarized TT admission with norm \(\sqrt2\);
4. cross-polarized TT admission with norm \(\sqrt2\);
5. exact \(2\phi\) phase-to-polarization map;
6. transversality and tracelessness for a generic symmetric source;
7. idempotence of \(\Pi_{\rm TT}\);
8. fail-closed behavior for a zero propagation direction.

## Next binding gate

The next unresolved dependency is

\[
\boxed{
\mathrm{BIND\_NEUTRINO\_HILBERT\_SOURCE\_TO\_PHYSICAL\_}T_{\mu\nu}
}
\]

including normalization, dimensions, conserved exchange current/Bianchi closure, and the linearized Einstein response. Until that binding is promoted, `01AJ` carries the status `CANDIDATE_TT_SOURCE_GATE`.
