# 01AA — Noether ↔ RFC Slice-Carrier Binding

Status: `EXACT_DEFECT_THEOREM_PASS / COMMON_SLICE_BINDING_CONDITIONAL / PHYSICAL_CURRENT_IDENTITY_OPEN`

This interface follows 01Z. Its purpose is to test whether the finite Noether charge

\[
Q_\vartheta=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h
\]

and the RFC extensive carrier

\[
Q_\Sigma=\int_\Sigma j_Q\,dV_h
\]

are the same conserved carrier on one explicitly pinned slice, rather than merely two conserved quantities of compatible type.

## 1. Common cell representation

Let a common indexed partition of the selected slice be

\[
\Sigma=\bigcup_{a=1}^N C_a.
\]

The Noether representation carries slice densities and cell measures

\[
j_{\vartheta,a},\qquad V_a^{(\vartheta)}>0,
\]

while the RFC representation carries

\[
j_{Q,a},\qquad V_a^{(Q)}>0.
\]

The two discretizations must refer to the same cell IDs and the same normal orientation. Their extensive charges are

\[
\boxed{
Q_\vartheta=\sum_a V_a^{(\vartheta)}j_{\vartheta,a},
\qquad
Q_\Sigma=\sum_a V_a^{(Q)}j_{Q,a}.
}
\]

The reference gate uses the positive Noether sector

\[
Q_\vartheta>0.
\]

## 2. Local current and measure defects

Define the normalized current mismatch

\[
\boxed{
\Delta_J
:=
\frac{\sum_a V_a^{(Q)}\,|j_{Q,a}-j_{\vartheta,a}|}{Q_\vartheta}
}
\]

and the normalized measure mismatch

\[
\boxed{
\Delta_V
:=
\frac{\sum_a |V_a^{(Q)}-V_a^{(\vartheta)}|\,|j_{\vartheta,a}|}{Q_\vartheta}.
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

## 3. Exact defect theorem

Cellwise,

\[
V_a^{(Q)}j_{Q,a}-V_a^{(\vartheta)}j_{\vartheta,a}
=
V_a^{(Q)}(j_{Q,a}-j_{\vartheta,a})
+
(V_a^{(Q)}-V_a^{(\vartheta)})j_{\vartheta,a}.
\]

Therefore the triangle inequality gives

\[
\boxed{
\Delta_\Sigma\le \Delta_J+\Delta_V.
}
\]

This is exact for the stated finite-cell representation.

Consequently,

\[
\Delta_J=0,
\qquad
\Delta_V=0
\]

implies

\[
\boxed{Q_\Sigma=Q_\vartheta.}
\]

On every cell with nonzero Noether support, zero local defects also bind the current density and measure representation used by the extensive carrier.

## 4. Global equality is a weaker condition

The converse is intentionally not used as an admission rule. It is possible to have

\[
Q_\Sigma=Q_\vartheta
\]

while nonzero cellwise current errors cancel in the sum. Hence

\[
\boxed{
\Delta_\Sigma=0
\not\Rightarrow
\Delta_J=0.
}
\]

The physical carrier gate therefore requires local current/measure control, not only equality of integrated totals.

## 5. Normalized profile consequence

On the positive sector define

\[
p_{\vartheta,a}
=
\frac{V_a^{(\vartheta)}j_{\vartheta,a}}{Q_\vartheta},
\qquad
p_{Q,a}
=
\frac{V_a^{(Q)}j_{Q,a}}{Q_\Sigma}.
\]

Under exact local current and measure binding,

\[
\boxed{p_{Q,a}=p_{\vartheta,a}.}
\]

Thus 01AA supplies the missing current/measure bridge needed before the existing normalized RFC profile can be compared physically with the IDT normalized state.

## 6. Relation to 01Z and epsilon

01Z supplies the finite Noether carrier candidate

\[
Q_\vartheta^{EB}
=I_A D_\tau\chi
\]

and

\[
\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}}.
\]

Once 01AA admits

\[
Q_\Sigma\leftrightarrow Q_\vartheta^{EB},
\]

the RFC energy-per-carrier coordinate receives the same carrier normalization:

\[
\boxed{
\epsilon_Q\leftrightarrow\epsilon_N^{EB}
}
\]

and therefore

\[
\boxed{
\epsilon_Q Q_\Sigma
=H_\Phi^{EB}
}
\]

on the bound sector.

## 7. Conservation and side-flux gate

The equality is evaluated on one common slice. Propagating it between slices additionally requires the already stated conservation/boundary conditions:

\[
\nabla_\mu J_\vartheta^\mu=0,
\qquad
\nabla_\mu J_Q^\mu=0,
\]

with vanishing side flux, periodic boundary conditions, or sufficient decay for the selected spacetime slab.

The reference gate therefore records separately:

```text
same cell IDs / partition             REQUIRED
same normal orientation               REQUIRED
Noether cell measures > 0             REQUIRED
RFC cell measures > 0                 REQUIRED
Q_theta > 0                           REQUIRED
Delta_J                               MEASURED
Delta_V                               MEASURED
Delta_Sigma                           MEASURED
Delta_Sigma <= Delta_J + Delta_V      EXACT THEOREM
cross-slice persistence               BOUNDARY-CONDITIONED
physical J_Q^mu <-> J_theta^mu        OPEN
```

## 8. Advancement

```text
01Z finite Noether carrier Q_theta                 PASS_CONDITIONAL
finite-cell charge construction                    PASS
local current/measure defect decomposition         PASS EXACT
Delta_Sigma <= Delta_J + Delta_V                   PASS EXACT
zero local defects -> Q_Sigma=Q_theta              PASS CONDITIONAL
Q_Sigma=Q_theta alone -> local current identity    REJECTED AS INSUFFICIENT
Q_Sigma <-> Q_theta physical carrier identity      OPEN measured binding
p_Q <-> p_theta after exact local binding           PASS CONDITIONAL
p_IDT <-> p_theta physical state-space binding     OPEN
```

The next executable PNCS gate should carry the same three defects through a closed Noether ↔ RFC slice-carrier holonomy loop.
