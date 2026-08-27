from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .temporal_wave_homogenization import (
    EffectiveLongWaveCoefficients,
    TemporalWaveError,
    effective_long_wave_coefficients,
)


@dataclass(frozen=True)
class HolonomyLongWaveState:
    holonomy_phase: float
    bloch_phase: float
    shifted_cell_phase: float
    shifted_wave_number: float
    coefficients: EffectiveLongWaveCoefficients
    predicted_exponent: complex


def _finite_phase_vector(values: Sequence[float], *, name: str = "link_phases") -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size < 2:
        raise TemporalWaveError(f"{name} must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(arr)):
        raise TemporalWaveError(f"{name} must be finite")
    return arr


def _positive_vector(values: Sequence[float], *, name: str, n: int) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size != n:
        raise TemporalWaveError(f"{name} must match link count")
    if not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise TemporalWaveError(f"{name} must be finite and strictly positive")
    return arr


def wrap_phase(x: float) -> float:
    value = float(x)
    if not math.isfinite(value):
        raise TemporalWaveError("phase must be finite")
    return math.atan2(math.sin(value), math.cos(value))


def total_holonomy_phase(link_phases: Sequence[float]) -> float:
    phases = _finite_phase_vector(link_phases)
    return wrap_phase(float(np.sum(phases)))


def gauge_redistribute_link_phases(
    link_phases: Sequence[float],
    node_phases: Sequence[float],
) -> np.ndarray:
    phases = _finite_phase_vector(link_phases)
    chi = np.asarray(node_phases, dtype=float)
    if chi.ndim != 1 or chi.size != phases.size or not np.all(np.isfinite(chi)):
        raise TemporalWaveError("node_phases must be finite and match link count")
    return phases + np.roll(chi, -1) - chi


def holonomy_bloch_incidence(
    link_phases: Sequence[float],
    bloch_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> np.ndarray:
    phases = _finite_phase_vector(link_phases)
    theta = float(bloch_phase)
    h = float(edge_spacing)
    if not math.isfinite(theta):
        raise TemporalWaveError("bloch_phase must be finite")
    if not math.isfinite(h) or h <= 0.0:
        raise TemporalWaveError("edge_spacing must be finite and strictly positive")
    n = phases.size
    D = np.zeros((n, n), dtype=complex)
    for j in range(n - 1):
        D[j, j] = -np.exp(1j * phases[j]) / h
        D[j, j + 1] = 1.0 / h
    D[-1, -1] = -np.exp(1j * phases[-1]) / h
    D[-1, 0] = np.exp(1j * theta) / h
    return D


def holonomy_bloch_operators(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    link_phases: Sequence[float],
    bloch_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    phases = _finite_phase_vector(link_phases)
    M = _positive_vector(mobility, name="mobility", n=phases.size)
    E = _positive_vector(viscosity, name="viscosity", n=phases.size)
    D = holonomy_bloch_incidence(phases, bloch_phase, edge_spacing=edge_spacing)
    K = D.conj().T @ (M[:, None] * D)
    C = D.conj().T @ (E[:, None] * D)
    return 0.5 * (K + K.conj().T), 0.5 * (C + C.conj().T)


def shifted_cell_phase(link_phases: Sequence[float], bloch_phase: float) -> float:
    return wrap_phase(float(bloch_phase) - total_holonomy_phase(link_phases))


def shifted_wave_number(
    link_phases: Sequence[float],
    bloch_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> float:
    phases = _finite_phase_vector(link_phases)
    h = float(edge_spacing)
    if not math.isfinite(h) or h <= 0.0:
        raise TemporalWaveError("edge_spacing must be finite and strictly positive")
    return shifted_cell_phase(phases, bloch_phase) / (phases.size * h)


def acoustic_holonomy_exponent(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    link_phases: Sequence[float],
    bloch_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> tuple[complex, float]:
    phases = _finite_phase_vector(link_phases)
    M = _positive_vector(mobility, name="mobility", n=phases.size)
    E = _positive_vector(viscosity, name="viscosity", n=phases.size)
    k = shifted_wave_number(phases, bloch_phase, edge_spacing=edge_spacing)
    if abs(k) <= 1e-15:
        raise TemporalWaveError("acoustic extraction requires non-zero shifted wave number")
    K, C = holonomy_bloch_operators(
        M,
        E,
        phases,
        bloch_phase,
        edge_spacing=edge_spacing,
    )
    n = M.size
    first_order = np.block([
        [np.zeros((n, n), dtype=complex), np.eye(n, dtype=complex)],
        [-K, -C],
    ])
    spectrum = np.linalg.eigvals(first_order)
    positive = [z for z in spectrum if z.imag > 1e-10]
    if not positive:
        raise TemporalWaveError("declared shifted Bloch point has no positive-frequency acoustic branch")
    acoustic = min(positive, key=abs)
    return complex(acoustic), float(k)


def holonomy_long_wave_state(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    link_phases: Sequence[float],
    bloch_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> HolonomyLongWaveState:
    phases = _finite_phase_vector(link_phases)
    coefficients = effective_long_wave_coefficients(mobility, viscosity)
    delta = shifted_cell_phase(phases, bloch_phase)
    k = delta / (phases.size * float(edge_spacing))
    predicted = complex(
        -0.5 * coefficients.damping_eff * k * k,
        coefficients.wave_speed * abs(k),
    )
    return HolonomyLongWaveState(
        holonomy_phase=total_holonomy_phase(phases),
        bloch_phase=float(bloch_phase),
        shifted_cell_phase=delta,
        shifted_wave_number=float(k),
        coefficients=coefficients,
        predicted_exponent=predicted,
    )
