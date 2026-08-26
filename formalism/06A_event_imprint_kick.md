# 06A — Event-Imprint Memory Kick Closure

Status: `MEMORY_FRONTIER_CANDIDATE / STRUCTURAL_JUMP_DERIVATION`

Dependency position:

\[
\mathrm{NOW}\rightarrow\mathrm{Bifurcation}\rightarrow\mathrm{Temporal\ Transport}\rightarrow\mathrm{Event\ Imprint}\rightarrow\mathrm{Memory\ Kick}.
\]

The purpose of this layer is to replace the free event-gain placeholder in the reference memory update with a closure built only from quantities already available upstream.

## 1. Upstream inputs

The NOW layer provides the non-negative gauge-invariant event magnitude
\[
q_n\ge 0.
\]
The memory-imprint layer provides the projective displacement
\[
\Delta M_n=\bar\rho_n^+-\bar\rho_n^-,
\]
and its memory-plane projection
\[
\delta m_n
=\operatorname{tr}(\Delta M_nQ_M)
+i\operatorname{tr}(\Delta M_nP_M).
\]
Both inputs are inherited from earlier nodes of the dependency graph.

## 2. T019D — minimal event action

Write the normalized memory coordinate as \(m=x_M+iy_M\), and \(\delta m_n=\delta x_n+i\delta y_n\). Define the localized event action
\[
\boxed{
S_n^{(M)}(m)
=q_n\operatorname{Re}(\delta m_n^*m)
=q_n(\delta x_nx_M+\delta y_ny_M).
}
\]
The event-augmented reference Lagrangian is
\[
L_M
=\frac12|\dot m|^2+\frac{\mu_M}{|m|}
+\sum_n\delta(\tau_{\rm int}-\tau_n)S_n^{(M)}(m).
\]
The smooth part reproduces the Kepler--Newton segment. Integrating the Euler--Lagrange equation through one event gives
\[
\dot m_n^+-\dot m_n^-
=\nabla_mS_n^{(M)}.
\]
Because the action is linear in the real memory-plane coordinates,
\[
\boxed{
\Delta v_{M,n}=q_n\,\delta m_n.
}
\]
Thus the event magnitude controls kick amplitude and the projective imprint controls kick direction. The only event amplitude entering the normalized reference closure is the already-defined \(q_n\).

The generic gain form
\[
\Delta v_M=\chi_M\delta m_n
\]
remains a broader parameterized family; the present reference closure selects the upstream-driven specialization \(\chi_{M,n}=q_n\).

## 3. T019E — exact orbital-invariant update

At fixed event position, substituting the derived kick into the Kepler invariants gives
\[
\boxed{
\Delta E_M
=q_n\operatorname{Re}(v_M^*\delta m_n)
+\frac12q_n^2|\delta m_n|^2,
}
\]
\[
\boxed{
\Delta h_M
=q_n\operatorname{Im}(m^*\delta m_n).
}
\]
These are exact algebraic jump identities for the declared event action.

## 4. Structural controls

The closure has the following immediate controls:

1. \(q_n=0\Rightarrow\Delta v_{M,n}=0\);
2. \(\delta m_n=0\Rightarrow\Delta v_{M,n}=0\);
3. global phase changes of \(\Psi_n^-\) and \(\Psi_n^+\) leave \(\Delta M_n\), \(\delta m_n\), and therefore the kick unchanged;
4. scaling \(q_n\mapsto c q_n\), \(c\ge0\), scales the kick linearly;
5. negative event weights fail closed because the admitted NOW magnitude is non-negative.

Reference-coordinate normalization is used in this layer. Physical-unit calibration belongs to the later metric-time calibration stage.
