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
    dissipation: float
    predicted_energy_rate: float
    directional_energy_rate: float
    energy_balance_residual: float
    norm_rate: float


def _state(values: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(values, dtype=complex)
    if psi.ndim != 1 or psi.size < 2:
        raise SchrodingerOnsagerBalanceError("state must be one-dimensional with at least two frames")
    if not np.all(np.isfinite(psi)):
        raise SchrodingerOnsagerBalanceError("state must be finite")
    if float(np.linalg.norm(psi)) <= 0.0:
        raise SchrodingerOnsagerBalanceError("state norm must be positive")
    return psi


def _seam_phases(values: Sequence[float], frame_count: int) -> np.ndarray:
    phi = np.asarray(values, dtype=float)
    if phi.ndim != 1 or phi.size != frame_count - 1:
        raise SchrodingerOnsagerBalanceError("seam phases must have frame_count-1 entries")
    if not np.all(np.isfinite(phi)):
        raise SchrodingerOnsagerBalanceError("seam phases must be finite")
    return phi


def _hermitian(values: Sequence[Sequence[complex]], frame_count: int, *, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=complex)
    if matrix.shape != (frame_count, frame_count):
        raise SchrodingerOnsagerBalanceError(f"{name} must have shape (N,N)")
    if not np.all(np.isfinite(matrix)):
        raise SchrodingerOnsagerBalanceError(f"{name} must be finite")
    if not np.allclose(matrix, matrix.conj().T, rtol=0.0, atol=1e-12):
        raise SchrodingerOnsagerBalanceError(f"{name} must be Hermitian")
    return matrix


def _onsager(
    values: float | Sequence[Sequence[float]],
    frame_count: int,
) -> np.ndarray:
    """Normalize scalar or matrix Onsager mobility to one PSD matrix.

    The scalar form is retained for compatibility with the previously hosted-PASS
    seam API, where ``mu`` denoted the isotropic matrix ``mu I``.  Matrix input is
    the current native representation.
    """

    if np.isscalar(values):
        mobility = float(values)
        if not isfinite(mobility) or mobility < 0.0:
            raise SchrodingerOnsagerBalanceError(
                "scalar Onsager mobility must be finite and non-negative"
            )
        return mobility * np.eye(frame_count, dtype=float)

    matrix = np.asarray(values, dtype=float)
    if matrix.shape != (frame_count, frame_count):
        raise SchrodingerOnsagerBalanceError("Onsager matrix must have shape (N,N)")
    if not np.all(np.isfinite(matrix)):
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be finite")
    if not np.allclose(matrix, matrix.T, rtol=0.0, atol=1e-12):
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be symmetric")
    eig = np.linalg.eigvalsh(matrix)
    if float(np.min(eig)) < -1e-12:
        raise SchrodingerOnsagerBalanceError("Onsager matrix must be positive semidefinite")
    return matrix


def seam_difference_operator(seam_phases: Sequence[float], frame_count: int) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count < 2:
        raise SchrodingerOnsagerBalanceError("frame_count must be an integer >= 2")
    phi = _seam_phases(seam_phases, frame_count)
    b = np.zeros((frame_count - 1, frame_count), dtype=complex)
    for edge, phase in enumerate(phi):
        b[edge, edge] = 0.5 * np.exp(0.5j * phase)
        b[edge, edge + 1] = -0.5 * np.exp(-0.5j * phase)
    return b


def seam_stiffness(
    seam_phases_or_frame_count: Sequence[float] | int,
    frame_count_or_seam_phases: int | Sequence[float],
) -> np.ndarray:
    """Return the phase-aware seam stiffness with dual API compatibility.

    Current API::

        seam_stiffness(seam_phases, frame_count)

    Hosted-PASS legacy seam consumers use::

        seam_stiffness(frame_count, seam_phases)

    Both normalize to the same ``B^* B`` operator; no mathematical branch is
    introduced by the compatibility surface.
    """

    if isinstance(seam_phases_or_frame_count, int) and not isinstance(
        seam_phases_or_frame_count, bool
    ):
        frame_count = seam_phases_or_frame_count
        seam_phases = frame_count_or_seam_phases
    else:
        seam_phases = seam_phases_or_frame_count
        frame_count = frame_count_or_seam_phases

    if not isinstance(frame_count, int) or isinstance(frame_count, bool):
        raise SchrodingerOnsagerBalanceError("frame_count must be an integer >= 2")
    if isinstance(seam_phases, (int, float, complex)):
        raise SchrodingerOnsagerBalanceError("seam phases must be a sequence")

    b = seam_difference_operator(seam_phases, frame_count)
    k = b.conj().T @ b
    return 0.5 * (k + k.conj().T)


def seam_defect_energy(state: Sequence[complex], seam_phases: Sequence[float]) -> float:
    psi = _state(state)
    b = seam_difference_operator(seam_phases, psi.size)
    defect = b @ psi
    return float(np.vdot(defect, defect).real)


def edge_mismatch_gradients(state: Sequence[complex], seam_phases: Sequence[float]) -> np.ndarray:
    psi = _state(state)
    phi = _seam_phases(seam_phases, psi.size)
    out = np.empty(psi.size - 1, dtype=float)
    for edge, phase in enumerate(phi):
        relative = np.exp(-1j * phase) * psi[edge + 1] * np.conj(psi[edge])
        out[edge] = 0.5 * float(np.imag(relative))
    return out


def path_incidence(frame_count: int) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count < 2:
        raise SchrodingerOnsagerBalanceError("frame_count must be an integer >= 2")
    d = np.zeros((frame_count - 1, frame_count), dtype=float)
    for edge in range(frame_count - 1):
        d[edge, edge] = -1.0
        d[edge, edge + 1] = 1.0
    return d


def node_phase_gradient(state: Sequence[complex], seam_phases: Sequence[float]) -> np.ndarray:
    psi = _state(state)
    edge_gradient = edge_mismatch_gradients(psi, seam_phases)
    return path_incidence(psi.size).T @ edge_gradient


def schrodinger_velocity(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
) -> np.ndarray:
    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size, name="Hamiltonian")
    return -1j * (h @ psi)


def schrodinger_seam_power(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
) -> float:
    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size, name="Hamiltonian")
    k = seam_stiffness(seam_phases, psi.size)
    commutator = h @ k - k @ h
    value = 1j * np.vdot(psi, commutator @ psi)
    return float(np.real(value))


def onsager_dissipation(
    state: Sequence[complex],
    seam_phases: Sequence[float],
    mobility: float | Sequence[Sequence[float]],
) -> float:
    """Return the exact Onsager quadratic dissipation ``grad^T G grad``.

    This restores the hosted-PASS public seam API while delegating to the current
    node-phase gradient and mobility normalization.  Scalar ``mobility`` means
    the isotropic matrix ``mobility * I``.
    """

    psi = _state(state)
    gradient = node_phase_gradient(psi, seam_phases)
    g = _onsager(mobility, psi.size)
    value = float(gradient @ g @ gradient)
    if value < -1e-12:
        raise SchrodingerOnsagerBalanceError(
            "Onsager dissipation became negative outside numerical tolerance"
        )
    return max(0.0, value)


def onsager_phase_velocity(
    state: Sequence[complex],
    seam_phases: Sequence[float],
    onsager_matrix: float | Sequence[Sequence[float]],
) -> tuple[np.ndarray, np.ndarray, float]:
    psi = _state(state)
    g = _onsager(onsager_matrix, psi.size)
    gradient = node_phase_gradient(psi, seam_phases)
    alpha_dot = -(g @ gradient)
    state_dot = 1j * alpha_dot * psi
    dissipation = float(gradient @ g @ gradient)
    return alpha_dot, state_dot, dissipation


def full_balance_velocity(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    onsager_matrix: float | Sequence[Sequence[float]],
) -> np.ndarray:
    psi = _state(state)
    reversible = schrodinger_velocity(psi, hamiltonian)
    _, dissipative, _ = onsager_phase_velocity(psi, seam_phases, onsager_matrix)
    return reversible + dissipative


def audit_instantaneous_balance(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    onsager_matrix: float | Sequence[Sequence[float]],
) -> SeamBalanceAudit:
    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size, name="Hamiltonian")
    g = _onsager(onsager_matrix, psi.size)
    k = seam_stiffness(seam_phases, psi.size)
    energy = float(np.vdot(psi, k @ psi).real)
    p_h = schrodinger_seam_power(psi, h, seam_phases)
    _, dissipative_velocity, dissipation = onsager_phase_velocity(psi, seam_phases, g)
    reversible_velocity = -1j * (h @ psi)
    total_velocity = reversible_velocity + dissipative_velocity
    directional = 2.0 * float(np.real(np.vdot(k @ psi, total_velocity)))
    predicted = p_h - dissipation
    norm_rate = 2.0 * float(np.real(np.vdot(psi, total_velocity)))
    return SeamBalanceAudit(
        seam_energy=energy,
        schrodinger_power=p_h,
        dissipation=dissipation,
        predicted_energy_rate=predicted,
        directional_energy_rate=directional,
        energy_balance_residual=abs(directional - predicted),
        norm_rate=norm_rate,
    )


def exact_unitary_step(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    delta_theta: float,
) -> np.ndarray:
    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size, name="Hamiltonian")
    dt = float(delta_theta)
    if not math.isfinite(dt):
        raise SchrodingerOnsagerBalanceError("delta_theta must be finite")
    eigenvalues, eigenvectors = np.linalg.eigh(h)
    phases = np.exp(-1j * eigenvalues * dt)
    return eigenvectors @ (phases * (eigenvectors.conj().T @ psi))


def phase_only_onsager_step(
    state: Sequence[complex],
    seam_phases: Sequence[float],
    onsager_matrix: float | Sequence[Sequence[float]],
    delta_theta: float,
) -> np.ndarray:
    psi = _state(state)
    dt = float(delta_theta)
    if not math.isfinite(dt) or dt < 0.0:
        raise SchrodingerOnsagerBalanceError("delta_theta must be finite and non-negative")
    alpha_dot, _, _ = onsager_phase_velocity(psi, seam_phases, onsager_matrix)
    return np.exp(1j * alpha_dot * dt) * psi


def strang_balance_step(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    seam_phases: Sequence[float],
    onsager_matrix: float | Sequence[Sequence[float]],
    delta_theta: float,
) -> np.ndarray:
    dt = float(delta_theta)
    if not math.isfinite(dt) or dt < 0.0:
        raise SchrodingerOnsagerBalanceError("delta_theta must be finite and non-negative")
    half = exact_unitary_step(state, hamiltonian, 0.5 * dt)
    locked = phase_only_onsager_step(half, seam_phases, onsager_matrix, dt)
    return exact_unitary_step(locked, hamiltonian, 0.5 * dt)
