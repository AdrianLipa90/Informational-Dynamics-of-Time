from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np


class InternalElapsedError(ValueError):
    pass


def _positive_finite(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise InternalElapsedError(f"{name} must be finite and strictly positive")
    return x


def elapsed_increment(activity: float, delta_lambda: float, *, reference_activity: float = 1.0) -> float:
    a = _positive_finite(activity, "activity")
    dl = _positive_finite(delta_lambda, "delta_lambda")
    ref = _positive_finite(reference_activity, "reference_activity")
    return float((a / ref) * dl)


def cumulative_elapsed_activity(
    activities: Sequence[float],
    delta_lambdas: Sequence[float],
    *,
    reference_activity: float = 1.0,
) -> np.ndarray:
    if len(activities) != len(delta_lambdas):
        raise InternalElapsedError("activities and delta_lambdas must have the same length")
    ref = _positive_finite(reference_activity, "reference_activity")
    increments = [elapsed_increment(a, dl, reference_activity=ref) for a, dl in zip(activities, delta_lambdas)]
    return np.concatenate(([0.0], np.cumsum(np.asarray(increments, dtype=float))))


def reparameterize_activity(activity: float, d_lambda_prime_d_lambda: float) -> float:
    """Transform activity as a one-density so a' dλ' = a dλ."""
    a = _positive_finite(activity, "activity")
    jac = _positive_finite(d_lambda_prime_d_lambda, "d_lambda_prime_d_lambda")
    return float(a / jac)
