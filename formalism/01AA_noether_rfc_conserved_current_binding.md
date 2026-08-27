# 01AA — Noether ↔ RFC Conserved-Current Binding Interface

Status: `COMMON_SLICE_MEASURE_EXPLICIT / LOCAL_CURRENT_BINDING_PASS_CONDITIONAL / TOTAL_CHARGE_BINDING_PASS_CONDITIONAL / RFC_PHYSICAL_PROMOTION_OPEN`

01AA follows 01Z and tests the physical carrier identity at the local-current level before promoting the integrated charge identity.

The target is

\[
\boxed{
Q_\Sigma
\stackrel{?}{\longleftrightarrow}
Q_\vartheta
=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h.
}
\]

## 1. One explicit slice and cell partition

Choose one oriented spatial slice \(\Sigma\) and an ordered finite-cell partition

\[
\Sigma=\bigcup_a C_a,
\qquad
V_a:=\int_{C_a}dV_h>0.
\]

The cross-repository binding carries explicit identifiers for:

```text
slice_id
measure_id
ordered cell_ids
cell volumes V_a
```

The semantic measure identifier and ordered cell identifiers must agree exactly across the Noether and RFC representations.

For independently supplied numerical cell-volume vectors \(V_a^{(\vartheta)}\) and \(V_a^{(Q)}\), define

\[
\boxed{
\Delta_V
:=
\frac{\sum_a|V_a^{(\vartheta)}-V_a^{(Q)}|}
{\sum_aV_a^{(\vartheta)}}.
}
\]

Exact common-measure closure has \(\Delta_V=0\).

## 2. Two independently supplied local currents

The Noether side supplies the oriented normal current samples

\[
j_{\vartheta,a}
\]

from the 01Z current

\[
J_\vartheta^\mu=2A^2\partial^\mu\vartheta.
\]

The RFC side supplies its carrier-current samples

\[
j_{Q,a}.
\]

On the common cell support, define

\[
\boxed{
Q_\vartheta=\sum_aV_a j_{\vartheta,a},
\qquad
Q_\Sigma=\sum_aV_a j_{Q,a}.
}
\]

The positive source sector uses

\[
Q_\vartheta>0,
\qquad
Q_\Sigma>0.
\]

## 3. Local-current defect

The primary physical binding defect is

\[
\boxed{
\Delta_{\rm local}
:=
\frac{\sum_aV_a|j_{Q,a}-j_{\vartheta,a}|}
{Q_\vartheta}.
}
\]

This prevents promotion from equality of integrated charges alone.

A constructive witness is

\[
j_\vartheta=(1,3),
\qquad
j_Q=(2,2),
\qquad
V=(1,1).
\]

Then

\[
Q_\vartheta=Q_\Sigma=4,
\]

while

\[
\boxed{\Delta_{\rm local}=1/2.}
\]

Thus \(Q_\vartheta=Q_\Sigma\) can hold while the local-current binding fails.

## 4. Integrated-charge defect

Define

\[
\boxed{
\Delta_Q
:=
\frac{|Q_\Sigma-Q_\vartheta|}{Q_\vartheta}.
}
\]

Exact local binding implies

\[
\Delta_{\rm local}=0
\quad\Longrightarrow\quad
\Delta_Q=0
\]

on the exact common measure.

The reverse implication is not used as the admission rule.

## 5. Conservation / side-flux gate

For a world-tube between slices, RF-N1B2 conservation uses the zero-side-flux sector. Carry the side-flux coordinate

\[
F_{\rm side}
\]

with defect

\[
\boxed{\Delta_F:=|F_{\rm side}|.}
\]

Exact conservation binding uses \(\Delta_F=0\).

## 6. Consequence for epsilon

01Z already supplies the finite Noether energy coordinate

\[
\epsilon_N^{EB}=rac{H_\Phi^{EB}}{Q_\vartheta}.
\]

Once the physical current identity is admitted,

\[
Q_\Sigma=Q_\vartheta,
\]

so the downstream RFC candidate becomes

\[
\boxed{
\epsilon_Q\stackrel{?}{=}\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{Q_\Sigma}.
}
\]

No additional free normalization is introduced at this step.

The extensive source-mass coordinate remains

\[
\boxed{
M_N
=\frac{\epsilon_N^{EB}Q_\vartheta}{c^2}
=\frac{H_\Phi^{EB}}{c^2}.
}
\]

## 7. PNCS executable gate

Pinned semantic loop:

```text
SOURCE.PHASE_NOETHER.RFC_CONSERVED_CURRENT.ROUNDTRIP
```

Contract:

```text
PNCS_PNV_NOETHER_RFC_CURRENT_BINDING_V0_1
```

The PNV state carries two independently supplied local-current arrays and two explicit measure descriptions. It audits

```text
SOURCE.NOETHER_TOTAL_CHARGE
SOURCE.RFC_TOTAL_CHARGE
SOURCE.COMMON_MEASURE_DEFECT
SOURCE.LOCAL_CURRENT_BINDING_DEFECT
SOURCE.TOTAL_CHARGE_BINDING_DEFECT
SOURCE.SIDE_FLUX_DEFECT
```

The current binding fails closed if local-current equality, integrated-charge equality, common-measure agreement, or the declared side-flux gate is violated.

## 8. Advancement

```text
common slice identifier                           EXPLICIT
common semantic measure identifier                EXPLICIT gate
ordered cell partition                            EXPLICIT gate
cell-volume defect Delta_V                        PASS as audit coordinate
local-current defect Delta_local                  PASS as audit coordinate
total-charge defect Delta_Q                       PASS as audit coordinate
zero-side-flux defect Delta_F                     PASS as audit coordinate
Q_Sigma <-> Q_theta                               PASS_CONDITIONAL at zero defects
epsilon_Q <-> epsilon_N^EB                        OPEN physical promotion after carrier identity
RF-N1C source coupling/universality                OPEN
```
