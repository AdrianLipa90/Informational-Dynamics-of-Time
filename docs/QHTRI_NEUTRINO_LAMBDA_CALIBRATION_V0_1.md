# QHTRI–Neutrino Lambda Calibration v0.1

**Reference gate:** `01AR`  
**Status:** VACUUM_OSCILLATION_PHASE_CALIBRATION

## Calibration split

The Lambda board has two independently measurable channels:

\[
\Lambda_A=\frac{4A}{E},
\qquad
0\le\Lambda_A\le1,
\]

which fixes the conserved source modulation amplitude, and

\[
\Lambda_\phi=g_\chi,
\qquad
\dot\phi=g_\chi\dot\chi,
\]

which fixes the phase/rate transfer from the differential QHTRI rotor coordinate \(\chi\) to the neutrino carrier phase.

## Vacuum neutrino calibration

For a mass-squared splitting \(\Delta m^2\) and neutrino energy \(E_\nu\), define the standard vacuum probability phase

\[
\delta_{\rm prob}=\frac{\Delta m^2 L}{4E_\nu}
\]

in natural units. In SI time units,

\[
\boxed{
\omega_{\rm prob}=\frac{\Delta m^2}{4E_\nu\hbar}
}
\]

and the relative propagation eigenphase rate is

\[
\boxed{
\omega_{\rm state}=\frac{\Delta m^2}{2E_\nu\hbar}=2\omega_{\rm prob}.
}
\]

The `01AO/01AQ` transverse source already carries spin-2 phase dependence

\[
T_+^{TT}=A\cos 2\phi,
\qquad
T_\times^{TT}=A\sin 2\phi.
\]

Therefore the calibration

\[
\boxed{
\phi\equiv\delta_{\rm prob}
}
\]

makes the doubled source phase \(2\phi\) track the physical relative neutrino state phase directly. No additional factor of two is inserted into the source map.

For a nonzero differential rotor rate \(\dot\chi\),

\[
\boxed{
\Lambda_\phi
=g_\chi
=\frac{\omega_{\rm prob}}{\dot\chi}
=\frac{\Delta m^2}{4E_\nu\hbar\dot\chi}.
}
\]

The full vacuum oscillation length follows from the \(\pi\)-periodicity of \(\sin^2\delta_{\rm prob}\):

\[
\boxed{
L_{\rm osc}
=\frac{4\pi\hbar c E_\nu}{\Delta m^2}.
}
\]

Using \(L\) in km, \(E_\nu\) in GeV, and \(\Delta m^2\) in eV\(^2\), the executable conversion is

\[
\delta_{\rm prob}
=1.266932679\,\frac{\Delta m^2[\mathrm{eV}^2]L[\mathrm{km}]}{E_\nu[\mathrm{GeV}]}.
\]

## 01AR executable checks

`01AR` verifies:

- exact factor-of-two relation \(\omega_{\rm state}=2\omega_{\rm prob}\);
- the standard km/GeV vacuum phase coefficient;
- \(L_{\rm osc}\) advances \(\delta_{\rm prob}\) by exactly \(\pi\);
- \(g_\chi\dot\chi=\omega_{\rm prob}\);
- \(\Lambda_A=4A/E\) exactly inverts the `01AO` amplitude law;
- a calibrated `LambdaBoard` reproduces the target neutrino probability-phase rate while its spin-2 doubled phase reproduces the relative state-phase rate;
- the resulting `01AP` collision four-moment remains zero.

## Frontier

The phase scale of the Lambda board is now tied to an experimentally measurable neutrino oscillation quantity \((\Delta m^2,E_\nu,L)\). The remaining empirical source calibration is the amplitude channel \(\Lambda_A\): one must bind the quadrupolar modulation fraction \(4A/E\) to a measured direction-correlated neutrino flux/stress anisotropy or another directly observable source quantity.
