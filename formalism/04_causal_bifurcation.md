# 04 — Causal Bifurcation

GREMLIN candidate lineage: `G-CAND-0002`.

Status: `ACTIVE_DERIVATION_TARGET / STRUCTURAL_REFERENCE_SUBCLASS_IMPLEMENTED`

The NOW layer localizes an admitted event. The bifurcation layer defines the action across that event:
\[
\boxed{
\Psi_T(s_n^+)=B_n\Psi_T(s_n^-),
\qquad s_n\in\mathcal N.
}
\]
Event existence and event orientation remain typed separately.

## 1. Generic event representation

For an additive scalar event parameter \(q\), representation consistency requires
\[
B(0)=I,
\qquad
B(q_1+q_2)=B(q_2)B(q_1).
\]
For a strongly continuous invertible representation of \((\mathbb R,+)\),
\[
\boxed{B(q)=e^{qG}.}
\]
The unitary subclass has \(G=-iA\) with self-adjoint \(A\):
\[
\boxed{B(q)=e^{-iqA}.}
\]
This is T024. It classifies an admissible reversible operator family without selecting a physical generator.

## 2. Directional phase parameter from activity/current

The earlier kinetic layer gives
\[
\mathfrak a_n>0,
\qquad
|\mathfrak j_n|<\mathfrak a_n.
\]
Define
\[
r_n:=\frac{\mathfrak j_n}{\mathfrak a_n}.
\]
The edge drive and affinity are reconstructed as
\[
A_n=2\operatorname{artanh}(r_n),
\qquad
\sigma_n=\frac{A_n}{\ln2}.
\]
The already-admitted Shannon-phase link therefore supplies a directed phase increment
\[
\boxed{
\beta_n:=\kappa\sigma_n
=\frac{2\kappa}{\ln2}\operatorname{artanh}(r_n).
}
\]
Using the canonical normalization
\[
\kappa=\frac{\ln2}{24\pi},
\]
this simplifies exactly to
\[
\boxed{
\beta_n=\frac{1}{12\pi}
\operatorname{artanh}\!\left(\frac{\mathfrak j_n}{\mathfrak a_n}\right).
}
\]
This is T025.

## 3. Reference unitary directional subclass

Let \(G\) be a declared self-adjoint generator. The directional phase-only bifurcation subclass is
\[
\boxed{B_\phi(\beta_n)=e^{-i\beta_n G}.}
\]
For the reference implementation, \(G^2=I\), hence
\[
B_\phi(\beta)=\cos\beta\,I-i\sin\beta\,G.
\]
The generator is part of the operator contract; the current formalism does not infer a unique physical \(G\).

The subclass obeys three structural controls:
\[
\mathfrak j=0\Rightarrow\beta=0\Rightarrow B_\phi=I,
\]
\[
\mathfrak j\mapsto-\mathfrak j
\Rightarrow
\beta\mapsto-\beta
\Rightarrow
B_\phi(-\beta)=B_\phi(\beta)^{-1},
\]
and, for one fixed generator,
\[
B_\phi(\beta_2)B_\phi(\beta_1)
=B_\phi(\beta_1+\beta_2).
\]
This is T026.

## 4. Dependency boundary

No memory coordinate, retrodictive operator or spacetime quantity is used in this derivation. Existing memory-orbit work is preserved as a provisional downstream candidate and can only be admitted after this bifurcation layer and the subsequent temporal-transport layer receive independent receipts.

## 5. Open bifurcation classes

The current unitary phase-only subclass supplies a reversible structural reference. Separate evidence is still required for:

1. non-unitary/contractive bifurcations;
2. branch-mixing generator selection;
3. information-change functionals across the jump;
4. coupling between the gauge-invariant event magnitude \(q_n\) and the operator generator;
5. ordered multi-event transport with non-commuting generators.
