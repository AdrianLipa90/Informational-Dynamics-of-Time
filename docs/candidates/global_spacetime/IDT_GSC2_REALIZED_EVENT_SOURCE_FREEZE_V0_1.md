# IDT GSC-2 Realized-Event Source Freeze v0.1

Status: `SOURCE_CAPTURE_DEFINED / DETERMINISTIC_FREEZE / 05H_HANDOFF / PRODUCTION_EVENT_COMPLEX_OPEN`

Date: 2026-08-31

## Purpose

The GSC-2 input contract consumes canonical event incidence with positive elapsed edges. This source-freeze layer provides the preceding acquisition interface for a realized event carrier.

The flow is

```text
source-owned realized event capture
 -> deterministic event/edge normalization
 -> source-capture SHA-256
 -> IDT_GLOBAL_EVENT_COMPLEX_INPUT_V0_1
 -> canonical incidence SHA-256
 -> 05H exactness certifier
```

## Capture schema

Schema:

`IDT_REALIZED_EVENT_COMPLEX_CAPTURE_V0_1`

A capture contains:

- `capture_id`;
- source `source_id`;
- source class in `{PRODUCTION_SOURCE, REFERENCE_CONTROL, CANDIDATE_SOURCE}`;
- immutable source reference;
- source `clock_id`;
- a 64-hex capture receipt for `PRODUCTION_SOURCE`;
- realized event records carrying unique `event_id` values;
- realized directed elapsed edges carrying unique `edge_id`, `source`, `target`, and positive `dtheta`.

Machine-readable schema:

`docs/candidates/global_spacetime/IDT_REALIZED_EVENT_COMPLEX_CAPTURE_V0_1.schema.json`

## Deterministic freeze

Implementation:

`src/idt/global_event_complex_source_freeze.py`

The adapter canonicalizes event order and elapsed-edge order for source-capture hashing. It then builds the existing GSC-2 dataset and immediately invokes the current input/05H validator.

The frozen dataset preserves:

- `source_class`;
- `clock_id`;
- source immutable reference;
- source capture SHA-256;
- capture receipt when supplied;
- canonical event-incidence SHA-256.

This gives the acquisition record and the graph-incidence record separate digests while retaining their lineage relation.

## Production admission

`PRODUCTION_SOURCE` admission requires `capture_receipt_sha256`. The downstream production condition remains

```text
source_class = PRODUCTION_SOURCE
AND capture receipt admitted
AND input_valid
AND integrity_valid
AND exact_clock_certified
```

The temporal exactness bit is evaluated by 05H from the supplied event data. It remains independent of structural input integrity.

## Controls

Reference tests cover:

- exact three-event cycle capture;
- canonical invariance under source record reordering;
- temporal-holonomy defect with valid structural input;
- production capture receipt gate;
- duplicate event and edge identifiers;
- undeclared event references;
- clock-lineage contribution to the source-capture digest.

Reference test:

`tests/reference/test_global_event_complex_source_freeze.py`

Target verdict:

`PASS_IDT_GSC2_SOURCE_FREEZE_WITH_PRODUCTION_CAPTURE_AND_05H_EXACTNESS_GATES`.
