from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .half_frame_temporal_gluing import HalfFrameGluingError, split_isometry


def _phase_vector(seam_phases: Sequence[float], frame_count: int) -> np.ndarray:
    phases = np.asarray(seam_phases, dtype=float)
    expected = max(0, frame_count - 1)
    if phases.ndim != 1 or phases.size != expected:
        raise HalfFrameGluingError("seam_phases must have frame_count-1 entries")
    if not np.all(np.isfinite(phases)):
        raise HalfFrameGluingError("seam_phases must be finite")
    return phases


def phase_aware_gluing_coisometry(frame_count: int, seam_phases: Sequence[float]) -> np.ndarray:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise HalfFrameGluingError("frame_count must be a positive integer")
    phases = _phase_vector(seam_phases, frame_count)
    q = np.zeros((frame_count + 1, 2 * frame_count), dtype=complex)
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    q[0, 0] = 1.0
    q[frame_count, 2 * frame_count - 1] = 1.0
    for seam, phi in enumerate(phases, start=1):
        right_left = 2 * (seam - 1) + 1
        left_right = 2 * seam
        q[seam, right_left] = np.exp(0.5j * phi) * inv_sqrt2
        q[seam, left_right] = np.exp(-0.5j * phi) * inv_sqrt2
    return q


def phase_aware_whole_to_glued(frame_count: int, seam_phases: Sequence[float]) -> np.ndarray:
    return phase_aware_gluing_coisometry(frame_count, seam_phases) @ split_isometry(frame_count)


def _normalized(amplitudes: Sequence[complex]) -> np.ndarray:
    a = np.asarray(amplitudes, dtype=complex)
    if a.ndim != 1 or a.size == 0 or not np.all(np.isfinite(a)):
        raise HalfFrameGluingError("amplitudes must be a finite non-empty vector")
    norm = float(np.linalg.norm(a))
    if norm <= 0.0 or not math.isfinite(norm):
        raise HalfFrameGluingError("amplitudes must have positive finite norm")
    return a / norm


def phase_aware_glued_amplitudes(amplitudes: Sequence[complex], seam_phases: Sequence[float]) -> np.ndarray:
    a = _normalized(amplitudes)
    return phase_aware_whole_to_glued(a.size, seam_phases) @ a


def phase_aware_seam_defects(amplitudes: Sequence[complex], seam_phases: Sequence[float]) -> np.ndarray:
    a = _normalized(amplitudes)
    phases = _phase_vector(seam_phases, int(a.size))
    if a.size == 1:
        return np.zeros(0, dtype=complex)
    return 0.5 * (
        np.exp(0.5j * phases) * a[:-1]
        - np.exp(-0.5j * phases) * a[1:]
    )


def phase_aware_norm_decomposition(
    amplitudes: Sequence[complex], seam_phases: Sequence[float]
) -> tuple[float, float, float]:
    a = _normalized(amplitudes)
    b = phase_aware_whole_to_glued(a.size, seam_phases) @ a
    d = phase_aware_seam_defects(a, seam_phases)
    glued = float(np.vdot(b, b).real)
    defect = float(np.vdot(d, d).real)
    return glued, defect, abs(1.0 - glued - defect)


def gauge_transform(
    amplitudes: Sequence[complex],
    seam_phases: Sequence[float],
    vertex_phases: Sequence[float],
) -> tuple[np.ndarray, np.ndarray]:
    a = _normalized(amplitudes)
    seam = _phase_vector(seam_phases, int(a.size))
    chi = np.asarray(vertex_phases, dtype=float)
    if chi.ndim != 1 or chi.size != a.size or not np.all(np.isfinite(chi)):
        raise HalfFrameGluingError("vertex_phases must be finite with frame_count entries")
    transformed_a = np.exp(1j * chi) * a
    transformed_seam = seam + np.diff(chi)
    return transformed_a, transformed_seam


def seam_probabilities(amplitudes: Sequence[complex], seam_phases: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    b = phase_aware_glued_amplitudes(amplitudes, seam_phases)
    d = phase_aware_seam_defects(amplitudes, seam_phases)
    return np.abs(b[1:-1]) ** 2, np.abs(d) ** 2


def remove_exact_gradient_seam(seam_phases: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    phases = np.asarray(seam_phases, dtype=float)
    if phases.ndim != 1 or not np.all(np.isfinite(phases)):
        raise HalfFrameGluingError("seam_phases must be a finite vector")
    beta = np.zeros(phases.size + 1, dtype=float)
    if phases.size:
        beta[1:] = np.cumsum(phases)
    transformed = phases - np.diff(beta)
    return beta, transformed
