from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class ContinuumPhaseOnsagerError(ValueError):
    pass


@dataclass(frozen=True)
class PhaseOnsagerAudit:
    energy: float
    functional_gradient: np.ndarray
    phase_velocity: np.ndarray
    dissipation_rate: float


def _positive_scalar(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out <= 0.0:
        raise ContinuumPhaseOnsagerError(f"{name} must be positive and finite")
    return out


def _vector(values: Sequence[float], name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 1 or out.size < 3 or not np.all(np.isfinite(out)):
        raise ContinuumPhaseOnsagerError(f"{name} must be a finite one-dimensional vector with at least three entries")
    return out


def periodic_covariant_phase_gradient(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    spacing: float,
) -> np.ndarray:
    alpha = _vector(phase, "phase")
    connection = _vector(connection_edge, "connection_edge")
    h = _positive_scalar(spacing, "spacing")
    if connection.shape != alpha.shape:
        raise ContinuumPhaseOnsagerError("connection_edge must have one periodic edge value per phase vertex")
    return (np.roll(alpha, -1) - alpha) / h - connection


def phase_gradient_energy_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
) -> float:
    alpha = _vector(phase, "phase")
    connection = _vector(connection_edge, "connection_edge")
    coefficient = _vector(edge_coefficient, "edge_coefficient")
    h = _positive_scalar(spacing, "spacing")
    if connection.shape != alpha.shape or coefficient.shape != alpha.shape:
        raise ContinuumPhaseOnsagerError("periodic edge arrays must match the phase shape")
    if np.any(coefficient <= 0.0):
        raise ContinuumPhaseOnsagerError("edge_coefficient must be strictly positive")
    q = periodic_covariant_phase_gradient(alpha, connection, h)
    return float(h * np.dot(coefficient, q * q))


def phase_energy_vertex_derivative_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
) -> np.ndarray:
    alpha = _vector(phase, "phase")
    connection = _vector(connection_edge, "connection_edge")
    coefficient = _vector(edge_coefficient, "edge_coefficient")
    h = _positive_scalar(spacing, "spacing")
    if connection.shape != alpha.shape or coefficient.shape != alpha.shape:
        raise ContinuumPhaseOnsagerError("periodic edge arrays must match the phase shape")
    if np.any(coefficient <= 0.0):
        raise ContinuumPhaseOnsagerError("edge_coefficient must be strictly positive")
    q = periodic_covariant_phase_gradient(alpha, connection, h)
    flux = coefficient * q
    return 2.0 * (np.roll(flux, 1) - flux)


def phase_functional_gradient_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
) -> np.ndarray:
    h = _positive_scalar(spacing, "spacing")
    return phase_energy_vertex_derivative_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        h,
    ) / h


def onsager_phase_velocity_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
    mobility: float,
) -> np.ndarray:
    mu = _positive_scalar(mobility, "mobility")
    gradient = phase_functional_gradient_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        spacing,
    )
    return -mu * gradient


def onsager_energy_rate_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
    mobility: float,
) -> float:
    h = _positive_scalar(spacing, "spacing")
    mu = _positive_scalar(mobility, "mobility")
    gradient = phase_functional_gradient_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        h,
    )
    return -mu * h * float(np.dot(gradient, gradient))


def audit_phase_onsager_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    edge_coefficient: Sequence[float],
    spacing: float,
    mobility: float,
) -> PhaseOnsagerAudit:
    energy = phase_gradient_energy_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        spacing,
    )
    gradient = phase_functional_gradient_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        spacing,
    )
    velocity = onsager_phase_velocity_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        spacing,
        mobility,
    )
    rate = onsager_energy_rate_periodic(
        phase,
        connection_edge,
        edge_coefficient,
        spacing,
        mobility,
    )
    return PhaseOnsagerAudit(
        energy=energy,
        functional_gradient=gradient,
        phase_velocity=velocity,
        dissipation_rate=rate,
    )


def gauge_transform_periodic(
    phase: Sequence[float],
    connection_edge: Sequence[float],
    gauge_phase: Sequence[float],
    spacing: float,
) -> tuple[np.ndarray, np.ndarray]:
    alpha = _vector(phase, "phase")
    connection = _vector(connection_edge, "connection_edge")
    chi = _vector(gauge_phase, "gauge_phase")
    h = _positive_scalar(spacing, "spacing")
    if connection.shape != alpha.shape or chi.shape != alpha.shape:
        raise ContinuumPhaseOnsagerError("gauge arrays must match the phase shape")
    transformed_phase = alpha + chi
    transformed_connection = connection + (np.roll(chi, -1) - chi) / h
    return transformed_phase, transformed_connection


def phase_only_state_tangent(
    amplitudes: Sequence[complex],
    phase_velocity: Sequence[float],
) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    velocity = np.asarray(phase_velocity, dtype=float)
    if psi.ndim != 1 or velocity.ndim != 1 or psi.shape != velocity.shape or psi.size < 1:
        raise ContinuumPhaseOnsagerError("amplitudes and phase_velocity must be equal non-empty vectors")
    if not np.all(np.isfinite(psi)) or not np.all(np.isfinite(velocity)):
        raise ContinuumPhaseOnsagerError("state tangent inputs must be finite")
    return 1j * velocity * psi


def density_rate_from_tangent(
    amplitudes: Sequence[complex],
    tangent: Sequence[complex],
) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    dpsi = np.asarray(tangent, dtype=complex)
    if psi.ndim != 1 or dpsi.ndim != 1 or psi.shape != dpsi.shape or psi.size < 1:
        raise ContinuumPhaseOnsagerError("amplitudes and tangent must be equal non-empty vectors")
    if not np.all(np.isfinite(psi)) or not np.all(np.isfinite(dpsi)):
        raise ContinuumPhaseOnsagerError("density-rate inputs must be finite")
    return 2.0 * np.real(np.conj(psi) * dpsi)


def periodic_laplacian(values: Sequence[float], spacing: float) -> np.ndarray:
    x = _vector(values, "values")
    h = _positive_scalar(spacing, "spacing")
    return (np.roll(x, -1) - 2.0 * x + np.roll(x, 1)) / (h * h)


def constant_coefficient_q_velocity(
    covariant_gradient: Sequence[float],
    coefficient: float,
    mobility: float,
    spacing: float,
) -> np.ndarray:
    q = _vector(covariant_gradient, "covariant_gradient")
    c = _positive_scalar(coefficient, "coefficient")
    mu = _positive_scalar(mobility, "mobility")
    h = _positive_scalar(spacing, "spacing")
    return 2.0 * mu * c * periodic_laplacian(q, h)


def constant_coefficient_current(
    covariant_gradient: Sequence[float],
    coefficient: float,
) -> np.ndarray:
    q = _vector(covariant_gradient, "covariant_gradient")
    c = _positive_scalar(coefficient, "coefficient")
    return 2.0 * c * q


def constant_coefficient_current_velocity(
    current: Sequence[float],
    coefficient: float,
    mobility: float,
    spacing: float,
) -> np.ndarray:
    j = _vector(current, "current")
    c = _positive_scalar(coefficient, "coefficient")
    mu = _positive_scalar(mobility, "mobility")
    h = _positive_scalar(spacing, "spacing")
    return 2.0 * mu * c * periodic_laplacian(j, h)
