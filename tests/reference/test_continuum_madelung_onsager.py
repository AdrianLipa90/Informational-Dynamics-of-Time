import math

import numpy as np
import pytest

from idt.continuum_madelung_onsager import (
    ContinuumMadelungOnsagerError,
    characteristic_residual,
    combined_madelung_rates,
    compact_phase_balance_residual,
    constant_m_velocity,
    constant_m_velocity_rate,
    covariant_phase_gradient,
    gauge_reexpress_phase_gradient,
    linearized_characteristic_coefficients,
    linearized_mode_roots,
    temporal_current,
)


def test_combined_phase_balance_closes_exactly_on_density_flux():
    r = np.array([1.2, 0.9, 1.1, 1.3])
    m = np.array([0.8, 1.0, 1.2, 0.7])
    q = np.array([0.2, -0.1, 0.35, -0.25])
    v = np.array([0.05, -0.02, 0.1, 0.0])
    d_mrx = np.array([0.3, -0.2, 0.15, 0.05])
    d_mrhoq = np.array([-0.4, 0.25, -0.1, 0.3])
    mu = 0.6

    rates = combined_madelung_rates(r, m, q, v, d_mrx, d_mrhoq, mu)
    np.testing.assert_allclose(rates.density_rate, -2.0 * d_mrhoq, rtol=0.0, atol=0.0)
    np.testing.assert_allclose(rates.onsager_phase_rate, -mu * rates.density_rate, rtol=0.0, atol=0.0)
    residual = compact_phase_balance_residual(
        rates.combined_phase_rate,
        rates.density_rate,
        rates.schrodinger_phase_rate,
        mu,
    )
    np.testing.assert_allclose(residual, 0.0, rtol=0.0, atol=2e-16)


def test_current_and_velocity_use_the_same_covariant_gradient():
    rho = np.array([1.0, 1.5, 0.7, 2.0])
    q = np.array([0.2, -0.3, 0.1, 0.4])
    m_scalar = 1.7
    current = temporal_current(np.full(rho.size, m_scalar), rho, q)
    velocity = constant_m_velocity(m_scalar, q)
    np.testing.assert_allclose(current, rho * velocity, rtol=0.0, atol=1e-15)


def test_spatial_gauge_reexpression_leaves_q_and_current_invariant():
    alpha_x = np.array([0.4, -0.2, 0.1, 0.7])
    connection = np.array([0.1, 0.05, -0.2, 0.3])
    chi_x = np.array([-0.3, 0.4, 0.2, -0.1])
    transformed_alpha_x, transformed_connection = gauge_reexpress_phase_gradient(alpha_x, connection, chi_x)
    q0 = covariant_phase_gradient(alpha_x, connection)
    q1 = covariant_phase_gradient(transformed_alpha_x, transformed_connection)
    np.testing.assert_allclose(q1, q0, rtol=0.0, atol=1e-15)

    rho = np.array([1.1, 0.8, 1.4, 0.9])
    mobility = np.array([0.7, 1.0, 1.3, 0.9])
    np.testing.assert_allclose(
        temporal_current(mobility, rho, q1),
        temporal_current(mobility, rho, q0),
        rtol=0.0,
        atol=2e-15,
    )


def test_constant_m_velocity_balance_matches_declared_terms():
    u = np.array([0.2, -0.1, 0.4])
    u_x = np.array([0.3, 0.1, -0.2])
    quantum_x = np.array([0.5, -0.4, 0.2])
    potential_x = np.array([0.1, 0.2, -0.05])
    rho_u_xx = np.array([-0.2, 0.3, 0.1])
    m = 1.4
    mu = 0.25
    rate = constant_m_velocity_rate(u, u_x, quantum_x, potential_x, rho_u_xx, m, mu)
    expected = -u * u_x + 2.0 * m**2 * quantum_x - 2.0 * m * potential_x + 2.0 * mu * m * rho_u_xx
    np.testing.assert_allclose(rate, expected, rtol=0.0, atol=2e-15)


def test_undamped_linear_modes_recover_quadratic_schrodinger_dispersion():
    k = 1.75
    m = 0.8
    roots = linearized_mode_roots(k, m, background_density=2.0, onsager_mobility=0.0)
    expected = m * k * k
    assert math.isclose(roots[0].real, 0.0, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(roots[1].real, 0.0, rel_tol=0.0, abs_tol=1e-15)
    assert sorted([round(root.imag, 14) for root in roots]) == sorted([round(expected, 14), round(-expected, 14)])


def test_positive_onsager_mobility_gives_nonpositive_linear_mode_growth_rates():
    for mu in (0.05, 0.5, 1.5, 4.0):
        roots = linearized_mode_roots(2.2, mobility=1.1, background_density=0.9, onsager_mobility=mu)
        for root in roots:
            assert root.real <= 1e-14


def test_linear_mode_roots_satisfy_characteristic_polynomial_exactly_to_roundoff():
    coefficients = linearized_characteristic_coefficients(1.3, mobility=0.75, background_density=1.4, onsager_mobility=0.6)
    roots = linearized_mode_roots(1.3, mobility=0.75, background_density=1.4, onsager_mobility=0.6)
    for root in roots:
        assert abs(characteristic_residual(root, coefficients)) < 2e-15


def test_zero_wave_number_has_double_neutral_linear_mode():
    roots = linearized_mode_roots(0.0, mobility=1.0, background_density=1.0, onsager_mobility=0.7)
    assert roots == (0j, 0j)


@pytest.mark.parametrize(
    "call",
    [
        lambda: combined_madelung_rates([1.0, 0.0], [1.0, 1.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], 0.1),
        lambda: temporal_current([1.0, -1.0], [1.0, 1.0], [0.0, 0.0]),
        lambda: linearized_mode_roots(1.0, mobility=0.0, background_density=1.0, onsager_mobility=0.1),
        lambda: linearized_mode_roots(1.0, mobility=1.0, background_density=0.0, onsager_mobility=0.1),
        lambda: linearized_mode_roots(1.0, mobility=1.0, background_density=1.0, onsager_mobility=-0.1),
    ],
)
def test_madelung_onsager_fails_closed(call):
    with pytest.raises(ContinuumMadelungOnsagerError):
        call()
