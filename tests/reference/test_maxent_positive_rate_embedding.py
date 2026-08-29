import math

import pytest

from src.idt.maxent_positive_rate_embedding import (
    MaxEntRateEmbeddingError,
    activity_clock_information_nats,
    common_scale_information_nats,
    exponential_density,
    fisher_metric_log_rate,
    fisher_metric_rate,
    maxent_entropy_nats,
    phase_rate_information_nats,
    phi_ratio,
    rate_information_nats,
    reciprocal_mean,
    uniform_same_mean_entropy_nats,
    uniform_to_maxent_kl_nats,
    xi_rate,
)


def test_exponential_embedding_has_reciprocal_mean_coordinate():
    for rate in (0.4, 1.0, 3.7):
        assert reciprocal_mean(rate) == pytest.approx(1.0 / rate)


def test_rate_embedding_is_scale_covariant():
    r = 1.7
    c = 3.2
    for t in (0.0, 0.1, 0.7, 2.0):
        assert exponential_density(c * r, t) == pytest.approx(c * exponential_density(r, c * t))


def test_exponential_entropy_beats_same_mean_uniform_competitor():
    for r in (0.3, 1.0, 4.2):
        h_exp = maxent_entropy_nats(r)
        h_uniform = uniform_same_mean_entropy_nats(r)
        assert h_exp > h_uniform
        assert h_exp - h_uniform == pytest.approx(1.0 - math.log(2.0))
        assert uniform_to_maxent_kl_nats(r) == pytest.approx(h_exp - h_uniform)


def test_rate_kl_equals_burg_phi_of_inverse_rate_ratio():
    a, b = 2.4, 0.9
    x = b / a
    assert rate_information_nats(a, b) == pytest.approx(phi_ratio(x))
    assert rate_information_nats(a, b) == pytest.approx(math.log(a / b) + b / a - 1.0)


def test_05d_activity_clock_specialization_is_recovered():
    a_ref, a_local = 1.3, 2.1
    n = a_local / a_ref
    j = activity_clock_information_nats(a_ref, a_local)
    assert j == pytest.approx(phi_ratio(n))
    assert j == pytest.approx(n - 1.0 - math.log(n))


def test_rfe16_phase_rate_specialization_produces_phi_of_reciprocal_rate_ratio():
    r0 = 2.0
    r_s = 1.4
    r_ratio = r_s / r0
    x_s = 1.0 / r_ratio
    j = phase_rate_information_nats(r_s, r0)
    assert j == pytest.approx(phi_ratio(x_s))
    assert j == pytest.approx(x_s - 1.0 - math.log(x_s))


def test_common_rate_scale_cancels_from_relative_information():
    base, scaled = common_scale_information_nats(1.4, 2.3, 7.2)
    assert scaled == pytest.approx(base)


def test_equal_rates_have_zero_information():
    for r in (0.5, 1.0, 5.0):
        assert rate_information_nats(r, r) == pytest.approx(0.0, abs=1.0e-15)


def test_information_is_nonnegative_for_distinct_rates():
    assert rate_information_nats(1.0, 2.0) > 0.0
    assert rate_information_nats(2.0, 1.0) > 0.0


def test_fisher_metric_is_flat_in_log_rate_coordinate():
    r = 1.8
    assert fisher_metric_rate(r) == pytest.approx(1.0 / r**2)
    assert fisher_metric_log_rate() == pytest.approx(1.0)

    # J(r || r*exp(d)) = exp(d)-1-d = 1/2 d^2 + O(d^3).
    for d in (1.0e-3, -1.0e-3):
        local = rate_information_nats(r, r * math.exp(d))
        assert local / (0.5 * d * d) == pytest.approx(1.0, rel=7.0e-4)


def test_01k_rate_information_curvature_has_inverse_area_scaling():
    a, b = 1.2, 1.9
    area = 3.5
    xi = xi_rate(a, b, area)
    assert xi == pytest.approx(rate_information_nats(a, b) / area)
    assert xi_rate(a, b, 4.0 * area) == pytest.approx(xi / 4.0)


@pytest.mark.parametrize("bad", [0.0, -1.0, math.inf, math.nan])
def test_invalid_rate_fails_closed(bad):
    with pytest.raises(MaxEntRateEmbeddingError):
        rate_information_nats(bad, 1.0)
    with pytest.raises(MaxEntRateEmbeddingError):
        exponential_density(bad, 0.0)


def test_invalid_time_and_area_fail_closed():
    with pytest.raises(MaxEntRateEmbeddingError):
        exponential_density(1.0, -0.1)
    with pytest.raises(MaxEntRateEmbeddingError):
        xi_rate(1.0, 2.0, 0.0)
