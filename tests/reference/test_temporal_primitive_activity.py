import math

import numpy as np
import pytest

from idt.temporal_primitive_activity import (
    TemporalPrimitiveError,
    activity_increment,
    activity_path_measure,
    calibrated_elapsed_increment,
    directed_kinetics,
    drive_from_shannon_affinity_bits,
    relational_lapse_from_activity,
    relational_mobility,
    reparameterize_transition_density,
    temporal_primitive_from_information,
)


def test_directed_kinetics_matches_hyperbolic_decomposition():
    k = directed_kinetics(2.5, 0.8)
    assert math.isclose(k.activity, 5.0 * math.cosh(0.4), rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(k.current, 5.0 * math.sinh(0.4), rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(k.orientation, math.tanh(0.4), rel_tol=0.0, abs_tol=1e-14)


def test_orientation_reversal_preserves_duration_density_and_flips_direction():
    plus = directed_kinetics(1.7, 1.2)
    minus = directed_kinetics(1.7, -1.2)
    assert math.isclose(plus.activity, minus.activity, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(plus.current, -minus.current, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(plus.orientation, -minus.orientation, rel_tol=0.0, abs_tol=1e-14)


def test_symmetric_point_has_positive_activity_and_zero_orientation():
    k = directed_kinetics(3.0, 0.0)
    assert k.activity == 6.0
    assert k.current == 0.0
    assert k.orientation == 0.0


def test_activity_measure_is_invariant_under_monotone_reparameterization():
    k = directed_kinetics(2.0, 0.6)
    d_lambda = 0.25
    d_lambda_prime = 0.5
    jac = d_lambda / d_lambda_prime
    forward_prime = reparameterize_transition_density(k.forward, jac)
    reverse_prime = reparameterize_transition_density(k.reverse, jac)
    activity_prime = forward_prime + reverse_prime
    assert math.isclose(
        activity_increment(k.activity, d_lambda),
        activity_increment(activity_prime, d_lambda_prime),
        rel_tol=0.0,
        abs_tol=1e-14,
    )


def test_activity_path_measure_is_additive():
    m = [1.0, 1.5, 0.8, 2.1]
    a = [0.2, -0.4, 0.7, 0.1]
    dl = [0.1, 0.3, 0.2, 0.4]
    full = activity_path_measure(m, a, dl)
    left = activity_path_measure(m[:2], a[:2], dl[:2])
    right = activity_path_measure(m[2:], a[2:], dl[2:])
    assert math.isclose(full, left + right, rel_tol=0.0, abs_tol=1e-14)


def test_relational_mobility_matches_density_viscosity_contract():
    m = relational_mobility(4.0, 9.0, 2.0, 4.0)
    assert math.isclose(m, 2.0, rel_tol=0.0, abs_tol=1e-15)


def test_shannon_affinity_maps_exactly_to_drive_and_temporal_primitive():
    sigma = 2.0
    drive = drive_from_shannon_affinity_bits(sigma)
    assert math.isclose(drive, math.log(4.0), rel_tol=0.0, abs_tol=1e-15)
    dtheta, chi = temporal_primitive_from_information(1.25, sigma, 0.4)
    expected_activity = 2.5 * math.cosh(0.5 * math.log(4.0))
    assert math.isclose(dtheta, expected_activity * 0.4, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(chi, math.tanh(0.5 * math.log(4.0)), rel_tol=0.0, abs_tol=1e-14)


def test_relational_lapse_and_calibrated_elapsed_compose():
    nxr = relational_lapse_from_activity(6.0, 3.0)
    nrs = relational_lapse_from_activity(3.0, 1.5)
    nxs = relational_lapse_from_activity(6.0, 1.5)
    assert nxr * nrs == nxs
    assert calibrated_elapsed_increment(6.0, 3.0, 0.25) == 0.5


@pytest.mark.parametrize(
    "call",
    [
        lambda: directed_kinetics(0.0, 0.2),
        lambda: activity_increment(1.0, 0.0),
        lambda: relational_lapse_from_activity(1.0, 0.0),
        lambda: relational_mobility(1.0, -1.0, 1.0, 1.0),
        lambda: activity_path_measure([1.0], [0.0, 0.2], [0.1]),
    ],
)
def test_temporal_primitive_fails_closed_on_invalid_domain(call):
    with pytest.raises(TemporalPrimitiveError):
        call()
