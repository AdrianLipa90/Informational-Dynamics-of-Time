import cmath
import math

import numpy as np


def commutator(A, B):
    return A @ B - B @ A


def charge_expectation(a, Q):
    return np.vdot(a, Q @ a)


def test_charge_derivative_equals_commutator_identity():
    H = np.array(
        [
            [0.3, 0.2 + 0.1j, -0.1j],
            [0.2 - 0.1j, -0.4, 0.05],
            [0.1j, 0.05, 0.7],
        ],
        dtype=np.complex128,
    )
    Q = np.diag([0.0, -1.0, -1.0]).astype(np.complex128)
    a = np.array([0.3 + 0.4j, -0.2 + 0.1j, 0.5 - 0.3j], dtype=np.complex128)

    adot = -1j * H @ a
    direct = np.vdot(adot, Q @ a) + np.vdot(a, Q @ adot)
    via_commutator = 1j * np.vdot(a, commutator(H, Q) @ a)
    assert abs(direct - via_commutator) < 1e-12


def test_equal_charge_block_commutes_with_any_hermitian_flavour_hamiltonian():
    H = np.array(
        [[0.2, 0.3j, 0.1], [-0.3j, 0.5, -0.2j], [0.1, 0.2j, -0.4]],
        dtype=np.complex128,
    )
    assert np.max(np.abs(H - H.conj().T)) < 1e-12
    Q = -1.0 * np.eye(3, dtype=np.complex128)
    assert np.max(np.abs(commutator(H, Q))) < 1e-12


def test_neutrino_charge_block_is_exact_null_for_arbitrary_hermitian_hamiltonian():
    H = np.array(
        [[0.1, 0.2, 0.3j], [0.2, -0.4, -0.1j], [-0.3j, 0.1j, 0.6]],
        dtype=np.complex128,
    )
    Q_nu = np.zeros((3, 3), dtype=np.complex128)
    a = np.array([0.2 + 0.1j, 0.6 - 0.2j, -0.3 + 0.4j], dtype=np.complex128)
    assert np.max(np.abs(commutator(H, Q_nu))) == 0.0
    assert charge_expectation(a, Q_nu) == 0.0


def test_neutrino_ab_factor_is_identity_even_with_nontrivial_flavour_rotation():
    theta = 0.43
    c, s = math.cos(theta), math.sin(theta)
    U = np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]], dtype=np.complex128)
    W_nu = np.eye(3, dtype=np.complex128)
    assert np.max(np.abs(U - np.eye(3))) > 1e-3
    assert np.max(np.abs(W_nu @ U - U @ W_nu)) < 1e-12


def test_equal_charge_ab_phase_is_central_in_flavour_space():
    q = -1.0
    hbar = 2.3
    line_integral = 0.71
    phase = cmath.exp(1j * (q / hbar) * line_integral)
    W = phase * np.eye(3, dtype=np.complex128)

    theta = 0.52
    c, s = math.cos(theta), math.sin(theta)
    U = np.array(
        [[c, 0.0, s], [0.0, cmath.exp(0.17j), 0.0], [-s, 0.0, c]],
        dtype=np.complex128,
    )
    assert np.max(np.abs(W @ U - U @ W)) < 1e-12


def test_charge_block_diagonal_hamiltonian_preserves_charge_operator():
    Q = np.diag([0.0, -1.0, -1.0]).astype(np.complex128)
    H = np.array(
        [[0.7, 0.0, 0.0], [0.0, 0.2, 0.3j], [0.0, -0.3j, -0.1]],
        dtype=np.complex128,
    )
    assert np.max(np.abs(H - H.conj().T)) < 1e-12
    assert np.max(np.abs(commutator(H, Q))) < 1e-12


def test_cross_charge_mixing_hamiltonian_fails_commutator_gate():
    Q = np.diag([0.0, -1.0]).astype(np.complex128)
    H = np.array([[0.0, 0.7], [0.7, 0.0]], dtype=np.complex128)
    defect = np.max(np.abs(commutator(H, Q)))
    assert defect > 0.5


def test_cross_charge_mixing_can_drive_nonzero_charge_derivative():
    Q = np.diag([0.0, -1.0]).astype(np.complex128)
    H = np.array([[0.0, 0.7], [0.7, 0.0]], dtype=np.complex128)
    a = np.array([1.0, 1.0j], dtype=np.complex128) / math.sqrt(2.0)
    qdot = 1j * np.vdot(a, commutator(H, Q) @ a)
    assert math.isclose(float(qdot.real), 0.7, rel_tol=1e-12, abs_tol=1e-12)
    assert abs(qdot.imag) < 1e-12
