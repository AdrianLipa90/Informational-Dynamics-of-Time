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


def bifurcation_parameter_from_activity_current(
    activity: float,
    current: float,
    *,
    kappa_value: float | None = None,
) -> BifurcationParameter:
    """Recover the directed phase parameter from positive activity/current data.

    For finite positive forward/reverse rates:
        r = j/a in (-1, 1)
        A = 2 atanh(r)
        sigma = A / ln(2)
        beta = kappa * sigma

    With the canonical kappa = ln(2)/(24*pi), beta = atanh(r)/(12*pi).
    """
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


def _hermitian_involution(generator: Sequence[Sequence[complex]], *, tol: float = 1e-12) -> np.ndarray:
    g = np.asarray(generator, dtype=complex)
    if g.ndim != 2 or g.shape[0] != g.shape[1] or g.shape[0] == 0:
        raise BifurcationError("generator must be a non-empty square matrix")
    if not np.all(np.isfinite(g.real)) or not np.all(np.isfinite(g.imag)):
        raise BifurcationError("generator must be finite")
    if not np.allclose(g, g.conj().T, atol=tol, rtol=0.0):
        raise BifurcationError("reference generator must be Hermitian")
    ident = np.eye(g.shape[0], dtype=complex)
    if not np.allclose(g @ g, ident, atol=tol, rtol=0.0):
        raise BifurcationError("reference generator must satisfy G^2 = I")
    return g


def unitary_bifurcation_operator(
    phase_increment_rad: float,
    generator: Sequence[Sequence[complex]],
) -> np.ndarray:
    """Reference unitary subclass B(beta)=exp(-i beta G), for Hermitian G^2=I."""
    beta = float(phase_increment_rad)
    if not math.isfinite(beta):
        raise BifurcationError("phase increment must be finite")
    g = _hermitian_involution(generator)
    ident = np.eye(g.shape[0], dtype=complex)
    return math.cos(beta) * ident - 1j * math.sin(beta) * g


def bifurcation_from_activity_current(
    activity: float,
    current: float,
    generator: Sequence[Sequence[complex]],
    *,
    kappa_value: float | None = None,
) -> tuple[BifurcationParameter, np.ndarray]:
    parameter = bifurcation_parameter_from_activity_current(
        activity, current, kappa_value=kappa_value
    )
    return parameter, unitary_bifurcation_operator(parameter.phase_increment_rad, generator)


def apply_bifurcation(operator: np.ndarray, state: Sequence[complex]) -> np.ndarray:
    op = np.asarray(operator, dtype=complex)
    psi = np.asarray(state, dtype=complex)
    if op.ndim != 2 or op.shape[0] != op.shape[1]:
        raise BifurcationError("operator must be square")
    if psi.ndim != 1 or psi.shape[0] != op.shape[1]:
        raise BifurcationError("state dimension must match operator")
    return op @ psi
