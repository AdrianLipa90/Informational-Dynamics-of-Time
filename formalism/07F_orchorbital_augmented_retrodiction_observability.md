# 07F — ORCHORBITAL-Augmented Retrodiction Observability

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / ORCHORBITAL_OBSERVABILITY_TARGETED_PASS`

This layer consumes the persisted Memory→ORCHORBITAL lineage and asks a narrower question: when ORCHORBITAL checkpoint observables are added to Retrodiction, do they supply genuinely new first-order information or only deterministic post-processing of an already retained Memory state?

## 1. Deterministic observables of a full checkpoint

Let the retained Memory phase-state checkpoint be
\[
X=(r_x,r_y,v_x,v_y)\in\mathbb R^4
\]
and let the continuous ORCHORBITAL observable vector be
\[
O=f(X),
\]
for example the bound-basin weight vector \(w=(w_1,\ldots,w_N)\).

For latent event coordinates \(z\),
\[
J_X=\frac{\partial X}{\partial z},
\qquad
J_O=\frac{\partial O}{\partial z}.
\]
Inside one fixed attractor/support regime the chain rule gives
\[
\boxed{
J_O=Df(X)J_X.
}
\]
Therefore
\[
\boxed{
\operatorname{rank}
\begin{pmatrix}
J_X\\J_O
\end{pmatrix}
=
\operatorname{rank}J_X.
}
\]
Basin weights, entropy, coherence and other deterministic continuous functions of a fully retained phase-state checkpoint cannot be counted as additional independent first-order observations.

The deterministic 500-case probe returned identical full-checkpoint rank before and after adding basin weights in all 500 cases. The maximum numerical residual of the ORCHORBITAL-weight Jacobian outside the row space of the full-state Jacobian was
\[
3.457720719261408\times10^{-16}.
\]

## 2. Partial checkpoints

Let a partial checkpoint retain
\[
Y_P=PX
\]
for a projection \(P\). The augmented measurement is
\[
Y_{P,O}=(PX,f(X)).
\]
Its Jacobian is
\[
\boxed{
J_{P,O}=
\begin{pmatrix}
P J_X\\Df(X)J_X
\end{pmatrix}.
}
\]
The ORCHORBITAL rows may add directions missing from \(PJ_X\), while the rank still obeys
\[
\operatorname{rank}J_{P,O}\le\operatorname{rank}J_X.
\]

For the tested two-kick reference with four latent coordinates, one final checkpoint retaining
\[
(r_x,r_y,v_x)
\]
had rank three. Adding the three basin weights raised the local rank to four in 500/500 deterministic nearby cases.

For a position-only checkpoint
\[
(r_x,r_y),
\]
the rank was two, while adding basin weights raised it to three in 500/500 cases and remained below the four-dimensional latent target.

## 3. Why one kinetic channel appears

At fixed position define
\[
u_i=\frac{\mu_i}{r_i},
\qquad
T=\frac12(v_x^2+v_y^2),
\]
so in a fixed positive-support regime
\[
b_i=u_i-T,
\qquad
w_i=\frac{u_i-T}{\sum_j(u_j-T)}.
\]
The basin weights therefore carry sensitivity to the scalar kinetic channel \(T\). If position and one velocity component are retained, and the omitted velocity component is nonzero, the weight Jacobian can supply the missing local derivative direction.

This is a local result. Since \(T\) depends quadratically on velocity, basin weights do not by themselves remove the corresponding global sign ambiguity of an omitted velocity component.

## 4. Active-basin labels and switching boundaries

The discrete active-attractor label is piecewise constant inside a basin interior. It therefore contributes no regular first-order Jacobian row away from switching boundaries.

At a switching, support-entry or `LEAK_MODE` boundary the observation map is non-smooth. The reference finite-difference implementation fails closed whenever the plus/minus perturbations cross a different active-attractor sequence or bound-support pattern. Such a point is classified as a boundary problem rather than assigned a misleading regular Jacobian.

## 5. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. The typed chain

`CHECKPOINT_STATE -> DETERMINISTIC_DERIVED_OBSERVABLE -> RETRODICTION_MEASUREMENT`

matched the generic observability/post-processing architecture with `structurally_isomorphic=true`, comparison SHA-256
`ce96e66a14072f5f89731cd42ff1ec7ca171232162349fd5cb0132e931d9651b`.

Three declared hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `2/2`, and `2/2`.

Reference implementation: `src/idt/retrodiction_orchorbital_observability.py`.
Reference tests: `tests/reference/test_retrodiction_orchorbital_observability.py`.
