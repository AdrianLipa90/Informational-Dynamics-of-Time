# 05D — Local Clock Relative-Entropy Potential

Status: `EXACT_CONDITIONAL_MEMORYLESS_CLOCK_REALIZATION / SHANNON_KL_GATE / NON_ENERGY_CARRIER`

This gate starts only from the already promoted IDT activity-derived temporal primitive and an explicit local stochastic realization. It does not assume any external kinetic-energy formula.

00E supplies the positive local temporal activity

\[
\mathfrak a=W_++W_->0
\]

and the relational lapse

\[
\boxed{N_R(x|r)=\frac{\mathfrak a_x}{\mathfrak a_r}>0.}
\]

The additional realization admitted in this gate is local, constant-activity and memoryless on one comparison patch.

## 1. Local memoryless clock realization

For a positive constant activity `a`, define the normalized holding-interval density

\[
\boxed{p_{\mathfrak a}(s)=\mathfrak a e^{-\mathfrak a s},\qquad s\ge0.}
\]

This is a stochastic realization of a locally constant activity carrier. The exact IDT duration and lapse algebra of 00E/05C remains the parent structure; memorylessness is an additional typed realization gate.

## 2. Reference-to-local KL divergence

For reference activity `a_r` and local activity `a_x`,

\[
D_{KL}(p_{\mathfrak a_r}\|p_{\mathfrak a_x})
=\int_0^\infty p_{\mathfrak a_r}(s)
\ln\frac{p_{\mathfrak a_r}(s)}{p_{\mathfrak a_x}(s)}\,ds.
\]

Using

\[
\mathbb E_{p_{\mathfrak a_r}}[s]=\frac1{\mathfrak a_r},
\]

one obtains exactly

\[
D_{KL}(p_{\mathfrak a_r}\|p_{\mathfrak a_x})
=\ln\frac{\mathfrak a_r}{\mathfrak a_x}
-1+\frac{\mathfrak a_x}{\mathfrak a_r}.
\]

Since

\[
N_R=\frac{\mathfrak a_x}{\mathfrak a_r},
\]

this becomes

\[
\boxed{
\Phi(N_R)
:=D_{KL}(p_{\mathfrak a_r}\|p_{\mathfrak a_x})
=N_R-1-\ln N_R.
}
\]

Thus the scalar generator

\[
\boxed{\Phi(x)=x-1-\ln x,\qquad x>0}
\]

is obtained directly from Shannon relative information on the admitted local memoryless clock realization.

## 3. Reverse orientation

Reversing the ordered clock comparison gives

\[
D_{KL}(p_{\mathfrak a_x}\|p_{\mathfrak a_r})
=\frac1{N_R}-1+\ln N_R
=\Phi(N_R^{-1}).
\]

Hence the directional pair is

\[
\boxed{
\mathcal I_{r\to x}=\Phi(N_R),
\qquad
\mathcal I_{x\to r}=\Phi(N_R^{-1}).
}
\]

The symmetrized divergence is

\[
\boxed{
\mathcal J(N_R)
=\Phi(N_R)+\Phi(N_R^{-1})
=N_R+N_R^{-1}-2.
}
\]

## 4. Exact properties

For `x>0`,

\[
\Phi(1)=0,
\qquad
\Phi'(x)=1-\frac1x,
\qquad
\Phi''(x)=\frac1{x^2}>0.
\]

Therefore the reference clock is the unique minimum and

\[
\boxed{\Phi(x)\ge0}
\]

with equality exactly at `x=1`.

For `x=1+epsilon`,

\[
\boxed{
\Phi(1+\epsilon)
=\frac12\epsilon^2-\frac13\epsilon^3+\frac14\epsilon^4+O(\epsilon^5).
}
\]

The Hessian at the reference point is unity,

\[
\boxed{\Phi''(1)=1,}
\]

so the local quadratic term is the one-dimensional Fisher metric of this exponential family.

## 5. Reparameterization compatibility

00E/05C gives common positive reparameterization scaling on one comparison patch,

\[
\mathfrak a_x\mapsto q\mathfrak a_x,
\qquad
\mathfrak a_r\mapsto q\mathfrak a_r,
\qquad q>0.
\]

The ratio `N_R` is unchanged, hence

\[
\boxed{\Phi(N_R)\mapsto\Phi(N_R).}
\]

The relative-information clock potential therefore inherits the exact clock-ratio reparameterization invariance.

## 6. Information-geometric crosslink

RFC RF-L4A already uses natural-log KL relative information and its Fisher Hessian. The 05D exponential-clock family supplies a one-dimensional positive-rate submanifold whose exact KL generator is `Phi(N)` and whose local Fisher metric is `dN^2/N^2`.

This produces the typed bridge

```text
IDT positive activity
 -> local memoryless clock realization
 -> exponential-family KL
 -> Phi(N)=N-1-ln N
 -> local Fisher metric 1/N^2
 -> RFC information geometry
```

## 7. Evidence and promotion boundary

The exact KL calculation, positivity, convexity, reverse-orientation law, Fisher Hessian and common-scale invariance are algebraic consequences of the stated local memoryless realization.

The realization of the IDT traffic weights as physical memoryless holding-rate hazards is a separate empirical/model gate. The scalar `Phi(N)` is dimensionless relative information at this layer. Binding it to a physical action, Hamiltonian or energy scale is assigned downstream to the relativistic-field bridge.

Reference implementation: `src/idt/local_clock_relative_entropy.py`.
Reference tests: `tests/reference/test_local_clock_relative_entropy.py`.
Validation receipt: `validation/LOCAL_CLOCK_RELATIVE_ENTROPY_V0_1.json`.
