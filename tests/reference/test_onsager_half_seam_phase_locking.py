import math

import numpy as np
import pytest

from idt.onsager_half_seam_phase_locking import (
    OnsagerHalfSeamError,
    audit_seam_lock_state,
    integrate_single_seam,
    locked_rate_residual,
    network_onsager_velocity,
    resonant_defect_potential,
    resonant_mismatch,
    resonant_onsager_velocity,
    seam_defect_gradient,
    seam_defect_potential,
    seam_lyapunov_rate,
    seam_onsager_velocity,
)


def test_seam_defect_gradient_matches_finite_difference():
    delta = 0.73
    r0, r1 = 0.8, 1.2
    eps = 1e-7
    numerical = (
        seam_defect_potential(delta + eps, r0, r1)
        - seam_defect_potential(delta - eps, r0, r1)
    ) / (2.0 * eps)
    analytic = seam_defect_gradient(delta, r0, r1)
    assert math.isclose(numerical, analytic, rel_tol=0.0, abs_tol=2e-9)


def test_onsager_velocity_is_negative_defect_gradient():
    delta = 0.8
    r0, r1, mu = 1.1, 0.9, 2.5
    grad = seam_defect_gradient(delta, r0, r1)
    vel = seam_onsager_velocity(delta, r0, r1, mu)
    assert math.isclose(vel, -mu * grad, rel_tol=0.0, abs_tol=1e-15)


def test_lyapunov_rate_is_nonpositive_and_exact():
    for delta in np.linspace(-math.pi, math.pi, 17):
        grad = seam_defect_gradient(float(delta), 0.7, 1.3)
        rate = seam_lyapunov_rate(float(delta), 0.7, 1.3, 1.8)
        assert rate <= 1e-15
        assert math.isclose(rate, -1.8 * grad * grad, rel_tol=0.0, abs_tol=1e-15)


def test_constructive_seam_is_stable_minimum_and_pi_is_null_maximum():
    eps = 1e-4
    v0 = seam_defect_potential(0.0, 1.0, 1.0)
    vp = seam_defect_potential(math.pi, 1.0, 1.0)
    assert v0 == 0.0
    assert math.isclose(vp, 1.0, rel_tol=0.0, abs_tol=1e-15)
    assert seam_defect_potential(eps, 1.0, 1.0) > v0
    assert seam_defect_potential(math.pi - eps, 1.0, 1.0) < vp
    assert abs(seam_onsager_velocity(0.0, 1.0, 1.0, 1.0)) < 1e-15
    assert abs(seam_onsager_velocity(math.pi, 1.0, 1.0, 1.0)) < 1e-15


def test_single_seam_flow_reduces_mismatch_and_defect():
    path = integrate_single_seam(
        mismatch0=1.2,
        magnitude_left=1.0,
        magnitude_right=1.0,
        mobility=2.0,
        delta_theta=4.0,
        steps=2000,
    )
    assert abs(path[-1]) < abs(path[0])
    v = np.array([seam_defect_potential(float(x), 1.0, 1.0) for x in path])
    assert np.max(np.diff(v)) < 2e-12
    assert v[-1] < 1e-3 * v[0]


def test_small_mismatch_relaxation_matches_linear_rate():
    delta0 = 1e-5
    r0, r1, mu = 0.8, 1.4, 3.0
    k = 0.5 * mu * r0 * r1
    delta_theta = 0.2
    path = integrate_single_seam(delta0, r0, r1, mu, delta_theta, steps=500)
    expected = delta0 * math.exp(-k * delta_theta)
    assert math.isclose(path[-1], expected, rel_tol=2e-7, abs_tol=1e-12)


def test_network_positive_semidefinite_onsager_matrix_gives_nonpositive_rate():
    grad = np.array([0.4, -0.2, 0.7])
    g = np.array([
        [2.0, 0.3, 0.0],
        [0.3, 1.2, 0.2],
        [0.0, 0.2, 0.8],
    ])
    velocity, rate = network_onsager_velocity([0.1, 0.2, -0.3], grad, g)
    np.testing.assert_allclose(velocity, -(g @ grad), atol=1e-15)
    assert rate <= 0.0
    assert math.isclose(rate, -float(grad @ g @ grad), rel_tol=0.0, abs_tol=1e-15)


def test_winding_weighted_resonant_mismatch_is_zero_at_target_ratio():
    m_i, m_j = 2, 3
    phi_i = 2.0
    phi_j = (m_j / m_i) * phi_i
    delta = resonant_mismatch(phi_i, phi_j, m_i, m_j, 0.0)
    assert abs(delta) < 1e-15
    assert resonant_defect_potential(delta, 1.7) == 0.0
    assert abs(resonant_onsager_velocity(delta, 1.7, 2.0)) < 1e-15


def test_locked_stationary_connection_gives_local_winding_rate_ratio():
    m_i, m_j = 3, 5
    omega_j = 7.0
    omega_i = (m_i / m_j) * omega_j
    residual = locked_rate_residual(
        omega_i=omega_i,
        omega_j=omega_j,
        winding_i=m_i,
        winding_j=m_j,
        connection_rate=0.0,
    )
    assert abs(residual) < 1e-14
    assert math.isclose(omega_i / omega_j, m_i / m_j, rel_tol=0.0, abs_tol=1e-15)


def test_connection_rate_is_exact_detuning_source():
    m_i, m_j = 2, 5
    omega_i, omega_j = 3.0, 4.0
    source = m_j * omega_i - m_i * omega_j
    residual = locked_rate_residual(omega_i, omega_j, m_i, m_j, source)
    assert abs(residual) < 1e-15


def test_audit_state_matches_declared_identities():
    state = audit_seam_lock_state(0.4, 0.9, 1.1, 1.5)
    assert state.lyapunov_rate <= 0.0
    assert math.isclose(state.theta_velocity, -1.5 * state.gradient, rel_tol=0.0, abs_tol=1e-15)


@pytest.mark.parametrize(
    "call",
    [
        lambda: seam_defect_potential(0.0, 0.0, 1.0),
        lambda: seam_onsager_velocity(0.0, 1.0, 1.0, 0.0),
        lambda: integrate_single_seam(0.0, 1.0, 1.0, 1.0, -1.0),
        lambda: integrate_single_seam(0.0, 1.0, 1.0, 1.0, 1.0, steps=0),
        lambda: network_onsager_velocity([0.0, 1.0], [1.0], np.eye(2)),
        lambda: network_onsager_velocity([0.0, 1.0], [1.0, 1.0], [[1.0, 2.0], [0.0, 1.0]]),
        lambda: resonant_defect_potential(0.0, 0.0),
    ],
)
def test_phase_locking_fails_closed_on_invalid_domain(call):
    with pytest.raises(OnsagerHalfSeamError):
        call()
