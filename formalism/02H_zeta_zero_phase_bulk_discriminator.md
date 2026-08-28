# 02H — Frozen Zeta-Zero Phase × Collatz Bulk Discriminator

Status: `CANDIDATE / FROZEN_ZERO_PHASE_GATE / LOCAL_OFF_ZERO_NEUTRAL_RESULT`

02G showed that the strong joint `ln p` × first-merge signal is localized to the low-prime boundary sector. This gate replaces the raw centered `ln p` operator by phase textures evaluated at independently frozen nontrivial zeta-zero ordinates and tests whether those ordinates are distinguished from nearby off-zero frequencies in bulk prime windows.

## 1. Frozen zero ordinates

The first 20 positive ordinates are copied verbatim from the existing `secret-of-a-half` reference dataset and pinned with its source blob SHA:

```text
AdrianLipa90/secret-of-a-half
data/processed/first_20_zeta_zeros.csv
blob 9a7e7bc48dc598d080895fe179a10fe078e9b7d7
```

The IDT fixture is

```text
data/reference/riemann_zeta_zeros_first20_v0_1.csv
```

No ordinate is selected after inspecting the Collatz response.

## 2. Exact neighboring prime-factor phase

For the prime factor

\[
z_p(\sigma,\tau)=p^{-\sigma}e^{-i\tau\ln p},
\]

the phase difference between neighboring prime frames at fixed ordinate `gamma` is

\[
\boxed{
L_k(\gamma)
=\exp\{-i\gamma[\ln p_{k+1}-\ln p_k]\}.
}
\]

Exactly,

\[
\boxed{|L_k(\gamma)|=1.}
\]

This is a phase texture on the already declared Zeta-ordered local frame path. It is not assigned a nontrivial closed-cycle holonomy on the open path.

## 3. Collatz bulk observable

From 02F,

\[
M_k=\frac{1}{1+d_C(p_k,p_{k+1})}.
\]

Within each fixed prime window center and standardize the mobility vector,

\[
\widehat M_k
=\frac{M_k-\langle M\rangle}{\operatorname{sd}(M)}.
\]

Define the zero-phase/Collatz coherence

\[
\boxed{
Q_W(\gamma)
=\left|
\frac{1}{N-1}
\sum_{k=1}^{N-1}
\widehat M_k L_k(\gamma)
\right|.
}
\]

This statistic asks whether the Collatz first-merge heterogeneity is coherently aligned with the neighboring Euler-factor phase texture at the tested ordinate.

## 4. Local frequency-matched controls

For every frozen zero ordinate `gamma_n`, define the symmetric control offsets

\[
\boxed{
\Delta\gamma
\in
\{-1,-0.5,-0.25,-0.125,0.125,0.25,0.5,1\}.
}
\]

The local control mean is

\[
\overline Q_W^{\rm ctrl}(\gamma_n)
=\frac18\sum_{\delta\in\Delta\gamma}
Q_W(\gamma_n+\delta).
\]

The contrast ratio is

\[
\boxed{
R_W(\gamma_n)
=\frac{Q_W(\gamma_n)}{\overline Q_W^{\rm ctrl}(\gamma_n)}.
}
\]

Because the controls are symmetric around each `gamma_n`, they remove the smooth frequency dependence of this particular coherence statistic without fitting a control frequency to the target result.

## 5. Predeclared bulk windows

The deterministic gate uses 128-prime windows beginning at prime-sequence indices

\[
\boxed{50,100,250,500,1000.}
\]

For every one of the 20 frozen ordinates in every declared bulk window, the reference result satisfies

\[
|R_W(\gamma_n)-1|<2\times10^{-3},
\]

and for every window

\[
\boxed{
\left|
\frac1{20}\sum_{n=1}^{20}R_W(\gamma_n)-1
\right|<5\times10^{-4}.
}
\]

The observed mean ratios are approximately:

| start index | mean zero/control ratio |
|---:|---:|
| 50 | 1.00002097 |
| 100 | 1.00001225 |
| 250 | 0.99999983 |
| 500 | 1.00000141 |
| 1000 | 1.00000032 |

## 6. Verdict

The current phase-texture discriminator gives

```text
FROZEN_ZETA_ZERO_FIXTURE: PASS
EXACT_UNIT_MODULUS_PRIME_GAP_PHASE: PASS
SYMMETRIC_LOCAL_OFF_ZERO_CONTROL: PASS
BULK_ZERO_PHASE_SPECIALITY: NEUTRAL / FAIL_TO_DISCRIMINATE
ZERO_ORDINATE_PROMOTION_FROM_PHASE_TEXTURE: OPEN
```

The neutral result is retained as a boundary on the mechanism. Evaluating the exact neighboring prime-factor phase at known zero ordinates does not, under this statistic, distinguish those ordinates from their local off-zero spectral neighborhoods.

## 7. Consequence for the next operator

The next gate must use additional zeta structure rather than only the local factor phase `exp(-i gamma Delta ln p)`. Valid candidate directions are:

- the completed-function dual phase on the critical axis;
- a genuine closed `U(1)` frame cell whose edge labels are independently justified;
- a zeta-zero spectral resolvent with a separately derived coupling to the frame Hamiltonian;
- a prime/zero explicit-formula observable with convergence and regularization typed separately;
- a joint holonomy observable that survives bulk-window and marginal-preserving null controls.

The derived intrinsic evolution coordinate remains `Theta` from 00E/00F throughout.

Reference implementation: `src/idt/zeta_zero_collatz_phase_discriminator.py`.
Reference tests: `tests/reference/test_zeta_zero_collatz_phase_discriminator.py`.
