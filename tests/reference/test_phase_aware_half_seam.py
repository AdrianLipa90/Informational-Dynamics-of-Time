import math

import numpy as np

from idt.half_frame_temporal_gluing import whole_to_glued_operator
from idt.phase_aware_half_seam import (
    gauge_transform,
    phase_aware_glued_amplitudes,
    phase_aware_gluing_coisometry,
    phase_aware_norm_decomposition,
    phase_aware_seam_defects,
    phase_aware_whole_to_glued,
    remove_exact_gradient_seam,
    seam_probabilities,
)


def test_phase_aware_gluing_is_coisometry():
    for n in (1, 2, 5, 9):
        phases = np.linspace(-1.7, 2.1, max(0, n - 1))
        q = phase_aware_gluing_coisometry(n, phases)
        np.testing.assert_allclose(q @ q.conj().T, np.eye(n + 1), rtol=0.0, atol=3e-15)


def test_zero_phase_reduces_exactly_to_half_frame_gluing():
    for n in (1, 2, 4, 7):
        phases = np.zeros(max(0, n - 1))
        np.testing.assert_allclose(
            phase_aware_whole_to_glued(n, phases),
            whole_to_glued_operator(n),
            rtol=0.0,
            atol=0.0,
        )


def test_phase_aware_norm_decomposition_is_exact():
    a = np.asarray([1.0 + 0.2j, -0.7 + 1.1j, 0.4 - 0.9j, 1.3 + 0.1j], dtype=complex)
    phases = np.asarray([0.3, -1.2, 2.4])
    glued, defect, residual = phase_aware_norm_decomposition(a, phases)
    assert math.isclose(glued + defect, 1.0, rel_tol=0.0, abs_tol=4e-14)
    assert residual < 4e-14


def test_gauge_transform_preserves_overlap_and_defect_probabilities():
    a = np.asarray([1.0 + 0.4j, -0.3 + 0.9j, 0.8 - 0.2j, -0.5 - 0.7j], dtype=complex)
    phases = np.asarray([0.2, -0.8, 1.1])
    chi = np.asarray([0.7, -1.3, 0.4, 2.0])
    p_overlap, p_defect = seam_probabilities(a, phases)
    a2, phases2 = gauge_transform(a, phases, chi)
    p_overlap2, p_defect2 = seam_probabilities(a2, phases2)
    np.testing.assert_allclose(p_overlap2, p_overlap, rtol=0.0, atol=4e-15)
    np.testing.assert_allclose(p_defect2, p_defect, rtol=0.0, atol=4e-15)


def test_equal_magnitude_delta_zero_is_constructive():
    phi = 1.3
    a = np.asarray([1.0, np.exp(1j * phi)], dtype=complex) / math.sqrt(2.0)
    overlap, defect = seam_probabilities(a, [phi])
    assert math.isclose(float(overlap[0]), 0.5, rel_tol=0.0, abs_tol=3e-15)
    assert float(defect[0]) < 3e-15


def test_equal_magnitude_delta_pi_is_interface_null():
    phi = -0.4
    a = np.asarray([1.0, np.exp(1j * (phi + math.pi))], dtype=complex) / math.sqrt(2.0)
    overlap, defect = seam_probabilities(a, [phi])
    assert float(overlap[0]) < 3e-15
    assert math.isclose(float(defect[0]), 0.5, rel_tol=0.0, abs_tol=3e-15)


def test_exact_gradient_seam_is_removed_by_open_path_rephasing():
    seam = np.asarray([0.2, -0.7, 1.5, 0.4])
    beta, transformed = remove_exact_gradient_seam(seam)
    np.testing.assert_allclose(np.diff(beta), seam, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(transformed, 0.0, rtol=0.0, atol=2e-15)

    a = np.asarray([1.0, 0.3 + 0.2j, -0.4j, 0.8, -0.5 + 0.1j])
    overlap, defect = seam_probabilities(a, seam)
    a2, seam2 = gauge_transform(a, seam, -beta)
    overlap2, defect2 = seam_probabilities(a2, seam2)
    np.testing.assert_allclose(seam2, 0.0, rtol=0.0, atol=2e-15)
    np.testing.assert_allclose(overlap2, overlap, rtol=0.0, atol=5e-15)
    np.testing.assert_allclose(defect2, defect, rtol=0.0, atol=5e-15)


def test_direct_amplitude_formula_matches_declared_half_link_phases():
    a = np.asarray([0.6 + 0.2j, -0.1 + 0.7j], dtype=complex)
    a = a / np.linalg.norm(a)
    phi = 0.9
    b = phase_aware_glued_amplitudes(a, [phi])
    d = phase_aware_seam_defects(a, [phi])
    expected_b = 0.5 * (np.exp(0.5j * phi) * a[0] + np.exp(-0.5j * phi) * a[1])
    expected_d = 0.5 * (np.exp(0.5j * phi) * a[0] - np.exp(-0.5j * phi) * a[1])
    assert abs(b[1] - expected_b) < 3e-15
    assert abs(d[0] - expected_d) < 3e-15
