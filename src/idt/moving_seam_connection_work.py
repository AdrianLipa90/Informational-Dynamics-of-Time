from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .schrodinger_onsager_seam_balance import (
    SchrodingerOnsagerBalanceError,
    onsager_dissipation,
    schrodinger_seam_power,
    seam_stiffness,
)


class MovingSeamConnectionError(ValueError):
    pass


@dataclass(frozen=True)
class MovingConnectionAudit:
    seam_energy: float
    schrodinger_power: float
    connection_work: float
    onsager_dissipation: float
    conservative_power: float
    full_balance_rate: float
    operator_connection_residual: float


def _state(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    if psi.ndim != 1 or psi.size == 0 or not np.all(np.isfinite(psi)):
        raise MovingSeamConnectionError("amplitudes must be a finite non-empty vector")
    norm = float(np.linalg.norm(psi))
    if not math.isfinite(norm) or norm <= 0.0:
        raise MovingSeamConnectionError("amplitudes must have positive finite norm")
    return psi


def _edge_vector(values: Sequence[float], frame_count: int, *, name: str) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size != max(0, frame_count - 1) or not np.all(np.isfinite(x)):
        raise MovingSeamConnectionError(f"{name} must be finite with frame_count-1 entries")
    return x


def _hermitian(hamiltonian: Sequence[Sequence[complex]], size: int) -> np.ndarray:
    h = np.asarray(hamiltonian, dtype=complex)
    if h.shape != (size, size) or not np.all(np.isfinite(h)):
        raise MovingSeamConnectionError("hamiltonian must be finite with frame_count square shape")
    if not np.allclose(h, h.conj().T, rtol=0.0, atol=1e-12):
        raise MovingSeamConnectionError("hamiltonian must be Hermitian")
    return h


def connection_phase_gradient(
    amplitudes: Sequence[complex], seam_phases: Sequence[float]
) -> np.ndarray:
    """Return grad_phi V_seam for the edge-native seam connection."""
    psi = _state(amplitudes)
    phases = _edge_vector(seam_phases, int(psi.size), name="seam_phases")
    if psi.size == 1:
        return np.zeros(0, dtype=float)
    return 0.5 * np.imag(np.exp(1j * phases) * psi[:-1] * np.conj(psi[1:]))


def connection_work(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    rates = _edge_vector(seam_rates, int(psi.size), name="seam_rates")
    gradient = connection_phase_gradient(psi, seam_phases)
    return float(gradient @ rates)


def seam_stiffness_rate(
    frame_count: int,
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise MovingSeamConnectionError("frame_count must be a positive integer")
    phases = _edge_vector(seam_phases, frame_count, name="seam_phases")
    rates = _edge_vector(seam_rates, frame_count, name="seam_rates")
    if frame_count == 1:
        return np.zeros((1, 1), dtype=complex)

    c = np.zeros((frame_count - 1, frame_count), dtype=complex)
    c_dot = np.zeros_like(c)
    for edge, (phi, rate) in enumerate(zip(phases, rates)):
        left = np.exp(0.5j * phi)
        right = np.exp(-0.5j * phi)
        c[edge, edge] = left
        c[edge, edge + 1] = -right
        c_dot[edge, edge] = 0.5j * rate * left
        c_dot[edge, edge + 1] = 0.5j * rate * right

    return 0.25 * (c_dot.conj().T @ c + c.conj().T @ c_dot)


def operator_connection_work(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    k_dot = seam_stiffness_rate(int(psi.size), seam_phases, seam_rates)
    return float(np.real(np.vdot(psi, k_dot @ psi)))


def conservative_seam_power(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
) -> tuple[float, float, float]:
    psi = _state(amplitudes)
    h = _hermitian(hamiltonian, int(psi.size))
    p_sch = schrodinger_seam_power(psi, h, seam_phases)
    p_conn = connection_work(psi, seam_phases, seam_rates)
    return p_sch, p_conn, p_sch + p_conn


def moving_seam_balance_rate(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> tuple[float, float, float, float]:
    psi = _state(amplitudes)
    p_sch, p_conn, conservative = conservative_seam_power(
        psi, hamiltonian, seam_phases, seam_rates
    )
    dissipation = onsager_dissipation(psi, seam_phases, mobility)
    return p_sch, p_conn, dissipation, conservative - dissipation


def time_dependent_gauge_transform(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    vertex_phases: Sequence[float],
    vertex_phase_rates: Sequence[float],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    psi = _state(amplitudes)
    n = int(psi.size)
    h = _hermitian(hamiltonian, n)
    seam = _edge_vector(seam_phases, n, name="seam_phases")
    seam_rate = _edge_vector(seam_rates, n, name="seam_rates")
    chi = np.asarray(vertex_phases, dtype=float)
    chi_rate = np.asarray(vertex_phase_rates, dtype=float)
    if chi.shape != (n,) or chi_rate.shape != (n,):
        raise MovingSeamConnectionError("vertex phases and rates must have frame_count entries")
    if not np.all(np.isfinite(chi)) or not np.all(np.isfinite(chi_rate)):
        raise MovingSeamConnectionError("vertex phases and rates must be finite")

    u = np.diag(np.exp(1j * chi))
    psi_prime = u @ psi
    seam_prime = seam + np.diff(chi)
    seam_rate_prime = seam_rate + np.diff(chi_rate)
    h_prime = u @ h @ u.conj().T - np.diag(chi_rate)
    return psi_prime, h_prime, seam_prime, seam_rate_prime


def audit_moving_connection(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    seam_rates: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> MovingConnectionAudit:
    psi = _state(amplitudes)
    h = _hermitian(hamiltonian, int(psi.size))
    k = seam_stiffness(seam_phases, int(psi.size))
    seam_energy = float(np.real(np.vdot(psi, k @ psi)))
    p_sch, p_conn, diss, balance = moving_seam_balance_rate(
        psi, h, seam_phases, seam_rates, mobility
    )
    p_conn_operator = operator_connection_work(psi, seam_phases, seam_rates)
    return MovingConnectionAudit(
        seam_energy=seam_energy,
        schrodinger_power=p_sch,
        connection_work=p_conn,
        onsager_dissipation=diss,
        conservative_power=p_sch + p_conn,
        full_balance_rate=balance,
        operator_connection_residual=abs(p_conn - p_conn_operator),
    )
