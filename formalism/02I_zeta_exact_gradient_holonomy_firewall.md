# 02I — Zeta Exact-Gradient Holonomy Firewall

Status: `EXACT_THEOREM / HOLONOMY_FIREWALL`

The 02H neighboring prime-factor phase texture is an exact vertex-phase gradient. This layer records the resulting closed-cycle theorem so that a non-zero Temporal Wave holonomy cannot be introduced by merely closing an open Zeta phase path.

## 1. Vertex phase

For an ordered finite prime set and any finite real spectral ordinate `gamma`, define

\[
\boxed{
u_k(\gamma)=e^{-i\gamma\ln p_k}.}
\]

Every vertex phase has unit modulus,

\[
|u_k|=1.
\]

## 2. Exact-gradient link

The neighboring phase texture of 02H is

\[
\boxed{
L_{k,k+1}
=u_{k+1}u_k^*
=e^{-i\gamma(\ln p_{k+1}-\ln p_k)}.
}
\]

For a closed frame cycle with `u_{N+1}=u_1`, define the closing link by the same rule,

\[
L_{N,1}=u_1u_N^*.
\]

## 3. Closed-cycle theorem

The total link product is

\[
\begin{aligned}
U_\gamma
&=\prod_{k=1}^{N}L_{k,k+1}\\
&=(u_2u_1^*)(u_3u_2^*)\cdots(u_1u_N^*)\\
&=\prod_{k=1}^{N}|u_k|^2\\
&=1.
\end{aligned}
\]

Therefore

\[
\boxed{U_\gamma=1}
\]

and the corresponding closed-cycle phase is

\[
\boxed{\phi_\gamma=0\pmod{2\pi}.}
\]

This result holds for every finite real `gamma`. In particular, choosing `gamma` equal to a recorded nontrivial zeta-zero ordinate does not change the conclusion.

## 4. Gauge statement

The link field

\[
L_{ij}=u_ju_i^*
\]

is exact/pure gauge on the finite frame graph. Redistribution of vertex phases changes the local representation but cannot generate a non-trivial cycle product from this exact sector.

This matches the 02D distinction between local phase redistribution and gauge-invariant total holonomy. 02D admits a non-zero cycle holonomy only when the link connection carries a non-exact component.

## 5. Firewall consequence

The following construction is rejected as a source of non-zero Zeta holonomy:

```text
prime vertex phases
-> neighboring phase differences
-> close the same path
-> claim non-zero U(1) holonomy
```

The exact result is instead

```text
prime vertex phases
-> exact neighboring gradient
-> closed product = 1
```

A future non-zero Zeta/Collatz Temporal Wave holonomy must therefore receive an independently justified non-exact link contribution. Candidate sources may include an admitted temporal `U(1)` connection from the existing 02D stack, a genuinely edge-native Euler-factor assignment with an explicit edge-label theorem, or another closed relational connection whose cycle product is not reducible to vertex differences.

No non-exact contribution is inserted in this gate.

Reference implementation: `closed_gradient_links` and `closed_gradient_holonomy` in `src/idt/zeta_zero_collatz_phase_discriminator.py`.
Reference tests: `tests/reference/test_zeta_zero_collatz_phase_discriminator.py`.
