from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kahler_time import kappa


class BifurcationError(ValueError):
    pass


@dataclass(frozen=True)
class BifurcationParameter:
    activity: float
    current: float
    current_fraction: float
    edge_drive: float
    affinity_bits: float
    phase_increment_rad: float


@dataclass(frozen=True)
class PolarBifurcation:
    event_strength: float
    phase_increment_rad: float
    contraction: np.ndarray
    unitary: np.ndarray
    operator: np.ndarray


def bifurcation_parameter_from_activity_current(activity: float, current: float, *, kappa_value: float | None = None) -> BifurcationParameter:
    a = float(activity)
    j = float(current)
    kap = kappa() if kappa_value is None else float(kappa_value)
    if not (math.isfinite(a) and a > 0.0):
        raise BifurcationError("activity must be finite and strictly positive")
    if not (math.isfinite(j) and math.isfinite(kap)):
        raise BifurcationError("current and kappa must be finite")
    r = j / a
    if not (-1.0 < r < 1.0):
        raise BifurcationError("finite positive rate pairs require |current/activity| < 1")
    drive = 2.0 * math.atanh(r)
    sigma = drive / math.log(2.0)
    beta = kap * sigma
    return BifurcationParameter(a, j, r, drive, sigma, beta)


def _square_finite_matrix(matrix: Sequence[Sequence[complex]], name: str) -> np.ndarray:
    m = np.asarray(matrix, dtype=complex)
    if m.ndim != 2 or m.shape[0] != m.shape[1] or m.shape[0] == 0:
        raise BifurcationError(f"{name} must be a non-empty square matrix")
    if not np.all(np.isfinite(m.real)) or not np.all(np.isfinite(m.imag)):
        raise BifurcationError(f"{name} must be finite")
    return m


def _hermitian_matrix(matrix: Sequence[Sequence[complex]], name: str, *, tol: float = 1e-12) -> np.ndarray:
    m = _square_finite_matrix(matrix, name)
    if not np.allclose(m, m.conj().T, atol=tol, rtol=0.0):
        raise BifurcationError(f"{name} must be Hermitian")
    return m


def _hermitian_involution(generator: Sequence[Sequence[complex]], *, tol: float = 1e-12) -> np.ndarray:
    g = _hermitian_matrix(generator, "reference generator", tol=tol)
    ident = np.eye(g.shape[0], dtype=complex)
    if not np.allclose(g @ g, ident, atol=tol, rtol=0.0):
        raise BifurcationError("reference generator must satisfy G^2 = I")
    return g


def unitary_bifurcation_operator(phase_increment_rad: float, generator: Sequence[Sequence[complex]]) -> np.ndarray:
    beta = float(phase_increment_rad)
    if not math.isfinite(beta):
        raise BifurcationError("phase increment must be finite")
    g = _hermitian_involution(generator)
    ident = np.eye(g.shape[0], dtype=complex)
    return math.cos(beta) * ident - 1j * math.sin(beta) * g


def unitary_from_hermitian(phase_increment_rad: float, generator: Sequence[Sequence[complex]]) -> np.ndarray:
    beta = float(phase_increment_rad)
    if not math.isfinite(beta):
        raise BifurcationError("phase increment must be finite")
    g = _hermitian_matrix(generator, "unitary generator")
    evals, evecs = np.linalg.eigh(g)
    phases = np.exp(-1j * beta * evals)
    return (evecs * phases) @ evecs.conj().T


def contractive_event_operator(event_strength: float, dissipator: Sequence[Sequence[complex]], *, tol: float = 1e-12) -> np.ndarray:
    q = float(event_strength)
    if not (math.isfinite(q) and q >= 0.0):
        raise BifurcationError("event strength must be finite and non-negative")
    d = _hermitian_matrix(dissipator, "dissipator", tol=tol)
    evals, evecs = np.linalg.eigh(d)
    if float(evals.min()) < -tol:
        raise BifurcationError("dissipator must be positive semidefinite")
    evals = np.maximum(evals, 0.0)
    weights = np.exp(-q * evals)
    return (evecs * weights) @ evecs.conj().T


def polar_bifurcation_operator(event_strength: float, phase_increment_rad: float, dissipator: Sequence[Sequence[complex]], generator: Sequence[Sequence[complex]]) -> PolarBifurcation:
    c = contractive_event_operator(event_strength, dissipator)
    u = unitary_from_hermitian(phase_increment_rad, generator)
    if c.shape != u.shape:
        raise BifurcationError("dissipator and unitary generator dimensions must match")
    return PolarBifurcation(float(event_strength), float(phase_increment_rad), c, u, c @ u)


def polar_bifurcation_from_event(event_strength: float, activity: float, current: float, dissipator: Sequence[Sequence[complex]], generator: Sequence[Sequence[complex]], *, kappa_value: float | None = None) -> tuple[BifurcationParameter, PolarBifurcation]:
    parameter = bifurcation_parameter_from_activity_current(activity, current, kappa_value=kappa_value)
    bif = polar_bifurcation_operator(event_strength, parameter.phase_increment_rad, dissipator, generator)
    return parameter, bif


def bifurcation_from_activity_current(activity: float, current: float, generator: Sequence[Sequence[complex]], *, kappa_value: float | None = None) -> tuple[BifurcationParameter, np.ndarray]:
    parameter = bifurcation_parameter_from_activity_current(activity, current, kappa_value=kappa_value)
    return parameter, unitary_bifurcation_operator(parameter.phase_increment_rad, generator)


def apply_bifurcation(operator: np.ndarray, state: Sequence[complex]) -> np.ndarray:
    op = np.asarray(operator, dtype=complex)
    psi = np.asarray(state, dtype=complex)
    if op.ndim != 2 or op.shape[0] != op.shape[1]:
        raise BifurcationError("operator must be square")
    if psi.ndim != 1 or psi.shape[0] != op.shape[1]:
        raise BifurcationError("state dimension must match operator")
    return op @ psi
