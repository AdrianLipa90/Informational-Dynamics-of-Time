# Formal Dependency Graph

This file is the canonical admission order for the temporal programme.

\[
\boxed{
\mathrm{TIR}
\rightarrow \mathrm{Temporal\ Primitive}
\rightarrow \mathrm{Temporal\ Wave}
\rightarrow \mathrm{NOW}
\rightarrow \mathrm{Bifurcation}
\rightarrow \mathrm{Temporal\ Transport}
\rightarrow \mathrm{Memory}
\rightarrow \mathrm{Retrodiction}
\rightarrow \mathrm{Retrocausal\ Tests}
\rightarrow \mathrm{Einstein\ Closure}
}
\]

## Admission rule

A downstream layer may be explored as a candidate before its parent is admitted, but it remains
`PROVISIONAL_DOWNSTREAM_BRANCH` and cannot define or modify an upstream primitive.

The admitted frontier is therefore not the newest file or newest equation. It is the deepest node
whose declared dependencies have independent formal and evidence receipts.

## Current frontier

| Node | Status | Notes |
|---|---|---|
| TIR entry point | `AVAILABLE` | inherited source layer |
| Temporal Primitive | `ACTIVE` | Shannon + relational phase primitives |
| Temporal Wave | `ACTIVE_CANDIDATE` | ordered phase transport |
| NOW | `STRUCTURAL_PASS` | positive gauge-invariant atomic event support |
| Bifurcation | `ACTIVE_DERIVATION_TARGET` | current frontier |
| Temporal Transport | `GATED` | opens after bifurcation receipt |
| Memory | `PROVISIONAL_DOWNSTREAM_BRANCH` | existing candidate work retained, not yet admitted |
| Retrodiction | `GATED` | depends on admitted memory |
| Retrocausal Tests | `GATED` | depends on admitted retrodiction and audits |
| Einstein Closure | `DEFERRED_FINAL_GATE` | spatial structure enters last |

## Invariant

No equation in a downstream layer may be used to prove an upstream claim. In particular, memory
coordinates, retrodictive operators and spacetime structure are excluded from the proof basis of
NOW and bifurcation.
