"""01AS: infer the Lambda amplitude and spin-2 phase from neutrino TT stress.

For the canonical 01AO transverse source (propagation axis z), define

    T_plus  = (T_xx - T_yy)/2
    T_cross = T_xy.

The observable spin-2 amplitude and phase are

    A_obs   = hypot(T_plus, T_cross)
    phi_obs = 1/2 atan2(T_cross, T_plus)  (mod pi),

and the Lambda-board amplitude fraction follows directly from the integrated
source energy E = T^00:

    Lambda_A = 4 A_obs / E.

This is an exact inverse of the 01AO source family.  For a generic source it is
a diagnostic transverse anisotropy fraction; values above one indicate that the
source is outside the positivity-bounded 01AO family rather than being clipped.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .neutrino_physical_stress import IntegratedNeutrinoStress


@dataclass(frozen=True)
class TransverseTTObservable:
    total_energy_joule: float
    plus_joule: float
    cross_joule: float
    amplitude_joule: float
    phase_rad_mod_pi: float
    lambda_amplitude_fraction: float


def transverse_tt_observable_z(
    source: IntegratedNeutrinoStress,
    *,
    zero_tolerance_joule: float = 1e-15,
) -> TransverseTTObservable:
    """Extract the canonical z-axis spin-2 observable from integrated stress."""

    energy = float(source.total_energy_joule)
    tol = float(zero_tolerance_joule)
    if not math.isfinite(energy) or energy <= 0.0:
        raise ValueError("source total energy must be finite and positive")
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError("zero_tolerance_joule must be finite and non-negative")

    t = source.tensor_joule
    plus = 0.5 * (float(t[1][1]) - float(t[2][2]))
    cross = 0.5 * (float(t[1][2]) + float(t[2][1]))
    if not all(math.isfinite(x) for x in (plus, cross)):
        raise ValueError("source transverse stress must be finite")

    amp = math.hypot(plus, cross)
    phase = 0.0 if amp <= tol else 0.5 * math.atan2(cross, plus)
    lam = 4.0 * amp / energy
    return TransverseTTObservable(
        total_energy_joule=energy,
        plus_joule=plus,
        cross_joule=cross,
        amplitude_joule=amp,
        phase_rad_mod_pi=phase,
        lambda_amplitude_fraction=lam,
    )


def spin2_phase_residual_rad(measured_phase_rad: float, reference_phase_rad: float) -> float:
    """Return the smallest phase residual modulo pi for a spin-2 carrier."""

    a = float(measured_phase_rad)
    b = float(reference_phase_rad)
    if not math.isfinite(a) or not math.isfinite(b):
        raise ValueError("phases must be finite")
    # Map a-b to [-pi/2, pi/2), the fundamental interval of phi modulo pi.
    return ((a - b + 0.5 * math.pi) % math.pi) - 0.5 * math.pi


def require_01ao_lambda_bound(observable: TransverseTTObservable, *, atol: float = 1e-12) -> float:
    """Return Lambda_A if the observable lies inside the 01AO positivity bound."""

    lam = float(observable.lambda_amplitude_fraction)
    tol = float(atol)
    if not math.isfinite(tol) or tol < 0.0:
        raise ValueError("atol must be finite and non-negative")
    if lam < -tol or lam > 1.0 + tol:
        raise ValueError("observable lies outside the 01AO bound 0 <= Lambda_A <= 1")
    return min(1.0, max(0.0, lam))
