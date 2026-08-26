# Falsifiability program

## F1 — Temporal phase transport

Test whether the temporal branch reproduces the standard phase evolution

\[
\Delta\phi_t=-E\Delta t/\hbar
\]

under the stated assumptions and parameter conventions.

Failure condition: the temporal transport equations cannot recover the standard phase relation without inserting it by definition.

## F2 — Spacetime closure

Develop the temporal branch independently, then combine it with a spatial branch and test the resulting phase transport against

\[
\Delta\phi=
\frac{1}{\hbar}
(\mathbf p\cdot\Delta\mathbf x-E\Delta t).
\]

Failure condition: the recombined construction is inconsistent with the target Lorentz-covariant phase structure in its declared domain.

## F3 — NOW/bifurcation model

Implement the NOW bifurcation operator as an explicit state-transition model.

Measure:

- branch conservation/integrity,
- lineage uniqueness for realized states,
- reversibility of reconstructive paths where specified,
- consistency under repeated state re-entry.

Failure condition: the formal branch semantics generate contradictory realized histories under identical admitted state and boundary conditions.

## F4 — Retrodiction versus retrocausality

A retrodictive result must be reproducible using later evidence without changing earlier recorded observables.

A retrocausal candidate requires a preregistered protocol with:

- future condition selected after the earlier measurement event,
- cryptographically committed timestamps and analysis plan,
- blinded condition assignment,
- classical-channel audit,
- shared-clock and scheduler controls,
- null/sham trials,
- no post-selection of earlier events,
- independent replication.

Primary statistical target:

\[
P(X_{\mathrm{past}}\mid Y_{\mathrm{future}})
\stackrel{?}{\neq}
P(X_{\mathrm{past}}).
\]

A deviation enters `RETROCAUSAL_CANDIDATE` only after the predefined null model is rejected and ordinary forward-causal explanations have been audited.

## F5 — Bell/CHSH discrimination where applicable

For experiments claiming nonclassical two-party correlations, use independently chosen measurement settings

\[
a,a',b,b'
\]

and compute

\[
S=E(a,b)+E(a,b')+E(a',b)-E(a',b').
\]

The protocol must document setting independence, timing, detection/selection rules, and classical communication constraints. A correlation coefficient alone does not substitute for CHSH structure.

## Verdict classes

- `PASS_MODEL_INTERNAL`
- `FAIL_MODEL_INTERNAL`
- `CLASSICAL_COMPATIBLE`
- `ANOMALY_CANDIDATE`
- `RETROCAUSAL_CANDIDATE`
- `NONCLASSICAL_CORRELATION_CANDIDATE`
- `MEASURED_PHYSICAL_RESULT`

Promotion between classes requires explicit receipts and preserved raw data.
