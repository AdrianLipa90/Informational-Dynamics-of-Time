from __future__ import annotations

import math
from typing import Sequence

import numpy as np


class MemoryOrbitError(ValueError):
    pass


def _finite_complex(z: complex, name: str) -> complex:
    c = complex(z)
    if not (math.isfinite(c.real) and math.isfinite(c.imag)):
        raise MemoryOrbitError(f"{name} must be finite")
    return c


def memory_edge_drive(m_a: complex, m_b: complex, *, coupling: float = 1.0) -> float:
    """Oriented memory-edge drive lambda * Im(conj(m_a) * m_b)."""
    a = _finite_complex(m_a, "m_a")
    b = _finite_complex(m_b, "m_b")
    lam = float(coupling)
    if not math.isfinite(lam):
        raise MemoryOrbitError("coupling must be finite")
    return float(lam * (a.conjugate() * b).imag)


def cycle_memory_drive(memory_coordinates: Sequence[complex], *, coupling: float = 1.0) -> float:
    coords = [_finite_complex(z, "memory coordinate") for z in memory_coordinates]
    if len(coords) < 3:
        raise MemoryOrbitError("closed memory orbit requires at least three vertices")
    return float(sum(memory_edge_drive(coords[i], coords[(i + 1) % len(coords)], coupling=coupling) for i in range(len(coords))))


def signed_polygon_area(memory_coordinates: Sequence[complex]) -> float:
    coords = [_finite_complex(z, "memory coordinate") for z in memory_coordinates]
    if len(coords) < 3:
        raise MemoryOrbitError("polygon area requires at least three vertices")
    xy = np.asarray([[z.real, z.imag] for z in coords], dtype=float)
    x = xy[:, 0]
    y = xy[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def memory_affinity_bits(m_a: complex, m_b: complex, *, coupling: float = 1.0) -> float:
    return float(memory_edge_drive(m_a, m_b, coupling=coupling) / math.log(2.0))


def cycle_memory_affinity_bits(memory_coordinates: Sequence[complex], *, coupling: float = 1.0) -> float:
    return float(cycle_memory_drive(memory_coordinates, coupling=coupling) / math.log(2.0))
