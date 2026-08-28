# 07U — Winding–Radius Exact Position Decoder

## Scope

This layer compresses the exact 07T Cartesian position-fiber baseline while preserving a constructive map into the ordered 07K position carrier.

Fix one retained active-attractor stratum

\[
\alpha=(a_1,\ldots,a_N)
\]

and let the ORCHORBITAL residence lineage retain the ordered signed winding

\[
\mathcal W=(\Delta W_1,\ldots,\Delta W_N).
\]

The base record retains the final position \(r_N\). For every pre-final checkpoint retain the active-attractor radius

\[
\rho_k=\|r_k-c_{a_k}\|>0,
\qquad 1\le k<N.
\]

## Exact decoder

For each pre-final segment define the angle of the preceding position relative to the active center,

\[
\theta_{k-1}^{(a_k)}
=\operatorname{atan2}\!\left(
(r_{k-1}-c_{a_k})_y,
(r_{k-1}-c_{a_k})_x
\right).
\]

The next position is then

\[
\boxed{
r_k=c_{a_k}+\rho_k
\begin{pmatrix}
\cos\!\left(\theta_{k-1}^{(a_k)}+2\pi\Delta W_k\right)\\
\sin\!\left(\theta_{k-1}^{(a_k)}+2\pi\Delta W_k\right)
\end{pmatrix},
\qquad k<N.
}
\]

The final position \(r_N\) is read from the declared base record. The final winding \(\Delta W_N\) is used as an independent consistency constraint on the last segment.

Hence the retained augmented coordinate admits the constructive lift

\[
\boxed{
L_s^{\rho W}:
(r_0,\alpha,\mathcal W,\rho_1,\ldots,\rho_{N-1},r_N)
\longmapsto
(r_1,\ldots,r_N).
}
\]

The implementation enforces finite two-component positions, unique finite attractor centers, positive radial coordinates, wrapped winding increments in \([-1/2,1/2]\), exact radial checkpoint coverage, and a finite positive final-winding tolerance.

## Scalar-retention budget

For the declared sparse schedule with the final position already retained, the 07T Cartesian baseline requires

\[
N_{\rm Cartesian}=2N-2
\]

new scalar coordinates. The 07U radial packet requires

\[
N_{\rm radial}=N-1
\]

new scalar coordinates while reusing the \(N\) winding scalars already carried by the augmented ORCHORBITAL record. Therefore, for \(N>1\),

\[
\boxed{
\frac{N_{\rm radial}}{N_{\rm Cartesian}}=\frac12.
}
\]

For \(N=1\), the retained final position is already the complete position carrier.

## Composition with 07K

The decoded carrier composes directly with the exact position-lineage inverse,

\[
\boxed{
(\alpha,\mathcal W,\rho_1,\ldots,\rho_{N-1},r_N)
\xrightarrow{\ L_s^{\rho W}\ }
(r_1,\ldots,r_N)
\xrightarrow{\ 07K^{-1}\ }
(u_1,\ldots,u_N).
}
\]

On the declared domain of positive radii and nonsingular active-center geometry, this is an exact conditional reconstruction chain. Cross-stratum separation continues to be supplied by the exactly retained active-attractor sequence from 07S.

## Evidence

Hosted Reference-suite run:

```text
run: 33205507810 (#673)
job: 98965399355
PR: #29
tested head: 56b5de2ff615e1165ba1f5f7fc007a80a8de7112
tested PR merge: 7a6815fdcba53464634b17ef0b86785a89dd29f5
result: 551 passed in 12.09s
Python: 3.12.14
Ubuntu: 24.04.4
main merge: f6ccb49cecbe9da9beb91f29b1c7bbc9e15283f3
```

Reference coverage includes real three-event carrier reconstruction, exact 07K kick recovery, the factor-two scalar budget, the \(N=1\) boundary case, an A→B active-attractor switch, and fail-closed checks for malformed radial/winding/attractor inputs and final-winding inconsistency.

## Status

```text
EXACT_WINDING_RADIUS_POSITION_DECODER_PASS
POSITION_FIBER_COMPRESSION_PASS
POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED
CONDITIONAL_AUGMENTED_WINDING_RADIUS_RECONSTRUCTION_PASS
RADIAL_PACKET_RESIDENCE_BINDING_ACTIVE_NEXT_GATE
GENERAL_GLOBAL_INJECTIVITY_OPEN
```
