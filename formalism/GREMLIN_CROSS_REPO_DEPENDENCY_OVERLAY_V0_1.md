# IDT — GREMLIN Cross-Repository Dependency Overlay v0.1

Status: `CANDIDATE_ONLY / CHYBA / NON_CANONICAL_OVERLAY`

This overlay augments the canonical IDT dependency graph with cross-repository candidates discovered by the PNCS GREMLIN relational-isomorphism bank. It does not replace `validation/dependency_graph.json` and does not promote a candidate into the IDT canon.

GREMLIN authority boundary:

```text
runtime_execution_authority = false
canon_write_authority = false
promotion_state = CANDIDATE_ONLY
epistemic = CHYBA
```

Source discovery surfaces:
- PNCS GREMLIN cross-formalism bank ROUND27 / v0.2;
- PNCS GREMLIN ROUND28 exact-cross-formalism candidate stack.

## Overlay graph

```text
TIR FIRST DISTINCTION
  -> HALF
  -> C^2 / CP^1
  -> TIR HALF FIBER / RELATIVE PHASE
  -> IDT TEMPORAL PRIMITIVE
  -> IDT HALF-FRAME TEMPORAL GLUING
  -> IDT TEMPORAL SEAM CURVATURE F_Theta
  -> IDT INTRINSIC TEMPORAL OFFSET
  -> MATERIAL TEMPORAL OFFSET BINDING                    [NEXT IDT GATE]

SOH SU(2) DOUBLE COVER
  -> GREMLIN XFI.03 SPINOR CENTRAL SIGN                  [EXACT_STRUCTURAL CANDIDATE]
  -> IDT HALF-SEAM DOUBLE-COVER SIGNATURE
  -> 2pi -> -1 ; 4pi -> +1                              [PROMOTION REQUIRES SOURCE-SIDE GATE]

SOH HALF-INTERFACE RELATIONAL ZERO / ORDER DOUBLING
  -> GREMLIN XFI.28.02                                   [EXACT CANDIDATE]
  -> TIR/IDT HALF-SEAM RELATIONAL ZERO                   [CANDIDATE CROSSLINK]

SOH CENTERED BLOCH RAPIDITY
  <-> GREMLIN XFI.28.03                                  [EXACT_COORDINATE_ISOMORPHISM CANDIDATE]
  <-> IDT NOW HYPERBOLIC CHART                          [CANDIDATE CROSSLINK]

IDT MOBILITY / ORIENTATION SPLIT
  <-> GREMLIN XFI.08                                     [STRONG_STRUCTURAL CANDIDATE]
  <-> TIR HOLONOMY MAGNITUDE / PHASE SPLIT

IDT TEMPORAL CURVATURE / CLOCK-LAPSE INTERFACE
  -> RFC PREMETRIC TEMPORAL-WAVE BRIDGE
  -> RFC METRIC-TIME CALIBRATION
  -> ADM / EINSTEIN CLOSURE                              [DOWNSTREAM OPEN GATE]
```

## Candidate promotion gates

| Candidate | Required IDT-side gate |
|---|---|
| XFI.03 | deterministic double-cover/sign validator with explicit representation binding |
| XFI.28.02 | exact kernel/order-doubling map with typed zero definition on both sides |
| XFI.28.03 | chart-domain, inverse-map and singular-boundary audit |
| XFI.08 | edge-reversal invariant test preserving mobility magnitude and reversing orientation coordinate |
| IDT -> RFC metric-time edge | material temporal-offset binding plus calibrated clock/lapse source pin |

## Dependency rule

A GREMLIN edge may become a canonical dependency only after:

```text
candidate
 -> explicit source pins
 -> typed realization map
 -> falsification gate
 -> deterministic validator
 -> receipt
 -> source-repository promotion
```

Compilation through `RelationalIsomorphism -> KAKU -> RADICAL -> OPERATORS -> READ_ONLY PNV` preserves the source evidence status and is not itself a canon-promotion event.