# 07M — Spatial Offset Divergence and Sparse Global Injectivity

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / SPARSE_GLOBAL_INJECTIVITY_FAIL_SOD_WITNESS_FOUND / KNOWN_SOD_SEPARATOR_PASS`

## 1. Sparse observation map

Let the retained 07L sparse checkpoint schedule define

\[
\mathcal F_S:z\mapsto Y_S,
\qquad
z=(u_1,\ldots,u_N)\in\mathbb R^{2N}.
\]

07L establishes local full-rank completion for the declared fixed-regime reference class. The present gate tests whether the resulting sparse observation map has a unique global preimage.

At this stage, *spatial* labels the two-component Memory/ORCHORBITAL position coordinate carried by the lineage.

## 2. Spatial Offset Divergence

For two latent histories \(z\) and \(z'\), let

\[
r_n(z),\; r_n(z')\in\mathbb R^2
\]

be their post-segment position checkpoints. Define the checkpointwise Spatial Offset Divergence vector

\[
\boxed{
\Delta_n^{\rm SOD}(z,z')=r_n(z')-r_n(z)
}
\]

and the lineage norm

\[
\boxed{
D_{\rm SOD}(z,z')
=
\left[
\sum_{n=1}^{N}
\|\Delta_n^{\rm SOD}(z,z')\|^2
\right]^{1/2}.
}
\]

The maximum checkpoint offset is

\[
D_{\rm SOD}^{\max}
=
\max_n\|\Delta_n^{\rm SOD}\|.
\]

A sparse global-null pair receives the SOD classification when

\[
\|\mathcal F_S(z')-\mathcal F_S(z)\|\le\varepsilon_Y,
\]

\[
\|z'-z\|>\varepsilon_z,
\]

and

\[
\boxed{D_{\rm SOD}(z,z')>\varepsilon_r.}
\]

This separates local rank sufficiency from global lineage uniqueness.

## 3. Four-event reference witness

A deterministic bounded fixed-regime multistart search used the same three-attractor family as 07F–07L, with

\[
\Delta\tau=(0.004,0.003,0.005,0.0025).
\]

For the 07L rank-minimal schedule, 60 starts produced 44 converged solutions grouped into two latent clusters. One cluster coincides with the retained reference lineage. A second distinct cluster reproduces the sparse observation record with

\[
\|\Delta Y_S\|_2
=2.2581\times10^{-13},
\]

while its latent separation is

\[
\|\Delta z\|_2
=1.94398\times10^{-3}.
\]

Both histories retain the active-attractor sequence

\[
(A,A,A,A).
\]

Their position-lineage difference is concentrated at the second checkpoint:

\[
\Delta_2^{\rm SOD}
\approx
\left(
2.89728\times10^{-6},
-5.30856\times10^{-7}
\right),
\]

with

\[
\boxed{
D_{\rm SOD}=2.94551\times10^{-6}.
}
\]

The other recorded position checkpoints agree at numerical precision in this witness.

Therefore the declared 07L minimal sparse schedule receives

`FAIL_GLOBAL_INJECTIVITY_SOD_WITNESS_FOUND`

for the four-event reference regime.

## 4. Known-witness spatial separator

The SOD vector directly identifies retained-coordinate candidates capable of separating a discovered branch pair. For the present witness,

\[
|\Delta r_{2x}|=2.89728\times10^{-6},
\qquad
|\Delta r_{2y}|=5.30856\times10^{-7}.
\]

Hence either \(r_{2x}\) or \(r_{2y}\), when promoted into the checkpoint record above the declared spatial tolerance, separates this known SOD pair.

This yields the operational rule

\[
\boxed{
\text{global-null witness}
\rightarrow
\Delta^{\rm SOD}
\rightarrow
\text{promote a separating spatial component}
\rightarrow
\text{repeat global search}.
}
\]

The known-witness separator gate passes. General sparse global injectivity remains a downstream search problem because eliminating one discovered SOD pair does not enumerate all possible global preimages.

## 5. Relation to 07K

07K retains the complete ordered two-component position lineage. Its recursive reconstruction makes the full position lineage an injective reference schedule within the retained active-attractor sequence and positive finite segment durations. Therefore any sparse preimage pair with

\[
D_{\rm SOD}>0
\]

is automatically distinguished by the 07K observation bank.

07M therefore measures exactly what the 07L compression can hide relative to that complete positional reference.

## 6. GREMLIN audit

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The typed relation

`DISTINCT_LATENT_PREIMAGES -> SAME_SPARSE_RECORD -> DISTINCT_STATE_LINEAGES`

matched the generic global-aliasing architecture with `structurally_isomorphic=true`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `1/1`, and `2/2`:

1. the 07L witness pair is observation-equivalent within tolerance and latent-distinct;
2. the pair has nonzero Spatial Offset Divergence;
3. the second-checkpoint spatial coordinates separate the witness.

GREMLIN does not promote the result to canon.

## 7. Evidence artifacts

- implementation: `src/idt/retrodiction_spatial_offset_divergence.py`
- targeted tests: `tests/reference/test_retrodiction_spatial_offset_divergence.py`
- reference run: `experiments/E003_retrodiction/runs/E003_SOD_0001.json`
- receipt: `validation/RETRODICTION_SPATIAL_OFFSET_DIVERGENCE_V0_1.json`
- GREMLIN artifact: `/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_SPATIAL_OFFSET_DIVERGENCE_20260827.json`
