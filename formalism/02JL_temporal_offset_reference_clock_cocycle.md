# 02JL — Temporal Offset Reference-Clock Cocycle

Status: `FORMAL_CANDIDATE / RELATIONAL_REFERENCE_CHANGE_GATE`

02JK assigns a signed intrinsic temporal offset relative to an explicitly admitted positive intrinsic phase clock `R`,

\[
\boxed{
d\Theta_{e,\mathrm{off}}^{[R]}
=\frac{F_{\Theta e}}{\Omega_R}\,d\Theta.
}
\]

This layer derives the exact change-of-reference law between admitted intrinsic phase clocks and identifies the reference-neutral carrier common to all such coordinates.

## 1. Two reference phase clocks

Let `R` and `S` be admitted intrinsic phase clocks on the same relational interval,

\[
\boxed{d\Phi_R=\Omega_R\,d\Theta,\qquad d\Phi_S=\Omega_S\,d\Theta,}
\]

with

\[
\boxed{\Omega_R>0,\qquad\Omega_S>0.}
\]

For the same gauge-invariant temporal seam curvature `F_Theta,e`, define

\[
d\Theta_{e,\mathrm{off}}^{[R]}
=\frac{F_{\Theta e}}{\Omega_R}d\Theta,
\qquad
 d\Theta_{e,\mathrm{off}}^{[S]}
=\frac{F_{\Theta e}}{\Omega_S}d\Theta.
\]

## 2. Exact reference-change factor

Define

\[
\boxed{
C_{R\to S}(\Theta)
:=\frac{\Omega_R(\Theta)}{\Omega_S(\Theta)}>0.
}
\]

Then pointwise

\[
\boxed{
d\Theta_{e,\mathrm{off}}^{[S]}
=C_{R\to S}\,d\Theta_{e,\mathrm{off}}^{[R]}.
}
\]

Thus the temporal-offset coordinate transforms by the ratio of the two admitted intrinsic phase-clock rates.

## 3. Cocycle identities

For any three admitted positive intrinsic phase clocks `R,S,T`,

\[
\boxed{C_{R\to R}=1,}
\]

\[
\boxed{C_{S\to R}=C_{R\to S}^{-1},}
\]

and

\[
\boxed{
C_{R\to T}
=C_{R\to S}C_{S\to T}.
}
\]

These identities follow exactly from the rate ratios. Hence the reference transformations form a positive multiplicative cocycle on the admitted phase-clock family.

## 4. Reference-neutral curvature carrier

Multiplying the offset coordinate by its reference phase rate removes the reference choice:

\[
\boxed{
\Omega_R\,d\Theta_{e,\mathrm{off}}^{[R]}
=F_{\Theta e}d\Theta.
}
\]

For any other admitted reference `S`,

\[
\boxed{
\Omega_S\,d\Theta_{e,\mathrm{off}}^{[S]}
=F_{\Theta e}d\Theta.
}
\]

Therefore

\[
\boxed{
 d\Phi_e^{\rm curv}
:=F_{\Theta e}d\Theta
=\Omega_Rd\Theta_{e,\mathrm{off}}^{[R]}
=\Omega_Sd\Theta_{e,\mathrm{off}}^{[S]}.
}
\]

The curvature phase one-form is the reference-neutral carrier, while `dTheta_off^[R]` is its coordinate measured in periods of phase clock `R`.

## 5. Variable-rate interval transformation

When `C_(R->S)` varies along the interval,

\[
\boxed{
\Delta\Theta_{e,\mathrm{off}}^{[S]}
=\int C_{R\to S}(\Theta)
\,d\Theta_{e,\mathrm{off}}^{[R]}.
}
\]

For constant `C_(R->S)`, this reduces to

\[
\boxed{
\Delta\Theta_{e,\mathrm{off}}^{[S]}
=C_{R\to S}\,
\Delta\Theta_{e,\mathrm{off}}^{[R]}.
}
\]

The pointwise law therefore remains exact when the reference phase-clock rates vary.

## 6. Information-rate representation

02JF supplies

\[
\Gamma_{\mathcal I,R}^{(\Theta)}=\kappa\Omega_R,
\qquad
\Gamma_{\mathcal I,S}^{(\Theta)}=\kappa\Omega_S,
\]

with common

\[
\kappa=\frac{\ln2}{24\pi}.
\]

Hence

\[
\boxed{
C_{R\to S}
=\frac{\Omega_R}{\Omega_S}
=\frac{\Gamma_{\mathcal I,R}^{(\Theta)}}
{\Gamma_{\mathcal I,S}^{(\Theta)}}.
}
\]

The phase-rate and information-rate descriptions therefore produce the same reference transformation.

## 7. Winding-locked reduction

TIR supplies a dimensionless common-cycle average phase-rate ratio from winding data. The admitted pointwise locking gate additionally supplies, for a locked sector,

\[
\frac{\Omega_S}{\Omega_R}
=\frac{m_S}{m_R},
\qquad m_R,m_S\in\mathbb N.
\]

Then

\[
\boxed{
C_{R\to S}
=\frac{m_R}{m_S},
}
\]

and therefore

\[
\boxed{
d\Theta_{e,\mathrm{off}}^{[S]}
=\frac{m_R}{m_S}
 d\Theta_{e,\mathrm{off}}^{[R]}.
}
\]

This is the arithmetic reference-change law in the pointwise winding-locked sector.

## 8. Calibrated clock reference change

If the two reference clocks carry physical calibrations

\[
dt_R=T_Rd\Theta,
\qquad
dt_S=T_Sd\Theta,
\qquad T_R,T_S>0,
\]

then

\[
dt_{e,\mathrm{off}}^{[R]}
=T_Rd\Theta_{e,\mathrm{off}}^{[R]},
\]

and

\[
\boxed{
 dt_{e,\mathrm{off}}^{[S]}
=\frac{T_S\Omega_R}{T_R\Omega_S}
 dt_{e,\mathrm{off}}^{[R]}.
}
\]

This is a calibration composition law. Spacetime transport remains a separate downstream gate.

## 9. Zero-curvature control

For

\[
F_{\Theta e}=0,
\]

all admitted reference clocks give

\[
\boxed{
d\Theta_{e,\mathrm{off}}^{[R]}=0.}
\]

The reference change therefore cannot generate a temporal offset from a zero curvature carrier.

## 10. Reference gate

Reference implementation: `src/idt/temporal_offset_reference_clock_cocycle.py`.

Reference tests: `tests/reference/test_temporal_offset_reference_clock_cocycle.py`.

Validation receipt: `validation/TEMPORAL_OFFSET_REFERENCE_CLOCK_COCYCLE_V0_1.json`.

The next downstream gate is the binding of the reference-covariant intrinsic offset coordinate to the realized material Temporal Wave / NOW carrier and then to an observational relative-clock protocol.
