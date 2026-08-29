# 02JH — Full Schrödinger–Onsager Half-Seam Balance

Status: `FORMAL_CANDIDATE / EXACT_INSTANTANEOUS_BALANCE_GATE`

This gate couples the phase-aware half-frame seam to the full Schrödinger frame-amplitude flow while retaining the positive Onsager phase response derived in 02JG. The evolution parameter is the activity-derived intrinsic temporal coordinate `Theta`.

## 1. Covariant seam operator

For `N` frame amplitudes

\[
\psi=(a_1,\ldots,a_N)^T
\]

and internal seam phases

\[
\boldsymbol\varphi=(\varphi_1,\ldots,\varphi_{N-1}),
\]

define the covariant seam incidence matrix by

\[
\boxed{
(C_\varphi)_{n,n}=e^{+i\varphi_n/2},
\qquad
(C_\varphi)_{n,n+1}=-e^{-i\varphi_n/2}.
}
\]

The 02JD seam-defect vector is

\[
\boxed{
\mathbf d=\frac12C_\varphi\psi.
}
\]

Define the Hermitian positive-semidefinite seam stiffness

\[
\boxed{
K_\varphi=\frac14C_\varphi^\dagger C_\varphi\succeq0.
}
\]

Then the total seam-defect functional is

\[
\boxed{
V_{\rm seam}
=\|\mathbf d\|^2
=\psi^\dagger K_\varphi\psi\ge0.
}
\]

## 2. Schrödinger contribution

The 02E frame dynamics uses the derived intrinsic temporal coordinate:

\[
\boxed{
iD_\Theta\psi=H\psi,
\qquad H=H^\dagger.
}
\]

For fixed seam connection during the instantaneous derivative,

\[
\left.\frac{dV_{\rm seam}}{d\Theta}\right|_{\rm Sch}
=
\dot\psi^\dagger K_\varphi\psi
+\psi^\dagger K_\varphi\dot\psi.
\]

Substitution of `dot psi = -i H psi` gives

\[
\boxed{
P_{\rm Sch}
:=
\left.\frac{dV_{\rm seam}}{d\Theta}\right|_{\rm Sch}
=
i\psi^\dagger[H,K_\varphi]\psi.
}
\]

The value is real because `i[H,K_varphi]` is Hermitian.

The commutator therefore measures the instantaneous mismatch between the Schrödinger generator and the half-seam geometry.

### Commuting-sector theorem

If

\[
\boxed{[H,K_\varphi]=0,}
\]

then

\[
\boxed{P_{\rm Sch}=0}
\]

for every admitted frame state.

## 3. Vertex-phase gradient without phase singularities

Write locally `a_n=r_n e^{i alpha_n}` when a polar chart is available. The derivative of `V_seam` with respect to vertex phases can be evaluated directly from complex amplitudes:

\[
\boxed{
(g_\alpha)_n
:=\frac{\partial V_{\rm seam}}{\partial\alpha_n}.
}
\]

For one seam `n -> n+1`, define

\[
\boxed{
j_n^{\rm seam}
=\frac12\operatorname{Im}\!\left(
e^{i\varphi_n}a_na_{n+1}^*
\right).
}
\]

Its contribution to the vertex gradient is

\[
(g_\alpha)_n\mathrel{+}=j_n^{\rm seam},
\qquad
(g_\alpha)_{n+1}\mathrel{-}=j_n^{\rm seam}.
\]

Hence

\[
\boxed{\sum_n(g_\alpha)_n=0,}
\]

which is the global `U(1)` zero mode.

## 4. Positive Onsager phase response

Let

\[
\boxed{G_\alpha=G_\alpha^T\succeq0}
\]

be the admitted symmetric Onsager mobility on vertex-phase coordinates. Define

\[
\boxed{
D_\Theta\boldsymbol\alpha\big|_{\rm O}
=-G_\alpha\mathbf g_\alpha.
}
\]

The corresponding state-space velocity is a phase-only flow,

\[
\boxed{
D_\Theta\psi\big|_{\rm O}
=
i\operatorname{diag}\!\left(
-G_\alpha\mathbf g_\alpha
\right)\psi.
}
\]

Because the diagonal rate is real,

\[
\boxed{
\left.\frac{d}{d\Theta}\|\psi\|^2\right|_{\rm O}=0.
}
\]

The seam functional changes by

\[
\boxed{
\left.\frac{dV_{\rm seam}}{d\Theta}\right|_{\rm O}
=-\mathbf g_\alpha^T G_\alpha\mathbf g_\alpha.
}
\]

Define the non-negative Onsager dissipation

\[
\boxed{
\mathcal D_{\rm O}
:=\mathbf g_\alpha^T G_\alpha\mathbf g_\alpha\ge0.
}
\]

## 5. Full instantaneous balance law

The coupled state velocity is

\[
\boxed{
D_\Theta\psi
=-iH\psi
+i\operatorname{diag}\!\left(-G_\alpha\mathbf g_\alpha\right)\psi.
}
\]

Both contributions preserve the frame-state norm instantaneously, so

\[
\boxed{
\frac{d}{d\Theta}\|\psi\|^2=0.
}
\]

For the seam functional,

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=P_{\rm Sch}-\mathcal D_{\rm O}.
}
\]

Equivalently,

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=
i\psi^\dagger[H,K_\varphi]\psi
-
\mathbf g_\alpha^TG_\alpha\mathbf g_\alpha.
}
\]

This is the central balance identity of the gate.

Three exact sectors follow.

### Pure descent sector

When `[H,K_varphi]=0`,

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=-\mathcal D_{\rm O}\le0.
}
\]

### Pump-dominated sector

When

\[
P_{\rm Sch}>\mathcal D_{\rm O},
\]

the seam-defect energy increases instantaneously.

### Dissipation-dominated sector

When

\[
P_{\rm Sch}<\mathcal D_{\rm O},
\]

the seam-defect energy decreases instantaneously.

A stationary seam-energy balance satisfies

\[
\boxed{P_{\rm Sch}=\mathcal D_{\rm O}.}
\]

## 6. Gauge covariance

For a static local frame re-expression

\[
\psi\mapsto U_\chi\psi,
\qquad
U_\chi=\operatorname{diag}(e^{i\chi_n}),
\]

and

\[
\varphi_n\mapsto
\varphi_n+\chi_{n+1}-\chi_n,
\]

the Hamiltonian transforms as

\[
\boxed{H\mapsto U_\chi H U_\chi^\dagger.}
\]

The seam operator transforms covariantly and the scalar quantities

\[
\boxed{
V_{\rm seam},
\qquad
P_{\rm Sch},
\qquad
\mathcal D_{\rm O},
\qquad
\frac{dV_{\rm seam}}{d\Theta}
}
\]

are invariant under the common re-expression.

## 7. Zeta–Collatz integration

The 02E candidate Hamiltonian

\[
\boxed{
H_{\zeta C}
=\alpha_\zeta\widetilde D_\zeta+g_C L_C
}
\]

can be inserted directly into the balance identity:

\[
\boxed{
P_{\zeta C\to seam}
=
i\psi^\dagger[H_{\zeta C},K_\varphi]\psi.
}
\]

Thus the same reference model that spreads amplitude among discrete frames now has an exact diagnostic for how strongly its Schrödinger flow excites or removes half-seam mismatch.

The Frobenius commutator norm

\[
\boxed{
\Xi_{HK}
:=\|[H_{\zeta C},K_\varphi]\|_F
}
\]

is a state-independent alignment diagnostic, while `P_Sch` is the state-dependent instantaneous transfer rate.

## 8. Relation to 02JG locking

02JG is recovered as the phase-only sector in which the Schrödinger contribution supplies no seam power over the considered step. The full gate promotes the one-way Lyapunov statement to the balance structure

\[
\boxed{
\text{Schrödinger seam transfer}
\;\leftrightarrow\;
\text{Onsager seam relaxation}.
}
\]

The locking state is therefore controlled by both the Hamiltonian/seam commutator and the positive Onsager response.

## 9. Evidence boundary

The algebraic gate uses:

- the 02JD phase-aware half-seam carrier;
- the 02E Hermitian Schrödinger generator acting in derived intrinsic `Theta`;
- the 02JG choice of seam defect as the dissipative scalar;
- a symmetric positive-semidefinite Onsager phase mobility;
- a fixed seam connection for the instantaneous balance derivative.

A dynamically evolving connection adds its explicit connection-work term through `D_Theta varphi`. Physical oscillator identification, measured dissipation coefficients and spinorial binding retain their downstream gates.

## 10. Reference gate

Reference implementation:
`src/idt/schrodinger_onsager_seam_balance.py`.

Reference tests:
`tests/reference/test_schrodinger_onsager_seam_balance.py`.

Validation receipt:
`validation/SCHRODINGER_ONSAGER_SEAM_BALANCE_V0_1.json`.
