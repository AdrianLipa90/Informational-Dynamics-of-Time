# 02JK — Seam Curvature Phase Offset to Intrinsic Duration

Status: `ALGEBRAIC_REFERENCE_PASS / REFERENCE_PHASE_CLOCK_NORMALIZATION_PASS`

02JJ supplies the gauge-invariant temporal seam curvature

\[
\boxed{
F_{\Theta e}
=D_\Theta\varphi_e+(BA_\Theta)_e
}
\]

and its accumulated phase offset

\[
\boxed{
\Delta\Phi_e^{\rm curv}
=\int F_{\Theta e}\,d\Theta.
}
\]

02JF supplies an intrinsic phase-rate coordinate measured against the activity-derived temporal measure. This layer uses an explicitly admitted reference phase clock to convert the seam curvature phase offset into a signed offset in the same intrinsic temporal coordinate.

## 1. Reference intrinsic phase clock

Let `R` denote an admitted reference phase clock on the interval. Its intrinsic phase one-form is

\[
\boxed{d\Phi_R=\Omega_R(\Theta)\,d\Theta,}
\]

with

\[
\boxed{\Omega_R(\Theta)>0.}
\]

The reference-clock identity is part of the coordinate type. The TIR/IDT normalization bridge supplies the structural form

\[
\Omega_R=\frac{d\Phi_R}{d\Theta}.
\]

## 2. Signed intrinsic temporal-offset rate

Both `F_Theta,e` and `Omega_R` are phase rates with respect to the same intrinsic temporal measure. Define the dimensionless signed offset rate

\[
\boxed{
\eta_e(\Theta):=\frac{F_{\Theta e}}{\Omega_R(\Theta)}.
}
\]

The corresponding intrinsic temporal-offset one-form is

\[
\boxed{d\Theta_e^{\rm off}:=\eta_e\,d\Theta=\frac{F_{\Theta e}}{\Omega_R}\,d\Theta.}
\]

Hence the accumulated intrinsic offset is

\[
\boxed{
\Delta\Theta_e^{\rm off}
=\int_{\Theta_1}^{\Theta_2}
\frac{F_{\Theta e}(\Theta)}{\Omega_R(\Theta)}\,d\Theta.
}
\]

The sign of `F_Theta,e` is retained. Reversing the oriented seam curvature reverses the signed temporal offset.

## 3. Gauge invariance

02JJ gives

\[
F'_{\Theta e}=F_{\Theta e}.
\]

For an admitted gauge-invariant reference intrinsic phase clock,

\[
\Omega'_R=\Omega_R.
\]

Therefore

\[
\boxed{\eta'_e=\eta_e,\qquad(d\Theta_e^{\rm off})'=d\Theta_e^{\rm off},}
\]

and

\[
\boxed{(\Delta\Theta_e^{\rm off})'=\Delta\Theta_e^{\rm off}.}
\]

The construction therefore inherits the time-dependent gauge closure of 02JJ.

## 4. Exact normalization control

If on an interval

\[
F_{\Theta e}=\Omega_R,
\]

then

\[
\boxed{d\Theta_e^{\rm off}=d\Theta.}
\]

More generally, if

\[
F_{\Theta e}=c\,\Omega_R
\]

for constant signed ratio `c`, then

\[
\boxed{\Delta\Theta_e^{\rm off}=c\,\Delta\Theta.}
\]

This fixes the local conversion without an additional normalization coefficient.

## 5. Constant reference-rate reduction

For constant intrinsic reference phase rate

\[
\Omega_R(\Theta)=\Omega_R,
\]

02JJ's accumulated curvature phase gives

\[
\boxed{\Delta\Theta_e^{\rm off}=\frac{\Delta\Phi_e^{\rm curv}}{\Omega_R}.}
\]

Define the intrinsic reference phase period

\[
\boxed{P_R^{(\Theta)}:=\frac{2\pi}{\Omega_R}.}
\]

If an independently admitted closed curvature sector carries

\[
\Delta\Phi_e^{\rm curv}=2\pi m,
\qquad m\in\mathbb Z,
\]

then

\[
\boxed{\Delta\Theta_e^{\rm off}=mP_R^{(\Theta)}.}
\]

Thus a closed integer curvature winding corresponds to an integer number of periods of the explicitly selected intrinsic reference phase clock.

The finite frame-budget winding `Phi_N=2pi N` remains a separately typed coordinate until an explicit binding map between the frame budget and a closed curvature sector is admitted.

## 6. Information-rate representation

The TIR/IDT bridge gives

\[
\boxed{
\Gamma_{\mathcal I,R}^{(\Theta)}
=\kappa\Omega_R,
\qquad
\kappa=\frac{\ln2}{24\pi}.
}
\]

Therefore

\[
\boxed{\eta_e=\frac{\kappa F_{\Theta e}}{\Gamma_{\mathcal I,R}^{(\Theta)}}.}
\]

Equivalently,

\[
\boxed{d\Theta_e^{\rm off}=\frac{\kappa F_{\Theta e}}{\Gamma_{\mathcal I,R}^{(\Theta)}}d\Theta.}
\]

This is exactly the same intrinsic offset coordinate written through the information-rate channel.

## 7. Physical clock calibration

Let the same reference temporal measure carry the admitted physical clock calibration

\[
\boxed{dt=T_R(\Theta)\,d\Theta,}
\]

with `T_R>0`. The corresponding calibrated coordinate-time offset is

\[
\boxed{
\Delta t_e^{\rm off}
=\int
T_R(\Theta)
\frac{F_{\Theta e}}{\Omega_R}
\,d\Theta.
}
\]

For a local subsystem `x` with relational lapse `N_R(x|R)>0`, the calibrated local proper-clock offset is

\[
\boxed{
\Delta\hat\tau_{x,e}^{\rm off}
=\int
N_R(x|R)T_R
\frac{F_{\Theta e}}{\Omega_R}
\,d\Theta.
}
\]

The sequence is therefore

\[
\boxed{
F_{\Theta e}
\to
\Delta\Phi_e^{\rm curv}
\to
\Delta\Theta_e^{\rm off}
\to
\Delta t_e^{\rm off}
\to
\Delta\hat\tau_{x,e}^{\rm off}.
}
\]

Each conversion carries its reference-clock and calibration data explicitly.

## 8. Additivity

For adjacent intrinsic intervals `[Theta_1,Theta_2]` and `[Theta_2,Theta_3]`,

\[
\boxed{
\Delta\Theta_e^{\rm off}[\Theta_1,\Theta_3]
=
\Delta\Theta_e^{\rm off}[\Theta_1,\Theta_2]
+
\Delta\Theta_e^{\rm off}[\Theta_2,\Theta_3].
}
\]

The same concatenation property holds for calibrated coordinate and local proper-clock offsets when the corresponding scale/lapse fields are integrated on the same history.

## 9. Reference gate

Reference implementation: `src/idt/seam_phase_offset_intrinsic_duration.py`.

Reference tests: `tests/reference/test_seam_phase_offset_intrinsic_duration.py`.

Validation receipt: `validation/SEAM_PHASE_OFFSET_INTRINSIC_DURATION_V0_1.json`.

The next typed gate after algebraic admission is the binding of this intrinsic offset coordinate to the existing material Temporal Wave / realized-NOW architecture, followed by an observational protocol for relative clock offset.
