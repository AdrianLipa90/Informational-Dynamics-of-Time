# 07T — Exact Per-Stratum Position Decoder Baseline

Status: `EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS / FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS / 07K_NDARRAY_CARRIER_INTERFACE_PASS / POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Purpose

07S reduced the Retrodiction closure problem to construction of a single-valued decoder inside each exact active-sequence stratum

\[
\mathcal Z_s=\{z:\alpha(z)=s\},
\qquad
\alpha(z)=(a_1,\ldots,a_N),
\]

with target equal to the injective 07K ordered position carrier

\[
P_s(z)=(r_1,\ldots,r_N).
\]

07T establishes an exact sufficiency baseline for that decoder using explicitly retained absolute position coordinates. The baseline gives a constructive upper bound on the additional retained information required before compression by winding/ORCHORBITAL coordinates is attempted.

## 2. Typed position coordinates

For every post-event checkpoint \(k\in\{1,\ldots,N\}\), define the scalar carrier labels

\[
\boxed{
r_{kx},\qquad r_{ky}.
}
\]

The complete ordered label set is

\[
\Lambda_P=
\bigl(r_{1x},r_{1y},\ldots,r_{Nx},r_{Ny}\bigr).
\]

07T represents an explicitly retained position-fiber scalar by

```text
PositionFiberCoordinate(checkpoint_index, axis, value)
```

with `axis` restricted to `x` or `y`, checkpoint index restricted to `[1,N]`, and finite scalar value.

## 3. Base/fiber assembly theorem

Let \(Y\) denote the declared retained base record. Some labels in \(\Lambda_P\) may already occur directly in \(Y\) as `rx` or `ry` checkpoint observations. Let \(F_{\rm pos}\) contain explicit absolute position fibers for every remaining label.

Define the coordinate map

\[
C(Y,F_{\rm pos})
=\{\lambda\mapsto r_\lambda:\lambda\in\Lambda_P\}.
\]

When every required label occurs exactly once across the base position coordinates and the fiber packet, define

\[
\boxed{
L_s^{\rm pos}(Y,F_{\rm pos})
=\bigl((r_{1x},r_{1y}),\ldots,(r_{Nx},r_{Ny})\bigr).
}
\]

The construction is single-valued because every output coordinate has one declared source. Therefore

\[
\boxed{
P_s=L_s^{\rm pos}\circ(Y,F_{\rm pos})|_{\mathcal Z_s}.
}
\]

Combined with the 07R composition theorem and the 07S exact stratum key, this supplies an exact per-stratum decoder for any declared retention schedule satisfying complete coordinate coverage.

## 4. Declared sparse-schedule baseline

The 07J sparse schedule contains the final position directly,

\[
(r_{Nx},r_{Ny})\subset Y.
\]

Hence the exact 07T baseline packet is

\[
\boxed{
F_{\rm pos}^{\rm baseline}
=\{r_{kx},r_{ky}:1\le k<N\}.
}
\]

Its additional scalar count is

\[
\boxed{
|F_{\rm pos}^{\rm baseline}|=2N-2.
}
\]

This number is an exact constructive sufficiency upper bound for the declared schedule. It is distinct from the 07L local-rank minimum \(N-3\): 07L measures the number of additional scalar rows needed for full first-order rank, while 07T measures an explicit coordinate packet sufficient to reconstruct the complete global 07K carrier.

## 5. Decoder firewall

The executable decoder emits the carrier only after all of the following checks pass:

1. active-sequence stratum is non-empty;
2. base observation specification and value vector have equal length;
3. all base and fiber position values are finite;
4. position checkpoint indices lie in `[1,N]`;
5. each position axis is `x` or `y`;
6. no absolute position label is duplicated inside the base record;
7. no absolute position label is duplicated inside the fiber packet;
8. no absolute position label is supplied simultaneously by the base record and fiber packet;
9. every label in \(\Lambda_P\) is covered exactly once.

Successful decoding returns

```text
EXACT_PER_STRATUM_POSITION_DECODER
```

and a finite \(N\times2\) ordered position array.

## 6. Real three-event composition

The reference trajectory uses three event kicks and the retained active sequence from the event-aware ORCHORBITAL residence layer. The base record contains

\[
(r_{3x},r_{3y},v_{3x}),
\]

while the explicit baseline packet contains

\[
(r_{1x},r_{1y},r_{2x},r_{2y}).
\]

07T assembles the exact ordered position lineage and passes it directly as a NumPy \((N,2)\) carrier to the 07S/07K composition. The recovered kick vector agrees with the generating three-event kick vector at the declared tolerance.

This integration exposed an interface defect in the earlier 07K implementation: `_positions` tested a generic sequence with `if not values`, which is ambiguous for a multi-element NumPy array. The 07K input contract already accepts `Sequence[Sequence[float]]`; the implementation was hardened to use explicit zero-length testing. The corrected interface accepts the typed \((N,2)\) carrier emitted by 07T.

## 7. Hosted evidence

Initial hosted run:

- workflow run `33204395192` / run number `655`;
- job `98961625586`;
- tested head `8a29c3b4cba1c4ab193e5e19f98918a1d09b4e58`;
- result: `1 failed, 527 passed in 14.36s`;
- failure localized to the 07K NumPy truth-value interface described above.

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

Reference implementation:

- `src/idt/retrodiction_per_stratum_position_decoder.py`;
- hardened carrier interface: `src/idt/retrodiction_position_lineage_exact.py`.

Reference tests:

- `tests/reference/test_retrodiction_per_stratum_position_decoder.py`.

## 8. Compression frontier

07T supplies an exact coordinate-complete decoder baseline. The active next gate is to reduce the additional scalar packet while preserving a single-valued map to the same 07K carrier.

The first analytic candidate uses the already retained ordered winding together with active-attractor radial coordinates. For active center \(c_{a_k}\), previous position \(r_{k-1}\), winding increment \(\Delta W_k\), and post-segment active radius

\[
\rho_k=\|r_k-c_{a_k}\|,
\]

the next position obeys

\[
\boxed{
r_k=c_{a_k}+\rho_k
\begin{pmatrix}
\cos(\theta_{k-1}+2\pi\Delta W_k)\\
\sin(\theta_{k-1}+2\pi\Delta W_k)
\end{pmatrix},
}
\]

where \(\theta_{k-1}=\arg(r_{k-1}-c_{a_k})\). For the declared schedule with final \(r_N\) already retained, this suggests replacing the \(2N-2\) explicit baseline position scalars by \(N-1\) active-radius scalars while reusing the existing \(N\)-component winding fiber.

The next gate is therefore

```text
POSITION_FIBER_COMPRESSION_ACTIVE_NEXT_GATE
```

with `GENERAL_GLOBAL_INJECTIVITY_OPEN` retained as the governing status for the compressed Retrodiction architecture.
