# IDT Collatz–Fubini–Study Phase Registry Supplement v0.1

**Status:** `ADDITIVE_REGISTRY_SUPPLEMENT / MATHEMATICAL_PHASE_MAP_PASS / PHYSICAL_TIME_BINDING_OPEN`

This file extends the canonical IDT claim/equation/dependency surfaces without rewriting historical registries.

## Claim supplement

| ID | Statement | Depends on | Evidence class | Status |
|---|---|---|---|---|
| T-CFS-001 | For the full Collatz map `C`, the parity itinerary `b_k(x)=C^k(x) mod 2` determines `q_C(x)=sum_{k>=0} b_k/2^(k+1)` whenever the infinite itinerary is specified. | Collatz map | exact definition | `FORMAL_DEFINITION` |
| T-CFS-002 | `q_C(Cx)=2 q_C(x) mod 1`. | T-CFS-001 | exact algebraic identity | `PROVED_STRUCTURAL_IDENTITY` |
| T-CFS-003 | `zeta_C(x)=exp(2 pi i q_C(x))` obeys `zeta_C(Cx)=zeta_C(x)^2`. | T-CFS-002 | exact algebraic identity | `PROVED_STRUCTURAL_IDENTITY` |
| T-CFS-004 | On the terminal cycle `4->2->1->4`, `q_C(4)=1/7`, `q_C(2)=2/7`, `q_C(1)=4/7`. | T-CFS-001 | exact rational evaluation | `PROVED_STRUCTURAL_IDENTITY` |
| T-CFS-005 | If `x` reaches `1` after `L_x` steps, then `q_C(x)` has denominator dividing `7*2^L_x` after reduction, hence `zeta_C(x)^(7*2^L_x)=1`. | T-CFS-001,T-CFS-004 | conditional exact theorem | `PROVED_CONDITIONAL_IDENTITY` |
| T-CFS-006 | The unit phase `zeta_C` defines an equatorial projective state `( |0> + zeta_C |1> )/sqrt(2)` in `CP1`, with `theta=pi/2`. | T-CFS-003 + CP1 geometry | exact projective embedding | `PROVED_CP1_REFERENCE_IDENTITY` |
| T-CFS-007 | Projective closure is `2pi`; the spinorial lift has `4pi` closure. | T-CFS-006 + SU(2)->SO(3) double cover | standard geometric structure | `PROVED_REFERENCE_STRUCTURE` |
| T-CFS-008 | Identifying this phase coordinate with physical elapsed time, energy, atomic transition rates, or gravitational lapse requires an independent physical binding. | T-CFS-001..007 | claim firewall | `OPEN_PHYSICAL_BINDING` |

## Equation supplement

**EQ-T-CFS-001 — parity itinerary**

\[
b_k(x)=C^k(x)\bmod 2,\qquad b_k\in\{0,1\}.
\]

**EQ-T-CFS-002 — binary phase coordinate**

\[
q_C(x)=\sum_{k=0}^{\infty}\frac{b_k(x)}{2^{k+1}}\pmod 1.
\]

**EQ-T-CFS-003 — doubling conjugacy on the phase coordinate**

\[
\boxed{q_C(Cx)=2q_C(x)\pmod1}.
\]

**EQ-T-CFS-004 — unit-circle lift**

\[
\boxed{\zeta_C(x)=e^{2\pi i q_C(x)}},\qquad
\boxed{\zeta_C(Cx)=\zeta_C(x)^2}.
\]

**EQ-T-CFS-005 — terminal-cycle rational phases**

\[
q_C(4)=\frac17,\qquad q_C(2)=\frac27,\qquad q_C(1)=\frac47.
\]

**EQ-T-CFS-006 — conditional root-of-unity quantization**

If `C^{L_x}(x)=1`, then

\[
q_C(x)=\sum_{k=0}^{L_x-1}\frac{b_k}{2^{k+1}}+\frac{4}{7\,2^{L_x}},
\]

hence

\[
\boxed{\zeta_C(x)^{7\,2^{L_x}}=1}.
\]

**EQ-T-CFS-007 — equatorial CP1 carrier**

\[
\boxed{|\psi_C(x)\rangle=\frac{|0\rangle+\zeta_C(x)|1\rangle}{\sqrt2}},
\qquad \theta=\frac\pi2.
\]

## Dependency insertion

The additive phase branch is

\[
\boxed{\mathrm{TIR}\to\mathrm{Parity\ Itinerary}\to q_C\to\zeta_C\to S^1\subset\mathbb{CP}^1\to\mathrm{Temporal\ Phase\ Interface}}.
\]

It joins the existing IDT temporal spine at the phase/transport layer. It does **not** replace the monotone internal elapsed-activity variable `tau_int`.

The current typed relation is therefore

\[
\boxed{\tau_{\rm IDT}=(\tau_{\rm int},\phi_C)}
\]

as a candidate composite temporal state, where `tau_int` preserves temporal ordering/elapsed activity and `phi_C=arg(zeta_C)` carries projective phase. The physical coupling between these coordinates remains OPEN.

## Validation provenance

Deterministic reference validator:

`validation/collatz_fs_temporal_phase_v0_1.py`

Reference run recorded on 2026-09-04:

- domain: `x=1..10000`;
- all tested trajectories reached `1`;
- doubling identity: `10000/10000 PASS`;
- denominator/root-of-unity condition: `10000/10000 PASS`;
- arithmetic exceptions: `0`.

This finite run is not a proof of the Collatz conjecture. The root-of-unity theorem is conditional on the orbit reaching the terminal `1-4-2` cycle.
