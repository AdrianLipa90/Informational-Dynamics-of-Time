# 06D — Memory Persistence and Recall

Status: `MEMORY_FRONTIER_CANDIDATE / REVERSIBLE_LINEAGE_REFERENCE_CLASS`

This layer defines persistence as an append-only event ledger attached to the event-driven Kepler memory branch and defines recall as reverse reconstruction through the recorded lineage. The result is a conditional reference-class identity: reconstruction is exact for the declared reversible numerical cell when the complete event ledger and the same model parameters are available.

## 1. T019M — persistent event receipt

For each admitted memory event record
\[
\boxed{
\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n),
}
\]
where \(\Delta\tau_n>0\) is the subsequent internal elapsed-activity segment, \(q_n\ge0\) is the NOW event magnitude and \(\delta m_n\) is the Kähler-memory displacement supplied by the admitted memory frame.

The event kick is therefore fully reconstructible from the receipt,
\[
\boxed{
K_{\mathcal E_n}:\quad v_M\mapsto v_M+q_n\delta m_n.
}
\]
The inverse event operation is
\[
\boxed{
K_{\mathcal E_n}^{-1}:\quad v_M\mapsto v_M-q_n\delta m_n.
}
\]
No additional free gain is introduced by the persistence layer.

## 2. T019N — reversible memory-lineage cell

Let \(\Phi_K(\Delta\tau_n;\mu_M)\) denote the declared velocity-Verlet Kepler reference step. A forward lineage cell is
\[
\boxed{
\mathcal C_n
=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n}.
}
\]
For the repository reference update
\[
r_1=r_0+v_0\Delta\tau+\frac12a_0\Delta\tau^2,
\]
\[
v_1=v_0+\frac12(a_0+a_1)\Delta\tau,
\]
the algebraic inverse is obtained from the final state by
\[
\boxed{
r_0=r_1-v_1\Delta\tau+\frac12a_1\Delta\tau^2,}
\]
\[
\boxed{
v_0=v_1-\frac12(a_0+a_1)\Delta\tau.}
\]
Consequently
\[
\boxed{
\mathcal C_n^{-1}
=K_{\mathcal E_n}^{-1}\circ\Phi_K^{-1}(\Delta\tau_n;\mu_M).
}
\]
The swept-area and internal-time bookkeeping carried by the reference state are reversed by subtracting the corresponding forward segment increments.

## 3. T034 — ledger-assisted RECALL

For a persisted sequence of \(N\) cells,
\[
X_N
=\mathcal C_{N-1}\cdots\mathcal C_1\mathcal C_0X_0.
\]
Define the recall operator on the recorded reference lineage by reverse chronological composition,
\[
\boxed{
\operatorname{RECALL}_{N\to0}
=\mathcal C_0^{-1}\mathcal C_1^{-1}\cdots\mathcal C_{N-1}^{-1}.
}
\]
Then, within the declared reference class,
\[
\boxed{
\operatorname{RECALL}_{N\to0}(X_N;\{\mathcal E_n\},\mu_M)=X_0.
}
\]
The chronological order of the persisted receipts is structural. Reversing the ledger before applying the reverse-time traversal is a negative control and does not in general reconstruct the initial state.

## 4. Persistence contract

Persistence is append-only. An admitted lineage record stores the ordered receipts
\[
\mathcal L_M=(\mathcal E_0,\mathcal E_1,\ldots,\mathcal E_{N-1})
\]
together with the model/version identity needed to interpret them. Earlier receipts are not rewritten when a later event arrives.

This persistence contract gives a deterministic provenance path

`NOW event -> Kähler displacement -> event kick -> Kepler segment -> receipt -> replay / recall`.

## 5. Retrodiction gate

T034 reconstructs a recorded prior memory state inside the reversible reference model. The next node, Retrodiction, must distinguish reconstruction of a persisted lineage from inference of an unrecorded prior state. Opening Retrodiction therefore requires its own estimator, null model and validation receipt.

Reference controls are recorded in `validation/MEMORY_PERSISTENCE_RECALL_V0_1.json`.
