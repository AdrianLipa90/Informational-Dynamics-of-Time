from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .internal_elapsed import elapsed_increment


class KeplerMemoryError(ValueError):
    pass


@dataclass(frozen=True)
class MemoryPhaseState:
    position: np.ndarray
    velocity: np.ndarray
    tau_internal: float = 0.0
    swept_area: float = 0.0


@dataclass(frozen=True)
class MemoryOrbitalElements:
    radius: float
    speed: float
    specific_energy: float
    angular_momentum: float
    areal_velocity: float
    eccentricity_vector: np.ndarray
    eccentricity: float
    semi_major_axis: float | None
    period: float | None
    orbit_class: str


def _vec2(value: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (2,):
        raise KeplerMemoryError(f"{name} must be a two-component vector")
    if not np.all(np.isfinite(arr)):
        raise KeplerMemoryError(f"{name} must be finite")
    return arr


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise KeplerMemoryError(f"{name} must be finite and strictly positive")
    return x


def memory_gravity(position: Sequence[float], mu_memory: float) -> np.ndarray:
    r = _vec2(position, "position")
    mu = _positive(mu_memory, "mu_memory")
    radius = float(np.linalg.norm(r))
    if radius <= 0.0:
        raise KeplerMemoryError("memory orbit is singular at zero radius")
    return -mu * r / (radius ** 3)


def specific_memory_energy(position: Sequence[float], velocity: Sequence[float], mu_memory: float) -> float:
    r = _vec2(position, "position")
    v = _vec2(velocity, "velocity")
    mu = _positive(mu_memory, "mu_memory")
    radius = float(np.linalg.norm(r))
    if radius <= 0.0:
        raise KeplerMemoryError("memory orbit is singular at zero radius")
    return float(0.5 * np.dot(v, v) - mu / radius)


def memory_angular_momentum(position: Sequence[float], velocity: Sequence[float]) -> float:
    r = _vec2(position, "position")
    v = _vec2(velocity, "velocity")
    return float(r[0] * v[1] - r[1] * v[0])


def memory_areal_velocity(position: Sequence[float], velocity: Sequence[float]) -> float:
    return 0.5 * memory_angular_momentum(position, velocity)


def memory_eccentricity_vector(position: Sequence[float], velocity: Sequence[float], mu_memory: float) -> np.ndarray:
    r = _vec2(position, "position")
    v = _vec2(velocity, "velocity")
    mu = _positive(mu_memory, "mu_memory")
    radius = float(np.linalg.norm(r))
    if radius <= 0.0:
        raise KeplerMemoryError("memory orbit is singular at zero radius")
    v2 = float(np.dot(v, v))
    rv = float(np.dot(r, v))
    return ((v2 - mu / radius) * r - rv * v) / mu


def kepler_semi_latus_rectum(angular_momentum: float, mu_memory: float) -> float:
    h = float(angular_momentum)
    mu = _positive(mu_memory, "mu_memory")
    if not math.isfinite(h):
        raise KeplerMemoryError("angular_momentum must be finite")
    return float((h * h) / mu)


def kepler_radius_from_true_anomaly(true_anomaly: float, angular_momentum: float, eccentricity: float, mu_memory: float) -> float:
    nu = float(true_anomaly)
    e = float(eccentricity)
    if not (math.isfinite(nu) and math.isfinite(e) and e >= 0.0):
        raise KeplerMemoryError("true_anomaly and non-negative eccentricity must be finite")
    p = kepler_semi_latus_rectum(angular_momentum, mu_memory)
    denom = 1.0 + e * math.cos(nu)
    if denom <= 0.0:
        raise KeplerMemoryError("true anomaly lies outside the admitted conic branch")
    return float(p / denom)


def kepler_period(semi_major_axis: float, mu_memory: float) -> float:
    a = _positive(semi_major_axis, "semi_major_axis")
    mu = _positive(mu_memory, "mu_memory")
    return float(2.0 * math.pi * math.sqrt((a ** 3) / mu))


def memory_orbital_elements(position: Sequence[float], velocity: Sequence[float], mu_memory: float, *, energy_tol: float = 1e-12) -> MemoryOrbitalElements:
    r = _vec2(position, "position")
    v = _vec2(velocity, "velocity")
    mu = _positive(mu_memory, "mu_memory")
    radius = float(np.linalg.norm(r))
    speed = float(np.linalg.norm(v))
    energy = specific_memory_energy(r, v, mu)
    h = memory_angular_momentum(r, v)
    evec = memory_eccentricity_vector(r, v, mu)
    ecc = float(np.linalg.norm(evec))
    scale = max(1.0, abs(mu / radius), 0.5 * speed * speed)
    tol = abs(float(energy_tol)) * scale
    if energy < -tol:
        orbit_class = "BOUND_ELLIPTIC"
        semi_major = float(-mu / (2.0 * energy))
        period = kepler_period(semi_major, mu)
    elif energy > tol:
        orbit_class = "UNBOUND_HYPERBOLIC"
        semi_major = float(-mu / (2.0 * energy))
        period = None
    else:
        orbit_class = "PARABOLIC_BOUNDARY"
        semi_major = None
        period = None
    return MemoryOrbitalElements(radius, speed, energy, h, 0.5 * h, evec, ecc, semi_major, period, orbit_class)


def apply_memory_impulse(state: MemoryPhaseState, delta_velocity: Sequence[float]) -> MemoryPhaseState:
    dv = _vec2(delta_velocity, "delta_velocity")
    return MemoryPhaseState(_vec2(state.position, "state.position").copy(), _vec2(state.velocity, "state.velocity") + dv, float(state.tau_internal), float(state.swept_area))


def kepler_memory_step(state: MemoryPhaseState, mu_memory: float, delta_tau: float) -> MemoryPhaseState:
    dt = _positive(delta_tau, "delta_tau")
    r0 = _vec2(state.position, "state.position")
    v0 = _vec2(state.velocity, "state.velocity")
    tau0 = float(state.tau_internal)
    area0 = float(state.swept_area)
    if not (math.isfinite(tau0) and math.isfinite(area0)):
        raise KeplerMemoryError("state tau_internal and swept_area must be finite")
    a0 = memory_gravity(r0, mu_memory)
    r1 = r0 + v0 * dt + 0.5 * a0 * dt * dt
    a1 = memory_gravity(r1, mu_memory)
    v1 = v0 + 0.5 * (a0 + a1) * dt
    swept = 0.5 * float(r0[0] * r1[1] - r0[1] * r1[0])
    return MemoryPhaseState(r1, v1, tau0 + dt, area0 + swept)


def temporal_memory_step(state: MemoryPhaseState, mu_memory: float, activity: float, delta_lambda: float, *, reference_activity: float = 1.0) -> MemoryPhaseState:
    dtau = elapsed_increment(activity, delta_lambda, reference_activity=reference_activity)
    return kepler_memory_step(state, mu_memory, dtau)


def propagate_memory_orbit(state: MemoryPhaseState, mu_memory: float, delta_tau: float, n_steps: int) -> list[MemoryPhaseState]:
    if not isinstance(n_steps, int) or n_steps <= 0:
        raise KeplerMemoryError("n_steps must be a positive integer")
    dt = _positive(delta_tau, "delta_tau")
    out = [state]
    current = state
    for _ in range(n_steps):
        current = kepler_memory_step(current, mu_memory, dt)
        out.append(current)
    return out
