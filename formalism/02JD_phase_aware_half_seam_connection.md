# 02JD — Phase-Aware Half-Frame Seam Connection

Status: `FORMAL_CANDIDATE / GAUGE_COVARIANT_SEAM_GATE`

02J derives the half-frame quotient. This layer adds an edge-native phase to each neighboring seam while preserving the quotient dimension, amplitude norm decomposition and elapsed-measure support.

## 1. Seam phase

For each internal seam introduce

\[
\boxed{L_n=e^{i\varphi_n}\in U(1),\qquad n=1,\ldots,N-1.}
\]

Use the symmetric half-link lift

\[
\boxed{
Q_{\varphi}|n,R\rangle
=\frac{e^{+i\varphi_n/2}}{\sqrt2}|n,n+1\rangle,
}
\]

\[
\boxed{
Q_{\varphi}|n+1,L\rangle
=\frac{e^{-i\varphi_n/2}}{\sqrt2}|n,n+1\rangle.
}
\]

Boundary half-supports retain unit embedding. Since every seam row has squared norm one and disjoint half-support input, exactly

\[
\boxed{Q_{\varphi}Q_{\varphi}^{\dagger}=I_{N+1}.}
\]

## 2. Phase-aware overlap and seam defect

After the equal split `S_N`, the internal glued amplitude is

\[
\boxed{
b_n(\varphi_n)
=\frac{e^{+i\varphi_n/2}a_n+e^{-i\varphi_n/2}a_{n+1}}{2}.
}
\]

The complementary antisymmetric seam amplitude is

\[
\boxed{
d_n(\varphi_n)
=\frac{e^{+i\varphi_n/2}a_n-e^{-i\varphi_n/2}a_{n+1}}{2}.
}
\]

For every seam,

\[
\boxed{
|b_n|^2+|d_n|^2
=\frac{|a_n|^2+|a_{n+1}|^2}{2}.
}
\]

Together with the boundary half-supports this gives the same exact global identity as 02J,

\[
\boxed{
\sum_{j=0}^{N}|b_j|^2
+\sum_{n=1}^{N-1}|d_n|^2
=\sum_{n=1}^{N}|a_n|^2.
}
\]

## 3. Gauge covariance

Under local frame rephasing

\[
\boxed{a_n\mapsto e^{i\chi_n}a_n,}
\]

let the edge phase transform as

\[
\boxed{
\varphi_n\mapsto
\varphi_n+\chi_{n+1}-\chi_n.
}
\]

Then both seam amplitudes acquire only the common phase

\[
\boxed{
b_n\mapsto e^{i(\chi_n+\chi_{n+1})/2}b_n,}
\]

\[
\boxed{d_n\mapsto e^{i(\chi_n+\chi_{n+1})/2}d_n.}
\]

Therefore

\[
\boxed{|b_n|^2\ \text{and}\ |d_n|^2\ \text{are gauge invariant}.}
\]

This supplies an edge-native non-exact phase slot compatible with the half-frame topology.

## 4. Relative-phase control

Write

\[
a_n=r_ne^{i\alpha_n},
\qquad
a_{n+1}=r_{n+1}e^{i\alpha_{n+1}}.
\]

Then

\[
\boxed{
|b_n|^2
=\frac14\left[
r_n^2+r_{n+1}^2
+2r_nr_{n+1}\cos(\alpha_{n+1}-\alpha_n-\varphi_n)
\right],
}
\]

\[
\boxed{
|d_n|^2
=\frac14\left[
r_n^2+r_{n+1}^2
-2r_nr_{n+1}\cos(\alpha_{n+1}-\alpha_n-\varphi_n)
\right].
}
\]

Hence the gauge-invariant seam mismatch is

\[
\boxed{
\delta_n
=\alpha_{n+1}-\alpha_n-\varphi_n
\pmod{2\pi}.
}
\]

For equal magnitudes and `delta_n=0`, the seam is fully constructive. For equal magnitudes and `delta_n=pi`, the overlap support is null and the weight occupies the mismatch sector.

## 5. Connection versus exact vertex gradient

If

\[
\varphi_n=\beta_{n+1}-\beta_n
\]

for a globally defined vertex phase `beta`, the link is an exact discrete gradient and can be removed on an open path by rephasing. A non-exact connection requires independently specified edge-native phase data or nontrivial cycle topology.

The half-frame seam therefore supplies the correct typed location for the active 02I frontier:

\[
\boxed{
\text{edge-native non-exact temporal phase}
\longrightarrow
\text{phase-aware neighboring overlap}.
}
\]

## 6. Modular phase sectors

The support-count identity remains

\[
\Phi_N=2\pi N,
\qquad
\#V=N+1.
\]

The seam phase `varphi_n` is an internal edge coordinate and is not identified with the total phase budget by this gate. Particular `pi`, `2pi` or `4pi` assignments are tested separately.

## 7. Spin-half comparison target

A later comparison may test whether an admitted spinorial transport law yields a seam transformation whose physical state closes only after a `4pi` cycle. The present gate supplies only the gauge-covariant half-seam carrier required for that comparison.

## 8. Falsification gates

Reference tests require:

- `Q_phi Q_phi^dagger = I` for arbitrary finite seam phases;
- exact norm decomposition for arbitrary complex amplitudes and seam phases;
- gauge invariance of overlap/defect probabilities;
- exact `delta=0` constructive control;
- exact `delta=pi` interface-null control;
- zero-phase reduction to 02J;
- exact-gradient seam phases are removable on an open path.

Reference implementation: `src/idt/phase_aware_half_seam.py`.
Reference tests: `tests/reference/test_phase_aware_half_seam.py`.
