# 07Q — Oriented Winding as a Retrodiction Fiber Coordinate

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS / QUOTIENT_FIBER_BINDING_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Purpose

07P established the finite-domain quotient/fiber criterion: whenever two distinct latent histories collide under the retained base observation, an admitted auxiliary fiber coordinate must distinguish them.

07Q tests an already persisted ORCHORBITAL coordinate rather than introducing a new state variable. Each smooth residence receipt carries the signed winding increment

\[
\Delta W_k
=\frac{1}{2\pi}\operatorname{wrap}(\theta_{k+1}-\theta_k),
\]

stored canonically as exact binary64 hexadecimal text.

For an \(N\)-event lineage define the ordered oriented winding fiber

\[
\boxed{
\mathcal W(z)
=\bigl(\Delta W_1(z),\ldots,\Delta W_N(z)\bigr).
}
\]

The ordering is part of the coordinate. The cumulative winding

\[
W_{\Sigma}(z)=\sum_{k=1}^{N}\Delta W_k(z)
\]

is retained as a derived diagnostic, while the separation gate uses the full ordered vector \(\mathcal W\).

## 2. Exact persistence binding

For every event-aware Memory→ORCHORBITAL cell, 07Q reads the existing

```text
residence_receipt.winding_increment_hex
```

field and decodes it with the exact binary64 `float.fromhex` inverse. The gate verifies that the decoded tuple agrees exactly with the winding tuple already exposed by the residence-lineage signature.

Thus the fiber path is

\[
\boxed{
\text{Memory event}
\to
\text{ORCH smooth segment}
\to
\Delta W_k\text{ receipt}
\to
\mathcal W(z).
}
\]

Content hashes remain provenance commitments and do not enter the separation metric.

## 3. Pair-scoped quotient/fiber gate

Let \(Y(z)\) be the declared base observation. For a distinct latent pair \(z,\widetilde z\), define

\[
\delta_B
=\|Y(\widetilde z)-Y(z)\|_2,
\qquad
\delta_Z
=\|\widetilde z-z\|_2,
\]

and the winding-fiber distance

\[
\boxed{
\delta_W
=\|\mathcal W(\widetilde z)-\mathcal W(z)\|_2.
}
\]

At declared tolerances \(\varepsilon_B,\varepsilon_Z,\varepsilon_W>0\), a base-null pair is winding-separated when

\[
\delta_B\le\varepsilon_B,
\qquad
\delta_Z>\varepsilon_Z,
\qquad
\boxed{\delta_W>\varepsilon_W}.
\]

The emitted status is

```text
BASE_NULL_SEPARATED_BY_ORIENTED_WINDING
```

for this condition.

## 4. Reflection-null result

The reference pair is the same two-event reflection null used by 07H and 07O. Its retained base vector contains

\[
(r_{x,2},r_{y,2},v_{x,2},w_{A,2},w_{B,2},w_{C,2}).
\]

The pair remains a base collision at the declared \(10^{-10}\) tolerance and its latent separation remains greater than \(0.9\). Its active-attractor sequence also remains identical across the pair.

07Q adds only the ordered signed winding fiber. The hosted reference test verifies

\[
\boxed{
\delta_W>10^{-12}
}
\]

for the same pair and therefore emits

```text
BASE_NULL_SEPARATED_BY_ORIENTED_WINDING
```

without using provenance hashes.

## 5. Binding to the 07P finite-domain gate

For the declared two-history candidate domain

\[
\mathcal C=\{z,\widetilde z\},
\]

07Q supplies

\[
F_{\rm winding}(z)=\mathcal W(z)
\]

to the generic 07P gate. Since the pair collides in the base projection and separates in \(F_{\rm winding}\), 07P returns

```text
FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER
```

with channel attribution

```text
oriented_winding
```

for the collision.

## 6. Relation to oriented holonomy

The repository already preserves orientation in the temporal-holonomy interface through the full phase carrier

\[
h_R=e^{i\tau_R},
\]

where the sign of \(\sin\tau_R\) retains cycle orientation. 07Q supplies the corresponding Retrodiction-side structural pattern at the ORCHORBITAL residence level: a projection may preserve the coarse/final class while an ordered signed circulation coordinate distinguishes histories inside that class.

GREMLIN classifies this relation as a structural candidate only. Repository promotion is governed by the executable 07Q tests, 07P integration and hosted suite.

## 7. Reference implementation and evidence

Implementation:

- `src/idt/retrodiction_oriented_winding_fiber.py`.

Reference tests:

- `tests/reference/test_retrodiction_oriented_winding_fiber.py`.

The test layer covers:

1. exact reflection-null separation by ordered winding;
2. exact binary64 hex round-trip;
3. deterministic replay for an identical history;
4. direct integration with the 07P finite-domain gate;
5. a non-null control;
6. event-count mismatch rejection;
7. non-positive elapsed-time rejection.

Hosted authority:

- workflow: `Reference suite`;
- run: `33201861565` / run number `607`;
- job: `98953023513`;
- tested branch head: `1c124b7cb37a00ea9ce3e5e96cb3e66c5d7e0363`;
- tested PR merge commit: `35b95bf5596014d76b8710047d036342a3b84e88`;
- command: `python -m pytest -q tests/reference`;
- result: `502 passed in 8.09s`;
- Python `3.12.14`, Ubuntu `24.04.4`;
- conclusion: `success`.

## 8. Active frontier

07Q establishes an oriented-winding separator for the declared reflection fiber and binds that coordinate into the generic 07P finite-domain machinery.

The next Retrodiction gate is to characterize complete base-collision fibers and prove or construct a separator cover using ordered winding together with the already retained continuous ORCHORBITAL and SOD coordinates. `GENERAL_GLOBAL_INJECTIVITY_OPEN` remains the governing global status until that domain-covering argument is receipted.
