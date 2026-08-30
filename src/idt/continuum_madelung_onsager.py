from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class ContinuumMadelungOnsagerError(ValueError):
    pass


@dataclass(frozen=True)
class MadelungRates:
    density_rate: np.ndarray
    schrodinger_phase_rate: np.ndarray
    onsager_phase_rate: np.ndarray
    combined_phase_rate: np.ndarray
    current: np.ndarray


def _finite_vector(values: Sequence[float], name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 1 or out.size == 0 or not np.all(np.isfinite(out)):
        raise ContinuumMadelungOnsagerError(f"{name} must be a finite non-empty one-dimensional vector")
    return out


def _positive_vector(values: Sequence[float], name: str) -> np.ndarray:
    out = _finite_vector(values, name)
    if np.any(out <= 0.0):
        raise ContinuumMadelungOnsagerError(f"{name} must be strictly positive")
    return out


def _positive_scalar(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out <= 0.0:
        raise ContinuumMadelungOnsagerError(f"{name} must be positive and finite")
    return out


def _nonnegative_scalar(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out < 0.0:
        raise ContinuumMadelungOnsagerError(f"{name} must be non-negative and finite")
    return out


def covariant_phase_gradient(
    phase_gradient: Sequence[float],
    connection: Sequence[float],
) -> np.ndarray:
    alpha_x = _finite_vector(phase_gradient, "phase_gradient")
    gauge = _finite_vector(connection, "connection")
    if gauge.shape != alpha_x.shape:
        raise ContinuumMadelungOnsagerError("phase_gradient and connection must have the same shape")
    return alpha_x - gauge


def temporal_current(
    mobility: Sequence[float],
    density: Sequence[float],
    covariant_gradient: Sequence[float],
) -> np.ndarray:
    m = _positive_vector(mobility, "mobility")
    rho = _positive_vector(density, "density")
    q = _finite_vector(covariant_gradient, "covariant_gradient")
    if m.shape != rho.shape or q.shape != rho.shape:
        raise ContinuumMadelungOnsagerError("mobility, density and covariant_gradient must have the same shape")
    return 2.0 * m * rho * q


def schrodinger_polar_rates(
    amplitude: Sequence[float],
    mobility: Sequence[float],
    covariant_gradient: Sequence[float],
    potential: Sequence[float],
    d_mobility_amplitude_gradient_dx: Sequence[float],
    d_mobility_density_q_dx: Sequence[float],
) -> tuple[np.ndarray, np.ndarray]:
    r = _positive_vector(amplitude, "amplitude")
    m = _positive_vector(mobility, "mobility")
    q = _finite_vector(covariant_gradient, "covariant_gradient")
    v = _finite_vector(potential, "potential")
    d_mrx = _finite_vector(d_mobility_amplitude_gradient_dx, "d_mobility_amplitude_gradient_dx")
    d_mrhoq = _finite_vector(d_mobility_density_q_dx, "d_mobility_density_q_dx")
    shape = r.shape
    if any(arr.shape != shape for arr in (m, q, v, d_mrx, d_mrhoq)):
        raise ContinuumMadelungOnsagerError("all polar-rate inputs must have the same shape")

    density_rate = -2.0 * d_mrhoq
    phase_rate = d_mrx / r - m * q * q - v
    return density_rate, phase_rate


def combined_madelung_rates(
    amplitude: Sequence[float],
    mobility: Sequence[float],
    covariant_gradient: Sequence[float],
    potential: Sequence[float],
    d_mobility_amplitude_gradient_dx: Sequence[float],
    d_mobility_density_q_dx: Sequence[float],
    onsager_mobility: float,
) -> MadelungRates:
    mu = _nonnegative_scalar(onsager_mobility, "onsager_mobility")
    r = _positive_vector(amplitude, "amplitude")
    m = _positive_vector(mobility, "mobility")
    q = _finite_vector(covariant_gradient, "covariant_gradient")
    density_rate, phase_h = schrodinger_polar_rates(
        r,
        m,
        q,
        potential,
        d_mobility_amplitude_gradient_dx,
        d_mobility_density_q_dx,
    )
    density = r * r
    current = temporal_current(m, density, q)
    phase_d = -mu * density_rate
    phase_total = phase_h + phase_d
    return MadelungRates(
        density_rate=density_rate,
        schrodinger_phase_rate=phase_h,
        onsager_phase_rate=phase_d,
        combined_phase_rate=phase_total,
        current=current,
    )


def compact_phase_balance_residual(
    combined_phase_rate: Sequence[float],
    density_rate: Sequence[float],
    schrodinger_phase_rate: Sequence[float],
    onsager_mobility: float,
) -> np.ndarray:
    alpha_t = _finite_vector(combined_phase_rate, "combined_phase_rate")
    rho_t = _finite_vector(density_rate, "density_rate")
    phase_h = _finite_vector(schrodinger_phase_rate, "schrodinger_phase_rate")
    mu = _nonnegative_scalar(onsager_mobility, "onsager_mobility")
    if rho_t.shape != alpha_t.shape or phase_h.shape != alpha_t.shape:
        raise ContinuumMadelungOnsagerError("phase-balance vectors must have the same shape")
    return alpha_t + mu * rho_t - phase_h


def gauge_reexpress_phase_gradient(
    phase_gradient: Sequence[float],
    connection: Sequence[float],
    gauge_gradient: Sequence[float],
) -> tuple[np.ndarray, np.ndarray]:
    alpha_x = _finite_vector(phase_gradient, "phase_gradient")
    a = _finite_vector(connection, "connection")
    chi_x = _finite_vector(gauge_gradient, "gauge_gradient")
    if a.shape != alpha_x.shape or chi_x.shape != alpha_x.shape:
        raise ContinuumMadelungOnsagerError("gauge re-expression vectors must have the same shape")
    return alpha_x + chi_x, a + chi_x


def constant_m_velocity(mobility: float, covariant_gradient: Sequence[float]) -> np.ndarray:
    m = _positive_scalar(mobility, "mobility")
    q = _finite_vector(covariant_gradient, "covariant_gradient")
    return 2.0 * m * q


def constant_m_velocity_rate(
    velocity: Sequence[float],
    velocity_gradient: Sequence[float],
    quantum_ratio_gradient: Sequence[float],
    potential_gradient: Sequence[float],
    density_current_second_derivative: Sequence[float],
    mobility: float,
    onsager_mobility: float,
) -> np.ndarray:
    u = _finite_vector(velocity, "velocity")
    u_x = _finite_vector(velocity_gradient, "velocity_gradient")
    qratio_x = _finite_vector(quantum_ratio_gradient, "quantum_ratio_gradient")
    v_x = _finite_vector(potential_gradient, "potential_gradient")
    rho_u_xx = _finite_vector(density_current_second_derivative, "density_current_second_derivative")
    m = _positive_scalar(mobility, "mobility")
    mu = _nonnegative_scalar(onsager_mobility, "onsager_mobility")
    shape = u.shape
    if any(arr.shape != shape for arr in (u_x, qratio_x, v_x, rho_u_xx)):
        raise ContinuumMadelungOnsagerError("velocity-balance vectors must have the same shape")
    return -u * u_x + 2.0 * m * m * qratio_x - 2.0 * m * v_x + 2.0 * mu * m * rho_u_xx


def linearized_characteristic_coefficients(
    wave_number: float,
    mobility: float,
    background_density: float,
    onsager_mobility: float,
) -> tuple[float, float, float]:
    k = float(wave_number)
    if not math.isfinite(k):
        raise ContinuumMadelungOnsagerError("wave_number must be finite")
    m = _positive_scalar(mobility, "mobility")
    rho0 = _positive_scalar(background_density, "background_density")
    mu = _nonnegative_scalar(onsager_mobility, "onsager_mobility")
    return (1.0, 2.0 * mu * m * rho0 * k * k, m * m * k**4)


def linearized_mode_roots(
    wave_number: float,
    mobility: float,
    background_density: float,
    onsager_mobility: float,
) -> tuple[complex, complex]:
    a, b, c = linearized_characteristic_coefficients(
        wave_number,
        mobility,
        background_density,
        onsager_mobility,
    )
    discriminant = complex(b * b - 4.0 * a * c, 0.0)
    root = cmath.sqrt(discriminant)
    return ((-b + root) / (2.0 * a), (-b - root) / (2.0 * a))


def characteristic_residual(root: complex, coefficients: tuple[float, float, float]) -> complex:
    if len(coefficients) != 3:
        raise ContinuumMadelungOnsagerError("coefficients must contain exactly three entries")
    a, b, c = (float(value) for value in coefficients)
    if not all(math.isfinite(value) for value in (a, b, c)):
        raise ContinuumMadelungOnsagerError("characteristic coefficients must be finite")
    z = complex(root)
    if not math.isfinite(z.real) or not math.isfinite(z.imag):
        raise ContinuumMadelungOnsagerError("root must be finite")
    return a * z * z + b * z + c
