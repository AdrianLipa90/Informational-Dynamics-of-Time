import math

import numpy as np


def covariant_component(grad_psi, psi, q_matrix, a_mu, hbar):
    return grad_psi + 1j * (a_mu / hbar) * (q_matrix @ psi)


def charge_projected_current(d_psi, psi, q_matrix):
    value = 1j * (np.vdot(d_psi, q_matrix @ psi) - np.vdot(psi, q_matrix @ d_psi))
    return float(np.real_if_close(value))


def test_gauge_covariant_derivative_matches_synchronized_idt_rfc_convention():
    hbar = 1.7
    q_diag = np.array([0.4, -0.9])
    q_matrix = np.diag(q_diag)
    psi = np.array([0.7 + 0.2j, -0.3 + 0.6j])
    grad = np.array([0.1 - 0.4j, 0.5 + 0.3j])
    a_mu = 0.8
    lam = -0.35
    dlam = 0.27

    u = np.exp(1j * q_diag * lam / hbar)
    psi_prime = u * psi
    grad_prime = u * grad + 1j * (q_diag * dlam / hbar) * psi_prime
    a_prime = a_mu - dlam

    before = covariant_component(grad, psi, q_matrix, a_mu, hbar)
    after = covariant_component(grad_prime, psi_prime, q_matrix, a_prime, hbar)
    assert np.allclose(after, u * before, rtol=2e-14, atol=2e-14)


def test_matter_action_variation_matches_charge_projected_current():
    hbar = 1.3
    q_matrix = np.diag([0.6, -1.1])
    psi = np.array([0.8 + 0.4j, -0.5 + 0.2j])
    grad = np.array([-0.2 + 0.7j, 0.3 - 0.6j])
    a_mu = -0.45

    def kinetic_density(a_value):
        dpsi = covariant_component(grad, psi, q_matrix, a_value, hbar)
        return float(np.vdot(dpsi, dpsi).real)

    dpsi = covariant_component(grad, psi, q_matrix, a_mu, hbar)
    expected = charge_projected_current(dpsi, psi, q_matrix) / hbar
    eps = 1e-7
    numeric = (kinetic_density(a_mu + eps) - kinetic_density(a_mu - eps)) / (2.0 * eps)
    assert math.isclose(numeric, expected, rel_tol=0.0, abs_tol=2e-8)


def test_single_charge_reduction_and_maxwell_source_coefficient():
    hbar = 2.2
    q = -0.7
    q_matrix = np.array([[q]])
    psi = np.array([0.9 - 0.3j])
    grad = np.array([0.2 + 0.5j])
    a_mu = 0.37
    dpsi = covariant_component(grad, psi, q_matrix, a_mu, hbar)

    j_q = charge_projected_current(dpsi, psi, q_matrix)
    j_theta_complex = 1j * (psi[0] * np.conjugate(dpsi[0]) - np.conjugate(psi[0]) * dpsi[0])
    j_theta = float(np.real_if_close(j_theta_complex))
    assert math.isclose(j_q, q * j_theta, rel_tol=2e-15, abs_tol=2e-15)

    j_em = -j_q / hbar
    assert math.isclose(j_em, -(q / hbar) * j_theta, rel_tol=2e-15, abs_tol=2e-15)


def test_charge_commutator_gate_rejects_cross_charge_mass_mixing():
    q_matrix = np.diag([0.0, 1.0, 1.0])
    commuting_mass2 = np.diag([0.2, 0.7, 1.4])
    adversarial_mass2 = commuting_mass2.astype(float).copy()
    adversarial_mass2[0, 1] = 0.31
    adversarial_mass2[1, 0] = 0.31

    commuting_defect = np.linalg.norm(commuting_mass2 @ q_matrix - q_matrix @ commuting_mass2)
    adversarial_defect = np.linalg.norm(adversarial_mass2 @ q_matrix - q_matrix @ adversarial_mass2)
    assert math.isclose(commuting_defect, 0.0, rel_tol=0.0, abs_tol=1e-15)
    assert adversarial_defect > 0.4


def test_neutrino_null_charge_has_zero_maxwell_source_with_nontrivial_dynamics():
    hbar = 1.9
    q_matrix = np.zeros((3, 3))
    psi = np.array([0.5 + 0.1j, -0.2 + 0.8j, 0.4 - 0.6j])
    grad = np.array([0.3 - 0.7j, 0.6 + 0.2j, -0.5 + 0.4j])
    dpsi = covariant_component(grad, psi, q_matrix, a_mu=1.4, hbar=hbar)
    assert np.linalg.norm(dpsi) > 0.5
    j_q = charge_projected_current(dpsi, psi, q_matrix)
    j_em = -j_q / hbar
    assert math.isclose(j_q, 0.0, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(j_em, 0.0, rel_tol=0.0, abs_tol=1e-15)
