# 05C — Relational Lapse from Activity-Derived Temporal Measures

Status: `EXACT_POSITIVE_CLOCK_RATIO / REPARAMETERIZATION_INVARIANT / PHYSICAL_CLOCK_BINDING_CANDIDATE`

## 1. Activity-derived clock measures

00E and 05A supply the intrinsic temporal measure

\[
\boxed{
d\Theta=\mathfrak a\,d\lambda,
\qquad
\mathfrak a=W_++W_->0.
}
\]

For a local subsystem \(x\) and an admitted reference subsystem \(r\) on the same ordered relational patch,

\[
\boxed{
d\Theta_x=\mathfrak a_xd\lambda,}
\qquad
\boxed{d\Theta_r=\mathfrak a_rd\lambda.}
\]

Define the relational lapse

\[
\boxed{
N_R(x|r)
:=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

This is the native IDT clock-ratio coordinate.

## 2. Reparameterization invariance

Under an increasing relabeling \(\lambda'=f(\lambda)\), transition activities transform as one-densities,

\[
\mathfrak a'
=\mathfrak a\frac{d\lambda}{d\lambda'}.
\]

Both local and reference activities acquire the same Jacobian factor, so

\[
\boxed{
N_R'
=\frac{\mathfrak a'_x}{\mathfrak a'_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}
=N_R.
}
\]

Thus the relational lapse is an invariant ratio of intrinsic temporal measures.

## 3. Kinetic realization

For each active pair,

\[
\mathfrak a=2M\cosh(A/2),
\]

with

\[
M
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
\]

Therefore

\[
\boxed{
N_R(x|r)
=\frac{M_x\cosh(A_x/2)}
{M_r\cosh(A_r/2)}.
}
\]

Using the Shannon affinity \(A=(\ln2)\sigma\),

\[
\boxed{
N_R(x|r)
=\frac{M_x\cosh[(\ln2)\sigma_x/2]}
{M_r\cosh[(\ln2)\sigma_r/2]}.
}
\]

The lapse ratio is therefore generated from the same relational density, viscosity and transition-affinity coordinates that generate the temporal primitive.

For a fixed reference sector,

\[
\boxed{
\nabla_\mu\ln N_R
=\nabla_\mu\ln M_x
+\frac12\tanh(A_x/2)\nabla_\mu A_x.
}
\]

The mobility gradient is

\[
\boxed{
\nabla_\mu\ln M
=\frac12\nabla_\mu\ln\rho_R(a)
+\frac12\nabla_\mu\ln\rho_R(b)
-\nabla_\mu\ln\!\left(\frac{\eta_R(a)+\eta_R(b)}{2}\right).
}
\]

## 4. Clock-reference composition

For three admitted clocks \(x,r,s\),

\[
\boxed{
N_{x|s}=N_{x|r}N_{r|s}.
}
\]

Hence

\[
\boxed{
N_{x|r}N_{r|s}N_{s|x}=1.
}
\]

The logarithmic lapse

\[
\boxed{
\nu_{x|r}=\ln N_{x|r}
}
\]

is additive under reference changes,

\[
\nu_{x|s}=\nu_{x|r}+\nu_{r|s}.
\]

At a selected normalization event \(x_\star\), the local/reference clocks may be calibrated to satisfy

\[
\boxed{N_R(x_\star)=1.}
\]

while their subsequent ratio follows their relational activities.

## 5. Physical clock calibration

Let the reference temporal measure be calibrated to a physical clock coordinate \(t\) by

\[
\boxed{
dt=T_r\,d\Theta_r,
\qquad T_r>0.
}
\]

Then the local calibrated elapsed interval is

\[
\boxed{
d\hat\tau_x=N_R(x|r)\,dt.
}
\]

The corresponding length-valued temporal one-form exported to the relativistic bridge is

\[
\boxed{
\Theta_R=N_Rc\,dt.
}
\]

The calibration protocol determines \(T_r\) in physical units. The upstream clock ratio remains the activity ratio \(\mathfrak a_x/\mathfrak a_r\).

## 6. Weak relational-lapse coordinate

Near the reference clock define

\[
\boxed{
\epsilon_N=N_R-1.
}
\]

For \(|\epsilon_N|\ll1\),

\[
\ln N_R=\epsilon_N+O(\epsilon_N^2).
\]

The downstream relativistic field bridge may use the energy-per-mass coordinate

\[
\boxed{
\Phi_N=c^2\ln N_R
}
\]

and test its weak-field relation to measured gravitational observables.

## 7. Export contract

```text
local_temporal_measure      = dTheta_x = activity_x d_lambda
reference_temporal_measure  = dTheta_r = activity_r d_lambda
relational_lapse            = N_R = activity_x / activity_r > 0
reparam_invariance          = exact
composition                 = N_x|s = N_x|r N_r|s
log_lapse                   = nu = ln N_R
kinetic_realization         = [M_x cosh(A_x/2)] / [M_r cosh(A_r/2)]
fixed_reference_gradient    = grad ln N_R = grad ln M + 1/2 tanh(A/2) grad A
physical_clock_binding      = dt = T_r dTheta_r; d tau_hat_x = N_R dt
relativistic_export         = Theta_R = N_R c dt
```

## 8. Evidence boundary

The algebraic gate covers positivity, dimensionlessness, reparameterization invariance, reference-clock composition, the kinetic ratio identity and the fixed-reference gradient decomposition. Physical clock calibration, relativistic coframe binding, source equations and weak-field/full-field tests retain their downstream evidence gates.
