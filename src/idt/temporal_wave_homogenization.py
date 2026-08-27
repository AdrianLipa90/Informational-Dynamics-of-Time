from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .temporal_wave import TemporalWaveError
from .temporal_wave_dissipation import viscosity_edge_weights
from .temporal_wave import mobility_edge_weights


@dataclass(frozen=True)
class EffectiveLongWaveCoefficients:
    mobility_eff: float
    damping_eff: float
    wave_speed: float
    attenuation: float


def _positive_vector(values: Sequence[float], *, name: str, minimum_length: int = 2) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size < int(minimum_length):
        raise TemporalWaveError(f"{name} must be one-dimensional with at least {minimum_length} entries")
    if not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise TemporalWaveError(f"{name} must be finite and strictly positive")
    return arr


def periodic_relational_edge_fields(
    rho: Sequence[float],
    eta: Sequence[float],
) -> tuple[np.ndarray, np.ndarray]:
    """Return periodic nearest-neighbour mobility M_e and pair viscosity eta_bar_e."""
    rho_arr = _positive_vector(rho, name="rho", minimum_length=3)
    eta_arr = _positive_vector(eta, name="eta", minimum_length=3)
    if rho_arr.size != eta_arr.size:
        raise TemporalWaveError("rho and eta must have the same periodic cell length")
    n = rho_arr.size
    edges = [(j, (j + 1) % n) for j in range(n)]
    mobility = mobility_edge_weights(edges, rho_arr, eta_arr)
    viscosity = viscosity_edge_weights(edges, eta_arr)
    return mobility, viscosity


def periodic_bloch_incidence(
    n_edges: int,
    cell_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> np.ndarray:
    """Periodic 1D Bloch incidence with total phase exp(i*cell_phase) across one cell."""
    n = int(n_edges)
    theta = float(cell_phase)
    h = float(edge_spacing)
    if n < 2:
        raise TemporalWaveError("periodic Bloch cell requires at least two edges")
    if not math.isfinite(theta):
        raise TemporalWaveError("cell_phase must be finite")
    if not math.isfinite(h) or h <= 0.0:
        raise TemporalWaveError("edge_spacing must be finite and strictly positive")
    D = np.zeros((n, n), dtype=complex)
    for j in range(n - 1):
        D[j, j] = -1.0 / h
        D[j, j + 1] = 1.0 / h
    D[-1, -1] = -1.0 / h
    D[-1, 0] = np.exp(1j * theta) / h
    return D


def periodic_bloch_operators(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    cell_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return stiffness K(theta) and damping C(theta) for one periodic heterogeneous cell."""
    M = _positive_vector(mobility, name="mobility")
    E = _positive_vector(viscosity, name="viscosity")
    if M.size != E.size:
        raise TemporalWaveError("mobility and viscosity must have the same cell length")
    D = periodic_bloch_incidence(M.size, cell_phase, edge_spacing=edge_spacing)
    K = D.conj().T @ (M[:, None] * D)
    C = D.conj().T @ (E[:, None] * D)
    K = 0.5 * (K + K.conj().T)
    C = 0.5 * (C + C.conj().T)
    return K, C


def effective_long_wave_coefficients(
    mobility: Sequence[float],
    viscosity: Sequence[float],
) -> EffectiveLongWaveCoefficients:
    """1D periodic acoustic coefficients obtained from the stiffness cell corrector.

    M_eff is the harmonic mean of M_e. The damping coefficient is evaluated on
    the same long-wave stiffness corrector, yielding
        beta_eff = M_eff^2 * mean(eta_e / M_e^2).
    """
    M = _positive_vector(mobility, name="mobility")
    E = _positive_vector(viscosity, name="viscosity")
    if M.size != E.size:
        raise TemporalWaveError("mobility and viscosity must have the same cell length")
    M_eff = float(1.0 / np.mean(1.0 / M))
    beta_eff = float(M_eff * M_eff * np.mean(E / (M * M)))
    return EffectiveLongWaveCoefficients(
        mobility_eff=M_eff,
        damping_eff=beta_eff,
        wave_speed=float(math.sqrt(M_eff)),
        attenuation=float(0.5 * beta_eff),
    )


def relational_effective_long_wave_coefficients(
    rho: Sequence[float],
    eta: Sequence[float],
) -> EffectiveLongWaveCoefficients:
    mobility, viscosity = periodic_relational_edge_fields(rho, eta)
    return effective_long_wave_coefficients(mobility, viscosity)


def acoustic_bloch_exponent(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    cell_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> tuple[complex, float]:
    """Return the positive-frequency acoustic exponent s and physical k.

    The second-order system is qddot + C qdot + K q = 0. For e^{s lambda},
    the acoustic pair has s=-Gamma(k)+/-i Omega(k). The returned member has
    positive imaginary part.
    """
    M = _positive_vector(mobility, name="mobility")
    E = _positive_vector(viscosity, name="viscosity")
    if M.size != E.size:
        raise TemporalWaveError("mobility and viscosity must have the same cell length")
    theta = float(cell_phase)
    h = float(edge_spacing)
    if theta == 0.0:
        raise TemporalWaveError("acoustic extraction requires non-zero cell_phase")
    K, C = periodic_bloch_operators(M, E, theta, edge_spacing=h)
    n = M.size
    first_order = np.block([
        [np.zeros((n, n), dtype=complex), np.eye(n, dtype=complex)],
        [-K, -C],
    ])
    spectrum = np.linalg.eigvals(first_order)
    positive = [z for z in spectrum if z.imag > 1e-10]
    if not positive:
        raise TemporalWaveError("declared Bloch point has no positive-frequency acoustic branch")
    acoustic = min(positive, key=abs)
    wave_number = theta / (n * h)
    return complex(acoustic), float(wave_number)


def acoustic_coefficient_estimate(
    mobility: Sequence[float],
    viscosity: Sequence[float],
    cell_phase: float,
    *,
    edge_spacing: float = 1.0,
) -> tuple[float, float]:
    """Estimate c and beta from the exact Bloch acoustic exponent.

    s = -beta*k^2/2 + i*c*k + higher-order terms for positive k.
    """
    s, k = acoustic_bloch_exponent(
        mobility,
        viscosity,
        cell_phase,
        edge_spacing=edge_spacing,
    )
    if k <= 0.0:
        raise TemporalWaveError("coefficient extraction requires positive cell_phase")
    c_est = float(s.imag / k)
    beta_est = float(-2.0 * s.real / (k * k))
    return c_est, beta_est


def harmonic_viscosity_candidate(viscosity: Sequence[float]) -> float:
    """Return the simple harmonic-viscosity comparison candidate used by the baseline gate."""
    E = _positive_vector(viscosity, name="viscosity")
    return float(1.0 / np.mean(1.0 / E))
