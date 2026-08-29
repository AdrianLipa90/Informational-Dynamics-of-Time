import math

import numpy as np
import pytest

from idt.moving_seam_connection_work import (
    connection_phase_gradient,
    conservative_seam_power,
)
from idt.schrodinger_onsager_seam_balance import onsager_dissipation
from idt.temporal_seam_curvature_response import (
    TemporalSeamCurvatureError,
    accumulated_curvature_offset,
    audit_curvature_response,
    covariant_hamiltonian,
    covariant_schrodinger_power,
    curvature_dissipation,
    curvature_power,
    curvature_response,
    curvature_response_balance_rate,
    edge_gradient,
    gauge_native_geometric_power,
    seam_rates_from_curvature_response,
    temporal_gauge_transform,
    temporal_seam_curvature,
)


def _normalized(values):
    psi = np.asarray(values, dtype=complex)
    return psi / np.linalg.norm(psi)


def test_temporal_seam_curvature_is_time_dependent_gauge_invariant():
    psi = _normalized([1.0 + 0.2j, -0.3 + 0.7j, 0.4 - 0.1j])
    h = np.array([[0.4, 0.2, 0.1j], [0.2, -0.3, 0.25], [-0.1j, 0.25, 0.8]], dtype=complex)
    seam = np.array([0.2, -0.5])
    omega = np.array([0.4, -0.1])
    a0 = np.array([0.3, -0.2, 0.6])
    chi = np.array([0.7, -0.4, 0.9])
    chi_rate = np.array([0.2, -0.6, 0.5])

    e = temporal_seam_curvature(omega, a0)
    _, _, seam_p, omega_p, a0_p = temporal_gauge_transform(
        psi, h, seam, omega, a0, chi, chi_rate
    )
    e_p = temporal_seam_curvature(omega_p, a0_p)
    np.testing.assert_allclose(e_p, e, atol=1e-15, rtol=0.0)
    np.testing.assert_allclose(seam_p, seam + np.diff(chi), atol=1e-15, rtol=0.0)


def test_covariant_hamiltonian_transforms_by_similarity_only():
    psi = _normalized([1.0, 0.4j, -0.2 + 0.5j])
    h = np.array([[0.2, 0.3, 0.1j], [0.3, -0.4, 0.2], [-0.1j, 0.2, 0.7]], dtype=complex)
    seam = np.array([0.1, -0.2])
    omega = np.array([0.3, 0.6])
    a0 = np.array([0.5, -0.1, 0.2])
    chi = np.array([0.2, -0.8, 1.1])
    chi_rate = np.array([0.4, -0.3, 0.7])

    hbar = covariant_hamiltonian(h, a0)
    psi_p, h_p, _, _, a0_p = temporal_gauge_transform(
        psi, h, seam, omega, a0, chi, chi_rate
    )
    hbar_p = covariant_hamiltonian(h_p, a0_p)
    u = np.diag(np.exp(1j * chi))
    np.testing.assert_allclose(hbar_p, u @ hbar @ u.conj().T, atol=2e-14, rtol=0.0)
    np.testing.assert_allclose(psi_p, u @ psi, atol=1e-15, rtol=0.0)


def test_gauge_native_geometric_power_equals_moving_connection_split():
    psi = _normalized([1.0 + 0.1j, -0.3 + 0.8j, 0.5 - 0.2j, 0.4j])
    h = np.array(
        [
            [0.3, 0.2, 0.0, 0.1j],
            [0.2, -0.5, 0.25j, 0.0],
            [0.0, -0.25j, 0.9, 0.2],
            [-0.1j, 0.0, 0.2, 0.1],
        ],
        dtype=complex,
    )
    seam = np.array([0.17, -0.42, 0.61])
    omega = np.array([0.4, -0.2, 0.5])
    a0 = np.array([0.3, -0.1, 0.6, -0.2])

    _, _, moving = conservative_seam_power(psi, h, seam, omega)
    native = gauge_native_geometric_power(psi, h, seam, omega, a0)
    assert math.isclose(native, moving, rel_tol=0.0, abs_tol=3e-14)


def test_temporal_connection_diagonal_identity_matches_edge_gradient_work():
    psi = _normalized([0.8 + 0.2j, 0.1 + 0.9j, -0.4 + 0.3j])
    h = np.diag([0.5, -0.2, 0.7])
    seam = np.array([0.12, -0.65])
    a0 = np.array([0.4, -0.3, 0.8])
    omega = np.zeros(2)

    p_full = conservative_seam_power(psi, h, seam, omega)[2]
    p_cov = covariant_schrodinger_power(psi, h, seam, a0)
    q = connection_phase_gradient(psi, seam)
    expected = p_cov + float(q @ np.diff(a0))
    assert math.isclose(p_full, expected, rel_tol=0.0, abs_tol=2e-14)


def test_curvature_response_is_gauge_invariant_and_selects_seam_rate_covariantly():
    psi = _normalized([1.0, 0.3 + 0.7j, -0.2 + 0.4j])
    h = np.array([[0.4, 0.2, 0.0], [0.2, -0.1, 0.3j], [0.0, -0.3j, 0.8]], dtype=complex)
    seam = np.array([0.25, -0.33])
    a0 = np.array([0.2, -0.4, 0.5])
    chi = np.array([0.6, -0.2, 0.9])
    chi_rate = np.array([0.3, -0.5, 0.7])
    g = np.array([[1.2, 0.2], [0.2, 0.8]])

    e = curvature_response(psi, seam, g)
    omega = seam_rates_from_curvature_response(psi, seam, a0, g)
    psi_p, _, seam_p, _, a0_p = temporal_gauge_transform(
        psi, h, seam, omega, a0, chi, chi_rate
    )
    e_p = curvature_response(psi_p, seam_p, g)
    omega_p = seam_rates_from_curvature_response(psi_p, seam_p, a0_p, g)

    np.testing.assert_allclose(e_p, e, atol=2e-14, rtol=0.0)
    np.testing.assert_allclose(omega_p, omega + np.diff(chi_rate), atol=2e-14, rtol=0.0)
    np.testing.assert_allclose(temporal_seam_curvature(omega, a0), e, atol=2e-14, rtol=0.0)


def test_curvature_response_gives_nonnegative_dissipation_and_negative_curvature_work():
    psi = _normalized([1.0, 1j, 0.2 - 0.5j])
    seam = np.array([0.0, 0.4])
    g = np.array([[1.4, 0.1], [0.1, 0.9]])
    q = connection_phase_gradient(psi, seam)
    e = curvature_response(psi, seam, g)
    diss = curvature_dissipation(psi, seam, g)
    assert diss >= 0.0
    assert math.isclose(float(q @ e), -diss, rel_tol=0.0, abs_tol=2e-14)


def test_full_curvature_response_balance_matches_original_moving_balance():
    psi = _normalized([1.0 + 0.2j, 0.1 + 0.8j, -0.3 + 0.4j, 0.5 - 0.1j])
    h = np.array(
        [
            [0.2, 0.3, 0.0, 0.1j],
            [0.3, -0.4, 0.2j, 0.0],
            [0.0, -0.2j, 0.8, 0.25],
            [-0.1j, 0.0, 0.25, 0.5],
        ],
        dtype=complex,
    )
    seam = np.array([0.2, -0.3, 0.7])
    a0 = np.array([0.4, -0.1, 0.3, -0.2])
    g_curv = np.array([[1.0, 0.1, 0.0], [0.1, 1.3, 0.2], [0.0, 0.2, 0.8]])
    g_vertex = 1.1

    audit = audit_curvature_response(psi, h, seam, a0, g_curv, g_vertex)
    assert audit.curvature_dissipation >= 0.0
    assert audit.vertex_phase_dissipation >= 0.0
    assert audit.curvature_power <= 1e-14
    assert audit.decomposition_residual < 4e-14

    p_cov, d_curv, d_vertex, rate = curvature_response_balance_rate(
        psi, h, seam, a0, g_curv, g_vertex
    )
    assert math.isclose(rate, p_cov - d_curv - d_vertex, abs_tol=1e-15)


def test_full_response_balance_is_time_dependent_gauge_invariant():
    psi = _normalized([0.9 + 0.1j, -0.2 + 0.7j, 0.4 - 0.5j])
    h = np.array([[0.5, 0.2, 0.1j], [0.2, -0.2, 0.3], [-0.1j, 0.3, 0.9]], dtype=complex)
    seam = np.array([0.14, -0.52])
    a0 = np.array([0.3, -0.4, 0.6])
    chi = np.array([0.2, -0.9, 0.5])
    chi_rate = np.array([0.4, -0.1, 0.7])
    g_curv = np.array([[1.1, 0.2], [0.2, 0.9]])

    omega = seam_rates_from_curvature_response(psi, seam, a0, g_curv)
    original = gauge_native_geometric_power(psi, h, seam, omega, a0)
    psi_p, h_p, seam_p, omega_p, a0_p = temporal_gauge_transform(
        psi, h, seam, omega, a0, chi, chi_rate
    )
    transformed = gauge_native_geometric_power(psi_p, h_p, seam_p, omega_p, a0_p)
    assert math.isclose(original, transformed, rel_tol=0.0, abs_tol=3e-14)
    assert math.isclose(
        curvature_dissipation(psi, seam, g_curv),
        curvature_dissipation(psi_p, seam_p, g_curv),
        rel_tol=0.0,
        abs_tol=2e-14,
    )
    assert math.isclose(
        onsager_dissipation(psi, seam, 0.8),
        onsager_dissipation(psi_p, seam_p, 0.8),
        rel_tol=0.0,
        abs_tol=2e-14,
    )


def test_accumulated_curvature_offset_is_additive_and_parameter_free_in_theta():
    e = np.array([[0.2, -0.1], [0.4, 0.3], [-0.2, 0.5]])
    dtheta = np.array([0.5, 0.25, 0.75])
    full = accumulated_curvature_offset(e, dtheta)
    left = accumulated_curvature_offset(e[:2], dtheta[:2])
    right = accumulated_curvature_offset(e[2:], dtheta[2:])
    np.testing.assert_allclose(full, left + right, atol=1e-15, rtol=0.0)


def test_edge_gradient_matches_declared_orientation():
    np.testing.assert_allclose(edge_gradient([0.2, -0.1, 0.7]), [-0.3, 0.8], atol=1e-15)


@pytest.mark.parametrize(
    "call",
    [
        lambda: temporal_seam_curvature([], []),
        lambda: temporal_seam_curvature([], [0.0, 1.0]),
        lambda: covariant_hamiltonian([[0.0, 1.0], [0.0, 0.0]], [0.0, 0.0]),
        lambda: curvature_response([1.0, 1.0], [0.0], -1.0),
        lambda: curvature_response([1.0, 1.0], [0.0], [[1.0]]),
        lambda: accumulated_curvature_offset([[0.2], [0.3]], [0.1, -0.2]),
    ],
)
def test_temporal_seam_curvature_gate_fails_closed(call):
    with pytest.raises((TemporalSeamCurvatureError, MovingSeamConnectionError, SchrodingerOnsagerBalanceError)):
        call()
