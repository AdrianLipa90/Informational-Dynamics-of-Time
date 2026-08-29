from __future__ import annotations

import math
from typing import Sequence


class ClockKLRefinementError(ValueError):
    pass


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ClockKLRefinementError(f"{name} must be positive finite")
    return value


def _validate_probability_vector(name: str, values: Sequence[float]) -> tuple[float, ...]:
    vals = tuple(float(v) for v in values)
    if not vals:
        raise ClockKLRefinementError(f"{name} must be nonempty")
    if not all(math.isfinite(v) and v > 0.0 for v in vals):
        raise ClockKLRefinementError(f"{name} must be strictly positive finite")
    if not math.isclose(sum(vals), 1.0, rel_tol=0.0, abs_tol=2.0e-12):
        raise ClockKLRefinementError(f"{name} must sum to one")
    return vals


def exponential_histogram(rate: float, bin_width: float, bins_before_tail: int) -> tuple[float, ...]:
    """Finite histogram for Exp(rate): M uniform bins plus one infinite tail bin."""
    rate = _positive("rate", rate)
    h = _positive("bin_width", bin_width)
    if not isinstance(bins_before_tail, int) or bins_before_tail < 1:
        raise ClockKLRefinementError("bins_before_tail must be a positive integer")

    one_minus = -math.expm1(-rate * h)
    decay = math.exp(-rate * h)
    out = [one_minus * (decay**k) for k in range(bins_before_tail)]
    out.append(decay**bins_before_tail)
    vals = tuple(out)
    if not math.isclose(sum(vals), 1.0, rel_tol=0.0, abs_tol=2.0e-12):
        raise ClockKLRefinementError("histogram normalization defect")
    if not all(v > 0.0 and math.isfinite(v) for v in vals):
        raise ClockKLRefinementError("histogram lost strict positivity")
    return vals


def kl_nats(p: Sequence[float], reference: Sequence[float]) -> float:
    p = _validate_probability_vector("p", p)
    q = _validate_probability_vector("reference", reference)
    if len(p) != len(q):
        raise ClockKLRefinementError("probability/reference lengths differ")
    return sum(pi * math.log(pi / qi) for pi, qi in zip(p, q))


def kl_bits(p: Sequence[float], reference: Sequence[float]) -> float:
    return kl_nats(p, reference) / math.log(2.0)


def reset_step(state: Sequence[float], stationary_reference: Sequence[float]) -> tuple[float, ...]:
    """Apply the row-constant kernel P_ij=pi_j; every state maps to pi."""
    _validate_probability_vector("state", state)
    pi = _validate_probability_vector("stationary_reference", stationary_reference)
    if len(state) != len(pi):
        raise ClockKLRefinementError("state/reference lengths differ")
    return pi


def finite_clock_kl(rate_reference: float, rate_local: float, bin_width: float, bins_before_tail: int) -> float:
    p = exponential_histogram(rate_reference, bin_width, bins_before_tail)
    q = exponential_histogram(rate_local, bin_width, bins_before_tail)
    return kl_nats(p, q)


def infinite_uniform_bin_kl(rate_reference: float, rate_local: float, bin_width: float) -> float:
    """Exact KL of the countably infinite uniform-bin geometric histograms."""
    ar = _positive("rate_reference", rate_reference)
    ax = _positive("rate_local", rate_local)
    h = _positive("bin_width", bin_width)
    ur = -math.expm1(-ar * h)
    ux = -math.expm1(-ax * h)
    occupancy_moment = h * math.exp(-ar * h) / ur
    return math.log(ur / ux) + (ax - ar) * occupancy_moment


def continuous_clock_kl(rate_reference: float, rate_local: float) -> float:
    ar = _positive("rate_reference", rate_reference)
    ax = _positive("rate_local", rate_local)
    ratio = ax / ar
    return ratio - 1.0 - math.log(ratio)


def reverse_continuous_clock_kl(rate_reference: float, rate_local: float) -> float:
    return continuous_clock_kl(rate_local, rate_reference)


def jeffreys_clock_kl(rate_reference: float, rate_local: float) -> float:
    return continuous_clock_kl(rate_reference, rate_local) + continuous_clock_kl(rate_local, rate_reference)


def clock_lapse(rate_reference: float, rate_local: float) -> float:
    ar = _positive("rate_reference", rate_reference)
    ax = _positive("rate_local", rate_local)
    return ax / ar


def clock_phi_from_lapse(lapse: float) -> float:
    n = _positive("lapse", lapse)
    return n - 1.0 - math.log(n)


def xi_clock(clock_information_nats: float, relational_area: float) -> float:
    j = float(clock_information_nats)
    area = _positive("relational_area", relational_area)
    if not math.isfinite(j) or j < 0.0:
        raise ClockKLRefinementError("clock information must be nonnegative finite")
    return j / area
