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
Registered evidence class: `COMPUTATIONAL_REFERENCE_DIAGNOSTIC`; physical significance evaluation is a later gate.

**EQ-T035 — checkpoint-noise covariance and whitened sensitivity**
\[
\boxed{
\Sigma_Y=LL^T,
\qquad
J_W=L^{-1}J_R.
}
\]
Weighted local identifiability requires
\[
\boxed{\operatorname{rank}J_W=\dim z}.
\]

**EQ-T036 — local Fisher information and latent covariance**
\[
\boxed{
F_z
=J_R^T\Sigma_Y^{-1}J_R
=J_W^TJ_W,
}
\]
and for full column rank,
\[
\boxed{
C_z\approx F_z^{-1},
\qquad
\sigma_{z_i}=\sqrt{(C_z)_{ii}}.
}
\]

**EQ-T037 — weighted residual diagnostic**
\[
\boxed{
Q_W=r^T\Sigma_Y^{-1}r.
}
\]
For observation dimension \(m\) and latent dimension \(p\), when \(m>p\),
\[
\boxed{
\bar Q_W=\frac{Q_W}{m-p}.
}
\]
Registered evidence class: `NOISE_MODEL_REFERENCE_DIAGNOSTIC`; experiment-specific statistical calibration is a later gate.

**EQ-T038 — partial-checkpoint cardinality lower bound**
For \(N\) latent two-component event kicks and four real observed coordinates per retained checkpoint,
\[
4|\mathcal C|\ge2N,
\]
so
\[
\boxed{
|\mathcal C|\ge\left\lceil\frac{N}{2}\right\rceil.
}
\]
This is a necessary dimensional bound; the actual subset must still pass the sensitivity-rank gate.

**EQ-T039 — minimal observable checkpoint selector**
\[
\boxed{
\mathcal C_*
=\arg\min_{\mathcal C\subseteq\mathcal C_{\rm avail}}
|\mathcal C|
\quad\text{subject to}\quad
\operatorname{rank}J_R(\mathcal C)=2N.
}
\]
With an explicitly declared stability threshold, admission additionally requires
\[
\boxed{
\kappa\!\left(J_R(\mathcal C)\right)\le\kappa_{\max}.
}
\]

**EQ-T040 — covariance-preserving checkpoint-permutation null ensemble**
For checkpoint-block permutation matrix \(P_\pi\),
\[
\boxed{
Y_\pi=P_\pi Y_{\rm obs},
\qquad
\Sigma_\pi=P_\pi\Sigma_YP_\pi^T.
}
\]
Every null is fitted with the same weighted model and latent dimension. The finite reference diagnostics are
\[
\boxed{
\Delta Q_{\rm null}=\min_{\pi\ne id}Q_\pi-Q_{\rm obs},
}
\]
and
\[
\boxed{
f_{\rm null}=\frac{\#\{\pi:Q_\pi\le Q_{\rm obs}\}}{N_{\rm null}}}.
\]
`f_null` is registered as a finite computational reference-ensemble diagnostic, not as a p-value.
