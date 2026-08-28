# 01Y — Euler-Closed Phase-Intention Energy-per-Action-Charge Interface

Status: `EULER_CLOSED_ACTION_CHARGE_PASS / ROTOR_ENERGY_PER_CHARGE_PASS_CONDITIONAL / RFC_CARRIER_CROSS_BINDING_OPEN / LOCAL_CURRENT_LIFT_OPEN`

This interface orders the source-normalization derivation as

```text
Euler/Berry closure
  -> allowed intention phase
  -> finite phase action-charge J_I
  -> canonical rotor energy H_Phi
  -> energy per action-charge epsilon_I
  -> effective Floquet time step Delta_tau_eff
  -> RFC carrier binding
```

It is a parallel cross-repository interface gate. The canonical Temporal Primitive -> Temporal Wave admission order is unchanged.

## 1. Euler/Berry closure comes first

The pinned phase-intention scaffold defines

\[
\Phi_{\rm tot}
=\Phi_{AB}+\Phi_B+\Phi_E+\Theta_I
=2\pi(D+\epsilon_{EB}),
\]

where

\[
\Phi_B=\int_\Sigma\mathcal F_B,
\qquad
\Phi_E=s_E\int_\Sigma\mathcal R_E.
\]

For a selected step, write all already accumulated intention phase before that step as \(\Theta_I^{<k}\). The Euler/Berry closure residual assigned to the next intention step is therefore

\[
\boxed{
\theta_{I,k}^{EB}
=2\pi(D+\epsilon_{EB})
-\Phi_{AB}
-\int_\Sigma(\mathcal F_B+s_E\mathcal R_E)
-\Theta_I^{<k}.
}
\]

At exact holonomic closure, \(\epsilon_{EB}=0\).

The important ordering rule is that the allowed intention phase is obtained from the closure sector before any energy-per-charge normalization is assigned.

## 2. Euler-closed action charge

The phase-intention derivation defines the intention action-charge for one step as

\[
J_{I,k}=\hbar\rho_s(k)\mathcal I_s(k).
\]

The same dimensionless phase increment is

\[
\theta_{I,k}=\rho_s(k)\mathcal I_s(k).
\]

Hence after Euler/Berry closure fixes the admissible phase residual,

\[
\boxed{
J_{I,k}^{EB}=\hbar\theta_{I,k}^{EB}.
}
\]

This is the first non-arbitrary normalization produced by the closure chain: topology/holonomy fixes phase and phase fixes action-charge.

## 3. Canonical rotor supplies the independent energy scale

The same pinned Hamiltonian scaffold contains the canonical phase rotor

\[
\boxed{
H_{\Phi,k}^{\rm rotor}
=\frac{(J_k-J_{I,k})^2}{2I_\phi}.
}
\]

Substituting the Euler-closed action charge gives

\[
\boxed{
H_{\Phi,k}^{EB}
=\frac{\left(J_k-\hbar\theta_{I,k}^{EB}\right)^2}{2I_\phi}.
}
\]

This step is important: the energy scale is supplied by the canonical rotor, so the derivation does not assume a Floquet time step in advance.

## 4. Energy per action-charge after Euler

On the positive non-degenerate action-charge sector

\[
J_{I,k}^{EB}>0,
\qquad
H_{\Phi,k}^{EB}>0,
\]

define

\[
\boxed{
\epsilon_{I,k}^{EB}
:=\frac{H_{\Phi,k}^{EB}}{J_{I,k}^{EB}}
=\frac{\left(J_k-\hbar\theta_{I,k}^{EB}\right)^2}
{2I_\phi\hbar\theta_{I,k}^{EB}}.
}
\]

Because \(J_I\) has action type and \(H_\Phi\) has energy type,

\[
\boxed{[\epsilon_I]=T^{-1}.}
\]

Thus the energy-per-action-charge normalization is obtained only after Euler/Berry closure has selected the admissible phase/action-charge sector.

## 5. Floquet time step becomes derived

The Floquet representation satisfies

\[
\Delta\tau_kH_{\Phi,k}=J_{I,k}.
\]

Using the Euler-closed rotor quantities, define the effective step

\[
\boxed{
\Delta\tau_{k,\rm eff}^{EB}
:=\frac{J_{I,k}^{EB}}{H_{\Phi,k}^{EB}}
=\frac{1}{\epsilon_{I,k}^{EB}}.
}
\]

Therefore the correct logical direction for this interface is

\[
\boxed{
\text{Euler/Berry}
\to\theta_I^{EB}
\to J_I^{EB}
\to H_\Phi^{EB}
\to\epsilon_I^{EB}
\to\Delta\tau_{\rm eff}^{EB}.
}
\]

The earlier identity \(H_\Phi=J_I/\Delta\tau\) remains exact as a Floquet representation, but it is no longer used as the primary derivation of \(\epsilon_I\).

## 6. RFC source-normalization candidate

RFC RF-N1B2 uses

\[
\varepsilon_Q=\epsilon_Qj_Q,
\qquad
\rho_Q=\frac{\epsilon_Q}{c^2}j_Q.
\]

01Y exports the typed candidate binding

\[
\boxed{Q_\Sigma\stackrel{?}{\longleftrightarrow}J_I^{EB}}
\]

and, only in that admitted bound sector,

\[
\boxed{\epsilon_Q\stackrel{?}{\longleftrightarrow}\epsilon_I^{EB}.}
\]

The associated extensive source-mass coordinate is then

\[
\boxed{
M_I
=\frac{\epsilon_I^{EB}J_I^{EB}}{c^2}
=\frac{H_\Phi^{EB}}{c^2}.
}
\]

No Newton matching condition enters this derivation.

## 7. Local current lift gate

A local RFC source density additionally requires a conserved current whose slice charge equals the Euler-closed action charge:

\[
\boxed{
J_I^{EB}
\stackrel{?}{=}
\int_{\Sigma_t}j_I\,dV_h.
}
\]

After that binding,

\[
\boxed{
\rho_I(x)
=\frac{\epsilon_I^{EB}}{c^2}j_I(x).
}
\]

The U(1) Noether current and temporal-fluid current remain explicit candidate current lifts for a later cross-binding gate.

## 8. Degenerate sectors and fail-closed conditions

The ratio form is evaluated only when

```text
I_phi > 0
J_I^EB > 0
H_Phi^EB > 0
all phase inputs finite
```

The linear/action-charge relation \(J_I^{EB}=\hbar\theta_I^{EB}\) remains meaningful before ratio evaluation. A zero closure residual or a rotor degeneracy \(J=J_I^{EB}\) is therefore retained as a separately typed sector rather than forcing a division.

## 9. PNCS information-holonomy contract

The executable control loop is upgraded to

```text
SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP

Euler/Berry closure data
  -> theta_I^EB
  -> J_I^EB = hbar theta_I^EB
  -> H_Phi^EB = (J-J_I^EB)^2/(2 I_phi)
  -> epsilon_I^EB = H_Phi^EB/J_I^EB
  -> Delta_tau_eff^EB = 1/epsilon_I^EB
  -> reconstruct J_I^EB
```

Required invariants:

```text
SOURCE.EULER_CLOSURE_SECTOR
SOURCE.INTENTION_ACTION_CHARGE
SOURCE.ROTOR_PHASE_ENERGY
SOURCE.ENERGY_PER_ACTION_CHARGE
```

The receipt must preserve the Euler/Berry inputs, closure defect, selected sector `D`, \(\theta_I^{EB}\), \(J_I^{EB}\), rotor parameters, \(H_\Phi^{EB}\), \(\epsilon_I^{EB}\), effective time step and inverse lineage.

## 10. Advancement state

```text
Euler/Berry closure equation                    PASS
Euler residual -> action charge J_I^EB          PASS
rotor energy from J, J_I^EB, I_phi              PASS
energy/action-charge epsilon_I^EB               PASS_CONDITIONAL positive non-degenerate sector
Delta_tau_eff=1/epsilon_I^EB                    PASS_CONDITIONAL same sector
Q_Sigma <-> J_I^EB RFC carrier binding          OPEN
finite J_I^EB <-> local conserved-current lift  OPEN
local measure/cell transport                    OPEN
```

The next coupled derivation target is therefore the finite Euler-closed action charge ↔ conserved local current lift, followed by the physical RFC carrier binding.