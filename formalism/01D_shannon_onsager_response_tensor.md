# 01D — Shannon–Onsager Response Tensor

Status: `TARGETED_DERIVATION_PASS_CANDIDATE`

This gate supplies an exact probability-simplex realization of the symmetric response tensor required by 01A. It begins from the Shannon relative-information scalar admitted in 01C and the relational transition kinetics already used by 00C and 02B.

## 1. Detailed-balance relational kinetics

Let \(p\) be a strictly positive probability state and let \(\pi\) be a strictly positive stationary reference. For a continuous-time generator \(Q\), assume the admitted detailed-balance sector
\[
\boxed{
\pi_a Q_{ab}=\pi_b Q_{ba}=c_{ab}>0
\qquad (a\neq b),
}
\]
with \(Q\mathbf 1=0\). Define
\[
r_a=\frac{p_a}{\pi_a}.
\]
Then the master equation may be written edgewise as
\[
\boxed{
\dot p_a=\sum_b c_{ab}(r_b-r_a).
}
\]

The scalar informational functional is the 01C quantity in bits,
\[
\boxed{
\mathcal I_\pi[p]
=D_{\rm KL}^{(2)}(p\|\pi)
=\sum_a p_a\log_2\frac{p_a}{\pi_a}.
}
\]

## 2. Logarithmic-mean identity

For positive \(x,y\), define the logarithmic mean
\[
\Lambda(x,y)=
\begin{cases}
\dfrac{x-y}{\ln x-\ln y}, & x\neq y,\\[1ex]
x, & x=y.
\end{cases}
\]
It is strictly positive and obeys the exact identity
\[
\boxed{
x-y=\Lambda(x,y)(\ln x-\ln y).
}
\]

Let \(D\) be an oriented edge-incidence matrix. The bit-gradient of relative information is
\[
\nabla_p\mathcal I_\pi
=\frac{\ln r+\mathbf 1}{\ln2}.
\]
The constant term is annihilated by \(D\).

## 3. Exact Shannon–Onsager tensor

Define the state-dependent symmetric response operator
\[
\boxed{
G^{(2)}_\pi(p)
=(\ln2)\,
D^\top
\operatorname{diag}\!\left[
 c_{ab}\,\Lambda(r_a,r_b)
\right]
D.
}
\]
Then the logarithmic-mean identity gives, without approximation,
\[
\boxed{
\dot p
=-G^{(2)}_\pi(p)\,\nabla_p\mathcal I_\pi[p].
}
\]
Thus the coordinate-covariant symmetric response type introduced in 01A has a concrete Shannon–Onsager realization on the probability simplex in the detailed-balance sector.

The information-production law follows immediately:
\[
\boxed{
\frac{d\mathcal I_\pi}{d\lambda}
=-\nabla\mathcal I_\pi^\top
G^{(2)}_\pi(p)
\nabla\mathcal I_\pi
\le0.
}
\]

## 4. Positivity, conservation null, and tangent metric

Every edge weight \(c_{ab}\Lambda(r_a,r_b)\) is positive. Therefore
\[
G^{(2)}_\pi(p)=G^{(2)}_\pi(p)^\top\succeq0.
\]
Because \(D\mathbf 1=0\),
\[
\boxed{G^{(2)}_\pi(p)\mathbf 1=0.}
\]
This null direction is the mass-conservation gauge of the probability simplex. For a connected admitted graph, the response is positive definite on the tangent quotient obtained after removing the constant covector. The corresponding metric is therefore defined on the mass-conserving tangent sector, equivalently by restricting the inverse or using the Moore–Penrose inverse on the full ambient chart.

This refines the nondegenerate metric statement of 01A for probability coordinates: the physically active response lives on the \((m-1)\)-dimensional simplex tangent space.

## 5. Exact bridge to the relational mobility Laplacian

In the zero-drive symmetric sector of 00C/02B,
\[
Q_{ab}=M_{ab}=M_{ba},
\qquad
\pi_a=u_a=\frac1m.
\]
Then
\[
c_{ab}=\frac{M_{ab}}m,
\qquad
r_a=mp_a.
\]
By homogeneity of the logarithmic mean,
\[
\Lambda(mp_a,mp_b)=m\Lambda(p_a,p_b),
\]
so
\[
\boxed{
G^{(2)}_u(p)
=(\ln2)D^\top
\operatorname{diag}\!\left[M_{ab}\Lambda(p_a,p_b)\right]D.
}
\]
At the uniform stationary state \(p=u\),
\[
\Lambda(u_a,u_b)=\frac1m,
\]
and therefore
\[
\boxed{
G^{(2)}_u(u)
=\frac{\ln2}{m}
D^\top\operatorname{diag}(M_{ab})D
=\frac{\ln2}{m}K_0.
}
\]
Thus the same relational-mobility Laplacian that becomes the untwisted Temporal Wave stiffness in 02B is the uniform-equilibrium linearization of the Shannon–Onsager information-response tensor.

Away from uniform equilibrium, the same edge skeleton is dressed by the positive logarithmic mean \(\Lambda(p_a,p_b)\).

## 6. Relation to the phase/connection sector

01C proves contraction of \(D_{\rm KL}(p\|\pi)\) for any admitted stationary Markov kernel. The exact symmetric Onsager factorization in this gate uses the detailed-balance conductances \(c_{ab}=c_{ba}\).

When admitted transition dynamics carries nonzero stationary circulation, the scalar contraction from 01C remains available, while the directional/global part is retained in the 01B connection/current sector. This preserves the typed separation between symmetric informational descent and antisymmetric/circulating orientation.

## 7. Evidence boundary

- Shannon relative-information scalar: inherited from 01C;
- exact detailed-balance gradient factorization: proved by the logarithmic-mean identity;
- symmetric positive-semidefinite response: exact;
- mass-conservation null: exact;
- tangent-space metric realization: exact for connected admitted response graphs;
- uniform bridge \(G^{(2)}_u(u)=(\ln2/m)K_0\): exact;
- nonreversible response decomposition beyond the scalar contraction law: next upstream gate;
- physical spacetime interpretation: deferred to Einstein Closure.
