# 00G — Occurrence / Terminal-State Input Contract

Status: `INPUT_CONTRACT_DEFINED / 00F_REALIZATION_EXPORT / 05J_OCCURRENCE_SET_BOUND / PRODUCTION_STATE_TABLE_OPEN`

## Purpose

00F defines each realized occurrence by its full prefix and terminal relational-state label,

\[
\nu_k=(P_k,x_k),\qquad x_k=t(P_k).
\]

Distinct occurrences may carry the same terminal-state label when relational state recurs. 05J independently supplies opaque occurrence identifiers and the occurrence-to-event quotient. 00G makes the 00F occurrence-to-terminal-state relation machine-readable and binds it to one exact 05J event-complex incidence witness.

## Dataset

Schema: `IDT_OCCURRENCE_TERMINAL_STATE_INPUT_V0_1`.

A dataset contains:

- non-empty `dataset_id`;
- explicit boolean `production`;
- source provenance `source` and `source_commit_or_digest`;
- the exact `event_complex_incidence_sha256` of the 05J dataset whose occurrence set is being enriched;
- rows `(occurrence_id, prefix_id_or_digest, terminal_state_id)`;
- canonical `table_sha256`.

The occurrence identifier and prefix identity are unique. `terminal_state_id` is intentionally allowed to recur across distinct prefix occurrences, preserving the 00F state-recurrence theorem.

## Exact occurrence-set binding

Let `O_05J` be the occurrence set of the supplied 05J dataset and `O_00G` the occurrence identifiers in the 00G table. Admission requires

\[
\boxed{O_{00G}=O_{05J}}.
\]

The event-complex incidence digest must also agree exactly with the 05J source receipt. This prevents a terminal-state table from being reused against a different occurrence/event complex.

## Cross-repo handoff

00G exports the source-owned map

\[
\boxed{x:O\to S,\qquad o\mapsto \texttt{terminal_state_id}(o).}
\]

A separate FPDG cross-repository contract owns the physical binding

\[
S\to V(\Sigma)
\]

to a TIR GSC-1 spatial vertex set. RFC GSC3B may then compose the two maps and test quotient-fibre constancy before descending to event placement.

## Promotion firewall

Reference controls use `production=false`. A validated production table becomes eligible for cross-repository review; `canon_allowed` remains false at this contract layer. Canonical promotion requires the downstream cross-repository binding and its independent provenance.

## Falsification rules

The certifier fails closed on malformed provenance, event-complex digest drift, incomplete or extra occurrence coverage, duplicate occurrence IDs, duplicate prefix identities, or table digest mismatch.

State-label recurrence across distinct prefix occurrences is a valid 00F realization and is retained explicitly.

## Validation authority

Implementation: `src/idt/occurrence_terminal_state_input.py`

Reference tests: `tests/reference/test_occurrence_terminal_state_input.py`

Dedicated workflow: `.github/workflows/idt-00g-occurrence-terminal-state-input.yml`

Verdict target: `PASS_IDT_00G_OCCURRENCE_TERMINAL_STATE_INPUT_WITH_PRODUCTION_TABLE_OPEN`.
