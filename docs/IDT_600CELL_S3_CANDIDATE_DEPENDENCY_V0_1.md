# IDT 600-cell / S^3 Candidate Dependency v0.1

Status: `CANDIDATE / ACTIVE_WORKING_DEPENDENCY / CANONICAL_TIME_DYNAMICS_UNCHANGED`

Date: 2026-09-11

This surface adopts the repository-wide rule that `CANDIDATE` means an active working implementation, not unused or failed code.

The candidate dependency is:

`TIR_600CELL_S3_CANDIDATE_WORKING_LAYER_V0_1`

with an executable PhaseNav counterpart:

`PNCS_600CELL_S3_CANDIDATE_V0_1`.

IDT may use this carrier in explicitly candidate-labelled experiments involving finite state support, event-state sampling, spectral transport and cross-repository carrier comparisons.

The following are NOT changed by this dependency:

- canonical IDT event-clock definitions;
- terminal-state semantics;
- occurrence/terminal-state bindings;
- existing holonomy or foliation claims;
- any canonical spacetime interpretation.

Candidate routing requirements:

```text
status = CANDIDATE
executable = true
explicit_candidate_admission = required
canonical_default = unchanged
candidate_result_may_feed_candidate = true
candidate_result_may_satisfy_canonical_gate = false unless separately promoted
```

The 600-cell layer is currently validated mathematically for the finite S^3 angular sectors ell=0..5. Any use in IDT beyond that domain must remain explicitly experimental and fail closed where a validated map is absent.

This file does not claim that the 600-cell repairs or replaces any historical IDT failure. It makes the new carrier available as a working candidate for the next round of IDT gates.
