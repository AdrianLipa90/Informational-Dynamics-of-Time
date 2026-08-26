import math

import numpy as np
import pytest

from src.idt.kepler_memory import (
    KeplerMemoryError, MemoryPhaseState, apply_memory_impulse, kepler_memory_step,
    kepler_radius_from_true_anomaly, kepler_semi_latus_rectum, memory_areal_velocity, memory_gravity, memory_orbital_elements,
    propagate_memory_orbit, temporal_memory_step,
)


def test_memory_gravity_is_inverse_square_and_radial():
    a = memory_gravity([2.0, 0.0], 8.0)
    assert np.allclose(a, [-2.0, 0.0], atol=1e-14, rtol=0.0)


def test_circular_reference_orbit_elements():
    mu = 1.0
    state = MemoryPhaseState(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    e = memory_orbital_elements(state.position, state.velocity, mu)
    assert e.orbit_class == "BOUND_ELLIPTIC"
    assert math.isclose(e.specific_energy, -0.5, abs_tol=1e-14)
    assert math.isclose(e.angular_momentum, 1.0, abs_tol=1e-14)
    assert math.isclose(e.areal_velocity, 0.5, abs_tol=1e-14)
    assert math.isclose(e.eccentricity, 0.0, abs_tol=1e-14)
    assert math.isclose(e.semi_major_axis, 1.0, abs_tol=1e-14)
    assert math.isclose(e.period, 2.0 * math.pi, rel_tol=0.0, abs_tol=1e-14)


def test_areal_velocity_is_half_angular_momentum():
    assert math.isclose(memory_areal_velocity([2.0, 0.0], [0.0, 3.0]), 3.0, abs_tol=1e-14)


def test_velocity_verlet_preserves_bound_orbit_invariants_reference_run():
    mu = 1.0
    s0 = MemoryPhaseState(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    e0 = memory_orbital_elements(s0.position, s0.velocity, mu)
    states = propagate_memory_orbit(s0, mu, 0.002, 4000)
    s1 = states[-1]
    e1 = memory_orbital_elements(s1.position, s1.velocity, mu)
    assert abs(e1.specific_energy - e0.specific_energy) < 2e-6
    assert abs(e1.angular_momentum - e0.angular_momentum) < 2e-12
    assert e1.orbit_class == "BOUND_ELLIPTIC"


def test_temporal_activity_supplies_internal_step_size():
    s0 = MemoryPhaseState(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    s1 = temporal_memory_step(s0, 1.0, activity=2.0, delta_lambda=0.1, reference_activity=4.0)
    assert math.isclose(s1.tau_internal, 0.05, abs_tol=1e-14)


def test_impulse_can_move_bound_orbit_to_unbound_class():
    mu = 1.0
    s0 = MemoryPhaseState(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    assert memory_orbital_elements(s0.position, s0.velocity, mu).orbit_class == "BOUND_ELLIPTIC"
    s1 = apply_memory_impulse(s0, [0.0, 1.0])
    assert memory_orbital_elements(s1.position, s1.velocity, mu).orbit_class == "UNBOUND_HYPERBOLIC"
    assert np.allclose(s1.position, s0.position)


def test_zero_radius_fails_closed():
    with pytest.raises(KeplerMemoryError):
        memory_gravity([0.0, 0.0], 1.0)


def test_nonpositive_mu_fails_closed():
    with pytest.raises(KeplerMemoryError):
        memory_gravity([1.0, 0.0], 0.0)


def test_kepler_conic_radius_reference_identity():
    p = kepler_semi_latus_rectum(1.0, 1.0)
    assert math.isclose(p, 1.0, abs_tol=1e-14)
    assert math.isclose(kepler_radius_from_true_anomaly(0.0, 1.0, 0.25, 1.0), 0.8, abs_tol=1e-14)


def test_one_circular_period_sweeps_pi_area():
    s0 = MemoryPhaseState(np.array([1.0, 0.0]), np.array([0.0, 1.0]))
    n = 5000
    dt = 2.0 * math.pi / n
    s1 = propagate_memory_orbit(s0, 1.0, dt, n)[-1]
    assert math.isclose(s1.swept_area, math.pi, rel_tol=0.0, abs_tol=2e-10)


def test_velocity_verlet_swept_area_matches_kepler_areal_law_per_step():
    s0 = MemoryPhaseState(np.array([1.3, -0.2]), np.array([0.4, 0.9]))
    dt = 0.017
    h0 = memory_orbital_elements(s0.position, s0.velocity, 1.7).angular_momentum
    s1 = kepler_memory_step(s0, 1.7, dt)
    assert math.isclose(s1.swept_area - s0.swept_area, 0.5 * h0 * dt, rel_tol=0.0, abs_tol=1e-14)
