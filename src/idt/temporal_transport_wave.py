from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .bifurcation import unitary_from_hermitian
from .temporal_transport import TemporalTransportError, interrupted_temporal_propagator


def _hermitian_psd(op, *, name: str, tol: float = 1e-11) -> np.ndarray:
    arr = np.asarray(op, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise TemporalTransportError(f"{name} must be a non-empty square matrix")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise TemporalTransportError(f"{name} must be finite")
    if not np.allclose(arr, arr.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalTransportError(f"{name} must be Hermitian")
    if float(np.min(np.linalg.eigvalsh(arr))) < -tol:
        raise TemporalTransportError(f"{name} must be positive semidefinite")
    return 0.5 * (arr + arr.conj().T)


def wave_phase_space_generator(K, C) -> np.ndarray:
    """Return A for qdot=-p, pdot=Kq-Cp."""
    stiffness = _hermitian_psd(K, name="K")
    damping = _hermitian_psd(C, name="C")
    if stiffness.shape != damping.shape:
        raise TemporalTransportError("K and C must have the same dimension")
    n = stiffness.shape[0]
    z = np.zeros((n, n), dtype=complex)
    ident = np.eye(n, dtype=complex)
    return np.block([[z, -ident], [stiffness, -damping]])


def wave_energy_metric(K) -> np.ndarray:
    """Return Q=diag(K,I) for H=1/2 x^dagger Q x, x=(q,p)."""
    stiffness = _hermitian_psd(K, name="K")
    n = stiffness.shape[0]
    z = np.zeros((n, n), dtype=complex)
    ident = np.eye(n, dtype=complex)
    return np.block([[stiffness, z], [z, ident]])


def generator_energy_identity(K, C) -> tuple[np.ndarray, np.ndarray]:
    """Return A^dagger Q+QA and its exact target diag(0,-2C)."""
    stiffness = _hermitian_psd(K, name="K")
    damping = _hermitian_psd(C, name="C")
    if stiffness.shape != damping.shape:
        raise TemporalTransportError("K and C must have the same dimension")
    A = wave_phase_space_generator(stiffness, damping)
    Q = wave_energy_metric(stiffness)
    n = stiffness.shape[0]
    z = np.zeros((n, n), dtype=complex)
    target = np.block([[z, z], [z, -2.0 * damping]])
    return A.conj().T @ Q + Q @ A, target


def cayley_wave_segment(K, C, step: float) -> np.ndarray:
    """Implicit-midpoint/Cayley segment U_h=(I-hA/2)^-1(I+hA/2)."""
    h = float(step)
    if not math.isfinite(h) or h <= 0.0:
        raise TemporalTransportError("step must be finite and strictly positive")
    A = wave_phase_space_generator(K, C)
    ident = np.eye(A.shape[0], dtype=complex)
    left = ident - 0.5 * h * A
    right = ident + 0.5 * h * A
    try:
        segment = np.linalg.solve(left, right)
    except np.linalg.LinAlgError as exc:
        raise TemporalTransportError("Cayley segment solve is singular") from exc
    if not np.all(np.isfinite(segment.real)) or not np.all(np.isfinite(segment.imag)):
        raise TemporalTransportError("Cayley segment must be finite")
    return segment


def energy_metric_defect(operator, Q) -> np.ndarray:
    op = np.asarray(operator, dtype=complex)
    metric = np.asarray(Q, dtype=complex)
    if op.ndim != 2 or op.shape[0] != op.shape[1]:
        raise TemporalTransportError("operator must be square")
    if metric.shape != op.shape or not np.allclose(metric, metric.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalTransportError("Q must be Hermitian and match operator dimension")
    defect = op.conj().T @ metric @ op - metric
    return 0.5 * (defect + defect.conj().T)


def maximum_energy_growth_eigenvalue(operator, Q) -> float:
    defect = energy_metric_defect(operator, Q)
    return float(np.max(np.linalg.eigvalsh(defect)))


def q_compatible_unitary_bifurcation(
    phase_increment_rad: float,
    generator: Sequence[Sequence[complex]],
    Q,
    *,
    commutator_tol: float = 1e-11,
) -> np.ndarray:
    """Return exp(-i beta G) after the sufficient Q-compatibility gate [G,Q]=0."""
    g = np.asarray(generator, dtype=complex)
    metric = np.asarray(Q, dtype=complex)
    if g.ndim != 2 or g.shape[0] != g.shape[1] or g.shape[0] == 0:
        raise TemporalTransportError("generator must be a non-empty square matrix")
    if metric.shape != g.shape:
        raise TemporalTransportError("Q must match generator dimension")
    if not np.all(np.isfinite(g.real)) or not np.all(np.isfinite(g.imag)):
        raise TemporalTransportError("generator must be finite")
    if not np.allclose(g, g.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalTransportError("generator must be Hermitian")
    if not np.allclose(metric, metric.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalTransportError("Q must be Hermitian")
    commutator = g @ metric - metric @ g
    if float(np.max(np.abs(commutator))) > float(commutator_tol):
        raise TemporalTransportError("generator failed the declared Q-compatibility gate")
    return unitary_from_hermitian(float(phase_increment_rad), g)


def wave_interrupted_transport(
    smooth_segments: Sequence[np.ndarray],
    event_operators: Sequence[np.ndarray],
) -> np.ndarray:
    return interrupted_temporal_propagator(smooth_segments, event_operators)
