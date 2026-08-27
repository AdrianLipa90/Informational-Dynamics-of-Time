# 01AB — Scalar-Field → Rotor Inertia Reduction

Status: `EXACT_COLLECTIVE_REDUCTION_PASS_CONDITIONAL / PHASE_RATE_BINDING_OPEN / COMMON_MEASURE_BINDING_OPEN`

01AB follows 01Z/01AA and resolves the apparent independent inertia gate between the Euler–Noether field and the canonical phase rotor.

The result is conditional on using the same scalar phase degree of freedom, covariant phase rate and spatial measure in both descriptions.

## 1. Scalar-field phase sector

The upstream Euler–Noether scalar field uses

\[
\mathcal L
=\partial_\mu\psi^*\partial^\mu\psi-V(|\psi|^2)
\]

with polar decomposition

\[
\psi=Ae^{i\vartheta}.
\]

Direct substitution gives

\[
\partial_\mu\psi^*\partial^\mu\psi
=(\partial_\mu A)(\partial^\mu A)
+A^2(\partial_\mu\vartheta)(\partial^\mu\vartheta)
\]

and the global-U(1) Noether current

\[
\boxed{J_\vartheta^\mu=2A^2\partial^\mu\vartheta.}
\]

## 2. Collective phase-rate reduction

Take a collective phase sector in which the phase motion carried by the rotor is one common coordinate \(\chi(\tau)\), with the same covariant rate used by the canonical rotor,

\[
\boxed{D_\tau\vartheta\leftrightarrow D_\tau\chi.}
\]

All spatial/amplitude/horizontal terms are retained in their own reduced sectors. The coefficient of the pure collective quadratic phase rate is then

\[
L_{\rm phase}^{field}
=
\int_\Sigma A^2(D_\tau\chi)^2dV_h.
\]

Define

\[
\boxed{I_A:=2\int_\Sigma A^2dV_h.}
\]

Therefore

\[
\boxed{
L_{\rm phase}^{field}
=\frac{I_A}{2}(D_\tau\chi)^2.
}
\]

## 3. Canonical rotor coefficient

The admitted canonical phase-rotor scaffold contains

\[
\boxed{
L_{\rm rotor}
=\frac{I_\phi}{2}(D_\tau\chi)^2
+J_I D_\tau\chi
+\cdots
}
\]

and

\[
\boxed{J=I_\phi D_\tau\chi+J_I.}
\]

The intention term is linear in the phase rate and the quadratic kinetic coefficient remains \(I_\phi/2\).

If the rotor is the collective-coordinate reduction of the stated scalar-field phase sector on the same measure, equality of the quadratic coefficients gives the exact conditional theorem

\[
\boxed{I_\phi=I_A=2\int_\Sigma A^2dV_h.}
\]

Thus the previously defined 01Z inertia defect

\[
\Delta_I^{01Z}=\left|\frac{I_A}{I_\phi}-1\right|
\]

satisfies

\[
\boxed{\Delta_I^{01Z}=0}
\]

inside this admitted collective reduction.

## 4. Noether charge equals rotor kinetic momentum

The finite Noether charge of the collective mode is

\[
Q_\vartheta
=\int_\Sigma 2A^2D_\tau\chi\,dV_h
=I_A D_\tau\chi.
\]

Using the coefficient theorem,

\[
Q_\vartheta
=I_\phi D_\tau\chi.
\]

The rotor kinetic momentum is

\[
P_\Phi:=J-J_I=I_\phi D_\tau\chi.
\]

Hence

\[
\boxed{Q_\vartheta=P_\Phi=J-J_I.}
\]

After Euler/Berry closure this becomes

\[
\boxed{Q_\vartheta^{EB}=P_\Phi^{EB}=J-J_I^{EB}.}
\]

## 5. Energy per finite Noether charge

The rotor phase energy is

\[
H_\Phi^{EB}
=\frac{(P_\Phi^{EB})^2}{2I_\phi}.
\]

On the positive nondegenerate carrier sector,

\[
\epsilon_N^{EB}
:=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}}.
\]

Since \(Q_\vartheta^{EB}=P_\Phi^{EB}\),

\[
\boxed{
\epsilon_N^{EB}
=\frac{P_\Phi^{EB}}{2I_\phi}
=\frac12D_\tau\chi.
}
\]

The collective phase-rate reduction therefore fixes the finite Noether energy-per-carrier coordinate.

## 6. Exact theorem versus interface gates

The coefficient matching is exact after the collective reduction is admitted. The remaining gates are upstream identification gates:

```text
same scalar phase mode theta <-> chi                 OPEN interface binding
same covariant phase rate D_tau theta <-> D_tau chi OPEN interface binding
same spatial slice and dV_h                          OPEN physical/measure binding
same collective-mode support                         OPEN support binding
I_phi = 2 integral A^2 dV_h after those bindings     PASS EXACT CONDITIONAL
Delta_I^01Z after those bindings                     ZERO EXACT
Q_theta = P_Phi after those bindings                 PASS EXACT CONDITIONAL
```

The inertia equality is thereby fixed by the admitted common reduction premises.

## 7. Relation to 01AA/RFC

01AA separately tests the downstream current/measure identity

\[
J_Q^\mu\stackrel{?}{\longleftrightarrow}J_\vartheta^\mu.
\]

01AB therefore removes one internal normalization degree of freedom while preserving the physical RFC current-binding gate.

After both 01AB and 01AA are admitted on the same carrier sector,

\[
\boxed{
Q_\Sigma=Q_\vartheta=P_\Phi^{EB}
}
\]

and

\[
\boxed{
\epsilon_Q
=\epsilon_N^{EB}
=\frac12D_\tau\chi
}
\]

becomes the downstream RFC candidate normalization.

## 8. Executable PNCS reduction coordinates

The PNCS collective-reduction loop evaluates the coefficient theorem from independently supplied finite-cell field data and rotor inertia.

For

\[
C_A:=\sum_a A_a^2V_a,
\qquad
I_A:=2C_A,
\]

define the executable reduction coordinates

\[
\boxed{
\Delta_I^{red}:=\frac{|I_\phi-I_A|}{I_A}}
\]

and

\[
\Delta_C:=\frac{|I_\phi/2-C_A|}{C_A},
\qquad
\Delta_Q^{red}:=\frac{|P_\Phi-Q_\vartheta|}{Q_\vartheta},
\]

\[
\Delta_\epsilon^{red}
:=\frac{|\epsilon_N-(D_\tau\chi)/2|}{(D_\tau\chi)/2}.
\]

For one common positive covariant phase rate,

\[
\boxed{
\Delta_I^{red}
=\Delta_C
=\Delta_Q^{red}
=\Delta_\epsilon^{red}.}
\]

The earlier 01Z coordinate \(\Delta_I^{01Z}=|I_A/I_\phi-1|\) and the executable reduction coordinate \(\Delta_I^{red}=|I_\phi-I_A|/I_A\) are separately typed away from the exact gate and share the same zero set \(I_A=I_\phi\).

Executable contract:

`PNCS_PNV_SCALAR_FIELD_ROTOR_INERTIA_REDUCTION_V0_1`

Semantic loop:

`SOURCE.PHASE_NOETHER.ROTOR_INERTIA.REDUCTION.ROUNDTRIP`
