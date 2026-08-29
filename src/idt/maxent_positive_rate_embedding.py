from __future__ import annotations

import math


class MaxEntRateEmbeddingError(ValueError):
    pass


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise MaxEntRateEmbeddingError(f"{name} must be positive finite")
    return value


def exponential_density(rate: float, t: float) -> float:
    r = _positive("rate", rate)
    t = float(t)
    if not math.isfinite(t) or t < 0.0:
        raise MaxEntRateEmbeddingError("t must be nonnegative finite")
    return r * math.exp(-r * t)


def reciprocal_mean(rate: float) -> float:
    return 1.0 / _positive("rate", rate)


def maxent_entropy_nats(rate: float) -> float:
    r = _positive("rate", rate)
    return 1.0 - math.log(r)


def uniform_same_mean_entropy_nats(rate: float) -> float:
    """Entropy of Uniform[0,2/r], which has the same mean 1/r."""
    r = _positive("rate", rate)
    return math.log(2.0 / r)


def uniform_to_maxent_kl_nats(rate: float) -> float:
    """Exact KL of Uniform[0,2/r] relative to Exp(r)."""
    _positive("rate", rate)
    return 1.0 - math.log(2.0)


def rate_information_nats(rate_a: float, rate_b: float) -> float:
    """D_KL(Exp(rate_a) || Exp(rate_b))."""
    a = _positive("rate_a", rate_a)
    b = _positive("rate_b", rate_b)
    return math.log(a / b) + b / a - 1.0


def phi_ratio(x: float) -> float:
    x = _positive("ratio", x)
    return x - 1.0 - math.log(x)


def phase_rate_information_nats(rate_directional: float, rate_reference: float) -> float:
    """Directional phase-rate information with x=rate_reference/rate_directional."""
    return rate_information_nats(rate_directional, rate_reference)


def activity_clock_information_nats(activity_reference: float, activity_local: float) -> float:
    """05D orientation: D_KL(Exp(a_ref)||Exp(a_local))=Phi(a_local/a_ref)."""
    return rate_information_nats(activity_reference, activity_local)


def common_scale_information_nats(rate_a: float, rate_b: float, scale: float) -> tuple[float, float]:
    c = _positive("scale", scale)
    base = rate_information_nats(rate_a, rate_b)
    scaled = rate_information_nats(c * rate_a, c * rate_b)
    return base, scaled


def fisher_metric_rate(rate: float) -> float:
    r = _positive("rate", rate)
    return 1.0 / (r * r)


def fisher_metric_log_rate() -> float:
    return 1.0


def xi_rate(rate_a: float, rate_b: float, relational_area: float) -> float:
    area = _positive("relational_area", relational_area)
    return rate_information_nats(rate_a, rate_b) / area
