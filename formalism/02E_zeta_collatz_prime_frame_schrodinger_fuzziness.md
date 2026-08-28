# 02E — Zeta–Collatz Prime Frames and Schrödinger Temporal Fuzziness

Status: `CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This layer tests a discrete-to-continuous realization of the Temporal Wave stack. Prime-indexed Collatz lineages define a discrete frame carrier. The prime frequencies inherited from the zeta factor `p^{-s}` define a diagonal Hermitian spectral generator. A symmetric Collatz-lineage overlap Laplacian couples the frames. The resulting self-adjoint operator generates unitary amplitude spreading with respect to the already derived intrinsic temporal coordinate `Theta`.

The physical identification of these mathematical frames with microscopic temporal frames remains a downstream evidence gate.

## 1. Prime-indexed frame carrier

Choose a finite audited prime set

\[
\mathcal P_N=\{p_1,\ldots,p_N\}.
\]

For every admitted prime seed, compute a finite verified Collatz lineage

\[
\boxed{
\mathcal C(p)
=(p,C(p),C^2(p),\ldots,1),
}
\]

with

\[
C(n)=
\begin{cases}
n/2,&n\equiv0\pmod2,\\
3n+1,&n\equiv1\pmod2.
\end{cases}
\]

The reference implementation admits a frame only after the declared finite orbit reaches the terminal anchor inside the explicit step budget.

Define the discrete frame basis

\[
\boxed{
\mathcal H_F
=\operatorname{span}\{|F_{p_1}\rangle,\ldots,|F_{p_N}\rangle\}.
}
\]

Each frame therefore carries

```text
prime label          p_k
Collatz lineage      C(p_k)
Collatz edge set     E_C(p_k)
prime spectral freq  ln p_k
intrinsic anchor     Theta_k [supplied by 00E/00F when bound to temporal history]
```

This is the candidate Zeta–Collatz prime-frame carrier.

## 2. Zeta prime-frequency generator

For one prime contribution to the complex-power structure,

\[
\boxed{
z_p(\sigma,\tau)=p^{-\sigma-i\tau}
=p^{-\sigma}e^{-i\tau\ln p}.}
\]

Differentiation with respect to the spectral ordinate gives the exact identity

\[
\boxed{
i\,\partial_\tau z_p=(\ln p)z_p.}
\]

Hence on the finite prime-frame basis define

\[
\boxed{
D_\zeta
=\operatorname{diag}(\ln p_1,\ldots,\ln p_N).
}
\]

The centred version

\[
\boxed{
\widetilde D_\zeta
=D_\zeta-\frac{\operatorname{tr}D_\zeta}{N}I
}
\]

removes the common global phase while preserving every relative prime-frequency difference.

The TIR zeta-information axis supplies the independent critical-axis and normalized recurrence context; the present gate uses only the finite prime-frequency identity above as its exact zeta input. Zeta-zero resonance assignments remain separately typed candidates.

## 3. Collatz frame overlap geometry

For each frame define the directed Collatz transition-edge set

\[
E_i:=E_C(p_i).
\]

For two frames define the symmetric overlap weight

\[
\boxed{
w_{ij}
=\frac{|E_i\cap E_j|}{\sqrt{|E_i||E_j|}},
\qquad
w_{ij}=w_{ji}\in[0,1].
}
\]

Set \(w_{ii}=0\). Let

\[
W_C=(w_{ij}),
\qquad
D_C=\operatorname{diag}\left(\sum_j w_{ij}\right).
\]

The Collatz frame Laplacian is

\[
\boxed{
L_C=D_C-W_C.
}
\]

Because \(W_C\) is real symmetric with nonnegative weights,

\[
\boxed{L_C=L_C^\dagger,\qquad L_C\succeq0.}
\]

This gives the discrete frame geometry independently of a continuum coordinate.

## 4. Zeta–Collatz frame Hamiltonian

Define the intrinsic-unit candidate

\[
\boxed{
H_{\zeta C}
=\alpha_\zeta\widetilde D_\zeta
+g_C L_C,
\qquad
\alpha_\zeta,g_C\in\mathbb R.
}
\]

Both terms are Hermitian, therefore

\[
\boxed{H_{\zeta C}=H_{\zeta C}^\dagger.}
\]

The two terms have distinct roles:

```text
prime/zeta sector  : relative ln(p) spectral phase rates
Collatz sector     : coupling geometry between discrete prime frames
```

The relative normalization \(\alpha_\zeta/g_C\) is an explicit model coordinate to be constrained by later derivation or evidence.

## 5. Schrödinger flow in derived intrinsic time

00E and 00F already provide the intrinsic accumulated coordinate

\[
\Theta(P)=\sum_e\theta(e),
\qquad
\theta(e)>0.
\]

Use this derived coordinate as the evolution parameter of the frame amplitude:

\[
\boxed{
i\frac{\partial}{\partial\Theta}|\psi(\Theta)\rangle
=H_{\zeta C}|\psi(\Theta)\rangle.
}
\]

In intrinsic units the exact finite-dimensional propagator is

\[
\boxed{
U_{\zeta C}(\Delta\Theta)
=e^{-iH_{\zeta C}\Delta\Theta}.
}
\]

Self-adjointness gives

\[
\boxed{
U_{\zeta C}^\dagger U_{\zeta C}=I,
}
\]

so frame probability is conserved:

\[
\boxed{
\sum_k|\psi_k(\Theta)|^2=1.
}
\]

For \(g_C=0\), a basis-frame input retains its basis populations and only accumulates prime-frequency phases. For \(g_C\ne0\), Collatz overlap permits coherent amplitude transfer between frames.

## 6. Discrete frame blur

For normalized amplitudes define

\[
\boxed{
P_k(\Theta)=|\psi_k(\Theta)|^2.
}
\]

A sharp frame has

\[
P_k=\delta_{kk_0}.
\]

Define the frame participation number

\[
\boxed{
N_{\rm eff}(\Theta)
=\frac{1}{\sum_kP_k(\Theta)^2}.
}
\]

Then

\[
N_{\rm eff}=1
\]

for one sharp frame, while coherent spreading across the frame basis gives

\[
N_{\rm eff}>1.
\]

This is the first discrete measure of temporal-frame fuzziness.

## 7. Continuous fuzzy temporal field

Let the prime frames be bound to strictly ordered intrinsic anchors from 00F,

\[
\boxed{
\Theta_1<\Theta_2<\cdots<\Theta_N.
}
\]

Introduce localized normalized frame packets

\[
\boxed{
g_k(\vartheta)
=(\pi\epsilon^2)^{-1/4}
\exp\left[-\frac{(\vartheta-\Theta_k)^2}{2\epsilon^2}\right],
\qquad\epsilon>0.
}
\]

The continuous reconstructed temporal amplitude is

\[
\boxed{
\Psi_T(\vartheta;\Theta)
=\frac{1}{\mathcal N(\Theta)}
\sum_{k=1}^N\psi_k(\Theta)g_k(\vartheta),
}
\]

with normalization chosen so that

\[
\int|\Psi_T|^2d\vartheta=1.
\]

Define

\[
\boxed{
\rho_T(\vartheta;\Theta)
=|\Psi_T(\vartheta;\Theta)|^2.
}
\]

This is the candidate smooth temporal fuzziness field generated from discrete prime/Collatz frames by the Zeta–Collatz Schrödinger flow and localized frame reconstruction.

Its mean and width are

\[
\boxed{
\bar\vartheta
=\int\vartheta\rho_Td\vartheta,
}
\]

\[
\boxed{
\sigma_T^2
=\int(\vartheta-\bar\vartheta)^2\rho_Td\vartheta.
}
\]

The pair

\[
\boxed{(N_{\rm eff},\sigma_T)}
\]

separates discrete frame participation from continuous temporal width.

## 8. Relation to the existing Temporal Wave stack

02A already supplies the generic Hermitian gauge-covariant graph operator

\[
K_L=D_L^\dagger W D_L.
\]

02C demonstrates that heterogeneous discrete temporal cells admit a controlled long-wave continuum with effective mobility and damping coefficients. 02D demonstrates that closed-cycle holonomy enters through the gauge-invariant phase mismatch while the homogenized coefficients remain separately typed.

The present gate supplies a candidate microscopic frame carrier for that architecture:

\[
\boxed{
\text{PRIMES}
\to
\text{COLLATZ LINEAGES}
\to
\text{DISCRETE FRAME GRAPH}
\to
H_{\zeta C}
\to
U_{\zeta C}(\Theta)
\to
\rho_T(\vartheta;\Theta).
}
\]

The continuum Temporal Wave sector may therefore be tested as the coarse-grained limit of the prime-frame carrier rather than introduced only as an abstract periodic cell.

## 9. Circularity firewall

The dependency direction for this candidate is

```text
00E/00F derived Theta and precedence
        +
finite prime labels / verified Collatz lineages / zeta prime-frequency identity
        ->
H_zetaC
        ->
unitary frame spreading
        ->
continuous fuzzy temporal reconstruction
```

Physical seconds enter only through the downstream clock-calibration layer. Zeta-zero resonance, critical-axis physical identification, microscopic prime-frame identification and universal Collatz completion each retain their explicit downstream evidence gates.

## 10. Immediate falsification gates

The candidate fails its declared algebraic/reference gate if any of the following occurs:

- the Collatz overlap matrix is asymmetric;
- the frame Laplacian or `H_zetaC` is non-Hermitian beyond numerical tolerance;
- the propagator fails norm conservation;
- `g_C=0` changes basis-frame populations;
- a connected `g_C>0` reference case cannot spread a sharp frame amplitude;
- the continuous temporal field fails finite normalization;
- frame permutation changes invariant spectra or reconstructed observables after the same permutation is applied to all frame data;
- an unverified Collatz orbit is silently admitted as a frame.

Reference implementation: `src/idt/zeta_collatz_temporal_fuzziness.py`.
Reference tests: `tests/reference/test_zeta_collatz_temporal_fuzziness.py`.
Validation receipt: `validation/ZETA_COLLATZ_TEMPORAL_FUZZINESS_V0_1.json`.
