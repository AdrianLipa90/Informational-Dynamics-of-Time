# 01Y — Phase-Intention Energy-per-Action-Charge Interface

Status: `FLOQUET_CHARGE_ENERGY_RATIO_EXACT_PASS / RFC_CARRIER_CROSS_BINDING_OPEN / LOCAL_CURRENT_LIFT_OPEN`

This interface isolates the energy-normalization statement already present in the admitted phase-intention Hamiltonian scaffold and exports it to the coupled IDT ↔ PNCS ↔ RFC source branch.

It is a parallel cross-repository interface gate. The canonical Temporal Primitive → Temporal Wave admission order remains unchanged.

## 1. Pinned phase-intention inputs

`Phase_Intention_Hamiltonian_Formal_Derivations.tex` defines the intention charge

\[
\boxed{
J_{I,s}(\tau,k)=\hbar\,\rho_s(k)\,\mathcal I_s(\tau,k)
}
\]

and the discrete Floquet phase Hamiltonian

\[
\boxed{
H_{\Phi,s}(\tau,k)
=\frac{\hbar}{\Delta\tau_k}\,\rho_s(k)\,\mathcal I_s(\tau,k).
}
\]

The same source defines the one-step propagator by

\[
U_\Phi(k+1,k)
=\exp[-i\rho_s(k)\mathcal I_s(k)]
=\exp\!\left[-\frac{i}{\hbar}\Delta\tau_k H_\Phi(k)\right].
\]

The Floquet time step is taken on the positive sector

\[
\Delta\tau_k>0.
\]

## 2. Exact charge-energy transport theorem

The two pinned definitions share the same operator factor

\[
\hbar\rho_s(k)\mathcal I_s(\tau,k).
\]

Therefore

\[
\boxed{
\Delta\tau_k H_{\Phi,s}=J_{I,s}
}
\]

and equivalently

\[
\boxed{
H_{\Phi,s}=\epsilon_{I,k}J_{I,s},
\qquad
\epsilon_{I,k}:=\frac{1}{\Delta\tau_k}.
}
\]

This identity is valid directly at the operator level and therefore remains defined on the zero-charge sector without dividing by \(J_{I,s}\).

The cancellation is independent of the numerical value of the rhythm \(\rho_s(k)\) and independent of the eigenvalue/expectation of \(\mathcal I_s\): those factors occur identically on both sides.

## 3. Dimensional type

From

\[
\exp\!\left[-\frac{i}{\hbar}\Delta\tau_kH_\Phi\right]
\]

the product \(\Delta\tau_kH_\Phi\) has action type. Since

\[
J_{I,s}=\Delta\tau_kH_{\Phi,s},
\]

\(J_{I,s}\) is an action-charge coordinate and

\[
\boxed{
[\epsilon_I]=[H/J_I]=T^{-1}.
}
\]

Thus `energy per carrier charge` has frequency type when the carrier charge is action-valued.

## 4. RFC source-normalization candidate

RFC RF-N1B2 uses the typed continuous conversion

\[
\varepsilon_Q=\epsilon_Q j_Q,
\qquad
\rho_Q=\frac{\epsilon_Q}{c^2}j_Q.
\]

01Y exports the candidate binding

\[
\boxed{
Q_\Sigma\stackrel{?}{\longleftrightarrow}J_{I,s}
}
\]

with the associated normalization

\[
\boxed{
\epsilon_Q\stackrel{?}{\longleftrightarrow}\epsilon_{I,k}
=\frac1{\Delta\tau_k}.
}
\]

Under an admitted action-charge carrier binding, the source mass coordinate becomes

\[
\boxed{
M_I
=\frac{J_{I,s}}{c^2\Delta\tau_k}
=\frac{H_{\Phi,s}}{c^2}.
}
\]

This is the extensive counterpart of the RFC cell/source factorization.

## 5. Local current lift gate

A local RFC source density requires a local current whose slice charge integrates to the same action charge:

\[
\boxed{
J_{I,s}
\stackrel{?}{=}
\int_{\Sigma_t}j_I\,dV_h.
}
\]

Once a conserved local current lift is admitted, the phase-intention source transport is

\[
\boxed{
\rho_I(x)
=\frac{1}{c^2\Delta\tau_k}j_I(x).
}
\]

Candidate local carriers already present upstream include the U(1) Noether current and the temporal-fluid current. Their binding to the finite phase-intention charge is retained as an explicit interface gate.

Current gate state:

```text
Floquet J_I <-> H_Phi operator identity       PASS
energy/action-charge epsilon_I=1/Delta_tau    PASS
Q_Sigma <-> J_I RFC carrier binding           OPEN
finite J_I <-> local conserved-current lift   OPEN
local measure/cell transport                  OPEN
```

## 6. Relation to q0

The continuous 01Y transport closes the energy-per-charge coordinate without requiring a discrete occupation number.

A separate compact-U(1) quantization gate may later bind a canonical phase-charge spacing and a discrete carrier count. That gate is independent of the continuous identity

\[
H_{\Phi,s}=J_{I,s}/\Delta\tau_k.
\]

## 7. PNCS information-holonomy contract

The corresponding executable control loop is

```text
SOURCE.PHASE_INTENTION.CHARGE_ENERGY.ROUNDTRIP

J_I
  -> H_Phi = J_I / Delta_tau
  -> J_I' = Delta_tau H_Phi
```

with the exact control invariant

```text
SOURCE.INTENTION_ACTION_CHARGE
```

and declared normalization

```text
epsilon_I = 1 / Delta_tau
```

The PNV audit must bind the same positive `Delta_tau` on both transport edges and report the state holonomy defect together with inverse lineage.

## 8. Coupled frontier

The next coupled source step is now sharply localized:

\[
\boxed{
\text{derive/admit }J_I\leftrightarrow Q_\Sigma
\quad\text{and}\quad
J_I\leftrightarrow\int j_I dV_h.
}
\]

Once those bindings pass, the existing RFC `epsilon_Q` source-density route receives the exact Floquet normalization \(1/\Delta\tau_k\), and the resulting transport can be inserted into the larger IDT ↔ PNCS ↔ RFC physical-law loop.
