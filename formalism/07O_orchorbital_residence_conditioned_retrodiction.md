# 07O — Event-aware ORCHORBITAL residence conditioning for Retrodiction

Status: `PROVISIONAL_DOWNSTREAM / EVENT_AWARE_RESIDENCE_BRIDGE_TARGETED_PASS / RESIDENCE_LABEL_KNOWN_NULL_PERSISTENCE_PASS / PROVENANCE_FIREWALL_PASS / HOSTED_FULL_SUITE_PASS / GLOBAL_INJECTIVITY_OPEN`.

## 1. Dependency position

The admitted promotion-branch path is

\[
\mathrm{Memory}
\rightarrow
\mathrm{ORCHORBITAL\ Attractors}
\rightarrow
\mathbf{Retrodiction}.
\]

07F and 07G already establish the local ORCHORBITAL observability/estimation interface. 07H records a declared global reflection-null pair and its separation by one earlier continuous basin-weight scalar. This layer connects Retrodiction to the newly admitted content-addressed ORCHORBITAL residence lineage while preserving the Memory event boundary explicitly.

Reference implementation:

`src/idt/retrodiction_orchorbital_residence_conditioning.py`.

## 2. Event-aware residence cell

A plain ORCHORBITAL residence ledger joins directly state-continuous smooth segments. A Memory lineage inserts an event kick before each smooth ORCHORBITAL segment:

\[
X_k^-
\xrightarrow{\mathcal E_k}
X_k^{K}
\xrightarrow{\Phi_{a_k}(\Delta\tau_k)}
X_k^+.
\]

The versioned bridge cell therefore binds

\[
\boxed{
\mathcal B_k=
\left(
 k,
 \tau_k^-,
 \mathcal E_k,
 H(X_k^-),
 \mathcal R_k^{\rm smooth},
 h_{k-1}
\right),
}
\]

where \(\mathcal R_k^{\rm smooth}\) is one verified genesis-form `idt.orchorbital-residence-receipt/v1` for the event-following smooth segment.

The outer bridge chain enforces

\[
\boxed{
H(X_{k-1}^+)=H(X_k^-)
}
\]

across event cells. Inside each cell, the Memory event is replayed before the smooth-segment receipt is committed, and

\[
\boxed{
H(K_{\mathcal E_k}X_k^-)
=
H(X_{k,\rm smooth}^-).
}
\]

The bridge itself is content-addressed by canonical JSON and SHA-256.

## 3. Exact elapsed-time binding

The Memory event stores the scheduled binary64 increment \(\Delta\tau_k^{E}\). The residence receipt stores the observed state increment

\[
\Delta\tau_k^{R}
=\tau_k^+-\tau_k^-.
\]

At finite binary64 precision the bridge validates the exact arithmetic path

\[
\boxed{
\Delta\tau_k^{R}
=
\operatorname{fl}
\left(
\operatorname{fl}(\tau_k^-+\Delta\tau_k^{E})-\tau_k^-
\right).
}
\]

This admits large-\(\tau\), small-\(\Delta\tau\) cases where the stored schedule and observed increment have distinct exact hexadecimal encodings while remaining linked by the declared arithmetic operation.

The reference hardening case uses

\[
\tau_k^-=36,
\qquad
\Delta\tau_k^{E}=10^{-8},
\]

for which the two binary64 encodings differ and the exact operation-level binding passes.

## 4. Retained residence signature

For an event-aware bridge lineage define

\[
\Sigma_R=
\left(
(a_k)_k,
(a_k^+)_k,
I_{\rm switch},
I_{\rm leak},
(\Delta W_k)_k
\right).
\]

The discrete conditioning coordinates are

- active-attractor sequence \((a_k)_k\);
- post-segment next-attractor sequence \((a_k^+)_k\);
- switch-index set \(I_{\rm switch}\);
- leak-index set \(I_{\rm leak}\).

Winding \((\Delta W_k)_k\) remains a separately reported continuous coordinate.

The bridge-head SHA-256 remains a provenance commitment. Pair-separation status is computed from declared retained semantic coordinates; the provenance hash is excluded from that decision.

## 5. Known reflection-null audit

Use the exact 07G/07H two-event pair

\[
\begin{aligned}
u_1&=(0.034,-0.023),\\
u_2&=(-0.008,0.028),
\end{aligned}
\]

and

\[
\begin{aligned}
\tilde u_1&=(0.03399999999998063,0.34071654937113033),\\
\tilde u_2&=(-0.00802729491823317,-0.8206629500579328).
\end{aligned}
\]

Their latent separation remains greater than \(0.9\), while the final retained base observation

\[
Y_B=(r_x,r_y,v_x,w_A,w_B,w_C)_2
\]

remains equivalent at the declared \(10^{-10}\) tolerance.

The event-aware residence audit returns

\[
\boxed{
(a_k)_k=(\tilde a_k)_k
}
\]

and the same next-attractor/switch/leak lineage for the pair. Therefore its pair-scoped status is

`KNOWN_NULL_PERSISTS_UNDER_RESIDENCE_LABELS`.

The two content-addressed bridge heads differ, demonstrating the provenance firewall in the reference control: cryptographic commitments remain integrity coordinates while the semantic residence-label gate preserves the declared global collision.

The continuous earlier basin weight from 07H remains an independently retained separator for this pair:

\[
|w_{A,1}(z)-w_{A,1}(\tilde z)|
=0.01918916841099516.
\]

Thus the current evidence distinguishes three information classes:

\[
\boxed{
\text{discrete residence labels}
\;\mid\;
\text{continuous ORCH observables}
\;\mid\;
\text{provenance commitments}.
}
\]

## 6. Reference controls

`tests/reference/test_retrodiction_orchorbital_residence_conditioning.py` covers:

- Memory-event-to-smooth-residence bridge construction;
- pre-event state continuity across bridge cells;
- event-mediated change between pre-event and smooth-segment input hashes;
- event-local verified residence receipts;
- content-hash tamper detection;
- the declared reflection-null active-label equivalence;
- switch-lineage equivalence for the declared reflection pair;
- provenance-head exclusion from semantic pair separation;
- independently reported winding diagnostic;
- distinct-latent-history admission;
- empty/mismatched lineage fail-closed controls.

`tests/reference/test_retrodiction_orchorbital_residence_time_binding.py` covers the large-internal-time exact binary64 elapsed-time binding.

Hosted repository gate:

- workflow: `Reference suite`;
- run: `33198069462` / run number `576`;
- job: `98940226102`;
- command: `python -m pytest -q tests/reference`;
- result: `486 passed in 8.89s`;
- Python: `3.12.14`;
- runner: Ubuntu `24.04.4`;
- tested branch commit: `7537322cbf9df4c4270d79619ed1dc6f2ae028b9`;
- tested PR merge commit: `adbf31231033ab602455a75393b65816857f6afd`;
- tested tree: `d6064dbb6092a976c376a1c4a14cf53225bcb263`.

## 7. Frontier result

The ORCHORBITAL residence-conditioning interface is now executable and hosted-suite validated. The declared 07G global reflection pair remains a residence-label-equivalent pair. The Retrodiction frontier therefore advances to information channels capable of separating remaining global branches, including previously demonstrated continuous earlier ORCHORBITAL scalars and the later spatial-offset/divergence separators, while `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status.
