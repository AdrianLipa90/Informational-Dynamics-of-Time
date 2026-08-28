# 07S — Stratified Global Reduction to Fixed-Sequence Position Lift

Status: `EXACT_STRATIFIED_GLOBAL_REDUCTION_PASS / CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_REFERENCE_PASS / PER_STRATUM_POSITION_DECODER_ACTIVE_NEXT_GATE / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Purpose

07R reduced Retrodiction injectivity to construction of a single-valued lift from retained augmented coordinates to an injective carrier. 07S sharpens that result using an exact discrete coordinate that is already retained by the event-aware ORCHORBITAL residence lineage: the complete active-attractor sequence.

For an admitted \(N\)-event history \(z\), define

\[
\boxed{
\alpha(z)=(a_1(z),\ldots,a_N(z)).
}
\]

The residence signature stores \(\alpha\) exactly as `active_sequence`. Hence histories with different active sequences are already separated by the retained observation.

## 2. Exact stratification

For every realizable active sequence \(s\), define the stratum

\[
\boxed{
\mathcal Z_s=\{z\in\mathcal Z:\alpha(z)=s\}.
}
\]

If

\[
\alpha(z_1)\ne\alpha(z_2),
\]

then the retained active-sequence coordinates differ exactly. Therefore

\[
\boxed{
\alpha(z_1)\ne\alpha(z_2)
\Longrightarrow
A(z_1)\ne A(z_2),
}
\]

where \(A=(Y,F)\) denotes the complete retained augmented record and includes the residence stratum key.

Every global collision candidate is therefore assigned to one fixed-sequence stratum.

## 3. Fixed-sequence injective carrier

Inside a declared stratum \(\mathcal Z_s\), retain the ordered post-segment position carrier

\[
\boxed{
P_s(z)=(r_1(z),\ldots,r_N(z)).
}
\]

For positive elapsed increments \(\Delta\tau_n\), the 07K recursion recovers every event kick algebraically from this carrier:

\[
\boxed{
u_n=
\frac{r_n-r_{n-1}-\frac12A_n(r_{n-1})\Delta\tau_n^2}
{\Delta\tau_n}
-v_{n-1},}
\]

\[
\boxed{
v_n=v_{n-1}+u_n+
\frac12\left[A_n(r_{n-1})+A_n(r_n)\right]\Delta\tau_n.}
\]

The ordered position-lineage map has \(2N\) scalar coordinates for \(2N\) latent kick coordinates. Its local sensitivity is block lower triangular with diagonal blocks

\[
\Delta\tau_n I_2,
\]

so for \(\Delta\tau_n>0\) its diagonal determinant is nonzero. The exact 07K constructive inverse supplies the fixed-sequence carrier used by 07S.

## 4. Stratified composition theorem

For each stratum \(\mathcal Z_s\), suppose there exists a single-valued decoder/lift

\[
\boxed{
L_s:A(\mathcal Z_s)\to P_s(\mathcal Z_s)
}
\]

such that

\[
\boxed{
P_s=L_s\circ A|_{\mathcal Z_s}.
}
\]

Then 07R implies that \(A|_{\mathcal Z_s}\) is injective on \(\mathcal Z_s\).

Since unequal strata are already separated by the exact retained coordinate \(\alpha\), injectivity on every stratum implies injectivity on their union:

\[
\boxed{
\left[
\forall s:\ A|_{\mathcal Z_s}\text{ injective}
\right]
\land
\left[
\alpha\text{ retained exactly}
\right]
\Longrightarrow
A\text{ injective on }\mathcal Z.
}
\]

### Proof

Take any \(z_1,z_2\in\mathcal Z\) with \(A(z_1)=A(z_2)\). Because \(\alpha\) is a retained component of \(A\),

\[
\alpha(z_1)=\alpha(z_2)=s.
\]

Thus \(z_1,z_2\in\mathcal Z_s\). By the assumed per-stratum lift and the 07R composition theorem, \(A|_{\mathcal Z_s}\) is injective, hence

\[
\boxed{z_1=z_2.}
\]

Therefore \(A\) is injective on the admitted union of strata. \(\square\)

## 5. Executable stratified certificate

The reference implementation exposes

```text
certify_stratified_global_reduction(active_sequence, delta_taus)
```

and returns

```text
cross_sequence_separator = RETAINED_ACTIVE_SEQUENCE_EXACT
fixed_sequence_inverse = 07K_EXACT_POSITION_LINEAGE_RECOVERY
remaining_requirement = Y_AUG_TO_ORDERED_POSITION_LINEAGE_LIFT_PER_FIXED_SEQUENCE_STRATUM
status = GLOBAL_INJECTIVITY_REDUCED_TO_FIXED_SEQUENCE_POSITION_LIFT
```

For \(N\) events, the certificate also requires

\[
\boxed{
\dim z=\dim P_s=2N.
}
\]

## 6. Constructive reference composition

The executable composition

```text
retrodict_from_retained_position_lift(...)
```

takes:

1. the retained `ResidenceLineageSignature`, including exact active sequence;
2. declared positive internal elapsed increments;
3. an already decoded ordered position lineage;
4. the existing attractor family and initial Memory state.

It then invokes the exact 07K inverse. On the real two-event reference trajectory it returns

```text
CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_RECOVERY
```

and reconstructs the generating kick pair within the declared numerical tolerance.

## 7. Decoder firewall

07S assigns two distinct roles:

\[
\boxed{
L_s:\text{retained record}\to\text{position carrier},
\qquad
07K^{-1}:\text{position carrier}\to\text{latent history}.
}
\]

When a supplied position lineage is changed while remaining dynamically admissible in the same active-sequence stratum, 07K reconstructs the latent history corresponding to that changed carrier. The exact inverse therefore gives a one-to-one carrier-to-history map on the admitted fixed-sequence domain, while carrier selection is supplied by \(L_s\).

The corrected control verifies

\[
\boxed{
P_s'\ne P_s
\Longrightarrow
07K^{-1}(P_s')\ne07K^{-1}(P_s)
}
\]

for the perturbed reference carrier while both remain valid fixed-stratum reconstructions.

The active constructive object is precisely

\[
\boxed{
L_s:(Y,F)|_{\mathcal Z_s}
\longrightarrow
(r_1,\ldots,r_N).
}
\]

This decoder is derived from retained coordinates such as ordered winding, continuous ORCHORBITAL observables and SOD/spatial coordinates, with its own injectivity and consistency audit.

## 8. Hosted reference evidence

Implementation:

- `src/idt/retrodiction_stratified_position_lift.py`.

Reference tests:

- `tests/reference/test_retrodiction_stratified_position_lift.py`.

The test layer covers:

1. exact active-sequence stratum keys;
2. exact cross-stratum separation for unequal active sequences;
3. the \(2N\)-dimensional stratified reduction certificate;
4. constructive real-trajectory composition with 07K;
5. the decoder firewall: a perturbed admissible position carrier maps to a different latent history under the exact 07K inverse;
6. sequence/elapsed-count mismatch rejection;
7. non-positive elapsed-time rejection;
8. empty attractor-label rejection.

The first hosted version encoded the stronger expectation that a perturbed dynamically admissible carrier should be rejected. Run `33203185181` returned `1 failed, 517 passed` and identified that mismatch with the carrier/decoder contract. The corrected control records the carrier-to-history behavior described above.

Hosted authority after correction:

- workflow: `Reference suite`;
- run: `33203339457` / run number `637`;
- job: `98958035895`;
- tested branch head: `5e7d36f248963cb9a0b1d8bcb7be9306eadc7051`;
- tested PR merge commit: `3386f3e1a8fb63812095333955640e37040fa645`;
- command: `python -m pytest -q tests/reference`;
- result: `518 passed in 12.06s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion: `success`.

## 9. Active frontier

07S resolves cross-active-sequence separation exactly and expresses the remaining closure as one constructive problem repeated over fixed-sequence strata:

```text
PER_STRATUM_POSITION_DECODER_ACTIVE_NEXT_GATE
```

The active target is to construct and audit \(L_s\) from retained base observations and the existing winding/ORCHORBITAL/SOD fiber channels to the ordered 07K position carrier. `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status through this active decoder gate.
