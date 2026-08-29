import math

import pytest

from src.idt.clock_kl_01c_refinement import (
    ClockKLRefinementError,
    clock_lapse,
    clock_phi_from_lapse,
    continuous_clock_kl,
    exponential_histogram,
    finite_clock_kl,
    infinite_uniform_bin_kl,
    jeffreys_clock_kl,
    kl_bits,
    kl_nats,
    reset_step,
    reverse_continuous_clock_kl,
    xi_clock,
)


def test_finite_exponential_histogram_is_strict_probability_vector():
    p = exponential_histogram(1.7, 0.2, 20)
    assert len(p) == 21
    assert all(x > 0.0 for x in p)
    assert sum(p) == pytest.approx(1.0, abs=2.0e-12)


def test_each_finite_histogram_is_an_01c_bit_to_nat_scalar():
    p = exponential_histogram(1.3, 0.25, 24)
    q = exponential_histogram(2.1, 0.25, 24)
    j = kl_nats(p, q)
    i_bits = kl_bits(p, q)
    assert j == pytest.approx(math.log(2.0) * i_bits)
    assert j >= 0.0


def test_rank_one_reset_kernel_has_reference_stationarity_and_contracts_kl_to_zero():
    p = exponential_histogram(1.3, 0.25, 24)
    q = exponential_histogram(2.1, 0.25, 24)
    p_after = reset_step(p, q)
    q_after = reset_step(q, q)
    assert p_after == q
    assert q_after == q
    assert kl_nats(p_after, q_after) == pytest.approx(0.0, abs=1.0e-15)
    assert kl_nats(p_after, q_after) <= kl_nats(p, q)


def test_nested_holding_time_partition_refinement_monotonically_increases_kl():
    ar, ax = 1.3, 2.1
    horizon = 8.0
    widths = (1.0, 0.5, 0.25, 0.125)
    values = []
    for h in widths:
        m = int(round(horizon / h))
        values.append(finite_clock_kl(ar, ax, h, m))
    assert all(b >= a - 1.0e-14 for a, b in zip(values, values[1:]))


def test_finite_tail_histogram_converges_to_infinite_uniform_bin_kl():
    ar, ax, h = 1.3, 2.1, 0.2
    target = infinite_uniform_bin_kl(ar, ax, h)
    coarse = finite_clock_kl(ar, ax, h, 10)
    fine = finite_clock_kl(ar, ax, h, 80)
    assert abs(fine - target) < abs(coarse - target)
    assert fine == pytest.approx(target, abs=2.0e-10)


def test_uniform_bin_refinement_converges_to_continuous_exponential_kl():
    ar, ax = 1.3, 2.1
    target = continuous_clock_kl(ar, ax)
    values = [infinite_uniform_bin_kl(ar, ax, h) for h in (0.5, 0.25, 0.125, 0.0625, 0.01)]
    errors = [abs(v - target) for v in values]
    assert all(b < a for a, b in zip(errors, errors[1:]))
    assert values[-1] == pytest.approx(target, rel=3.0e-5)


def test_05d_phi_is_exact_continuous_01c_refinement_completion():
    ar, ax = 1.7, 0.9
    n = clock_lapse(ar, ax)
    assert continuous_clock_kl(ar, ax) == pytest.approx(clock_phi_from_lapse(n))
    assert continuous_clock_kl(ar, ax) == pytest.approx(n - 1.0 - math.log(n))


def test_reverse_orientation_and_jeffreys_identity():
    ar, ax = 1.4, 2.3
    n = ax / ar
    forward = continuous_clock_kl(ar, ax)
    reverse = reverse_continuous_clock_kl(ar, ax)
    assert forward == pytest.approx(n - 1.0 - math.log(n))
    assert reverse == pytest.approx(1.0 / n - 1.0 + math.log(n))
    assert jeffreys_clock_kl(ar, ax) == pytest.approx(n + 1.0 / n - 2.0)


def test_common_rate_rescaling_preserves_clock_information():
    ar, ax = 1.4, 2.3
    base = continuous_clock_kl(ar, ax)
    for scale in (0.2, 3.7, 11.0):
        assert continuous_clock_kl(scale * ar, scale * ax) == pytest.approx(base)


def test_01k_clock_numerator_has_inverse_area_typing():
    ar, ax = 1.2, 1.8
    j = continuous_clock_kl(ar, ax)
    area = 4.5
    assert xi_clock(j, area) == pytest.approx(j / area)
    assert xi_clock(j, 9.0 * area) == pytest.approx(xi_clock(j, area) / 9.0)


def test_equal_clock_rates_give_zero_completed_information():
    for rate in (0.4, 1.0, 7.0):
        assert continuous_clock_kl(rate, rate) == pytest.approx(0.0, abs=1.0e-15)


@pytest.mark.parametrize("bad", [0.0, -1.0, math.inf, math.nan])
def test_invalid_rate_fails_closed(bad):
    with pytest.raises(ClockKLRefinementError):
        continuous_clock_kl(bad, 1.0)
    with pytest.raises(ClockKLRefinementError):
        exponential_histogram(1.0, bad, 4)


def test_invalid_histogram_size_fails_closed():
    with pytest.raises(ClockKLRefinementError):
        exponential_histogram(1.0, 0.2, 0)


def test_invalid_relational_area_fails_closed():
    with pytest.raises(ClockKLRefinementError):
        xi_clock(0.2, 0.0)
    with pytest.raises(ClockKLRefinementError):
        xi_clock(-0.1, 1.0)
