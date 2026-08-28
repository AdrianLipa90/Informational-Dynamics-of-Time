# 06K — ORCHORBITAL typed observables from pinned PNCS source

Status: `PNCS_V0_27_SOURCE_PINNED / TYPED_OBSERVABLE_REFERENCE_PASS / HOSTED_FULL_SUITE_PASS`.

## Source contract

This layer imports three retained ORCHORBITAL observable families from the exact PNCS snapshot:

- repository: `AdrianLipa90/PhaseNav-Natural-Coding-System`;
- commit: `7a54596c1794be29e0b85f5c363213cc81eb87d7`;
- observable source: `src/phasenav_natural_code/orch_orbital_core_v27.py`;
- reduction source: `src/phasenav_natural_code/orch_orbital_reduction_v27.py`;
- observable contract: `PNCS_ORCHORBITAL_BINDING_V0_27`.

The IDT binding is implemented in `src/idt/orchorbital_pncs_observables.py`.

## Truth scalar

For a typed PNCS observable record

\[
\texttt{pncs:orch-observables:sha256:<digest>},
\]

the retained truth coordinate is

\[
T\in[0,1]
\]

or the explicit null state carried by the upstream PNCS observable contract.

The source repository, source commit, source file and source contract are part of the binding invariant.

## Semantic mass

For each dynamically admitted attractor \(a\), semantic mass is carried as the pair

\[
\bigl(m_{\rm sem}(a),\;\mathrm{mass\_binding\_id}(a)\bigr),
\qquad
m_{\rm sem}(a)\ge 0,
\]

with provenance through the corresponding typed PNCS entity projection.

Complete binding mode requires every attractor leaf in the PNCS hierarchy binding to carry its semantic-mass pair. Partial mode preserves only the explicitly available pairs.

## Reduction readiness

The pinned PNCS reduction contract defines

\[
\Omega
=\lambda_1 C
+\lambda_2 R(S,I)
-\lambda_3\Delta
-\lambda_4\Xi.
\]

The IDT readiness binding preserves the upstream threshold rule exactly:

\[
\boxed{\mathrm{reduce\_ready}\iff \Omega\ge\Omega_{\rm crit}}.
\]

A selected orbital index is carried only for a reduction-ready record and remains a typed non-negative integer.

## Typed observable frame

The ORCHORBITAL observable frame is

\[
\mathcal O_{\rm ORCH}
=
\bigl(
T,
\mathcal R_{\Omega},
\{m_{\rm sem}(a_i)\}
\bigr),
\]

where \(T\), reduction readiness \(\mathcal R_{\Omega}\), and semantic-mass bindings remain separately typed coordinates with independent provenance.

## Residence-weighted semantic mass

Given a verified append-only residence lineage with segment dwell times \(\Delta\tau_k>0\) and active attractors \(a_k\), the temporal aggregate is

\[
\boxed{
\bar m_{\rm sem}^{(\tau)}
=
\frac{\sum_k \Delta\tau_k\,m_{\rm sem}(a_k)}
     {\sum_k \Delta\tau_k}
}.
\]

The aggregate is admitted only when every active attractor in the verified residence lineage resolves to a semantic-mass binding.

## Reference controls

`tests/reference/test_orchorbital_pncs_observables.py` covers:

- typed PNCS observable IDs and source pinning;
- truth scalar closed-unit-interval domain and explicit null state;
- complete and partial semantic-mass extraction;
- exact mass/provenance pairing;
- exact reduction-threshold readiness;
- orbital-selection readiness constraint;
- typed reduction decision, kernel and state IDs;
- separation of truth, reduction and mass carriers;
- residence-weighted semantic mass;
- missing active-attractor mass fail-closed control.

Hosted repository gate:

- workflow: `Reference suite`;
- run: `33196818703` / run number `557`;
- job: `98935954122`;
- command: `python -m pytest -q tests/reference`;
- result: `475 passed in 11.91s`;
- Python: `3.12.14`;
- runner: Ubuntu `24.04`;
- tested PR merge commit: `00057b9a7acb9874bc8cae3a47bd9bcf6877fe7f`;
- tested tree: `42b93983941098c02b350d9fb7bf18536ef4aeee`.

This completes the typed-observable condition declared for the ORCHORBITAL admission gate on the promotion branch.
