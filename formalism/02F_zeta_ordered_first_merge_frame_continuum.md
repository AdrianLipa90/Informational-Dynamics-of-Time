# 02F — Zeta-Ordered First-Merge Frame Continuum

Status: `CANDIDATE / FIRST_MERGE_LOCALITY_AND_HOMOGENIZATION_GATE`

This layer replaces the complete-orbit Collatz overlap as the locality carrier for the 02E frame model. The complete-orbit overlap remains a global coherent-coupling baseline. Local neighboring-frame transport is instead built from two distinct ingredients:

1. the Zeta prime factor supplies the ordered spectral coordinate `ln p`;
2. Collatz supplies the first-merge distance between neighboring prime frames.

The resulting nearest-frame path is tested against the existing one-dimensional heterogeneous Temporal Wave continuum structure.

## 1. First-merge distance

For two verified Collatz seeds `a,b`, define

\[
\boxed{
d_C(a,b)
=\min_{r,s\ge0\,:\,C^r(a)=C^s(b)}(r+s).
}
\]

Let `(r_*,s_*,m_*)` be a minimizing witness. Then

\[
C^{r_*}(a)=C^{s_*}(b)=m_*.
\]

All later common descendants belong to the shared post-merge tail. The first-merge distance therefore depends on the two pre-merge legs and does not grow with the length of the common terminal tail.

Example:

\[
3\to10\to5,
\]

so for seeds `3` and `5`,

\[
\boxed{m_*=5,\qquad d_C(3,5)=2.}
\]

This removes the complete-graph degeneracy produced by counting all shared terminal-tail edges.

## 2. Zeta ordering of prime frames

For the prime Euler-factor phase,

\[
z_p(\sigma,\tau)=p^{-\sigma}e^{-i\tau\ln p},
\]

02E established the exact spectral generator

\[
i\partial_\tau z_p=(\ln p)z_p.
\]

For increasing primes

\[
p_1<p_2<\cdots<p_N,
\]

we therefore have the strictly ordered prime-frequency sequence

\[
\boxed{
\omega_k=\ln p_k,
\qquad
\omega_1<\omega_2<\cdots<\omega_N.
}
\]

The local frame path follows this Zeta/prime ordering. Collatz is then used to set the heterogeneous coupling between consecutive frames rather than to define the one-dimensional order by itself.

## 3. Scale-free first-merge mobility

For consecutive ordered prime frames define

\[
\boxed{
d_k=d_C(p_k,p_{k+1}).}
\]

The reference mobility is

\[
\boxed{
M_k=\frac{1}{1+d_k}>0.
}
\]

This transform is monotone, bounded, positive and introduces no fitted Collatz length scale.

The finite path contains `N` frame vertices and `N-1` edge mobilities.

## 4. Hermitian nearest-frame stiffness

Normalize the finite frame interval to unit length,

\[
h=\frac{1}{N-1}.
\]

Let `D` be the nearest-neighbor incidence operator with entries

\[
(Dq)_k=\frac{q_{k+1}-q_k}{h}.
\]

Define

\[
\boxed{
K_{\zeta C}^{\rm path}
=D^\dagger\operatorname{diag}(M_k)D.
}
\]

Then exactly

\[
\boxed{
K_{\zeta C}^{\rm path}
=(K_{\zeta C}^{\rm path})^\dagger,
\qquad
K_{\zeta C}^{\rm path}\succeq0.
}
\]

The path has exactly `N-1` undirected off-diagonal couplings, replacing the dense all-to-all locality failure of the naive complete-orbit overlap.

## 5. Homogenized long-wave target

For a one-dimensional positive heterogeneous path, define the harmonic effective mobility

\[
\boxed{
M_{\rm eff}
=\left[\frac{1}{N-1}\sum_{k=1}^{N-1}\frac{1}{M_k}\right]^{-1}.
}
\]

The normalized Neumann continuum target for the low nonzero modes is

\[
\boxed{
\lambda_m^{\rm cont}
=M_{\rm eff}(\pi m)^2,
\qquad m=1,2,\ldots.
}
\]

For the discrete path eigenvalues `lambda_m`, define

\[
R_m=\frac{\lambda_m}{\lambda_m^{\rm cont}}
\]

and the first-five-mode mean absolute relative error

\[
\boxed{
E_5=\frac15\sum_{m=1}^5|R_m-1|.
}
\]

## 6. Deterministic prime-frame convergence witness

For the first `N` prime frames, the reference implementation gives:

| N | `M_eff` | `E_5` |
|---:|---:|---:|
| 64 | 0.014590088003705417 | 0.08565962761355066 |
| 128 | 0.013088735442646606 | 0.06962156645259879 |
| 256 | 0.010143601575241657 | 0.014908007099230037 |

At `N=256`, the first five mode ratios are

\[
\boxed{
(R_1,R_2,R_3,R_4,R_5)
=(0.9603624780,\ 1.0100856686,\ 0.9880357876,\ 1.0061679651,\ 0.9933153326).
}
\]

Thus the tested prime-frame path reaches a first-five-mode continuum mismatch of about `1.49%` at `N=256` under the declared mobility rule.

This is a positive coarse-graining witness for

\[
\boxed{
\text{ordered discrete prime frames}
\longrightarrow
\text{low-mode one-dimensional continuum}.
}
\]

## 7. Composite and randomized null controls

The same local-path construction is applied to non-prime Collatz seeds as an explicit null control by disabling the prime-label admission requirement while retaining the same first-merge mobility rule.

For the first 256 odd composite seeds:

\[
M_{\rm eff}=0.01070484026699131,
\]

\[
\boxed{E_5=0.02771242777487193.}
\]

Its first five ratios are

\[
(0.9796869472,\ 0.9422456197,\ 0.9744425705,\ 1.0070721994,\ 0.9721349232).
\]

Therefore low-mode homogenization is also present in the composite null.

A second null holds the prime-derived set of edge mobilities fixed and randomly permutes their path order. Deterministic permutations include cases with finite-size continuum error below the canonical prime ordering and cases above it.

The resulting status is:

```text
LOCAL_FIRST_MERGE_GEOMETRY: PASS
SPARSE_NEAREST_FRAME_PATH: PASS
PRIME_PATH_LOW_MODE_HOMOGENIZATION: PASS
COMPOSITE_PATH_HOMOGENIZATION_NULL: PASS
RANDOMIZED_ORDER_NULL_CAN_MATCH_OR_BEAT_FINITE_SIZE_ERROR: PASS
PRIME_SPECIFIC_CONTINUUM_PRIVILEGE: OPEN
```

The continuum result is therefore assigned to the positive local heterogeneous path coarse-graining. Prime labels retain their separate Zeta Euler-factor provenance from 02E; a stronger prime-specific physical role requires an independent discriminator beyond continuum emergence alone.

## 8. Relation to Schrödinger fuzziness

02E supplies the unitary frame evolution

\[
i\partial_\Theta\psi=H_{\zeta C}\psi
\]

and continuous reconstruction

\[
\rho_T(\vartheta;\Theta)=|\Psi_T(\vartheta;\Theta)|^2.
\]

02F supplies the local sparse frame geometry on which a refined Hamiltonian can act:

\[
\boxed{
H_{\zeta C}^{\rm local}
=\alpha_\zeta\widetilde D_\zeta
+g_C K_{\zeta C}^{\rm path}.
}
\]

The chain under test is therefore

\[
\boxed{
\text{prime Euler factors}
\to
\ln p\text{ frame order}
\to
d_C\text{ first-merge coupling}
\to
K_{\zeta C}^{\rm path}
\to
H_{\zeta C}^{\rm local}
\to
U(\Theta)
\to
\rho_T.
}
\]

The evolution coordinate remains the intrinsic `Theta` already derived upstream in 00E/00F.

## 9. Next gate

The next discriminator is not another continuum fit. It is a structural comparison of the **joint Zeta-frequency plus Collatz-coupling operator** against null carriers:

```text
prime Euler-factor frequencies + first-merge Collatz coupling
vs
frequency-matched composite controls
vs
permuted Collatz coupling controls
```

Required observables:

- low-mode spectral statistics;
- frame-spreading rate under the same intrinsic `Theta` interval;
- participation-number growth;
- continuous `sigma_T` growth;
- stability under increasing frame count;
- sensitivity to destroying prime-frequency/Collatz-coupling alignment while preserving one marginal at a time.

Reference implementation: `src/idt/zeta_collatz_frame_continuum.py`.
Reference tests: `tests/reference/test_zeta_collatz_frame_continuum.py`.
