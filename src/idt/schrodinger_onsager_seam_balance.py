from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class SchrodingerOnsagerBalanceError(ValueError):
    pass


@dataclass(frozen=True)
class SeamBalanceAudit:
    seam_energy: float
    schrodinger_power: float
    onsager_dissipation: float
    balance_rate: float
    direct_directional_rate: float
    balance_residual: float
    norm_rate: float


def _state(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    if psi.ndim != 1 or psi.size == 0 or not np.all(np.isfinite(psi)):
        raise SchrodingerOnsagerBalanceError("amplitudes must be a finite non-empty vector")
    norm = float(np.linalg.norm(psi))
    if not math.isfinite(norm) or norm <= 0.0:
        raise SchrodingerOnsagerBalanceError("amplitudes must have positive finite norm")
    return psi


def _seam_phases(seam_phases: Sequence[float], frame_count: int) -> np.ndarray:
    phases = np.asarray(seam_phases, dtype=float)
    if phases.ndim != 1 or phases.size != max(0, frame_count - 1):
        raise SchrodingerOnsagerBalanceError("seam_phases must have frame_count-1 entries")
    if not np.all(np.isfinite(phases)):
        raise SchrodingerOnsagerBalanceError("seam_phases must be finite")
    return phases


def _hermitian(matrix: Sequence[Sequence[complex]], size: int, *, name: str) -> np.ndarray:
    a = np.asarray(matrix, dtype=complex)
    if a.shape != (size, size) or not np.all(np.isfinite(a)):
        raise SchrodingerOnsagerBalanceError(f"{name} must be a finite {size}x{size} matrix")
    if not np.allclose(a, a.conj().T, rtol=0.0, atol=1e-12):
        raise SchrodingerOnsagerBalanceError(f"{name} must be Hermitian")
    return a


def _onsager_matrix(mobility: float | Sequence[Sequence[float]], size: int) -> np.ndarray:
    if np.isscalar(mobility):
        mu = float(mobility)
        if not math.isfinite(mu) or mu < 0.0:
            raise SchrodingerOnsagerBalanceError("scalar Onsager mobility must be finite and non-negative")
        return mu * np.eye(size, dtype=float)

    g = np.asarray(mobility, dtype=float)
    if g.shape != (size, size) or not np.all(np.isfinite(g)):
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be finite with frame_count square shape")
    if not np.allclose(g, g.T, rtol=0.0, atol=1e-12):
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be symmetric")
    eigenvalues = np.linalg.eigvalsh(g)
    if float(np.min(eigenvalues)) < -1e-12:
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be positive semidefinite")
    return g


def seam_covariant_incidence(frame_count: int, seam_phases: Sequence[float]) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise SchrodingerOnsagerBalanceError("frame_count must be a positive integer")
    phases = _seam_phases(seam_phases, frame_count)
    c = np.zeros((max(0, frame_count - 1), frame_count), dtype=complex)
    for edge, phi in enumerate(phases):
        c[edge, edge] = np.exp(0.5j * phi)
        c[edge, edge + 1] = -np.exp(-0.5j * phi)
    return c


def seam_stiffness(frame_count: int, seam_phases: Sequence[float]) -> np.ndarray:
    c = seam_covariant_incidence(frame_count, seam_phases)
    return 0.25 * (c.conj().T @ c)


def seam_defect_energy(amplitudes: Sequence[complex], seam_phases: Sequence[float]) -> float:
    psi = _state(amplitudes)
    k = seam_stiffness(int(psi.size), seam_phases)
    value = float(np.vdot(psi, k @ psi).real)
    if value < -1e-12:
        raise SchrodingerOnsagerBalanceError("seam energy became negative outside numerical tolerance")
    return max(0.0, value)


def seam_phase_gradient(amplitudes: Sequence[complex], seam_phases: Sequence[float]) -> np.ndarray:
    """Gradient dV/dalpha in vertex-phase coordinates, without taking arg(psi)."""
    psi = _state(amplitudes)
    phases = _seam_phases(seam_phases, int(psi.size))
    grad = np.zeros(psi.size, dtype=float)
    for edge, phi in enumerate(phases):
        edge_current = 0.5 * float(np.imag(np.exp(1j * phi) * psi[edge] * np.conj(psi[edge + 1])))
        grad[edge] += edge_current
        grad[edge + 1] -= edge_current
    return grad


def schrodinger_velocity(amplitudes: Sequence[complex], hamiltonian: Sequence[Sequence[complex]]) -> np.ndarray:
    psi = _state(amplitudes)
    h = _hermitian(hamiltonian, int(psi.size), name="hamiltonian")
    return -1j * (h @ psi)


def schrodinger_seam_power(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    h = _hermitian(hamiltonian, int(psi.size), name="hamiltonian")
    k = seam_stiffness(int(psi.size), seam_phases)
    commutator = h @ k - k @ h
    value = 1j * np.vdot(psi, commutator @ psi)
    return float(np.real(value))


def onsager_phase_rates(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> np.ndarray:
    psi = _state(amplitudes)
    g_alpha = seam_phase_gradient(psi, seam_phases)
    g = _onsager_matrix(mobility, int(psi.size))
    return -(g @ g_alpha)


def onsager_state_velocity(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> np.ndarray:
    psi = _state(amplitudes)
    alpha_rate = onsager_phase_rates(psi, seam_phases, mobility)
    return 1j * alpha_rate * psi


def onsager_dissipation(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> float:
    psi = _state(amplitudes)
    g_alpha = seam_phase_gradient(psi, seam_phases)
    g = _onsager_matrix(mobility, int(psi.size))
    value = float(g_alpha @ g @ g_alpha)
    if value < -1e-12:
        raise SchrodingerOnsagerBalanceError("Onsager dissipation became negative outside numerical tolerance")
    return max(0.0, value)


def combined_state_velocity(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> np.ndarray:
    return schrodinger_velocity(amplitudes, hamiltonian) + onsager_state_velocity(
        amplitudes, seam_phases, mobility
    )


def seam_energy_directional_rate(
    amplitudes: Sequence[complex],
    velocity: Sequence[complex],
    seam_phases: Sequence[float],
) -> float:
    psi = _state(amplitudes)
    vel = np.asarray(velocity, dtype=complex)
    if vel.shape != psi.shape or not np.all(np.isfinite(vel)):
        raise SchrodingerOnsagerBalanceError("velocity must be finite and match amplitude shape")
    k = seam_stiffness(int(psi.size), seam_phases)
    return float(2.0 * np.real(np.vdot(k @ psi, vel)))


def norm_directional_rate(amplitudes: Sequence[complex], velocity: Sequence[complex]) -> float:
    psi = _state(amplitudes)
    vel = np.asarray(velocity, dtype=complex)
    if vel.shape != psi.shape or not np.all(np.isfinite(vel)):
        raise SchrodingerOnsagerBalanceError("velocity must be finite and match amplitude shape")
    return float(2.0 * np.real(np.vdot(psi, vel)))


def seam_balance_rate(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> tuple[float, float, float]:
    power = schrodinger_seam_power(amplitudes, hamiltonian, seam_phases)
    dissipation = onsager_dissipation(amplitudes, seam_phases, mobility)
    return power, dissipation, power - dissipation


def commutator_frobenius(
    hamiltonian: Sequence[Sequence[complex]], seam_phases: Sequence[float]
) -> float:
    h = np.asarray(hamiltonian, dtype=complex)
    if h.ndim != 2 or h.shape[0] != h.shape[1] or h.size == 0:
        raise SchrodingerOnsagerBalanceError("hamiltonian must be a non-empty square matrix")
    h = _hermitian(h, int(h.shape[0]), name="hamiltonian")
    k = seam_stiffness(int(h.shape[0]), seam_phases)
    return float(np.linalg.norm(h @ k - k @ h, ord="fro"))


def audit_seam_balance(
    amplitudes: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> SeamBalanceAudit:
    psi = _state(amplitudes)
    velocity = combined_state_velocity(psi, hamiltonian, seam_phases, mobility)
    power, dissipation, balance = seam_balance_rate(psi, hamiltonian, seam_phases, mobility)
    direct = seam_energy_directional_rate(psi, velocity, seam_phases)
    return SeamBalanceAudit(
        seam_energy=seam_defect_energy(psi, seam_phases),
        schrodinger_power=power,
        onsager_dissipation=dissipation,
        balance_rate=balance,
        direct_directional_rate=direct,
        balance_residual=abs(direct - balance),
        norm_rate=norm_directional_rate(psi, velocity),
    )
