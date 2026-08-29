# 02JM — Material Temporal Offset Binding

Status: `ALGEBRAIC_MATERIAL_CLOCK_BINDING_CANDIDATE / RFC_EXPORT_GATE`

02JL supplies the reference-covariant intrinsic offset

\[
\boxed{
d\Theta_{e,\mathrm{off}}^{[R]}
=\frac{F_{\Theta e}}{\Omega_R}\,d\Theta_r,
\qquad \Omega_R>0,
}
\]

on an admitted reference temporal patch. 05C independently supplies a positive material clock/lapse binding. This layer composes those two already-derived structures.

## 1. Reference physical clock

Let the admitted reference subsystem `r` carry

\[
\boxed{d\Theta_r=\mathfrak a_r\,d\lambda,\qquad \mathfrak a_r>0,}
\]

and physical calibration

\[
\boxed{dt=T_r\,d\Theta_r,\qquad T_r>0.}
\]

For a material subsystem `x`, 05C supplies

\[
\boxed{
N_R(x|r)=\frac{\mathfrak a_x}{\mathfrak a_r}>0
}
\]

and local calibrated elapsed interval

\[
\boxed{d\hat\tau_x=N_R(x|r)\,dt.}
\]

Hence

\[
\boxed{
d\hat\tau_x=N_R T_r\,d\Theta_r.}
\]

## 2. Material offset one-form

Define the reference-clock seam ratio

\[
\boxed{
\eta_e^{[R]}:=\frac{F_{\Theta e}}{\Omega_R}.
}
\]

The intrinsic offset is

\[
d\Theta_{e,\mathrm{off}}^{[R]}
=\eta_e^{[R]}d\Theta_r.
\]

The corresponding coordinate-clock offset is

\[
\boxed{
dt_{e,\mathrm{off}}^{[R]}
:=T_r d\Theta_{e,\mathrm{off}}^{[R]}
=T_r\eta_e^{[R]}d\Theta_r.
}
\]

The local material elapsed-time offset is then

\[
\boxed{
d\hat\tau_{x,e,\mathrm{off}}^{[R]}
:=N_Rdt_{e,\mathrm{off}}^{[R]}
=N_RT_r\frac{F_{\Theta e}}{\Omega_R}d\Theta_r.}
\]

Equivalently,

\[
\boxed{
d\hat\tau_{x,e,\mathrm{off}}^{[R]}
=\eta_e^{[R]}d\hat\tau_x.}
\]

This is the exact material-clock binding of the seam offset.

## 3. Fractional-offset theorem

Whenever the local elapsed interval is nonzero,

\[
\boxed{
\frac{d\hat\tau_{x,e,\mathrm{off}}^{[R]}}
{d\hat\tau_x}
=\frac{F_{\Theta e}}{\Omega_R}.
}
\]

The lapse and dimensional calibration multiply both the base elapsed one-form and its seam offset by the same positive factor. Therefore the fractional material offset is exactly the reference-clock seam ratio.

For two material subsystems `x,y` using the same reference patch and seam carrier,

\[
\boxed{
\frac{d\hat\tau_{x,e,\mathrm{off}}^{[R]}}{d\hat\tau_x}
=
\frac{d\hat\tau_{y,e,\mathrm{off}}^{[R]}}{d\hat\tau_y}
=\eta_e^{[R]}.
}
\]

Their absolute offsets still differ through their respective lapse factors.

## 4. Reference-clock cocycle on the material offset

For two admitted phase clocks `R,S`, 02JL gives

\[
C_{R\to S}=\frac{\Omega_R}{\Omega_S}>0.
\]

Holding the same material calibration `(N_R,T_r)` fixed on the patch,

\[
\boxed{
d\hat\tau_{x,e,\mathrm{off}}^{[S]}
=C_{R\to S}
 d\hat\tau_{x,e,\mathrm{off}}^{[R]}.}
\]

The material binding therefore preserves the exact positive multiplicative cocycle.

The reference-neutral phase carrier remains

\[
\boxed{
d\Phi_e^{\rm curv}=F_{\Theta e}d\Theta_r.}
\]

## 5. Ordering-coordinate rate identities

Using

\[
d\Theta_r=\mathfrak a_r d\lambda,
\qquad
N_R=\frac{\mathfrak a_x}{\mathfrak a_r},
\]

the reference physical-clock slope is

\[
\boxed{
\Gamma_{t,r}:=\frac{dt}{d\lambda}
=T_r\mathfrak a_r.}
\]

The local material elapsed-time slope is

\[
\boxed{
\Gamma_{\tau,x|r}
:=\frac{d\hat\tau_x}{d\lambda}
=N_R\Gamma_{t,r}
=T_r\mathfrak a_x.}
\]

Thus the lapse composition collapses exactly to the local activity rate under the common reference calibration `T_r`.

For the material seam offset,

\[
\boxed{
\frac{d\hat\tau_{x,e,\mathrm{off}}^{[R]}}{d\lambda}
=T_r\mathfrak a_x\frac{F_{\Theta e}}{\Omega_R}
=\Gamma_{\tau,x|r}\eta_e^{[R]}.}
\]

## 6. RFC RF-L5A source pin

RF-L5A uses a local affine calibration

\[
t-t_\star=\Gamma_t(\lambda-\lambda_\star).
\]

On an interval where `T_r` and `a_r` are treated as constant in that affine approximation, IDT exports the typed reference-clock identification

\[
\boxed{
\Gamma_t\equiv\Gamma_{t,r}=T_r\mathfrak a_r.}
\]

For a local proper-time calibration of subsystem `x`, the corresponding slope is

\[
\boxed{
\Gamma_\tau\equiv\Gamma_{\tau,x|r}=T_r\mathfrak a_x=N_R\Gamma_t.}
\]

This resolves which IDT quantity can populate the RF-L5A time-calibration slot: the slope is a calibrated clock derivative with respect to the same ordering coordinate `lambda`, while the intrinsic phase rate `Omega_R` remains a separate carrier.

## 7. Zero and sign controls

Because

\[
N_R>0,\qquad T_r>0,\qquad \Omega_R>0,
\]

one has

\[
F_{\Theta e}=0
\Longrightarrow
 d\hat\tau_{x,e,\mathrm{off}}^{[R]}=0,
\]

and for nonzero `dTheta_r`,

\[
\boxed{
\operatorname{sgn}
\left(d\hat\tau_{x,e,\mathrm{off}}^{[R]}\right)
=
\operatorname{sgn}(F_{\Theta e}d\Theta_r).
}
\]

Positive material calibration does not reverse the seam-offset orientation.

## 8. Evidence and downstream gate

The algebraic gate covers:

- exact composition of intrinsic offset with physical calibration and lapse;
- fractional-offset theorem;
- preservation of the reference-clock cocycle;
- ordering-coordinate clock-rate identities;
- the RF-L5A `Gamma_t` source pin under the shared affine `lambda` calibration;
- zero/sign controls.

The observational identification of this material clock with a particular laboratory clock species, the spatial calibration `Gamma_x`, and full relativistic/ADM transport remain downstream experimental/geometric gates.

Reference implementation: `src/idt/material_temporal_offset_binding.py`.

Reference tests: `tests/reference/test_material_temporal_offset_binding.py`.

Validation receipt: `validation/MATERIAL_TEMPORAL_OFFSET_BINDING_V0_1.json`.
