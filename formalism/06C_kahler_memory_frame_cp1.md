# 06C — CP1 Kähler Memory Frame

Status: `MEMORY_FRONTIER_CANDIDATE / KÄHLER_FRAME_REFERENCE_SUBCLASS`

This layer refines the general Hermitian-observable memory projection by deriving a local two-axis memory frame directly from the \(\mathbb{CP}^1\) / Bloch geometry already present in the temporal phase formalism.

## 1. T019J — Bloch representation and Fubini–Study logarithm

For a normalized qubit state \(|\psi\rangle\), let \(\mathbf n\in S^2\) be its Bloch vector. For two non-antipodal states \(a,b\), define
\[
\theta_{ab}=\arccos(\mathbf n_a\cdot\mathbf n_b).
\]
The pure-state Fubini–Study distance is
\[
\boxed{d_{FS}(a,b)=\frac{\theta_{ab}}{2}}.
\]
The corresponding half-angle tangent logarithm at \(a\) is
\[
\boxed{
\xi^{FS}_{a\to b}
=\frac12\frac{\theta_{ab}}{\sin\theta_{ab}}
\left(\mathbf n_b-\cos\theta_{ab}\,\mathbf n_a\right),
}
\]
with
\[
\|\xi^{FS}_{a\to b}\|=d_{FS}(a,b).
\]

## 2. T019K — Kähler-conjugate memory dyad

For the first admitted nonzero displacement, define
\[
\mathbf e_Q
=\frac{\xi^{FS}}{\|\xi^{FS}\|},
\qquad
\boxed{\mathbf e_P=\mathbf n\times\mathbf e_Q}.
\]
Then \((\mathbf e_Q,\mathbf e_P)\) is an oriented orthonormal tangent dyad in Bloch coordinates, and \(\mathbf e_P\) is the \(\mathbb{CP}^1\) complex-structure rotation of \(\mathbf e_Q\) in this reference chart.

For any later non-antipodal event arriving at the same anchor, define the local memory displacement
\[
\boxed{
\delta m
=\xi^{FS}\cdot\mathbf e_Q
+i\,\xi^{FS}\cdot\mathbf e_P.
}
\]
Because the dyad spans the tangent plane,
\[
\boxed{|\delta m|=d_{FS}}
\]
for the local event displacement represented by \(\xi^{FS}\).

## 3. T019L — geodesic frame transport

Between anchors \(\mathbf n_a\) and \(\mathbf n_b\), let \(R_{b\leftarrow a}\in SO(3)\) be the minimal rotation that maps \(\mathbf n_a\) to \(\mathbf n_b\) along the selected non-antipodal geodesic. The memory frame propagates as
\[
\boxed{
\mathbf e_Q^{(b)}=R_{b\leftarrow a}\mathbf e_Q^{(a)},
\qquad
\mathbf e_P^{(b)}=R_{b\leftarrow a}\mathbf e_P^{(a)}.
}
\]
This preserves tangency, orthonormality and orientation,
\[
\mathbf e_P^{(b)}
=\mathbf n_b\times\mathbf e_Q^{(b)}.
\]
For \(\mathbb{CP}^1\), this minimal great-circle rotation is the discrete reference realization of Levi–Civita/Kähler parallel transport along the chosen geodesic segment.

## 4. Relation to the general memory projection

The general \((Q_M,P_M)\) projection remains available as the broad operator family. The CP1 reference subclass supplies a geometry-derived local frame and normalization for the memory-plane displacement before it enters the already-defined event action
\[
\Delta v_{M,n}=q_n\delta m_n.
\]

Antipodal points are a chart/geodesic ambiguity and fail closed in the reference implementation. Reference controls are recorded in `validation/KAHLER_MEMORY_FRAME_CP1_V0_1.json`.
