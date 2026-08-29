from __future__ import annotations

import math


class LocalClockRelativeEntropyError(ValueError):
    pass


def _positive_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise LocalClockRelativeEntropyError(f"{name} must be positive finite")
    return value


def phi_ratio(x: float) -> float:
    """Natural-log relative-information generator Phi(x)=x-1-ln(x)."""
    x = _positive_finite("x", x)
    return x - 1.0 - math.log(x)


def exponential_rate_kl(rate_p: float, rate_q: float) -> float:
    """KL(Exp(rate_p) || Exp(rate_q)) for rate-parameterized exponentials."""
    rate_p = _positive_finite("rate_p", rate_p)
    rate_q = _positive_finite("rate_q", rate_q)
    return math.log(rate_p / rate_q) - 1.0 + rate_q / rate_p


def clock_relative_entropy(activity_x: float, activity_r: float) -> dict[str, float]:
    """Return the IDT clock-ratio KL pair for positive local activities."""
    activity_x = _positive_finite("activity_x", activity_x)
    activity_r = _positive_finite("activity_r", activity_r)
    lapse = activity_x / activity_r
    ref_to_local = exponential_rate_kl(activity_r, activity_x)
    local_to_ref = exponential_rate_kl(activity_x, activity_r)
    return {
        "N_R": lapse,
        "ref_to_local": ref_to_local,
        "local_to_ref": local_to_ref,
        "jeffreys": ref_to_local + local_to_ref,
        "fisher_metric": 1.0 / (lapse * lapse),
    }


def common_scale_invariant(activity_x: float, activity_r: float, scale: float) -> bool:
    scale = _positive_finite("scale", scale)
    base = clock_relative_entropy(activity_x, activity_r)
    moved = clock_relative_entropy(scale * activity_x, scale * activity_r)
    return all(
        math.isclose(base[key], moved[key], rel_tol=1.0e-13, abs_tol=1.0e-15)
        for key in ("N_R", "ref_to_local", "local_to_ref", "jeffreys", "fisher_metric")
    )
