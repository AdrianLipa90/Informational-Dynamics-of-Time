# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_ACTIVE / RECALL_REFERENCE_CANDIDATE / RETRODICTION_PROVISIONAL_DOWNSTREAM`

The canonical admitted dependency frontier remains

\[
\boxed{\text{Temporal Primitive}\rightarrow\text{Temporal Wave}\rightarrow\text{NOW}\rightarrow\text{Bifurcation}\rightarrow\text{Temporal Transport}\rightarrow\mathbf{Memory}}
\]

Temporal Transport has passed its declared structural reference gate. The active Memory node contains an event-driven Kepler--Newton reference branch,
\[
\Delta\tau_{\rm int}=\frac{\mathfrak a}{\mathfrak a_\star}\Delta\lambda,
\qquad
\ddot m=-\mu_M\frac{m}{|m|^3},
\qquad
\Delta v_{M,n}=q_n\delta m_n.
\]
The central parameter \(\mu_M\) is conditionally identifiable from orbit observables inside this reference class.

For the pure-state \(\mathbb{CP}^1\) reference subclass, the memory displacement is derived from the Kähler/Fubini--Study state geometry and satisfies
\[
|\delta m|=d_{FS}.
\]

Memory persistence is represented by the append-only event receipt
\[
\boxed{\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n)}
\]
and the reversible reference cell
\[
\mathcal C_n=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n},
\qquad
\mathcal C_n^{-1}=K_{\mathcal E_n}^{-1}\circ\Phi_K^{-1}(\Delta\tau_n;\mu_M).
\]
The complete persisted ledger yields the ledger-assisted recall candidate.

A provisional downstream Retrodiction contract treats one receipt factor as withheld. Reversing the known smooth segment reconstructs
\[
\boxed{\Delta v_{M,n}=\widetilde v_{M,n}-v_{M,n}}.
\]
Conditional factor identification obeys
\[
\boxed{
\widehat q_n=
\frac{\operatorname{Re}(\Delta v_{M,n}\delta m_n^*)}{|\delta m_n|^2}
},
\qquad
\boxed{\widehat{\delta m}_n=\Delta v_{M,n}/q_n}.
\]
When both factors are withheld, the scale family
\[
(q_n,\delta m_n)\mapsto(cq_n,\delta m_n/c),\qquad c>0,
\]
preserves the kick and gives the registered product-only ambiguity.

For multi-event Retrodiction,
\[
\boxed{
J_R(z_0)=\left.\frac{\partial Y}{\partial z}\right|_{z_0},
\qquad z\in\mathbb R^{2N},
}
\]
with first-order local-identifiability gate
\[
\boxed{\operatorname{rank}J_R=2N.}
\]
One final four-component memory checkpoint gives \(\operatorname{rank}J_R\le4\); retained intermediate checkpoints enlarge the observation space and are admitted only after the actual full-column-rank audit.

After this gate passes, the provisional reference estimator is
\[
\boxed{
\widehat z=\arg\min_z\frac12\|Y_{\rm obs}-Y(z)\|_2^2
}
\]
with damped Gauss--Newton update
\[
\boxed{
(J_k^TJ_k+\lambda I)\delta z_k=J_k^Tr_k
}
\]
and strict residual-descent step admission. The estimate is content-committed before sealed truth enters scoring. Zero-kick and checkpoint-order nulls are carried as reference comparisons.

The provisional uncertainty layer introduces a declared checkpoint covariance
\[
\boxed{\Sigma_Y=LL^T},
\qquad
\boxed{J_W=L^{-1}J_R}.
\]
The local Fisher geometry is
\[
\boxed{
F_z=J_R^T\Sigma_Y^{-1}J_R=J_W^TJ_W,
\qquad
C_z\approx F_z^{-1},
}
\]
with local coordinate uncertainties
\[
\boxed{\sigma_{z_i}=\sqrt{(C_z)_{ii}}.}
\]
The committed residual carries weighted diagnostic
\[
\boxed{Q_W=r^T\Sigma_Y^{-1}r.}
\]

Partial checkpoint retention is now represented as a separate observability-selection problem. Because each retained memory checkpoint contributes four real phase-state coordinates while \(N\) event kicks contribute \(2N\) latent coordinates, the dimensional lower bound is
\[
\boxed{
|\mathcal C|\ge\left\lceil\frac{N}{2}\right\rceil.
}
\]
The actual selected set must satisfy
\[
\boxed{
\operatorname{rank}J_R(\mathcal C)=2N.
}
\]
The provisional minimal-information selector is
\[
\boxed{
\mathcal C_*
=\arg\min_{\mathcal C\subseteq\mathcal C_{\rm avail}}|\mathcal C|
\quad\text{subject to}\quad
\operatorname{rank}J_R(\mathcal C)=2N.
}
\]
An explicit numerical-stability gate may additionally impose \(\kappa(J_R(\mathcal C))\le\kappa_{\max}\). Thus checkpoint cardinality and conditioning remain separate measured properties of the inverse problem.

The Retrodiction layer remains `PROVISIONAL_DOWNSTREAM_BRANCH`. Memory admission is pending a real full repository reference-suite result on the integrated tree, so the canonical admitted frontier remains at Memory.
