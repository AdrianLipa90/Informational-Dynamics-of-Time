# Monograph status

Repository policy: LaTeX source is canonical; compiled PDF is a local QA artifact and is not committed.

Current downstream reference chapters now include the Retrodiction sequence through 08N:

- `08A_memory_admission.tex` — integrated Memory reference gate;
- `08F_orchorbital_attractors.tex` — ORCHORBITAL attractor dynamics and residence lineage;
- `08I_orchorbital_residence_conditioning.tex` — event-aware Memory/ORCH residence bridge;
- `08J_quotient_fiber_finite_injectivity.tex` — finite-domain quotient/fiber injectivity;
- `08K_oriented_winding_fiber.tex` — ordered signed winding fiber;
- `08L_fiber_lift_composition.tex` — exact carrier/lift composition theorem;
- `08M_stratified_position_lift.tex` — exact active-sequence stratification;
- `08N_per_stratum_position_decoder.tex` — exact coordinate-complete per-stratum decoder baseline and 07K ndarray carrier hardening.

The Retrodiction composition is

```text
retained active-sequence stratum
+ retained base/fiber coordinates
-> per-stratum decoder L_s
-> ordered 07K position carrier
-> exact 07K inverse
-> latent history
```

07T supplies the exact baseline decoder using complete Cartesian position coverage. For the declared sparse schedule with final position retained in the base record,

\[
\boxed{|F_{\rm pos}^{baseline}|=2N-2}.
\]

The active monograph frontier is now

```text
EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS
FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS
07K_NDARRAY_CARRIER_INTERFACE_PASS
POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE
GENERAL_GLOBAL_INJECTIVITY_OPEN
```

Hosted Retrodiction evidence:

- 07P run `33200684482`: `495 passed in 10.14s`;
- 07Q run `33201861565`: `502 passed in 8.09s`;
- 07R run `33202559485`: `510 passed in 14.11s`;
- 07S run `33203339457`: `518 passed in 12.06s`;
- 07T corrected run `33204551313`, job `98962152065`: `528 passed in 14.20s`;
- all-branch integration PR #24: `534/534 PASS`;
- latest 07T forward-port PR #26: `534/534 PASS`.

The monograph's Einstein chapter remains downstream of both the temporal/retrodiction spine and the parallel IDT 01AG -> RFC RF-M1/RF-E0 relativistic field prerequisite recorded in the executable dependency graph.
