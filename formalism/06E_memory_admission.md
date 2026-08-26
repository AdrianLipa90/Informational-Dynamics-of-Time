# 06E — Memory Admission Integration Gate

Status: `INTEGRATION_REFERENCE_PASS_CANDIDATE / FULL_SUITE_PENDING`

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

## 4. Gate discipline

The integration result verifies compatibility of the declared Memory reference components. Final Memory admission additionally requires the repository reference suite to be rerun on the integrated tree, because a cross-component regression outside the targeted integration surface would invalidate promotion.

Therefore the present status is
\[
\boxed{\text{Memory}:\ \mathrm{INTEGRATION\ PASS\ CANDIDATE},}
\]
with Retrodiction remaining gated until the full-suite condition and combined Memory receipt are satisfied.
