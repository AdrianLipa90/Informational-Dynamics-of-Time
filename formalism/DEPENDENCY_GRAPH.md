# Formal Dependency Graph

Canonical admission order:

\[
\boxed{\mathrm{TIR}\rightarrow\mathrm{Temporal\ Primitive}\rightarrow\mathrm{Temporal\ Wave}\rightarrow\mathrm{NOW}\rightarrow\mathrm{Bifurcation}\rightarrow\mathrm{Temporal\ Transport}\rightarrow\mathrm{Memory}\rightarrow\mathrm{ORCHORBITAL\ Attractors}\rightarrow\mathrm{Retrodiction}\rightarrow\mathrm{Retrocausal\ Tests}\rightarrow\mathrm{Einstein\ Closure}}
\]

A downstream layer may be explored as a candidate before its parent is admitted; its status remains provisional until the parent gate and its own admission receipt are satisfied.

| Node | Status | Notes |
|---|---|---|
| TIR entry point | `AVAILABLE` | inherited source layer |
| Temporal Primitive | `ACTIVE / RELATIONAL_TENSOR_SCALAR_FORCING_TARGETED_PASS / PHASE_CONNECTION_HOLONOMY_TARGETED_PASS / SHANNON_RELATIVE_INFORMATION_MONOTONICITY_TARGETED_PASS / SHANNON_ONSAGER_RESPONSE_TARGETED_PASS_CANDIDATE` | 01A derives scalar pace and local response typing; 01B types global orientation as connection/holonomy data; 01C fixes the dissipative scalar as stationary-reference Shannon relative information; 01D derives the exact detailed-balance Shannon–Onsager response tensor and its uniform bridge to the 02B mobility Laplacian |
| Temporal Wave | `TARGETED_DERIVATION_CONTINUUM_HOLONOMY_PASS_CANDIDATE` | gauge-covariant stiffness, relational mobility, viscosity damping, heterogeneous continuum and holonomy-shift gates recorded in 02A–02D |
| NOW | `STRUCTURAL_PASS / WAVE_ACTIVATION_TARGETED_PASS_CANDIDATE` | structural signature carrier plus wave-active realization support |
| Bifurcation | `FORMAL_CONTRACT_PASS / NOW_BRIDGE_TARGETED_PASS_CANDIDATE` | exact activity/current hyperbolic coordinates feed wave mobility and directional phase |
| Temporal Transport | `STRUCTURAL_REFERENCE_GATE_PASS / WAVE_ENERGY_TARGETED_PASS_CANDIDATE` | Cayley smooth segments and common wave-energy contraction metric |
| Memory | `INTEGRATION_PASS / TRANSPORT_BRIDGE_TARGETED_PASS_CANDIDATE` | transport/NOW-derived duration and event-gated memory receipts |
| ORCHORBITAL Attractors | `PROVISIONAL_MEMORY_EXTENSION / LINEAGE_BRIDGE_TARGETED_PASS_CANDIDATE` | active-attractor snapshot persisted for exact recall |
| Retrodiction | `PROVISIONAL_DOWNSTREAM / SPATIAL_OFFSET_DIVERGENCE_WITNESS_FOUND / ADAPTIVE_SOD_SEPARATOR_TARGETED_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN / GATED_PENDING_MEMORY_ORCHORBITAL_ADMISSION` | 07F–07N observability, exact lineage, sparse completion, SOD witness and adaptive separator gates |
| Retrocausal Tests | `GATED` | depends on admitted Retrodiction and audits |
| Einstein Closure | `DEFERRED_FINAL_GATE` | spatial closure enters at the declared final node |

The Temporal Primitive has an explicit upstream forcing chain:
\[
\boxed{
\text{relational context}
\Rightarrow
\phi=\frac{d\tau_{\rm int}}{d\lambda}
}
\]
for scalar pace,
\[
\boxed{
\mathcal I_\pi=D_{\rm KL}^{(2)}(p\|\pi),
\qquad
\mathcal I_\pi[pP]\le\mathcal I_\pi[p]
}
\]
for stationary-reference informational descent, and in the detailed-balance sector
\[
\boxed{
\dot p=-G^{(2)}_\pi(p)\nabla\mathcal I_\pi,
\qquad
G^{(2)}_\pi(p)=(\ln2)D^\top\operatorname{diag}[c_{ab}\Lambda(r_a,r_b)]D.
}
\]
At uniform symmetric equilibrium,
\[
\boxed{G^{(2)}_u(u)=\frac{\ln2}{m}K_0,}
\]
so the symmetric Shannon response and the later Temporal Wave stiffness share the same relational-mobility Laplacian. Global orientation remains carried by the 01B temporal connection and its holonomy.

## Cross-repository interface branch: IDT 01X/01Y ↔ PNCS ↔ RFC

The normalized 01D simplex state and the phase-intention source normalization are exported through a parallel cross-repository branch:

\[
\boxed{
\text{IDT 01D normalized }p
\to
\text{01X shape/scale}
\to
\text{01Y Euler-closed phase/action normalization}
\leftrightarrow
\text{PNV physical-law frame}
\leftrightarrow
\text{RFC RF-N1B2H/RF-N1B2I}.
}
\]

### 01X — normalized shape and extensive scale

\[
\mathcal N(Q)=\frac{Q}{Q_\Sigma},
\qquad
\mathcal H_s(Q)=\frac{s}{Q_\Sigma}Q,
\qquad
\boxed{\Delta_{\rm ext}=\left|1-\frac{s}{Q_\Sigma}\right|}.
\]

Exact inverse transport uses \(s=Q_\Sigma\), and RFC factorizes

\[
\boxed{Q_a=Q_\Sigma p_{Q,a}.}
\]

### 01Y — Euler closure before energy per action-charge

The phase closure is

\[
\Phi_{\rm tot}
=\Phi_{AB}+\int_\Sigma(\mathcal F_B+s_E\mathcal R_E)+\Theta_I
=2\pi(D+\epsilon_{EB}).
\]

For the next intention step,

\[
\boxed{
\theta_{I,k}^{EB}
=2\pi(D+\epsilon_{EB})
-\Phi_{AB}
-\int_\Sigma(\mathcal F_B+s_E\mathcal R_E)
-\Theta_I^{<k}.
}
\]

The closure-selected phase fixes the action charge,

\[
\boxed{J_{I,k}^{EB}=\hbar\theta_{I,k}^{EB},}
\]

and the canonical rotor supplies

\[
\boxed{
H_{\Phi,k}^{EB}
=\frac{(J_k-J_{I,k}^{EB})^2}{2I_\phi}.
}
\]

On the positive non-degenerate sector,

\[
\boxed{
\epsilon_{I,k}^{EB}
=\frac{H_{\Phi,k}^{EB}}{J_{I,k}^{EB}},
\qquad
\Delta\tau_{k,\rm eff}^{EB}
=\frac{J_{I,k}^{EB}}{H_{\Phi,k}^{EB}}
=\frac1{\epsilon_{I,k}^{EB}}.
}
\]

Thus the normalization order is

```text
Euler/Berry closure
 -> theta_I^EB
 -> J_I^EB
 -> rotor H_Phi^EB
 -> epsilon_I^EB
 -> Delta_tau_eff^EB
 -> RFC carrier/current binding
```

After the physical carrier binding \(Q_\Sigma\leftrightarrow J_I^{EB}\), the RFC candidate coordinate becomes

\[
\epsilon_Q\leftrightarrow\epsilon_I^{EB},
\qquad
\boxed{M_I=\frac{H_\Phi^{EB}}{c^2}.}
\]

A local source additionally requires

\[
\boxed{J_I^{EB}\stackrel{?}{=}\int_{\Sigma_t}j_I\,dV_h.}
\]

## PNCS physical-law frame and executable holonomy

Pinned execution layer:

```text
PNCS_GREMLIN_NATIVE_PNV_BRIDGE_V0_2
PNCS_PNV_INFORMATION_HOLONOMY_V0_1
PNCS_PNV_SOURCE_HOLONOMY_LOOPS_V0_1
```

Pinned source-normalization snapshot:

```text
AdrianLipa90/PhaseNav-Natural-Coding-System
feat/gremlin-pnv-authoring-v0.2
e6d5e217aeed2906372fdd0aa41845f0df32bbae
```

For a closed law path \(\gamma\),

\[
\mathcal H_\gamma=T_{n-1}\cdots T_1T_0,
\qquad
\Delta_\gamma=d\!\left(I,\mathcal H_\gamma(I)\right).
\]

The source-law loops are:

```text
SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP
  Q_a -> (Q_Sigma,p_Q) -> Q_a'
  invariants: SOURCE.TOTAL_Q, SOURCE.PROFILE_NORM

SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP
  Q_a -> n_a=Q_a/q0 -> Q_a'
  gate: q0 CONDITIONAL

SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP
  j_Q -> rho_Q=(epsilon_Q/c^2)j_Q -> j_Q'
  gate: epsilon_Q DOWNSTREAM CONDITIONAL CONSUMER

SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP
  Euler/Berry data
    -> theta_I^EB
    -> J_I^EB
    -> H_Phi^EB
    -> epsilon_I^EB
    -> Delta_tau_eff^EB
    -> exact reconstructed closure input
  invariants:
    SOURCE.EULER_CLOSURE_SECTOR
    SOURCE.INTENTION_ACTION_CHARGE
    SOURCE.ROTOR_PHASE_ENERGY
    SOURCE.ENERGY_PER_ACTION_CHARGE
```

The fourth loop supplies the candidate normalization upstream of the conditional RFC density conversion. The physical bridge into RFC remains explicit through the carrier/current bindings.

Paired validation is recorded in both repositories as

```text
validation/IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json
```

Latest executed reference gates on the pinned test snapshots:

```text
IDT Reference suite     348 passed, 0 failed
RFC Reference suite      40 passed, 0 failed
```

The PNCS native source-loop workflow is `CI_EXECUTION_UNRESOLVED_PRE_TEST`; the observed job has `steps=null`, so the PNCS code verdict remains a separate admission gate.

Current cross-repository frontier:

```text
Euler/Berry -> J_I^EB -> H_Phi^EB -> epsilon_I^EB   PASS / PASS_CONDITIONAL
Q_Sigma <-> J_I^EB                                   OPEN
J_I^EB <-> integral j_I dV_h                         OPEN
IDT p <-> RFC p_Q physical state-space binding       OPEN
local measure/cell transport                         OPEN
RFC source coupling/universality                     OPEN
```

The canonical Temporal Primitive → Temporal Wave admission order remains the authoritative sequential path; 01X/01Y and the PNV physical-law frame form a parallel cross-repository connection/audit branch.

The next upstream Temporal Primitive gate is the nonreversible response decomposition: retain the 01C scalar contraction while separating its symmetric gradient contribution from stationary circulation in a form compatible with the 01B connection sector.

The downstream Retrodiction frontier remains preregistered adaptive global search across broader latent boxes and attractor/support regimes. Retrocausal Tests remain gated until the Retrodiction admission conditions are satisfied.
