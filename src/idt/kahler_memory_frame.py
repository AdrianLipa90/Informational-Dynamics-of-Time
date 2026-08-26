from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class KahlerMemoryFrameError(ValueError):
    pass


@dataclass(frozen=True)
class CP1MemoryFrame:
    anchor_bloch: np.ndarray
    e_q: np.ndarray
    e_p: np.ndarray


def _finite_vec3(value: Sequence[float], name: str) -> np.ndarray:
    v = np.asarray(value, dtype=float)
    if v.shape != (3,):
        raise KahlerMemoryFrameError(f"{name} must be a three-component vector")
    if not np.all(np.isfinite(v)):
        raise KahlerMemoryFrameError(f"{name} must be finite")
    return v


def _unit_bloch(value: Sequence[float], name: str) -> np.ndarray:
    v = _finite_vec3(value, name)
    n = float(np.linalg.norm(v))
    if n <= 0.0:
        raise KahlerMemoryFrameError(f"{name} must have positive norm")
    out = v / n
    if not np.isclose(np.linalg.norm(out), 1.0, atol=1e-12, rtol=0.0):
        raise KahlerMemoryFrameError(f"{name} normalization failed")
    return out


def qubit_bloch(state: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(state, dtype=complex)
    if psi.shape != (2,):
        raise KahlerMemoryFrameError("qubit state must have exactly two components")
    if not np.all(np.isfinite(psi.real)) or not np.all(np.isfinite(psi.imag)):
        raise KahlerMemoryFrameError("qubit state must be finite")
    norm = float(np.vdot(psi, psi).real)
    if norm <= 0.0:
        raise KahlerMemoryFrameError("qubit state must have positive norm")
    a, b = psi / math.sqrt(norm)
    ab = np.conj(a) * b
    bloch = np.array([2.0 * ab.real, 2.0 * ab.imag, abs(a) ** 2 - abs(b) ** 2], dtype=float)
    return _unit_bloch(bloch, "bloch")


def fs_distance_cp1(bloch_a: Sequence[float], bloch_b: Sequence[float]) -> float:
    a = _unit_bloch(bloch_a, "bloch_a")
    b = _unit_bloch(bloch_b, "bloch_b")
    c = float(np.clip(np.dot(a, b), -1.0, 1.0))
    return 0.5 * math.acos(c)


def fs_log_map_cp1(bloch_from: Sequence[float], bloch_to: Sequence[float], *, antipodal_tol: float = 1e-12) -> np.ndarray:
    a = _unit_bloch(bloch_from, "bloch_from")
    b = _unit_bloch(bloch_to, "bloch_to")
    c = float(np.clip(np.dot(a, b), -1.0, 1.0))
    theta = math.acos(c)
    if theta <= 1e-14:
        return np.zeros(3, dtype=float)
    if math.pi - theta <= antipodal_tol:
        raise KahlerMemoryFrameError("CP1 geodesic is ambiguous at the antipodal point")
    tangent = b - c * a
    s = float(np.linalg.norm(tangent))
    if s <= 0.0:
        raise KahlerMemoryFrameError("CP1 logarithm tangent is singular")
    return 0.5 * (theta / s) * tangent


def initial_cp1_memory_frame(bloch_from: Sequence[float], bloch_to: Sequence[float]) -> CP1MemoryFrame:
    anchor = _unit_bloch(bloch_from, "bloch_from")
    xi = fs_log_map_cp1(anchor, bloch_to)
    n = float(np.linalg.norm(xi))
    if n <= 0.0:
        raise KahlerMemoryFrameError("initial memory frame requires a nonzero event displacement")
    e_q = xi / n
    e_p = np.cross(anchor, e_q)
    e_p /= np.linalg.norm(e_p)
    return CP1MemoryFrame(anchor.copy(), e_q, e_p)


def _minimal_rotation_matrix(bloch_from: Sequence[float], bloch_to: Sequence[float], *, antipodal_tol: float = 1e-12) -> np.ndarray:
    a = _unit_bloch(bloch_from, "bloch_from")
    b = _unit_bloch(bloch_to, "bloch_to")
    c = float(np.clip(np.dot(a, b), -1.0, 1.0))
    v = np.cross(a, b)
    s = float(np.linalg.norm(v))
    if s <= 1e-14:
        if c > 0.0:
            return np.eye(3, dtype=float)
        raise KahlerMemoryFrameError("CP1 geodesic rotation is ambiguous at the antipodal point")
    if 1.0 + c <= antipodal_tol:
        raise KahlerMemoryFrameError("CP1 geodesic rotation is ambiguous at the antipodal point")
    K = np.array([[0.0, -v[2], v[1]], [v[2], 0.0, -v[0]], [-v[1], v[0], 0.0]], dtype=float)
    return np.eye(3, dtype=float) + K + K @ K * ((1.0 - c) / (s * s))


def parallel_transport_cp1_frame(frame: CP1MemoryFrame, bloch_to: Sequence[float]) -> CP1MemoryFrame:
    anchor = _unit_bloch(frame.anchor_bloch, "frame.anchor_bloch")
    e_q = _finite_vec3(frame.e_q, "frame.e_q")
    e_p = _finite_vec3(frame.e_p, "frame.e_p")
    if abs(float(np.dot(anchor, e_q))) > 1e-10 or abs(float(np.dot(anchor, e_p))) > 1e-10:
        raise KahlerMemoryFrameError("frame axes must be tangent to the anchor Bloch vector")
    R = _minimal_rotation_matrix(anchor, bloch_to)
    target = _unit_bloch(bloch_to, "bloch_to")
    q1 = R @ e_q
    p1 = R @ e_p
    q1 /= np.linalg.norm(q1)
    p1 /= np.linalg.norm(p1)
    return CP1MemoryFrame(target, q1, p1)


def project_cp1_event(frame: CP1MemoryFrame, bloch_to: Sequence[float]) -> complex:
    anchor = _unit_bloch(frame.anchor_bloch, "frame.anchor_bloch")
    e_q = _finite_vec3(frame.e_q, "frame.e_q")
    e_p = _finite_vec3(frame.e_p, "frame.e_p")
    xi = fs_log_map_cp1(anchor, bloch_to)
    return complex(float(np.dot(xi, e_q)), float(np.dot(xi, e_p)))
