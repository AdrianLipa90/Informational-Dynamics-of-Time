from __future__ import annotations

import math
from dataclasses import dataclass


class MemoryMuError(ValueError):
    pass


@dataclass(frozen=True)
class EllipseFromApses:
    periapsis: float
    apoapsis: float
    semi_major_axis: float
    eccentricity: float
    semi_latus_rectum: float


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise MemoryMuError(f"{name} must be finite and strictly positive")
    return x


def ellipse_from_apses(periapsis: float, apoapsis: float) -> EllipseFromApses:
    rp = _positive(periapsis, "periapsis")
    ra = _positive(apoapsis, "apoapsis")
    if ra < rp:
        raise MemoryMuError("apoapsis must be greater than or equal to periapsis")
    a = 0.5 * (rp + ra)
    e = (ra - rp) / (ra + rp)
    p = 2.0 * rp * ra / (rp + ra)
    return EllipseFromApses(rp, ra, a, e, p)


def mu_from_angular_momentum_and_latus_rectum(angular_momentum: float, semi_latus_rectum: float) -> float:
    h = float(angular_momentum)
    p = _positive(semi_latus_rectum, "semi_latus_rectum")
    if not math.isfinite(h):
        raise MemoryMuError("angular_momentum must be finite")
    return float((h * h) / p)


def mu_from_period_and_semimajor_axis(period: float, semi_major_axis: float) -> float:
    T = _positive(period, "period")
    a = _positive(semi_major_axis, "semi_major_axis")
    return float(4.0 * math.pi * math.pi * a**3 / (T * T))


def mu_from_circulation_rate(circulation_rate: float, coupling: float, semi_latus_rectum: float) -> float:
    rate = float(circulation_rate)
    lam = float(coupling)
    p = _positive(semi_latus_rectum, "semi_latus_rectum")
    if not math.isfinite(rate):
        raise MemoryMuError("circulation_rate must be finite")
    if not math.isfinite(lam) or lam == 0.0:
        raise MemoryMuError("coupling must be finite and nonzero")
    h = rate / lam
    return float((h * h) / p)
