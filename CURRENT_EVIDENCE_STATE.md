# CURRENT EVIDENCE STATE

Status: `TRANSPORT_STRUCTURAL_GATE_PASS / MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_ACTIVE_NEXT_GATE / EVENT_AWARE_RESIDENCE_CONDITIONING_PASS / QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS / ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS / FIBER_LIFT_COMPOSITION_THEOREM_PASS / FINITE_DOMAIN_FIBER_LIFT_REFERENCE_PASS / STRATIFIED_GLOBAL_REDUCTION_PASS / CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_REFERENCE_PASS / PER_STRATUM_POSITION_DECODER_ACTIVE_NEXT_GATE / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

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

Hosted run `33202559485`, job `98955383447`, tested head `6abca4ad72c04cdca5d1128e690c17898b8650d7` and returned `510 passed in 14.11s`.

Receipt: `validation/RETRODICTION_FIBER_LIFT_COMPOSITION_V0_1.json`.

### 07S — stratified global reduction

07S uses `ResidenceLineageSignature.active_sequence` as an exact discrete stratum key

\[
\alpha(z)=(a_1,\ldots,a_N).
\]

Unequal active sequences are exactly separated by the retained record. Every collision candidate is therefore assigned to a fixed-sequence stratum \(\mathcal Z_s\). Inside each stratum, the 07K ordered position lineage is the exact constructive carrier, with \(2N\) position scalars for \(2N\) latent kick coordinates and a block-lower-triangular sensitivity with diagonal blocks \(\Delta\tau_nI_2\).

The executable reference verifies:

1. exact stratum-key normalization;
2. exact cross-stratum separation;
3. the \(2N\)-dimensional rank certificate;
4. real two-event constructive composition from retained active sequence and replayed position lineage through 07K to the generating kicks;
5. carrier/decoder separation: a perturbed dynamically admissible position lineage is mapped by 07K to a different latent history;
6. mismatch, elapsed-time and label fail-closed controls.

The first hosted control expected a perturbed admissible carrier to raise. Run `33203185181`, job `98957507517`, correctly returned `1 failed, 517 passed in 11.81s`. The failure identified a test-contract mismatch: the exact 07K inverse maps each admissible carrier to its corresponding latent history, while carrier selection belongs to the decoder \(L_s\). The test was corrected accordingly.

Corrected hosted authority:

- workflow: `Reference suite`;
- run: `33203339457` / run number `637`;
- job: `98958035895`;
- tested branch head: `5e7d36f248963cb9a0b1d8bcb7be9306eadc7051`;
- tested PR merge commit: `3386f3e1a8fb63812095333955640e37040fa645`;
- command: `python -m pytest -q tests/reference`;
- result: `518 passed in 12.06s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion: `success`.

Evidence files:

- `src/idt/retrodiction_stratified_position_lift.py`;
- `tests/reference/test_retrodiction_stratified_position_lift.py`;
- `formalism/07S_stratified_position_lift_reduction.md`;
- `validation/RETRODICTION_STRATIFIED_POSITION_LIFT_V0_1.json`.

The active constructive gate is `PER_STRATUM_POSITION_DECODER_ACTIVE_NEXT_GATE`:

\[
\boxed{
L_s:(Y,F)|_{\mathcal Z_s}\to(r_1,\ldots,r_N).
}
\]

`GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status through this decoder gate.

## Canonical integration state

The promotion branch carries Memory and ORCHORBITAL admission receipts plus provisional Retrodiction evidence through the 07S exact stratified reduction and hosted reference pass. Canonical `main` remains unchanged until explicit merge authorization.
