from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class OnsagerHalfSeamError(ValueError):
    pass


@dataclass(frozen=True)
class SeamLockState:
    mismatch: float
    defect: float
    gradient: float
    theta_velocity: float
    lyapunov_rate: float


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise OnsagerHalfSeamError(f"{name} must be finite")
    return out


def principal_phase(value: float) -> float:
    x = _finite(value, "phase")
    return math.atan2(math.sin(x), math.cos(x))


def seam_defect_potential(
    mismatch: float,
    magnitude_left: float,
    magnitude_right: float,
) -> float:
    delta = _finite(mismatch, "mismatch")
    r0 = _finite(magnitude_left, "magnitude_left")
    r1 = _finite(magnitude_right, "magnitude_right")
    if r0 <= 0.0 or r1 <= 0.0:
        raise OnsagerHalfSeamError("seam magnitudes must be positive")
    return 0.25 * (r0 * r0 + r1 * r1 - 2.0 * r0 * r1 * math.cos(delta))


def seam_defect_gradient(
    mismatch: float,
    magnitude_left: float,
    magnitude_right: float,
) -> float:
    delta = _finite(mismatch, "mismatch")
    r0 = _finite(magnitude_left, "magnitude_left")
    r1 = _finite(magnitude_right, "magnitude_right")
    if r0 <= 0.0 or r1 <= 0.0:
        raise OnsagerHalfSeamError("seam magnitudes must be positive")
    return 0.5 * r0 * r1 * math.sin(delta)


def seam_onsager_velocity(
    mismatch: float,
    magnitude_left: float,
    magnitude_right: float,
    mobility: float,
) -> float:
    mu = _finite(mobility, "mobility")
    if mu <= 0.0:
        raise OnsagerHalfSeamError("mobility must be positive")
    return -mu * seam_defect_gradient(mismatch, magnitude_left, magnitude_right)


def seam_lyapunov_rate(
    mismatch: float,
    magnitude_left: float,
    magnitude_right: float,
    mobility: float,
) -> float:
    mu = _finite(mobility, "mobility")
    if mu <= 0.0:
        raise OnsagerHalfSeamError("mobility must be positive")
    grad = seam_defect_gradient(mismatch, magnitude_left, magnitude_right)
    return -mu * grad * grad


def audit_seam_lock_state(
    mismatch: float,
    magnitude_left: float,
    magnitude_right: float,
    mobility: float,
) -> SeamLockState:
    delta = principal_phase(mismatch)
    defect = seam_defect_potential(delta, magnitude_left, magnitude_right)
    gradient = seam_defect_gradient(delta, magnitude_left, magnitude_right)
    velocity = seam_onsager_velocity(delta, magnitude_left, magnitude_right, mobility)
    rate = seam_lyapunov_rate(delta, magnitude_left, magnitude_right, mobility)
    return SeamLockState(
        mismatch=delta,
        defect=defect,
        gradient=gradient,
        theta_velocity=velocity,
        lyapunov_rate=rate,
    )


def integrate_single_seam(
    mismatch0: float,
    magnitude_left: float,
    magnitude_right: float,
    mobility: float,
    delta_theta: float,
    *,
    steps: int = 1000,
) -> np.ndarray:
    if not isinstance(steps, int) or isinstance(steps, bool) or steps <= 0:
        raise OnsagerHalfSeamError("steps must be a positive integer")
    total = _finite(delta_theta, "delta_theta")
    if total < 0.0:
        raise OnsagerHalfSeamError("delta_theta must be non-negative")
    r0 = _finite(magnitude_left, "magnitude_left")
    r1 = _finite(magnitude_right, "magnitude_right")
    mu = _finite(mobility, "mobility")
    if r0 <= 0.0 or r1 <= 0.0 or mu <= 0.0:
        raise OnsagerHalfSeamError("magnitudes and mobility must be positive")

    out = np.empty(steps + 1, dtype=float)
    out[0] = principal_phase(mismatch0)
    if total == 0.0:
        out[1:] = out[0]
        return out
    h = total / steps
    for k in range(steps):
        delta = out[k]
        # RK4 for d delta / d Theta = -K sin(delta).
        def f(x: float) -> float:
            return -0.5 * mu * r0 * r1 * math.sin(x)

        k1 = f(delta)
        k2 = f(delta + 0.5 * h * k1)
        k3 = f(delta + 0.5 * h * k2)
        k4 = f(delta + h * k3)
        out[k + 1] = principal_phase(delta + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4))
    return out


def network_onsager_velocity(
    mismatches: Sequence[float],
    gradient: Sequence[float],
    onsager_matrix: Sequence[Sequence[float]],
) -> tuple[np.ndarray, float]:
    delta = np.asarray(mismatches, dtype=float)
    grad = np.asarray(gradient, dtype=float)
    g = np.asarray(onsager_matrix, dtype=float)
    if delta.ndim != 1 or grad.ndim != 1 or delta.shape != grad.shape or delta.size == 0:
        raise OnsagerHalfSeamError("mismatches and gradient must be equal non-empty vectors")
    if g.shape != (delta.size, delta.size):
        raise OnsagerHalfSeamError("onsager_matrix must be square with seam dimension")
    if not np.all(np.isfinite(delta)) or not np.all(np.isfinite(grad)) or not np.all(np.isfinite(g)):
        raise OnsagerHalfSeamError("network inputs must be finite")
    if not np.allclose(g, g.T, atol=1e-12, rtol=0.0):
        raise OnsagerHalfSeamError("onsager_matrix must be symmetric")
    eig = np.linalg.eigvalsh(g)
    if float(np.min(eig)) < -1e-12:
        raise OnsagerHalfSeamError("onsager_matrix must be positive semidefinite")
    velocity = -(g @ grad)
    lyapunov_rate = -float(grad @ g @ grad)
    return velocity, lyapunov_rate


def resonant_mismatch(
    phase_i: float,
    phase_j: float,
    winding_i: int,
    winding_j: int,
    connection_phase: float,
) -> float:
    if not isinstance(winding_i, int) or isinstance(winding_i, bool):
        raise OnsagerHalfSeamError("winding_i must be an integer")
    if not isinstance(winding_j, int) or isinstance(winding_j, bool):
        raise OnsagerHalfSeamError("winding_j must be an integer")
    pi = _finite(phase_i, "phase_i")
    pj = _finite(phase_j, "phase_j")
    a = _finite(connection_phase, "connection_phase")
    return principal_phase(winding_j * pi - winding_i * pj - a)


def resonant_defect_potential(mismatch: float, stiffness: float) -> float:
    delta = _finite(mismatch, "mismatch")
    rho = _finite(stiffness, "stiffness")
    if rho <= 0.0:
        raise OnsagerHalfSeamError("stiffness must be positive")
    return rho * (1.0 - math.cos(delta))


def resonant_onsager_velocity(mismatch: float, stiffness: float, mobility: float) -> float:
    delta = _finite(mismatch, "mismatch")
    rho = _finite(stiffness, "stiffness")
    mu = _finite(mobility, "mobility")
    if rho <= 0.0 or mu <= 0.0:
        raise OnsagerHalfSeamError("stiffness and mobility must be positive")
    return -mu * rho * math.sin(delta)


def locked_rate_residual(
    omega_i: float,
    omega_j: float,
    winding_i: int,
    winding_j: int,
    connection_rate: float = 0.0,
) -> float:
    if not isinstance(winding_i, int) or isinstance(winding_i, bool):
        raise OnsagerHalfSeamError("winding_i must be an integer")
    if not isinstance(winding_j, int) or isinstance(winding_j, bool):
        raise OnsagerHalfSeamError("winding_j must be an integer")
    oi = _finite(omega_i, "omega_i")
    oj = _finite(omega_j, "omega_j")
    oa = _finite(connection_rate, "connection_rate")
    return winding_j * oi - winding_i * oj - oa
