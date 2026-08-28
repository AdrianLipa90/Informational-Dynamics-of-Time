# CURRENT EVIDENCE STATE

Status: `MEMORY_REFERENCE_GATE_ADMISSION_PASS / ORCHORBITAL_REFERENCE_GATE_ADMISSION_PASS / RETRODICTION_07T_BASELINE_PASS / POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE / RELATIVISTIC_FIELD_BRIDGE_PREREQUISITE_HARDENED / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## Canonical hosted checkpoints

Memory admission: run `33193861826`, job `98925901636`, `431 passed in 7.08s`.

ORCHORBITAL synchronized checkpoint: run `33197346515`, job `98937750103`, `476 passed in 11.95s`.

Retrodiction 07P: run `33200684482`, job `98949092398`, `495 passed in 10.14s`.

Retrodiction 07Q: run `33201861565`, job `98953023513`, `502 passed in 8.09s`.

Retrodiction 07R: run `33202559485`, job `98955383447`, `510 passed in 14.11s`.

Retrodiction 07S: run `33203339457`, job `98958035895`, `518 passed in 12.06s`.

## 07T — per-stratum position decoder baseline

07T implements the exact coordinate assembler from retained base position coordinates plus explicit absolute position fibers to the ordered 07K position carrier.

For a declared `N`-event stratum the required scalar labels are

\[
\Lambda_P=(r_{1x},r_{1y},\ldots,r_{Nx},r_{Ny}).
\]

The decoder passes only when every required label is supplied exactly once across base and fiber coordinates, all values are finite, and indices/axes satisfy the typed firewall.

For the sparse schedule carrying `(r_Nx,r_Ny)` in the base observation, the baseline additional packet has exact size

\[
|F_{pos}^{baseline}|=2N-2.
\]

Initial hosted integration run `33204395192`, job `98961625586`, returned `1 failed, 527 passed in 14.36s`. The failure localized the generic 07K sequence parser to an ambiguous NumPy truth-value test.

The carrier interface was hardened from a generic truth test to an explicit zero-length test. Corrected hosted authority:

- run `33204551313` / run number `659`;
- job `98962152065`;
- tested branch head `8d0964f1d6d343193bb72966f4443780d2edafe0`;
- tested PR merge commit `11c9f9f5a912fc351c7e44bc16d3903bfb161a06`;
- command `python -m pytest -q tests/reference`;
- result `528 passed in 14.20s`;
- conclusion `success`.

Receipt: `validation/RETRODICTION_PER_STRATUM_POSITION_DECODER_V0_1.json`.

## Relativistic bridge evidence

IDT 01AG executable source hardening records the variation-level current bridge

\[
J_{EM}^{\mu}=-\frac{1}{\hbar}J_Q^{\mu},
\qquad
J_{EM}^{\mu}=-\frac{q}{\hbar}J_{\theta}^{\mu}
\]

for the single-charge reduction, with the charge-compatibility gate `[M^2,Q]=0` and a neutral-neutrino null control.

RFC RF-M1/RF-E0 is hardened and merged to RFC `main` at `786a872efa0dc75cad7c2b1591a8cb8a1dc45858`. Post-merge RFC workflow run `33203930064` concluded `success`. The pinned cross-repository receipt remains `crossrefs/IDT_RFC_RELATIVISTIC_BRIDGE_UPDATE_2026-08-28_01AG.json`.

## All-branch consolidation authority

IDT consolidation PR #24 combined the Memory/ORCHORBITAL promotion stack, 01AG relativistic bridge, phase-clock 01L/01K work, relational lapse content and the first 07T executable baseline. Final PR run `33204645439` returned `534 passed` and concluded `success`; merge commit on `main` is `ea59854ef6e0c105e8bee91945d25cea0e1efb8f`.

The current 07T forward-port preserves that merged tree and advances the Retrodiction evidence marker to:

```text
EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS
FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS
07K_NDARRAY_CARRIER_INTERFACE_PASS
POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE
GENERAL_GLOBAL_INJECTIVITY_OPEN
```
