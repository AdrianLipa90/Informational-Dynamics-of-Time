# 02JI — Moving Half-Seam Connection Work

Status: `FORMAL_CANDIDATE / TIME_DEPENDENT_GAUGE_BALANCE_GATE`

02JH derives the full Schrödinger–Onsager seam balance for a fixed edge connection. This layer promotes the seam phase to an intrinsic-time-dependent edge coordinate

\[
\boxed{\varphi_e=\varphi_e(\Theta)}
\]

and derives the corresponding connection-work term and time-dependent gauge closure.

## 1. Moving seam geometry

The seam functional is

\[
\boxed{
V_{\rm seam}(\psi,\varphi)
=\psi^\dagger K_\varphi\psi,
\qquad
K_\varphi=\frac14C_\varphi^\dagger C_\varphi.
}
\]

When the edge connection evolves,

\[
\boxed{
\Omega_{\varphi,e}:=D_\Theta\varphi_e.
}
\]

The explicit geometric contribution to the seam-energy derivative is

\[
\boxed{
P_{\rm conn}
:=
\psi^\dagger(D_\Theta K_\varphi)\psi.
}
\]

By the chain rule,

\[
\boxed{
P_{\rm conn}
=\sum_e
\frac{\partial V_{\rm seam}}{\partial\varphi_e}
\Omega_{\varphi,e}.
}
\]

For one edge `e:n -> n+1`,

\[
\boxed{
q_e^{\rm conn}
:=
\frac{\partial V_{\rm seam}}{\partial\varphi_e}
=
\frac12\operatorname{Im}\!\left(
e^{i\varphi_e}a_na_{n+1}^*
\right).
}
\]

Hence

\[
\boxed{
P_{\rm conn}
=(\mathbf q^{\rm conn})^T\boldsymbol\Omega_\varphi.
}
\]

The connection work can have either sign.

## 2. Full moving-connection balance

02JH supplies

\[
P_{\rm Sch}
=i\psi^\dagger[H,K_\varphi]\psi
\]

and

\[
\mathcal D_{\rm O}
=\mathbf g_\alpha^TG_\alpha\mathbf g_\alpha\ge0.
\]

The full balance is therefore

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=
P_{\rm Sch}
+P_{\rm conn}
-\mathcal D_{\rm O}.
}
\]

Define the conservative geometric transfer

\[
\boxed{
P_{\rm geom}
:=P_{\rm Sch}+P_{\rm conn}.
}
\]

Then

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=P_{\rm geom}-\mathcal D_{\rm O}.
}
\]

The fixed-connection theorem is recovered at

\[
\boldsymbol\Omega_\varphi=0.
\]

## 3. Exact operator derivative

For the covariant incidence matrix, each edge row is

\[
(C_\varphi)_{e,e}=e^{+i\varphi_e/2},
\qquad
(C_\varphi)_{e,e+1}=-e^{-i\varphi_e/2}.
\]

Its intrinsic derivative is

\[
(D_\Theta C_\varphi)_{e,e}
=\frac{i}{2}\Omega_{\varphi,e}e^{+i\varphi_e/2},
\]

\[
(D_\Theta C_\varphi)_{e,e+1}
=\frac{i}{2}\Omega_{\varphi,e}e^{-i\varphi_e/2}.
\]

Therefore

\[
\boxed{
D_\Theta K_\varphi
=
\frac14\left[
(D_\Theta C_\varphi)^\dagger C_\varphi
+C_\varphi^\dagger D_\Theta C_\varphi
\right].
}
\]

The operator expression and the edge-gradient expression for `P_conn` are identical.

## 4. Time-dependent local gauge transformation

Let

\[
U_\chi(\Theta)
=\operatorname{diag}(e^{i\chi_1(\Theta)},\ldots,e^{i\chi_N(\Theta)}).
\]

The frame state transforms as

\[
\boxed{\psi'=U_\chi\psi.}
\]

The seam connection transforms as

\[
\boxed{
\varphi'_e
=
\varphi_e+\chi_{e+1}-\chi_e,
}
\]

so its rate transforms as

\[
\boxed{
\Omega'_{\varphi,e}
=
\Omega_{\varphi,e}
+D_\Theta\chi_{e+1}-D_\Theta\chi_e.
}
\]

For the Schrödinger equation

\[
iD_\Theta\psi=H\psi,
\]

the Hamiltonian chart transforms as

\[
\boxed{
H'
=U_\chi H U_\chi^\dagger
+i(D_\Theta U_\chi)U_\chi^\dagger.
}
\]

For diagonal `U_chi`,

\[
\boxed{
H'
=U_\chi H U_\chi^\dagger
-\operatorname{diag}(D_\Theta\chi_n).
}
\]

## 5. Gauge closure of conservative seam power

Under a time-dependent gauge re-expression, the two terms

\[
P_{\rm Sch},
\qquad
P_{\rm conn}
\]

can change separately because the connection-rate contribution is redistributed between `H` and `D_Theta K_varphi`.

Their sum satisfies

\[
\boxed{
P'_{\rm geom}=P_{\rm geom}.
}
\]

Thus the gauge-closed conservative transfer is

\[
\boxed{
P_{\rm geom}
=
i\psi^\dagger[H,K_\varphi]\psi
+
\psi^\dagger(D_\Theta K_\varphi)\psi.
}
\]

The Onsager dissipation remains a gauge-invariant non-negative scalar. Therefore

\[
\boxed{
\left(\frac{dV_{\rm seam}}{d\Theta}\right)'
=
\frac{dV_{\rm seam}}{d\Theta}.
}
\]

## 6. Temporal seam-offset coordinate

The moving connection accumulates an intrinsic phase displacement

\[
\boxed{
\Delta\varphi_e[\Theta_1,\Theta_2]
=
\int_{\Theta_1}^{\Theta_2}
\Omega_{\varphi,e}\,d\Theta.
}
\]

This is the native edge-phase offset carried by the temporal gluing connection. Conversion of such a phase offset into a clock-duration offset requires an admitted local phase-rate map and remains a separate downstream gate.

## 7. Evidence boundary

This gate derives the work term for an admitted moving seam connection. It does not yet provide an independent equation selecting `Omega_varphi`. Such an equation may be supplied by a later connection-response/curvature gate. Physical clock-offset interpretation, measured connection rates and spacetime transport remain downstream.

## 8. Reference gate

Reference implementation: `src/idt/moving_seam_connection_work.py`.

Reference tests: `tests/reference/test_moving_seam_connection_work.py`.

Validation receipt: `validation/MOVING_SEAM_CONNECTION_WORK_V0_1.json`.
