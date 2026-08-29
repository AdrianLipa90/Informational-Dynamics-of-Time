# QHTRI–Neutrino Lambda Observable v0.1

**Reference gate:** `01AS`  
**Status:** TT_OBSERVABLE_AMPLITUDE_INVERSION

For the canonical transverse source with propagation axis \(z\), define

\[
T_+ = \frac{T_{xx}-T_{yy}}{2},
\qquad
T_\times=T_{xy}.
\]

The spin-2 amplitude and phase are directly observable from the integrated neutrino stress:

\[
\boxed{
A_{\rm obs}=\sqrt{T_+^2+T_\times^2}
}
\]

and

\[
\boxed{
\phi_{\rm obs}=\frac12\operatorname{atan2}(T_\times,T_+)\pmod\pi.
}
\]

Because `01AO` uses

\[
A=\Lambda_A\frac E4,
\]

the amplitude channel of the Lambda board is obtained directly as

\[
\boxed{
\Lambda_A
=\frac{4A_{\rm obs}}{E}
=\frac{4}{T^{00}}
\sqrt{\left(\frac{T_{xx}-T_{yy}}2\right)^2+T_{xy}^2}.
}
\]

For the `01AO` positivity-bounded family, \(0\le\Lambda_A\le1\). A generic measured stress tensor may yield a larger diagnostic value; the implementation exposes that result rather than clipping it, because such a source lies outside the canonical `01AO` family.

`01AS` verifies exact inversion of the analytic `01AO` family, phase recovery modulo \(\pi\), invariance of \(\Lambda_A\) under total-energy rescaling, a tetrahedral isotropic null control, and fail-closed rejection when a generic source violates the canonical Lambda bound.

Together with `01AR`, both Lambda channels now have operational calibration equations:

\[
\boxed{
\Lambda_\phi
=\frac{\Delta m^2}{4E_\nu\hbar\dot\chi},
\qquad
\Lambda_A
=\frac{4A_{\rm obs}}{E}.
}
\]

The remaining empirical task is therefore data binding: supply an experimentally measured or instrument-derived neutrino directional stress/flux distribution and compare the inferred \((\Lambda_A,\phi)\) against the QHTRI rotor prediction.
