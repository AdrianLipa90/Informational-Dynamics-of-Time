# 06E — Memory Admission Integration Gate

Status: `INTEGRATION_REFERENCE_PASS_CANDIDATE / TRANSPORT_PARENT_BRIDGE_TARGETED_PASS / HOSTED_FULL_SUITE_BLOCKED`

This gate composes the previously recorded Memory components without introducing a new upstream primitive. Its purpose is to verify that one admitted temporal event can traverse the complete declared Memory reference path and can be reconstructed from the persisted lineage.

## 1. Integrated map

For pure-state \(\mathbb{CP}^1\) anchors, the admitted reference path is

\[
\boxed{
(\psi_a,\psi_b)
\longrightarrow
\xi^{FS}_{a\to b}
\longrightarrow
\delta m_n
\longrightarrow
q_n\delta m_n
\longrightarrow
\mathcal C_n
\longrightarrow
\mathcal E_n.
}
\]

The CP1 displacement is normalized by
\[
\boxed{|\delta m_n|=d_{FS}(a,b)},
\]
while the event action supplies
\[
\boxed{\Delta v_{M,n}=q_n\delta m_n}.
\]
Thus the integrated kick magnitude is
\[
\boxed{|\Delta v_{M,n}|=q_n d_{FS}(a,b)}
\]
inside the CP1 reference subclass. No additional gain parameter is introduced by this gate.

## 2. Persisted memory cell

The append-only receipt
\[
\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n)
\]
specifies the forward reference cell
\[
\mathcal C_n
=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n}.
\]
For a sequence of receipts,
\[
X_N=\mathcal C_{N-1}\cdots\mathcal C_0X_0.
\]
The inverse traversal uses the already declared cell inverses in reverse chronology and must reconstruct every stored checkpoint as well as \(X_0\).

## 3. Admission controls

The integration reference controls require simultaneously:

1. CP1 displacement norm equals the Fubini--Study distance;
2. the upstream event weight \(q_n\) alone sets the kick scale;
3. a multi-event geometry-to-kick-to-Kepler lineage is reconstructed by ledger-assisted recall;
4. every forward checkpoint is recovered in reverse order;
5. tampering with a persisted event weight breaks reconstruction as a negative control;
6. global phase changes of the upstream pure states leave the CP1 receipt geometry unchanged;
7. a zero-weight event leaves only the smooth Kepler segment and remains reversible.

The repository integration test is `tests/reference/test_memory_admission.py`. The isolated exact-formula integration harness passed all six test functions represented there; detailed evidence is recorded in `validation/MEMORY_ADMISSION_V0_1.json`.

## 4. Temporal Transport parent closure

The parent boundary is now supplied by `formalism/06G_transport_memory_admission_bridge.md`.
For one ordered Temporal Transport segment,
\[
\boxed{
\Delta\tau_n
=\frac{\mathfrak a_n}{\mathfrak a_\star}\Delta\lambda_n
}
\]
is inherited from the existing positive-activity clock and is invariant under the declared increasing reparameterizations.

The wave-active NOW layer supplies
\[
r_n^{(W)}=q_n\epsilon_n^{(W)}\ge0
\]
and the exact support gate
\[
g_n=\mathbf 1[r_n^{(W)}>0].
\]
The receipt consumed by Memory is therefore
\[
\boxed{
\mathcal E_n^{T\to M}
=(\Delta\tau_n,g_nq_n,\delta m_n).
}
\]
For a wave-inactive transition, \(g_n=0\) and the receipt advances only the smooth Memory segment. For a wave-active transition, the existing event amplitude \(q_n\) is retained without an additional gain.

Using \(q_n\epsilon_n^{(W)}\) itself as the kick amplitude is recorded as `BLOCKED_NORMALIZATION_DEPENDENT`, because \(\epsilon_n^{(W)}\) scales as \(|c|^2\) under a nonzero rescaling \(\Phi\mapsto c\Phi\), while the positive realization support does not change.

The deterministic transport-to-Memory probe covered 5,000 cases and returned zero gate failures, reparameterization defect below \(1.8\times10^{-15}\), and forward/reverse lineage reconstruction defect below \(4.9\times10^{-13}\). GREMLIN remained `CANDIDATE_ONLY` and returned `SUPPORTED_BY_DECLARED_TESTS` for the three declared hypotheses.

## 5. Gate discipline

The integration result verifies compatibility of the declared Memory reference components and now also supplies a targeted parent bridge from Temporal Transport. Hosted GitHub Actions still terminates before executing repository test steps, so the full-suite condition remains infrastructure-blocked rather than recorded as a code failure.

Therefore the present status is
\[
\boxed{\text{Memory}:\ \mathrm{INTEGRATION\ PASS\ +\ TRANSPORT\ BRIDGE\ PASS\ CANDIDATE},}
\]
with Retrodiction remaining gated until the combined Memory/ORCHORBITAL admission conditions are satisfied.
