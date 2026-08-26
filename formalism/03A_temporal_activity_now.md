# 03A — Positive Temporal Activity and NOW Localization

Status: `FORMAL_CANDIDATE_WITH_PROVED_STRUCTURAL_IDENTITIES`

The directed kinetic pair supplies two algebraically distinct observables. For
\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2},
\]
define the symmetric activity and antisymmetric current
\[
\boxed{\mathfrak a_{ab}:=W_{a\to b}+W_{b\to a}=2M_{ab}\cosh(A_{ab}/2)>0,}
\]
\[
\boxed{\mathfrak j_{ab}:=W_{a\to b}-W_{b\to a}=2M_{ab}\sinh(A_{ab}/2).}
\]
Under edge reversal, \(\mathfrak a_{ba}=\mathfrak a_{ab}\) and \(\mathfrak j_{ba}=-\mathfrak j_{ab}\). Moreover,
\[
\frac{\mathfrak j_{ab}}{\mathfrak a_{ab}}=\tanh(A_{ab}/2),
\]
so the drive is recoverable whenever the rates are finite and positive:
\[
\boxed{A_{ab}=2\operatorname{artanh}\!\left(\frac{\mathfrak j_{ab}}{\mathfrak a_{ab}}\right).}
\]
Thus activity carries transition pace, while current carries directed imbalance.

## Positive atomic activity measure

For realized transition events at ordered locations \(s_n\), define
\[
\boxed{\mathcal A_T:=\sum_n \mathfrak a_n\,\delta_{s_n},\qquad \mathfrak a_n>0.}
\]
The active localization candidate is refined to
\[
\boxed{\mathcal N:=\operatorname{supp}_{\rm at}\mathcal A_T.}
\]
The earlier signed transition measure remains useful for phase/current bookkeeping; the positive activity measure is used for event existence because coincident positive atoms add rather than cancel.

## Positive pushforward-support theorem

Let \(f:S\to S'\) be any map defined on the atomic support. For a positive atomic measure
\[
\mu=\sum_j a_j\delta_{x_j},\qquad a_j>0,
\]
its pushforward satisfies
\[
(f_*\mu)(\{y\})=\sum_{j:f(x_j)=y}a_j.
\]
Every non-empty fibre intersecting the original support has strictly positive total mass. Therefore
\[
\boxed{\operatorname{supp}_{\rm at}(f_*\mu)=f(\operatorname{supp}_{\rm at}\mu).}
\]
Injectivity is no longer required for support preservation because positive masses cannot cancel when several atoms merge. Admissible monotone reparameterizations are an immediate special case.
