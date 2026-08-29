# 01AT — Directional Neutrino Event Stress Adapter

**Status:** INSTRUMENT_READY / RESPONSE_CALIBRATION_REQUIRED  
**Target public sample:** IceCube IceTracks-DR2 (2008–2022), DOI `10.7910/DVN/MMIIZA`.

IceTracks-DR2 exposes reconstructed track-event fields through the public IceCube/SkyLLH tooling, including `ra`, `dec`, `ang_err`, `time`, and `log_energy`.  The adapter uses only the directional second moment required by the existing 01AS observable inversion.

For reconstructed unit directions

\[
\mathbf n_a=(\cos\delta_a\cos\alpha_a,\cos\delta_a\sin\alpha_a,\sin\delta_a)
\]

and non-negative weights \(w_a\), define

\[
\boxed{
S_{ij}=\frac{\sum_a w_a n_i^{(a)}n_j^{(a)}}{\sum_a w_a}.
}
\]

`S` is a normalized spatial stress tensor when the weights are physical packet energies.  With unit event weights or reconstructed detector energy proxies it is an angular-shape estimator.  Physical stress normalization is admitted only after response/effective-area calibration.

For a chosen propagation axis, 01AT applies the existing TT projector and evaluates a deterministic transverse polarization basis:

\[
S_+,\quad S_\times,
\]

then directly inverts the normalized 01AS observables

\[
\boxed{
\frac{A_{\rm obs}}{E}=\sqrt{S_+^2+S_\times^2},
\qquad
\Lambda_A=4\sqrt{S_+^2+S_\times^2},
}
\]

\[
\boxed{
\phi_{\rm obs}=\frac12\operatorname{atan2}(S_\times,S_+)\pmod\pi.
}
\]

## Detector-response firewall

A direction-dependent detector acceptance \(a_a>0\) is removed at the estimator level by inverse weighting

\[
\tilde w_a=\frac{w_a}{a_a}.
\]

The absolute normalization of \(a_a\) cancels in `S`; only the relative directional response is required for the shape inversion.  Zero, negative, non-finite, or missing acceptance values fail closed.

The `log_energy` field may optionally be converted to relative proxy weights by subtracting the sample maximum before exponentiation.  This preserves ratios while explicitly retaining proxy-only status; it is not interpreted as true neutrino energy.

## Reference gate

`tests/reference/test_01AT_directional_event_stress_adapter.py` verifies:

- exact RA/Dec unit-vector geometry;
- isotropic six-axis null control;
- exact reconstruction of the analytic 01AO spin-2 family from event directions and weights;
- exact recovery after a deliberately anisotropic detector acceptance distortion;
- equality of Cartesian and RA/Dec estimators;
- scale invariance of log-energy proxy weighting;
- fail-closed response/input validation.

## Experimental frontier

The remaining step is now data rather than formalism:

\[
\boxed{
\text{IceTracks-DR2 events + detector response}
\rightarrow
S_{ij}^{\rm corrected}
\rightarrow
(\Lambda_A,\phi)_{\rm data}
\stackrel{?}{=}
(\Lambda_A,\phi)_{\rm QHTRI}.
}
\]

The comparison must be performed season-by-season or with an equivalent response treatment so detector exposure is not mistaken for source anisotropy.  The repository may suggest a QHTRI/neutrino correspondence after this comparison, yet does not state the correspondence as an established empirical result until the response-corrected data test is executed.
