import math

import pytest

from idt.tir_half_fiber_temporal_normalization import (
    KAPPA,
    TIRTemporalNormalizationError,
    common_cycle_average_rates,
    intrinsic_information_rate,
    intrinsic_phase_rate,
    modular_support_count_from_winding,
    phase_clock_bridge,
    relational_lapse,
    reparameterize_rate_and_activity,
)


def test_intrinsic_phase_rate_is_reparameterization_invariant():
    omega = 7.5
    activity = 2.5
    original = intrinsic_phase_rate(omega, activity)
    omega_p, activity_p = reparameterize_rate_and_activity(
        omega,
        activity,
        d_lambda_d_lambda_prime=0.2,
    )
    transformed = intrinsic_phase_rate(omega_p, activity_p)
    assert math.isclose(original, transformed, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(original, 3.0, rel_tol=0.0, abs_tol=1e-15)


def test_intrinsic_information_rate_preserves_tir_kappa_identity():
    omega_theta = intrinsic_phase_rate(12.0, 3.0)
    gamma = intrinsic_information_rate(12.0, 3.0)
    assert math.isclose(gamma, KAPPA * omega_theta, rel_tol=0.0, abs_tol=1e-15)


def test_phase_clock_bridge_reproduces_lapse_rate_identity():
    bridge = phase_clock_bridge(
        phase_rate_lambda=15.0,
        activity_x=5.0,
        activity_ref=2.0,
        reference_time_scale=4.0,
    )
    assert math.isclose(bridge.relational_lapse, 2.5, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(bridge.intrinsic_phase_rate, 3.0, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(bridge.local_calibrated_phase_rate, 0.75, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(
        bridge.coordinate_phase_rate,
        bridge.relational_lapse * bridge.local_calibrated_phase_rate,
        rel_tol=0.0,
        abs_tol=1e-15,
    )


def test_relational_lapse_is_activity_ratio():
    assert math.isclose(relational_lapse(6.0, 1.5), 4.0, rel_tol=0.0, abs_tol=1e-15)


def test_common_cycle_average_rate_ratio_is_winding_ratio():
    for m_i, m_j, delta_theta in (
        (1, 2, 0.75),
        (2, 3, 4.0),
        (5, 2, 11.5),
        (-3, 4, 2.25),
    ):
        omega_i, omega_j, ratio = common_cycle_average_rates(m_i, m_j, delta_theta)
        assert math.isclose(omega_i / omega_j, ratio, rel_tol=0.0, abs_tol=1e-15)
        assert math.isclose(ratio, m_i / m_j, rel_tol=0.0, abs_tol=1e-15)


def test_common_cycle_ratio_is_independent_of_intrinsic_interval_scale():
    _, _, ratio_a = common_cycle_average_rates(3, 5, 1.0)
    _, _, ratio_b = common_cycle_average_rates(3, 5, 100.0)
    assert math.isclose(ratio_a, ratio_b, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(ratio_a, 3.0 / 5.0, rel_tol=0.0, abs_tol=1e-15)


def test_modular_frame_winding_gives_n_plus_one_half_frame_supports():
    assert modular_support_count_from_winding(1) == 2
    assert modular_support_count_from_winding(2) == 3
    assert modular_support_count_from_winding(3) == 4
    assert modular_support_count_from_winding(4) == 5


@pytest.mark.parametrize(
    "call",
    [
        lambda: intrinsic_phase_rate(1.0, 0.0),
        lambda: reparameterize_rate_and_activity(1.0, 1.0, 0.0),
        lambda: relational_lapse(1.0, 0.0),
        lambda: phase_clock_bridge(1.0, 1.0, 1.0, 0.0),
        lambda: common_cycle_average_rates(1, 0, 1.0),
        lambda: common_cycle_average_rates(1, 2, 0.0),
        lambda: modular_support_count_from_winding(0),
    ],
)
def test_bridge_fails_closed_on_invalid_domain(call):
    with pytest.raises(TIRTemporalNormalizationError):
        call()
