# 00B — Directed Transition Affinity

Status: `FORMAL_CANDIDATE_WITH_PROVED_STRUCTURAL_IDENTITIES`

This layer closes the first explicit version of derivational debt `A0-SIGMA` from the Shannon–phase core. It introduces a path-level quantity from forward/reverse transition asymmetry rather than treating the non-exact edge increment as a free number.

For two relational states `a,b` with strictly positive admitted transition probabilities
\[
P(b\mid a)>0,
\qquad
P(a\mid b)>0,
\]
define the directed transition affinity in bits
\[
\boxed{
\sigma_{a\to b}
=
\log_2\frac{P(b\mid a)}{P(a\mid b)}.
}
\]

This is a transition quantity. It is not a state entropy and it need not be an exact difference of a scalar state function.

## Theorem T007 — antisymmetry

\[
\sigma_{b\to a}=-\sigma_{a\to b}.
\]

Immediate consequence:
\[
P(b\mid a)=P(a\mid b)
\quad\Longrightarrow\quad
\sigma_{a\to b}=0.
\]

## Cycle affinity

For a directed cycle
\[
C=(s_0\to s_1\to\cdots\to s_N=s_0),
\]
define
\[
\boxed{
\mathcal A_C
=
\sum_{e\in C}\sigma_e
=
\log_2
\prod_{e\in C}
\frac{P(s_{e+1}\mid s_e)}{P(s_e\mid s_{e+1})}.
}
\]

Unlike the exact Shannon difference, \(\mathcal A_C\) is not forced to vanish by telescoping.

## Theorem T008 — detailed-balance cycle cancellation

Assume there exists a strictly positive relational weight \(\pi_s\) such that every admitted pair obeys
\[
\pi_a P(b\mid a)=\pi_b P(a\mid b).
\]
Then
\[
\sigma_{a\to b}=\log_2\frac{\pi_b}{\pi_a}
\]
and therefore every closed cycle satisfies
\[
\boxed{\mathcal A_C=0.}
\]

Hence non-zero cycle affinity is a precise obstruction to this pairwise detailed-balance representation on the declared cycle.

## Shannon–phase closure v1

Using
\[
\sigma_e
=
\log_2\frac{P_{e,+}}{P_{e,-}},
\]
the composite temporal transition link becomes
\[
L_e
=
G_e\exp\!\left[
 i\kappa\left(
 \Delta H_e+
 \log_2\frac{P_{e,+}}{P_{e,-}}
 \right)
\right].
\]
For a closed cycle,
\[
\boxed{
\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=
\gamma_B(C)+\kappa\mathcal A_C
\pmod{2\pi}.
}
\]

This is the first candidate microscopic closure of \(\sigma_e\). It is a formal information-theoretic construction. Its later identification with a physical temporal arrow requires an independent physical evidence path.

## Next derivational debt

`A0-RHO-ETA`: derive how the relational density field \(\rho_R\) and relational viscosity field \(\eta_R\) modify or generate the forward/reverse transition probabilities without defining those probabilities by hand.
