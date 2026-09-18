# IDT adapter — PhaseNav promotion geometry v0.1

Status: `CANDIDATE_ONLY / TEMPORAL_CORE_MUTATED_FALSE / CANON_WRITE_AUTHORITY_FALSE / EPISTEMIC_CHYBA`.

This adapter records compatibility only. It does not alter the IDT temporal core, monotone elapsed coordinate, clock/covering lift, or existing canonical equations.

Imported candidate objects:

- metric defect `Delta_G = P^† G' P - G`;
- complex-structure defect `Upsilon = J'P - PJ`;
- connection defect `Xi = D'P - PD`;
- curvature defect `Delta_F = F'P - PF`;
- quantum geometric tensor `QGT_{mu,nu} = (d_mu P)^†(I-PP^†)(d_nu P)`.

IDT may supply a declared temporal parameter `tau` to a promotion family `P(tau)` or Hamiltonian family `H(tau)`. In that case the adapter permits evaluation of `d_tau P`, Berry connection, quantum metric and transition-response quantities along the IDT coordinate.

No statement in this adapter identifies IDT elapsed time with laboratory time, energy, mass, gravity, spectroscopy or a physical Cayley–Dickson carrier. Those bindings remain separate calibration/falsification problems.

Invariant: `temporal_core_mutated=false`.
