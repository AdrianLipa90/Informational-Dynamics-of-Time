# 06H — Memory to ORCHORBITAL Lineage Admission Bridge

Status: `CANDIDATE / MEMORY_TO_ORCHORBITAL_TARGETED_PASS`

This layer closes the next declared dependency boundary

\[
\mathrm{Memory}\rightarrow\mathrm{ORCHORBITAL\ Attractors}
\]

using the transport-derived Memory receipt and the existing active-centre ORCHORBITAL reference dynamics.

## 1. Event-first ordering

Let the admitted Memory receipt be
\[
\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n).
\]
The event kick is applied first,
\[
X_n^-\xrightarrow{K_{\mathcal E_n}}X_n^+,
\qquad
\Delta v_{M,n}=q_n\delta m_n.
\]
The ORCHORBITAL field is then evaluated on \(X_n^+\), selecting the active attractor used for the following smooth segment.

## 2. Velocity-kick active-attractor invariant

For fixed memory position \(m\), define
\[
u_i:=\frac{\mu_i}{\|m-c_i\|},
\qquad
T:=\frac12\|v_M\|^2.
\]
The binding margin is
\[
\boxed{b_i=[u_i-T]_+.}
\]
A velocity-only Memory kick changes \(T\) while leaving every \(u_i\) unchanged. Whenever the post-kick field remains non-leaking,
\[
\max_i b_i>0,
\]
the maximizing basin obeys
\[
\boxed{
\arg\max_i b_i
=
\arg\max_i u_i.
}
\]
Therefore the active attractor is invariant under an instantaneous velocity-only Memory kick as long as the state remains bound:
\[
\boxed{a_n^+=a_n^-\quad\text{or the kick enters LEAK_MODE}.}
\]
The kick can still change the normalized weights \(w_i\), basin entropy and coherence because the common kinetic subtraction changes the positive margins and their normalization.

A deterministic 3,000-case probe produced 2,998 before/after bound comparisons, zero active-attractor changes, and changed basin weights in all 2,998 comparable cases. Two tested kicks crossed the explicit `LEAK_MODE` boundary.

## 3. Persisted active-centre cell

The smooth ORCHORBITAL segment uses
\[
\ddot m
=-\mu_{a_n}\frac{m-c_{a_n}}{\|m-c_{a_n}\|^3}
\]
for the active basin selected at the segment boundary.

Exact ledger-assisted inversion requires the attractor used by the completed segment. The persisted cell therefore records the already selected attractor snapshot,
\[
\boxed{
\mathcal O_n
=\left(
\mathcal E_n,
 a_n,
 c_{a_n},
 \mu_{a_n}
\right).
}
\]
This introduces no new dynamical parameter; it persists the centre and coupling already consumed by the forward segment.

The forward cell is
\[
\boxed{
X_{n+1}
=\Phi_{a_n}(\Delta\tau_n)
K_{\mathcal E_n}X_n.
}
\]
The inverse cell is
\[
\boxed{
X_n
=K_{\mathcal E_n}^{-1}
\Phi_{a_n}^{-1}(\Delta\tau_n)X_{n+1}.
}
\]
The centred smooth inverse is obtained by translating to \(c_{a_n}\), applying the already declared algebraic inverse of the velocity-Verlet Memory segment, and translating back.

## 4. Lineage and provenance

For an ordered sequence of cells,
\[
X_N=\mathcal C_{N-1}\cdots\mathcal C_0X_0,
\]
where each \(\mathcal C_n\) carries its own persisted active-attractor snapshot. Recall applies the persisted inverse cells in reverse chronology.

A deterministic 500-trajectory probe with six cells per trajectory returned maximum multi-cell reconstruction defect
\[
9.21418979169833\times10^{-16}.
\]
The one-cell centred forward/inverse defect was below
\[
1.5903451134154656\times10^{-15}.
\]

A negative control replaced the persisted active attractor by a different valid centre/coupling. The reconstruction error became
\[
1.779837262553\times10^{-2},
\]
confirming that the active-centre snapshot is provenance required by the inverse lineage rather than decorative metadata.

## 5. Leak boundary

If the event-first state satisfies
\[
\max_i u_i\le T,
\]
then every binding margin vanishes and the field enters `LEAK_MODE`. The v0.1 bridge remains fail-closed and does not fabricate an orbital segment for that event. A separate leak-transport law remains its own future typed contract.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. Forward and inverse lineage cells matched under the explicit typed structure

`POSITIVE_DURATION + TYPED_EVENT_RECEIPT + PERSISTED_ACTIVE_BASIN -> LINEAGE_CELL`.

The relation comparison returned `structurally_isomorphic=true`, SHA-256
`0f09b584029d7896834d7d643a1a646424a63c19f21d78fc09f343db8f6d3c46`.

Three hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `3/3`, and `1/1`.

Reference implementation: `src/idt/memory_orchorbital_bridge.py`.
Reference tests: `tests/reference/test_memory_orchorbital_bridge.py`.
