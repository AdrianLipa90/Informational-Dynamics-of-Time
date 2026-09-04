# CURRENT THEORY STATE — PHASE SUPPLEMENT v0.1

Date: 2026-09-04

Status:

`COLLATZ_FS_PHASE_MAP_STRUCTURAL_PASS / CP1_EQUATORIAL_EMBEDDING_PASS / CONDITIONAL_ROOT_OF_UNITY_QUANTIZATION_PASS / COMPOSITE_TEMPORAL_STATE_CANDIDATE / PHYSICAL_TIME_COUPLING_OPEN / EINSTEIN_BINDING_OPEN`

## Additive temporal coordinate

The existing monotone internal elapsed-activity coordinate remains authoritative for ordering:

\[
d\tau_{\rm int}=\frac{\mathfrak a}{\mathfrak a_\star}\,d\lambda.
\]

The newly admitted mathematical phase branch defines

\[
b_k(x)=C^k(x)\bmod2,
\qquad
q_C(x)=\sum_{k\ge0}\frac{b_k(x)}{2^{k+1}},
\]

with

\[
\boxed{q_C(Cx)=2q_C(x)\pmod1},
\]

and

\[
\boxed{\zeta_C(x)=e^{2\pi i q_C(x)}},
\qquad
\boxed{\zeta_C(Cx)=\zeta_C(x)^2}.
\]

The phase is embedded into the equatorial projective carrier

\[
|\psi_C(x)\rangle
=\frac{|0\rangle+\zeta_C(x)|1\rangle}{\sqrt2}
\in\mathbb{CP}^1,
\]

so the additive candidate temporal state is

\[
\boxed{\tau_{\rm IDT}=(\tau_{\rm int},\phi_C)},
\qquad
\phi_C=\arg\zeta_C.
\]

This is a typed product/interface statement only. No metric coefficient, energy scale, physical clock rate, lapse, or stress-energy source is inferred from `phi_C` at this stage.

## Terminal-cycle theorem

For the standard terminal cycle

\[
4\to2\to1\to4,
\]

\[
q_C(4)=\frac17,\qquad
q_C(2)=\frac27,\qquad
q_C(1)=\frac47.
\]

If `C^{L_x}(x)=1`, then

\[
q_C(x)=\sum_{k=0}^{L_x-1}\frac{b_k}{2^{k+1}}+\frac{4}{7\,2^{L_x}},
\]

and therefore

\[
\boxed{\zeta_C(x)^{7\,2^{L_x}}=1}.
\]

This theorem is conditional on the orbit reaching the terminal cycle and is not a proof of the Collatz conjecture.

## 2pi / 4pi hierarchy

The projective phase closes modulo `2pi`. The spinorial lift retains the standard double-cover structure with `4pi` closure. IDT records these as distinct state layers; it does not identify them by convention.

## Dependency insertion

The new branch is

\[
\mathrm{TIR}
\to\mathrm{Parity\ Itinerary}
\to q_C
\to\zeta_C
\to S^1\subset\mathbb{CP}^1
\to\mathrm{Temporal\ Phase\ Interface}.
\]

It joins the existing temporal spine upstream of physical Einstein closure and downstream of the relational/projective primitives. It does not replace NOW, positive activity, temporal transport, or memory.

## Evidence

Validator:

`validation/collatz_fs_temporal_phase_v0_1.py`

Reference finite run, `x=1..10000`:

- all tested trajectories reached `1`;
- doubling identity: `10000/10000 PASS`;
- conditional denominator/root-of-unity condition: `10000/10000 PASS`;
- arithmetic exceptions: `0`.

## Open gates

1. derive or falsify a non-arbitrary coupling between `tau_int` and `phi_C`;
2. test whether the phase branch contributes to the existing temporal-wave/transport operator rather than remaining a passive coordinate;
3. derive the relation, if any, between `phi_C` and the existing phase-clock `omega_t`;
4. preserve reparameterization invariance of `tau_int` under any coupling;
5. propagate only derived quantities to RFC/Einstein;
6. test atomic/spectroscopic consequences downstream rather than using them as premises.

## Provenance

Primary formal document:

`docs/IDT_COLLATZ_FS_TEMPORAL_PHASE_V0_1.md`

Registry supplement:

`docs/IDT_COLLATZ_FS_PHASE_REGISTRY_SUPPLEMENT_V0_1.md`
