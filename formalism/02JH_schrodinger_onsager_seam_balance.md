# 02JH — Schrödinger–Onsager Half-Seam Balance

Status: `FORMAL_CANDIDATE / EXACT_INSTANTANEOUS_BALANCE_GATE`

This gate couples the reversible frame evolution of 02E to the dissipative phase-locking sector of 02JG without replacing the activity-derived intrinsic temporal coordinate `Theta`.

## 1. Phase-aware seam operator

For a frame state

\[
|\psi\rangle=(\psi_1,\ldots,\psi_N)^T
\]

and edge-native seam phases

\[
\boldsymbol\varphi=(\varphi_1,\ldots,\varphi_{N-1}),
\]

define the phase-aware seam difference operator `B_varphi` by

\[
\boxed{
(B_\varphi\psi)_n
=\frac12\left(
 e^{+i\varphi_n/2}\psi_n
-e^{-i\varphi_n/2}\psi_{n+1}
\right).
}
\]

The seam stiffness is

\[
\boxed{
K_\varphi=B_\varphi^\dagger B_\varphi\succeq0.
}
\]

Hence the total half-seam defect is the quadratic functional

\[
\boxed{
V_{\rm seam}[\psi]
=\|B_\varphi\psi\|^2
=\psi^\dagger K_\varphi\psi
=\sum_{n=1}^{N-1}|d_n|^2.
}
\]

For a normalized whole-frame state, 02J identifies this sum with the total antisymmetric seam-defect weight complementary to the glued sector.

## 2. Reversible Schrödinger sector

Let `H=H^dagger` be any admitted finite-frame Hamiltonian, including the declared Zeta–Collatz candidate. The reversible sector evolves against the already-derived intrinsic temporal measure,

\[
\boxed{
i\partial_\Theta\psi=H\psi.
}
\]

Equivalently,

\[
\dot\psi_H=-iH\psi.
\]

The frame norm is exactly conserved,

\[
\boxed{
\frac{d}{d\Theta}\|\psi\|^2\bigg|_H=0.
}
\]

The seam functional need not be conserved. Its reversible power is

\[
\boxed{
P_H
:=\frac{dV_{\rm seam}}{d\Theta}\bigg|_H
=i\psi^\dagger[H,K_\varphi]\psi.
}
\]

Thus the Schrödinger sector can move weight into or out of the seam-defect sector whenever

\[
[H,K_\varphi]\neq0.
\]

If

\[
[H,K_\varphi]=0,
\]

then the reversible sector preserves `V_seam` exactly.

## 3. Node-phase gradient of the seam functional

Write

\[
\psi_n=r_ne^{i\alpha_n}.
\]

For edge mismatch

\[
\delta_n=\alpha_{n+1}-\alpha_n-\varphi_n,
\]

the edge derivative is

\[
\boxed{
g_n:=\frac{\partial V_{\rm seam}}{\partial\delta_n}
=\frac12r_nr_{n+1}\sin\delta_n.
}
\]

Let `D` be the oriented path incidence matrix with row `n` equal to `(-1,+1)` on nodes `(n,n+1)`. Then

\[
\boldsymbol\delta=D\boldsymbol\alpha-\boldsymbol\varphi
\]

and

\[
\boxed{
\nabla_\alpha V_{\rm seam}=D^T\mathbf g.
}
\]

The gradient is orthogonal to the global phase direction,

\[
\boxed{
\mathbf1^T\nabla_\alpha V_{\rm seam}=0,
}
\]

because `D 1 = 0`.

## 4. Onsager phase-only sector

Let

\[
\boxed{G_\alpha=G_\alpha^T\succeq0}
\]

be the admitted phase-response matrix. Define

\[
\boxed{
\dot{\boldsymbol\alpha}_D
=-G_\alpha\nabla_\alpha V_{\rm seam}.
}
\]

The corresponding state-space tangent is

\[
\boxed{
\dot\psi_D
=i\,\operatorname{diag}(\dot{\boldsymbol\alpha}_D)\psi.
}
\]

Because `dot alpha_D` is real, this sector changes phases while preserving every component magnitude and therefore

\[
\boxed{
\frac{d}{d\Theta}\|\psi\|^2\bigg|_D=0.
}
\]

Its seam-defect rate is exactly

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}\bigg|_D
=-(\nabla_\alpha V_{\rm seam})^T
G_\alpha
(\nabla_\alpha V_{\rm seam})
\le0.
}
\]

Define the non-negative dissipation rate

\[
\boxed{
\mathcal D_\alpha
:=(\nabla_\alpha V_{\rm seam})^T
G_\alpha
(\nabla_\alpha V_{\rm seam})\ge0.
}
\]

## 5. Full norm-preserving dynamics

Combine the two tangent fields,

\[
\boxed{
\partial_\Theta\psi
=-iH\psi
+i\,\operatorname{diag}(\dot{\boldsymbol\alpha}_D)\psi,
}
\]

with

\[
\dot{\boldsymbol\alpha}_D
=-G_\alpha\nabla_\alpha V_{\rm seam}.
\]

Both terms are tangent to the unit sphere in frame Hilbert space, so

\[
\boxed{
\frac{d}{d\Theta}\|\psi\|^2=0.
}
\]

The exact instantaneous seam balance is

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=P_H-\mathcal D_\alpha
}
\]

or explicitly

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=i\psi^\dagger[H,K_\varphi]\psi
-(\nabla_\alpha V_{\rm seam})^T
G_\alpha
(\nabla_\alpha V_{\rm seam}).
}
\]

This is the central balance law of the gate.

## 6. Three exact regimes

### 6.1 Pure Schrödinger

For `G_alpha=0`,

\[
\boxed{
\dot V_{\rm seam}=P_H.
}
\]

Seam fuzziness can oscillate reversibly.

### 6.2 Pure Onsager

For `H=0`,

\[
\boxed{
\dot V_{\rm seam}=-\mathcal D_\alpha\le0.
}
\]

The compatible glued-sector weight increases correspondingly whenever the 02J norm decomposition applies.

### 6.3 Commuting reversible carrier

If

\[
[H,K_\varphi]=0,
\]

then

\[
\boxed{
\dot V_{\rm seam}=-\mathcal D_\alpha\le0.
}
\]

The Hamiltonian cannot inject seam mismatch in this sector.

## 7. Locking criterion under reversible pumping

For general `H`, monotone local seam descent occurs whenever

\[
\boxed{
P_H<\mathcal D_\alpha.
}
\]

The balance point satisfies

\[
\boxed{
P_H=\mathcal D_\alpha.
}
\]

If `P_H` becomes larger than the dissipative rate, the reversible sector temporarily increases seam mismatch while preserving total frame norm.

This separates reversible fuzziness transport from irreversible phase alignment.

## 8. Relation to the modular half-frame picture

The support pattern

\[
|1|\,|12|\,|23|\cdots|N|
\]

is the symmetric glued quotient of 02J. For a normalized state,

\[
\boxed{
W_{\rm glued}+V_{\rm seam}=1
}
\]

on the declared half-frame decomposition, where `V_seam` is the total antisymmetric seam weight.

Therefore the pure Onsager sector obeys

\[
\boxed{
\frac{dW_{\rm glued}}{d\Theta}
=\mathcal D_\alpha\ge0.
}
\]

while the full reversible+dissipative system obeys

\[
\boxed{
\frac{dW_{\rm glued}}{d\Theta}
=-P_H+\mathcal D_\alpha.
}
\]

The user's `|1|12|23|...|N|` picture is therefore represented by a norm-conserving transfer between symmetric overlap and antisymmetric mismatch sectors.

## 9. Split-step reference integrator

A reference finite-step scheme is allowed to alternate:

1. exact unitary half-step `exp(-i H DeltaTheta/2)`;
2. phase-only Onsager update implemented as multiplication by unit-modulus node phases;
3. exact unitary half-step.

Each substep preserves the frame norm. The finite-step seam balance approaches the instantaneous theorem as `DeltaTheta -> 0`.

The split-step implementation is a numerical reference, while the exact claims of this gate concern the continuous vector field and instantaneous balance identity.

## 10. Evidence boundary

The exact gate assumes:

- finite Hermitian `H`;
- fixed edge-native seam phases during the instantaneous balance evaluation;
- the 02JD half-seam functional;
- positive-semidefinite node-phase Onsager response;
- the activity-derived intrinsic temporal coordinate `Theta`.

The gate does not impose unconditional monotonicity on the combined Schrödinger–Onsager system. The reversible commutator power is retained explicitly.

Physical identification of `H`, `G_alpha`, and seam variables remains downstream of the existing model/evidence gates.

## 11. Next gate

The next test is the continuum limit of this mixed reversible/dissipative half-frame system: whether the path-complex balance converges to the already admitted Temporal Wave stiffness/damping structure while retaining the TIR/IDT phase-rate normalization.

Reference implementation: `src/idt/schrodinger_onsager_seam_balance.py`.
Reference tests: `tests/reference/test_schrodinger_onsager_seam_balance.py`.
Validation receipt: `validation/SCHRODINGER_ONSAGER_SEAM_BALANCE_V0_1.json`.
