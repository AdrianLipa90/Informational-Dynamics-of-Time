"""Typed QHTRI/neutrino -> transverse-traceless source gate.

This module implements only the algebraic TT projection and source-admissibility
layer. The physical normalization binding from a neutrino Hilbert-space source to
an Einstein stress-energy tensor is kept as an explicit downstream gate.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence


Matrix3 = tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]
Vector3 = tuple[float, float, float]


def _as_vector3(v: Sequence[float]) -> Vector3:
    if len(v) != 3:
        raise ValueError("expected a 3-vector")
    out = tuple(float(x) for x in v)
    if not all(math.isfinite(x) for x in out):
        raise ValueError("vector entries must be finite")
    return out  # type: ignore[return-value]


def _as_matrix3(m: Sequence[Sequence[float]]) -> Matrix3:
    if len(m) != 3 or any(len(row) != 3 for row in m):
        raise ValueError("expected a 3x3 matrix")
    out = tuple(tuple(float(x) for x in row) for row in m)
    if not all(math.isfinite(x) for row in out for x in row):
        raise ValueError("matrix entries must be finite")
    return out  # type: ignore[return-value]


def normalize_direction(direction: Sequence[float]) -> Vector3:
    n = _as_vector3(direction)
    norm = math.sqrt(sum(x * x for x in n))
    if norm == 0.0:
        raise ValueError("propagation direction must be non-zero")
    return tuple(x / norm for x in n)  # type: ignore[return-value]


def transverse_projector(direction: Sequence[float]) -> Matrix3:
    n = normalize_direction(direction)
    return tuple(
        tuple((1.0 if i == j else 0.0) - n[i] * n[j] for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def project_tt(stress: Sequence[Sequence[float]], direction: Sequence[float]) -> Matrix3:
    """Return the spatial transverse-traceless projection of a symmetric source.

    Implements
        T^TT_ij = (P_i^k P_j^l - 1/2 P_ij P^kl) T_kl
    with P_ij = delta_ij - n_i n_j.
    """

    t = _as_matrix3(stress)
    p = transverse_projector(direction)

    # Symmetrise input explicitly so the gate has one unambiguous tensor type.
    s = tuple(
        tuple(0.5 * (t[i][j] + t[j][i]) for j in range(3))
        for i in range(3)
    )

    ptspt = tuple(
        tuple(
            sum(p[i][k] * s[k][l] * p[j][l] for k in range(3) for l in range(3))
            for j in range(3)
        )
        for i in range(3)
    )
    transverse_trace = sum(p[k][l] * s[k][l] for k in range(3) for l in range(3))
    return tuple(
        tuple(ptspt[i][j] - 0.5 * p[i][j] * transverse_trace for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def frobenius_norm(m: Sequence[Sequence[float]]) -> float:
    a = _as_matrix3(m)
    return math.sqrt(sum(x * x for row in a for x in row))


def trace3(m: Sequence[Sequence[float]]) -> float:
    a = _as_matrix3(m)
    return a[0][0] + a[1][1] + a[2][2]


def transverse_residual(m: Sequence[Sequence[float]], direction: Sequence[float]) -> Vector3:
    a = _as_matrix3(m)
    n = normalize_direction(direction)
    return tuple(sum(a[i][j] * n[j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def polarization_components_z(tt: Sequence[Sequence[float]]) -> tuple[float, float]:
    """Return (+, x) amplitudes for propagation along the z axis."""

    a = _as_matrix3(tt)
    plus = 0.5 * (a[0][0] - a[1][1])
    cross = 0.5 * (a[0][1] + a[1][0])
    return plus, cross


def phase_encoded_quadrupole(phase: float, amplitude: float = 1.0) -> Matrix3:
    """Minimal spin-2 quadrupole carrying a phase through 2*phase."""

    if not math.isfinite(phase) or not math.isfinite(amplitude):
        raise ValueError("phase and amplitude must be finite")
    c = amplitude * math.cos(2.0 * phase)
    s = amplitude * math.sin(2.0 * phase)
    return ((c, s, 0.0), (s, -c, 0.0), (0.0, 0.0, 0.0))


@dataclass(frozen=True)
class TTGateResult:
    tt: Matrix3
    norm: float
    trace_residual: float
    transverse_residual: Vector3
    admitted: bool


def tt_source_gate(
    stress: Sequence[Sequence[float]],
    direction: Sequence[float],
    *,
    atol: float = 1e-12,
) -> TTGateResult:
    if atol < 0.0 or not math.isfinite(atol):
        raise ValueError("atol must be finite and non-negative")
    tt = project_tt(stress, direction)
    norm = frobenius_norm(tt)
    tr = trace3(tt)
    trans = transverse_residual(tt, direction)
    clean = abs(tr) <= atol and max(abs(x) for x in trans) <= atol
    return TTGateResult(tt=tt, norm=norm, trace_residual=tr, transverse_residual=trans, admitted=clean and norm > atol)
