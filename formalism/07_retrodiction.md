# 07 — Retrodiction from a Withheld Memory Receipt

Status: `PROVISIONAL_DOWNSTREAM_BRANCH / SINGLE_MISSING_RECEIPT_REFERENCE_CANDIDATE`

Dependency position:

\[
\mathrm{Temporal\ Transport}\rightarrow\mathrm{Memory}\rightarrow\mathbf{Retrodiction}.
\]

The active Memory node has targeted integration evidence but remains pending the full repository reference-suite gate. The construction below is therefore a downstream candidate and cannot promote the Retrodiction node until Memory is admitted.

## 1. Recall and retrodiction are distinct operations

For a complete persisted event ledger, recall applies the known inverse cells
\[
\operatorname{RECALL}_{N\to0}
=\mathcal C_0^{-1}\mathcal C_1^{-1}\cdots\mathcal C_{N-1}^{-1}.
\]
Retrodiction begins when part of that lineage is withheld and must be inferred from the remaining constraints.

Consider one memory cell
\[
X_{n+1}
=\Phi_K(\Delta\tau_n;\mu_M)
\circ K(q_n,\delta m_n)
\,X_n,
\]
where
\[
K(q_n,\delta m_n):
\quad v_M\mapsto v_M+q_n\delta m_n.
\]
The two checkpoints \(X_n\) and \(X_{n+1}\) are retained while one receipt factor is withheld.

## 2. T024 — missing-kick reconstruction

Reverse only the known smooth Kepler segment:
\[
\widetilde X_n
=\Phi_K^{-1}(\Delta\tau_n;\mu_M)X_{n+1}.
\]
Consistency requires the recovered position, internal elapsed activity and swept area to agree with the pre-event checkpoint. The event kick is then
\[
\boxed{
\Delta v_{M,n}
=\widetilde v_{M,n}-v_{M,n}.
}
\]
For the declared reference cell this reconstructs the product
\[
\boxed{
\Delta v_{M,n}=q_n\delta m_n.
}
\]

## 3. T025 — event-weight identifiability from a known imprint

If a nonzero memory displacement \(\delta m_n\) is independently supplied by the upstream state-geometry layer, the scalar event weight is identifiable by projection:
\[
\boxed{
\widehat q_n
=
\frac{\operatorname{Re}(\Delta v_{M,n}\delta m_n^*)}
{|\delta m_n|^2}.
}
\]
The reconstruction is admitted only when
\[
\boxed{
r_n
=\Delta v_{M,n}-\widehat q_n\delta m_n
}
\]
satisfies the declared residual tolerance and \(\widehat q_n\ge0\). A directional mismatch therefore fails closed rather than being silently projected onto the candidate imprint.

For the \(\mathbb{CP}^1\) reference subclass, the upstream normalization
\[
|\delta m_n|=d_{FS}
\]
provides the independent geometric scale needed by this estimator.

## 4. T026 — imprint identifiability from a known event weight

If \(q_n>0\) is independently known while the memory displacement is withheld, then
\[
\boxed{
\widehat{\delta m}_n
=\frac{\Delta v_{M,n}}{q_n}.
}
\]
For \(q_n=0\), consistency requires \(\Delta v_{M,n}=0\); the zero-kick reference returns the zero displacement.

## 5. T027 — product-only scale ambiguity

If neither factor is independently known, the two checkpoints determine only their product. For every \(c>0\),
\[
(q_n,\delta m_n)
\mapsto
(cq_n,\delta m_n/c)
\]
leaves
\[
q_n\delta m_n
\]
unchanged. Hence the factorization is not identifiable from the memory checkpoints alone:
\[
\boxed{
(X_n,X_{n+1},\mu_M,\Delta\tau_n)
\Rightarrow
q_n\delta m_n,
\quad
q_n\ \text{and}\ \delta m_n\ \text{separately require one independent constraint}.
}
\]
The reference implementation therefore raises an explicit ambiguity error when both factors are withheld.

## 6. Evidence boundary

This layer is a structural inverse-problem candidate. It tests identifiability inside the declared event-driven Kepler memory reference class. It does not change the evidence status of Memory and does not open retrocausal claims.

Targeted controls are implemented in `tests/reference/test_retrodiction.py`. A dedicated validation receipt records the isolated exact-formula harness separately from the pending full repository suite.
