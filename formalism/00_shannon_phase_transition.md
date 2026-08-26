# 00A — Shannon–Phase Transition Core

Status: `FORMAL_CANDIDATE_WITH_PROVED_STRUCTURAL_IDENTITIES`

This layer is upstream of metric time and spacetime. A relational state `s` carries two typed objects:

1. a probability distribution
   \[
   p(s)=(p_1,\ldots,p_m),\qquad p_i\ge 0,\qquad \sum_i p_i=1,
   \]
2. a normalized complex state representative
   \[
   \psi(s)\in\mathbb C^m,\qquad \langle\psi|\psi\rangle=1.
   \]

The Shannon entropy in bits is
\[
H_S(s)=-\sum_i p_i(s)\log_2 p_i(s).
\]

For an admitted directed transition `e:a→b`, define the exact state-function difference
\[
\Delta H_e=H_S(b)-H_S(a).
\]

## Geometric phase link

Whenever \(\langle\psi_a|\psi_b\rangle\neq0\), define the normalized Pancharatnam link
\[
G_e
=
\frac{\langle\psi_a|\psi_b\rangle}
{|\langle\psi_a|\psi_b\rangle|}
\in U(1).
\]

Under local phase changes \(\psi_s\mapsto e^{i\chi_s}\psi_s\),
\[
G_{a\to b}\mapsto e^{i(\chi_b-\chi_a)}G_{a\to b}.
\]
Therefore an individual open-edge phase is gauge-covariant, while the ordered product around a closed cycle is gauge-invariant.

## Candidate composite temporal link

Introduce a transition-associated non-exact information-production increment \(\sigma_e\). Its microscopic derivation is intentionally left open at this stage. Define
\[
\boxed{
L_e
=
G_e\exp\!\left[i\kappa\left(\Delta H_e+\sigma_e\right)\right],
\qquad
\kappa=\frac{\ln2}{24\pi}.
}
\]

The phase weight of the admitted transition is
\[
q_e=\operatorname{Arg}L_e.
\]
This can feed the existing atomic transition measure
\[
\mathcal K_T=\sum_e q_e\,\delta_{s_e}.
\]

## Theorem T003 — exact Shannon differences telescope

For any closed directed cycle \(C=(s_0\to s_1\to\cdots\to s_N=s_0)\),
\[
\sum_{e\in C}\Delta H_e=0.
\]

### Proof

By definition,
\[
\sum_{n=0}^{N-1}[H_S(s_{n+1})-H_S(s_n)]
=H_S(s_N)-H_S(s_0)=0.
\]
\(\square\)

## Corollary — state entropy alone cannot generate temporal circulation

If \(\sigma_e=0\) on every edge, then
\[
\prod_{e\in C}L_e=\prod_{e\in C}G_e.
\]
Thus an exact Shannon state-function difference can modify an open transition phase, but it cannot create an additional closed-cycle phase by itself.

This is a structural no-go result for any construction that attempts to obtain non-zero temporal circulation solely from \(H_S(b)-H_S(a)\).

## Theorem T006 — non-exact information production survives cycle closure

For a closed cycle,
\[
\boxed{
\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=
\gamma_B(C)
+
\kappa\sum_{e\in C}\sigma_e
\pmod{2\pi},
}
\]
where
\[
\gamma_B(C)=\operatorname{Arg}\!\left(\prod_{e\in C}G_e\right)
\]
is the discrete geometric holonomy.

Hence the formalism separates two typed contributions:

- geometric phase/holonomy from the complex state bundle;
- non-exact information production from the directed transition structure.

The exact Shannon potential remains present on open edges but disappears under closed-cycle summation.

## First candidate closure of `A0-SIGMA`

The companion layer `00B_transition_affinity.md` defines the first explicit path-level closure
\[
\sigma_{a\to b}=\log_2\frac{P(b\mid a)}{P(a\mid b)}.
\]
The remaining debt is upstream: derive the forward/reverse transition weights from relational density, viscosity, and later dynamical fields rather than assigning them by hand.
