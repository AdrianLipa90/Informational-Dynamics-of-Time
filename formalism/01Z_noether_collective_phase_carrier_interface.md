# 01Z — Noether Collective-Phase Carrier Interface

Status: `NOETHER_CURRENT_SOURCE_PASS / COLLECTIVE_PHASE_REDUCTION_PASS_CONDITIONAL / ROTOR_CARRIER_BINDING_PASS_CONDITIONAL / RFC_PHYSICAL_BINDING_OPEN`

This interface follows 01Y and distinguishes two action-charge coordinates in the phase rotor:

\[
J=I_\phi D_\tau\chi+J_I.
\]

The Euler-closed intention charge \(J_I^{EB}\) shifts the rotor. The local conserved Noether carrier is tested against the dynamical rotor charge

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

On a spatial slice \(\Sigma\), define the oriented normal phase rate

\[
\nu_\vartheta:=n_\mu\partial^\mu\vartheta
\]

and the corresponding finite phase charge

\[
\boxed{
Q_\vartheta
:=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h
=2\int_\Sigma A^2\nu_\vartheta\,dV_h.
}
\]

The sign sector is carried by the chosen slice orientation and phase-flow orientation. The positive-source sector below uses \(Q_\vartheta>0\).

## 2. Collective-phase reduction

Consider a collective phase sector in which the local phase shares one normal rate with the relational phase coordinate:

\[
\boxed{\nu_\vartheta(x)=D_\tau\chi}
\]

throughout the selected support on \(\Sigma\).

Define the field phase inertia

\[
\boxed{
I_A:=2\int_\Sigma A^2\,dV_h.
}
\]

Then exactly within this reduction,

\[
\boxed{Q_\vartheta=I_A D_\tau\chi.}
\]

The amplitude profile may vary spatially; only the collective normal phase rate is shared. The entire amplitude dependence is carried by \(I_A\).

## 3. Rotor-inertia binding

The relational phase rotor gives

\[
J=I_\phi D_\tau\chi+J_I,
\]

hence

\[
\boxed{P_\Phi:=J-J_I=I_\phi D_\tau\chi.}
\]

The cross-representation inertia gate is

\[
\boxed{I_A\stackrel{?}{=}I_\phi.}
\]

When this gate is admitted,

\[
\boxed{Q_\vartheta=P_\Phi=J-J_I.}
\]

For nonzero common phase rate, the exact relative inertia/charge mismatch is

\[
\boxed{
\Delta_{I}
:=\frac{|Q_\vartheta-P_\Phi|}{|P_\Phi|}
=\left|\frac{I_A}{I_\phi}-1\right|.
}
\]

Thus the local-current lift has a direct falsification coordinate rather than an untyped identification.

## 4. Euler-closed rotor carrier

01Y supplies

\[
J_I^{EB}=\hbar\theta_I^{EB}.
\]

Therefore

\[
\boxed{P_\Phi^{EB}=J-\hbar\theta_I^{EB}.}
\]

The canonical rotor energy is

\[
\boxed{
H_\Phi^{EB}
=\frac{(P_\Phi^{EB})^2}{2I_\phi}.
}
\]

On the positive carrier sector

\[
P_\Phi^{EB}>0,
\qquad I_\phi>0,
\]

the energy per Noether/rotor carrier is

\[
\boxed{
\epsilon_{N}^{EB}
:=\frac{H_\Phi^{EB}}{P_\Phi^{EB}}
=\frac{P_\Phi^{EB}}{2I_\phi}.
}
\]

Since \(P_\Phi=I_\phi D_\tau\chi\), this also gives

\[
\boxed{\epsilon_N^{EB}=\frac12D_\tau\chi.}
\]

This quantity and the 01Y intention-charge ratio

\[
\epsilon_I^{EB}=H_\Phi^{EB}/J_I^{EB}
\]

are separately typed coordinates. The Noether-current route selects \(\epsilon_N^{EB}\) as the preferred candidate for an RFC conserved-carrier energy conversion once the current/rotor binding is admitted.

## 5. RFC carrier candidate

RFC RF-N1B2 defines

\[
Q_\Sigma=\int_{\Sigma_t}j_Q\,dV_h.
\]

The preferred current-level chain is now

\[
\boxed{
Q_\Sigma
\stackrel{?}{\longleftrightarrow}
Q_\vartheta
\stackrel{I_A=I_\phi}{\longleftrightarrow}
P_\Phi^{EB}=J-J_I^{EB}.
}
\]

In an admitted positive bound sector,

\[
\boxed{
\epsilon_Q\stackrel{?}{=}\epsilon_N^{EB}
=\frac{J-\hbar\theta_I^{EB}}{2I_\phi}.
}
\]

The extensive mass coordinate becomes

\[
\boxed{
M_N
=\frac{\epsilon_N^{EB}P_\Phi^{EB}}{c^2}
=\frac{H_\Phi^{EB}}{c^2}.
}
\]

## 6. Local density route

Under the admitted current binding, the local positive carrier density is inherited from the normal Noether current. With the RFC energy conversion,

\[
\boxed{
\rho_N(x)=\frac{\epsilon_N^{EB}}{c^2}j_\vartheta(x).
}
\]

This supplies a concrete local-current target for the next PNV information-holonomy loop.

## 7. Fail-closed gates

The positive-sector energy-per-carrier ratio requires

```text
finite Euler/Berry closure data
I_phi > 0
P_Phi^EB > 0
finite field inertia I_A > 0
collective normal phase-rate binding declared
```

The inertia mismatch \(\Delta_I\) remains measurable before promotion of the exact binding.

## 8. Next executable loop

PNCS target:

```text
SOURCE.PHASE_NOETHER.COLLECTIVE_CARRIER.ROUNDTRIP

Euler-closed J_I^EB
 -> P_Phi^EB = J-J_I^EB
 -> collective Noether charge Q_theta = I_A D_tau chi
 -> inertia binding audit I_A/I_phi
 -> epsilon_N^EB = H_Phi^EB/P_Phi^EB
 -> reconstruct rotor carrier
```

Required invariants:

```text
SOURCE.EULER_CLOSURE_SECTOR
SOURCE.ROTOR_KINETIC_CHARGE
SOURCE.NOETHER_FINITE_CHARGE
SOURCE.ROTOR_PHASE_ENERGY
SOURCE.NOETHER_ENERGY_PER_CHARGE
```

## 9. Advancement

```text
local U(1) Noether current                     PASS
polar current J_theta^mu=2 A^2 d^mu theta     PASS
collective-phase finite-charge reduction       PASS_CONDITIONAL
field inertia I_A                              PASS as defined integral
I_A <-> I_phi rotor normalization              OPEN physical cross-binding
Q_theta <-> P_Phi=J-J_I                       PASS_CONDITIONAL on inertia binding
Euler-closed epsilon_N=H/P_Phi                 PASS_CONDITIONAL positive sector
Q_Sigma <-> Q_theta RFC carrier binding        OPEN
local cell/state-space transport               OPEN
```
