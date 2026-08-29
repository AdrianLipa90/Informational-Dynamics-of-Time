from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class HalfFrameContinuumError(ValueError):
    pass


@dataclass(frozen=True)
class HalfFrameContinuumProfile:
    fuzzy_density: np.ndarray
    defect_density: np.ndarray
    fuzzy_quality: np.ndarray
    defect_amplitudes: np.ndarray


def _positive_spacing(h: float) -> float:
    out = float(h)
    if not math.isfinite(out) or out <= 0.0:
        raise HalfFrameContinuumError("mesh spacing h must be finite and positive")
    return out


def _finite_complex(value: complex, name: str) -> complex:
    z = complex(value)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise HalfFrameContinuumError(f"{name} must be finite")
    return z


def phase_aware_defect(left: complex, right: complex, seam_phase: float) -> complex:
    a0 = _finite_complex(left, "left")
    a1 = _finite_complex(right, "right")
    phi = float(seam_phase)
    if not math.isfinite(phi):
        raise HalfFrameContinuumError("seam_phase must be finite")
    return 0.5 * (
        np.exp(0.5j * phi) * a0
        - np.exp(-0.5j * phi) * a1
    )


def pair_fuzzy_quality(left: complex, right: complex, seam_phase: float) -> float:
    a0 = _finite_complex(left, "left")
    a1 = _finite_complex(right, "right")
    phi = float(seam_phase)
    if not math.isfinite(phi):
        raise HalfFrameContinuumError("seam_phase must be finite")
    r0 = abs(a0)
    r1 = abs(a1)
    denom = r0 * r0 + r1 * r1
    if denom == 0.0:
        return 0.0
    g = 2.0 * r0 * r1 / denom
    if r0 == 0.0 or r1 == 0.0:
        return 0.0
    delta = float(np.angle(a1) - np.angle(a0) - phi)
    return float(g * math.cos(0.5 * delta) ** 2)


def fuzzy_interface_mass(left: complex, right: complex, seam_phase: float) -> float:
    a0 = _finite_complex(left, "left")
    a1 = _finite_complex(right, "right")
    quality = pair_fuzzy_quality(a0, a1, seam_phase)
    return float((abs(a0) ** 2 + abs(a1) ** 2) * quality)


def continuum_fuzzy_density(
    left: complex,
    right: complex,
    seam_phase: float,
    h: float,
) -> float:
    spacing = _positive_spacing(h)
    return fuzzy_interface_mass(left, right, seam_phase) / (2.0 * spacing)


def continuum_defect_density(
    left: complex,
    right: complex,
    seam_phase: float,
    h: float,
) -> float:
    spacing = _positive_spacing(h)
    defect = phase_aware_defect(left, right, seam_phase)
    return float(4.0 * abs(defect) ** 2 / spacing**3)


def continuum_profiles(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    h: float,
) -> HalfFrameContinuumProfile:
    spacing = _positive_spacing(h)
    psi = np.asarray(amplitudes, dtype=complex)
    phi = np.asarray(seam_phases, dtype=float)
    if psi.ndim != 1 or psi.size < 2 or not np.all(np.isfinite(psi)):
        raise HalfFrameContinuumError("amplitudes must be a finite one-dimensional vector with N>=2")
    if phi.ndim != 1 or phi.size != psi.size - 1 or not np.all(np.isfinite(phi)):
        raise HalfFrameContinuumError("seam_phases must contain exactly N-1 finite entries")

    fuzzy_density = np.empty(phi.size, dtype=float)
    defect_density = np.empty(phi.size, dtype=float)
    fuzzy_quality = np.empty(phi.size, dtype=float)
    defects = np.empty(phi.size, dtype=complex)

    for i, seam in enumerate(phi):
        left = psi[i]
        right = psi[i + 1]
        fuzzy_quality[i] = pair_fuzzy_quality(left, right, float(seam))
        fuzzy_density[i] = continuum_fuzzy_density(left, right, float(seam), spacing)
        defects[i] = phase_aware_defect(left, right, float(seam))
        defect_density[i] = 4.0 * abs(defects[i]) ** 2 / spacing**3

    return HalfFrameContinuumProfile(
        fuzzy_density=fuzzy_density,
        defect_density=defect_density,
        fuzzy_quality=fuzzy_quality,
        defect_amplitudes=defects,
    )


def integrated_fuzzy_measure(fuzzy_density: Sequence[float], h: float) -> float:
    spacing = _positive_spacing(h)
    rho = np.asarray(fuzzy_density, dtype=float)
    if rho.ndim != 1 or rho.size == 0 or not np.all(np.isfinite(rho)) or np.any(rho < -1e-14):
        raise HalfFrameContinuumError("fuzzy_density must be a finite non-negative vector")
    return float(spacing * np.sum(np.maximum(rho, 0.0)))


def weighted_defect_energy(
    defect_density: Sequence[float],
    mobilities: Sequence[float],
    h: float,
) -> float:
    spacing = _positive_spacing(h)
    eps = np.asarray(defect_density, dtype=float)
    mob = np.asarray(mobilities, dtype=float)
    if eps.ndim != 1 or mob.ndim != 1 or eps.shape != mob.shape or eps.size == 0:
        raise HalfFrameContinuumError("defect_density and mobilities must be equal non-empty vectors")
    if not np.all(np.isfinite(eps)) or not np.all(np.isfinite(mob)):
        raise HalfFrameContinuumError("weighted energy inputs must be finite")
    if np.any(eps < -1e-14) or np.any(mob <= 0.0):
        raise HalfFrameContinuumError("defect density must be non-negative and mobilities positive")
    return float(spacing * np.dot(mob, np.maximum(eps, 0.0)))


def gauge_transform_samples(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    vertex_gauge: Sequence[float],
) -> tuple[np.ndarray, np.ndarray]:
    psi = np.asarray(amplitudes, dtype=complex)
    phi = np.asarray(seam_phases, dtype=float)
    chi = np.asarray(vertex_gauge, dtype=float)
    if psi.ndim != 1 or psi.size < 2 or not np.all(np.isfinite(psi)):
        raise HalfFrameContinuumError("amplitudes must be finite with N>=2")
    if chi.ndim != 1 or chi.shape != psi.shape or not np.all(np.isfinite(chi)):
        raise HalfFrameContinuumError("vertex_gauge must match amplitudes")
    if phi.ndim != 1 or phi.size != psi.size - 1 or not np.all(np.isfinite(phi)):
        raise HalfFrameContinuumError("seam_phases must contain N-1 finite entries")
    transformed_state = np.exp(1j * chi) * psi
    transformed_seams = phi + np.diff(chi)
    return transformed_state, transformed_seams
