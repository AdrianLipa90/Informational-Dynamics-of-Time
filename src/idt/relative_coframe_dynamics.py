from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


class RelativeCoframeDynamicsError(ValueError):
    pass


PAIR_BASIS = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))


def _matrix4(value: Sequence[Sequence[float]], name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (4, 4) or not np.all(np.isfinite(arr)):
        raise RelativeCoframeDynamicsError(f"{name} must be a finite 4x4 matrix")
    return arr


def _invertible(matrix: np.ndarray, name: str) -> np.ndarray:
    det = float(np.linalg.det(matrix))
    if not np.isfinite(det) or abs(det) <= 1e-14:
        raise RelativeCoframeDynamicsError(f"{name} must be invertible")
    return np.linalg.inv(matrix)


def exterior_square4(matrix4: Sequence[Sequence[float]]) -> np.ndarray:
    e = _matrix4(matrix4, "matrix4")
    out = np.zeros((6, 6), dtype=float)
    for row, (i, j) in enumerate(PAIR_BASIS):
        for col, (mu, nu) in enumerate(PAIR_BASIS):
            out[row, col] = (
                e[i, mu] * e[j, nu]
                - e[i, nu] * e[j, mu]
            )
    return out


def lie_exterior_square(generator4: Sequence[Sequence[float]]) -> np.ndarray:
    h = _matrix4(generator4, "generator4")
    out = np.zeros((6, 6), dtype=float)
    for col, (i, j) in enumerate(PAIR_BASIS):
        for row, (k, ell) in enumerate(PAIR_BASIS):
            out[row, col] = (
                h[k, i] * (1.0 if ell == j else 0.0)
                - h[ell, i] * (1.0 if k == j else 0.0)
                + (1.0 if k == i else 0.0) * h[ell, j]
                - (1.0 if ell == i else 0.0) * h[k, j]
            )
    return out


def frame_generator(
    frame4: Sequence[Sequence[float]],
    frame_velocity4: Sequence[Sequence[float]],
) -> np.ndarray:
    e = _matrix4(frame4, "frame4")
    v = _matrix4(frame_velocity4, "frame_velocity4")
    return v @ _invertible(e, "frame4")


def relative_coframe(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
) -> np.ndarray:
    a = _matrix4(source_frame4, "source_frame4")
    b = _matrix4(target_frame4, "target_frame4")
    return b @ _invertible(a, "source_frame4")


def relative_coframe_velocity(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
    source_velocity4: Sequence[Sequence[float]],
    target_velocity4: Sequence[Sequence[float]],
) -> np.ndarray:
    a = _matrix4(source_frame4, "source_frame4")
    b = _matrix4(target_frame4, "target_frame4")
    va = _matrix4(source_velocity4, "source_velocity4")
    vb = _matrix4(target_velocity4, "target_velocity4")
    inv_a = _invertible(a, "source_frame4")
    relative = b @ inv_a
    return vb @ inv_a - relative @ va @ inv_a


def relative_coframe_velocity_generator_form(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
    source_velocity4: Sequence[Sequence[float]],
    target_velocity4: Sequence[Sequence[float]],
) -> np.ndarray:
    relative = relative_coframe(source_frame4, target_frame4)
    la = frame_generator(source_frame4, source_velocity4)
    lb = frame_generator(target_frame4, target_velocity4)
    return lb @ relative - relative @ la


def relative_bivector(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
) -> np.ndarray:
    return exterior_square4(relative_coframe(source_frame4, target_frame4))


def relative_bivector_velocity(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
    source_velocity4: Sequence[Sequence[float]],
    target_velocity4: Sequence[Sequence[float]],
) -> np.ndarray:
    relative = relative_coframe(source_frame4, target_frame4)
    relative_velocity = relative_coframe_velocity(
        source_frame4,
        target_frame4,
        source_velocity4,
        target_velocity4,
    )

    out = np.zeros((6, 6), dtype=float)
    for row, (i, j) in enumerate(PAIR_BASIS):
        for col, (mu, nu) in enumerate(PAIR_BASIS):
            out[row, col] = (
                relative_velocity[i, mu] * relative[j, nu]
                + relative[i, mu] * relative_velocity[j, nu]
                - relative_velocity[i, nu] * relative[j, mu]
                - relative[i, nu] * relative_velocity[j, mu]
            )
    return out


def relative_bivector_velocity_generator_form(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
    source_velocity4: Sequence[Sequence[float]],
    target_velocity4: Sequence[Sequence[float]],
) -> np.ndarray:
    b = relative_bivector(source_frame4, target_frame4)
    la = lie_exterior_square(frame_generator(source_frame4, source_velocity4))
    lb = lie_exterior_square(frame_generator(target_frame4, target_velocity4))
    return lb @ b - b @ la


@dataclass(frozen=True)
class RelativeCoframeDynamicsAudit:
    coframe_residual: float
    bivector_residual: float
    source_generator_norm: float
    target_generator_norm: float


def audit_relative_dynamics(
    source_frame4: Sequence[Sequence[float]],
    target_frame4: Sequence[Sequence[float]],
    source_velocity4: Sequence[Sequence[float]],
    target_velocity4: Sequence[Sequence[float]],
) -> RelativeCoframeDynamicsAudit:
    de_direct = relative_coframe_velocity(
        source_frame4,
        target_frame4,
        source_velocity4,
        target_velocity4,
    )
    de_generator = relative_coframe_velocity_generator_form(
        source_frame4,
        target_frame4,
        source_velocity4,
        target_velocity4,
    )
    db_direct = relative_bivector_velocity(
        source_frame4,
        target_frame4,
        source_velocity4,
        target_velocity4,
    )
    db_generator = relative_bivector_velocity_generator_form(
        source_frame4,
        target_frame4,
        source_velocity4,
        target_velocity4,
    )
    la = frame_generator(source_frame4, source_velocity4)
    lb = frame_generator(target_frame4, target_velocity4)
    return RelativeCoframeDynamicsAudit(
        coframe_residual=float(np.linalg.norm(de_direct - de_generator, ord=np.inf)),
        bivector_residual=float(np.linalg.norm(db_direct - db_generator, ord=np.inf)),
        source_generator_norm=float(np.linalg.norm(la)),
        target_generator_norm=float(np.linalg.norm(lb)),
    )
