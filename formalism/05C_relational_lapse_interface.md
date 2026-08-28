# 05C — Relational Lapse from Internal Elapsed-Activity Ratios

Status: `EXACT_POSITIVE_CLOCK_RATIO / REPARAMETERIZATION_INVARIANT / PHYSICAL_PROPER_TIME_BINDING_CANDIDATE`

## 1. Purpose

IDT already supplies a positive system-internal elapsed one-form before spacetime closure,

\[
\boxed{
d\tau_{\rm int}=\phi\,d\lambda,
\qquad
\phi:=\frac{\mathfrak a}{\mathfrak a_\star}>0.
}
\]

RF-02I shows that a constant temporal lapse cannot produce the Newtonian slow-motion acceleration term. This gate therefore asks for the minimal lapse-like object already available inside IDT, without importing a gravitational potential or an Einstein metric.

The answer is a ratio of two admitted positive elapsed-activity one-forms.

## 2. Local and reference elapsed clocks

Let one local relational subsystem carry

\[
\boxed{
d\tau_x=\phi_x\,d\lambda,
\qquad \phi_x>0,
}
\]

and let an admitted reference subsystem/clock carry

\[
\boxed{
d\tau_{\rm ref}=\phi_{\rm ref}\,d\lambda,
\qquad \phi_{\rm ref}>0.
}
\]

Both are defined on the same ordered relational patch and with the same orientation of the ordering parameter.

Define the relational lapse ratio

\[
\boxed{
N_R(x)
:=\frac{d\tau_x}{d\tau_{\rm ref}}
=\frac{\phi_x}{\phi_{\rm ref}}.
}
\]

Then exactly

\[
\boxed{N_R(x)>0}
\]

and `N_R` is dimensionless because it is a ratio of like elapsed one-forms.

Equivalently,

\[
\boxed{d\tau_x=N_R\,d\tau_{\rm ref}.}
\]

This is the native IDT lapse interface.

## 3. Reparameterization invariance

Under an increasing relabeling

\[
\lambda'=f(\lambda),
\]

05A requires the elapsed-density pace to transform as

\[
\phi'(\lambda')
=\phi(\lambda)\frac{d\lambda}{d\lambda'}.
\]

Therefore both local and reference pace acquire the same Jacobian factor and

\[
\boxed{
N_R'
=\frac{\phi_x'}{\phi_{\rm ref}'}
=\frac{\phi_x}{\phi_{\rm ref}}
=N_R.
}
\]

Thus the relational lapse ratio is invariant under the admitted ordering reparameterization even though the individual pace densities are not scalars.

This is an exact structural reason to use a clock ratio rather than a bare `phi` as the downstream lapse carrier.

## 4. Kinetic realization

05A gives

\[
\phi
=\frac{2M}{\mathfrak a_\star}\cosh(A/2),
\]

where

\[
M
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
\]

If local and reference clocks use the same positive activity normalization `a_star`, then

\[
\boxed{
N_R
=\frac{M_x\cosh(A_x/2)}
{M_{\rm ref}\cosh(A_{\rm ref}/2)}.
}
\]

Hence the lapse ratio is determined structurally by the same relational density, viscosity and drive variables already present in IDT.

For a fixed reference clock,

\[
\boxed{
\ln N_R
=\ln M_x+\ln\cosh(A_x/2)+\text{constant}.
}
\]

Where the fields are differentiable,

\[
\boxed{
\nabla_\mu\ln N_R
=\nabla_\mu\ln M_x
+\frac12\tanh(A_x/2)\,\nabla_\mu A_x
}
\]

for a spatially/temporally constant reference sector.

Using the explicit mobility,

\[
\boxed{
\nabla_\mu\ln M
=\frac12\nabla_\mu\ln\rho_R(a)
+\frac12\nabla_\mu\ln\rho_R(b)
-\nabla_\mu\ln\!\left(\frac{\eta_R(a)+\eta_R(b)}{2}\right).
}
\]

Thus the lapse-gradient carrier has an exact decomposition into relational density, viscosity and directed-drive gradients once the local kinetic realization is admitted.

## 5. Reference normalization

At a chosen reference event/patch `x_*`, normalize the local and reference clock to agree,

\[
\boxed{N_R(x_*)=1.}
\]

This fixes only the relative clock normalization. It does not impose `N_R=1` away from the reference patch.

Changing the reference clock from `r` to `s` gives

\[
\boxed{
N_{x|s}
=N_{x|r}\,N_{r|s}.
}
\]

Therefore relational lapse ratios compose multiplicatively.

For three clocks `x,y,z`,

\[
\boxed{
N_{x|y}N_{y|z}N_{z|x}=1.
}
\]

The logarithmic lapse

\[
\boxed{\nu_{x|r}:=\ln N_{x|r}}
\]

is additive under reference changes.

## 6. Empirical clock binding

Let the reference elapsed coordinate be calibrated monotonically to a physical clock coordinate `t`,

\[
\boxed{dt=T_{\rm ref}\,d\tau_{\rm ref},\qquad T_{\rm ref}>0,}
\]

with the conversion fixed by an explicit clock-calibration protocol.

Then the local calibrated elapsed interval is

\[
\boxed{d\hat\tau_x=N_R\,dt}
\]

when the local and reference intervals have been placed in the same physical time units.

The corresponding length-valued temporal one-form exported to RFC is

\[
\boxed{\Theta_R=N_Rc\,dt.}
\]

This is a physical proper-time/lapse binding candidate. The ratio `N_R` itself is already exact and reparameterization invariant before this empirical unit calibration.

## 7. Weak relational-lapse variable

Near the reference clock define the dimensionless deviation

\[
\boxed{\epsilon_N:=N_R-1.}
\]

For `|epsilon_N|<<1`,

\[
\ln N_R=\epsilon_N+O(\epsilon_N^2).
\]

RFC may later define an energy-per-mass potential variable from the calibrated lapse by

\[
\boxed{\Phi_N:=c^2\ln N_R}
\]

or use the first-order form `c^2(N_R-1)`. IDT exports only the lapse ratio and its gradients; the interpretation of `Phi_N` as a gravitational potential is a downstream weak-field test, not an IDT premise.

## 8. Export contract to RFC

IDT exports:

```text
local_elapsed_one_form      = d tau_x = phi_x d lambda
reference_elapsed_one_form  = d tau_ref = phi_ref d lambda
relational_lapse            = N_R = phi_x / phi_ref > 0
reparam_invariance          = exact
composition                 = N_x|s = N_x|r N_r|s
log_lapse                   = nu = ln N_R
fixed-reference_gradient    = grad ln N_R = grad ln M + 1/2 tanh(A/2) grad A
physical_time_binding       = Theta_R = N_R c dt   [calibration candidate]
```

## 9. Evidence boundary

Exact at this gate:

- positivity and dimensionlessness of `N_R`;
- invariance under the admitted ordering reparameterization;
- multiplicative reference-clock composition;
- the kinetic ratio formula when local/reference clocks share `a_star`;
- the fixed-reference logarithmic-gradient decomposition.

Downstream gates:

- empirical/proper-time calibration of `d tau_ref -> dt`;
- physical identification of `Theta_R=N_R c dt` as the spacetime temporal coframe;
- action/source equation determining the spatial profile of `N_R`;
- Newton weak-field/Poisson closure;
- full Einstein dynamics.
