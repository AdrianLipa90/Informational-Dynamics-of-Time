from __future__ import annotations

import math
from typing import Sequence

import numpy as np


KAPPA = math.log(2.0) / (24.0 * math.pi)


class PhaseConnectionError(ValueError):
    pass


def _real_cycle(values: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size < 2 or not np.all(np.isfinite(arr)):
        raise PhaseConnectionError(f"{name} must be a finite one-dimensional cycle with at least two entries")
    return arr


def _state(value: Sequence[complex], name: str) -> np.ndarray:
    z = np.asarray(value, dtype=complex)
    if z.ndim != 1 or z.size < 2 or not np.all(np.isfinite(z.real)) or not np.all(np.isfinite(z.imag)):
        raise PhaseConnectionError(f"{name} must be a finite complex state vector")
    norm = float(np.linalg.norm(z))
    if norm <= 0.0:
        raise PhaseConnectionError(f"{name} must have nonzero norm")
    return z / norm


def exact_cycle_edges(state_scalar: Sequence[float]) -> np.ndarray:
    h = _real_cycle(state_scalar, "state_scalar")
    return np.roll(h, -1) - h


def pancharatnam_link(state_a: Sequence[complex], state_b: Sequence[complex], *, overlap_tol: float = 1e-14) -> complex:
    a = _state(state_a, "state_a")
    b = _state(state_b, "state_b")
    if a.shape != b.shape:
        raise PhaseConnectionError("state vectors must have equal dimension")
    overlap = np.vdot(a, b)
    if abs(overlap) <= float(overlap_tol):
        raise PhaseConnectionError("Pancharatnam link requires nonzero overlap")
    return complex(overlap / abs(overlap))


def cycle_pancharatnam_links(states: Sequence[Sequence[complex]]) -> np.ndarray:
    if len(states) < 2:
        raise PhaseConnectionError("cycle requires at least two states")
    normalized = [_state(s, f"states[{i}]") for i, s in enumerate(states)]
    shape = normalized[0].shape
    if any(s.shape != shape for s in normalized):
        raise PhaseConnectionError("all states must have equal dimension")
    return np.asarray([pancharatnam_link(normalized[i], normalized[(i + 1) % len(normalized)]) for i in range(len(normalized))], dtype=complex)


def composite_temporal_links(states: Sequence[Sequence[complex]], state_entropy_bits: Sequence[float], affinity_bits: Sequence[float], *, kappa: float = KAPPA) -> np.ndarray:
    berry = cycle_pancharatnam_links(states)
    h = _real_cycle(state_entropy_bits, "state_entropy_bits")
    sigma = _real_cycle(affinity_bits, "affinity_bits")
    if berry.size != h.size or sigma.shape != h.shape:
        raise PhaseConnectionError("states, entropy values and affinity edges must have equal cycle length")
    k = float(kappa)
    if not math.isfinite(k):
        raise PhaseConnectionError("kappa must be finite")
    exact = exact_cycle_edges(h)
    return berry * np.exp(1j * k * (exact + sigma))


def cycle_holonomy_phase(links: Sequence[complex]) -> float:
    z = np.asarray(links, dtype=complex)
    if z.ndim != 1 or z.size < 2 or not np.all(np.isfinite(z.real)) or not np.all(np.isfinite(z.imag)):
        raise PhaseConnectionError("links must be a finite one-dimensional cycle")
    if np.any(np.abs(z) <= 0.0):
        raise PhaseConnectionError("links must be nonzero")
    z = z / np.abs(z)
    return float(np.angle(np.prod(z)))


def principal_phase_difference(a: float, b: float) -> float:
    return float(np.angle(np.exp(1j * (float(a) - float(b)))))


def rephase_states(states: Sequence[Sequence[complex]], phases: Sequence[float]) -> list[np.ndarray]:
    chi = np.asarray(phases, dtype=float)
    if chi.ndim != 1 or chi.size != len(states) or not np.all(np.isfinite(chi)):
        raise PhaseConnectionError("one finite gauge phase is required per state")
    return [np.exp(1j * chi[i]) * _state(s, f"states[{i}]") for i, s in enumerate(states)]


def transform_links(links: Sequence[complex], phases: Sequence[float]) -> np.ndarray:
    z = np.asarray(links, dtype=complex)
    chi = np.asarray(phases, dtype=float)
    if z.ndim != 1 or chi.ndim != 1 or z.size != chi.size or z.size < 2:
        raise PhaseConnectionError("one link and one node phase are required per cycle edge/node")
    return np.asarray([np.exp(1j * (chi[(i + 1) % chi.size] - chi[i])) * z[i] for i in range(z.size)], dtype=complex)


def covariant_cycle_difference(values: Sequence[complex], links: Sequence[complex]) -> np.ndarray:
    q = np.asarray(values, dtype=complex)
    L = np.asarray(links, dtype=complex)
    if q.ndim != 1 or L.ndim != 1 or q.size != L.size or q.size < 2:
        raise PhaseConnectionError("one scalar state value and one link are required per cycle node/edge")
    return np.asarray([q[(i + 1) % q.size] - L[i] * q[i] for i in range(q.size)], dtype=complex)
