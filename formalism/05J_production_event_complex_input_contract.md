# 05J — Production Event-Complex Input Contract

Status: `INPUT_CONTRACT_DEFINED / 05H_HANDOFF_FAIL_CLOSED / PRODUCTION_EVENT_COMPLEX_OPEN`

## Purpose

05H proves exactness of the elapsed-time one-cochain on a supplied connected event graph. The remaining GSC-2 dependency is the concrete global event incidence and the branch-merger/identity quotient that converts prefix occurrences into event vertices.

05J makes that input explicit and machine-readable.

## Quotient carrier

Let `O` be the finite supplied set of occurrence identifiers produced by realized-history bookkeeping. A supplied partition

\[
q:O\to E
\]

defines event classes. In machine form each event class has one `event_id` and a non-empty list of occurrence `members`.

05J requires that every supplied occurrence belongs to exactly one event class. This makes mergers explicit rather than inferred from matching labels.

## Directed elapsed edges

Each supplied relation edge contains:

- `source_event`;
- `target_event`;
- positive finite `dtheta`;
- a non-empty `source_relation_id` for provenance.

After input validation these are converted directly to the existing 05H `EventEdge` objects and passed to `certify_event_clock`.

## Integrity contract

The dataset also carries:

- schema `IDT_PRODUCTION_EVENT_COMPLEX_INPUT_V0_1`;
- non-empty `dataset_id`;
- explicit boolean `production`;
- provenance `source` and `source_commit_or_digest`;
- canonical `incidence_sha256` over occurrences, quotient classes and directed elapsed edges.

The contract rejects malformed partitions, duplicated membership, unknown edge endpoints, duplicate relation identifiers, non-positive elapsed increments, missing provenance and digest mismatch.

## 05H handoff and promotion

A structurally valid dataset may still fail 05H because of temporal holonomy. 05J retains that as `exact_clock_certified=false` rather than hiding it as an input parse error.

Promotion requires

```text
production = true
AND input_valid
AND integrity_valid
AND quotient_valid
AND exact_clock_certified
```

The reference diamond contains an explicit merger class and equal elapsed sums along both paths. It is frozen with `production=false` and therefore cannot itself promote GSC-2.

## Dependency result

```text
00F prefix occurrences
 + supplied occurrence-to-event quotient
 + supplied directed elapsed-edge incidence
 -> 05J provenance / digest / quotient gate
 -> 05H temporal-holonomy certifier
 -> GSC-2 production event-complex eligibility
```

The production event complex remains an open source-owned input.

## Validation authority

Implementation:
`src/idt/production_event_complex_input.py`

Reference tests:
`tests/reference/test_production_event_complex_input.py`

Static contract receipt:
`validation/PRODUCTION_EVENT_COMPLEX_INPUT_V0_1.json`

Hosted workflow:
`.github/workflows/idt-05j-production-event-complex-input.yml`

Verdict target:
`PASS_IDT_PRODUCTION_EVENT_COMPLEX_INPUT_CONTRACT_WITH_PRODUCTION_INPUT_OPEN`.
