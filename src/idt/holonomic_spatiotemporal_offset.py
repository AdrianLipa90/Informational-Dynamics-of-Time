from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


HBAR_SI = 1.054_571_817e-34


class HolonomicOffsetError(ValueError):
    pass


@dataclass(frozen=True)
class HolonomicOffsetAudit:
    spatial_offset: np.ndarray
    coordinate_time_offset: float
    geometric_phase: float
    winding: int
    total_phase: float
    closure_residual: float


def _finite_scalar(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise HolonomicOffsetError(f"{name} must be finite")
    return out


def principal_phase(value: float) -> float:
    x = _finite_scalar(value, "phase")
    return float(math.atan2(math.sin(x), math.cos(x)))


def total_holonomic_phase(
    p_dot_dx: float,
    energy: float,
    delta_t: float,
    geometric_phase: float,
    *,
    hbar: float = HBAR_SI,
) -> float:
    p_dx = _finite_scalar(p_dot_dx, "p_dot_dx")
    e = _finite_scalar(energy, "energy")
    dt = _finite_scalar(delta_t, "delta_t")
    gamma = _finite_scalar(geometric_phase, "geometric_phase")
    hb = _finite_scalar(hbar, "hbar")
    if hb <= 0.0:
        raise HolonomicOffsetError("hbar must be positive")
    return (p_dx - e * dt) / hb + gamma


def temporal_offset_from_phase_closure(
    p_dot_dx: float,
    energy: float,
    geometric_phase: float,
    winding: int,
    *,
    hbar: float = HBAR_SI,
) -> float:
    p_dx = _finite_scalar(p_dot_dx, "p_dot_dx")
    e = _finite_scalar(energy, "energy")
    gamma = _finite_scalar(geometric_phase, "geometric_phase")
    hb = _finite_scalar(hbar, "hbar")
    if e <= 0.0:
        raise HolonomicOffsetError("energy must be positive")
    if hb <= 0.0:
        raise HolonomicOffsetError("hbar must be positive")
    if not isinstance(winding, int):
        raise HolonomicOffsetError("winding must be an integer")
    return (p_dx + hb * gamma - 2.0 * math.pi * winding * hb) / e


def phase_closure_residual(
    p_dot_dx: float,
    energy: float,
    delta_t: float,
    geometric_phase: float,
    winding: int,
    *,
    hbar: float = HBAR_SI,
) -> float:
    phi = total_holonomic_phase(
        p_dot_dx,
        energy,
        delta_t,
        geometric_phase,
        hbar=hbar,
    )
    return principal_phase(phi - 2.0 * math.pi * winding)


def calibrated_elapsed_time(
    segment_dt: Sequence[float],
    relational_lapse: Sequence[float],
) -> float:
    dt = np.asarray(segment_dt, dtype=float)
    lapse = np.asarray(relational_lapse, dtype=float)
    if dt.ndim != 1 or lapse.ndim != 1 or dt.shape != lapse.shape or dt.size == 0:
        raise HolonomicOffsetError("segment_dt and relational_lapse must be equal non-empty one-dimensional arrays")
    if not np.all(np.isfinite(dt)) or not np.all(np.isfinite(lapse)):
        raise HolonomicOffsetError("elapsed inputs must be finite")
    if np.any(dt <= 0.0):
        raise HolonomicOffsetError("segment_dt must be positive")
    if np.any(lapse <= 0.0):
        raise HolonomicOffsetError("relational_lapse must be positive")
    return float(np.dot(dt, lapse))


def temporal_offset_divergence(
    elapsed_a: Sequence[float],
    elapsed_b: Sequence[float],
) -> tuple[np.ndarray, float]:
    a = np.asarray(elapsed_a, dtype=float)
    b = np.asarray(elapsed_b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.shape != b.shape or a.size == 0:
        raise HolonomicOffsetError("elapsed lineages must be equal non-empty one-dimensional arrays")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise HolonomicOffsetError("elapsed lineages must be finite")
    delta = b - a
    return delta, float(np.linalg.norm(delta))


def audit_phase_closed_offset(
    spatial_offset: Sequence[float],
    momentum: Sequence[float],
    energy: float,
    geometric_phase: float,
    winding: int,
    *,
    hbar: float = HBAR_SI,
) -> HolonomicOffsetAudit:
    dx = np.asarray(spatial_offset, dtype=float)
    p = np.asarray(momentum, dtype=float)
    if dx.ndim != 1 or p.ndim != 1 or dx.shape != p.shape or dx.size == 0:
        raise HolonomicOffsetError("spatial_offset and momentum must be equal non-empty one-dimensional arrays")
    if not np.all(np.isfinite(dx)) or not np.all(np.isfinite(p)):
        raise HolonomicOffsetError("spatial_offset and momentum must be finite")
    p_dot_dx = float(np.dot(p, dx))
    dt = temporal_offset_from_phase_closure(
        p_dot_dx,
        energy,
        geometric_phase,
        winding,
        hbar=hbar,
    )
    total = total_holonomic_phase(
        p_dot_dx,
        energy,
        dt,
        geometric_phase,
        hbar=hbar,
    )
    residual = principal_phase(total - 2.0 * math.pi * winding)
    return HolonomicOffsetAudit(
        spatial_offset=dx.copy(),
        coordinate_time_offset=dt,
        geometric_phase=float(geometric_phase),
        winding=winding,
        total_phase=total,
        closure_residual=residual,
    )
