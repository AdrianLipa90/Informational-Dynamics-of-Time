from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from .relational_precedence import Occurrence, serial_now_frontier
from .temporal_density_quantile_front import (
    QuantileFront,
    TemporalDensityFrontError,
    audit_quantile_front,
    quantile_position,
)


class NowMaterialBindingError(ValueError):
    pass


@dataclass(frozen=True)
class BoundNowMarker:
    occurrence: Occurrence
    material_front: QuantileFront


def reflected_mass_fraction(q: float) -> float:
    value = float(q)
    if not math.isfinite(value) or not (0.0 < value < 1.0):
        raise NowMaterialBindingError("mass fraction must lie strictly between zero and one")
    return 1.0 - value


def symmetric_mass_fraction() -> float:
    return 0.5


def exchange_fixed_point_residual(q: float) -> float:
    value = float(q)
    if not math.isfinite(value) or not (0.0 < value < 1.0):
        raise NowMaterialBindingError("mass fraction must lie strictly between zero and one")
    return value - reflected_mass_fraction(value)


def mirror_quantile_residual(
    grid: Sequence[float],
    density: Sequence[float],
    center: float,
    q: float,
) -> float:
    c = float(center)
    if not math.isfinite(c):
        raise NowMaterialBindingError("center must be finite")
    try:
        left = quantile_position(grid, density, q)
        right = quantile_position(grid, density, reflected_mass_fraction(q))
    except TemporalDensityFrontError as exc:
        raise NowMaterialBindingError(str(exc)) from exc
    return left + right - 2.0 * c


def bind_serial_now_to_quantile(
    occurrences: Sequence[Occurrence],
    grid: Sequence[float],
    density: Sequence[float],
    current: Sequence[float],
    *,
    mass_fraction: float = 0.5,
    left_boundary_current: float = 0.0,
) -> BoundNowMarker:
    frontier = serial_now_frontier(occurrences)
    if len(frontier) != 1:
        raise NowMaterialBindingError("serial binding requires exactly one supported NOW occurrence")
    try:
        material = audit_quantile_front(
            grid,
            density,
            current,
            mass_fraction,
            left_boundary_current=left_boundary_current,
        )
    except TemporalDensityFrontError as exc:
        raise NowMaterialBindingError(str(exc)) from exc
    return BoundNowMarker(frontier[0], material)


def bind_concurrent_now_to_quantiles(
    frontier_ids: Sequence[str],
    branch_fields: Mapping[str, tuple[Sequence[float], Sequence[float], Sequence[float]]],
    *,
    mass_fraction: float = 0.5,
) -> dict[str, QuantileFront]:
    ids = tuple(frontier_ids)
    if not ids or len(set(ids)) != len(ids):
        raise NowMaterialBindingError("frontier_ids must be unique and non-empty")
    if set(ids) != set(branch_fields):
        raise NowMaterialBindingError("branch fields must match the concurrent frontier IDs exactly")
    out: dict[str, QuantileFront] = {}
    for branch_id in ids:
        grid, density, current = branch_fields[branch_id]
        try:
            out[branch_id] = audit_quantile_front(grid, density, current, mass_fraction)
        except TemporalDensityFrontError as exc:
            raise NowMaterialBindingError(f"branch {branch_id}: {exc}") from exc
    return out


def symmetric_density_about(grid: Sequence[float], density: Sequence[float], center: float, *, atol: float = 1e-12) -> bool:
    x = np.asarray(grid, dtype=float)
    rho = np.asarray(density, dtype=float)
    c = float(center)
    if x.ndim != 1 or rho.ndim != 1 or x.shape != rho.shape or x.size < 2:
        raise NowMaterialBindingError("grid and density must have equal one-dimensional shape")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(rho)) or not math.isfinite(c):
        raise NowMaterialBindingError("symmetry inputs must be finite")
    if np.any(np.diff(x) <= 0.0) or np.any(rho < 0.0):
        raise NowMaterialBindingError("grid must increase and density must be non-negative")
    reflected_x = 2.0 * c - x
    reflected_rho = np.interp(reflected_x, x, rho, left=np.nan, right=np.nan)
    valid = np.isfinite(reflected_rho)
    if not np.any(valid):
        raise NowMaterialBindingError("grid does not resolve reflection about center")
    return bool(np.allclose(rho[valid], reflected_rho[valid], rtol=0.0, atol=atol))
