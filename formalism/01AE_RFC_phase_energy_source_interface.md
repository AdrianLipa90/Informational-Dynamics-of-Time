# 01AE — RFC Phase-Energy Source Interface

Status: `EXACT_PHASE_ENERGY_CURRENT_FACTORIZATION / RFC_SOURCE_HANDOFF_PASS_CONDITIONAL / GRAVITY_COUPLING_RFC_OWNED`

01AE follows 01AD and exports the gauge-covariant proper-time phase rate and its local Noether-energy factorization to the Relational Field Closure source layer.

## 1. Proper-time phase-rate coordinate

01AD supplies the exact conditional bridge

\[
\boxed{
\omega_Q
:=D_{\hat\tau}\chi
=r_n^{(\tau)}
=\frac{D_t\chi}{N_R}.
}
\]

The corresponding energy-per-action-charge coordinate is

\[
\boxed{
\epsilon_N
=\frac12\omega_Q
=\frac{D_t\chi}{2N_R}.
}
\]

These are the IDT source-normalization coordinates handed downstream.

## 2. Local phase Noether carrier

For the admitted complex scalar phase field

\[
\psi=Ae^{i\vartheta},
\]

with the gauge-covariant phase one-form from 01AC, the positive normal-flow phase carrier density is

\[
\boxed{
j_\vartheta
=2A^2\omega_Q.
}
\]

This is the local normal component of the same Noether carrier whose collective reduction appears in 01AB–01AD.

## 3. Local phase-energy factorization

The normal phase-rate Hamiltonian density is

\[
\boxed{
\mathcal E_\vartheta
=A^2\omega_Q^2.
}
\]

Using the carrier density,

\[
\mathcal E_\vartheta
=A^2\omega_Q^2
=\frac{\omega_Q}{2}(2A^2\omega_Q).
\]

Therefore

\[
\boxed{
\mathcal E_\vartheta
=\epsilon_N j_\vartheta.
}
\]

The identity is local and remains valid for spatially varying `A(x)` and `omega_Q(x)` on the admitted regular positive-source sector.

## 4. RFC mass-density consumer coordinate

The RFC source interface receives the equivalent phase-sector mass-density coordinate

\[
\boxed{
\rho_\vartheta
=\frac{\mathcal E_\vartheta}{c^2}
=\frac{\epsilon_N}{c^2}j_\vartheta
=\frac{A^2\omega_Q^2}{c^2}.
}
\]

Using the relational lapse,

\[
\boxed{
\rho_\vartheta
=\frac{A^2}{c^2}
\left(\frac{D_t\chi}{N_R}\right)^2.
}
\]

This is the typed handoff consumed by RFC RF-N1B2O and the downstream RF-N1C coupling/universality gates.

## 5. Collective consistency

For one common proper-time rate on a slice,

\[
Q_\vartheta
=\int_\Sigma j_\vartheta dV_h,
\qquad
H_\vartheta
=\int_\Sigma\mathcal E_\vartheta dV_h.
\]

Using

\[
I_A=2\int_\Sigma A^2dV_h,
\]

one obtains

\[
\boxed{
Q_\vartheta=I_A\omega_Q,
\qquad
H_\vartheta=\frac12I_A\omega_Q^2,
}
\]

and therefore

\[
\boxed{
\frac{H_\vartheta}{Q_\vartheta}
=\frac12\omega_Q
=\epsilon_N.
}
\]

Thus the local field-density handoff and the collective rotor normalization carry the same energy-per-carrier coordinate.

## 6. Interface ownership

IDT 01AE exports the following source primitives:

```text
N_R
D_t chi
omega_Q = D_hat_tau chi = D_t chi / N_R
epsilon_N = omega_Q / 2
A
j_theta = 2 A^2 omega_Q
E_theta = epsilon_N j_theta
rho_theta = E_theta / c^2
```

RFC owns the downstream gravitational source operator, Newton coupling audit, double-copy comparison, Einstein normalization and universality tests.

The electromagnetic charge projection remains separately typed at the RFC Maxwell interface.

## 7. Admission surface

01AE inherits:

- 05C calibrated relational lapse;
- 01AC gauge-covariant common-U(1) phase pullback;
- 01AB scalar-field/rotor coefficient reduction;
- 01AD normal proper-time phase-rate bridge;
- common phase-field normalization and physical measure;
- positive regular source sector for the carrier ratio.

## 8. RFC handoff

Canonical downstream consumer:

```text
AdrianLipa90/Relational-Field-Closure
formalism/RFN1B2O_PHASE_ENERGY_CURRENT_SOURCE_BINDING.md
```

The exported identity is

\[
\boxed{
\rho_\vartheta c^2
=\mathcal E_\vartheta
=\epsilon_N j_\vartheta.
}
\]

This closes the IDT-side source-energy handoff while preserving the RFC-side coupling and universality gates as independently audited downstream structure.
