from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class TemporalDensityFrontError(ValueError):
    pass


@dataclass(frozen=True)
class QuantileFront:
    mass_fraction: float
    position: float
    local_density: float
    local_current: float
    theta_velocity: float


def _grid(values: Sequence[float]) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.all(np.isfinite(x)):
        raise TemporalDensityFrontError("grid must be a finite one-dimensional vector with at least two points")
    if np.any(np.diff(x) <= 0.0):
        raise TemporalDensityFrontError("grid must be strictly increasing")
    return x


def _field(values: Sequence[float], size: int, name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 1 or out.size != size or not np.all(np.isfinite(out)):
        raise TemporalDensityFrontError(f"{name} must be a finite vector matching the grid")
    return out


def total_mass(grid: Sequence[float], density: Sequence[float]) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    if np.any(rho < 0.0):
        raise TemporalDensityFrontError("density must be non-negative")
    mass = float(np.trapezoid(rho, x))
    if not math.isfinite(mass) or mass <= 0.0:
        raise TemporalDensityFrontError("density must have positive finite total mass")
    return mass


def cumulative_mass_fraction(grid: Sequence[float], density: Sequence[float]) -> np.ndarray:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    if np.any(rho < 0.0):
        raise TemporalDensityFrontError("density must be non-negative")
    dx = np.diff(x)
    cell_mass = 0.5 * (rho[:-1] + rho[1:]) * dx
    cumulative = np.empty_like(x)
    cumulative[0] = 0.0
    cumulative[1:] = np.cumsum(cell_mass)
    mass = float(cumulative[-1])
    if not math.isfinite(mass) or mass <= 0.0:
        raise TemporalDensityFrontError("density must have positive finite total mass")
    return cumulative / mass


def quantile_position(
    grid: Sequence[float],
    density: Sequence[float],
    mass_fraction: float,
) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    q = float(mass_fraction)
    if not math.isfinite(q) or not (0.0 < q < 1.0):
        raise TemporalDensityFrontError("mass_fraction must lie strictly between zero and one")
    c = cumulative_mass_fraction(x, rho)
    hi = int(np.searchsorted(c, q, side="left"))
    if hi <= 0 or hi >= x.size:
        raise TemporalDensityFrontError("quantile is outside the resolved interior")
    lo = hi - 1
    dc = float(c[hi] - c[lo])
    if dc <= 1e-15:
        raise TemporalDensityFrontError("quantile lies on an unresolved zero-mass plateau")
    t = (q - float(c[lo])) / dc
    return float(x[lo] + t * (x[hi] - x[lo]))


def interpolate_field(grid: Sequence[float], values: Sequence[float], position: float) -> float:
    x = _grid(grid)
    y = _field(values, x.size, "values")
    pos = float(position)
    if not math.isfinite(pos) or pos < float(x[0]) or pos > float(x[-1]):
        raise TemporalDensityFrontError("position must lie inside the grid")
    return float(np.interp(pos, x, y))


def quantile_velocity(
    local_density: float,
    local_current: float,
    *,
    left_boundary_current: float = 0.0,
) -> float:
    rho = float(local_density)
    current = float(local_current)
    left = float(left_boundary_current)
    if not all(math.isfinite(v) for v in (rho, current, left)):
        raise TemporalDensityFrontError("local front inputs must be finite")
    if rho <= 0.0:
        raise TemporalDensityFrontError("local quantile density must be positive")
    return (current - left) / rho


def audit_quantile_front(
    grid: Sequence[float],
    density: Sequence[float],
    current: Sequence[float],
    mass_fraction: float,
    *,
    left_boundary_current: float = 0.0,
) -> QuantileFront:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    j = _field(current, x.size, "current")
    pos = quantile_position(x, rho, mass_fraction)
    local_rho = interpolate_field(x, rho, pos)
    local_j = interpolate_field(x, j, pos)
    velocity = quantile_velocity(local_rho, local_j, left_boundary_current=left_boundary_current)
    return QuantileFront(
        mass_fraction=float(mass_fraction),
        position=pos,
        local_density=local_rho,
        local_current=local_j,
        theta_velocity=velocity,
    )


def discrete_cumulative_mass_rate(
    edge_currents: Sequence[float],
    cut_edge: int,
    *,
    left_boundary_current: float = 0.0,
) -> float:
    j = np.asarray(edge_currents, dtype=float)
    if j.ndim != 1 or j.size == 0 or not np.all(np.isfinite(j)):
        raise TemporalDensityFrontError("edge_currents must be a finite non-empty vector")
    if not isinstance(cut_edge, int) or isinstance(cut_edge, bool) or not (0 <= cut_edge < j.size):
        raise TemporalDensityFrontError("cut_edge must index an internal cumulative boundary")
    left = float(left_boundary_current)
    if not math.isfinite(left):
        raise TemporalDensityFrontError("left_boundary_current must be finite")
    return left - float(j[cut_edge])


def barycenter(grid: Sequence[float], density: Sequence[float]) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    mass = total_mass(x, rho)
    return float(np.trapezoid(x * rho, x) / mass)


def barycenter_rate_zero_flux(
    grid: Sequence[float],
    density: Sequence[float],
    current: Sequence[float],
) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    j = _field(current, x.size, "current")
    mass = total_mass(x, rho)
    return float(np.trapezoid(j, x) / mass)


def variance(grid: Sequence[float], density: Sequence[float]) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    mass = total_mass(x, rho)
    mean = barycenter(x, rho)
    return float(np.trapezoid((x - mean) ** 2 * rho, x) / mass)


def variance_rate_zero_flux(
    grid: Sequence[float],
    density: Sequence[float],
    current: Sequence[float],
) -> float:
    x = _grid(grid)
    rho = _field(density, x.size, "density")
    j = _field(current, x.size, "current")
    mass = total_mass(x, rho)
    mean = barycenter(x, rho)
    return float(2.0 * np.trapezoid((x - mean) * j, x) / mass)
