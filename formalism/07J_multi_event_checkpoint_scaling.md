# 07J — Multi-Event Retrodiction Checkpoint Scaling

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / CHECKPOINT_SCALING_BOUND_PASS / DECLARED_SCHEDULE_N_GE_4_DIMENSIONAL_NO_GO`

This layer asks how the 07F–07I partial-checkpoint architecture scales when the number of unknown two-component event kicks increases.

## 1. Latent dimension

For \(N\) unknown planar kicks,

\[
z=(u_1,\ldots,u_N)\in\mathbb R^{2N},
\]

so

\[
\boxed{d_{\rm latent}=2N.}
\]

## 2. Declared sparse checkpoint schedule

Consider the schedule consisting of:

1. one final partial Memory checkpoint \((r_x,r_y,v_x)\);
2. the final ORCHORBITAL basin-weight vector;
3. one scalar basin weight at each of the \(N-1\) earlier checkpoints.

The final position and retained velocity component supply three scalar channels. Inside a fixed basin-support regime, the complete final basin-weight vector depends on velocity through the single kinetic scalar

\[
T_f=\frac12(v_{x,f}^2+v_{y,f}^2).
\]

Therefore, conditional on the retained final position, all final basin weights add at most one independent first-order channel. The final block has rank at most four.

Each earlier single basin weight contributes at most one additional row. Hence

\[
\boxed{
\operatorname{rank}J_{\rm schedule}
\le 4+(N-1)=N+3.
}
\]

## 3. Necessary identifiability condition

First-order local identifiability of all kick coordinates requires

\[
\operatorname{rank}J=2N.
\]

The declared schedule therefore requires

\[
N+3\ge2N,
\]

or

\[
\boxed{N\le3.}
\]

For \(N\ge4\), the dimensional rank deficit is at least

\[
\boxed{
\Delta d_{\min}
=2N-(N+3)=N-3.
}
\]

Consequently at least \(N-3\) additional independent scalar channels are required before an \(N\ge4\) version of this schedule can reach full local rank.

## 4. Numerical reference

A deterministic fixed-regime finite-difference probe used the same three-attractor family as 07F–07I and 500 random cases for every event count \(N=2,3,4,5,6\).

Observed ranks were:

| \(N\) | latent dim \(2N\) | bound \(N+3\) | observed rank | deficit |
|---:|---:|---:|---:|---:|
| 2 | 4 | 5 | 4 | 0 |
| 3 | 6 | 6 | 6 | 0 |
| 4 | 8 | 7 | 7 | 1 |
| 5 | 10 | 8 | 8 | 2 |
| 6 | 12 | 9 | 9 | 3 |

Every event-count group completed 500/500 finite-difference cases without a regime-boundary failure in the declared probe.

The \(N=3\) reference therefore reaches the dimensional ceiling with local rank six, while the \(N=4,5,6\) references saturate the predicted deficient bound.

## 5. Design consequence

The theorem turns checkpoint design into a budget condition. For the declared family,

\[
\boxed{
\text{additional independent scalar channels required}
\ge\max(0,N-3).
}
\]

The channels may come from additional retained state components or separately derived observables whose Jacobian rows are independent of the existing schedule. The 07F anti-double-counting rule remains active: deterministic post-processing of an already retained full checkpoint cannot be counted again as an independent channel.

The \(N=3\) global-injectivity problem is therefore the next finite case to test. General \(N\)-event injectivity remains downstream of checkpoint sufficiency.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The typed relation

`LATENT_DIMENSION -> MEASUREMENT_RANK_BOUND -> IDENTIFIABILITY_GATE`

matched the generic inverse-problem dimension-count architecture with `structurally_isomorphic=true`, comparison SHA-256
`1ee6f9d915d945befb5e9fb5a51f522f8693ff2ea6fa1c734790528f9a068273`.

Three hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `2/2`, and `1/1`.

Probe artifact:
`/dev/shm/ciel_noema/gremlin/IDT_RETRODICTION_CHECKPOINT_SCALING_PROBE_20260827.json`

SHA-256:
`35e31e9bb044867bf6a2221c25ac1187f845e58640fb5b0ee46f58e3c7a7ab94`

GREMLIN artifact:
`/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_CHECKPOINT_SCALING_20260827.json`

SHA-256:
`fc5fc5b8d3dc8fc9dbabe40ae82b007f53c2634753ebdbad6ff02c942be0f9e2`.
