# 02JN — Continuum Madelung Schrödinger–Onsager Split

Status: `FORMAL_CANDIDATE / COUPLED_DENSITY_PHASE_BALANCE_GATE`

This gate combines the continuum density-current law of 02JL with the phase-gradient Onsager flow of 02JM. The common evolution coordinate is the already-derived intrinsic temporal measure `Theta`.

## 1. Gauge-covariant Schrödinger operator

Let

\[
\boxed{
D_A:=\partial_x-iA(x,\Theta),
}
\]

with real connection `A`, positive mobility/stiffness field `M(x)>0`, and real scalar potential `V(x,Theta)`. The continuum Temporal Wave operator is

\[
\boxed{
H=D_A^\dagger M D_A+V
=-D_A M D_A+V,
}
\]

on an admitted periodic or boundary-flux-controlled domain.

Write

\[
\boxed{
\Psi=R e^{i\alpha},
\qquad R>0,
\qquad \rho=R^2,
}
\]

and define the gauge-invariant phase gradient

\[
\boxed{
q=\partial_x\alpha-A.
}
\]

Then

\[
D_A\Psi=e^{i\alpha}(R_x+iRq).
\]

## 2. Exact polar decomposition of the reversible flow

The Schrödinger sector is

\[
\boxed{
i\partial_\Theta\Psi=H\Psi.}
\]

Using

\[
-D_A M D_A\Psi
=e^{i\alpha}
\left[
-\partial_x(MR_x)+MRq^2
-i\left(\partial_x(MRq)+MqR_x\right)
\right],
\]

and separating real and imaginary parts gives

\[
\boxed{
\left.\partial_\Theta\rho\right|_H
=-2\partial_x(M\rho q),
}
\]

and

\[
\boxed{
\left.\partial_\Theta\alpha\right|_H
=\frac{\partial_x(MR_x)}{R}-Mq^2-V.
}
\]

The first identity is exactly the 02JL continuity equation with

\[
\boxed{
\mathcal J=2M\rho q.
}
\]

Thus

\[
\boxed{
\partial_\Theta\rho+\partial_x\mathcal J=0
}
\]

for the reversible density transport.

## 3. Add the 02JM phase-only Onsager response

02JM supplies

\[
\boxed{
\left.\partial_\Theta\alpha\right|_D
=2\mu\partial_x(M\rho q),
\qquad \mu>0,
}
\]

while

\[
\boxed{
\left.\partial_\Theta\rho\right|_D=0.
}
\]

Therefore the combined system is

\[
\boxed{
\partial_\Theta\rho
=-2\partial_x(M\rho q),
}
\]

\[
\boxed{
\partial_\Theta\alpha
=\frac{\partial_x(MR_x)}{R}-Mq^2-V
+2\mu\partial_x(M\rho q).
}
\]

Because the density equation implies

\[
2\partial_x(M\rho q)=-\partial_\Theta\rho,
\]

the coupled phase balance has the compact form

\[
\boxed{
\partial_\Theta\alpha
+\mu\partial_\Theta\rho
=\frac{\partial_x(MR_x)}{R}-Mq^2-V.
}
\]

The Onsager correction is therefore tied directly to the same density flux that appears in the continuity equation.

## 4. Gauge covariance

Under

\[
\Psi\mapsto e^{i\chi}\Psi,
\qquad
\alpha\mapsto\alpha+\chi,
\qquad
A\mapsto A+\partial_x\chi,
\]

we have

\[
q\mapsto q,
\qquad
\rho\mapsto\rho,
\qquad
\mathcal J\mapsto\mathcal J.
\]

The density equation and every `q`-dependent term remain invariant. For a time-independent gauge representative on the local comparison patch, the displayed phase-rate equation transforms covariantly by the same phase-coordinate re-expression.

## 5. Constant-M current-velocity representation

For constant `M>0` define

\[
\boxed{
u:=\frac{\mathcal J}{\rho}=2Mq.}
\]

Then the continuity equation becomes

\[
\boxed{
\partial_\Theta\rho+\partial_x(\rho u)=0.
}
\]

Assume the connection is stationary in `Theta`. Differentiating the compact phase balance and multiplying by `2M` gives

\[
\boxed{
\partial_\Theta u+u\partial_xu
=2M^2\partial_x\left(\frac{R_{xx}}R\right)
-2M\partial_xV
+2\mu M\partial_x^2(\rho u).
}
\]

The last term is the density-current smoothing term inherited from the phase-gradient Onsager response. Its physical interpretation remains downstream of this algebraic gate.

## 6. Linearized uniform-background mode

Let

\[
\rho=\rho_0+\delta\rho,
\qquad
u=\delta u,
\qquad
\rho_0>0,
\]

around a uniform zero-current, constant-M, constant-potential background. To first order,

\[
\boxed{
\partial_\Theta\delta\rho
+\rho_0\partial_x\delta u=0,
}
\]

and

\[
\boxed{
\partial_\Theta\delta u
=\frac{M^2}{\rho_0}\partial_x^3\delta\rho
+2\mu M\rho_0\partial_x^2\delta u.
}
\]

Eliminating `delta u` gives

\[
\boxed{
\partial_\Theta^2\delta\rho
+M^2\partial_x^4\delta\rho
-2\mu M\rho_0\partial_x^2\partial_\Theta\delta\rho
=0.
}
\]

For a Fourier mode `exp(s Theta + i k x)`, the characteristic equation is

\[
\boxed{
s^2+2\mu M\rho_0k^2s+M^2k^4=0.
}
\]

At `mu=0` this reduces to the quadratic Schrödinger dispersion `s=± i M k^2`; positive `mu` supplies the declared phase-gradient damping channel.

## 7. Relation to the half-frame picture

The finite half-frame architecture supplies neighboring overlaps `|n,n+1|`, their seam phase and their gauge-invariant mismatch. 02JK takes the smooth limit of the overlap/defect channels; 02JL derives density transport; 02JM derives continuum seam-gradient descent. The present gate combines those already-admitted channels into one coupled density/phase system:

\[
\boxed{
\text{half-frame overlaps}
\to
(\rho,q)
\to
\begin{cases}
\rho_\Theta=-\partial_x\mathcal J,\\
\alpha_\Theta+\mu\rho_\Theta=Q_M-Mq^2-V,
\end{cases}
}
\]

where

\[
\boxed{
Q_M:=\frac{\partial_x(MR_x)}R.
}
\]

No additional temporal parameter is introduced.

## 8. Falsification gates

Reference tests require:

- exact algebraic equivalence between continuity and `rho_Theta=-2 partial_x(M rho q)`;
- exact compact identity `alpha_Theta + mu rho_Theta = Q_M-Mq^2-V`;
- gauge invariance of `q`, `rho` and `J` under local phase re-expression;
- exact constant-M conversion between `(rho,q)` and `(rho,u)` forms;
- exact linearized characteristic polynomial;
- recovery of undamped quadratic Schrödinger dispersion at `mu=0`;
- non-positive real part of the linear mode exponents for `mu>0`;
- fail-closed behavior for non-positive density, mobility or malformed inputs.

Reference implementation: `src/idt/continuum_madelung_onsager.py`.
Reference tests: `tests/reference/test_continuum_madelung_onsager.py`.
Validation receipt: `validation/CONTINUUM_MADELUNG_ONSAGER_V0_1.json`.
