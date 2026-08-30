# 05G — Relational Lapse to Temporal Foliation

Status: `LOCAL_FROBENIUS_PASS / REGULAR_LEVEL_SET_THEOREM_PASS_ON_GLOBAL_CLOCK_INPUT / GLOBAL_CLOCK_SCALAR_INPUT_OPEN / CAUCHY_GLOBAL_HYPERBOLICITY_OPEN`

Date: 2026-08-30

## 1. Purpose

This gate binds the positive relational lapse of 05C to the hypersurface geometry required by the TIR × IDT → RFC relativistic join.

The upstream chain already supplies:

```text
00E positive activity-derived elapsed increment
 -> 00F realized-history precedence and cumulative activity coordinate
 -> 05A reference-clock calibration on an ordered comparison patch
 -> 05C positive relational lapse N_R
 -> temporal coframe E^0 = Theta_R = N_R c dt
```

The remaining question is whether the temporal coframe selects codimension-one spatial leaves and what additional condition promotes the local construction to a domain-wide foliation.

## 2. Parent ledger

### 2.1 Activity-derived duration

00E gives, on each admitted realized relation,

\[
d\Theta=\mathfrak a\,d\lambda_e,
\qquad
\mathfrak a>0,
\]

where \(\lambda_e\) is an increasing local relation parameter and the product \(\mathfrak a\,d\lambda_e\) is invariant under admitted increasing reparameterization.

### 2.2 Derived precedence

00F unfolds realized histories into prefix-labelled occurrences and defines

\[
\Theta(P_k)=\sum_{r=1}^k\theta(e_r),
\qquad
\theta(e_r)>0.
\]

Hence prefix extension is embedded monotonically into \(\mathbb R\) on each realized history.

### 2.3 Clock calibration and lapse

05A/05C compare two active systems on one ordered comparison patch:

\[
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda,
\]

\[
\boxed{N_R(x|r)=\frac{\mathfrak a_x}{\mathfrak a_r}>0.}
\]

After reference-clock calibration,

\[
\boxed{dt=T_r\,d\Theta_r,\qquad T_r>0,}
\]

and the temporal coframe exported to RFC is

\[
\boxed{\Theta_R=E^0=N_R c\,dt.}
\]

## 3. Local Frobenius theorem

Let \(U\) be an admitted smooth comparison patch. Assume

\[
t\in C^2(U,\mathbb R),
\qquad
dt\neq0,
\]

and

\[
N_R\in C^1(U,\mathbb R_{>0}).
\]

Define

\[
\Theta_R=N_Rc\,dt.
\]

Because \(d^2t=0\),

\[
\begin{aligned}
d\Theta_R
&=c\,dN_R\wedge dt+N_Rc\,d(dt)\\
&=c\,dN_R\wedge dt.
\end{aligned}
\]

Therefore

\[
\begin{aligned}
\Theta_R\wedge d\Theta_R
&=N_Rc\,dt\wedge c\,dN_R\wedge dt\\
&=0.
\end{aligned}
\]

Hence

\[
\boxed{\Theta_R\wedge d\Theta_R=0.}
\]

By the codimension-one Frobenius theorem, the distribution

\[
\boxed{\mathcal H:=\ker\Theta_R}
\]

is integrable on the patch.

This result allows spatially varying relational lapse. Exactness of \(\Theta_R\) is a stronger condition than the Frobenius condition and is not required for the local foliation theorem.

## 4. Kernel invariance under positive lapse

Since \(N_Rc>0\), multiplication by the scalar factor does not change the kernel:

\[
\boxed{\ker\Theta_R=\ker dt.}
\]

Thus the lapse controls temporal scale while the calibrated clock scalar determines the local spatial-leaf distribution.

The positive sign also preserves the temporal orientation selected by increasing calibrated clock time.

## 5. Regular level-set realization

If \(dt_p\neq0\) at every point \(p\in U\), then \(t\) is a submersion on \(U\). The regular level-set theorem gives

\[
\boxed{\Sigma_s:=t^{-1}(s)}
\]

as smooth codimension-one hypersurfaces wherever the level is represented in the patch.

Their tangent spaces satisfy

\[
\boxed{T_p\Sigma_s=\ker dt_p=\ker\Theta_{R,p}.}
\]

Therefore the IDT temporal coframe and the level-set hypersurfaces select the same local spatial distribution.

## 6. Conditional domain-wide promotion

Let \(M\) be an admitted spacetime domain. If the clock calibration extends to one smooth scalar

\[
\boxed{t:M\to I\subseteq\mathbb R}
\]

with

\[
dt\neq0
\]

everywhere, and if \(N_R:M\to\mathbb R_{>0}\) is smooth, then the same calculation holds on all of \(M\):

\[
\Theta_R=N_Rc\,dt,
\qquad
\Theta_R\wedge d\Theta_R=0,
\]

and the regular level sets of \(t\) define a codimension-one foliation of the admitted domain.

The current source-owned IDT parents provide calibrated \(dt\) and \(N_R\) on common ordered comparison patches and along admitted reference-clock constructions. The domain-wide scalar extension is therefore the remaining input for global foliation promotion.

Status:

`GLOBAL_CLOCK_SCALAR_INPUT_OPEN`.

## 7. Causal completion ledger

A regular temporal foliation supplies the hypersurface geometry needed by the ADM join. Stronger global causal statements require their own gates.

The remaining causal completion targets are typed separately:

```text
regular temporal foliation                   CONDITIONAL ON GLOBAL CLOCK INPUT
Cauchy property of every admitted leaf       OPEN
intersection of every inextendible causal
curve with each Cauchy leaf                  OPEN
global hyperbolicity                         OPEN
product/splitting theorem hypotheses         OPEN
```

This separation keeps the ADM foliation theorem independent from future global-causality promotion.

## 8. TIR × IDT × RFC handoff

On a TIR spatial domain carrying the selected spatial metric \(h\), combine

\[
\Theta_R=N_Rc\,dt
\]

with

\[
\ker\Theta_R=T\Sigma_t.
\]

The local Lorentzian carrier is

\[
\boxed{g=-\Theta_R\otimes\Theta_R+h_\perp}
\]

up to the already typed shift/ADM frame representation used by RFC.

The handoff is therefore

```text
TIR spatial metric / Levi-Civita sector
 + IDT positive lapse and temporal coframe
 + calibrated clock scalar on a patch
 -> integrable spatial distribution ker(Theta_R)
 -> local ADM foliation
 -> RFC RF-E24 local Einstein-form closure
```

With a domain-wide regular clock scalar and a certified global TIR 3-manifold input, the same chain becomes eligible for a global Einstein-manifold promotion gate.

## 9. Falsification rules

The gate fails on an admitted domain if any of the following occurs:

1. \(N_R\le0\) or becomes non-finite on the target sector;
2. the calibrated clock differential vanishes at an admitted point targeted by the regular-foliation claim;
3. the temporal coframe is not proportional to the calibrated clock differential on the claimed 05C interface;
4. an explicit computation of \(\Theta_R\wedge d\Theta_R\) is nonzero on that interface;
5. a domain-wide foliation is promoted without a domain-wide regular scalar clock or an equivalent independently proved foliation structure.

## 10. Claim ledger

| Claim | Status |
|---|---|
| `N_R=a_x/a_r>0` | `PARENT IDT 05C` |
| `Theta_R=N_R c dt` | `PARENT IDT 05C` |
| `dTheta_R=c dN_R wedge dt` | `EXACT DIFFERENTIAL-FORM IDENTITY` |
| `Theta_R wedge dTheta_R=0` | `EXACT` |
| `ker Theta_R = ker dt` for positive lapse | `EXACT` |
| local hypersurface orthogonality/integrability | `STANDARD FROBENIUS THEOREM` |
| regular `t=const` hypersurfaces when `dt!=0` | `STANDARD REGULAR-LEVEL THEOREM` |
| domain-wide foliation from global regular `t` | `EXACT CONDITIONAL THEOREM` |
| source-owned global scalar clock over full target spacetime domain | `OPEN_INPUT` |
| Cauchy/global-hyperbolicity promotion | `OPEN` |

## 11. Validation authority

Reference implementation:

`src/idt/global_temporal_foliation.py`

Reference tests:

`tests/reference/test_global_temporal_foliation.py`

Static receipt:

`validation/GLOBAL_TEMPORAL_FOLIATION_V0_1.json`

Verdict target:

`PASS_IDT_LOCAL_FROBENIUS_WITH_GLOBAL_CLOCK_INPUT_OPEN`.
