# 01Z — Noether Collective-Phase Carrier Interface

Status: `NOETHER_CURRENT_SOURCE_PASS / COLLECTIVE_PHASE_REDUCTION_PASS_CONDITIONAL / ROTOR_CARRIER_BINDING_PASS_CONDITIONAL / RFC_PHYSICAL_BINDING_OPEN`

This interface follows 01Y and distinguishes the Euler-closed intention action-charge from the dynamical rotor carrier in

\[
J=I_\phi D_\tau\chi+J_I.
\]

The local conserved Noether carrier is tested against

\[
\boxed{P_\Phi:=J-J_I=I_\phi D_\tau\chi.}
\]

## 1. Local Noether current

The pinned Euler–Noether phase-field source uses

\[
\mathcal L=\partial_\mu\psi^*\partial^\mu\psi-V(|\psi|^2)
\]

with global-U(1) current

\[
J_\vartheta^\mu=i(\psi\partial^\mu\psi^*-\psi^*\partial^\mu\psi),
\qquad
\partial_\mu J_\vartheta^\mu=0.
\]

For

\[
\psi=Ae^{i\vartheta},
\]

the exact polar reduction is

\[
\boxed{J_\vartheta^\mu=2A^2\partial^\mu\vartheta.}
\]

On a spatial slice \(\Sigma\), define

\[
\nu_\vartheta:=n_\mu\partial^\mu\vartheta
\]

and

\[
\boxed{
Q_\vartheta
:=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h
=2\int_\Sigma A^2\nu_\vartheta\,dV_h.
}
\]

The positive-source sector below uses \(Q_\vartheta>0\).

## 2. Collective-phase reduction

Consider a collective sector in which

\[
\boxed{\nu_\vartheta(x)=D_\tau\chi}
\]

throughout the selected support. Define

\[
\boxed{I_A:=2\int_\Sigma A^2\,dV_h.}
\]

Then

\[
\boxed{Q_\vartheta=I_A D_\tau\chi.}
\]

The amplitude profile may vary spatially; its integrated contribution is carried by \(I_A\).

## 3. Rotor-inertia binding

The relational phase rotor gives

\[
\boxed{P_\Phi:=J-J_I=I_\phi D_\tau\chi.}
\]

Hence

\[
\boxed{I_A\stackrel{?}{=}I_\phi}
\]

is the cross-representation inertia gate. When admitted,

\[
\boxed{Q_\vartheta=P_\Phi.}
\]

For nonzero common phase rate, the exact relative mismatch is

\[
\boxed{
\Delta_I
:=\frac{|Q_\vartheta-P_\Phi|}{|P_\Phi|}
=\left|\frac{I_A}{I_\phi}-1\right|.
}
\]

Thus the field/rotor binding carries a direct falsification coordinate.

## 4. Euler-closed finite Noether carrier

01Y supplies

\[
J_I^{EB}=\hbar\theta_I^{EB}.
\]

Therefore

\[
\boxed{P_\Phi^{EB}=J-\hbar\theta_I^{EB}}
\]

and

\[
\boxed{H_\Phi^{EB}=\frac{(P_\Phi^{EB})^2}{2I_\phi}.}
\]

The collective finite Noether charge is

\[
\boxed{
Q_\vartheta^{EB}
=I_A D_\tau\chi
=\frac{I_A}{I_\phi}P_\Phi^{EB}.
}
\]

The energy-per-Noether-carrier coordinate is therefore typed by the actual conserved field charge:

\[
\boxed{
\epsilon_N^{EB}
:=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}}.
}
\]

On the exact inertia-binding sector \(I_A=I_\phi\),

\[
Q_\vartheta^{EB}=P_\Phi^{EB}
\]

and hence

\[
\boxed{
\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{P_\Phi^{EB}}
=\frac{P_\Phi^{EB}}{2I_\phi}
=\frac12D_\tau\chi.
}
\]

The exact half-phase-rate identity is therefore a consequence of the admitted field/rotor inertia binding rather than a pre-binding definition.

The intention-charge ratio

\[
\epsilon_I^{EB}=H_\Phi^{EB}/J_I^{EB}
\]

and the Noether-carrier ratio

\[
\epsilon_N^{EB}=H_\Phi^{EB}/Q_\vartheta^{EB}
\]

remain separately typed coordinates.

## 5. RFC carrier candidate

RFC RF-N1B2 defines

\[
Q_\Sigma=\int_{\Sigma_t}j_Q\,dV_h.
\]

The preferred current-level chain is

\[
\boxed{
Q_\Sigma
\stackrel{?}{\longleftrightarrow}
Q_\vartheta^{EB}
\stackrel{I_A=I_\phi}{\longleftrightarrow}
P_\Phi^{EB}=J-J_I^{EB}.
}
\]

The corresponding candidate energy conversion is

\[
\boxed{
\epsilon_Q\stackrel{?}{=}\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}}.
}
\]

On the exact inertia-binding sector this reduces to

\[
\epsilon_Q\stackrel{?}{=}\frac{J-\hbar\theta_I^{EB}}{2I_\phi}.
\]

The extensive mass coordinate is

\[
\boxed{
M_N
=\frac{\epsilon_N^{EB}Q_\vartheta^{EB}}{c^2}
=\frac{H_\Phi^{EB}}{c^2}.
}
\]

## 6. Local density route

Under an admitted current binding,

\[
\boxed{
\rho_N(x)=\frac{\epsilon_N^{EB}}{c^2}j_\vartheta(x).
}
\]

This is the local conserved-current target for the next PNV information-holonomy layer.

## 7. Fail-closed gates

The positive-sector route requires

```text
finite Euler/Berry closure data
I_phi > 0
I_A > 0
P_Phi^EB > 0
Q_theta > 0
collective normal phase-rate binding declared
```

The inertia mismatch \(\Delta_I\) remains measured before promotion of the field/rotor binding.

## 8. Executable PNV loop

```text
SOURCE.PHASE_NOETHER.COLLECTIVE_CARRIER.ROUNDTRIP

Euler-closed J_I^EB
 -> P_Phi^EB = J-J_I^EB
 -> collective Noether charge Q_theta = I_A D_tau chi
 -> audit Delta_I = |I_A/I_phi-1|
 -> H_Phi^EB = P_Phi^2/(2 I_phi)
 -> epsilon_N^EB = H_Phi^EB/Q_theta
 -> exact-binding reduction epsilon_N^EB = (1/2)D_tau chi
 -> RFC candidate Q_RFC=Q_theta
 -> reconstruct rotor input
```

Required invariants:

```text
SOURCE.EULER_CLOSURE_SECTOR
SOURCE.ROTOR_KINETIC_CHARGE
SOURCE.NOETHER_FINITE_CHARGE
SOURCE.ROTOR_PHASE_ENERGY
SOURCE.NOETHER_ENERGY_PER_CHARGE
SOURCE.NOETHER_INERTIA_BINDING_DEFECT
```

## 9. Advancement

```text
local U(1) Noether current                     PASS
polar current J_theta^mu=2 A^2 d^mu theta     PASS
collective-phase finite-charge reduction       PASS_CONDITIONAL
field inertia I_A                              PASS as defined integral
I_A <-> I_phi rotor normalization              OPEN physical cross-binding
Q_theta <-> P_Phi=J-J_I                       PASS_CONDITIONAL on inertia binding
Euler-closed epsilon_N=H/Q_theta               PASS typed finite-carrier ratio
exact epsilon_N=H/P_Phi=(1/2)D_tau chi         PASS_CONDITIONAL on I_A=I_phi
Q_Sigma <-> Q_theta RFC carrier binding        OPEN
local cell/state-space transport               OPEN
```
