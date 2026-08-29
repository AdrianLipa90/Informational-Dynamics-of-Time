import math

import numpy as np
import pytest

from idt.phase_aware_half_seam import phase_aware_seam_defects
from idt.schrodinger_onsager_seam_balance import (
    SchrodingerOnsagerBalanceError,
    audit_seam_balance,
    combined_state_velocity,
    commutator_frobenius,
    norm_directional_rate,
    onsager_dissipation,
    onsager_state_velocity,
    schrodinger_seam_power,
    seam_balance_rate,
    seam_covariant_incidence,
    seam_defect_energy,
    seam_energy_directional_rate,
    seam_phase_gradient,
    seam_stiffness,
)
from idt.zeta_collatz_temporal_fuzziness import (
    build_prime_frames,
    unitary_propagator,
    zeta_collatz_hamiltonian,
)


def _normalized(values):
    psi = np.asarray(values, dtype=complex)
    return psi / np.linalg.norm(psi)


def test_covariant_stiffness_is_hermitian_psd_and_matches_direct_defects():
    psi = _normalized([1.0 + 0.2j, -0.3 + 0.8j, 0.5 - 0.4j, 0.7 + 0.1j])
    seam = np.array([0.2, -0.7, 1.1])
    c = seam_covariant_incidence(4, seam)
    k = seam_stiffness(4, seam)
    np.testing.assert_allclose(k, 0.25 * c.conj().T @ c, atol=1e-15)
    np.testing.assert_allclose(k, k.conj().T, atol=1e-15)
    assert np.min(np.linalg.eigvalsh(k)) >= -1e-13
    direct = float(np.vdot(phase_aware_seam_defects(psi, seam), phase_aware_seam_defects(psi, seam)).real)
    assert math.isclose(seam_defect_energy(psi, seam), direct, rel_tol=0.0, abs_tol=1e-14)


def test_vertex_phase_gradient_matches_finite_difference_without_arg_extraction():
    psi = _normalized([0.9 + 0.3j, 0.4 - 0.8j, -0.5 + 0.7j])
    seam = np.array([0.35, -0.61])
    analytic = seam_phase_gradient(psi, seam)
    eps = 1e-7
    numerical = []
    for vertex in range(psi.size):
        mask = np.zeros(psi.size)
        mask[vertex] = 1.0
        plus = np.exp(1j * eps * mask) * psi
        minus = np.exp(-1j * eps * mask) * psi
        numerical.append((seam_defect_energy(plus, seam) - seam_defect_energy(minus, seam)) / (2.0 * eps))
    np.testing.assert_allclose(analytic, numerical, atol=3e-9, rtol=0.0)
    assert abs(float(np.sum(analytic))) < 1e-14


def test_schrodinger_commutator_power_matches_exact_unitary_finite_difference():
    psi = _normalized([1.0, 1j, 0.4 - 0.2j])
    seam = np.array([0.17, -0.43])
    h = np.array(
        [
            [0.7, 0.2 + 0.1j, -0.3j],
            [0.2 - 0.1j, -0.4, 0.15],
            [0.3j, 0.15, 0.9],
        ],
        dtype=complex,
    )
    exact = schrodinger_seam_power(psi, h, seam)
    eps = 1e-6
    plus = unitary_propagator(h, eps) @ psi
    minus = unitary_propagator(h, -eps) @ psi
    numerical = (seam_defect_energy(plus, seam) - seam_defect_energy(minus, seam)) / (2.0 * eps)
    assert math.isclose(exact, numerical, rel_tol=0.0, abs_tol=2e-10)


def test_onsager_phase_flow_preserves_norm_and_dissipates_exactly():
    psi = _normalized([0.8 + 0.1j, 0.2 + 0.7j, -0.4 + 0.6j])
    seam = np.array([0.2, -0.5])
    g = np.array([[1.4, 0.2, 0.0], [0.2, 1.0, 0.1], [0.0, 0.1, 0.8]])
    vel = onsager_state_velocity(psi, seam, g)
    diss = onsager_dissipation(psi, seam, g)
    direct = seam_energy_directional_rate(psi, vel, seam)
    assert abs(norm_directional_rate(psi, vel)) < 1e-14
    assert diss >= 0.0
    assert math.isclose(direct, -diss, rel_tol=0.0, abs_tol=1e-14)


def test_full_balance_identity_and_norm_conservation_are_exact():
    psi = _normalized([1.0 + 0.3j, -0.2 + 0.6j, 0.4 - 0.9j, 0.5 + 0.1j])
    seam = np.array([0.12, -0.31, 0.77])
    h = np.array(
        [
            [0.2, 0.3, 0.0, 0.1j],
            [0.3, -0.1, 0.25j, 0.0],
            [0.0, -0.25j, 0.8, 0.2],
            [-0.1j, 0.0, 0.2, 0.4],
        ],
        dtype=complex,
    )
    vel = combined_state_velocity(psi, h, seam, 1.7)
    power, diss, balance = seam_balance_rate(psi, h, seam, 1.7)
    direct = seam_energy_directional_rate(psi, vel, seam)
    assert diss >= 0.0
    assert math.isclose(balance, power - diss, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(direct, balance, rel_tol=0.0, abs_tol=2e-14)
    assert abs(norm_directional_rate(psi, vel)) < 2e-14
    audit = audit_seam_balance(psi, h, seam, 1.7)
    assert audit.balance_residual < 2e-14
    assert abs(audit.norm_rate) < 2e-14


def test_commuting_hamiltonian_removes_schrodinger_pump_and_recovers_pure_descent():
    psi = _normalized([1.0, 0.6j, -0.4 + 0.3j])
    seam = np.array([0.0, 0.0])
    k = seam_stiffness(3, seam)
    h = 0.7 * np.eye(3) + 2.3 * k
    assert commutator_frobenius(h, seam) < 1e-14
    power, diss, balance = seam_balance_rate(psi, h, seam, 2.0)
    assert abs(power) < 1e-14
    assert diss >= 0.0
    assert math.isclose(balance, -diss, rel_tol=0.0, abs_tol=1e-14)


def test_noncommuting_schrodinger_flow_can_pump_or_remove_seam_energy():
    seam = [0.0]
    h = np.diag([1.0, -1.0])
    plus = _normalized([1.0, 1j])
    minus = _normalized([1.0, -1j])
    assert math.isclose(schrodinger_seam_power(plus, h, seam), 0.5, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(schrodinger_seam_power(minus, h, seam), -0.5, rel_tol=0.0, abs_tol=1e-15)


def test_static_gauge_reexpression_preserves_energy_power_and_dissipation():
    psi = _normalized([1.0 + 0.1j, -0.3 + 0.8j, 0.4 - 0.2j])
    seam = np.array([0.23, -0.51])
    h = np.array([[0.2, 0.3, 0.1j], [0.3, -0.4, 0.25], [-0.1j, 0.25, 0.9]], dtype=complex)
    chi = np.array([0.7, -0.2, 1.1])
    u = np.diag(np.exp(1j * chi))
    psi_t = u @ psi
    seam_t = seam + np.diff(chi)
    h_t = u @ h @ u.conj().T
    assert math.isclose(seam_defect_energy(psi, seam), seam_defect_energy(psi_t, seam_t), abs_tol=1e-14)
    assert math.isclose(
        schrodinger_seam_power(psi, h, seam),
        schrodinger_seam_power(psi_t, h_t, seam_t),
        abs_tol=2e-14,
    )
    assert math.isclose(
        onsager_dissipation(psi, seam, 1.3),
        onsager_dissipation(psi_t, seam_t, 1.3),
        abs_tol=2e-14,
    )


def test_real_zeta_collatz_hamiltonian_enters_same_balance_gate():
    frames = build_prime_frames([2, 3, 5, 7])
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.7, collatz_coupling=0.4)
    psi = _normalized([1.0, 0.3 + 0.5j, -0.2j, 0.4 - 0.1j])
    audit = audit_seam_balance(psi, h, [0.0, 0.0, 0.0], 0.9)
    assert math.isfinite(audit.schrodinger_power)
    assert audit.onsager_dissipation >= 0.0
    assert audit.balance_residual < 3e-14
    assert abs(audit.norm_rate) < 3e-14


@pytest.mark.parametrize(
    "call",
    [
        lambda: seam_covariant_incidence(0, []),
        lambda: seam_defect_energy([1.0, 0.0], []),
        lambda: schrodinger_seam_power([1.0, 0.0], [[0.0, 1.0], [0.0, 0.0]], [0.0]),
        lambda: onsager_dissipation([1.0, 1.0], [0.0], -1.0),
        lambda: onsager_dissipation([1.0, 1.0], [0.0], [[1.0, 2.0], [0.0, 1.0]]),
        lambda: onsager_dissipation([1.0, 1.0], [0.0], [[1.0, 0.0], [0.0, -0.1]]),
    ],
)
def test_full_balance_gate_fails_closed_on_invalid_domain(call):
    with pytest.raises(SchrodingerOnsagerBalanceError):
        call()
