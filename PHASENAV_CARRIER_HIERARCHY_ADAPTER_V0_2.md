# IDT adapter — PhaseNav carrier hierarchy v0.2

Status: `CANDIDATE_ONLY / TEMPORAL_CORE_MUTATED_FALSE / CANON_WRITE_AUTHORITY_FALSE / EPISTEMIC_CHYBA`.

This adapter records dimensional and parameterisation compatibility only. It does not alter the IDT temporal core, monotone elapsed coordinate, clock/covering lift, chirality rules, or any existing canonical temporal equation.

Imported candidate carrier metadata:

- `H ~ C^2 ~ R^4`, pure-state space `CP^1`, 1Q;
- `O ~ C^4 ~ R^8`, pure-state space `CP^3`, 2Q;
- `S_16 ~ C^8 ~ R^16`, pure-state space `CP^7`, 3Q;
- `A_32 ~ C^16 ~ R^32`, pure-state space `CP^15`, 4Q.

`S_16` and `A_32` are dimensional carrier labels. They are not physical ion counts. `PHYSICAL_ION_BINDING_OPEN` remains mandatory.

IDT may provide a declared temporal parameter `tau` to a candidate family `P_n(tau)`, `H_n(tau)`, connection `A_n(tau)`, or an observable family, enabling evaluation of quantities such as

`d_tau P_n`, `QGT_{tau,tau}`, Berry connection along `tau`, transition-response derivatives, and connection/curvature defects along the declared trajectory.

The 4Q ceiling is imported from `PHASENAV_CARRIER_HIERARCHY_V0_2`; it is not an IDT canonical statement. Any request for a 5Q-or-higher carrier through this adapter is unsupported and must fail closed until a separately validated PhaseNav contract extends the hierarchy.

No statement in this adapter identifies IDT elapsed time with laboratory time, energy, mass, gravity, spectroscopy, a physical ion device, Standard-Model fields, or a Cayley–Dickson substrate. Those remain separate calibration and falsification problems.

Invariant: `temporal_core_mutated=false`.
