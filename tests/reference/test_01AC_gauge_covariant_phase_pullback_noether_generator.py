import math
import pytest


def transformed_connection(connection, d_lambda):
    return connection - d_lambda


def transformed_phase_gradient(d_theta, d_lambda):
    return d_theta + d_lambda


def covariant_phase_gradient(d_theta, connection):
    return d_theta + connection


def field_inertia(amplitudes, volumes):
    if len(amplitudes) != len(volumes) or not amplitudes:
        raise ValueError("common non-empty support required")
    if any(a < 0.0 for a in amplitudes):
        raise ValueError("non-negative amplitudes required")
    if any(v <= 0.0 for v in volumes):
        raise ValueError("positive volumes required")
    return 2.0 * sum(a * a * v for a, v in zip(amplitudes, volumes))


def test_admitted_berry_sign_makes_dtheta_plus_connection_gauge_invariant():
    d_theta = 0.7
    connection = -0.2
    d_lambda = 1.3
    before = covariant_phase_gradient(d_theta, connection)
    after = covariant_phase_gradient(
        transformed_phase_gradient(d_theta, d_lambda),
        transformed_connection(connection, d_lambda),
    )
    assert math.isclose(before, after, rel_tol=1e-15, abs_tol=1e-15)


def test_opposite_connection_sign_fails_same_gauge_invariance_witness():
    d_theta = 0.7
    connection = -0.2
    d_lambda = 1.3
    before = d_theta - connection
    after = transformed_phase_gradient(d_theta, d_lambda) - transformed_connection(connection, d_lambda)
    assert not math.isclose(before, after, rel_tol=1e-15, abs_tol=1e-15)


def test_pullback_of_common_fiber_coordinate_equals_rotor_covariant_rate():
    d_theta_dq = [0.4, -0.2, 0.3]
    connection = [0.1, 0.5, -0.4]
    qdot = [0.7, -0.6, 0.2]
    theta_dot = sum(g * v for g, v in zip(d_theta_dq, qdot))
    pullback = sum((g + a) * v for g, a, v in zip(d_theta_dq, connection, qdot))
    dchi = theta_dot + sum(a * v for a, v in zip(connection, qdot))
    assert math.isclose(pullback, dchi, rel_tol=1e-15, abs_tol=1e-15)


def test_covariant_field_action_reduces_to_rotor_quadratic_coefficient():
    amplitudes = [1.0, 0.5, 1.5]
    volumes = [0.75, 2.0, 0.5]
    rate = 0.8
    i_a = field_inertia(amplitudes, volumes)
    field_phase = sum(a * a * v * rate * rate for a, v in zip(amplitudes, volumes))
    rotor_phase = 0.5 * i_a * rate * rate
    assert math.isclose(field_phase, rotor_phase, rel_tol=1e-15, abs_tol=1e-15)


def test_noether_moment_map_equals_rotor_generator_after_coefficient_match():
    amplitudes = [1.2, 0.6]
    volumes = [1.0, 1.5]
    rate = 0.45
    i_a = field_inertia(amplitudes, volumes)
    i_phi = i_a
    q_theta = sum(2.0 * a * a * rate * v for a, v in zip(amplitudes, volumes))
    p_phi = i_phi * rate
    assert math.isclose(q_theta, p_phi, rel_tol=1e-15, abs_tol=1e-15)


def test_energy_per_common_generator_is_half_covariant_rate():
    i_phi = field_inertia([1.0, 0.75], [1.25, 0.8])
    rate = 0.55
    p_phi = i_phi * rate
    q_theta = p_phi
    h_phi = p_phi * p_phi / (2.0 * i_phi)
    epsilon = h_phi / q_theta
    assert math.isclose(epsilon, 0.5 * rate, rel_tol=1e-15, abs_tol=1e-15)


def test_rate_and_generator_defects_detect_independent_mismatch():
    field_rate = 0.6
    rotor_rate = 0.5
    i_a = 4.0
    i_phi = 4.0
    q_theta = i_a * field_rate
    p_phi = i_phi * rotor_rate
    delta_rate = abs(field_rate - rotor_rate) / abs(rotor_rate)
    delta_q = abs(q_theta - p_phi) / abs(p_phi)
    assert delta_rate > 0.0
    assert delta_q > 0.0


def test_admission_inputs_fail_closed_on_degenerate_support_or_zero_reference_rate():
    with pytest.raises(ValueError, match="common non-empty support"):
        field_inertia([1.0], [])
    with pytest.raises(ValueError, match="non-negative amplitudes"):
        field_inertia([-0.1], [1.0])
    with pytest.raises(ValueError, match="positive volumes"):
        field_inertia([1.0], [0.0])
    rotor_rate = 0.0
    with pytest.raises(ZeroDivisionError):
        _ = abs(0.1 - rotor_rate) / abs(rotor_rate)
