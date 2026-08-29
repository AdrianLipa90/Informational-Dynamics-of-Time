"""01AT: directional neutrino-event -> normalized stress -> Lambda observable adapter.

This module is instrument-facing rather than detector-specific.  It accepts reconstructed
sky directions plus non-negative event weights and forms the normalized second angular
moment

    S_ij = sum_a w_a n_i n_j / sum_a w_a.

If ``w_a`` are physical packet energies, ``S`` is the spatial stress divided by total
energy.  If they are detector/event proxies, the output is only a dimensionless shape
estimator until an exposure/response calibration is supplied.

The adapter is suitable for public IceCube track samples whose reconstructed fields include
RA, Dec and log-energy-like observables, but it does not promote a detector energy proxy to
true neutrino energy.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

from .qhtri_neutrino_gravity import normalize_direction, project_tt


Matrix3 = tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]
Vector3 = tuple[float, float, float]


def radec_unit_vector(ra_deg: float, dec_deg: float) -> Vector3:
    """Convert right ascension/declination in degrees to a Cartesian unit vector."""
    ra = math.radians(float(ra_deg))
    dec = math.radians(float(dec_deg))
    if not math.isfinite(ra) or not math.isfinite(dec):
        raise ValueError("RA and Dec must be finite")
    if dec < -0.5 * math.pi or dec > 0.5 * math.pi:
        raise ValueError("declination must lie in [-90, 90] degrees")
    c = math.cos(dec)
    return (c * math.cos(ra), c * math.sin(ra), math.sin(dec))


def relative_energy_proxy_weights(log10_energy: Sequence[float]) -> tuple[float, ...]:
    """Turn log10 energy/proxy values into scale-free positive relative weights.

    Subtracting the maximum before exponentiation preserves all weight ratios while
    avoiding overflow.  These weights carry no physical-energy normalization.
    """
    xs = tuple(float(x) for x in log10_energy)
    if not xs or not all(math.isfinite(x) for x in xs):
        raise ValueError("log10_energy must contain finite values")
    shift = max(xs)
    return tuple(10.0 ** (x - shift) for x in xs)


def exposure_corrected_weights(
    raw_weights: Sequence[float],
    relative_acceptance: Sequence[float],
) -> tuple[float, ...]:
    """Return inverse-acceptance corrected event weights.

    ``relative_acceptance`` may be any consistently normalized positive detector
    exposure/effective-area factor.  Its absolute normalization cancels from the
    normalized stress shape.
    """
    if len(raw_weights) == 0 or len(raw_weights) != len(relative_acceptance):
        raise ValueError("raw_weights and relative_acceptance must have equal non-zero length")
    out = []
    for weight, acceptance in zip(raw_weights, relative_acceptance):
        w = float(weight)
        a = float(acceptance)
        if not math.isfinite(w) or w < 0.0:
            raise ValueError("raw weights must be finite and non-negative")
        if not math.isfinite(a) or a <= 0.0:
            raise ValueError("relative acceptance must be finite and strictly positive")
        out.append(w / a)
    if sum(out) <= 0.0:
        raise ValueError("corrected weights must contain positive total weight")
    return tuple(out)


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(float(x) * float(y) for x, y in zip(a, b))


def _cross(a: Sequence[float], b: Sequence[float]) -> Vector3:
    return (
        float(a[1]) * float(b[2]) - float(a[2]) * float(b[1]),
        float(a[2]) * float(b[0]) - float(a[0]) * float(b[2]),
        float(a[0]) * float(b[1]) - float(a[1]) * float(b[0]),
    )


def transverse_basis(axis: Sequence[float]) -> tuple[Vector3, Vector3, Vector3]:
    """Return right-handed (e1,e2,n) basis for an arbitrary propagation axis."""
    n = normalize_direction(axis)
    seed: Vector3 = (1.0, 0.0, 0.0) if abs(n[2]) > 0.9 else (0.0, 0.0, 1.0)
    parallel = _dot(seed, n)
    e1 = normalize_direction(tuple(seed[i] - parallel * n[i] for i in range(3)))
    e2 = normalize_direction(_cross(n, e1))
    return e1, e2, n


def polarization_in_basis(
    tt: Sequence[Sequence[float]],
    axis: Sequence[float],
) -> tuple[float, float]:
    """Return (+,x) components of a TT tensor in a deterministic transverse basis."""
    e1, e2, _ = transverse_basis(axis)

    def bilinear(a: Sequence[float], b: Sequence[float]) -> float:
        return sum(float(a[i]) * float(tt[i][j]) * float(b[j]) for i in range(3) for j in range(3))

    plus = 0.5 * (bilinear(e1, e1) - bilinear(e2, e2))
    cross = 0.5 * (bilinear(e1, e2) + bilinear(e2, e1))
    return plus, cross


@dataclass(frozen=True)
class DirectionalStressEstimate:
    total_weight: float
    stress_shape: Matrix3
    tt_shape: Matrix3
    plus: float
    cross: float
    amplitude_fraction: float
    lambda_amplitude: float
    phase_rad_mod_pi: float
    canonical_lambda_family: bool


def estimate_directional_stress(
    directions: Sequence[Sequence[float]],
    weights: Sequence[float] | None = None,
    *,
    propagation_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> DirectionalStressEstimate:
    """Estimate normalized spatial stress and invert the 01AS Lambda observables."""
    if len(directions) == 0:
        raise ValueError("directions must be non-empty")
    ns = tuple(normalize_direction(d) for d in directions)
    if weights is None:
        ws = (1.0,) * len(ns)
    else:
        if len(weights) != len(ns):
            raise ValueError("weights and directions must have equal length")
        ws = tuple(float(w) for w in weights)
    if not all(math.isfinite(w) and w >= 0.0 for w in ws) or sum(ws) <= 0.0:
        raise ValueError("weights must be finite, non-negative, and have positive sum")

    total = sum(ws)
    shape: Matrix3 = tuple(
        tuple(sum(w * n[i] * n[j] for w, n in zip(ws, ns)) / total for j in range(3))
        for i in range(3)
    )  # type: ignore[assignment]
    tt = project_tt(shape, propagation_axis)
    plus, cross = polarization_in_basis(tt, propagation_axis)
    amp = math.hypot(plus, cross)
    lam = 4.0 * amp
    phase = 0.0 if amp == 0.0 else (0.5 * math.atan2(cross, plus)) % math.pi
    return DirectionalStressEstimate(
        total_weight=total,
        stress_shape=shape,
        tt_shape=tt,
        plus=plus,
        cross=cross,
        amplitude_fraction=amp,
        lambda_amplitude=lam,
        phase_rad_mod_pi=phase,
        canonical_lambda_family=(-1e-12 <= lam <= 1.0 + 1e-12),
    )


def estimate_radec_events(
    ra_deg: Sequence[float],
    dec_deg: Sequence[float],
    weights: Sequence[float] | None = None,
    *,
    relative_acceptance: Sequence[float] | None = None,
    propagation_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> DirectionalStressEstimate:
    """RA/Dec convenience wrapper with optional inverse-acceptance correction."""
    if len(ra_deg) == 0 or len(ra_deg) != len(dec_deg):
        raise ValueError("RA and Dec arrays must have equal non-zero length")
    directions = tuple(radec_unit_vector(ra, dec) for ra, dec in zip(ra_deg, dec_deg))
    raw = (1.0,) * len(directions) if weights is None else tuple(float(w) for w in weights)
    if len(raw) != len(directions):
        raise ValueError("weights and events must have equal length")
    final = raw if relative_acceptance is None else exposure_corrected_weights(raw, relative_acceptance)
    return estimate_directional_stress(directions, final, propagation_axis=propagation_axis)


def estimate_icetracks_rows(
    rows: Sequence[Mapping[str, float]],
    *,
    energy_proxy_weighted: bool = False,
    relative_acceptance: Sequence[float] | None = None,
    propagation_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> DirectionalStressEstimate:
    """Adapter for IceTracks-like mappings containing ``ra``, ``dec``, ``log_energy``.

    When ``energy_proxy_weighted`` is false every selected event receives unit weight.
    When true, ``log_energy`` is used only as a relative detector proxy weight.
    """
    if not rows:
        raise ValueError("rows must be non-empty")
    try:
        ra = tuple(float(row["ra"]) for row in rows)
        dec = tuple(float(row["dec"]) for row in rows)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("each row must contain finite numeric ra and dec") from exc
    if energy_proxy_weighted:
        try:
            proxy = tuple(float(row["log_energy"]) for row in rows)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("energy-proxy weighting requires numeric log_energy") from exc
        weights = relative_energy_proxy_weights(proxy)
    else:
        weights = (1.0,) * len(rows)
    return estimate_radec_events(
        ra,
        dec,
        weights,
        relative_acceptance=relative_acceptance,
        propagation_axis=propagation_axis,
    )
