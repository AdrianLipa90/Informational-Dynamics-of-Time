# 01B — Temporal Phase Connection Requirement

Status: `TARGETED_DERIVATION_PASS_CANDIDATE`

This gate resolves the global typing of the phase/orientation sector after 01A. The local Kähler response may use a scalar phase generator on an exact patch, while the admitted Shannon–Pancharatnam and directed-affinity primitives carry global cycle information through a U(1) connection.

## Premises inherited from 00A–00C

For an admitted edge `e:a→b`,
\[
L_e=G_e\exp\!\left[i\kappa(\Delta H_e+\sigma_e)\right],
\qquad
\kappa=\frac{\ln2}{24\pi},
\]
with Pancharatnam link \(G_e\in U(1)\), exact Shannon difference
\[
\Delta H_e=H_S(b)-H_S(a),
\]
and directed non-exact information-production increment \(\sigma_e\).

Define the discrete temporal connection phase by the edge class
\[
\boxed{\mathcal A_T(e)\equiv\operatorname{Arg}L_e\pmod{2\pi}.}
\]
An open-edge representative is gauge-covariant. Its closed-cycle holonomy is gauge-invariant.

## 1. Exact scalar increments carry zero cycle circulation

For any scalar state function \(F\),
\[
\sum_{e\in C}[F(b_e)-F(a_e)]=0
\]
on every closed directed cycle. Therefore every globally exact phase contribution has zero cycle integral.

The Shannon contribution obeys this identity exactly:
\[
\boxed{\sum_{e\in C}\Delta H_e=0.}
\]

## 2. Admitted phase data has a global connection sector

The composite cycle phase is
\[
\boxed{
\Phi_T(C)
=\operatorname{Arg}\!\left(\prod_{e\in C}L_e\right)
=\gamma_B(C)+\kappa\sum_{e\in C}\sigma_e
\pmod{2\pi}.
}
\]
Whenever \(\Phi_T(C)\neq0\), the global phase/orientation data requires a connection-level carrier whose holonomy records that cycle class.

This separates two roles:

- \(\mathcal H_\alpha\): local scalar phase generator on an exact chart or patch \(U_\alpha\);
- \(\mathcal A_T\): global connection/holonomy carrier across the admitted relational state bundle.

The 01A local response
\[
V_H=J\operatorname{grad}_{g_K}\mathcal H_\alpha
\]
is recovered on an exact patch where the phase covector is represented by \(d\mathcal H_\alpha\). Across patches and closed cycles, the connection transition data carries the additional global information.

## 3. Gauge structure

Under local phase changes \(\psi_s\mapsto e^{i\chi_s}\psi_s\),
\[
G_{a\to b}\mapsto e^{i(\chi_b-\chi_a)}G_{a\to b}.
\]
Therefore each open-edge representative changes by an endpoint phase, while
\[
\boxed{\prod_{e\in C}G_e}
\]
and hence \(\Phi_T(C)\) are invariant on a closed cycle.

The geometric sector is therefore carried by bundle connection data and its holonomy. The exact Shannon sector remains an open-edge scalar contribution. Directed non-exact affinity contributes through its cycle sum.

## 4. Consequence for the tensor–scalar Kähler architecture

The phase/orientation side of the response is typed at two compatible levels:
\[
\boxed{
\text{local: }d\mathcal H_\alpha,
\qquad
\text{global: }\mathcal A_T\text{ with holonomy }\Phi_T(C).
}
\]
Thus the Kähler response of 01A is the local exact-patch factorization, while the Berry/affinity connection supplies the global patching data already used by Temporal Wave.

The informational side is now supplied independently by 01C and 01D: 01C fixes the stationary Shannon relative-information scalar \(\mathcal I_\pi=D_{\rm KL}^{(2)}(p\|\pi)\), while 01D derives its exact symmetric Shannon–Onsager response tensor in the detailed-balance sector. This keeps scalar informational contraction and global phase circulation as separately typed ingredients of the same temporal primitive.

## 5. Evidence boundary

- exact scalar cycle cancellation: proved structurally;
- Berry cycle phase: gauge-invariant by the closed product;
- non-exact affinity contribution: inherited from 00B and tested here in the composite link;
- global connection requirement: forced for representing admitted nonzero cycle holonomy;
- local scalar \(\mathcal H_\alpha\): retained as the exact-patch generator;
- stationary informational scalar: supplied by 01C;
- exact detailed-balance symmetric response tensor: supplied by 01D;
- physical spacetime interpretation: deferred to the declared Einstein Closure.

The next upstream task is the nonreversible response decomposition coupling the 01C contraction law to the circulating connection/current sector.
