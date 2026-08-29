import math

import pytest

from src.idt.local_clock_relative_entropy import (
    LocalClockRelativeEntropyError,
    clock_relative_entropy,
    common_scale_invariant,
    exponential_rate_kl,
    phi_ratio,
)


def test_exponential_kl_reduces_exactly_to_phi_of_lapse():
    ax = 3.7
    ar = 1.9
    n = ax / ar
    assert exponential_rate_kl(ar, ax) == pytest.approx(phi_ratio(n))
    assert exponential_rate_kl(ax, ar) == pytest.approx(phi_ratio(1.0 / n))


def test_reference_clock_is_unique_zero():
    assert phi_ratio(1.0) == pytest.approx(0.0)
    for x in (0.1, 0.5, 0.9, 1.1, 2.0, 10.0):
        assert phi_ratio(x) > 0.0


def test_reverse_orientation_and_jeffreys_identity():
    state = clock_relative_entropy(5.0, 2.0)
    n = state["N_R"]
    assert state["ref_to_local"] == pytest.approx(phi_ratio(n))
    assert state["local_to_ref"] == pytest.approx(phi_ratio(1.0 / n))
    assert state["jeffreys"] == pytest.approx(n + 1.0 / n - 2.0)


def test_local_fisher_hessian_is_one_at_reference():
    eps = 1.0e-5
    second = (phi_ratio(1.0 + eps) - 2.0 * phi_ratio(1.0) + phi_ratio(1.0 - eps)) / eps**2
    assert second == pytest.approx(1.0, rel=2.0e-5)


def test_small_lapse_series_has_half_quadratic_leading_term():
    eps = 1.0e-4
    exact = phi_ratio(1.0 + eps)
    series = 0.5 * eps**2 - eps**3 / 3.0 + eps**4 / 4.0
    assert exact == pytest.approx(series, rel=1.0e-4, abs=1.0e-15)


def test_common_activity_rescaling_is_invariant():
    assert common_scale_invariant(2.3, 0.8, 7.1)


def test_fisher_metric_is_inverse_square_lapse():
    state = clock_relative_entropy(6.0, 2.0)
    assert state["fisher_metric"] == pytest.approx(1.0 / 9.0)


@pytest.mark.parametrize("value", [0.0, -1.0, math.inf, math.nan])
def test_phi_domain_fails_closed(value):
    with pytest.raises(LocalClockRelativeEntropyError):
        phi_ratio(value)


@pytest.mark.parametrize(
    "ax,ar",
    [(0.0, 1.0), (1.0, 0.0), (-1.0, 2.0), (math.nan, 1.0), (1.0, math.inf)],
)
def test_invalid_clock_activity_fails_closed(ax, ar):
    with pytest.raises(LocalClockRelativeEntropyError):
        clock_relative_entropy(ax, ar)
