# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE / EVENT_AWARE_RESIDENCE_CONDITIONING_PASS / QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS / ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS / FIBER_LIFT_COMPOSITION_THEOREM_PASS / FINITE_DOMAIN_FIBER_LIFT_REFERENCE_PASS / STRATIFIED_GLOBAL_REDUCTION_PASS / CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_REFERENCE_PASS / EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS / FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS / 07K_NDARRAY_CARRIER_INTERFACE_PASS / POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## Upstream admitted evidence

Memory hosted admission: run `33193861826`, job `98925901636`, `431 passed in 7.08s`; receipt `validation/MEMORY_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json`.

ORCHORBITAL hosted admission is bound by `validation/ORCHORBITAL_ADMISSION_HOSTED_FULL_SUITE_2026_08_28.json` and contains residence-ledger, strict-schema, PNCS hierarchy and typed-observable evidence. The synchronized ORCHORBITAL checkpoint run `33197346515`, job `98937750103`, returned `476 passed in 11.95s`.

## Retrodiction evidence frontier

### 07O — event-aware residence conditioning

The declared reflection pair retains equivalent final sparse base observation and equivalent active/switch/leak residence class, while its latent histories remain separated by more than `0.9`. The earlier continuous `weight:A@1` coordinate separates the pair by `0.01918916841099516`.

Hosted hardening: run `33198069462`, job `98940226102`, `486 passed in 8.89s`.

### 07P — quotient/fiber finite-domain injectivity

For every distinct-latent pair colliding under the base projection, the finite-domain gate requires at least one declared fiber channel to separate the pair. Hosted run `33200684482`, job `98949092398`, returned `495 passed in 10.14s`.

Receipt: `validation/RETRODICTION_QUOTIENT_FIBER_FINITE_INJECTIVITY_V0_1.json`.

### 07Q — oriented winding fiber

The persisted ordered signed winding

\[
\mathcal W(z)=\bigl(\Delta W_1(z),\ldots,\Delta W_N(z)\bigr)
\]

separates the exact reflection null at fiber tolerance `1e-12`; direct 07P integration gives one base collision, one separated collision and zero unresolved collisions with channel `oriented_winding`.

Hosted run `33201861565`, job `98953023513`, returned `502 passed in 8.09s`.

Receipt: `validation/RETRODICTION_ORIENTED_WINDING_FIBER_V0_1.json`.

### 07R — fiber-lift composition theorem

For injective carrier \(P\), augmented record \(A=(Y,F)\), and a single-valued lift satisfying \(P=L\circ A\), 07R proves exactly that \(A\) is injective. The finite executable audit checks carrier injectivity and lift functionality separately.

Hosted run `33202559485`, job `98955383447`, returned `510 passed in 14.11s`.

Receipt: `validation/RETRODICTION_FIBER_LIFT_COMPOSITION_V0_1.json`.

### 07S — stratified global reduction

07S uses `ResidenceLineageSignature.active_sequence` as an exact discrete stratum key

\[
\alpha(z)=(a_1,\ldots,a_N).
\]

Unequal active sequences are exactly separated by the retained record. Every collision candidate is therefore assigned to a fixed-sequence stratum \(\mathcal Z_s\). Inside each stratum, the 07K ordered position lineage is the exact constructive carrier.

The first hosted control run `33203185181`, job `98957507517`, returned `1 failed, 517 passed in 11.81s` and identified an over-strong carrier-rejection expectation. After correcting the carrier/decoder contract, run `33203339457`, job `98958035895`, returned `518 passed in 12.06s`.

Receipt: `validation/RETRODICTION_STRATIFIED_POSITION_LIFT_V0_1.json`.

### 07T — exact per-stratum position decoder baseline

07T represents every absolute position coordinate by a typed label

\[
\Lambda_P=(r_{1x},r_{1y},\ldots,r_{Nx},r_{Ny})
\]

and constructs a deterministic assembler from position coordinates already present in the base record plus explicitly retained absolute position fibers.

The decoder requires each label in \(\Lambda_P\) exactly once and returns

```text
EXACT_PER_STRATUM_POSITION_DECODER
```

with the complete finite \(N\times2\) 07K carrier.

For the declared sparse schedule the base record contains \((r_{Nx},r_{Ny})\), hence the exact baseline packet contains the earlier coordinates

\[
F_{\rm pos}^{\rm baseline}=\{r_{kx},r_{ky}:1\le k<N\},
\]

with

\[
\boxed{|F_{\rm pos}^{\rm baseline}|=2N-2.}
\]

The three-event reference composes the decoded carrier through the 07S/07K inverse and recovers the generating kick history within tolerance.

Initial hosted run `33204395192`, job `98961625586`, returned `1 failed, 527 passed in 14.36s`. The failure exposed the 07K generic-sequence parser using a boolean test on a multi-element NumPy carrier. The parser was hardened with explicit zero-length testing.

Corrected hosted authority:

- workflow: `Reference suite`;
- run: `33204551313` / run number `659`;
- job: `98962152065`;
- tested branch head: `8d0964f1d6d343193bb72966f4443780d2edafe0`;
- tested PR merge commit: `11c9f9f5a912fc351c7e44bc16d3903bfb161a06`;
- command: `python -m pytest -q tests/reference`;
- result: `528 passed in 14.20s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion: `success`.

Evidence files:

- `src/idt/retrodiction_per_stratum_position_decoder.py`;
- `src/idt/retrodiction_position_lineage_exact.py`;
- `tests/reference/test_retrodiction_per_stratum_position_decoder.py`;
- `formalism/07T_per_stratum_position_decoder_baseline.md`;
- `validation/RETRODICTION_PER_STRATUM_POSITION_DECODER_V0_1.json`.

The active constructive gate is now `POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE`. The first analytic candidate reuses the already retained ordered winding and supplies active-attractor post-segment radial scalars to reconstruct earlier position vectors recursively.

`GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status for the compressed Retrodiction architecture.

## Canonical integration state

Canonical `main` contains Memory, ORCHORBITAL and the Retrodiction stack through 07S. 07T is carried by draft PR #23 and remains separate from `main` pending explicit merge authorization.
