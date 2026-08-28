# 02JG — Onsager Half-Seam Phase Locking

Status: `FORMAL_CANDIDATE / EXACT_CONDITIONAL_SEAM_DEFECT_DESCENT_GATE`

This gate combines three already typed ingredients:

1. the activity-derived intrinsic temporal measure `dTheta`;
2. the phase-aware half-seam mismatch of 02JD;
3. the positive symmetric Onsager response sector of 01A/01D.

The goal is to test whether local phase synchronization can arise as descent of the gauge-invariant seam-defect functional rather than being inserted as an external phase-locking rule.

## 1. Gauge-invariant seam defect

For neighboring frame amplitudes

\[
a_n=r_ne^{i\alpha_n},
\qquad
a_{n+1}=r_{n+1}e^{i\alpha_{n+1}},
\]

and seam connection phase `varphi_n`, 02JD defines

\[
\boxed{
\delta_n
=\alpha_{n+1}-\alpha_n-\varphi_n
\pmod{2\pi}.
}
\]

The complementary seam-defect amplitude satisfies

\[
\boxed{
V_n(\delta_n)
:=|d_n|^2
=\frac14\left[
r_n^2+r_{n+1}^2
-2r_nr_{n+1}\cos\delta_n
\right].
}
\]

`V_n` is non-negative and gauge invariant.

At fixed positive magnitudes,

\[
\boxed{
\frac{\partial V_n}{\partial\delta_n}
=\frac12r_nr_{n+1}\sin\delta_n.
}
\]

## 2. Onsager descent in intrinsic temporal measure

Let the seam mismatch be an admitted scalar response coordinate with positive Onsager mobility

\[
\boxed{\mu_n>0.}
\]

Use the activity-derived intrinsic temporal coordinate `Theta` as the evolution measure and impose the symmetric dissipative response

\[
\boxed{
D_\Theta\delta_n
=-\mu_n\frac{\partial V_n}{\partial\delta_n}.
}
\]

Therefore

\[
\boxed{
D_\Theta\delta_n
=-\frac{\mu_nr_nr_{n+1}}2\sin\delta_n.
}
\]

This is the exact one-seam sine-locking equation induced by the declared defect functional and positive Onsager response.

## 3. Lyapunov identity

Along the flow,

\[
\frac{dV_n}{d\Theta}
=\frac{\partial V_n}{\partial\delta_n}
D_\Theta\delta_n.
\]

Substituting the Onsager law gives

\[
\boxed{
\frac{dV_n}{d\Theta}
=-\mu_n\left(
\frac{\partial V_n}{\partial\delta_n}
\right)^2
\le0.
}
\]

Explicitly,

\[
\boxed{
\frac{dV_n}{d\Theta}
=-\frac{\mu_n r_n^2r_{n+1}^2}{4}
\sin^2\delta_n
\le0.
}
\]

Thus `V_n` is an exact Lyapunov function on the fixed-magnitude seam sector.

## 4. Fixed points and stability

The stationary points satisfy

\[
\sin\delta_n=0,
\]

so

\[
\delta_n=k\pi.
\]

The second derivative is

\[
\boxed{
\frac{\partial^2V_n}{\partial\delta_n^2}
=\frac12r_nr_{n+1}\cos\delta_n.
}
\]

For positive magnitudes:

- `delta_n = 0 mod 2pi` is a local minimum and stable locking point;
- `delta_n = pi mod 2pi` is a local maximum and unstable interface-null point.

At the stable point,

\[
\boxed{d_n=0}
\]

for equal-magnitude neighboring frames, and the seam weight is carried by the constructive overlap sector.

## 5. Small-mismatch relaxation

Near the stable point,

\[
\sin\delta_n=\delta_n+O(\delta_n^3).
\]

Hence

\[
\boxed{
D_\Theta\delta_n
=-K_n\delta_n+O(\delta_n^3),
\qquad
K_n:=\frac{\mu_nr_nr_{n+1}}2>0.
}
\]

The linearized relaxation is

\[
\boxed{
\delta_n(\Theta)
\sim
\delta_n(0)e^{-K_n\Theta}.
}
\]

The locking scale is intrinsic because it is measured against the derived temporal coordinate `Theta`.

## 6. Network form

For a chain of phase-aware half seams, define

\[
\boxed{
V_{\rm seam}
=\sum_{n=1}^{N-1}V_n(\delta_n).
}
\]

For diagonal positive seam mobilities,

\[
D_\Theta\delta_n
=-\mu_n\partial_{\delta_n}V_{\rm seam}.
\]

Then

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=-\sum_{n=1}^{N-1}\mu_n
\left(\partial_{\delta_n}V_{\rm seam}\right)^2
\le0.
}
\]

The multidimensional extension with a positive-semidefinite Onsager matrix `G_delta` is

\[
\boxed{
D_\Theta\boldsymbol\delta
=-G_\delta\nabla_\delta V_{\rm seam},
}
\]

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=-(\nabla_\delta V_{\rm seam})^T
G_\delta
(\nabla_\delta V_{\rm seam})
\le0.
}
\]

## 7. Winding-weighted resonant seam

TIR PR #96 supplies a common-cycle relative-rate theorem. If two phase fibers close with winding integers

\[
m_i,m_j,
\]

their average intrinsic phase-rate ratio on a common cycle is

\[
\frac{\bar\Omega_i}{\bar\Omega_j}
=\frac{m_i}{m_j}.
\]

To test local resonant locking, define the winding-weighted gauge-invariant mismatch

\[
\boxed{
\Delta_{ij}
:=m_j\varphi_i
-m_i\varphi_j
-\mathcal A_{ij}
\pmod{2\pi},
}
\]

where `A_ij` is an admitted edge-native relative connection phase.

Use the periodic defect potential

\[
\boxed{
V_{ij}^{(m)}
=\rho_{ij}\left(1-\cos\Delta_{ij}\right),
\qquad
\rho_{ij}>0.
}
\]

With positive Onsager mobility `mu_ij`,

\[
\boxed{
D_\Theta\Delta_{ij}
=-\mu_{ij}\rho_{ij}\sin\Delta_{ij}.
}
\]

The same Lyapunov identity follows,

\[
\boxed{
\frac{dV_{ij}^{(m)}}{d\Theta}
=-\mu_{ij}\rho_{ij}^2\sin^2\Delta_{ij}
\le0.
}
\]

## 8. Local rational phase locking

At a locked seam,

\[
\boxed{D_\Theta\Delta_{ij}=0.}
\]

Differentiating the mismatch definition gives

\[
\boxed{
m_j\Omega_i
-m_i\Omega_j
-\Omega_{\mathcal A,ij}=0,
}
\]

where

\[
\Omega_{\mathcal A,ij}:=D_\Theta\mathcal A_{ij}.
\]

If the relative connection phase is covariantly stationary on the locked sector,

\[
\boxed{\Omega_{\mathcal A,ij}=0,}
\]

then

\[
\boxed{
\frac{\Omega_i}{\Omega_j}
=\frac{m_i}{m_j}
}
\]

pointwise wherever `Omega_j != 0`.

This is the exact conditional bridge from the TIR common-cycle average winding ratio to a local intrinsic phase-rate ratio.

## 9. Relation to Kuramoto structure

The one-seam equation

\[
D_\Theta\delta=-K\sin\delta
\]

has the standard sine-coupling form of a two-phase locking sector. In this gate the sine term is not inserted as a phenomenological oscillator rule: it follows by differentiating the declared half-seam defect functional and applying the existing positive Onsager response architecture.

A broader Kuramoto network comparison remains downstream of the explicit mapping between phase-node variables, seam connections, mobility matrix and any measured oscillator system.

## 10. Evidence boundary

The exact algebraic claims of this gate are conditional on:

- the 02JD phase-aware seam amplitudes;
- fixed positive frame magnitudes for the one-seam Lyapunov/stability theorem;
- adoption of `V=|d|^2` as the seam mismatch scalar supplied to the symmetric Onsager response;
- positive Onsager mobility;
- the activity-derived intrinsic temporal measure `Theta`;
- for rational local locking, the declared winding-weighted mismatch and a stationary relative connection phase.

The gate establishes a synchronization mechanism inside the declared model. Experimental identification of the seam variables with a physical oscillator system remains a separate evidence layer.

## 11. Next gate

The next test is to couple the locking law back to the Schrödinger frame amplitudes, allowing `r_n(Theta)` to evolve rather than remain fixed, and test whether the full amplitude+phase system preserves norm while decreasing the seam mismatch functional.

Reference implementation: `src/idt/onsager_half_seam_phase_locking.py`.
Reference tests: `tests/reference/test_onsager_half_seam_phase_locking.py`.
Validation receipt: `validation/ONSAGER_HALF_SEAM_PHASE_LOCKING_V0_1.json`.
