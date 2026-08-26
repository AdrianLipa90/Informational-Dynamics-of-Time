# 07D — Partial Checkpoint Selection for Retrodiction

Status: `PROVISIONAL_DOWNSTREAM_REFERENCE_CONTRACT`

Dependency position:

\[
\mathrm{Observability}\rightarrow\mathrm{Estimation}\rightarrow\mathrm{Uncertainty}\rightarrow\mathrm{Checkpoint\ Selection}.
\]

The canonical admitted frontier remains Memory pending its full-suite admission result. This layer asks which retained checkpoint subsets are sufficient to support a locally identifiable latent-lineage inverse problem.

## 1. Cardinality lower bound

For \(N\) unknown two-component event kicks,
\[
\dim z=2N.
\]
Each retained memory phase-state checkpoint contributes four observed real coordinates. Therefore any checkpoint set \(\mathcal C\) must satisfy the necessary dimensional bound
\[
4|\mathcal C|\ge2N,
\]
or equivalently
\[
\boxed{
|\mathcal C|\ge\left\lceil\frac{N}{2}\right\rceil.
}
\]
This is a lower bound only; causal structure and dynamical degeneracy may reduce actual rank.

## 2. Exact subset admission rule

For candidate retained checkpoint set \(\mathcal C\), define
\[
J_R(\mathcal C)=\frac{\partial Y_{\mathcal C}}{\partial z}.
\]
A subset is locally observable when
\[
\boxed{
\operatorname{rank}J_R(\mathcal C)=2N.
}
\]
If an explicit conditioning threshold \(\kappa_{\max}\) is supplied, admission additionally requires
\[
\boxed{
\kappa\!\left(J_R(\mathcal C)\right)\le\kappa_{\max}.
}
\]

## 3. Minimal observable checkpoint set

The provisional selection problem is
\[
\boxed{
\mathcal C_*=
\arg\min_{\mathcal C\subseteq\mathcal C_{\rm avail}}
|\mathcal C|
\quad\text{subject to}\quad
\operatorname{rank}J_R(\mathcal C)=2N.
}
\]
When multiple subsets have the same minimal cardinality, the reference tie-break minimizes the local condition number and then uses lexicographic checkpoint order.

With a declared condition gate, the same cardinality minimization is applied to subsets satisfying both full rank and the declared \(\kappa_{\max}\).

## 4. Information minimality versus numerical stability

The three-kick reference branch demonstrates that minimal cardinality and stable inversion are distinct properties. With available checkpoints \(\{1,2,3\}\), the dimensional lower bound is two. In the recorded reference case, both \(\{1,3\}\) and \(\{2,3\}\) have rank six. The condition numbers are approximately
\[
\kappa_{13}\approx66.3,
\qquad
\kappa_{23}\approx72.2.
\]
Thus the minimal-cardinality selector chooses
\[
\boxed{\mathcal C_* = \{1,3\}}.
\]
Retaining all three checkpoints gives
\[
\boxed{\kappa_{123}\approx4.076,}
\]
which is substantially better conditioned. Under an explicit reference condition gate \(\kappa_{\max}=10\), the selected set therefore becomes \(\{1,2,3\}\).

## 5. Causal information loss

For the same three-kick lineage, retaining only checkpoints \(\{1,2\}\) gives rank four for six latent coordinates. The later third-event kick has no downstream checkpoint in that retained set, and the subset is rejected by the rank gate.

This behavior is measured through the forward sensitivity matrix rather than imposed as an additional symbolic rule.

## 6. Reference evidence

The executable implementation is `src/idt/retrodiction_checkpoint_selection.py`, with targeted tests in `tests/reference/test_retrodiction_checkpoint_selection.py` and receipt `validation/RETRODICTION_CHECKPOINT_SELECTION_V0_1.json`.

The reference audit also samples the declared three-event parameter range to compare minimal full-rank subsets with the better-conditioned all-checkpoint geometry. Its evidence class is `PARTIAL_OBSERVATION_REFERENCE_DIAGNOSTIC`.
