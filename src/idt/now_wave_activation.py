from __future__ import annotations

import math
from collections.abc import Hashable, Sequence

import numpy as np

from .temporal_wave import TemporalWaveError, gauge_incidence_matrix


def _finite_nonnegative_vector(values: Sequence[float], *, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise TemporalWaveError(f"{name} must be one-dimensional")
    if not np.all(np.isfinite(arr)) or np.any(arr < 0.0):
        raise TemporalWaveError(f"{name} must be finite and non-negative")
    return arr


def structural_transition_signature(
    fs_distance: float,
    entropy_difference_bits: float,
    affinity_bits: float,
    *,
    kappa_value: float,
) -> float:
    """Gauge-invariant structural event signature q_e from the NOW contract."""
    d = float(fs_distance)
    dH = float(entropy_difference_bits)
    sigma = float(affinity_bits)
    kap = float(kappa_value)
    if not all(math.isfinite(x) for x in (d, dH, sigma, kap)):
        raise TemporalWaveError("event-signature inputs must be finite")
    if d < 0.0:
        raise TemporalWaveError("Fubini-Study distance must be non-negative")
    return float(math.sqrt(d * d + (kap * dH) ** 2 + (kap * sigma) ** 2))


def mobility_from_activity_current(activity: float, current: float) -> float:
    """Recover M from the exact hyperbolic invariant a^2-j^2=4M^2."""
    a = float(activity)
    j = float(current)
    if not (math.isfinite(a) and math.isfinite(j)) or a <= 0.0:
        raise TemporalWaveError("activity must be positive finite and current finite")
    if abs(j) >= a:
        raise TemporalWaveError("admitted positive rates require |current| < activity")
    return float(0.5 * math.sqrt((a - j) * (a + j)))


def mobility_from_activity_current_arrays(
    activities: Sequence[float], currents: Sequence[float]
) -> np.ndarray:
    a = np.asarray(activities, dtype=float)
    j = np.asarray(currents, dtype=float)
    if a.ndim != 1 or j.ndim != 1 or a.size == 0 or a.shape != j.shape:
        raise TemporalWaveError("activities and currents must be non-empty vectors of equal shape")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(j)) or np.any(a <= 0.0):
        raise TemporalWaveError("activities must be positive finite and currents finite")
    if np.any(np.abs(j) >= a):
        raise TemporalWaveError("admitted positive rates require |current| < activity on every edge")
    return 0.5 * np.sqrt((a - j) * (a + j))


def wave_edge_activation(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    wave_state: Sequence[complex],
    edge_mobility: Sequence[float],
) -> np.ndarray:
    """Return epsilon_e=M_e |(D_L Phi)_e|^2 for each admitted edge."""
    edge_list = list(edges)
    D = gauge_incidence_matrix(n_nodes, edge_list, links)
    phi = np.asarray(wave_state, dtype=complex)
    if phi.ndim != 1 or phi.size != int(n_nodes):
        raise TemporalWaveError("wave_state must match n_nodes")
    if not np.all(np.isfinite(phi.real)) or not np.all(np.isfinite(phi.imag)):
        raise TemporalWaveError("wave_state must be finite")
    mobility = np.asarray(edge_mobility, dtype=float)
    if mobility.ndim != 1 or mobility.size != len(edge_list):
        raise TemporalWaveError("one mobility is required per edge")
    if not np.all(np.isfinite(mobility)) or np.any(mobility <= 0.0):
        raise TemporalWaveError("edge mobility must be finite and strictly positive")
    gradient = D @ phi
    return mobility * np.abs(gradient) ** 2


def wave_edge_activation_from_activity_current(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    wave_state: Sequence[complex],
    activities: Sequence[float],
    currents: Sequence[float],
) -> np.ndarray:
    mobility = mobility_from_activity_current_arrays(activities, currents)
    return wave_edge_activation(n_nodes, edges, links, wave_state, mobility)


def realized_now_weights(
    structural_signatures: Sequence[float],
    wave_activations: Sequence[float],
) -> np.ndarray:
    q = _finite_nonnegative_vector(structural_signatures, name="structural_signatures")
    eps = _finite_nonnegative_vector(wave_activations, name="wave_activations")
    if q.shape != eps.shape:
        raise TemporalWaveError("structural signatures and wave activations must have equal shape")
    return q * eps


def realized_now_measure(
    points: Sequence[Hashable],
    structural_signatures: Sequence[float],
    wave_activations: Sequence[float],
) -> dict[Hashable, float]:
    weights = realized_now_weights(structural_signatures, wave_activations)
    if len(points) != weights.size:
        raise TemporalWaveError("points must match edge weights")
    out: dict[Hashable, float] = {}
    for point, weight in zip(points, weights):
        value = float(weight)
        if value == 0.0:
            continue
        out[point] = out.get(point, 0.0) + value
    return out


def realized_now_support(
    points: Sequence[Hashable],
    structural_signatures: Sequence[float],
    wave_activations: Sequence[float],
) -> set[Hashable]:
    return set(realized_now_measure(points, structural_signatures, wave_activations))


def total_wave_activation(wave_activations: Sequence[float]) -> float:
    eps = _finite_nonnegative_vector(wave_activations, name="wave_activations")
    return float(np.sum(eps))
