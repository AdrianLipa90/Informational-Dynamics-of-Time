import math

import numpy as np
import pytest

from idt.continuum_phase_onsager import (
    ContinuumPhaseOnsagerError,
    audit_phase_onsager_periodic,
    constant_coefficient_current,
    constant_coefficient_current_velocity,
    constant_coefficient_q_velocity,
    density_rate_from_tangent,
    gauge_transform_periodic,
    onsager_phase_velocity_periodic,
    periodic_covariant_phase_gradient,
    phase_energy_vertex_derivative_periodic,
    phase_gradient_energy_periodic,
    phase_only_state_tangent,
)


def _fixture(n=64):
    length = 2.0 * math.pi
    h = length / n
    x = np.arange(n) * h
    xm = (x + 0.5 * h) % length
    alpha = 0.3 * np.sin(x) + 0.1 * np.cos(2.0 * x)
    connection = 0.15 * np.cos(xm)
    coefficient = 1.2 + 0.2 * np.sin(xm)
    return h, x, xm, alpha, connection, coefficient


def test_exact_periodic_energy_derivative_matches_finite_difference():
    h, _, _, alpha, connection, coefficient = _fixture(32)
    grad = phase_energy_vertex_derivative_periodic(alpha, connection, coefficient, h)
    eps = 1e-7
    for index in (0, 5, 17, 31):
        plus = alpha.copy()
        minus = alpha.copy()
        plus[index] += eps
        minus[index] -= eps
        numeric = (
            phase_gradient_energy_periodic(plus, connection, coefficient, h)
            - phase_gradient_energy_periodic(minus, connection, coefficient, h)
        ) / (2.0 * eps)
        assert math.isclose(numeric, grad[index], rel_tol=0.0, abs_tol=2e-8)


def test_onsager_phase_flow_has_exact_nonpositive_energy_rate():
    h, _, _, alpha, connection, coefficient = _fixture(48)
    mu = 0.7
    audit = audit_phase_onsager_periodic(alpha, connection, coefficient, h, mu)
    euclidean_derivative = phase_energy_vertex_derivative_periodic(alpha, connection, coefficient, h)
    direct_rate = float(np.dot(euclidean_derivative, audit.phase_velocity))
    assert audit.energy > 0.0
    assert audit.dissipation_rate < 0.0
    assert math.isclose(direct_rate, audit.dissipation_rate, rel_tol=0.0, abs_tol=2e-13)


def test_discrete_gauge_transformation_preserves_q_energy_and_flow():
    h, x, _, alpha, connection, coefficient = _fixture(64)
    chi = 0.27 * np.sin(3.0 * x) - 0.11 * np.cos(x)
    transformed_alpha, transformed_connection = gauge_transform_periodic(alpha, connection, chi, h)

    q0 = periodic_covariant_phase_gradient(alpha, connection, h)
    q1 = periodic_covariant_phase_gradient(transformed_alpha, transformed_connection, h)
    np.testing.assert_allclose(q1, q0, rtol=0.0, atol=2e-14)

    e0 = phase_gradient_energy_periodic(alpha, connection, coefficient, h)
    e1 = phase_gradient_energy_periodic(transformed_alpha, transformed_connection, coefficient, h)
    assert math.isclose(e1, e0, rel_tol=0.0, abs_tol=2e-14)

    v0 = onsager_phase_velocity_periodic(alpha, connection, coefficient, h, 0.4)
    v1 = onsager_phase_velocity_periodic(transformed_alpha, transformed_connection, coefficient, h, 0.4)
    np.testing.assert_allclose(v1, v0, rtol=0.0, atol=3e-13)


def test_phase_only_tangent_preserves_vertex_density_pointwise():
    psi = np.array([1.0 + 0.5j, -0.2 + 0.7j, 0.3 - 0.1j, -0.8j], dtype=complex)
    velocity = np.array([0.2, -0.3, 0.5, 0.1])
    tangent = phase_only_state_tangent(psi, velocity)
    density_rate = density_rate_from_tangent(psi, tangent)
    np.testing.assert_allclose(density_rate, 0.0, rtol=0.0, atol=2e-15)


def test_constant_coefficient_covariant_gradient_obeys_exact_discrete_diffusion():
    n = 40
    h = 2.0 * math.pi / n
    x = np.arange(n) * h
    alpha = 0.4 * np.sin(x) + 0.2 * np.cos(2.0 * x)
    connection = np.zeros(n)
    coefficient = 1.7
    mu = 0.35
    edge_coeff = np.full(n, coefficient)

    q = periodic_covariant_phase_gradient(alpha, connection, h)
    alpha_dot = onsager_phase_velocity_periodic(alpha, connection, edge_coeff, h, mu)
    q_dot_from_phase = (np.roll(alpha_dot, -1) - alpha_dot) / h
    q_dot_diffusion = constant_coefficient_q_velocity(q, coefficient, mu, h)
    np.testing.assert_allclose(q_dot_from_phase, q_dot_diffusion, rtol=0.0, atol=2e-12)

    current = constant_coefficient_current(q, coefficient)
    current_dot_from_q = 2.0 * coefficient * q_dot_from_phase
    current_dot_diffusion = constant_coefficient_current_velocity(current, coefficient, mu, h)
    np.testing.assert_allclose(current_dot_from_q, current_dot_diffusion, rtol=0.0, atol=5e-12)


def _continuum_gradient_error(n):
    length = 2.0 * math.pi
    h = length / n
    x = np.arange(n) * h
    xm = (x + 0.5 * h) % length

    alpha = 0.3 * np.sin(x) + 0.1 * np.cos(2.0 * x)
    connection = 0.15 * np.cos(xm)
    coefficient = 1.2 + 0.2 * np.sin(xm)

    discrete = phase_energy_vertex_derivative_periodic(alpha, connection, coefficient, h) / h

    alpha_x = 0.3 * np.cos(x) - 0.2 * np.sin(2.0 * x)
    alpha_xx = -0.3 * np.sin(x) - 0.4 * np.cos(2.0 * x)
    connection_vertex = 0.15 * np.cos(x)
    connection_x = -0.15 * np.sin(x)
    coefficient_vertex = 1.2 + 0.2 * np.sin(x)
    coefficient_x = 0.2 * np.cos(x)

    q = alpha_x - connection_vertex
    q_x = alpha_xx - connection_x
    exact = -2.0 * (coefficient_x * q + coefficient_vertex * q_x)
    return float(np.sqrt(np.mean((discrete - exact) ** 2)))


def test_functional_gradient_converges_second_order_to_continuum_variation():
    e64 = _continuum_gradient_error(64)
    e128 = _continuum_gradient_error(128)
    e256 = _continuum_gradient_error(256)
    assert e128 < e64 / 3.8
    assert e256 < e128 / 3.8


@pytest.mark.parametrize(
    "call",
    [
        lambda: phase_gradient_energy_periodic([0.0, 1.0], [0.0, 0.0], [1.0, 1.0], 1.0),
        lambda: phase_gradient_energy_periodic([0.0, 1.0, 2.0], [0.0, 0.0, 0.0], [1.0, -1.0, 1.0], 1.0),
        lambda: onsager_phase_velocity_periodic([0.0, 1.0, 2.0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], 1.0, 0.0),
        lambda: periodic_covariant_phase_gradient([0.0, 1.0, 2.0], [0.0, 0.0, 0.0], 0.0),
    ],
)
def test_continuum_phase_onsager_fails_closed(call):
    with pytest.raises(ContinuumPhaseOnsagerError):
        call()
