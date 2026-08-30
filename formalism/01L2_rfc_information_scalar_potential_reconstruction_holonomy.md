# 01L2 — RFC Information-Scalar Potential Reconstruction Holonomy Bridge

Status: `RFC_RFL3_FUNCTIONAL_RECONSTRUCTION_BINDING / XI_I_LINEAGE_PRESERVED / TAU_R_ORIENTATION_PRESERVED / ALPHA_I_CALIBRATION_OPEN`

01L2 extends the 01L cross-repository interface with the RF-L2/RF-L3 dynamic-Lambda action line while preserving the original IDT information scalar and temporal holonomy coordinates.

## 1. IDT export

From 01K/01L,

\[
\boxed{
\Xi_I=\frac{\mathcal J_\pi}{\mathcal A_{\rm rel}},
\qquad [\Xi_I]=L^{-2}
}
\]

and for an admitted temporal cycle `C`,

\[
\boxed{
\tau_R(C)=\operatorname{wrap}_\pi\Phi_T(C),
\qquad h_R=e^{i\tau_R}.
}
\]

IDT therefore exports the typed pair

\[
\boxed{(\Xi_I,\tau_R)}.
\]

## 2. RFC scalar return

RF-L3 consumes the 01L information-sector family

\[
\boxed{\Lambda_I=\alpha_I\Xi_I}
\]

with dimensionless `alpha_I` and combines it with the RF-L2 action coordinate

\[
\Lambda_0=\Lambda_{ref}+\kappa_EU_L.
\]

The resulting information-sector reconstruction is

\[
\boxed{
U_I=\frac{\alpha_I}{\kappa_E}\Xi_I
}
\]

and

\[
\boxed{
\Lambda_0=\Lambda_{ref}+\alpha_I\Xi_I.
}
\]

This gives the exact cross-repository scalar roundtrip

\[
\boxed{
\Xi_I
\xrightarrow{\alpha_I}
\Delta\Lambda_I
\xrightarrow{/\kappa_E}
U_I
\xrightarrow{\kappa_E,+\Lambda_{ref}}
\Lambda_0.
}
\]

## 3. Temporal-holonomy preservation

The RFC reconstruction acts on the scalar-magnitude coordinate only. The IDT orientation coordinate is transported unchanged:

\[
\boxed{
(\Xi_I,\tau_R)
\longmapsto
(\Lambda_{ref}+\alpha_I\Xi_I,\tau_R)
\longmapsto
(U_I,\tau_R).
}
\]

Hence the 01L oriented coupling remains available with the same

\[
h_R=e^{i\tau_R}
\]

after the scalar potential reconstruction.

## 4. Differential interface

When the admitted RFC closure coordinate parameterizes the information scalar,

\[
\Xi_I=\Xi_I(\phi_L),
\]

RF-L3 returns

\[
\boxed{
U_I'(\phi_L)=\frac{\alpha_I}{\kappa_E}\Xi_I'(\phi_L),
\qquad
U_I''(\phi_L)=\frac{\alpha_I}{\kappa_E}\Xi_I''(\phi_L).
}
\]

Thus the RF-L2 stationary and local stability gates can be evaluated directly on the IDT-exported information scalar once `alpha_I` and the `phi_L` pullback are admitted.

## 5. Einstein-Bianchi transfer interface

RF-L2 supplies

\[
\kappa_E\nabla^\mu T^{\rm displayed}_{\mu\nu}=\nabla_\nu\Lambda_0.
\]

With constant `Lambda_ref` and constant `alpha_I`, RF-L3 gives

\[
\boxed{
\nabla_\nu\Lambda_0=\alpha_I\nabla_\nu\Xi_I,
}
\]

so the IDT scalar lineage enters the existing RFC transfer law as

\[
\boxed{
\kappa_E\nabla^\mu T^{\rm displayed}_{\mu\nu}
=\alpha_I\nabla_\nu\Xi_I.
}
\]

## 6. Holonomy ledger

```text
IDT Xi_I scalar lineage                         PRESERVED
IDT tau_R oriented phase                        PRESERVED
RFC Lambda0 action coordinate                   BOUND THROUGH RF-L2/RF-L3
U_I functional reconstruction                   PASS EXACT GIVEN alpha_I
Bianchi derivative transfer                     PASS EXACT GIVEN RF-L2
stationary/stability pullback                    PASS EXACT
alpha_I physical calibration                    OPEN
parameter-free alpha_I derivation               OPEN
phi_L <-> Xi_I physical pullback attribution    OPEN
```

## 7. Cross-repository advancement

01L originally required an RFC derivation or bound for the scalar-field coupling into `Lambda_R`. RF-L3 advances that requirement by isolating the coupling into one explicit dimensionless coefficient `alpha_I` and closing the functional potential reconstruction around it.

The next joint gate is therefore the physical derivation or bound for `alpha_I` together with the physical `phi_L <-> Xi_I` pullback. The scalar and temporal-orientation lineages remain separately auditable throughout that step.
