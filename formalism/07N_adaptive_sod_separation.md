# 07N — Adaptive Spatial Offset Divergence Separation

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / KNOWN_SOD_ADAPTIVE_SEPARATOR_PASS / BOUNDED_REFERENCE_SEARCH_SINGLE_CLUSTER / GENERAL_GLOBAL_INJECTIVITY_OPEN`

## 1. Input from 07M

07M supplies a concrete sparse global-null pair and its Spatial Offset Divergence lineage

\[
\Delta_n^{\rm SOD}=r_n(z')-r_n(z).
\]

The present gate turns that witness into a deterministic checkpoint refinement. It does not promote a bounded search result into a global uniqueness theorem.

## 2. Separator selection

For a recorded SOD witness define

\[
(k_\star,a_\star)=\arg\max_{k,a\in\{x,y\}} |\Delta_{k,a}^{\rm SOD}|,
\]

with deterministic tie breaking by earliest checkpoint and then \(x\) before \(y\). The promoted scalar is

\[
\boxed{s_{\rm SOD}=r_{k_\star,a_\star}.}
\]

For the 07M four-event witness,

\[
\boxed{s_{\rm SOD}=r_{2x}},
\qquad
|\Delta r_{2x}|=2.897277293967271\times10^{-6}.
\]

Adding this scalar to the 07L record separates that exact pair by the same amount in the augmented observation norm.

## 3. Augmented local gate

For the same four-event reference, the augmented measurement dimension is 11 while the latent dimension remains 8. The finite-difference Jacobian has

\[
\operatorname{rank}J=8,
\]

smallest singular value

\[
\sigma_{\min}=1.0483429761\times10^{-3},
\]

and condition number

\[
\kappa(J)=1.9084322033\times10^3.
\]

Thus the known-witness separator preserves full local observability and improves the recorded conditioning relative to the rank-minimal 07L reference.

## 4. Bounded reference global search

A deterministic fixed-regime damped Gauss-Newton audit used 40 declared starts: the known 07M SOD witness, the reference solution, reference-near perturbations and bounded random starts. Of these, 32 converged without leaving the retained regime. All 32 converged solutions belonged to one latent cluster at the reference solution.

The old 07M witness is no longer observation-equivalent after the refinement:

\[
\|\Delta Y_{S+}\|_2=2.8972772939672797\times10^{-6}.
\]

This gate therefore records `KNOWN_SOD_ADAPTIVE_SEPARATOR_PASS` and `BOUNDED_REFERENCE_SEARCH_SINGLE_CLUSTER`.

General global injectivity remains open because a finite bounded multistart search does not enumerate all possible preimages or all attractor/support regimes.

## 5. Adaptive checkpoint rule

The operational Retrodiction refinement is

\[
\boxed{
\mathcal F_S
\to \text{global-null search}
\to \Delta^{\rm SOD}
\to s_{\rm SOD}
\to \mathcal F_{S+}
\to \text{repeat search}.
}
\]

A future admission gate may terminate this refinement only under a separately declared global search or analytic injectivity criterion.

## 6. GREMLIN audit

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The relation

`AMBIGUOUS_PAIR -> DIFFERENCE_WITNESS -> SEPARATOR -> REFINED_OBSERVATION`

was structurally isomorphic to the generic inverse-problem refinement architecture. Three hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `2/2`, and `3/3`.
