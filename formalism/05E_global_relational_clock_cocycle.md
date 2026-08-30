# 05E — Global Relational Clock Cocycle

Status: `EXACT_FINITE_CLOCK_COCYCLE_THEOREM / GLOBAL_POSITIVE_LAPSE_POTENTIAL_PASS_ON_CYCLE_CLOSURE / COMMON_REPARAMETERIZATION_INVARIANT / CAUSAL_TIME_FUNCTION_GATE_NEXT`

Date: 2026-08-30

## 1. Purpose

IDT 05C supplies the local relational lapse ratio

\[
\boxed{
N_{x|r}
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0
}
\]

and the exact composition law

\[
\boxed{
N_{x|s}=N_{x|r}N_{r|s}.
}
\]

05E promotes this local ratio algebra into a global synchronization certificate on a connected relational clock network.

The gate asks whether the pairwise lapse ratios arise from one positive global clock-rate potential, unique up to the already admitted common clock normalization.

## 2. Clock graph

Let

\[
G_C=(V_C,E_C)
\]

be a connected graph of admitted local clocks. An oriented edge `x <- y` carries

\[
\boxed{N_{x|y}>0.}
\]

Reversal obeys

\[
\boxed{N_{y|x}=N_{x|y}^{-1}.}
\]

For a path

\[
P:y=x_0\to x_1\to\cdots\to x_m=x
\]

define the path ratio by ordered multiplication,

\[
\boxed{
N_P=\prod_{k=0}^{m-1}N_{x_{k+1}|x_k}.
}
\]

## 3. Cycle-closure theorem

Suppose every closed oriented cycle `C` satisfies

\[
\boxed{
\prod_{e\in C}N_e=1.
}
\]

Choose one reference node `r` and set

\[
\mathfrak a_r=1.
\]

For any node `x`, choose a path `P_{r\to x}` and define

\[
\boxed{
\mathfrak a_x:=N_{P_{r\to x}}.
}
\]

If `P` and `Q` are two paths from `r` to `x`, then `P Q^{-1}` is a closed cycle. The cycle condition gives

\[
N_PN_Q^{-1}=1,
\]

hence

\[
\boxed{N_P=N_Q.}
\]

Therefore `a_x` is path independent and positive.

For every oriented edge,

\[
\boxed{
N_{x|y}=\frac{\mathfrak a_x}{\mathfrak a_y}.
}
\]

Thus the multiplicative clock cocycle is an exact coboundary.

## 4. Uniqueness up to common scale

Let `a_x` and `b_x` be two positive potentials producing the same pairwise ratios. Then

\[
\frac{a_x}{a_y}=\frac{b_x}{b_y}
\]

for every edge. Connectedness implies

\[
\boxed{b_x=\lambda a_x,\qquad \lambda>0}
\]

for all nodes.

This is exactly the normalization freedom already present in the choice of reference clock.

## 5. Additive logarithmic form

Define

\[
\ell_{x|y}:=\ln N_{x|y}.
\]

Then reversal and composition become

\[
\ell_{y|x}=-\ell_{x|y},
\qquad
\ell_{x|z}=\ell_{x|y}+\ell_{y|z},
\]

and cycle closure is

\[
\boxed{\sum_{e\in C}\ell_e=0.}
\]

The global potential is

\[
\boxed{
\phi_x:=\ln\mathfrak a_x,
\qquad
\ell_{x|y}=\phi_x-\phi_y.
}
\]

This is the discrete exact-one-form representation of the global relational lapse.

## 6. Reparameterization invariance

05C proves that for one common increasing reparameterization

\[
\lambda\mapsto\lambda'=f(\lambda),
\qquad
\frac{d\lambda'}{d\lambda}>0,
\]

every local activity rescales by the same positive factor at the comparison event,

\[
\mathfrak a_x\mapsto\mathfrak a'_x
=\frac{\mathfrak a_x}{d\lambda'/d\lambda}.
\]

Therefore

\[
\boxed{
\frac{\mathfrak a'_x}{\mathfrak a'_y}
=\frac{\mathfrak a_x}{\mathfrak a_y}
=N_{x|y}.
}
\]

The global cocycle certificate is consequently invariant under the same clock-parameter freedom as 05C.

## 7. Compatibility with temporal half-frame gluing

The existing IDT half-frame temporal-gluing module treats an ordered path of positive frame measures and conserves the total elapsed measure across interfaces.

05E extends the global consistency question from a path to a general connected graph. On a tree there are no independent cycles and one reference clock reconstructs all positive relative rates directly. When additional edges close cycles, their product-one tests are the exact obstruction checks for path-independent synchronization.

Thus

```text
half-frame/path gluing
 -> connected clock graph
 -> cycle closure
 -> global positive rate potential
```

is a compatible refinement of the existing IDT temporal-gluing line.

## 8. Continuum target

For a refining clock network, let the logarithmic edge ratio approximate a one-form `q`:

\[
\ell_{x|y}
=q_i\Delta x^i+O(|\Delta x|^2).
\]

Vanishing loop sums at leading order give the local closedness condition, while global cycle closure supplies the zero-period condition required for an exact potential on the admitted network class.

The continuum target is therefore

\[
\boxed{
q=d\phi,
\qquad
N_R=e^{\phi-\phi_r}>0.
}
\]

With the physical clock calibration inherited from 05C/01AD, the temporal coframe is

\[
\boxed{
\Theta_R=N_R c\,dt.
}
\]

## 9. Causal/global-time interface

05E certifies global synchronization of the positive lapse ratio. The next global temporal gate is the existence of a smooth temporal function `t` whose gradient is everywhere timelike on the joined TIR × IDT spacetime carrier and whose level sets provide the required global foliation/Cauchy structure for the selected sector.

That gate is typed separately because it combines temporal ordering with the global Lorentzian geometry rather than only pairwise clock ratios.

## 10. Failure witnesses

The executable gate rejects:

- nonpositive or nonfinite lapse ratios;
- a disconnected clock network when one global reference scale is requested;
- an inconsistent cycle whose multiplicative holonomy differs from one.

These are direct obstructions to one globally defined positive clock-rate potential on the declared graph.

## 11. Claim ledger

| Claim | Status |
|---|---|
| positive local ratio `N_x|y=a_x/a_y` | `PARENT 05C EXACT` |
| reciprocal edge law | `EXACT` |
| product-one cycle condition implies path independence | `EXACT GRAPH THEOREM` |
| global positive potential exists on connected consistent graph | `EXACT` |
| potential unique up to common positive scale | `EXACT` |
| log-ratio cocycle is exact | `EXACT` |
| common increasing reparameterization preserves all ratios | `PARENT 05C + EXACT` |
| incompatible cycle rejection | `EXECUTABLE` |
| disconnected-network rejection for one reference scale | `EXECUTABLE` |
| global smooth lapse continuum potential | `REFINEMENT TARGET ON REGULARITY` |
| global causal time/Cauchy foliation | `NEXT TIR × IDT × RFC GATE` |

## 12. Validation authority

Reference implementation:

`src/idt/global_relational_clock.py`

Reference tests:

`tests/reference/test_05E_global_relational_clock_cocycle.py`

Static receipt:

`validation/05E_GLOBAL_RELATIONAL_CLOCK_COCYCLE_V0_1.json`

Verdict target:

`PASS_IDT_05E_GLOBAL_RELATIONAL_CLOCK_COCYCLE`.
