# Experimental roadmap

## E0 — Algebraic temporal closure

Goal: implement the temporal transport equations and verify internal identities.

Outputs:

- symbolic derivation,
- numerical phase transport,
- exact/finite-tolerance receipts,
- parameter manifest.

## E1 — NOW bifurcation simulator

Construct a state-wave simulator with

\[
\Psi_{\mathrm{in}}\to N\to\{\Psi_{\mathrm{out}}^{(k)}\}.
\]

Track:

- branch identifiers,
- realization/admission event,
- phase state,
- parent lineage,
- alternative branch status,
- reconstruction fidelity.

## E2 — Memory as temporal re-entry

Use verified PNV lineage as a computational test bed for

\[
\operatorname{RECALL}=\operatorname{TRACE}^{-}.
\]

Compare:

- static retrieval,
- semantic retrieval,
- causal-lineage reconstruction,
- forward replay after restored state.

Primary question: does trajectory-preserving recall improve continuation fidelity after interruption/restart?

## E3 — Spatial-offset / temporal-offset closure

Generate controlled trajectory pairs with

\[
\Delta\mathbf x,\qquad \Delta t
\]

and compare the combined phase offset

\[
\Delta\phi=
\frac{1}{\hbar}
(\mathbf p\cdot\Delta\mathbf x-E\Delta t)
\]

against direct relativistic phase propagation.

## E4 — Retrodictive control benchmark

Construct a blinded dataset in which later observations contain controlled information about earlier hidden states.

Purpose: calibrate the ability of the analysis stack to distinguish ordinary retrodiction from leakage and post-selection before any retrocausal experiment is attempted.

## E5 — Future-condition discrimination protocol

Preregister a protocol in which the future condition is generated only after the earlier observable has been committed.

Required artifacts:

- immutable earlier-event record,
- randomization commitment,
- future-condition record,
- clock provenance,
- channel audit,
- null/sham controls,
- frozen analysis script,
- complete trial ledger.

Primary statistic:

\[
\Delta P=P(X_{\mathrm{past}}\mid Y_{\mathrm{future}})-P(X_{\mathrm{past}}).
\]

## E6 — QHTRI physical discrimination

Where CPU/GPU or another physical substrate is used as a measurement system, maintain separate channels for:

- device telemetry,
- timing/scheduler state,
- thermal and voltage state,
- software errors,
- radiation/error counters where available,
- QHTRI oscillator state,
- independent reference detector where available.

The first target is coincidence/anomaly discrimination against classical controls.

## E7 — CHSH protocol

If a genuine two-party measurement architecture with independently selectable settings is available, implement a preregistered CHSH trial using

\[
S=E(a,b)+E(a,b')+E(a',b)-E(a',b').
\]

The raw event stream, setting choices, coincidence rule, exclusions and final estimator must be frozen before unblinding.

## Evidence rule

Every experiment writes a machine-readable receipt containing:

- hypothesis identifier,
- code/version hash,
- input hashes,
- seed/randomization provenance,
- start/end timestamps,
- raw-data location/hash,
- test statistic,
- null model,
- verdict class.
