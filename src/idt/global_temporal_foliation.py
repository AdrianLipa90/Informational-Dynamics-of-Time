"""Reference algebra for the IDT 05G temporal-foliation gate.

The target coframe is

    Theta = N * c * dt

with positive lapse N.  For an exact clock differential dt,

    dTheta = c dN ^ dt

and therefore Theta ^ dTheta vanishes identically.  The routines below
make that exterior-algebra statement executable without assuming a
particular metric or coordinate chart.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import isfinite, sqrt
from typing import Iterable, Sequence


class TemporalFoliationError(ValueError):
    """Raised when the declared 05G foliation inputs leave their domain."""


def _finite_vector(values: Iterable[float], name: str) -> tuple[float, ...]:
    out = tuple(float(value) for value in values)
    if not out:
        raise TemporalFoliationError(f"{name} must be non-empty")
    if not all(isfinite(value) for value in out):
        raise TemporalFoliationError(f"{name} must be finite")
    return out


def _validate_lapse(lapse: float) -> float:
    value = float(lapse)
    if not isfinite(value) or value <= 0.0:
        raise TemporalFoliationError("relational lapse must be finite and positive")
    return value


def _validate_light_speed(c: float) -> float:
    value = float(c)
    if not isfinite(value) or value <= 0.0:
        raise TemporalFoliationError("coframe conversion scale c must be finite and positive")
    return value


def covector_norm(covector: Sequence[float]) -> float:
    """Euclidean coefficient norm used only to detect a zero covector."""

    vec = _finite_vector(covector, "covector")
    return sqrt(sum(value * value for value in vec))


def temporal_coframe(lapse: float, dt_covector: Sequence[float], c: float = 1.0) -> tuple[float, ...]:
    """Return the coordinate coefficients of Theta = N c dt.

    No spacetime metric is used.  The operation is only positive scalar
    multiplication of the calibrated clock one-form.
    """

    n = _validate_lapse(lapse)
    scale = _validate_light_speed(c)
    dt = _finite_vector(dt_covector, "dt_covector")
    if covector_norm(dt) == 0.0:
        raise TemporalFoliationError("dt_covector must be nonzero on a regular clock patch")
    return tuple(n * scale * value for value in dt)


def d_temporal_coframe(
    lapse_gradient: Sequence[float],
    dt_covector: Sequence[float],
    c: float = 1.0,
) -> tuple[tuple[float, ...], ...]:
    """Return the antisymmetric 2-form coefficients of dTheta = c dN ^ dt."""

    grad_n = _finite_vector(lapse_gradient, "lapse_gradient")
    dt = _finite_vector(dt_covector, "dt_covector")
    scale = _validate_light_speed(c)
    if len(grad_n) != len(dt):
        raise TemporalFoliationError("lapse_gradient and dt_covector dimensions must match")
    if covector_norm(dt) == 0.0:
        raise TemporalFoliationError("dt_covector must be nonzero on a regular clock patch")

    dim = len(dt)
    return tuple(
        tuple(scale * (grad_n[i] * dt[j] - grad_n[j] * dt[i]) for j in range(dim))
        for i in range(dim)
    )


def frobenius_three_form(
    lapse: float,
    lapse_gradient: Sequence[float],
    dt_covector: Sequence[float],
    c: float = 1.0,
) -> dict[tuple[int, int, int], float]:
    """Compute independent components of Theta ^ dTheta.

    For a one-form a and two-form B,

        (a ^ B)_{ijk} = a_i B_jk + a_j B_ki + a_k B_ij.

    For Theta=N c dt and dTheta=c dN^dt these components cancel
    algebraically.  Returning the components makes the cancellation
    directly testable for arbitrary lapse gradients.
    """

    theta = temporal_coframe(lapse, dt_covector, c=c)
    dtheta = d_temporal_coframe(lapse_gradient, dt_covector, c=c)
    if len(theta) < 3:
        raise TemporalFoliationError("Frobenius three-form requires dimension at least three")

    return {
        (i, j, k): theta[i] * dtheta[j][k]
        + theta[j] * dtheta[k][i]
        + theta[k] * dtheta[i][j]
        for i, j, k in combinations(range(len(theta)), 3)
    }


def frobenius_residual(
    lapse: float,
    lapse_gradient: Sequence[float],
    dt_covector: Sequence[float],
    c: float = 1.0,
) -> float:
    """Maximum absolute component of Theta ^ dTheta."""

    components = frobenius_three_form(lapse, lapse_gradient, dt_covector, c=c)
    return max(abs(value) for value in components.values())


@dataclass(frozen=True)
class TemporalFoliationCertificate:
    """Fail-closed status ledger for an admitted clock domain."""

    positive_lapse: bool
    regular_clock: bool
    local_frobenius: bool
    kernel_preserved: bool
    global_clock_scalar_supplied: bool
    global_regular_foliation: bool
    cauchy_global_hyperbolicity: str = "OPEN"


def certify_clock_domain(
    lapse_samples: Sequence[float],
    dt_norm_samples: Sequence[float],
    *,
    global_clock_scalar_supplied: bool = False,
) -> TemporalFoliationCertificate:
    """Build the 05G promotion ledger from sampled domain guards.

    Sampling cannot prove smoothness or globality; those are explicit
    declared inputs.  The function only fails closed on positivity and
    regularity violations and records whether the global scalar-clock
    premise has been supplied by an upstream theorem/certificate.
    """

    lapses = _finite_vector(lapse_samples, "lapse_samples")
    norms = _finite_vector(dt_norm_samples, "dt_norm_samples")
    if len(lapses) != len(norms):
        raise TemporalFoliationError("lapse and dt-norm sample counts must match")
    if any(value <= 0.0 for value in lapses):
        raise TemporalFoliationError("all relational lapse samples must be positive")
    if any(value <= 0.0 for value in norms):
        raise TemporalFoliationError("all clock-differential norms must be positive")

    global_input = bool(global_clock_scalar_supplied)
    return TemporalFoliationCertificate(
        positive_lapse=True,
        regular_clock=True,
        local_frobenius=True,
        kernel_preserved=True,
        global_clock_scalar_supplied=global_input,
        global_regular_foliation=global_input,
    )
