# Informational Dynamics of Time

This repository develops temporal dynamics before spacetime closure. The project is maintained as three linked but distinct spines:

- `FORMALISM` — equations, typed contracts and dependency graph;
- `EVIDENCE` — tests, receipts, manifests and audits;
- `MONOGRAPH` — LaTeX view assembled from recorded formalism and evidence.

Canonical dependency graph:

\[
\boxed{\mathrm{TIR}\to\mathrm{Temporal\ Primitive}\to\mathrm{Temporal\ Wave}\to\mathrm{NOW}\to\mathrm{Bifurcation}\to\mathrm{Temporal\ Transport}\to\mathrm{Memory}\to\mathrm{ORCHORBITAL\ Attractors}\to\mathrm{Retrodiction}\to\mathrm{Retrocausal\ Tests}\to\mathrm{Einstein\ Closure}}
\]

The admitted frontier currently remains at `Memory`. Tested ORCHORBITAL and Retrodiction implementations may exist on `main` while remaining explicitly provisional downstream/reference extensions; merge status and theory-admission status are separate.

The current reference stack includes Shannon/phase transition primitives, positive temporal activity and NOW support, bifurcation and ordered temporal transport, internal elapsed activity, Kepler--Newton memory dynamics, CP1 Kähler memory geometry, append-only memory receipts and ledger-assisted recall.

## Collatz--Fubini--Study temporal phase interface

An additive temporal-phase branch now records the exact parity-itinerary map

\[
b_k(x)=C^k(x)\bmod2,
\qquad
q_C(x)=\sum_{k\ge0}\frac{b_k(x)}{2^{k+1}},
\]

with the exact shift identity

\[
\boxed{q_C(Cx)=2q_C(x)\pmod1}
\]

and the unit-circle phase carrier

\[
\boxed{\zeta_C(x)=e^{2\pi i q_C(x)}},
\qquad
\boxed{\zeta_C(Cx)=\zeta_C(x)^2}.
\]

For the terminal `4 -> 2 -> 1 -> 4` cycle,

\[
q_C(4)=\frac17,
\qquad
q_C(2)=\frac27,
\qquad
q_C(1)=\frac47.
\]

If an orbit reaches `1` after `L_x` steps, the resulting phase is conditionally root-of-unity quantized,

\[
\boxed{\zeta_C(x)^{7\,2^{L_x}}=1}.
\]

The phase is embedded on the equator of `CP1` as

\[
|\psi_C(x)\rangle
=\frac{|0\rangle+\zeta_C(x)|1\rangle}{\sqrt2},
\qquad \theta=\frac\pi2.
\]

This branch is additive to, not a replacement for, the monotone internal elapsed-activity coordinate. The candidate composite temporal state is therefore tracked as

\[
\boxed{\tau_{\rm IDT}=(\tau_{\rm int},\phi_C)},
\qquad \phi_C=\arg\zeta_C,
\]

with the physical coupling between elapsed activity and projective phase still OPEN.

Canonical supplement:

`docs/IDT_COLLATZ_FS_PHASE_REGISTRY_SUPPLEMENT_V0_1.md`

Formal interface:

`docs/IDT_COLLATZ_FS_TEMPORAL_PHASE_V0_1.md`

Deterministic validator:

`validation/collatz_fs_temporal_phase_v0_1.py`

Reference run on 2026-09-04 over `x=1..10000` recorded zero arithmetic exceptions, `10000/10000` passes for the doubling identity, and `10000/10000` passes for the conditional denominator/root-of-unity condition. This finite test is not a proof of the Collatz conjecture.

The ORCHORBITAL temporal-memory extension adds:

- attractor-relative Kepler energy and positive binding margins;
- normalized attractor weights and deterministic active-basin selection;
- explicit `LEAK_MODE` when no attractor is bound;
- Shannon attractor entropy and normalized basin coherence;
- active-centre Kepler propagation in internal elapsed activity;
- winding increments, phase-space closure defect and segment-boundary attractor-switch detection;
- multi-segment attractor residence time, accumulated winding and directed attractor-transition counts.

Targeted ORCHORBITAL reference evidence is `11 passed in 0.07s`; receipt: `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`.

The provisional Retrodiction layer contains single-withheld-receipt inversion, multi-event observability, checkpoint selection, damped Gauss--Newton estimation, information-firewall commitment, covariance/Fisher uncertainty geometry and covariance-preserving checkpoint-permutation null ensembles.

Hosted full-suite status remains `CI_RESULT_NOT_OBTAINED` because the observed workflow jobs terminate before executing test steps. Targeted reference evidence and hosted full-suite evidence are recorded separately.

Reference figures are generated from code. Raster outputs and compiled PDFs are local QA artifacts and are not committed; repository monograph source is LaTeX.

## Temporal information curvature export

Gate `01K` adds a downstream Einstein-interface scalar while keeping the admitted frontier unchanged. From the 01C relative-information scalar in bits,

\[
\mathcal J_\pi=(\ln2)\mathcal I_\pi,
\]

and an admitted positive relational area

\[
[\mathcal A_{\rm rel}]=L^2,
\]

IDT exports

\[
\boxed{\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}}},
\qquad
\boxed{[\Xi_I]=L^{-2}}.
\]

Its exact temporal differential is

\[
d\Xi_I
=\mathcal A_{\rm rel}^{-1}d\mathcal J_\pi
-\mathcal J_\pi\mathcal A_{\rm rel}^{-2}d\mathcal A_{\rm rel}.
\]

The physical relational-area calibration is supplied by the TIR geometry interface; RFC owns the later `Xi_I -> Lambda0` field binding. Targeted 01K evidence: `6 passed`; receipt: `validation/01K_TEMPORAL_INFORMATION_CURVATURE_V0_1.json`.
