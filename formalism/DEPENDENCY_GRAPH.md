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

The Temporal Primitive now has an explicit upstream forcing chain:
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

## Cross-repository interface branch: IDT 01X-RFC

The normalized 01D simplex state is exported to the RFC source-carrier audit through a separate interface branch:

\[
\boxed{
\text{IDT 01D normalized }p
\longrightarrow
\text{IDT 01X-RFC shape/scale interface}
\stackrel{?}{\longleftrightarrow}
\text{RFC RF-N1B2H}.
}
\]

The interface theorem is

\[
\mathcal N(Q)=\frac{Q}{Q_\Sigma},
\qquad
\mathcal H_s(Q)=\frac{s}{Q_\Sigma}Q,
\qquad
\boxed{\Delta_{\rm ext}=\left|1-\frac{s}{Q_\Sigma}\right|}.
\]

The normalized shape is preserved on every positive ray. Exact inverse transport uses the explicit scale coordinate \(s=Q_\Sigma\). RFC's continuous energy conversion combines with that scale as

\[
\boxed{
M_Q=\frac{\epsilon_QQ_\Sigma}{c^2},
\qquad
m_{Q,a}=M_Qp_a^{(Q)}.
}
\]

Status:

```text
01D normalized simplex shape                PASS
01X-RFC scale-quotient theorem              PASS
analytic extensive holonomy defect          PASS
IDT full reference suite                    PASS 337/337
RFC full reference suite                    PASS 29/29
IDT p <-> RFC p_Q physical cross-binding    OPEN
common cell/state-space transport binding   OPEN
physical source-mass coordinate M_Q         OPEN
```

### PNCS physical-law frame and executable holonomy

The interface now has a pinned execution layer in `PhaseNav-Natural-Coding-System`:

```text
PNCS_GREMLIN_NATIVE_PNV_BRIDGE_V0_2
PNCS_PNV_INFORMATION_HOLONOMY_V0_1
PNCS_PNV_SOURCE_HOLONOMY_LOOPS_V0_1
```

Pinned code snapshot:

```text
AdrianLipa90/PhaseNav-Natural-Coding-System
feat/gremlin-pnv-authoring-v0.2
5f3bf90998b8c3547d51e7c47bddaf0d6be25d60
```

The dependency relation is therefore upgraded from a document-only bridge to a connection with executable control loops:

\[
\boxed{
\text{IDT 01D/01X}
\leftrightarrow
\text{PNV physical-law frame}
\leftrightarrow
\text{RFC RF-N1B2/RF-N1B2H}.
}
\]

For a closed law path \(\gamma\), PNV records

\[
\mathcal H_\gamma=T_{n-1}\cdots T_1T_0,
\qquad
\Delta_\gamma=d\!\left(I,\mathcal H_\gamma(I)\right).
\]

The first source-law loops are:

```text
SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP
  Q_a -> (Q_Sigma,p_Q) -> Q_a'
  invariants: SOURCE.TOTAL_Q, SOURCE.PROFILE_NORM
  reference status: EXACT CONTROL LOOP

SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP
  Q_a -> n_a=Q_a/q0 -> Q_a'
  gate: q0 CONDITIONAL

SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP
  j_Q -> rho_Q=(epsilon_Q/c^2)j_Q -> j_Q'
  gate: epsilon_Q CONDITIONAL
```

The first loop is the executable control for the exact extensive/normalized factorization

\[
\boxed{Q_a=Q_\Sigma p_{Q,a}.}
\]

The next two loops become physical normalization tests when their independent input gates are admitted. Their presence in the law frame gives `q0` and `epsilon_Q` explicit dependency edges instead of hidden scale choices.

Paired validation is recorded in both repositories as

```text
validation/IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json
```

with executed reference gates:

```text
IDT Reference suite     337 passed
RFC Reference suite      29 passed
```

The PNCS native source-loop workflow is currently recorded as `CI_EXECUTION_UNRESOLVED_PRE_TEST`; its code verdict remains a separate admission gate.

The canonical Temporal Primitive → Temporal Wave admission order remains the authoritative sequential path; 01X-RFC and the PNV physical-law frame form a parallel cross-repository connection/audit branch.

The next source-normalization frontier is an independent derivation of \(\epsilon_Q\), or of \(q_0\) together with a per-carrier energy, from the admitted phase/time Hamiltonian. Any resulting normalization must be inserted as a declared PNV transport edge and audited through a closed information-holonomy loop before it advances the RFC source-coupling gate.

The next upstream Temporal Primitive gate is the nonreversible response decomposition: retain the 01C scalar contraction while separating its symmetric gradient contribution from stationary circulation in a form compatible with the 01B connection sector.

The downstream Retrodiction frontier remains preregistered adaptive global search across broader latent boxes and attractor/support regimes. Retrocausal Tests remain gated until the Retrodiction admission conditions are satisfied.
