# Monograph status

Repository policy: LaTeX source is canonical; compiled PDF is a QA/build artifact.

The monograph now follows the synchronized Retrodiction sequence through 08O:

- `08A_memory_admission.tex` — integrated Memory reference gate;
- `08F_orchorbital_attractors.tex` — ORCHORBITAL attractor dynamics and residence lineage;
- `08I_orchorbital_residence_conditioning.tex` — event-aware Memory/ORCH residence bridge;
- `08J_quotient_fiber_finite_injectivity.tex` — finite-domain quotient/fiber injectivity;
- `08K_oriented_winding_fiber.tex` — ordered signed winding fiber;
- `08L_fiber_lift_composition.tex` — exact carrier/lift composition theorem;
- `08M_stratified_position_lift.tex` — exact active-sequence stratification;
- `08N_per_stratum_position_decoder.tex` — exact coordinate-complete per-stratum decoder baseline and 07K ndarray carrier hardening;
- `08O_winding_radius_position_decoder.tex` — winding-radius exact position decoder and factor-two new-scalar compression.

The current constructive Retrodiction chain is

```text
retained active-sequence stratum
+ ordered signed winding
+ pre-final active radii
+ retained final position
-> winding-radius decoder L_s^(rho W)
-> ordered 07K position carrier
-> exact 07K inverse
-> latent history
```

07T supplies the coordinate-complete Cartesian baseline. For the declared sparse schedule with final position retained in the base record,

\[
|F_{\rm pos}^{baseline}|=2N-2.
\]

07U reuses the already retained ordered winding and replaces the pre-final Cartesian packet with one positive active-attractor radius per pre-final checkpoint,

\[
N_{\rm radial}=N-1,
\qquad
\frac{N_{\rm radial}}{N_{\rm Cartesian}}=\frac12
\quad(N>1).
\]

The executable 07U decoder reconstructs the ordered position carrier segment by segment using the exact retained active-attractor sequence. The final retained position supplies an independent consistency check against the last winding increment. A switching A->B reference trajectory exercises the segment-wise change of active center.

Hosted Retrodiction evidence:

- 07P run `33200684482`: `495 passed in 10.14s`;
- 07Q run `33201861565`: `502 passed in 8.09s`;
- 07R run `33202559485`: `510 passed in 14.11s`;
- 07S run `33203339457`: `518 passed in 12.06s`;
- 07T corrected run `33204551313`, job `98962152065`: `528 passed in 14.20s`;
- all-branch integration PR #24: `534/534 PASS`;
- final 07T consolidation: `534/534 PASS`;
- 07U run `33205507810`, job `98965399355`: `551 passed in 12.09s`;
- 07U merge commit: `f6ccb49cecbe9da9beb91f29b1c7bbc9e15283f3`.

Current monograph Retrodiction status:

```text
EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS
FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS
07K_NDARRAY_CARRIER_INTERFACE_PASS
EXACT_WINDING_RADIUS_POSITION_DECODER_PASS
POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED
CONDITIONAL_AUGMENTED_WINDING_RADIUS_RECONSTRUCTION_PASS
GENERAL_GLOBAL_INJECTIVITY_OPEN
```

The next implementation coordinate is direct append-only binding of the radial packet to the persisted ORCHORBITAL residence lineage, preserving one provenance path from residence observation to compressed position carrier.

The Einstein chapter remains downstream of both the temporal/retrodiction spine and the parallel IDT 01AG -> RFC RF-M1/RF-E0 relativistic field prerequisite recorded in the executable dependency graph.
