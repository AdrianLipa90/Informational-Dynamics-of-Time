# IDT GSC-2 Production Event-Complex Input Contract v0.1

Status: `INPUT_CONTRACT_DEFINED / 05H_HANDOFF_FAIL_CLOSED / MINIMAL_CYCLE_CONTROL_IMPLEMENTED / PRODUCTION_EVENT_COMPLEX_OPEN`

Date: 2026-08-31

## 1. Purpose

IDT 05H already gives the exact graph-cohomology criterion for one global discrete event clock. The remaining GSC-2 dependency is source-owned event incidence with positive elapsed-edge data.

This contract turns that open input into a machine-readable, provenance-bearing dataset while preserving the distinction between:

- malformed/integrity-failing input;
- structurally valid input carrying nonzero temporal holonomy;
- structurally valid exact input;
- production-eligible exact input.

## 2. Dataset

Schema:

`IDT_GLOBAL_EVENT_COMPLEX_INPUT_V0_1`

Required fields:

- non-empty `dataset_id`;
- representation `connected_directed_event_complex_with_elapsed_edges`;
- boolean `production`;
- provenance `source` and `source_commit_or_digest`;
- at least two unique event identifiers;
- at least one realized directed edge;
- unique `edge_id` for every edge;
- declared `source` and `target` event identifiers;
- finite positive `dtheta` on every realized edge;
- canonical `incidence_sha256` over event ids and oriented elapsed-edge records.

Every declared event must occur in at least one realized edge for this production-global contract.

## 3. Two-stage verdict

The input gate first checks structural integrity and canonical digest. A structurally valid dataset is then passed to the existing 05H certifier.

Therefore the two principal states are independent:

```text
input_valid / integrity_valid
clock_exactness
```

A temporal-holonomy defect on otherwise valid data is retained as an exactness failure rather than being reclassified as malformed input.

Promotion eligibility is

```text
production = true
AND input_valid
AND integrity_valid
AND exact_clock_certified
```

Reference controls use `production=false`.

## 4. Minimal nontrivial exactness witness

A tree has a unique path between vertices, so 05H exactness is automatic there. The smallest simple connected graph with a nontrivial cycle has three vertices and three edges.

Choose the acyclic orientation

```text
a -> b -> c
 \------> c
```

with positive elapsed weights. Exactness requires

\[
\boxed{\theta_{ab}+\theta_{bc}=\theta_{ac}.}
\]

The positive reference uses

\[
\theta_{ab}=1,\qquad
\theta_{bc}=2,\qquad
\theta_{ac}=3,
\]

and reconstructs

\[
t_a=0,\qquad t_b=1,\qquad t_c=3.
\]

The negative control preserves the same incidence and changes only

\[
\theta_{ac}=4,
\]

which produces a temporal-holonomy defect.

This triangle is minimal for testing the graph exactness theorem itself. The diamond already documented in 05H remains the minimal symmetric two-branch merger pattern with two length-two histories.

## 5. Production boundary

The minimal triangle is a validator control. GSC-2 promotion requires the actual source-owned global IDT event incidence and elapsed-edge dataset.

A reference fixture, synthetic event graph or software-runtime event DAG carries validation/provenance value only. Production promotion is reserved for the event carrier admitted by the physical IDT formalism and its source provenance.

## 6. Handoff

```text
00E positive elapsed primitive
 -> production event incidence + elapsed-edge input contract
 -> 05H exactness certifier
 -> one discrete scalar t_v up to an additive constant
 -> 05I general smooth-extension route
    OR RFC GSC3 product-clock lift when product realization is independently admitted
 -> 05G temporal foliation
```

## 7. Falsification rules

The input contract fails on malformed identifiers, duplicate edge ids, undeclared event references, isolated declared production events, non-positive/non-finite elapsed weights, missing provenance or digest mismatch.

A valid input receives `exact_clock_certified=false` when 05H detects temporal holonomy, disconnectedness under the global connected-domain claim, or another 05H exactness failure.

## 8. Validation authority

Implementation:

`src/idt/global_event_complex_input.py`

Reference tests:

`tests/reference/test_global_event_complex_input.py`

Target verdict:

`PASS_IDT_GSC2_EVENT_COMPLEX_INPUT_CONTRACT_WITH_PRODUCTION_INPUT_OPEN`.
