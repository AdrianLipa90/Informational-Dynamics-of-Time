from __future__ import annotations

import math
from collections.abc import Callable, Hashable, Mapping, Sequence
from dataclasses import dataclass
from typing import TypeVar

from .relational_kinetics import DirectedRates, directed_rates


class TemporalActivityError(ValueError):
    pass


K = TypeVar("K", bound=Hashable)
L = TypeVar("L", bound=Hashable)


@dataclass(frozen=True)
class ActivityCurrent:
    activity: float
    current: float
    drive: float
    affinity_bits: float


def activity_current_from_rates(forward: float, reverse: float) -> ActivityCurrent:
    f = float(forward)
    r = float(reverse)
    if not (math.isfinite(f) and math.isfinite(r)) or f <= 0.0 or r <= 0.0:
        raise TemporalActivityError("forward and reverse rates must be finite and strictly positive")
    activity = f + r
    current = f - r
    ratio = current / activity
    if not (-1.0 < ratio < 1.0):
        raise TemporalActivityError("finite positive rates require |current/activity| < 1")
    drive = 2.0 * math.atanh(ratio)
    affinity_bits = drive / math.log(2.0)
    return ActivityCurrent(activity, current, drive, affinity_bits)


def activity_current_from_fields(
    rho_a: float,
    rho_b: float,
    eta_a: float,
    eta_b: float,
    edge_drive: float,
) -> ActivityCurrent:
    rates: DirectedRates = directed_rates(rho_a, rho_b, eta_a, eta_b, edge_drive)
    return activity_current_from_rates(rates.forward, rates.reverse)


def positive_activity_measure(points: Sequence[K], activities: Sequence[float]) -> dict[K, float]:
    if len(points) != len(activities):
        raise TemporalActivityError("points and activities must have the same length")
    out: dict[K, float] = {}
    for point, raw in zip(points, activities):
        a = float(raw)
        if not math.isfinite(a) or a <= 0.0:
            raise TemporalActivityError("activity atom weights must be finite and strictly positive")
        out[point] = out.get(point, 0.0) + a
    return out


def atomic_support(measure: Mapping[K, float]) -> set[K]:
    support: set[K] = set()
    for point, raw in measure.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0.0:
            raise TemporalActivityError("positive activity measure requires finite non-negative masses")
        if value > 0.0:
            support.add(point)
    return support


def pushforward_positive_measure(
    measure: Mapping[K, float],
    mapping: Mapping[K, L] | Callable[[K], L],
) -> dict[L, float]:
    out: dict[L, float] = {}
    for point, raw in measure.items():
        value = float(raw)
        if not math.isfinite(value) or value < 0.0:
            raise TemporalActivityError("positive activity measure requires finite non-negative masses")
        if value == 0.0:
            continue
        image = mapping(point) if callable(mapping) else mapping[point]
        out[image] = out.get(image, 0.0) + value
    return out


def image_support(support: set[K], mapping: Mapping[K, L] | Callable[[K], L]) -> set[L]:
    return {mapping(point) if callable(mapping) else mapping[point] for point in support}
