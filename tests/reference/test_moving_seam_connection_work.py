import math

import numpy as np
import pytest

from idt.moving_seam_connection_work import (
    MovingSeamConnectionError,
    audit_moving_connection,
    connection_phase_gradient,
    connection_work,
    conservative_seam_power,
    moving_seam_balance_rate,
    operator_connection_work,
    seam_stiffness_rate,
    time_dependent_gauge_transform,
)
from idt.schrodinger_onsager_seam_balance import (
    onsager_dissipation,
    schrodinger_seam_power,
    seam_defect_energy,
    seam_stiffness,
)


def _normalized(values):
    psi = np.asarray(values, dtype=complex)
    return psi / np.linalg.norm(psi)


def test_connection_gradient_matches_finite_difference():
    psi = _normalized([1.0 + 0.2j, -0.3 + 0.7j, 0.5 - 0.4j])
    seam = np.array([0.31, -0.47])
    analytic = connection_phase_gradient(psi, seam)
    eps = 1e-7
    numerical = []
    for edge in range(seam.size):
        direction = np.zeros_like(seam)
        direction[edge] = eps
        numerical.append(
            (seam_defect_energy(psi, seam + direction) - seam_defect_energy(psi, seam - direction))
            / (2.0 * eps)
        )
    np.testing.assert_allclose(analytic, numerical, atol=3e-9, rtol=0.0)


def test_connection_work_matches_stiffness_operator_derivative():
    psi = _normalized([0.7 + 0.4j, -0.2 + 0.8j, 0.3 - 0.5j, 0.6 + 0.1j])
    seam = np.array([0.2, -0.8, 0.55])
    rates = np.array([0.4, -0.3, 0.7])
    direct = connection_work(psi, seam, rates)
    operator = operator_connection_work(psi, seam, rates)
    assert math.isclose(direct, operator, rel_tol=0.0, abs_tol=2e-14)


def test_stiffness_rate_matches_finite_difference_of_K():
    seam = np.array([0.13, -0.72, 0.44])
    rates = np.array([0.3, 0.2, -0.5])
    analytic = seam_stiffness_rate(4, seam, rates)
    eps = 1e-7
    numerical = (seam_stiffness(4, seam + eps * rates) - seam_stiffness(4, seam - eps * rates)) / (2.0 * eps)
    np.testing.assert_allclose(analytic, numerical, atol=2e-9, rtol=0.0)
    np.testing.assert_allclose(analytic, analytic.conj().T, atol=1e-15)


def test_total_conservative_power_matches_two_parameter_finite_difference():
    psi = _normalized([1.0, 0.4 + 0.6j, -0.3j])
    seam = np.array([0.21, -0.49])
    rates = np.array([0.7, -0.2])
    h = np.array([[0.4, 0.25, 0.1j], [0.25, -0.3, 0.2], [-0.1j, 0.2, 0.8]], dtype=complex)
    _, _, power = conservative_seam_power(psi, h, seam, rates)

    eig, vec = np.linalg.eigh(h)
    eps = 1e-6
    u_plus = (vec * np.exp(-1j * eig * eps)) @ vec.conj().T
    u_minus = (vec * np.exp(+1j * eig * eps)) @ vec.conj().T
    v_plus = seam_defect_energy(u_plus @ psi, seam + eps * rates)
    v_minus = seam_defect_energy(u_minus @ psi, seam - eps * rates)
    numerical = (v_plus - v_minus) / (2.0 * eps)
    assert math.isclose(power, numerical, rel_tol=0.0, abs_tol=3e-10)


def test_time_dependent_gauge_mixes_split_powers_but_preserves_their_sum():
    psi = _normalized([1.0 + 0.1j, -0.2 + 0.9j, 0.5 - 0.3j, 0.4j])
    seam = np.array([0.25, -0.4, 0.73])
    seam_rates = np.array([0.3, -0.6, 0.2])
    h = np.array(
        [
            [0.2, 0.3, 0.0, 0.1j],
            [0.3, -0.5, 0.2j, 0.0],
            [0.0, -0.2j, 0.7, 0.25],
            [-0.1j, 0.0, 0.25, 0.1],
        ],
        dtype=complex,
    )
    chi = np.array([0.7, -0.3, 0.4, 1.0])
    chi_rates = np.array([0.2, -0.5, 0.9, -0.1])

    p_s, p_c, total = conservative_seam_power(psi, h, seam, seam_rates)
    psi_p, h_p, seam_p, rates_p = time_dependent_gauge_transform(
        psi, h, seam, seam_rates, chi, chi_rates
    )
    p_s_p, p_c_p, total_p = conservative_seam_power(psi_p, h_p, seam_p, rates_p)

    assert abs(p_s_p - p_s) > 1e-5
    assert abs(p_c_p - p_c) > 1e-5
    assert math.isclose(total_p, total, rel_tol=0.0, abs_tol=3e-14)
    assert math.isclose(
        seam_defect_energy(psi, seam),
        seam_defect_energy(psi_p, seam_p),
        rel_tol=0.0,
        abs_tol=2e-14,
    )


def test_full_moving_balance_is_time_dependent_gauge_invariant():
    psi = _normalized([0.8 + 0.2j, 0.1 + 0.9j, -0.4 + 0.3j])
    seam = np.array([0.12, -0.65])
    rates = np.array([0.45, -0.15])
    h = np.array([[0.5, 0.2, 0.15j], [0.2, -0.1, 0.3], [-0.15j, 0.3, 0.6]], dtype=complex)
    chi = np.array([0.2, -0.7, 0.9])
    chi_rates = np.array([0.4, -0.2, 0.5])

    original = moving_seam_balance_rate(psi, h, seam, rates, 1.3)
    psi_p, h_p, seam_p, rates_p = time_dependent_gauge_transform(
        psi, h, seam, rates, chi, chi_rates
    )
    transformed = moving_seam_balance_rate(psi_p, h_p, seam_p, rates_p, 1.3)

    assert math.isclose(original[2], transformed[2], rel_tol=0.0, abs_tol=2e-14)
    assert math.isclose(original[3], transformed[3], rel_tol=0.0, abs_tol=3e-14)


def test_zero_connection_rate_reduces_to_fixed_connection_balance():
    psi = _normalized([1.0, 0.5j, -0.2 + 0.4j])
    seam = np.array([0.3, -0.1])
    h = np.diag([0.7, -0.2, 0.4])
    p_s, p_c, diss, full = moving_seam_balance_rate(psi, h, seam, [0.0, 0.0], 0.8)
    assert p_c == 0.0
    assert math.isclose(p_s, schrodinger_seam_power(psi, h, seam), abs_tol=1e-15)
    assert math.isclose(diss, onsager_dissipation(psi, seam, 0.8), abs_tol=1e-15)
    assert math.isclose(full, p_s - diss, abs_tol=1e-15)


def test_connection_work_can_have_both_signs():
    psi = _normalized([1.0, 1j])
    seam = [0.0]
    positive = connection_work(psi, seam, [-1.0])
    negative = connection_work(psi, seam, [1.0])
    assert positive > 0.0
    assert negative < 0.0
    assert math.isclose(positive, -negative, rel_tol=0.0, abs_tol=1e-15)


def test_audit_reports_operator_identity():
    psi = _normalized([1.0, 0.3 + 0.2j, -0.4j])
    seam = [0.1, -0.2]
    rates = [0.3, 0.4]
    h = np.diag([0.2, -0.3, 0.9])
    audit = audit_moving_connection(psi, h, seam, rates, 1.1)
    assert audit.operator_connection_residual < 2e-14
    assert math.isclose(
        audit.full_balance_rate,
        audit.schrodinger_power + audit.connection_work - audit.onsager_dissipation,
        abs_tol=1e-15,
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: connection_phase_gradient([1.0, 0.0], []),
        lambda: connection_work([1.0, 1.0], [0.0], []),
        lambda: seam_stiffness_rate(0, [], []),
        lambda: seam_stiffness_rate(2, [0.0], [float("nan")]),
        lambda: conservative_seam_power([1.0, 1.0], [[0.0, 1.0], [0.0, 0.0]], [0.0], [0.0]),
        lambda: time_dependent_gauge_transform([1.0, 1.0], np.eye(2), [0.0], [0.0], [0.0], [0.0, 0.0]),
    ],
)
def test_moving_connection_gate_fails_closed(call):
    with pytest.raises((MovingSeamConnectionError, SchrodingerOnsagerBalanceError)):
        call()
