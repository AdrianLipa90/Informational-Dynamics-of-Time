from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class HalfFrameGluingError(ValueError):
    pass


@dataclass(frozen=True)
class HalfFrameAudit:
    frame_count: int
    phase_budget: float
    support_labels: tuple[str, ...]
    glued_amplitudes: np.ndarray
    seam_defects: np.ndarray
    glued_weight: float
    seam_defect_weight: float
    norm_residual: float


def _validate_frame_count(frame_count: int) -> int:
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise HalfFrameGluingError("frame_count must be a positive integer")
    return frame_count


def modular_phase_budget(frame_count: int) -> float:
    n = _validate_frame_count(frame_count)
    return 2.0 * math.pi * n


def glued_support_labels(frame_count: int) -> tuple[str, ...]:
    n = _validate_frame_count(frame_count)
    if n == 1:
        return ("1", "1")
    labels = ["1"]
    labels.extend(f"{k}{k + 1}" for k in range(1, n))
    labels.append(str(n))
    return tuple(labels)


def split_isometry(frame_count: int) -> np.ndarray:
    n = _validate_frame_count(frame_count)
    s = np.zeros((2 * n, n), dtype=complex)
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    for k in range(n):
        s[2 * k, k] = inv_sqrt2
        s[2 * k + 1, k] = inv_sqrt2
    return s


def gluing_coisometry(frame_count: int) -> np.ndarray:
    n = _validate_frame_count(frame_count)
    q = np.zeros((n + 1, 2 * n), dtype=complex)
    inv_sqrt2 = 1.0 / math.sqrt(2.0)

    q[0, 0] = 1.0
    q[n, 2 * n - 1] = 1.0
    for seam in range(1, n):
        right_of_left_frame = 2 * (seam - 1) + 1
        left_of_right_frame = 2 * seam
        q[seam, right_of_left_frame] = inv_sqrt2
        q[seam, left_of_right_frame] = inv_sqrt2
    return q


def antisymmetric_seam_basis(frame_count: int) -> np.ndarray:
    n = _validate_frame_count(frame_count)
    if n == 1:
        return np.zeros((2, 0), dtype=complex)
    a = np.zeros((2 * n, n - 1), dtype=complex)
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    for seam in range(1, n):
        right_of_left_frame = 2 * (seam - 1) + 1
        left_of_right_frame = 2 * seam
        a[right_of_left_frame, seam - 1] = inv_sqrt2
        a[left_of_right_frame, seam - 1] = -inv_sqrt2
    return a


def whole_to_glued_operator(frame_count: int) -> np.ndarray:
    return gluing_coisometry(frame_count) @ split_isometry(frame_count)


def _normalized_frame_amplitudes(amplitudes: Sequence[complex]) -> np.ndarray:
    a = np.asarray(amplitudes, dtype=complex)
    if a.ndim != 1 or a.size == 0:
        raise HalfFrameGluingError("amplitudes must be a non-empty one-dimensional vector")
    if not np.all(np.isfinite(a)):
        raise HalfFrameGluingError("amplitudes must be finite")
    norm = float(np.linalg.norm(a))
    if not math.isfinite(norm) or norm <= 0.0:
        raise HalfFrameGluingError("amplitudes must have positive finite norm")
    return a / norm


def glued_amplitudes(amplitudes: Sequence[complex]) -> np.ndarray:
    a = _normalized_frame_amplitudes(amplitudes)
    return whole_to_glued_operator(a.size) @ a


def seam_defect_amplitudes(amplitudes: Sequence[complex]) -> np.ndarray:
    a = _normalized_frame_amplitudes(amplitudes)
    if a.size == 1:
        return np.zeros(0, dtype=complex)
    return 0.5 * (a[:-1] - a[1:])


def norm_decomposition(amplitudes: Sequence[complex]) -> tuple[float, float, float]:
    a = _normalized_frame_amplitudes(amplitudes)
    b = whole_to_glued_operator(a.size) @ a
    d = seam_defect_amplitudes(a)
    glued_weight = float(np.vdot(b, b).real)
    defect_weight = float(np.vdot(d, d).real)
    residual = abs(1.0 - glued_weight - defect_weight)
    return glued_weight, defect_weight, residual


def interface_occupancy(amplitudes: Sequence[complex]) -> float:
    b = glued_amplitudes(amplitudes)
    if b.size <= 2:
        return 0.0
    return float(np.sum(np.abs(b[1:-1]) ** 2))


def conditional_glued_probabilities(amplitudes: Sequence[complex]) -> np.ndarray:
    b = glued_amplitudes(amplitudes)
    norm2 = float(np.vdot(b, b).real)
    if norm2 <= 1e-15:
        raise HalfFrameGluingError("glued sector has zero norm")
    return (np.abs(b) ** 2) / norm2


def audit_half_frame_state(amplitudes: Sequence[complex]) -> HalfFrameAudit:
    a = _normalized_frame_amplitudes(amplitudes)
    b = whole_to_glued_operator(a.size) @ a
    d = seam_defect_amplitudes(a)
    glued_weight = float(np.vdot(b, b).real)
    defect_weight = float(np.vdot(d, d).real)
    return HalfFrameAudit(
        frame_count=int(a.size),
        phase_budget=modular_phase_budget(int(a.size)),
        support_labels=glued_support_labels(int(a.size)),
        glued_amplitudes=b,
        seam_defects=d,
        glued_weight=glued_weight,
        seam_defect_weight=defect_weight,
        norm_residual=abs(1.0 - glued_weight - defect_weight),
    )
