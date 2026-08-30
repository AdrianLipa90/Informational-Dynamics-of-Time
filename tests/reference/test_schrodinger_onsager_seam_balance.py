import math

import numpy as np
import pytest

from idt.schrodinger_onsager_seam_balance import (
    SchrodingerOnsagerBalanceError,
    audit_instantaneous_balance,
    edge_mismatch_gradients,
    exact_unitary_step,
    full_balance_velocity,
    node_phase_gradient,
    onsager_phase_velocity,
    path_incidence,
    phase_only_onsager_step,
    schrodinger_seam_power,
    schrodinger_velocity,
    seam_defect_energy,
    seam_difference_operator,
    seam_stiffness,
    strang_balance_step,
)


def _reference_state():
    psi = np.array([1.0 + 0.4j, -0.3 + 0.8j, 0.7 - 0.2j, 0.2 + 0.6j], dtype=complex)
    return psi / np.linalg.norm(psi)


def _reference_hamiltonian():
    return np.array([
        [0.4, 0.3 + 0.1j, 0.0, 0.0],
        [0.3 - 0.1j, -0.2, 0.25, 0.0],
        [0.0, 0.25, 0.7, -0.15j],
        [0.0, 0.0, 0.15j, -0.1],
    ], dtype=complex)


def _reference_onsager():
    return np.array([
        [1.2, 0.1, 0.0, 0.0],
        [0.1, 1.0, 0.1, 0.0],
        [0.0, 0.1, 0.9, 0.05],
        [0.0, 0.0, 0.05, 0.7],
    ])


PHI = np.array([0.2, -0.35, 0.5])


def test_phase_aware_seam_stiffness_is_hermitian_psd():
    b = seam_difference_operator(PHI, 4)
    k = seam_stiffness(PHI, 4)
    np.testing.assert_allclose(k, b.conj().T @ b, atol=2e-15)
    np.testing.assert_allclose(k, k.conj().T, atol=2e-15)
    assert np.min(np.linalg.eigvalsh(k)) > -1e-14


def test_quadratic_seam_energy_matches_explicit_defect_norm():
    psi = _reference_state()
    b = seam_difference_operator(PHI, 4)
    k = seam_stiffness(PHI, 4)
    expected = float(np.vdot(b @ psi, b @ psi).real)
    quadratic = float(np.vdot(psi, k @ psi).real)
    assert math.isclose(seam_defect_energy(psi, PHI), expected, abs_tol=2e-15)
    assert math.isclose(quadratic, expected, abs_tol=2e-15)


def test_node_phase_gradient_matches_finite_difference():
    psi = _reference_state()
    gradient = node_phase_gradient(psi, PHI)
    eps = 1e-7
    numerical = np.empty(psi.size)
    for node in range(psi.size):
        plus = psi.copy()
        minus = psi.copy()
        plus[node] *= np.exp(1j * eps)
        minus[node] *= np.exp(-1j * eps)
        numerical[node] = (
            seam_defect_energy(plus, PHI) - seam_defect_energy(minus, PHI)
        ) / (2.0 * eps)
    np.testing.assert_allclose(gradient, numerical, atol=2e-9, rtol=0.0)
    assert abs(float(np.sum(gradient))) < 2e-15


def test_edge_and_node_gradients_obey_incidence_pullback():
    psi = _reference_state()
    edge = edge_mismatch_gradients(psi, PHI)
    d = path_incidence(4)
    np.testing.assert_allclose(node_phase_gradient(psi, PHI), d.T @ edge, atol=2e-15)
    np.testing.assert_allclose(d @ np.ones(4), 0.0, atol=0.0)


def test_schrodinger_commutator_power_matches_directional_derivative():
    psi = _reference_state()
    h = _reference_hamiltonian()
    k = seam_stiffness(PHI, 4)
    velocity = schrodinger_velocity(psi, h)
    directional = 2.0 * float(np.real(np.vdot(k @ psi, velocity)))
    commutator_power = schrodinger_seam_power(psi, h, PHI)
    assert math.isclose(directional, commutator_power, rel_tol=0.0, abs_tol=2e-14)


def test_schrodinger_sector_preserves_norm_instantaneously():
    psi = _reference_state()
    velocity = schrodinger_velocity(psi, _reference_hamiltonian())
    norm_rate = 2.0 * float(np.real(np.vdot(psi, velocity)))
    assert abs(norm_rate) < 2e-14


def test_onsager_phase_sector_preserves_norm_and_dissipates_seam_energy():
    psi = _reference_state()
    g = _reference_onsager()
    k = seam_stiffness(PHI, 4)
    _, velocity, dissipation = onsager_phase_velocity(psi, PHI, g)
    norm_rate = 2.0 * float(np.real(np.vdot(psi, velocity)))
    energy_rate = 2.0 * float(np.real(np.vdot(k @ psi, velocity)))
    assert abs(norm_rate) < 2e-14
    assert dissipation >= 0.0
    assert math.isclose(energy_rate, -dissipation, rel_tol=0.0, abs_tol=2e-14)


def test_full_instantaneous_balance_is_exact():
    audit = audit_instantaneous_balance(
        _reference_state(),
        _reference_hamiltonian(),
        PHI,
        _reference_onsager(),
    )
    assert audit.dissipation >= 0.0
    assert abs(audit.norm_rate) < 2e-14
    assert audit.energy_balance_residual < 3e-14
    assert math.isclose(
        audit.directional_energy_rate,
        audit.schrodinger_power - audit.dissipation,
        rel_tol=0.0,
        abs_tol=3e-14,
    )


def test_commuting_hamiltonian_has_zero_reversible_seam_power():
    psi = _reference_state()
    k = seam_stiffness(PHI, 4)
    power = schrodinger_seam_power(psi, k, PHI)
    assert abs(power) < 2e-14
    audit = audit_instantaneous_balance(psi, k, PHI, _reference_onsager())
    assert math.isclose(audit.predicted_energy_rate, -audit.dissipation, abs_tol=2e-14)


def test_pure_onsager_small_steps_reduce_seam_defect_and_preserve_norm():
    psi = _reference_state()
    g = _reference_onsager()
    initial_norm = np.linalg.norm(psi)
    energies = [seam_defect_energy(psi, PHI)]
    for _ in range(500):
        psi = phase_only_onsager_step(psi, PHI, g, 2e-3)
        energies.append(seam_defect_energy(psi, PHI))
    assert abs(np.linalg.norm(psi) - initial_norm) < 2e-13
    assert np.max(np.diff(energies)) < 2e-8
    assert energies[-1] < energies[0]


def test_exact_unitary_step_preserves_norm():
    psi = _reference_state()
    out = exact_unitary_step(psi, _reference_hamiltonian(), 1.7)
    assert abs(np.linalg.norm(out) - np.linalg.norm(psi)) < 2e-14


def test_strang_reference_step_preserves_norm_over_many_steps():
    psi = _reference_state()
    norm0 = np.linalg.norm(psi)
    h = _reference_hamiltonian()
    g = _reference_onsager()
    for _ in range(200):
        psi = strang_balance_step(psi, h, PHI, g, 0.005)
    assert abs(np.linalg.norm(psi) - norm0) < 2e-12


def test_global_phase_does_not_change_seam_energy_or_gradient():
    psi = _reference_state()
    rotated = np.exp(1.234j) * psi
    assert math.isclose(
        seam_defect_energy(rotated, PHI),
        seam_defect_energy(psi, PHI),
        abs_tol=2e-15,
    )
    np.testing.assert_allclose(
        node_phase_gradient(rotated, PHI),
        node_phase_gradient(psi, PHI),
        atol=2e-15,
    )


def test_full_velocity_is_tangent_to_norm_sphere():
    psi = _reference_state()
    velocity = full_balance_velocity(psi, _reference_hamiltonian(), PHI, _reference_onsager())
    assert abs(2.0 * float(np.real(np.vdot(psi, velocity)))) < 2e-14


@pytest.mark.parametrize(
    "call",
    [
        lambda: seam_difference_operator([0.1], 4),
        lambda: seam_defect_energy([1.0], []),
        lambda: schrodinger_velocity([1.0, 0.0], [[0.0, 1.0], [0.0, 0.0]]),
        lambda: onsager_phase_velocity([1.0, 0.0], [0.0], [[1.0, 2.0], [0.0, 1.0]]),
        lambda: onsager_phase_velocity([1.0, 0.0], [0.0], [[1.0, 0.0], [0.0, -1.0]]),
        lambda: phase_only_onsager_step([1.0, 0.0], [0.0], np.eye(2), -0.1),
    ],
)
def test_balance_gate_fails_closed_on_invalid_domain(call):
    with pytest.raises(SchrodingerOnsagerBalanceError):
        call()
