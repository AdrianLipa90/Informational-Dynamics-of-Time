from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .moving_seam_connection_work import (
    MovingSeamConnectionError,
    connection_phase_gradient,
    conservative_seam_power,
)
from .schrodinger_onsager_seam_balance import (
    SchrodingerOnsagerBalanceError,
    onsager_dissipation,
    schrodinger_seam_power,
)


class TemporalSeamCurvatureError(ValueError):
    pass


@dataclass(frozen=True)
class TemporalSeamCurvatureAudit:
    covariant_schrodinger_power: float
    curvature_power: float
    curvature_dissipation: float
    vertex_phase_dissipation: float
    gauge_native_balance_rate: float
    moving_balance_rate: float
    decomposition_residual: float


def _state(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    if psi.ndim != 1 or psi.size == 0 or not np.all(np.isfinite(psi)):
        raise TemporalSeamCurvatureError("amplitudes must be a finite non-empty vector")
    norm = float(np.linalg.norm(psi))
    if not math.isfinite(norm) or norm <= 0.0:
        raise TemporalSeamCurvatureError("amplitudes must have positive finite norm")
    return psi


def _vertex_vector(values: Sequence[float], size: int, *, name: str) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.shape != (size,) or not np.all(np.isfinite(x)):
        raise TemporalSeamCurvatureError(f"{name} must be finite with frame_count entries")
    return x


def _edge_vector(values: Sequence[float], size: int, *, name: str) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.shape != (max(0, size - 1),) or not np.all(np.isfinite(x)):
        raise TemporalSeamCurvatureError(f"{name} must be finite with frame_count-1 entries")
    return x


def _hermitian(matrix: Sequence[Sequence[complex]], size: int, *, name: str) -> np.ndarray:
    a = np.asarray(matrix, dtype=complex)
    if a.shape != (size, size) or not np.all(np.isfinite(a)):
        raise TemporalSeamCurvatureError(f"{name} must be a finite {size}x{size} matrix")
    if not np.allclose(a, a.conj().T, rtol=0.0, atol=1e-12):
        raise TemporalSeamCurvatureError(f"{name} must be Hermitian")
    return a


def _psd_matrix(matrix: float | Sequence[Sequence[float]], size: int, *, name: str) -> np.ndarray:
    if np.isscalar(matrix):
        value = float(matrix)
        if not math.isfinite(value) or value < 0.0:
            raise TemporalSeamCurvatureError(f"scalar {name} must be finite and non-negative")
        return value * np.eye(size, dtype=float)

    a = np.asarray(matrix, dtype=float)
    if a.shape != (size, size) or not np.all(np.isfinite(a)):
        raise TemporalSeamCurvatureError(f"{name} must be finite with the required square shape")
    if not np.allclose(a, a.T, rtol=0.0, atol=1e-12):
        raise TemporalSeamCurvatureError(f"{name} must be symmetric")
    if size and float(np.min(np.linalg.eigvalsh(a))) < -1e-12:
        raise TemporalSeamCurvatureError(f"{name} must be positive semidefinite")
    return a


def edge_gradient(vertex_values: Sequence[float]) -> np.ndarray:
    values = np.asarray(vertex_values, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise TemporalSeamCurvatureError("vertex_values must be a finite non-empty vector")
    return np.diff(values)


def temporal_seam_curvature(
    seam_rates: Sequence[float], temporal_vertex_connection: Sequence[float]
) -> np.ndarray:
    a0 = np.asarray(temporal_vertex_connection, dtype=float)
    if a0.ndim != 1 or a0.size == 0 or not np.all(np.isfinite(a0)):
        raise TemporalSeamCurvatureError("temporal_vertex_connection must be finite and non-empty")
    omega = _edge_vector(seam_rates, int(a0.size), name="seam_rates")
    return omega + np.diff(a0)


def covariant_hamiltonian(
    hamiltonian: Sequence[Sequence[complex]], temporal_vertex_connection: Sequence[float]
) -> np.ndarray:
    a0 = np.asarray(temporal_vertex_connection, dtype=float)
    if a0.ndim != 1 or a0.size == 0 or not np.all(np.isfinite(a0)):
        raise TemporalSeamCurvatureError("temporal_vertex_connection must be finite and non-empty")
    h = _hermitian(hamiltonian, int(a0.size), name="hamiltonian")
    return h - np.diag(a0)


def temporal_gauge_transform(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    temporal_vertex_connection: Sequence[float],
    vertex_phases: Sequence[float],
    vertex_phase_rates: Sequence[float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    psi = _state(amplitudes)
    n = int(psi.size)
    h = _hermitian(hamiltonian, n, name="hamiltonian")
    seam = _edge_vector(seam_phases, n, name="seam_phases")
    omega = _edge_vector(seam_rates, n, name="seam_rates")
    a0 = _vertex_vector(temporal_vertex_connection, n, name="temporal_vertex_connection")
    chi = _vertex_vector(vertex_phases, n, name="vertex_phases")
    chi_rate = _vertex_vector(vertex_phase_rates, n, name="vertex_phase_rates")

    u = np.diag(np.exp(1j * chi))
    return (
        u @ psi,
        u @ h @ u.conj().T - np.diag(chi_rate),
        seam + np.diff(chi),
        omega + np.diff(chi_rate),
        a0 - chi_rate,
    )


def covariant_schrodinger_power(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    temporal_vertex_connection: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    hbar = covariant_hamiltonian(hamiltonian, temporal_vertex_connection)
    return schrodinger_seam_power(psi, hbar, seam_phases)


def curvature_power(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    temporal_vertex_connection: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    q = connection_phase_gradient(psi, seam_phases)
    e = temporal_seam_curvature(seam_rates, temporal_vertex_connection)
    return float(q @ e)


def gauge_native_geometric_power(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    temporal_vertex_connection: Sequence[float],
) -> float:
    return covariant_schrodinger_power(
        amplitudes, hamiltonian, seam_phases, temporal_vertex_connection
    ) + curvature_power(
        amplitudes, seam_phases, seam_rates, temporal_vertex_connection
    )


def curvature_response(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    curvature_mobility: float | Sequence[Sequence[float]],
) -> np.ndarray:
    psi = _state(amplitudes)
    q = connection_phase_gradient(psi, seam_phases)
    g = _psd_matrix(curvature_mobility, int(q.size), name="curvature_mobility")
    return -(g @ q)


def seam_rates_from_curvature_response(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    temporal_vertex_connection: Sequence[float],
    curvature_mobility: float | Sequence[Sequence[float]],
) -> np.ndarray:
    psi = _state(amplitudes)
    a0 = _vertex_vector(
        temporal_vertex_connection, int(psi.size), name="temporal_vertex_connection"
    )
    e = curvature_response(psi, seam_phases, curvature_mobility)
    return e - np.diff(a0)


def curvature_dissipation(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    curvature_mobility: float | Sequence[Sequence[float]],
) -> float:
    psi = _state(amplitudes)
    q = connection_phase_gradient(psi, seam_phases)
    g = _psd_matrix(curvature_mobility, int(q.size), name="curvature_mobility")
    value = float(q @ g @ q)
    if value < -1e-12:
        raise TemporalSeamCurvatureError("curvature dissipation became negative outside tolerance")
    return max(0.0, value)


def curvature_response_balance_rate(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    temporal_vertex_connection: Sequence[float],
    curvature_mobility: float | Sequence[Sequence[float]],
    vertex_phase_mobility: float | Sequence[Sequence[float]],
) -> tuple[float, float, float, float]:
    psi = _state(amplitudes)
    p_cov = covariant_schrodinger_power(
        psi, hamiltonian, seam_phases, temporal_vertex_connection
    )
    d_curv = curvature_dissipation(psi, seam_phases, curvature_mobility)
    d_vertex = onsager_dissipation(psi, seam_phases, vertex_phase_mobility)
    return p_cov, d_curv, d_vertex, p_cov - d_curv - d_vertex


def accumulated_curvature_offset(
    curvature_samples: Sequence[Sequence[float]], delta_theta: Sequence[float]
) -> np.ndarray:
    samples = np.asarray(curvature_samples, dtype=float)
    steps = np.asarray(delta_theta, dtype=float)
    if samples.ndim != 2 or not np.all(np.isfinite(samples)):
        raise TemporalSeamCurvatureError("curvature_samples must be a finite 2D array")
    if steps.ndim != 1 or steps.shape != (samples.shape[0],) or not np.all(np.isfinite(steps)):
        raise TemporalSeamCurvatureError("delta_theta must match curvature sample count")
    if np.any(steps <= 0.0):
        raise TemporalSeamCurvatureError("delta_theta entries must be positive")
    return np.sum(samples * steps[:, None], axis=0)


def audit_curvature_response(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    temporal_vertex_connection: Sequence[float],
    curvature_mobility: float | Sequence[Sequence[float]],
    vertex_phase_mobility: float | Sequence[Sequence[float]],
) -> TemporalSeamCurvatureAudit:
    psi = _state(amplitudes)
    seam_rates = seam_rates_from_curvature_response(
        psi, seam_phases, temporal_vertex_connection, curvature_mobility
    )
    p_cov, d_curv, d_vertex, native_rate = curvature_response_balance_rate(
        psi,
        hamiltonian,
        seam_phases,
        temporal_vertex_connection,
        curvature_mobility,
        vertex_phase_mobility,
    )
    q = connection_phase_gradient(psi, seam_phases)
    e = temporal_seam_curvature(seam_rates, temporal_vertex_connection)
    p_curv = float(q @ e)
    _, _, moving_power = conservative_seam_power(
        psi, hamiltonian, seam_phases, seam_rates
    )
    moving_rate = moving_power - onsager_dissipation(
        psi, seam_phases, vertex_phase_mobility
    )
    return TemporalSeamCurvatureAudit(
        covariant_schrodinger_power=p_cov,
        curvature_power=p_curv,
        curvature_dissipation=d_curv,
        vertex_phase_dissipation=d_vertex,
        gauge_native_balance_rate=native_rate,
        moving_balance_rate=moving_rate,
        decomposition_residual=abs(native_rate - moving_rate),
    )
