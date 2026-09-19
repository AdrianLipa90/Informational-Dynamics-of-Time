# Canonical surface index

Status: `CURRENT_MAIN_SURFACE_MAP / STATUS_PRESERVING_CONSOLIDATION`

This index maps active Informational Dynamics of Time surfaces to repository locations. Presence on `main` does not itself promote an evidence class.

## Core clock and global-time chain

- 05H event-clock exactness: `formalism/05H_global_event_clock_exactness.md`, `src/idt/global_event_clock_exactness.py`.
- 05I regular smooth clock extension: `formalism/05I_regular_smooth_clock_extension.md`, `src/idt/regular_smooth_clock_extension.py`.
- 05J production event-complex input: `formalism/05J_production_event_complex_input_contract.md`, `src/idt/production_event_complex_input.py`.
- 05K precision-safe global-lapse capture: `formalism/05K_global_lapse_precision_capture.md`, `src/idt/global_lapse_precision_production_capture.py`, `src/idt/global_lapse_precision_evidence_v0_2.py`, `src/idt/global_lapse_precision_receipt_v0_2.py`.

05K remains a source/integrity contract; it does not self-canonize a physical realization.

## Event-complex source freeze

- documentation/schema: `docs/candidates/global_spacetime/`;
- implementation: `src/idt/global_event_complex_input.py`, `src/idt/global_event_complex_source_freeze.py`, `src/idt/freeze_global_event_complex.py`;
- tests: `tests/reference/test_global_event_complex_input.py`, `tests/reference/test_global_event_complex_source_freeze.py`;
- receipt: `validation/IDT_GSC2_PRODUCTION_EVENT_COMPLEX_INPUT_V0_1.receipt.json`.

The freeze step has no repository-promotion authority.

## Temporal density / material NOW crosswalk

- `formalism/02JO_temporal_density_material_front_now_crosswalk.md`;
- `src/idt/temporal_material_front.py`;
- `tests/reference/test_temporal_material_front.py`.

Status remains `FORMAL_CANDIDATE / MATERIAL_FRONT_KINEMATICS_AND_NOW_SELECTOR_GATE`.

## EB/BEC nonlinear Madelung / orbital / acoustic candidate

- `formalism/02JP_eb_bec_orbital_bogoliubov_acoustic_bridge.md`;
- `src/idt/eb_bec_madelung_bridge.py`;
- `tests/reference/test_eb_bec_madelung_bridge.py`;
- `validation/EB_BEC_MADELUNG_BRIDGE_V0_1.json`.

Status remains `FORMAL_CANDIDATE / CONDITIONAL_SPATIAL_LIFT / NO_SPACETIME_PROMOTION`. The hosted reference suite validates the algebra and fail-closed contract but does not bind the one-dimensional IDT continuum to physical space, identify GREMLIN source roles with a condensate experiment, calibrate the RFC information-potential coupling, or identify the analogue acoustic metric with spacetime geometry.

## 600-cell / S3 candidate carrier

The two PhaseNav adapter contracts remain at repository root because their existing candidate workflows validate those exact locations:

- `PHASENAV_CARRIER_HIERARCHY_ADAPTER_V0_2.md`;
- `PHASENAV_PROMOTION_GEOMETRY_ADAPTER_V0_1.md`.

IDT candidate dependency notes are grouped under `docs/candidates/geometry/`. Executable surfaces are `src/idt/orchorbital_600cell_candidate_v01.py` and `tests/reference/test_orchorbital_600cell_candidate_v01.py`.

Invariant: `canonical=false`, `temporal_core_mutated=false`, `physical_time_binding=OPEN`.

## Onsager seam API

The public dissipation contract is `src/idt/schrodinger_onsager_seam_balance.py`. Scalar and matrix mobility use one PSD normalization path; boolean scalar mobility is rejected fail-closed. Regression coverage: `tests/reference/test_onsager_dissipation_contract.py`.

## Monograph

Canonical entry point: `monograph/main.tex`. Chapters 10--14 are populated under `monograph/chapters/`. Build authority: `.github/workflows/monograph-pdf.yml`.

## Machine-readable dependency authority

`validation/dependency_graph.json` is the machine-readable dependency authority. Candidate/source-contract nodes remain explicitly typed and do not satisfy canonical promotion gates merely by being present.
