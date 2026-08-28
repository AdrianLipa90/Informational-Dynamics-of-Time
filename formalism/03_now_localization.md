# 03 — NOW Localization as a Realized Event Frontier

GREMLIN candidate lineage: `G-CAND-0001`, refined by 00F from positive event support to maximal realized occurrence frontier.

Status: `STRUCTURAL_CANDIDATE / RELATIONAL_PRECEDENCE_FRONTIER_GATE`

## 1. Gauge-invariant event signature

For an admitted relational edge \(e:a\to b\), retain the open oriented phase
\[
\vartheta_e=\operatorname{Arg}L_e
\]
as a gauge-covariant transport quantity. Define the non-negative event signature
\[
\boxed{
q_e=
\sqrt{
 d_{FS}(a,b)^2+
 \kappa^2\Delta H_e^2+
 \kappa^2\sigma_e^2
 }\ge 0.
}
\]
Here
\[
d_{FS}(a,b)=\arccos|\langle\psi_a|\psi_b\rangle|
\]
is the Fubini--Study ray distance.

The positive atomic event measure is
\[
\boxed{\mathcal K_T^+=\sum_e q_e\,\delta_{s_e}.}
\]

Its atomic support
\[
\boxed{
\mathcal E_q:=\operatorname{supp}_{\rm at}\mathcal K_T^+
}
\]
is the carrier of admitted nonzero event signatures.

This carrier records which relational transitions have nonzero event content. NOW is obtained only after lifting this carrier to realized history occurrences.

## 2. Positive realization weighting

Relational density and viscosity supply the positive mobility
\[
M_{ab}=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}>0.
\]

Define
\[
\boxed{\mathcal R_T=\sum_e M_{ab}q_e\,\delta_{s_e}.}
\]

Because \(M_{ab}>0\),
\[
\boxed{
\operatorname{supp}_{\rm at}\mathcal R_T
=\operatorname{supp}_{\rm at}\mathcal K_T^+
=\mathcal E_q.
}
\]

The weighting changes realization strength while preserving the nonzero event carrier.

## 3. Lift from event labels to realized occurrences

00F unfolds a realized relational history into prefix-labelled occurrences
\[
\nu_k=(P_k,x_k)
\]
with derived temporal precedence
\[
\nu_i\prec_T\nu_j
\iff
P_i\text{ is a strict prefix of }P_j.
\]

Each noninitial occurrence has a terminal realized edge \(e(\nu_k)\). For a finite realized down-set \(D\), define its supported realized events by
\[
\boxed{
D_q
:=\{\nu\in D:q_{e(\nu)}>0\}.
}
\]

State-label recurrence leaves the occurrence identities distinct because the full prefixes remain distinct.

## 4. NOW frontier

Define
\[
\boxed{
\mathcal N(D)
:=\operatorname{Max}_{\prec_T}(D_q).
}
\]

Thus NOW is the maximal frontier of supported realized event occurrences.

For a serial realized word with at least one supported event,
\[
\boxed{|\mathcal N(D)|=1.}
\]

For a realized partially ordered structure with independent concurrent branches, \(\mathcal N(D)\) is the antichain of maximal supported occurrences.

The construction therefore supports both a unique serial NOW and a concurrent relational NOW frontier within the same definition.

## 5. Frontier update under realized extension

Let a serial history prefix \(P_n\) be extended by one composable edge
\[
P_{n+1}=e_{n+1}\circ P_n.
\]

If
\[
q_{e_{n+1}}>0,
\]
then the new occurrence is above every earlier prefix occurrence and
\[
\boxed{
\mathcal N(D_{n+1})=\{\nu_{n+1}\}.
}
\]

00E simultaneously gives
\[
\boxed{
\Theta(P_{n+1})
=\Theta(P_n)+\theta(e_{n+1})
>\Theta(P_n).
}
\]

A supported realized extension therefore advances both the maximal event frontier and the intrinsic accumulated duration.

If a composable relation has \(q_e=0\), it does not enter the event-support frontier; the latest supported occurrence remains maximal in \(D_q\).

## 6. Positive pushforward-support identity

For any map \(f\) defined on the atomic event carrier,
\[
(f_*\mathcal K_T^+)(\{y\})
=\sum_{e:f(s_e)=y}q_e.
\]
Every nonempty fibre intersecting \(\mathcal E_q\) has positive total mass, so
\[
\boxed{
\operatorname{supp}_{\rm at}(f_*\mathcal K_T^+)
=f(\mathcal E_q).
}
\]

This identity governs the event carrier. The current NOW object is obtained by the additional maximal-frontier operation on realized occurrences.

## 7. Temporal typing

The typed coordinates entering the bifurcation layer are

```text
relation composition                  : source-target composability
occurrence precedence                 : prefix order from 00F
dTheta_e = activity_e d_lambda_e      : local intrinsic duration
theta(e)                              : invariant integrated edge duration
Theta(P)                              : cumulative realized duration
chi_e = current_e/activity_e          : local directional affinity
q_e                                   : gauge-invariant event signature
E_q                                   : all nonzero event-signature carrier
N(D) = Max_<T(D_q)                    : current realized NOW frontier
M_e q_e                               : positive realization weight
```

The dependency handoff is
\[
\boxed{
\text{RELATIONAL COMPOSITION}
\to
\text{DERIVED PRECEDENCE + DURATION}
\to
\text{SUPPORTED REALIZED OCCURRENCES}
\to
\text{NOW FRONTIER}
\to
\text{BIFURCATION}.
}
\]

Reference implementation for the occurrence/frontier layer: `src/idt/relational_precedence.py`.
Reference tests: `tests/reference/test_relational_precedence.py`.
Validation receipt: `validation/RELATIONAL_PRECEDENCE_NOW_V0_1.json`.
