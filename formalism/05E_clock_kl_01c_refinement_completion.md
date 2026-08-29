# 05E — Clock-KL as the Refinement Completion of the 01C Shannon Relative-Information Scalar

Status: `EXACT_FINITE_01C_EMBEDDING / MONOTONE_REFINEMENT_PASS / EXPONENTIAL_CLOCK_CONTINUUM_LIMIT_PASS / 01K_NUMERATOR_TYPE_COMPLETION_PASS`

## 1. Purpose

05D derives, on the explicitly typed local memoryless-clock realization,

\[
\mathcal J_{clk}(N_R)
= D_{KL}(\operatorname{Exp}(\mathfrak a_r)\|\operatorname{Exp}(\mathfrak a_x))
= N_R-1-\ln N_R,
\qquad
N_R=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
\]

01C, by contrast, is written for a finite relational probability vector `p` and a strictly positive stationary reference `pi`. 01K then defines the natural-log information numerator

\[
\mathcal J_\pi=(\ln2)\mathcal I_\pi
\]

and exports

\[
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{rel}}.
\]

05E closes the type seam by constructing 05D as the canonical refinement completion of finite 01C states. No identification by name or analogy is used.

## 2. Finite holding-time histogram

Let

\[
f_r(t)=\mathfrak a_r e^{-\mathfrak a_r t},
\qquad
f_x(t)=\mathfrak a_x e^{-\mathfrak a_x t},
\qquad t\ge0,
\]

with `a_r>0`, `a_x>0`.

For bin width `h>0` and integer `M>=1`, define the finite partition

\[
B_k=[kh,(k+1)h),\qquad k=0,\ldots,M-1,
\]

and the tail bin

\[
B_M=[Mh,\infty).
\]

The induced finite probability vectors are

\[
\boxed{
p_k=e^{-\mathfrak a_rkh}(1-e^{-\mathfrak a_rh}),
\qquad
\pi_k=e^{-\mathfrak a_xkh}(1-e^{-\mathfrak a_xh})
}
\]

for `k<M`, with

\[
\boxed{
p_M=e^{-\mathfrak a_rMh},
\qquad
\pi_M=e^{-\mathfrak a_xMh}.}
\]

Every component is strictly positive and each vector sums exactly to one. Therefore `(p,pi)` is an admitted finite 01C probability/reference pair.

## 3. Explicit stationary 01C kernel

Define the rank-one reset kernel

\[
\boxed{P_{ij}=\pi_j.}
\]

Every row sums to one and

\[
\boxed{\pi P=\pi.}
\]

Moreover

\[
pP=\pi,
\]

so the 01C data-processing inequality gives the exact one-step contraction

\[
D_{KL}(pP\|\pi P)=0\le D_{KL}(p\|\pi).
\]

Thus every finite clock histogram used below lies inside the existing 01C stationary-reference contract.

## 4. Finite natural-log information scalar

Define

\[
\mathcal J_{h,M}
:=\sum_{k=0}^{M}p_k\ln\frac{p_k}{\pi_k}.
\]

This is exactly the natural-log form of the 01C scalar:

\[
\boxed{
\mathcal J_{h,M}
=(\ln2)\,\mathcal I_{\pi^{(h,M)}}[p^{(h,M)}].
}
\]

Hence each `J_hM` is already an 01K-compatible numerator before taking any continuum limit.

For the non-tail bins,

\[
\ln\frac{p_k}{\pi_k}
=
\ln\frac{1-e^{-\mathfrak a_rh}}
        {1-e^{-\mathfrak a_xh}}
+(\mathfrak a_x-\mathfrak a_r)kh,
\]

while for the tail bin

\[
\ln\frac{p_M}{\pi_M}
=(\mathfrak a_x-\mathfrak a_r)Mh.
\]

This gives a deterministic finite expression for the refinement sequence.

## 5. Refinement monotonicity

Let `P1` and `P2` be finite holding-time partitions with `P2` refining `P1`. The coarse histogram is obtained from the refined histogram by a deterministic stochastic coarse-graining map `C`:

\[
p^{(1)}=p^{(2)}C,
\qquad
\pi^{(1)}=\pi^{(2)}C.
\]

The 01C data-processing inequality therefore gives

\[
\boxed{
\mathcal J_{\mathcal P_1}
\le
\mathcal J_{\mathcal P_2}.
}
\]

Thus clock relative information is monotone nondecreasing under finite partition refinement.

Define the 01C refinement completion on this carrier by

\[
\boxed{
\mathcal J_{01C}^{comp}(f_r\|f_x)
:=
\sup_{\mathcal P\in\mathfrak P_{fin}}
D_{KL}(p_{\mathcal P}\|\pi_{\mathcal P}),
}
\]

where `P_fin` denotes the admitted finite measurable holding-time partitions.

This completion preserves the finite 01C lineage: every approximant is an admitted 01C scalar, and refinement order is controlled by the same data-processing theorem already used by 01C.

## 6. Exact exponential-family continuum value

For the continuous exponential carriers,

\[
\ln\frac{f_r(t)}{f_x(t)}
=
\ln\frac{\mathfrak a_r}{\mathfrak a_x}
+(\mathfrak a_x-\mathfrak a_r)t.
\]

Since

\[
\mathbb E_r[t]=\frac1{\mathfrak a_r},
\]

one obtains exactly

\[
\begin{aligned}
D_{KL}(f_r\|f_x)
&=
\ln\frac{\mathfrak a_r}{\mathfrak a_x}
+rac{\mathfrak a_x-\mathfrak a_r}{\mathfrak a_r}\\
&=
\frac{\mathfrak a_x}{\mathfrak a_r}-1
-\ln\frac{\mathfrak a_x}{\mathfrak a_r}.
\end{aligned}
\]

Therefore, with

\[
N_R=\frac{\mathfrak a_x}{\mathfrak a_r},
\]

\[
\boxed{
D_{KL}(f_r\|f_x)
=N_R-1-\ln N_R
=\mathcal J_{clk}(N_R).
}
\]

For the uniform-width infinite-bin histogram obtained after `M -> infinity`,

\[
\mathcal J_h
=
\ln\frac{1-e^{-\mathfrak a_rh}}
        {1-e^{-\mathfrak a_xh}}
+(\mathfrak a_x-\mathfrak a_r)h
\frac{e^{-\mathfrak a_rh}}
     {1-e^{-\mathfrak a_rh}}.
\]

Using

\[
1-e^{-ah}=ah+O(h^2),
\qquad
h\frac{e^{-ah}}{1-e^{-ah}}=\frac1a+O(h),
\]

one gets

\[
\boxed{
\lim_{h\to0^+}\mathcal J_h
=N_R-1-\ln N_R.
}
\]

Together with the finite-tail limit `M -> infinity`, this supplies an explicit constructive sequence of finite 01C states converging to the 05D scalar.

## 7. 01K numerator completion

01K types

\[
\mathcal J_\pi=(\ln2)\mathcal I_\pi
\]

as the dimensionless natural-log numerator of

\[
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{rel}}.
\]

05E extends that numerator by its canonical finite-partition refinement completion. On the memoryless clock carrier,

\[
\boxed{
\mathcal J_{clk}
=\mathcal J_{01C}^{comp}(f_r\|f_x).
}
\]

Therefore the clock scalar has a typed 01K numerator realization

\[
\boxed{
\Xi_{clk}
:=\frac{\mathcal J_{clk}}{\mathcal A_{rel}}
=
\frac{N_R-1-\ln N_R}{\mathcal A_{rel}}.
}
\]

This is a type-completion result for the information numerator. Selection of the physical relational area, the phase-clock cell, and the downstream coupling remain the existing 01K/RFC gates.

## 8. Reverse orientation and symmetrized completion

Interchanging local and reference clock rates gives

\[
D_{KL}(f_x\|f_r)
=N_R^{-1}-1+\ln N_R
=\Phi(N_R^{-1}).
\]

Their Jeffreys sum is

\[
\boxed{
D_{KL}(f_r\|f_x)+D_{KL}(f_x\|f_r)
=N_R+N_R^{-1}-2.
}
\]

Each orientation independently admits the same finite-histogram 01C refinement lineage.

## 9. Promotion boundary

05E closes:

```text
05D exponential clock KL
 -> finite holding-time histograms
 -> admitted finite 01C probability/reference states
 -> explicit stationary reset kernel
 -> 01C KL scalar in bits
 -> exact bit-to-nat 01K numerator
 -> monotone finite refinement
 -> canonical refinement completion
 -> J_clk = N_R - 1 - ln N_R
 -> Xi_clk = J_clk / A_rel
```

The memoryless-clock realization remains the explicit 05D physical/model domain. The physical selection of `A_rel`, coupling into the RFC scalar action, mass-scale promotion, matter-flow domain and observable assignment retain their downstream gates.

Reference implementation: `src/idt/clock_kl_01c_refinement.py`.
Reference tests: `tests/reference/test_clock_kl_01c_refinement.py`.
Validation receipt: `validation/CLOCK_KL_01C_REFINEMENT_COMPLETION_V0_1.json`.
