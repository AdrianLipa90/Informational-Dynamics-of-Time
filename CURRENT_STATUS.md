# CURRENT STATUS

The repository is maintained as three parallel spines:

- **FORMALISM** — canonical equations, dependency graph and typed operator contracts;
- **EVIDENCE** — tests, receipts, manifests and audits;
- **MONOGRAPH** — a LaTeX view of admitted formalism and recorded evidence.

Current admitted frontier:

\[
\boxed{\text{Temporal Primitive}\rightarrow\text{Temporal Wave}\rightarrow\text{NOW}\rightarrow\text{Bifurcation}\rightarrow\text{Temporal Transport}\rightarrow\mathbf{Memory}}
\]

Temporal Transport has passed its declared structural reference gate. The active Memory node contains the event-driven Kepler--Newton branch, the upstream event kick \(\Delta v_{M,n}=q_n\delta m_n\), conditional \(\mu_M\) identifiability, the \(\mathbb{CP}^1\) Kähler memory-frame reference subclass, append-only event receipts and ledger-assisted recall.

The integrated Memory path is explicitly tested as
\[
\mathbb{CP}^1\ \text{state geometry}
\rightarrow\delta m_n
\rightarrow q_n\delta m_n
\rightarrow\mathcal C_n
\rightarrow\mathcal E_n
\rightarrow\operatorname{RECALL}.
\]
Targeted integration controls pass in `validation/MEMORY_ADMISSION_V0_1.json`.

A provisional downstream Retrodiction branch now replaces exact ledger replay with one withheld receipt factor. Its reference contract first reconstructs the missing kick
\[
\Delta v_{M,n}=\widetilde v_{M,n}-v_{M,n},
\]
then identifies either \(q_n\) from an independently known \(\delta m_n\), or \(\delta m_n\) from an independently known positive \(q_n\). If both factors are withheld, the implementation fails closed because only the product \(q_n\delta m_n\) is identifiable.

This Retrodiction work remains `PROVISIONAL_DOWNSTREAM_BRANCH`. Memory admission is still `PENDING_FULL_REFERENCE_SUITE`; the first integrated GitHub Actions attempt produced no executable job steps and is recorded as `CI_RESULT_NOT_OBTAINED`. Retrodiction therefore remains gated at the canonical dependency level.
