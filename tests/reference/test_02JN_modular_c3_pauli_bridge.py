import numpy as np

from idt.modular_c3_pauli_bridge import (
    audit_mod6pi_c3_pauli_bridge,
    character_basis_f3,
    cyclic_incidence,
    cyclic_shift,
    pauli_basis,
    su2_cyclic_lift,
)


def test_periodic_open_cut_quotient_is_c3():
    b = cyclic_incidence()
    assert b.shape == (3, 3)
    assert np.linalg.matrix_rank(b) == 2
    assert np.allclose(np.sum(b, axis=0), 0.0)
    assert np.all(np.sum(np.abs(b), axis=1) == 2.0)


def test_regular_c3_shift_and_character_basis():
    p = cyclic_shift()
    f3 = character_basis_f3()
    assert np.allclose(np.linalg.matrix_power(p, 3), np.eye(3))
    assert np.allclose(f3.conj().T @ f3, np.eye(3))

    omega = np.exp(2j * np.pi / 3.0)
    expected = np.diag([1.0, omega**2, omega])
    assert np.allclose(f3.conj().T @ p @ f3, expected)


def test_pauli_triplet_is_c3_equivariant_under_su2_lift():
    pauli = pauli_basis()
    u = su2_cyclic_lift()

    assert np.allclose(u.conj().T @ u, np.eye(2))
    np.testing.assert_allclose(np.linalg.det(u), 1.0, atol=1e-12)

    for j, sigma in enumerate(pauli):
        assert np.allclose(u @ sigma @ u.conj().T, pauli[(j + 1) % 3])

    assert np.allclose(np.linalg.matrix_power(u, 3), -np.eye(2))
    assert np.allclose(np.linalg.matrix_power(u, 6), np.eye(2))


def test_full_bridge_audit_passes():
    audit = audit_mod6pi_c3_pauli_bridge()
    assert audit.passed, audit.checks
