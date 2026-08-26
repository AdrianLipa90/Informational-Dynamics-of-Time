from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class CPNMemoryFrameError(ValueError):
    pass


@dataclass(frozen=True)
class CPNMemoryFrame:
    anchor_state: np.ndarray
    e_q: np.ndarray
    e_p: np.ndarray


@dataclass(frozen=True)
class CPNMemoryProjection:
    delta_m: complex
    fs_distance: float
    residual_norm: float


def _normalized_state(state: Sequence[complex], name: str) -> np.ndarray:
    psi = np.asarray(state, dtype=complex)
    if psi.ndim != 1 or psi.size < 2:
        raise CPNMemoryFrameError(f"{name} must be a complex vector of dimension at least two")
    if not np.all(np.isfinite(psi.real)) or not np.all(np.isfinite(psi.imag)):
        raise CPNMemoryFrameError(f"{name} must be finite")
    norm2 = float(np.vdot(psi, psi).real)
    if not math.isfinite(norm2) or norm2 <= 0.0:
        raise CPNMemoryFrameError(f"{name} must have positive finite norm")
    return psi / math.sqrt(norm2)


def _same_dimension(a: np.ndarray, b: np.ndarray) -> None:
    if a.shape != b.shape:
        raise CPNMemoryFrameError("state dimensions must match")


def _aligned_geodesic(
    state_from: Sequence[complex],
    state_to: Sequence[complex],
    *,
    cut_locus_tol: float = 1e-12,
) -> tuple[np.ndarray, np.ndarray, float, np.ndarray | None]:
    psi = _normalized_state(state_from, "state_from")
    phi = _normalized_state(state_to, "state_to")
    _same_dimension(psi, phi)

    overlap = np.vdot(psi, phi)
    c = float(abs(overlap))
    c = float(np.clip(c, 0.0, 1.0))
    if c <= cut_locus_tol:
        raise CPNMemoryFrameError("Fubini-Study shortest geodesic is ambiguous at the orthogonal cut locus")

    phase = np.exp(-1j * np.angle(overlap))
    aligned = phi * phase
    theta = float(math.acos(c))
    if theta <= 1e-14:
        return psi, aligned, 0.0, None

    raw = aligned - c * psi
    s = float(np.linalg.norm(raw))
    if not math.isfinite(s) or s <= 0.0:
        raise CPNMemoryFrameError("Fubini-Study logarithm tangent is singular")
    u = raw / s
    if abs(np.vdot(psi, u)) > 1e-10:
        raise CPNMemoryFrameError("Fubini-Study logarithm must be horizontal")
    return psi, aligned, theta, u


def fs_distance_cpn(state_a: Sequence[complex], state_b: Sequence[complex]) -> float:
    psi = _normalized_state(state_a, "state_a")
    phi = _normalized_state(state_b, "state_b")
    _same_dimension(psi, phi)
    overlap = float(abs(np.vdot(psi, phi)))
    overlap = float(np.clip(overlap, 0.0, 1.0))
    return float(math.acos(overlap))


def fs_log_map_cpn(
    state_from: Sequence[complex],
    state_to: Sequence[complex],
    *,
    cut_locus_tol: float = 1e-12,
) -> np.ndarray:
    psi, _, theta, u = _aligned_geodesic(state_from, state_to, cut_locus_tol=cut_locus_tol)
    if u is None:
        return np.zeros_like(psi)
    return theta * u


def _validated_frame(frame: CPNMemoryFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    psi = _normalized_state(frame.anchor_state, "frame.anchor_state")
    e_q = np.asarray(frame.e_q, dtype=complex)
    e_p = np.asarray(frame.e_p, dtype=complex)
    if e_q.shape != psi.shape or e_p.shape != psi.shape:
        raise CPNMemoryFrameError("frame axes must match the anchor dimension")
    if not np.all(np.isfinite(e_q.real)) or not np.all(np.isfinite(e_q.imag)):
        raise CPNMemoryFrameError("frame.e_q must be finite")
    if not np.all(np.isfinite(e_p.real)) or not np.all(np.isfinite(e_p.imag)):
        raise CPNMemoryFrameError("frame.e_p must be finite")
    if abs(np.vdot(psi, e_q)) > 1e-10 or abs(np.vdot(psi, e_p)) > 1e-10:
        raise CPNMemoryFrameError("frame axes must be horizontal at the anchor")
    if not np.isclose(np.linalg.norm(e_q), 1.0, atol=1e-10, rtol=0.0):
        raise CPNMemoryFrameError("frame.e_q must have unit norm")
    if not np.isclose(np.linalg.norm(e_p), 1.0, atol=1e-10, rtol=0.0):
        raise CPNMemoryFrameError("frame.e_p must have unit norm")
    if abs(float(np.vdot(e_q, e_p).real)) > 1e-10:
        raise CPNMemoryFrameError("frame axes must be orthogonal in the Fubini-Study real metric")
    if not np.allclose(e_p, 1j * e_q, atol=1e-10, rtol=0.0):
        raise CPNMemoryFrameError("reference subclass requires e_p = J e_q = i e_q")
    return psi, e_q, e_p


def initial_cpn_memory_frame(
    state_from: Sequence[complex],
    state_to: Sequence[complex],
    *,
    cut_locus_tol: float = 1e-12,
) -> CPNMemoryFrame:
    psi, _, theta, u = _aligned_geodesic(state_from, state_to, cut_locus_tol=cut_locus_tol)
    if u is None or theta <= 0.0:
        raise CPNMemoryFrameError("initial memory frame requires a nonzero projective displacement")
    e_q = u
    e_p = 1j * u
    frame = CPNMemoryFrame(psi.copy(), e_q.copy(), e_p.copy())
    _validated_frame(frame)
    return frame


def project_cpn_event(
    frame: CPNMemoryFrame,
    state_to: Sequence[complex],
    *,
    cut_locus_tol: float = 1e-12,
) -> CPNMemoryProjection:
    psi, e_q, e_p = _validated_frame(frame)
    xi = fs_log_map_cpn(psi, state_to, cut_locus_tol=cut_locus_tol)
    distance = float(np.linalg.norm(xi))
    x = float(np.vdot(e_q, xi).real)
    y = float(np.vdot(e_p, xi).real)
    delta_m = complex(x, y)
    residual2 = distance * distance - abs(delta_m) ** 2
    if residual2 < -1e-10:
        raise CPNMemoryFrameError("memory-plane projection exceeds the Fubini-Study tangent norm")
    residual = math.sqrt(max(0.0, residual2))
    return CPNMemoryProjection(delta_m, distance, residual)


def parallel_transport_cpn_frame(
    frame: CPNMemoryFrame,
    state_to: Sequence[complex],
    *,
    cut_locus_tol: float = 1e-12,
) -> CPNMemoryFrame:
    psi, e_q, e_p = _validated_frame(frame)
    anchor, aligned, theta, u = _aligned_geodesic(psi, state_to, cut_locus_tol=cut_locus_tol)
    if u is None or theta <= 1e-14:
        return CPNMemoryFrame(anchor.copy(), e_q.copy(), e_p.copy())

    c = math.cos(theta)
    s = math.sin(theta)
    u_end = -s * anchor + c * u

    def transport(vector: np.ndarray) -> np.ndarray:
        a = np.vdot(anchor, vector)
        b = np.vdot(u, vector)
        orthogonal = vector - a * anchor - b * u
        return a * aligned + b * u_end + orthogonal

    q1 = transport(e_q)
    p1 = transport(e_p)
    q1 = q1 / np.linalg.norm(q1)
    p1 = p1 / np.linalg.norm(p1)
    out = CPNMemoryFrame(aligned.copy(), q1, p1)
    _validated_frame(out)
    return out
