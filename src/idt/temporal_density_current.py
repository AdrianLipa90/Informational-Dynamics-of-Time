from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class TemporalDensityCurrentError(ValueError):
    pass


@dataclass(frozen=True)
class SeamQuadratures:
    pair_scale: float
    coherence: float
    transport: float
    fuzzy_mass: float
    current: float
    circle_residual: float


def _positive_spacing(h: float) -> float:
    out = float(h)
    if not math.isfinite(out) or out <= 0.0:
        raise TemporalDensityCurrentError("mesh spacing h must be finite and positive")
    return out


def _state(values: Sequence[complex]) -> np.ndarray:
    state = np.asarray(values, dtype=complex)
    if state.ndim != 1 or state.size < 2 or not np.all(np.isfinite(state)):
        raise TemporalDensityCurrentError("state must be a finite one-dimensional vector with N>=2")
    return state


def _edges(mobilities: Sequence[float], seam_phases: Sequence[float], n: int) -> tuple[np.ndarray, np.ndarray]:
    mobility = np.asarray(mobilities, dtype=float)
    phase = np.asarray(seam_phases, dtype=float)
    if mobility.ndim != 1 or phase.ndim != 1 or mobility.size != n - 1 or phase.size != n - 1:
        raise TemporalDensityCurrentError("mobilities and seam phases must contain N-1 entries")
    if not np.all(np.isfinite(mobility)) or not np.all(np.isfinite(phase)):
        raise TemporalDensityCurrentError("edge data must be finite")
    if np.any(mobility <= 0.0):
        raise TemporalDensityCurrentError("edge mobilities must be positive")
    return mobility, phase


def covariant_difference_matrix(seam_phases: Sequence[float]) -> np.ndarray:
    phase = np.asarray(seam_phases, dtype=float)
    if phase.ndim != 1 or phase.size == 0 or not np.all(np.isfinite(phase)):
        raise TemporalDensityCurrentError("seam phases must be a finite non-empty vector")
    n = phase.size + 1
    d = np.zeros((n - 1, n), dtype=complex)
    for edge, phi in enumerate(phase):
        d[edge, edge] = -np.exp(1j * phi)
        d[edge, edge + 1] = 1.0
    return d


def covariant_path_hamiltonian(
    mobilities: Sequence[float],
    seam_phases: Sequence[float],
    h: float,
    potential: Sequence[float] | None = None,
) -> np.ndarray:
    spacing = _positive_spacing(h)
    phase = np.asarray(seam_phases, dtype=float)
    if phase.ndim != 1 or phase.size == 0 or not np.all(np.isfinite(phase)):
        raise TemporalDensityCurrentError("seam phases must be a finite non-empty vector")
    n = phase.size + 1
    mobility, phase = _edges(mobilities, phase, n)
    d = covariant_difference_matrix(phase)
    hamiltonian = d.conj().T @ np.diag(mobility) @ d / spacing**2
    if potential is not None:
        v = np.asarray(potential, dtype=float)
        if v.ndim != 1 or v.size != n or not np.all(np.isfinite(v)):
            raise TemporalDensityCurrentError("potential must contain N finite real entries")
        hamiltonian = hamiltonian + np.diag(v)
    return hamiltonian


def edge_currents(
    amplitudes: Sequence[complex],
    mobilities: Sequence[float],
    seam_phases: Sequence[float],
    h: float,
) -> np.ndarray:
    spacing = _positive_spacing(h)
    state = _state(amplitudes)
    mobility, phase = _edges(mobilities, seam_phases, state.size)
    current = np.empty(state.size - 1, dtype=float)
    for edge in range(state.size - 1):
        covariant_pair = np.conj(state[edge]) * np.exp(-1j * phase[edge]) * state[edge + 1]
        current[edge] = 2.0 * mobility[edge] * float(np.imag(covariant_pair)) / spacing**2
    return current


def schrodinger_density_derivative(
    amplitudes: Sequence[complex], hamiltonian: Sequence[Sequence[complex]]
) -> np.ndarray:
    state = _state(amplitudes)
    hamiltonian_array = np.asarray(hamiltonian, dtype=complex)
    if hamiltonian_array.shape != (state.size, state.size) or not np.all(np.isfinite(hamiltonian_array)):
        raise TemporalDensityCurrentError("Hamiltonian must match state dimension and be finite")
    if not np.allclose(hamiltonian_array, hamiltonian_array.conj().T, rtol=0.0, atol=1e-12):
        raise TemporalDensityCurrentError("Hamiltonian must be Hermitian")
    tangent = -1j * (hamiltonian_array @ state)
    return 2.0 * np.real(np.conj(state) * tangent)


def continuity_rhs(currents: Sequence[float], vertex_count: int) -> np.ndarray:
    edge_current = np.asarray(currents, dtype=float)
    if not isinstance(vertex_count, int) or isinstance(vertex_count, bool) or vertex_count < 2:
        raise TemporalDensityCurrentError("vertex_count must be an integer >=2")
    if edge_current.ndim != 1 or edge_current.size != vertex_count - 1 or not np.all(np.isfinite(edge_current)):
        raise TemporalDensityCurrentError("currents must contain vertex_count-1 finite entries")
    rhs = np.zeros(vertex_count, dtype=float)
    rhs[0] = -edge_current[0]
    rhs[-1] = edge_current[-1]
    if vertex_count > 2:
        rhs[1:-1] = edge_current[:-1] - edge_current[1:]
    return rhs


def continuity_residual(
    amplitudes: Sequence[complex],
    mobilities: Sequence[float],
    seam_phases: Sequence[float],
    h: float,
    potential: Sequence[float] | None = None,
) -> float:
    state = _state(amplitudes)
    hamiltonian = covariant_path_hamiltonian(mobilities, seam_phases, h, potential=potential)
    derivative = schrodinger_density_derivative(state, hamiltonian)
    rhs = continuity_rhs(edge_currents(state, mobilities, seam_phases, h), state.size)
    return float(np.max(np.abs(derivative - rhs)))


def seam_quadratures(
    left: complex,
    right: complex,
    seam_phase: float,
    mobility: float,
    h: float,
) -> SeamQuadratures:
    spacing = _positive_spacing(h)
    m = float(mobility)
    phi = float(seam_phase)
    a0 = complex(left)
    a1 = complex(right)
    if not math.isfinite(m) or m <= 0.0 or not math.isfinite(phi):
        raise TemporalDensityCurrentError("mobility must be positive and seam phase finite")
    if not all(math.isfinite(value) for value in (a0.real, a0.imag, a1.real, a1.imag)):
        raise TemporalDensityCurrentError("pair amplitudes must be finite")
    r0 = abs(a0)
    r1 = abs(a1)
    pair_scale = r0 * r1
    if pair_scale == 0.0:
        delta = 0.0
    else:
        delta = float(np.angle(a1) - np.angle(a0) - phi)
    coherence = pair_scale * math.cos(delta)
    transport = pair_scale * math.sin(delta)
    fuzzy_mass = pair_scale + coherence
    current = 2.0 * m * transport / spacing**2
    circle_residual = abs(coherence**2 + transport**2 - pair_scale**2)
    return SeamQuadratures(
        pair_scale=pair_scale,
        coherence=coherence,
        transport=transport,
        fuzzy_mass=fuzzy_mass,
        current=current,
        circle_residual=circle_residual,
    )


def phase_only_density_derivative(
    amplitudes: Sequence[complex], phase_rates: Sequence[float]
) -> np.ndarray:
    state = _state(amplitudes)
    rates = np.asarray(phase_rates, dtype=float)
    if rates.ndim != 1 or rates.shape != state.shape or not np.all(np.isfinite(rates)):
        raise TemporalDensityCurrentError("phase_rates must match the state and be finite")
    tangent = 1j * rates * state
    return 2.0 * np.real(np.conj(state) * tangent)


def gauge_transform(
    amplitudes: Sequence[complex], seam_phases: Sequence[float], vertex_gauge: Sequence[float]
) -> tuple[np.ndarray, np.ndarray]:
    state = _state(amplitudes)
    phase = np.asarray(seam_phases, dtype=float)
    chi = np.asarray(vertex_gauge, dtype=float)
    if phase.ndim != 1 or phase.size != state.size - 1 or not np.all(np.isfinite(phase)):
        raise TemporalDensityCurrentError("seam phases must contain N-1 finite entries")
    if chi.ndim != 1 or chi.shape != state.shape or not np.all(np.isfinite(chi)):
        raise TemporalDensityCurrentError("vertex gauge must match the state")
    return np.exp(1j * chi) * state, phase + np.diff(chi)
