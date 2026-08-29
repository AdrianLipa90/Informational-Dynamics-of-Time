import math

import numpy as np
import pytest

from idt.temporal_offset_reference_clock_cocycle import (
    TemporalOffsetReferenceClockError,
    accumulated_offset_from_rate,
    audit_reference_clock_change,
    calibrated_reference_factor,
    compose_reference_factors,
    information_rate_from_phase_rate,
    information_reference_change_factor,
    neutral_curvature_rate,
    pointwise_reference_change,
    reference_change_factor,
    transform_offset_rate,
    winding_locked_reference_factor,
)


def test_reference_change_identity_inverse_and_cocycle_are_exact():
    omega_r, omega_s, omega_t = 2.0, 5.0, 7.5
    assert reference_change_factor(omega_r, omega_r) == 1.0
    crs = reference_change_factor(omega_r, omega_s)
    csr = reference_change_factor(omega_s, omega_r)
    assert math.isclose(crs * csr, 1.0, rel_tol=0.0, abs_tol=1e-15)
    direct, composed = compose_reference_factors(omega_r, omega_s, omega_t)
    assert math.isclose(direct, composed, rel_tol=0.0, abs_tol=1e-15)


def test_direct_target_offset_rate_matches_transformed_source_rate():
    curvature = np.array([0.6, -0.3, 1.2])
    omega_r, omega_s = 2.5, 4.0
    eta_r = curvature / omega_r
    eta_s_direct = curvature / omega_s
    eta_s_transformed = transform_offset_rate(eta_r, omega_r, omega_s)
    np.testing.assert_allclose(eta_s_transformed, eta_s_direct, atol=1e-15, rtol=0.0)


def test_reference_neutral_curvature_carrier_is_preserved():
    curvature = np.array([0.2, -0.4, 0.7])
    omega_r, omega_s = 1.7, 3.4
    eta_r = curvature / omega_r
    eta_s = curvature / omega_s
    np.testing.assert_allclose(neutral_curvature_rate(eta_r, omega_r), curvature, atol=1e-15, rtol=0.0)
    np.testing.assert_allclose(neutral_curvature_rate(eta_s, omega_s), curvature, atol=1e-15, rtol=0.0)


def test_variable_reference_change_matches_direct_target_integration():
    curvature = np.array([[0.2, -0.1], [0.5, 0.3], [-0.4, 0.8]])
    omega_r = np.array([1.0, 2.0, 4.0])
    omega_s = np.array([2.0, 1.5, 5.0])
    dtheta = np.array([0.4, 0.25, 0.6])

    eta_r = curvature / omega_r[:, None]
    eta_s_transformed = pointwise_reference_change(eta_r, omega_r, omega_s)
    eta_s_direct = curvature / omega_s[:, None]
    np.testing.assert_allclose(eta_s_transformed, eta_s_direct, atol=1e-15, rtol=0.0)
    np.testing.assert_allclose(
        accumulated_offset_from_rate(eta_s_transformed, dtheta),
        accumulated_offset_from_rate(eta_s_direct, dtheta),
        atol=1e-15,
        rtol=0.0,
    )


def test_information_rate_reference_factor_equals_phase_rate_factor():
    omega_r, omega_s = 2.3, 5.1
    gamma_r = information_rate_from_phase_rate(omega_r)
    gamma_s = information_rate_from_phase_rate(omega_s)
    assert math.isclose(
        information_reference_change_factor(gamma_r, gamma_s),
        reference_change_factor(omega_r, omega_s),
        rel_tol=0.0,
        abs_tol=1e-15,
    )


def test_winding_locked_reference_factor_matches_locked_phase_rate_ratio():
    m_r, m_s = 3, 5
    assert winding_locked_reference_factor(m_r, m_s) == m_r / m_s
    omega_base = 1.7
    omega_r = m_r * omega_base
    omega_s = m_s * omega_base
    assert math.isclose(
        reference_change_factor(omega_r, omega_s),
        winding_locked_reference_factor(m_r, m_s),
        rel_tol=0.0,
        abs_tol=1e-15,
    )


def test_calibrated_reference_factor_is_exact_composition():
    omega_r, omega_s = 2.0, 5.0
    t_r, t_s = 3.0, 7.0
    factor = calibrated_reference_factor(omega_r, omega_s, t_r, t_s)
    assert math.isclose(factor, (t_s / t_r) * (omega_r / omega_s), rel_tol=0.0, abs_tol=1e-15)


def test_zero_curvature_stays_zero_in_every_reference():
    eta_r = np.zeros(4)
    eta_s = transform_offset_rate(eta_r, 2.0, 9.0)
    np.testing.assert_allclose(eta_s, np.zeros(4), atol=0.0, rtol=0.0)
    np.testing.assert_allclose(neutral_curvature_rate(eta_s, 9.0), np.zeros(4), atol=0.0, rtol=0.0)


def test_reference_change_audit_closes_both_residuals():
    audit = audit_reference_clock_change([0.3, -0.8, 0.4], 1.9, 4.6)
    assert audit.max_rate_residual < 2e-16
    assert audit.max_neutral_residual < 2e-16


@pytest.mark.parametrize(
    "call",
    [
        lambda: reference_change_factor(0.0, 1.0),
        lambda: reference_change_factor(1.0, -1.0),
        lambda: transform_offset_rate([[0.2]], 1.0, 2.0),
        lambda: pointwise_reference_change([[0.2], [0.3]], [1.0], [2.0, 3.0]),
        lambda: pointwise_reference_change([[0.2]], [0.0], [2.0]),
        lambda: accumulated_offset_from_rate([[0.2]], [0.0]),
        lambda: information_rate_from_phase_rate(1.0, kappa=0.0),
        lambda: information_reference_change_factor(0.0, 1.0),
        lambda: winding_locked_reference_factor(0, 1),
        lambda: winding_locked_reference_factor(1, -2),
        lambda: calibrated_reference_factor(1.0, 2.0, 0.0, 1.0),
    ],
)
def test_reference_clock_cocycle_gate_fails_closed(call):
    with pytest.raises(TemporalOffsetReferenceClockError):
        call()
