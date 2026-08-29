import math

import numpy as np

from idt.neutrino_tensor_source import (
    commutator_norm,
    expectation,
    expectation_rate,
    tensor_expectation,
)
from idt.qhtri_neutrino_gravity import polarization_components_z, tt_source_gate


def _zero(dim=3):
    return np.zeros((dim, dim), dtype=np.complex128)


def _tensor_ops(fill=None):
    if fill is None:
        fill = _zero()
    return [[np.array(fill, dtype=np.complex128, copy=True) for _ in range(3)] for _ in range(3)]


def test_flavour_central_source_commutes_with_arbitrary_hamiltonian():
    H = np.array(
        [[0.2, 0.3j, 0.1], [-0.3j, -0.4, 0.2j], [0.1, -0.2j, 0.7]],
        dtype=np.complex128,
    )
    O = 2.7 * np.eye(3, dtype=np.complex128)
    psi = np.array([0.3 + 0.4j, -0.2 + 0.1j, 0.5 - 0.3j], dtype=np.complex128)
    psi /= np.linalg.norm(psi)
    assert commutator_norm(H, O) < 1e-12
    assert abs(expectation_rate(psi, H, O)) < 1e-12
    assert math.isclose(expectation(psi, O), 2.7, rel_tol=1e-12, abs_tol=1e-12)


def test_noncentral_flavour_tensor_operator_has_nonzero_commutator_rate():
    H = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.complex128)
    O = np.diag([1.0, -1.0, 0.0]).astype(np.complex128)
    psi = np.array([1.0, 1.0j, 0.0], dtype=np.complex128) / math.sqrt(2.0)
    assert commutator_norm(H, O) > 1.0
    assert math.isclose(expectation_rate(psi, H, O), 2.0, rel_tol=1e-12, abs_tol=1e-12)


def test_exact_two_flavour_rotation_modulates_noncentral_tensor_expectation():
    O = np.diag([1.0, -1.0, 0.0]).astype(np.complex128)
    for t in (0.0, 0.13, 0.41, 0.79):
        psi = np.array([math.cos(t), -1j * math.sin(t), 0.0], dtype=np.complex128)
        value = expectation(psi, O)
        assert math.isclose(value, math.cos(2.0 * t), rel_tol=1e-12, abs_tol=1e-12)


def test_noncentral_flavour_quadrupole_reaches_tt_gate():
    O = np.diag([1.0, -1.0, 0.0]).astype(np.complex128)
    ops = _tensor_ops()
    ops[0][0] = O
    ops[1][1] = -O

    t = 0.23
    psi = np.array([math.cos(t), -1j * math.sin(t), 0.0], dtype=np.complex128)
    stress = tensor_expectation(psi, ops)
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    plus, cross = polarization_components_z(result.tt)

    assert result.admitted
    assert math.isclose(plus, math.cos(2.0 * t), rel_tol=1e-12, abs_tol=1e-12)
    assert abs(cross) < 1e-12


def test_flavour_central_isotropic_tensor_is_rejected_by_tt_gate():
    I = np.eye(3, dtype=np.complex128)
    ops = _tensor_ops()
    ops[0][0] = I
    ops[1][1] = I
    ops[2][2] = I
    psi = np.array([0.2, 0.3j, math.sqrt(0.87)], dtype=np.complex128)
    stress = tensor_expectation(psi, ops)
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    assert not result.admitted
    assert result.norm < 1e-12


def test_central_tensor_expectation_is_flavour_state_invariant():
    O = 1.9 * np.eye(3, dtype=np.complex128)
    psi_a = np.array([1.0, 0.0, 0.0], dtype=np.complex128)
    psi_b = np.array([0.3 + 0.4j, -0.2 + 0.1j, 0.5 - 0.3j], dtype=np.complex128)
    psi_b /= np.linalg.norm(psi_b)
    assert math.isclose(expectation(psi_a, O), expectation(psi_b, O), rel_tol=1e-12, abs_tol=1e-12)
