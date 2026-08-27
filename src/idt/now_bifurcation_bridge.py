from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .bifurcation import BifurcationError, unitary_from_hermitian
from .kahler_time import kappa
from .now_wave_activation import mobility_from_activity_current


@dataclass(frozen=True)
class WaveBifurcationCoordinates:
    mobility: float
    edge_drive: float
    phase_increment_rad: float


@dataclass(frozen=True)
class GatedBifurcation:
    realized: bool
    realization_weight: float
    coordinates: WaveBifurcationCoordinates
    operator: np.ndarray


def wave_bifurcation_coordinates(
    activity: float,
    current: float,
    *,
    kappa_value: float | None = None,
) -> WaveBifurcationCoordinates:
    """Invert the positive kinetic pair into wave magnitude M and oriented phase beta."""
    a = float(activity)
    j = float(current)
    kap = kappa() if kappa_value is None else float(kappa_value)
    if not (math.isfinite(a) and a > 0.0):
        raise BifurcationError("activity must be finite and strictly positive")
    if not (math.isfinite(j) and math.isfinite(kap) and kap != 0.0):
        raise BifurcationError("current and non-zero kappa must be finite")
    if abs(j) >= a:
        raise BifurcationError("positive kinetic pairs require |current| < activity")
    mobility = mobility_from_activity_current(a, j)
    drive = 2.0 * math.atanh(j / a)
    beta = kap * drive / math.log(2.0)
    return WaveBifurcationCoordinates(mobility, drive, beta)


def activity_current_from_wave_bifurcation(
    mobility: float,
    phase_increment_rad: float,
    *,
    kappa_value: float | None = None,
) -> tuple[float, float]:
    """Reconstruct the kinetic pair from wave magnitude M and bifurcation phase beta."""
    M = float(mobility)
    beta = float(phase_increment_rad)
    kap = kappa() if kappa_value is None else float(kappa_value)
    if not (math.isfinite(M) and M > 0.0):
        raise BifurcationError("mobility must be finite and strictly positive")
    if not (math.isfinite(beta) and math.isfinite(kap) and kap != 0.0):
        raise BifurcationError("phase increment and non-zero kappa must be finite")
    drive = beta * math.log(2.0) / kap
    activity = 2.0 * M * math.cosh(drive / 2.0)
    current = 2.0 * M * math.sinh(drive / 2.0)
    if not (math.isfinite(activity) and math.isfinite(current)):
        raise BifurcationError("reconstructed kinetic pair overflowed")
    return float(activity), float(current)


def canonical_activity_current_from_wave_bifurcation(
    mobility: float,
    phase_increment_rad: float,
) -> tuple[float, float]:
    """Canonical kappa specialization: A=24*pi*beta."""
    M = float(mobility)
    beta = float(phase_increment_rad)
    if not (math.isfinite(M) and M > 0.0 and math.isfinite(beta)):
        raise BifurcationError("mobility must be positive finite and phase finite")
    return (
        float(2.0 * M * math.cosh(12.0 * math.pi * beta)),
        float(2.0 * M * math.sinh(12.0 * math.pi * beta)),
    )


def realized_event_weight(structural_signature: float, wave_activation: float) -> float:
    q = float(structural_signature)
    eps = float(wave_activation)
    if not (math.isfinite(q) and math.isfinite(eps)) or q < 0.0 or eps < 0.0:
        raise BifurcationError("event signature and wave activation must be finite and non-negative")
    return float(q * eps)


def wave_active_bifurcation_operator(
    structural_signature: float,
    wave_activation: float,
    activity: float,
    current: float,
    generator: Sequence[Sequence[complex]],
    *,
    kappa_value: float | None = None,
) -> GatedBifurcation:
    """Apply directional unitary bifurcation exactly on the wave-active NOW support.

    The positive product q_e*epsilon_e gates realization. The current/activity
    rapidity supplies beta. Zero realization weight returns the identity operator.
    """
    coordinates = wave_bifurcation_coordinates(
        activity, current, kappa_value=kappa_value
    )
    weight = realized_event_weight(structural_signature, wave_activation)
    g = np.asarray(generator, dtype=complex)
    if g.ndim != 2 or g.shape[0] != g.shape[1] or g.shape[0] == 0:
        raise BifurcationError("generator must be a non-empty square matrix")
    if not np.all(np.isfinite(g.real)) or not np.all(np.isfinite(g.imag)):
        raise BifurcationError("generator must be finite")
    if not np.allclose(g, g.conj().T, atol=1e-12, rtol=0.0):
        raise BifurcationError("generator must be Hermitian")
    if weight == 0.0:
        op = np.eye(g.shape[0], dtype=complex)
        return GatedBifurcation(False, weight, coordinates, op)
    op = unitary_from_hermitian(coordinates.phase_increment_rad, g)
    return GatedBifurcation(True, weight, coordinates, op)
