import math
import pytest


def proper_rate_from_coordinate_rate(coordinate_rate, lapse):
    if lapse <= 0.0:
        raise ValueError("positive lapse required")
    return coordinate_rate / lapse


def test_relational_lapse_converts_coordinate_rate_to_local_proper_rate():
    lapse = 1.25
    coordinate_rate = 0.8
    proper_rate = proper_rate_from_coordinate_rate(coordinate_rate, lapse)
    assert math.isclose(proper_rate, 0.64, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose(coordinate_rate, lapse * proper_rate, rel_tol=1e-15, abs_tol=1e-15)


def test_zero_shift_temporal_coframe_normal_rate_matches_proper_rotor_rate():
    lapse = 0.75
    coordinate_phase_rate = 0.9
    normal_proper_rate = coordinate_phase_rate / lapse
    rotor_proper_rate = proper_rate_from_coordinate_rate(coordinate_phase_rate, lapse)
    assert math.isclose(normal_proper_rate, rotor_proper_rate, rel_tol=1e-15, abs_tol=1e-15)


def test_lapse_rate_defect_is_zero_for_exact_bridge():
    lapse = 1.4
    normal_rate = 0.5
    coordinate_rate = lapse * normal_rate
    delta = abs(coordinate_rate - lapse * normal_rate) / abs(coordinate_rate)
    assert delta == 0.0


def test_lapse_rate_defect_detects_independent_normal_mismatch():
    lapse = 1.4
    coordinate_rate = 0.7
    normal_rate = 0.48
    delta = abs(coordinate_rate - lapse * normal_rate) / abs(coordinate_rate)
    assert delta > 0.0


def test_noether_and_rotor_generators_match_after_lapse_and_inertia_gates():
    lapse = 1.2
    coordinate_rate = 0.72
    proper_rate = proper_rate_from_coordinate_rate(coordinate_rate, lapse)
    i_a = 3.5
    i_phi = i_a
    q_theta = i_a * proper_rate
    p_phi = i_phi * proper_rate
    assert math.isclose(q_theta, p_phi, rel_tol=1e-15, abs_tol=1e-15)


def test_energy_per_carrier_has_coordinate_and_proper_time_forms():
    lapse = 1.6
    coordinate_rate = 0.96
    proper_rate = proper_rate_from_coordinate_rate(coordinate_rate, lapse)
    epsilon_from_proper_rate = 0.5 * proper_rate
    epsilon_from_coordinate_rate = coordinate_rate / (2.0 * lapse)
    assert math.isclose(epsilon_from_proper_rate, epsilon_from_coordinate_rate, rel_tol=1e-15, abs_tol=1e-15)


def test_reference_clock_rescaling_cancels_in_proper_rate_when_lapse_transforms_consistently():
    lapse = 1.5
    coordinate_rate = 0.9
    proper = coordinate_rate / lapse
    reference_rescale = 2.0
    transformed_coordinate_rate = coordinate_rate / reference_rescale
    transformed_lapse = lapse / reference_rescale
    assert math.isclose(transformed_coordinate_rate / transformed_lapse, proper, rel_tol=1e-15, abs_tol=1e-15)


def test_degenerate_lapse_and_coordinate_reference_fail_closed():
    with pytest.raises(ValueError, match="positive lapse"):
        proper_rate_from_coordinate_rate(0.5, 0.0)
    coordinate_rate = 0.0
    with pytest.raises(ZeroDivisionError):
        _ = abs(coordinate_rate - 1.0 * 0.2) / abs(coordinate_rate)
