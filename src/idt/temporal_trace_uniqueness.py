"""Uniqueness of the rotationally invariant extensive temporal scalar on Herm(2).

Candidate-only executable support for IDT_TEMPORAL_TRACE_UNIQUENESS_V0_6.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

Coords4: TypeAlias = tuple[float, float, float, float]
Rotation3: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


class TemporalTraceUniquenessError(ValueError):
    """Fail-closed error for invalid candidate carrier data."""


ROT_X_PI: Rotation3 = ((1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0))
ROT_Y_PI: Rotation3 = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0))
ROT_Z_PI: Rotation3 = ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0))


def _validate_coords(x: Coords4) -> None:
    if len(x) != 4 or not all(isfinite(v) for v in x):
        raise TemporalTraceUniquenessError("expected four finite Hermitian coordinates")


def add(a: Coords4, b: Coords4) -> Coords4:
    _validate_coords(a)
    _validate_coords(b)
    return tuple(x + y for x, y in zip(a, b, strict=True))  # type: ignore[return-value]


def rotate_spatial(x: Coords4, r: Rotation3) -> Coords4:
    _validate_coords(x)
    v = x[1:]
    out = tuple(sum(r[i][j] * v[j] for j in range(3)) for i in range(3))
    return (x[0], *out)


def linear_functional(coefficients: Coords4, x: Coords4) -> float:
    _validate_coords(coefficients)
    _validate_coords(x)
    return sum(a * b for a, b in zip(coefficients, x, strict=True))


def trace_temporal_scalar(x: Coords4, calibration: float = 1.0) -> float:
    """For X=x0 I+x.sigma, Tr(X)=2 x0."""
    _validate_coords(x)
    if not isfinite(calibration) or calibration <= 0:
        raise TemporalTraceUniquenessError("calibration must be finite and positive")
    return 2.0 * calibration * x[0]


def positive_cone_admitted(x: Coords4, tol: float = 1e-15) -> bool:
    """PSD Herm(2) condition x0 >= |x| with future/nonnegative scalar orientation."""
    _validate_coords(x)
    spatial2 = sum(v * v for v in x[1:])
    return x[0] >= -tol and x[0] * x[0] + tol >= spatial2


def invariance_constraints(coefficients: Coords4) -> tuple[float, ...]:
    """Defects under three pi rotations that force all vector coefficients to zero."""
    _validate_coords(coefficients)
    probes: tuple[Coords4, ...] = (
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )
    rotations = (ROT_X_PI, ROT_Y_PI, ROT_Z_PI)
    defects: list[float] = []
    for r in rotations:
        for probe in probes:
            defects.append(
                linear_functional(coefficients, rotate_spatial(probe, r))
                - linear_functional(coefficients, probe)
            )
    return tuple(defects)


@dataclass(frozen=True)
class TraceUniquenessCertificate:
    vector_coefficients_zero: bool
    trace_additive: bool
    trace_rotation_invariant: bool
    trace_positive_on_positive_examples: bool


def certificate() -> TraceUniquenessCertificate:
    candidate_vector_coeffs = (
        invariance_constraints((0.0, 1.0, 0.0, 0.0)),
        invariance_constraints((0.0, 0.0, 1.0, 0.0)),
        invariance_constraints((0.0, 0.0, 0.0, 1.0)),
    )
    vector_zero = all(any(abs(d) > 0.0 for d in defects) for defects in candidate_vector_coeffs)

    a = (2.0, 0.25, -0.5, 0.75)
    b = (3.0, -0.25, 0.5, -0.75)
    additive = trace_temporal_scalar(add(a, b)) == trace_temporal_scalar(a) + trace_temporal_scalar(b)

    rotated = rotate_spatial(a, ROT_Y_PI)
    invariant = trace_temporal_scalar(rotated) == trace_temporal_scalar(a)

    positive_examples = (
        (1.0, 0.0, 0.0, 0.0),
        (2.0, 1.0, 0.0, 0.0),
        (3.0, 1.0, 2.0, 1.0),
    )
    positive = all(
        positive_cone_admitted(x) and trace_temporal_scalar(x) >= 0.0
        for x in positive_examples
    )
    return TraceUniquenessCertificate(
        vector_coefficients_zero=vector_zero,
        trace_additive=additive,
        trace_rotation_invariant=invariant,
        trace_positive_on_positive_examples=positive,
    )
