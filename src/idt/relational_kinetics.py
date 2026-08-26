from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence


class RelationalKineticsError(ValueError):
    pass


def _positive_finite(x: float, name: str) -> float:
    v = float(x)
    if not math.isfinite(v) or v <= 0.0:
        raise RelationalKineticsError(f"{name} must be finite and strictly positive")
    return v


def pair_mobility(rho_a: float, rho_b: float, eta_a: float, eta_b: float) -> float:
    """Symmetric relational mobility sqrt(rho_a*rho_b) / mean(eta_a,eta_b)."""
    ra = _positive_finite(rho_a, "rho_a")
    rb = _positive_finite(rho_b, "rho_b")
    ea = _positive_finite(eta_a, "eta_a")
    eb = _positive_finite(eta_b, "eta_b")
    return math.sqrt(ra * rb) / (0.5 * (ea + eb))


@dataclass(frozen=True)
class DirectedRates:
    mobility: float
    edge_drive: float
    forward: float
    reverse: float
    affinity_bits: float


def directed_rates(
    rho_a: float,
    rho_b: float,
    eta_a: float,
    eta_b: float,
    edge_drive: float,
) -> DirectedRates:
    """Minimal positive pair rates with an antisymmetric dimensionless drive."""
    A = float(edge_drive)
    if not math.isfinite(A):
        raise RelationalKineticsError("edge_drive must be finite")
    M = pair_mobility(rho_a, rho_b, eta_a, eta_b)
    fwd = M * math.exp(0.5 * A)
    rev = M * math.exp(-0.5 * A)
    affinity = math.log2(fwd / rev)
    return DirectedRates(M, A, fwd, rev, affinity)


def exact_edge_drive(v_a: float, v_b: float) -> float:
    a = float(v_a)
    b = float(v_b)
    if not (math.isfinite(a) and math.isfinite(b)):
        raise RelationalKineticsError("state potentials must be finite")
    return b - a


def cycle_drive(edge_drives: Sequence[float]) -> float:
    values = [float(x) for x in edge_drives]
    if len(values) == 0 or not all(math.isfinite(x) for x in values):
        raise RelationalKineticsError("cycle requires finite edge drives")
    return float(sum(values))
