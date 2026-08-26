# CURRENT EVIDENCE STATE

Status: `CAUSAL_BIFURCATION_V0_1_PASS_STRUCTURAL_REFERENCE_SUBCLASS`

Current full reference suite: `71 passed in 0.16s`.

NOW controls:

- Fubini–Study event component is invariant under local phase changes: PASS;
- positive event signature is non-negative and zero signatures are omitted from support: PASS;
- positive atomic pushforward support equals the image support even for non-injective maps: PASS.

Bifurcation controls:

- zero current gives zero directed phase increment and identity reference operator: PASS;
- current reversal gives phase reversal and inverse unitary operator: PASS;
- activity/current reconstruction agrees with the forward/reverse affinity: PASS;
- canonical `kappa = ln(2)/(24*pi)` gives `beta = atanh(j/a)/(12*pi)`: PASS;
- fixed-generator reference operator is unitary: PASS;
- fixed-generator event operators compose by phase addition: PASS;
- invalid `|j/a| >= 1` fails closed: PASS.

Architecture controls:

- dependency graph is acyclic: PASS;
- canonical dependency order is enforced in the reference test: PASS;
- memory remains `PROVISIONAL_DOWNSTREAM_BRANCH` while Temporal Transport is gated: PASS.

Validation receipt: `validation/CAUSAL_BIFURCATION_V0_1.json`.
Payload SHA-256: `7d997804b435acb68dd2773788d1da9d10d013c9ab4c3f492bfe0a0a3819f673`.

The reference evidence establishes structural properties of the declared reversible phase-only bifurcation subclass. Selection of a unique physical generator, branch-mixing dynamics, non-unitary classes, memory interpretation, subjective elapsed time and metric-time calibration remain downstream/open evidence targets.
