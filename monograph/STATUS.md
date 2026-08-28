# Monograph status

Repository policy: LaTeX source is canonical; compiled PDF is a local QA artifact and is not committed.

Current included downstream reference chapters:

- `08A_memory_admission.tex` — integrated Memory reference gate;
- `08B_retrodiction_contract.tex` — withheld-lineage inverse problem;
- `08C_retrodiction_uncertainty.tex` — covariance and local Fisher geometry;
- `08D_partial_checkpoint_selection.tex` — partial-retention observability and conditioning;
- `08E_weighted_retrodiction_nulls.tex` — covariance-weighted estimator and permutation-null ensemble;
- `08F_orchorbital_attractors.tex` — ORCHORBITAL attractor dynamics, residence lineage, pinned PNCS hierarchy and typed observables;
- `08G_spatial_offset_divergence.tex` — spatial-offset/divergence witness layer;
- `08H_adaptive_sod_separation.tex` — adaptive SOD separator layer;
- `08I_orchorbital_residence_conditioning.tex` — event-aware Memory/ORCH residence bridge and global-null residence-label audit;
- `08J_quotient_fiber_finite_injectivity.tex` — all-collision finite-domain quotient/fiber injectivity gate;
- `08K_oriented_winding_fiber.tex` — ordered signed ORCHORBITAL winding as an explicit Retrodiction fiber coordinate;
- `08L_fiber_lift_composition.tex` — exact composition theorem linking retained base/fiber coordinates to an injective position-lineage carrier.

Promotion-branch admitted frontier:

`Temporal Transport -> Memory -> ORCHORBITAL Attractors`.

Retrodiction is the active next dependency gate. 07P, 07Q and 07R now organize the global closure as

```text
retained base + fiber coordinates
-> single-valued position-lineage lift
-> exact 07K inverse carrier
-> latent history
```

The exact 07R theorem states that if the position-lineage carrier `P` is injective and `P = L o (Y,F)` for a single-valued lift `L`, then the augmented retained observation `(Y,F)` is injective. The active constructive target is `POSITION_LINEAGE_LIFT_ACTIVE_NEXT_GATE`; the governing global status remains `GENERAL_GLOBAL_INJECTIVITY_OPEN`.

Memory hosted admission evidence: run `33193861826`, job `98925901636`, `431 passed in 7.08s`.

ORCHORBITAL completion evidence includes:

- residence long-profile run `33194693525`: `440 passed in 14.50s`;
- strict residence-schema run `33194962289`: `449 passed in 9.19s`;
- PNCS hierarchy-binding run `33195337839`: `457 passed in 13.90s`;
- typed-observable completion run `33196818703`: `475 passed in 11.91s`;
- synchronized ORCHORBITAL admission checkpoint run `33197346515`: `476 passed in 11.95s`.

Retrodiction evidence includes:

- event-aware residence hardening run `33198069462`: `486 passed in 8.89s`;
- quotient/fiber run `33200684482`, job `98949092398`: `495 passed in 10.14s`;
- oriented-winding run `33201861565`, job `98953023513`: `502 passed in 8.09s`;
- fiber-lift composition run `33202559485`, job `98955383447`: `510 passed in 14.11s` on tested branch head `6abca4ad72c04cdca5d1128e690c17898b8650d7`;
- 07R receipt: `validation/RETRODICTION_FIBER_LIFT_COMPOSITION_V0_1.json`.

Admission receipts:

- `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`;
- `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

Canonical `main` remains unchanged until explicit merge authorization.
