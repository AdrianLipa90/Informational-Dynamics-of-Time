# 09C — Tetra-SIC Shannon–Onsager Packet Flow

Status: `FORMAL_CANDIDATE / EXACT_SIC_TO_ONSAGER_CROSSWALK / PHYSICAL_RATE_SOURCE_OPEN`

Date: 2026-09-24

## 1. Tetrahedral SIC coordinates for one binary-state packet

For the four tetrahedral Bloch directions \(\mathbf n_a\), define

\[
\boxed{
p_a
=
\frac14(1+\mathbf r\cdot\mathbf n_a).
}
\]

The exact reconstruction is

\[
\boxed{
\mathbf r
=
3\sum_{a=0}^{3}p_a\mathbf n_a.
}
\]

Thus the three Bloch coordinates are equivalent to the four normalized tetra-SIC probabilities subject to \(\sum_a p_a=1\).

For the tetrahedral pure states themselves the probabilities are a permutation of

\[
\left(\frac12,\frac16,\frac16,\frac16\right),
\]

so the strictly-positive domain required by 01D is satisfied.

## 2. S4-symmetric detailed-balance control sector

On the four SIC outcomes, impose the maximally symmetric complete-graph mobility:

\[
M_{ab}=m>0
\qquad
(a\ne b).
\]

This is the unique off-diagonal scalar form invariant under every permutation of the four outcome labels, up to the overall positive rate \(m\).

The corresponding continuous-time generator has

\[
Q_{ab}=m
\quad(a\ne b),
\qquad
Q_{aa}=-3m,
\]

with uniform stationary state

\[
\pi_a=\frac14.
\]

Therefore

\[
\boxed{
\dot p_a=m(1-4p_a).
}
\]

This is exactly inside the 01D Shannon–Onsager detailed-balance sector.

## 3. Exact Bloch radial flow

Differentiate the SIC reconstruction:

\[
\dot{\mathbf r}
=
3\sum_a\dot p_a\mathbf n_a.
\]

Using \(\sum_a\mathbf n_a=0\) and the tetrahedral reconstruction identity gives

\[
\boxed{
\dot{\mathbf r}
=
-4m\mathbf r.
}
\]

Thus the S4-symmetric dissipative control sector is exactly radial in the Bloch ball. No preferred spatial axis is introduced.

This is a formal control sector, not a claim that physical spacetime evolution is depolarization.

## 4. Elapsed-state packet velocity

For

\[
x=\frac{\ell}{2}(1,\mathbf r),
\]

the product rule gives

\[
\boxed{
\dot x^0=\frac12\dot\ell,
}
\]

and

\[
\boxed{
\dot{\mathbf x}
=
\frac12
\left(
\dot\ell\,\mathbf r
+
\ell\,\dot{\mathbf r}
\right).
}
\]

In the S4-symmetric Onsager control sector,

\[
\boxed{
\dot{\mathbf x}
=
\frac12
(\dot\ell-4m\ell)\mathbf r.
}
\]

The elapsed-scale rate \(\dot\ell\) is supplied by the separate activity/lapse/clock branch. This file does not invent it.

## 5. Canonical tetra-frame control

Take four tetrahedral directions with one common elapsed scale and one common constant rate \(m\). Then

\[
\mathbf r_a(\Theta)
=
q(\Theta)\mathbf n_a,
\qquad
q(\Theta)=e^{-4m\Theta}.
\]

If

\[
s(\Theta)=\frac{\ell(\Theta)}{\ell(0)},
\]

the relative coframe to the initial tetra frame is

\[
\boxed{
e(\Theta)
=
\operatorname{diag}
\bigl(
s,
sq,
sq,
sq
\bigr).
}
\]

Its exterior-square representation is

\[
\boxed{
C_2(e)
=
\operatorname{diag}
\bigl(
s^2q,s^2q,s^2q,
s^2q^2,s^2q^2,s^2q^2
\bigr).
}
\]

This supplies an exact 3+3 isotropic control trajectory for the coframe/bivector bridge.

A purely time-dependent homogeneous control is not by itself evidence for spacetime curvature or cosmology.

## 6. What remains open

The exact crosswalk closes:

\[
\text{Bloch packet}
\leftrightarrow
\text{tetra-SIC probabilities}
\to
\text{01D Onsager flow}
\to
\dot{\mathbf r}
\to
\dot x
\to
\dot E.
\]

Still open:

- the physical transition-rate/mobility source \(m\);
- non-S4 inhomogeneous mobility generated from physical relations;
- reversible/Berry contribution on the packet field;
- preservation and gluing of a physical four-packet frame field;
- gravity/source normalization and empirical validation.

Reference implementation:

`src/idt/tetra_sic_packet_onsager.py`

Reference tests:

`tests/reference/test_tetra_sic_packet_onsager.py`


## 7. 00C/02B mobility binding

The overall tetra transition rate need not be an independent parameter.

00C already defines the symmetric pair mobility

\[
\boxed{
M_{ab}
=
\frac{
\sqrt{\rho_R(a)\rho_R(b)}
}{
\tfrac12[\eta_R(a)+\eta_R(b)]
}.
}
\]

On the tetrahedral complete graph, the zero-drive generator is therefore obtained by assigning the six edge rates \(M_{ab}\).

The general symmetric packet flow becomes

\[
\boxed{
\dot p=pQ[\rho_R,\eta_R],
}
\]

followed exactly by

\[
\boxed{
\dot{\mathbf r}
=
3\sum_a\dot p_a\mathbf n_a.
}
\]

For uniform relational fields

\[
\rho_R(a)=\rho_0,
\qquad
\eta_R(a)=\eta_0,
\]

all six mobilities coincide:

\[
\boxed{
M=\frac{\rho_0}{\eta_0}.
}
\]

Therefore the S4-symmetric radial control law is no longer written with a free rate:

\[
\boxed{
\dot{\mathbf r}
=
-4\frac{\rho_0}{\eta_0}\mathbf r.
}
\]

and

\[
q(\Theta)
=
\exp\left[
-4\frac{\rho_0}{\eta_0}\Theta
\right]
\]

when the uniform fields are constant in intrinsic time.

This closes the symmetric mobility source **within the declared 00C zero-drive sector**. It does not derive the physical relational density/viscosity fields themselves.

For heterogeneous positive \(\rho_R,\eta_R\), the six edge mobilities remain explicit and the implementation preserves probability normalization rather than collapsing them to one scalar.
