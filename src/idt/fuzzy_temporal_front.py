from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .fuzzy_temporal_interface import (
    FuzzyTemporalInterfaceError,
    fuzzy_interface_strength,
    gauge_invariant_mismatch,
)


class FuzzyTemporalFrontError(ValueError):
    pass


@dataclass(frozen=True)
class PathPowerCertificate:
    lower_power_max_abs: float
    leading_coefficients: tuple[complex, ...]
    frame_orders: tuple[int, ...]
    interface_orders: tuple[int, ...]


def _state(values: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(values, dtype=complex)
    if psi.ndim != 1 or psi.size < 2 or not np.all(np.isfinite(psi)):
        raise FuzzyTemporalFrontError("state must be a finite one-dimensional vector with N>=2")
    if float(np.linalg.norm(psi)) <= 0.0:
        raise FuzzyTemporalFrontError("state norm must be positive")
    return psi


def _seams(values: Sequence[float], n: int) -> np.ndarray:
    phi = np.asarray(values, dtype=float)
    if phi.ndim != 1 or phi.size != n - 1 or not np.all(np.isfinite(phi)):
        raise FuzzyTemporalFrontError("seam phases must have N-1 finite entries")
    return phi


def _hermitian_path(values: Sequence[Sequence[complex]]) -> np.ndarray:
    h = np.asarray(values, dtype=complex)
    if h.ndim != 2 or h.shape[0] != h.shape[1] or h.shape[0] < 2:
        raise FuzzyTemporalFrontError("Hamiltonian must be a square matrix with N>=2")
    if not np.all(np.isfinite(h)):
        raise FuzzyTemporalFrontError("Hamiltonian must be finite")
    if not np.allclose(h, h.conj().T, rtol=0.0, atol=1e-12):
        raise FuzzyTemporalFrontError("Hamiltonian must be Hermitian")
    n = h.shape[0]
    for i in range(n):
        for j in range(n):
            if abs(i - j) > 1 and abs(h[i, j]) > 1e-12:
                raise FuzzyTemporalFrontError("Hamiltonian must be nearest-neighbour/tridiagonal")
    if any(abs(h[i + 1, i]) <= 1e-15 for i in range(n - 1)):
        raise FuzzyTemporalFrontError("every nearest-neighbour path coupling must be nonzero")
    return h


def fuzzy_interface_mass(left: complex, right: complex, seam_phase: float) -> float:
    a0 = complex(left)
    a1 = complex(right)
    if not all(math.isfinite(v) for v in (a0.real, a0.imag, a1.real, a1.imag, float(seam_phase))):
        raise FuzzyTemporalFrontError("interface inputs must be finite")
    pair_weight = abs(a0) ** 2 + abs(a1) ** 2
    if pair_weight == 0.0:
        return 0.0
    return float(pair_weight * fuzzy_interface_strength(a0, a1, float(seam_phase)))


def fuzzy_interface_mass_profile(
    amplitudes: Sequence[complex], seam_phases: Sequence[float]
) -> np.ndarray:
    psi = _state(amplitudes)
    phi = _seams(seam_phases, psi.size)
    return np.asarray(
        [fuzzy_interface_mass(psi[i], psi[i + 1], phi[i]) for i in range(psi.size - 1)],
        dtype=float,
    )


def locked_seam_phases(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = _state(amplitudes)
    out = np.zeros(psi.size - 1, dtype=float)
    for i in range(psi.size - 1):
        if abs(psi[i]) == 0.0 or abs(psi[i + 1]) == 0.0:
            out[i] = 0.0
        else:
            out[i] = float(np.angle(psi[i + 1]) - np.angle(psi[i]))
    return out


def locked_fuzzy_mass_profile(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = _state(amplitudes)
    return fuzzy_interface_mass_profile(psi, locked_seam_phases(psi))


def expected_interface_orders(frame_count: int) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count < 2:
        raise FuzzyTemporalFrontError("frame_count must be an integer >= 2")
    return 2 * np.arange(1, frame_count, dtype=int) - 1


def path_power_certificate(hamiltonian: Sequence[Sequence[complex]]) -> PathPowerCertificate:
    h = _hermitian_path(hamiltonian)
    n = h.shape[0]
    lower_max = 0.0
    coeffs: list[complex] = []
    for target in range(n):
        for power in range(target):
            value = np.linalg.matrix_power(h, power)[target, 0]
            lower_max = max(lower_max, float(abs(value)))
        leading_power = target
        leading_matrix = np.linalg.matrix_power(h, leading_power)
        leading = ((-1j) ** leading_power / math.factorial(leading_power)) * leading_matrix[target, 0]
        coeffs.append(complex(leading))
    return PathPowerCertificate(
        lower_power_max_abs=lower_max,
        leading_coefficients=tuple(coeffs),
        frame_orders=tuple(range(n)),
        interface_orders=tuple(int(x) for x in expected_interface_orders(n)),
    )


def expected_leading_path_products(hamiltonian: Sequence[Sequence[complex]]) -> np.ndarray:
    h = _hermitian_path(hamiltonian)
    n = h.shape[0]
    out = np.ones(n, dtype=complex)
    for target in range(1, n):
        out[target] = out[target - 1] * h[target, target - 1]
    return out


def locked_front_leading_coefficients(hamiltonian: Sequence[Sequence[complex]]) -> np.ndarray:
    cert = path_power_certificate(hamiltonian)
    coeffs = np.asarray(cert.leading_coefficients, dtype=complex)
    return 2.0 * np.abs(coeffs[:-1]) * np.abs(coeffs[1:])


def exact_unitary_state(
    initial_state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    delta_theta: float,
) -> np.ndarray:
    psi = _state(initial_state)
    h = _hermitian_path(hamiltonian)
    if h.shape != (psi.size, psi.size):
        raise FuzzyTemporalFrontError("Hamiltonian dimension must match state dimension")
    dt = float(delta_theta)
    if not math.isfinite(dt):
        raise FuzzyTemporalFrontError("delta_theta must be finite")
    values, vectors = np.linalg.eigh(h)
    return vectors @ (np.exp(-1j * values * dt) * (vectors.conj().T @ psi))


def sharp_boundary_locked_front(
    hamiltonian: Sequence[Sequence[complex]], delta_theta: float
) -> tuple[np.ndarray, np.ndarray]:
    h = _hermitian_path(hamiltonian)
    initial = np.zeros(h.shape[0], dtype=complex)
    initial[0] = 1.0
    state = exact_unitary_state(initial, h, delta_theta)
    return state, locked_fuzzy_mass_profile(state)


def front_total_and_barycenter(interface_masses: Sequence[float]) -> tuple[float, float]:
    masses = np.asarray(interface_masses, dtype=float)
    if masses.ndim != 1 or masses.size == 0 or not np.all(np.isfinite(masses)) or np.any(masses < -1e-14):
        raise FuzzyTemporalFrontError("interface masses must be a finite non-negative vector")
    masses = np.maximum(masses, 0.0)
    total = float(np.sum(masses))
    if total <= 0.0:
        return 0.0, math.nan
    positions = np.arange(1, masses.size + 1, dtype=float)
    return total, float(np.dot(positions, masses) / total)


def interface_identity_residual(left: complex, right: complex, seam_phase: float) -> float:
    a0 = complex(left)
    a1 = complex(right)
    delta = gauge_invariant_mismatch(a0, a1, float(seam_phase))
    rhs = 2.0 * abs(a0) * abs(a1) * math.cos(0.5 * delta) ** 2
    return abs(fuzzy_interface_mass(a0, a1, float(seam_phase)) - rhs)
