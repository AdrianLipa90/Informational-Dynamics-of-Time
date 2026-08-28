# 09A — Holonomic Spatiotemporal Offset / WARP Interface

Status: `CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This gate extends the admitted temporal-state synthesis and Spatial Offset Divergence architecture into a typed holonomic spatiotemporal-offset interface. It preserves the current dependency order and keeps the WARP interpretation at candidate status pending independent spacetime/field promotion gates.

## 1. Temporal-state input

IDT supplies the calibrated local elapsed interval

\[
\boxed{d\hat\tau=N_R\,dt,\qquad N_R>0,}
\]

with ordered state transport, bifurcation, memory lineage and retrodiction carried separately.

For two admissible histories \(\Gamma\) and \(\Gamma'\), define the calibrated temporal offset

\[
\boxed{
\Delta_{\rm TOD}(\Gamma,\Gamma')
=
\hat\tau(\Gamma')-\hat\tau(\Gamma).
}
\]

For a checkpointed lineage,

\[
\Delta^{\rm TOD}_n
=
\hat\tau_n(z')-\hat\tau_n(z),
\qquad
D_{\rm TOD}
=
\left(\sum_n |\Delta^{\rm TOD}_n|^2\right)^{1/2}.
\]

This is the temporal analogue of the existing Spatial Offset Divergence coordinate

\[
\Delta^{\rm SOD}_n=r_n(z')-r_n(z),
\qquad
D_{\rm SOD}
=
\left(\sum_n \|\Delta^{\rm SOD}_n\|^2\right)^{1/2}.
\]

The two diagnostics remain separately typed.

## 2. Canonical phase/action comparison

The spacetime phase comparison target is

\[
\boxed{
d\phi_{\rm kin}=\frac{1}{\hbar}\left(p_i\,dx^i-E\,dt\right).
}
\]

Let \(\gamma_\Gamma\) denote the geometric/connection contribution accumulated along the lifted path \(\Gamma\). The total path phase is

\[
\boxed{
\Phi_\Gamma
=
\frac{1}{\hbar}
\left(\mathbf p\!\cdot\!\Delta\mathbf x_\Gamma-E\Delta t_\Gamma\right)
+\gamma_\Gamma.
}
\]

For a phase-closed branch with winding integer \(m\),

\[
\Phi_\Gamma=2\pi m.
\]

Therefore

\[
\boxed{
\Delta t_\Gamma
=
\frac{
\mathbf p\!\cdot\!\Delta\mathbf x_\Gamma
+\hbar\gamma_\Gamma
-2\pi m\hbar
}{E}.
}
\]

This is the candidate algebraic bridge between spatial offset, temporal offset and geometric holonomy.

## 3. Holonomic displacement as horizontal-lift anholonomy

Let \(q^I\) denote internal/phase control coordinates and \(x^\mu\) the spacetime-base coordinates. Introduce a horizontal-lift connection

\[
\boxed{
\mathcal B^\mu=dx^\mu+B^\mu{}_I(q,x)\,dq^I.
}
\]

Horizontal transport satisfies

\[
\mathcal B^\mu=0.
\]

For a closed internal loop \(C_q\),

\[
q^I_{\rm final}=q^I_{\rm initial},
\]

the lifted base displacement is

\[
\boxed{
\Delta x_H^\mu
=-\oint_{C_q} B^\mu{}_I\,dq^I.
}
\]

On a surface \(\Sigma_q\) bounded by the loop, the local curvature representation is

\[
\boxed{
\Delta x_H^\mu
=-\int_{\Sigma_q}\mathcal F_B^\mu,
}
\]

with \(\mathcal F_B^\mu\) the curvature two-form of the horizontal-lift connection in the admitted local chart.

This gives the precise candidate meaning of a holonomic WARP displacement: a cyclic excursion in internal/phase coordinates closes in the control fiber while its horizontal lift accumulates a nonzero spacetime-base offset.

## 4. Spatial and temporal components of the same holonomy

Write

\[
\Delta x_H^\mu=(c\Delta t_H,\Delta\mathbf x_H).
\]

The phase-closure relation then binds the two components,

\[
\boxed{
E\Delta t_H
=
\mathbf p\!\cdot\!\Delta\mathbf x_H
+\hbar\gamma_H
-2\pi m\hbar.
}
\]

Hence a fixed holonomy class admits a spatial/temporal trade relation rather than two independent offsets.

For two path classes \(\Gamma\) and \(\Gamma'\), define the holonomic phase-offset residual

\[
\boxed{
\Delta\Phi_H
=
\frac{1}{\hbar}
\left[
\mathbf p\!\cdot\!\Delta\mathbf x_H
-E\Delta t_H
\right]
+\Delta\gamma_H.
}
\]

A checkpointed WARP/offset audit therefore carries the typed triple

```text
Spatial Offset Divergence : Delta_SOD_n
Temporal Offset Divergence: Delta_TOD_n
Holonomic phase residual  : Delta_Phi_H
```

without collapsing spatial, elapsed-time and phase information into one scalar.

## 5. Same endpoint, different history

If two histories share the same observed base endpoint while their geometric path classes differ, then

\[
\Delta\mathbf x_H=0
\]

can coexist with a nonzero geometric phase difference \(\Delta\gamma_H\). The closure equation gives the corresponding temporal offset coordinate

\[
\boxed{
\Delta t_H
=
\frac{\hbar}{E}
\left(\Delta\gamma_H-2\pi\Delta m\right).
}
\]

This is the direct holonomic mechanism by which equal spatial endpoints may retain different temporal lineage coordinates.

## 6. Relation to Retrodiction and Retrocausal Tests

Three operations remain separately typed:

1. **Retrodiction** reconstructs an earlier latent history from a retained present record.
2. **Holonomic temporal offset** compares accumulated elapsed/phase coordinates of two admissible path classes.
3. **Retrocausal Tests** apply the preregistered sealed-record protocol in which a later independently generated condition is tested against an earlier committed record after the classical-channel audit.

The physical retrocausal label is reserved for the third evidence path. A negative or path-dependent temporal offset is therefore first classified as a holonomic/temporal-lineage result and then passed through the downstream retrocausal evidence gate when the experiment satisfies that protocol.

## 7. Candidate WARP mechanism

The candidate mechanism is

\[
\boxed{
\text{internal phase/control loop}
\to
\text{connection curvature}
\to
\text{horizontal-lift holonomy}
\to
\Delta x_H^\mu
\to
(\Delta\mathbf x_H,\Delta t_H)
\to
\text{phase-closure audit}.
}
\]

IDT supplies the temporal ordering, relational lapse, phase rate, Memory lineage, SOD and Retrodiction coordinates. Physical promotion of the WARP interpretation requires the downstream spacetime connection, source/stress-energy realization, Einstein/RFC closure and empirical holonomy-displacement tests.

## 8. Immediate falsification targets

The candidate gate is rejected on its declared domain if any of the following fails:

- the phase-closure inversion does not reconstruct the supplied temporal offset;
- the spatial/temporal trade relation fails at fixed energy and holonomy;
- the calibrated elapsed-time integral fails under positive relational lapse;
- the horizontal-lift displacement depends on a pure coordinate reparameterization of the same geometric loop;
- a claimed retrocausal classification bypasses the preregistered sealed-record/classical-channel audit.

Reference implementation: `src/idt/holonomic_spatiotemporal_offset.py`.
Reference tests: `tests/reference/test_holonomic_spatiotemporal_offset.py`.
