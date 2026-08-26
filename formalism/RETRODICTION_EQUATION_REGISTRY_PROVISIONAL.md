# Provisional Retrodiction Equation Registry

Status: `DOWNSTREAM_STAGING_ONLY`

These equation IDs are reserved for the single-missing-receipt Retrodiction candidate while the parent Memory node remains pending its full repository reference-suite admission gate. On Memory admission, these entries may be promoted into the canonical `EQUATION_REGISTRY.md` without renumbering.

**EQ-T024 — missing event kick from retained checkpoints**
\[
\widetilde X_n=\Phi_K^{-1}(\Delta\tau_n;\mu_M)X_{n+1},
\qquad
\boxed{\Delta v_{M,n}=\widetilde v_{M,n}-v_{M,n}}.
\]

**EQ-T025 — event-weight retrodiction from a known imprint**
\[
\boxed{
\widehat q_n=
\frac{\operatorname{Re}(\Delta v_{M,n}\delta m_n^*)}{|\delta m_n|^2}
},
\qquad |\delta m_n|>0,
\]
with residual
\[
\boxed{r_n=\Delta v_{M,n}-\widehat q_n\delta m_n}.
\]

**EQ-T026 — imprint retrodiction from a known positive event weight**
\[
\boxed{
\widehat{\delta m}_n=\frac{\Delta v_{M,n}}{q_n}
},
\qquad q_n>0.
\]

**EQ-T027 — product-only scale ambiguity**
\[
\boxed{
(q_n,\delta m_n)\mapsto(cq_n,\delta m_n/c),
\qquad c>0,
}
\]
so
\[
(cq_n)(\delta m_n/c)=q_n\delta m_n.
\]
Therefore the two factors are separately non-identifiable from the memory checkpoints unless one independent factor constraint is supplied.
