# CURRENT EVIDENCE STATE

Status: `MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_07T_BASELINE_PASS / RETRODICTION_07U_WINDING_RADIUS_PASS / POSITION_FIBER_COMPRESSION_PASS / RADIAL_PACKET_RESIDENCE_BINDING_ACTIVE_NEXT_GATE / RELATIVISTIC_FIELD_BRIDGE_PREREQUISITE_HARDENED / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## Canonical hosted checkpoints

Memory admission: run `33193861826`, job `98925901636`, `431 passed in 7.08s`.

ORCHORBITAL synchronized checkpoint: run `33197346515`, job `98937750103`, `476 passed in 11.95s`.

Retrodiction 07P: run `33200684482`, job `98949092398`, `495 passed in 10.14s`.

Retrodiction 07Q: run `33201861565`, job `98953023513`, `502 passed in 8.09s`.

Retrodiction 07R: run `33202559485`, job `98955383447`, `510 passed in 14.11s`.

Retrodiction 07S: run `33203339457`, job `98958035895`, `518 passed in 12.06s`.

## 07T — per-stratum position decoder baseline

07T implements the exact coordinate assembler from retained base position coordinates plus explicit absolute position fibers to the ordered 07K position carrier.

For the sparse schedule carrying `(r_Nx,r_Ny)` in the base observation, the baseline additional packet has exact size

\[
|F_{pos}^{baseline}|=2N-2.
\]

The first hosted integration run `33204395192`, job `98961625586`, returned `1 failed, 527 passed in 14.36s` and localized the generic 07K sequence parser to an ambiguous NumPy truth-value test. The carrier interface was hardened to explicit zero-length testing.

Corrected hosted authority:

- run `33204551313` / run number `659`;
- job `98962152065`;
- tested branch head `8d0964f1d6d343193bb72966f4443780d2edafe0`;
- result `528 passed in 14.20s`;
- conclusion `success`.

Receipt: `validation/RETRODICTION_PER_STRATUM_POSITION_DECODER_V0_1.json`.

## 07U — winding-radius position decoder

07U compresses the explicit Cartesian pre-final packet by reusing the already retained ordered signed winding and adding one active-attractor radius for each pre-final checkpoint,

\[
\rho_k=\|r_k-c_{a_k}\|>0.
\]

Given the previous position, exact active center and signed winding increment, the decoder reconstructs each pre-final position from the retained radius. The final position is supplied by the declared base record and the final winding is used as a segment consistency gate.

For `N>1`,

\[
N_{\rm Cartesian}=2N-2,
\qquad
N_{\rm radial}=N-1,
\qquad
\boxed{N_{\rm radial}/N_{\rm Cartesian}=1/2}.
\]

Hosted authority:

- workflow: `Reference suite`;
- run `33205507810` / run number `673`;
- job `98965399355`;
- tested head `56b5de2ff615e1165ba1f5f7fc007a80a8de7112`;
- tested PR merge `7a6815fdcba53464634b17ef0b86785a89dd29f5`;
- result `551 passed in 12.09s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion `success`;
- merged to main as `f6ccb49cecbe9da9beb91f29b1c7bbc9e15283f3`.

Reference coverage includes real three-event position reconstruction, exact 07K kick recovery, factor-two new-scalar budget, the `N=1` boundary, A->B active-center switching and fail-closed malformed-input/consistency gates.

Receipt: `validation/RETRODICTION_WINDING_RADIUS_POSITION_DECODER_V0_1.json`.

Current Retrodiction evidence markers:

```text
EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS
FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS
07K_NDARRAY_CARRIER_INTERFACE_PASS
POSITION_FIBER_COMPRESSION_PASS
EXACT_WINDING_RADIUS_POSITION_DECODER_PASS
POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED
CONDITIONAL_AUGMENTED_WINDING_RADIUS_RECONSTRUCTION_PASS
RADIAL_PACKET_RESIDENCE_BINDING_ACTIVE_NEXT_GATE
GENERAL_GLOBAL_INJECTIVITY_OPEN
```

## Relativistic bridge evidence

IDT 01AG executable source hardening records the variation-level current bridge

\[
J_{EM}^{\mu}=-\frac{1}{\hbar}J_Q^{\mu},
\qquad
J_{EM}^{\mu}=-\frac{q}{\hbar}J_{\theta}^{\mu}
\]

for the single-charge reduction, with charge-compatibility gate `[M^2,Q]=0` and a neutral-neutrino null control.

RFC RF-M1/RF-E0 is hardened and merged to RFC `main` at `786a872efa0dc75cad7c2b1591a8cb8a1dc45858`. Post-merge RFC workflow run `33203930064` concluded `success`. The pinned cross-repository receipt remains `crossrefs/IDT_RFC_RELATIVISTIC_BRIDGE_UPDATE_2026-08-28_01AG.json`.

## All-branch consolidation authority

IDT consolidation PR #24 combined the Memory/ORCHORBITAL promotion stack, 01AG relativistic bridge, phase-clock 01L/01K work, relational lapse content and the 07T baseline. Its final run `33204645439` returned `534 passed` and concluded `success`; merge commit is `ea59854ef6e0c105e8bee91945d25cea0e1efb8f`.

The final 07T consolidation also passed `534/534`, and 07U subsequently passed `551/551` before merge.
