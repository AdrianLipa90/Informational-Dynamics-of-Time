# 01C — Shannon Relative Information Monotonicity

Status: `TARGETED_DERIVATION_PASS_CANDIDATE`

This gate constrains the dissipative/informational scalar required by 01A directly from the upstream Shannon state and an admitted stationary relational transition kernel.

## 1. Stationary relational reference

Let
\[
p=(p_1,\ldots,p_m),\qquad p_a\ge0,\qquad \sum_a p_a=1
\]
be an admitted relational probability state. Let \(P\) be a row-stochastic transition kernel and let \(\pi\) be a strictly positive stationary relational reference,
\[
\boxed{\pi P=\pi.}
\]

Define the Shannon relative-information scalar in bits,
\[
\boxed{
\mathcal I_\pi[p]
=D_{\rm KL}^{(2)}(p\|\pi)
=\sum_{a:p_a>0}p_a\log_2\frac{p_a}{\pi_a}.
}
\]

## 2. Exact one-step monotonicity

The log-sum/data-processing inequality gives
\[
D_{\rm KL}(pP\|\pi P)\le D_{\rm KL}(p\|\pi).
\]
Using stationarity \(\pi P=\pi\),
\[
\boxed{
\mathcal I_\pi[pP]\le \mathcal I_\pi[p].
}
\]
Therefore the sign of the informational descent channel is fixed by the admitted transition dynamics once the stationary relational reference is specified.

This statement applies independently of pairwise detailed balance. A stationary nonreversible kernel may carry cyclic probability currents while relative information still contracts.

## 3. Uniform symmetric reduction

For the zero-drive symmetric kinetics of 00C/02B, the stationary reference is uniform,
\[
u_a=1/m.
\]
Then
\[
\boxed{
\mathcal I_u[p]
=D_{\rm KL}^{(2)}(p\|u)
=\log_2 m-H_S(p).
}
\]
Hence symmetric relational relaxation decreases the Shannon information deficit relative to the uniform stationary state, equivalently increasing Shannon entropy toward its stationary maximum.

This fixes the earlier sign ambiguity: the 01A descent scalar in this sector is relative information to the stationary relational reference.

## 4. Relation to nonzero cycle affinity

00B allows nonzero cycle affinity,
\[
\mathcal A_C=\sum_{e\in C}\sigma_e\ne0,
\]
which obstructs pairwise detailed balance on that cycle. The monotonicity theorem above remains available whenever the full admitted kernel has a stationary reference \(\pi\).

Thus two pieces are typed separately:

- \(\mathcal I_\pi\): scalar distance from the stationary relational reference;
- 01B \(\mathcal A_T\): connection/holonomy carrier for directional circulation.

A nonzero circulation is therefore compatible with scalar relative-information contraction.

## 5. Consequence for 01A

The informational functional required by the local tensor response has the admitted Shannon realization
\[
\boxed{
\mathcal I\longleftarrow \mathcal I_\pi=D_{\rm KL}^{(2)}(p\|\pi).
}
\]
The remaining tensor question is sharper: under what conditions does the transition dynamics factor exactly as
\[
\dot p=-G(p)\nabla\mathcal I_\pi?
\]
That exact response-tensor factorization is the separate 01D Shannon–Onsager gate.

## 6. Evidence boundary

- stationary-reference KL contraction: exact data-processing result;
- uniform identity \(D_{\rm KL}(p\|u)=\log_2m-H_S(p)\): exact;
- nonreversible stationary kernels: admitted by this scalar monotonicity gate;
- exact symmetric Onsager tensor: deferred to 01D;
- directional holonomy: retained in 01B;
- physical spacetime interpretation: deferred to Einstein Closure.
