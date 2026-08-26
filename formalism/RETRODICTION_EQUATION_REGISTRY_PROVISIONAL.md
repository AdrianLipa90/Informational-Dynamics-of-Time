# Provisional Retrodiction Equation Registry

Status: `DOWNSTREAM_STAGING_ONLY`

These equation IDs are reserved for the provisional Retrodiction branch while the parent Memory node remains pending its full repository reference-suite admission gate. On Memory admission, these entries may be promoted into the canonical `EQUATION_REGISTRY.md` without renumbering.

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

**EQ-T028 — multi-event Retrodiction sensitivity matrix**
\[
\boxed{
J_R(z_0)=\left.\frac{\partial Y}{\partial z}\right|_{z_0},
\qquad
z=(u_1,\ldots,u_N)\in\mathbb R^{2N}.
}
\]
The first-order local identifiability gate is
\[
\boxed{\operatorname{rank}J_R=2N}.
\]

**EQ-T029 — final-checkpoint dimensional bound**
\[
Y_f\in\mathbb R^4,
\qquad
J_R^{\rm final}\in\mathbb R^{4\times2N},
\qquad
\boxed{\operatorname{rank}J_R^{\rm final}\le4}.
\]
Hence
\[
\boxed{N>2\Longrightarrow 4<2N\Longrightarrow\text{final-only multi-kick Retrodiction is dimensionally underdetermined}.}
\]

**EQ-T030 — checkpoint-augmented observability dimension**
For retained post-event checkpoint set \(\mathcal C\),
\[
Y_{\mathcal C}\in\mathbb R^{4|\mathcal C|},
\qquad
J_R\in\mathbb R^{4|\mathcal C|\times2N}.
\]
A necessary dimensional condition is
\[
\boxed{4|\mathcal C|\ge2N},
\]
followed by the actual full-column-rank check
\[
\boxed{\operatorname{rank}J_R=2N}.
\]

**EQ-T031 — gated damped Gauss--Newton Retrodiction estimator**
\[
\boxed{
\widehat z
=\arg\min_z\frac12\|Y_{\rm obs}-Y(z)\|_2^2
}
\]
with iteration
\[
\boxed{
(J_k^TJ_k+\lambda I)\delta z_k=J_k^Tr_k,
\qquad
r_k=Y_{\rm obs}-Y(z_k),
\qquad \lambda\ge0.
}
\]
Only a line-search step satisfying
\[
\|Y_{\rm obs}-Y(z_k+\alpha\delta z_k)\|_2<\|r_k\|_2
\]
is admitted.

**EQ-T032 — pre-truth estimate commitment**
\[
\boxed{
C_{\rm est}
=\operatorname{SHA256}(\widehat z\,\|\,\widehat Y\,\|\,r\,\|\,\mathrm{metadata}).
}
\]
The scorer verifies \(C_{\rm est}\) before sealed truth enters the scoring stage.

**EQ-T033 — reference-null residual reductions**
For zero-kick and checkpoint-shuffle null residuals \(r_0\) and \(r_{\rm shuf}\),
\[
\boxed{
R_0=1-\frac{r_{\rm est}}{r_0},
\qquad
R_{\rm shuf}=1-\frac{r_{\rm est}}{r_{\rm shuf}}.
}
\]
These are reference-model computational diagnostics rather than physical significance statistics.
