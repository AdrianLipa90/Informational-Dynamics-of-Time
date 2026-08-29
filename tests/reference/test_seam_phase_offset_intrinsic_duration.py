import math

import numpy as np
import pytest

from idt.seam_phase_offset_intrinsic_duration import (
    KAPPA,
    SeamPhaseOffsetDurationError,
    audit_temporal_offset_map,
    calibrated_coordinate_offset,
    calibrated_proper_offset,
    constant_reference_phase_offset,
    intrinsic_duration_offset,
    intrinsic_information_rate,
    intrinsic_offset_rate,
    intrinsic_offset_rate_from_information,
    reference_phase_period,
    winding_offset_control,
)
from idt.temporal_seam_curvature_response import (
    temporal_gauge_transform,
    temporal_seam_curvature,
)


def test_offset_rate_is_curvature_over_reference_phase_rate():
    f = np.array([0.4, -0.2, 0.8])
    np.testing.assert_allclose(intrinsic_offset_rate(f, 2.0), [0.2, -0.1, 0.4], atol=1e-15)


def test_phase_clock_identity_control_recovers_intrinsic_interval():
    curvature = np.array([[2.0], [3.0], [4.0]])
    omega = np.array([2.0, 3.0, 4.0])
    dtheta = np.array([0.2, 0.4, 0.3])
    offset = intrinsic_duration_offset(curvature, omega, dtheta)
    assert math.isclose(float(offset[0]), float(np.sum(dtheta)), rel_tol=0.0, abs_tol=1e-15)


def test_constant_reference_reduces_to_accumulated_phase_divided_by_rate():
    curvature = np.array([[0.4, -0.2], [0.1, 0.5], [-0.3, 0.2]])
    dtheta = np.array([0.5, 0.25, 0.75])
    omega = 1.7
    delta_phi = np.sum(curvature * dtheta[:, None], axis=0)
    integrated = intrinsic_duration_offset(curvature, [omega] * 3, dtheta)
    closed = constant_reference_phase_offset(delta_phi, omega)
    np.testing.assert_allclose(integrated, closed, atol=1e-15, rtol=0.0)


def test_intrinsic_offset_is_additive_and_signed():
    curvature = np.array([[0.2, -0.1], [0.4, 0.3], [-0.2, 0.5]])
    omega = np.array([1.0, 1.5, 0.8])
    dtheta = np.array([0.5, 0.25, 0.75])
    full = intrinsic_duration_offset(curvature, omega, dtheta)
    left = intrinsic_duration_offset(curvature[:2], omega[:2], dtheta[:2])
    right = intrinsic_duration_offset(curvature[2:], omega[2:], dtheta[2:])
    np.testing.assert_allclose(full, left + right, atol=1e-15, rtol=0.0)
    np.testing.assert_allclose(
        intrinsic_duration_offset(-curvature, omega, dtheta),
        -full,
        atol=1e-15,
        rtol=0.0,
    )


def test_time_dependent_gauge_reexpression_preserves_intrinsic_offset_rate():
    psi = np.array([1.0 + 0.2j, -0.3 + 0.7j, 0.4 - 0.1j], dtype=complex)
    psi /= np.linalg.norm(psi)
    h = np.array([[0.4, 0.2, 0.1j], [0.2, -0.3, 0.25], [-0.1j, 0.25, 0.8]], dtype=complex)
    seam = np.array([0.2, -0.5])
    seam_rate = np.array([0.4, -0.1])
    a0 = np.array([0.3, -0.2, 0.6])
    chi = np.array([0.7, -0.4, 0.9])
    chi_rate = np.array([0.2, -0.6, 0.5])
    omega_ref = 2.3

    f = temporal_seam_curvature(seam_rate, a0)
    _, _, _, seam_rate_p, a0_p = temporal_gauge_transform(
        psi, h, seam, seam_rate, a0, chi, chi_rate
    )
    f_p = temporal_seam_curvature(seam_rate_p, a0_p)
    np.testing.assert_allclose(
        intrinsic_offset_rate(f, omega_ref),
        intrinsic_offset_rate(f_p, omega_ref),
        atol=2e-15,
        rtol=0.0,
    )


def test_information_rate_form_is_exactly_the_same_offset_coordinate():
    f = np.array([0.7, -0.4, 0.2])
    omega = 3.1
    gamma = intrinsic_information_rate(omega)
    direct = intrinsic_offset_rate(f, omega)
    via_information = intrinsic_offset_rate_from_information(f, gamma)
    np.testing.assert_allclose(via_information, direct, atol=2e-15, rtol=0.0)
    assert math.isclose(gamma, KAPPA * omega, rel_tol=0.0, abs_tol=1e-15)


def test_calibration_and_lapse_compose_after_intrinsic_offset():
    curvature = np.array([[0.6, -0.2], [0.4, 0.5]])
    omega = np.array([2.0, 4.0])
    scale = np.array([3.0, 5.0])
    lapse = np.array([0.8, 1.2])
    dtheta = np.array([0.25, 0.5])

    coordinate = calibrated_coordinate_offset(curvature, omega, scale, dtheta)
    proper = calibrated_proper_offset(curvature, omega, scale, lapse, dtheta)
    expected_coordinate = np.sum(curvature * (scale * dtheta / omega)[:, None], axis=0)
    expected_proper = np.sum(curvature * (lapse * scale * dtheta / omega)[:, None], axis=0)
    np.testing.assert_allclose(coordinate, expected_coordinate, atol=1e-15, rtol=0.0)
    np.testing.assert_allclose(proper, expected_proper, atol=1e-15, rtol=0.0)


def test_winding_control_is_integer_number_of_reference_phase_periods():
    omega = 5.0
    period = reference_phase_period(omega)
    for winding in (-3, -1, 0, 1, 4):
        assert math.isclose(
            winding_offset_control(winding, omega),
            winding * period,
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_audit_information_identity_residual_is_zero_to_machine_precision():
    audit = audit_temporal_offset_map(
        [[0.2, -0.1], [0.4, 0.3]],
        [1.2, 1.7],
        [2.0, 2.5],
        [0.9, 1.1],
        [0.3, 0.4],
    )
    assert audit.information_identity_residual < 2e-16


@pytest.mark.parametrize(
    "call",
    [
        lambda: intrinsic_offset_rate([0.2], 0.0),
        lambda: intrinsic_duration_offset([[0.2]], [-1.0], [0.1]),
        lambda: intrinsic_duration_offset([[0.2]], [1.0], [0.0]),
        lambda: intrinsic_duration_offset([[0.2], [0.3]], [1.0], [0.1, 0.2]),
        lambda: calibrated_coordinate_offset([[0.2]], [1.0], [0.0], [0.1]),
        lambda: calibrated_proper_offset([[0.2]], [1.0], [1.0], [0.0], [0.1]),
        lambda: intrinsic_information_rate(1.0, kappa=0.0),
        lambda: intrinsic_offset_rate_from_information([0.2], 0.0),
        lambda: winding_offset_control(1.5, 1.0),
    ],
)
def test_phase_offset_duration_gate_fails_closed(call):
    with pytest.raises(SeamPhaseOffsetDurationError):
        call()
