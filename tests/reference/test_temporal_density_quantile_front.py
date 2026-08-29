import math

import numpy as np
import pytest

from idt.temporal_density_quantile_front import (
    TemporalDensityFrontError,
    audit_quantile_front,
    barycenter,
    barycenter_rate_zero_flux,
    cumulative_mass_fraction,
    discrete_cumulative_mass_rate,
    quantile_position,
    quantile_velocity,
    total_mass,
    variance,
    variance_rate_zero_flux,
)


def _gaussian_reference():
    x = np.linspace(-8.0, 8.0, 4001)
    rho = np.exp(-0.5 * x * x)
    return x, rho


def test_cumulative_mass_fraction_is_normalized_and_monotone():
    x, rho = _gaussian_reference()
    c = cumulative_mass_fraction(x, rho)
    assert c[0] == 0.0
    assert math.isclose(c[-1], 1.0, rel_tol=0.0, abs_tol=1e-15)
    assert np.all(np.diff(c) >= 0.0)


def test_half_mass_marker_is_center_for_symmetric_reference():
    x, rho = _gaussian_reference()
    x_half = quantile_position(x, rho, 0.5)
    assert abs(x_half) < 1e-12


def test_quantile_positions_are_invariant_under_positive_density_rescaling():
    x, rho = _gaussian_reference()
    for q in (0.1, 0.25, 0.5, 0.75, 0.9):
        a = quantile_position(x, rho, q)
        b = quantile_position(x, 17.0 * rho, q)
        assert math.isclose(a, b, rel_tol=0.0, abs_tol=1e-13)


def test_translating_current_advects_every_quantile_at_same_velocity():
    x, rho = _gaussian_reference()
    velocity = 1.75
    current = velocity * rho
    for q in (0.1, 0.25, 0.5, 0.75, 0.9):
        front = audit_quantile_front(x, rho, current, q)
        assert math.isclose(front.theta_velocity, velocity, rel_tol=0.0, abs_tol=2e-13)


def test_quantile_velocity_includes_left_boundary_flux_exactly():
    assert quantile_velocity(2.0, 7.0, left_boundary_current=1.0) == 3.0


def test_discrete_cumulative_mass_rate_is_edge_flux_telescoping():
    edge = np.array([0.2, -0.1, 0.5])
    dp = np.array([-edge[0], edge[0] - edge[1], edge[1] - edge[2], edge[2]])
    assert math.isclose(float(np.sum(dp[:2])), discrete_cumulative_mass_rate(edge, 1), abs_tol=1e-15)
    assert math.isclose(float(np.sum(dp[:3])), discrete_cumulative_mass_rate(edge, 2), abs_tol=1e-15)


def test_barycenter_rate_matches_mass_weighted_translation_velocity():
    x, rho = _gaussian_reference()
    velocity = -0.8
    current = velocity * rho
    assert abs(barycenter(x, rho)) < 1e-14
    assert math.isclose(barycenter_rate_zero_flux(x, rho, current), velocity, rel_tol=0.0, abs_tol=1e-13)


def test_variance_rate_vanishes_for_rigid_translation():
    x, rho = _gaussian_reference()
    current = 2.4 * rho
    assert variance(x, rho) > 0.0
    assert abs(variance_rate_zero_flux(x, rho, current)) < 1e-13


def test_variance_rate_matches_linear_expansion_flow():
    x, rho = _gaussian_reference()
    mean = barycenter(x, rho)
    beta = 0.35
    current = beta * (x - mean) * rho
    expected = 2.0 * beta * variance(x, rho)
    measured = variance_rate_zero_flux(x, rho, current)
    assert math.isclose(measured, expected, rel_tol=0.0, abs_tol=2e-13)


def test_total_mass_positive_reference():
    x, rho = _gaussian_reference()
    assert total_mass(x, rho) > 0.0


@pytest.mark.parametrize(
    "call",
    [
        lambda: quantile_position([0.0, 1.0], [1.0, 1.0], 0.0),
        lambda: quantile_position([0.0, 1.0], [1.0, 1.0], 1.0),
        lambda: quantile_position([0.0, 1.0], [1.0, -1.0], 0.5),
        lambda: quantile_velocity(0.0, 1.0),
        lambda: total_mass([0.0, 0.0], [1.0, 1.0]),
        lambda: discrete_cumulative_mass_rate([1.0], 1),
    ],
)
def test_front_gate_fails_closed(call):
    with pytest.raises(TemporalDensityFrontError):
        call()
