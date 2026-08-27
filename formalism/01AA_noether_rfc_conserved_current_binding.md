# 01AA — Noether ↔ RFC Conserved-Current Binding Interface

Status: `EXACT_DEFECT_THEOREM_PASS / COMMON_SLICE_MEASURE_ORIENTATION_EXPLICIT / LOCAL_CURRENT_BINDING_PASS_CONDITIONAL / RFC_PHYSICAL_PROMOTION_OPEN`

01AA follows 01Z and tests whether the finite Euler–Noether phase charge and the RFC extensive source carrier are the same conserved carrier on one explicitly pinned spatial slice.

The target is

\[
\boxed{
Q_\Sigma
\stackrel{?}{\longleftrightarrow}
Q_\vartheta
=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h.
}
\]

## 1. One explicit slice, orientation and cell partition

Choose one oriented spatial slice and ordered finite-cell support

\[
\Sigma=\bigcup_a C_a.
\]

The Noether representation carries

\[
j_{\vartheta,a},\qquad V_a^{(\vartheta)}>0,
\]

while RFC carries

\[
j_{Q,a},\qquad V_a^{(Q)}>0.
\]

The interface pins the same `slice_id`, normal-orientation identifier, semantic measure identifier and ordered `cell_ids` before any current promotion.

The finite positive-sector charges are

\[
\boxed{
Q_\vartheta=\sum_aV_a^{(\vartheta)}j_{\vartheta,a}>0,
\qquad
Q_\Sigma=\sum_aV_a^{(Q)}j_{Q,a}>0.
}
\]

## 2. Independent current and measure defects

Define the local-current defect

\[
\boxed{
\Delta_J
:=
\frac{\sum_aV_a^{(Q)}|j_{Q,a}-j_{\vartheta,a}|}{Q_\vartheta}
}
\]

and the charge-weighted measure defect

\[
\boxed{
\Delta_V
:=
\frac{\sum_a|V_a^{(Q)}-V_a^{(\vartheta)}|\,|j_{\vartheta,a}|}{Q_\vartheta}.
}
\]

The global extensive-charge defect is

\[
\boxed{
\Delta_\Sigma
:=
\frac{|Q_\Sigma-Q_\vartheta|}{Q_\vartheta}.
}
\]

These defects are intentionally independent coordinates. A current mismatch cannot be hidden inside a measure choice and a measure mismatch cannot be hidden inside current normalization.

## 3. Exact defect theorem

Cellwise,

\[
V_a^{(Q)}j_{Q,a}-V_a^{(\vartheta)}j_{\vartheta,a}
=
V_a^{(Q)}(j_{Q,a}-j_{\vartheta,a})
+
(V_a^{(Q)}-V_a^{(\vartheta)})j_{\vartheta,a}.
\]

The triangle inequality therefore gives

\[
\boxed{
\Delta_\Sigma\le\Delta_J+\Delta_V.
}
\]

Hence exact local current and measure binding,

\[
\Delta_J=0,
\qquad
\Delta_V=0,
\]

implies

\[
\boxed{Q_\Sigma=Q_\vartheta.}
\]

This implication is exact for the stated finite-cell representation.

## 4. Equality of totals is deliberately weaker

Local current errors can cancel after integration. For

\[
j_\vartheta=(1,3),
\qquad
j_Q=(2,2),
\qquad
V=(1,1),
\]

we have

\[
Q_\vartheta=Q_\Sigma=4,
\qquad
\Delta_\Sigma=0,
\qquad
\Delta_J=1/2.
\]

Therefore

\[
\boxed{
\Delta_\Sigma=0
\not\Rightarrow
\Delta_J=0.
}
\]

Integrated charge equality alone is never used as the physical current-admission rule.

## 5. Normalized profile consequence

On the positive sector define

\[
p_{\vartheta,a}
=\frac{V_a^{(\vartheta)}j_{\vartheta,a}}{Q_\vartheta},
\qquad
p_{Q,a}
=\frac{V_a^{(Q)}j_{Q,a}}{Q_\Sigma}.
\]

Under exact local current and measure binding,

\[
\boxed{p_{Q,a}=p_{\vartheta,a}.}
\]

Thus the same gate that closes the extensive carrier also supplies the phase-current profile needed by the later `p_IDT ↔ p_Q` physical state-space binding.

## 6. Conservation and side flux

For a world-tube between slices, both currents must satisfy the selected conservation law and one declared side-boundary convention. Carry

\[
F_{\rm side}
\]

with

\[
\boxed{\Delta_F:=|F_{\rm side}|.}
\]

Exact cross-slice persistence uses \(\Delta_F=0\), periodic boundary conditions, or the equivalent admitted sufficient-decay condition.

## 7. Consequence for epsilon

01Z supplies

\[
\epsilon_N^{EB}=\frac{H_\Phi^{EB}}{Q_\vartheta}.
\]

Once the physical current/measure identity is admitted,

\[
Q_\Sigma=Q_\vartheta,
\]

so the RFC carrier coordinate receives

\[
\boxed{
\epsilon_Q\stackrel{?}{=}\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{Q_\Sigma}.
}
\]

The corresponding extensive source-mass coordinate is

\[
\boxed{
M_N
=\frac{\epsilon_N^{EB}Q_\vartheta}{c^2}
=\frac{H_\Phi^{EB}}{c^2}.
}
\]

## 8. PNCS executable gate

Canonical semantic loop:

```text
SOURCE.PHASE_NOETHER.RFC_CONSERVED_CURRENT.ROUNDTRIP
```

Contract:

```text
PNCS_PNV_NOETHER_RFC_CURRENT_BINDING_V0_1
```

PNV audits

```text
SOURCE.NOETHER_TOTAL_CHARGE
SOURCE.RFC_TOTAL_CHARGE
SOURCE.COMMON_MEASURE_DEFECT
SOURCE.LOCAL_CURRENT_BINDING_DEFECT
SOURCE.TOTAL_CHARGE_BINDING_DEFECT
SOURCE.CURRENT_MEASURE_BOUND_MARGIN
SOURCE.NOETHER_PROFILE_NORM
SOURCE.RFC_PROFILE_NORM
SOURCE.SIDE_FLUX_DEFECT
```

The executable `Delta_bound_margin` is

\[
\max\{0,\Delta_\Sigma-(\Delta_J+\Delta_V)\}
\]

and must remain zero within the declared numerical floor.

## 9. Advancement

```text
common slice identifier                           EXPLICIT
common normal orientation                         EXPLICIT gate
common semantic measure identifier                EXPLICIT gate
ordered cell partition                            EXPLICIT gate
Delta_J                                            PASS exact audit coordinate
Delta_V                                            PASS exact audit coordinate
Delta_Sigma                                        PASS exact audit coordinate
Delta_Sigma <= Delta_J + Delta_V                  PASS EXACT THEOREM
Delta_F                                            PASS audit coordinate
zero local defects -> Q_Sigma=Q_theta             PASS CONDITIONAL
Q_Sigma=Q_theta alone -> local current identity    INSUFFICIENT
Q_Sigma <-> Q_theta physical carrier identity     OPEN measured binding
epsilon_Q <-> epsilon_N^EB                        OPEN promotion after carrier identity
p_IDT <-> p_theta physical state-space binding    OPEN
RF-N1C source coupling/universality                OPEN
```
