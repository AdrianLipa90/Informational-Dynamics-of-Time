import math

import numpy as np

from idt.phase_aware_half_seam import (
    phase_aware_glued_amplitudes,
    phase_aware_gluing_coisometry,
    phase_aware_seam_defects,
    seam_probabilities,
)


def test_internal_seam_amplitudes_flip_at_2pi_and_return_at_4pi():
    a = np.asarray([0.7 + 0.2j, -0.1 + 0.9j], dtype=complex)
    phi = 0.37

    b0 = phase_aware_glued_amplitudes(a, [phi])[1]
    b2 = phase_aware_glued_amplitudes(a, [phi + 2.0 * math.pi])[1]
    b4 = phase_aware_glued_amplitudes(a, [phi + 4.0 * math.pi])[1]

    d0 = phase_aware_seam_defects(a, [phi])[0]
    d2 = phase_aware_seam_defects(a, [phi + 2.0 * math.pi])[0]
    d4 = phase_aware_seam_defects(a, [phi + 4.0 * math.pi])[0]

    assert abs(b2 + b0) < 3e-15
    assert abs(b4 - b0) < 3e-15
    assert abs(d2 + d0) < 3e-15
    assert abs(d4 - d0) < 3e-15


def test_quadratic_seam_observables_return_at_2pi():
    a = np.asarray([1.0, 0.2 + 0.8j, -0.6 + 0.3j], dtype=complex)
    phases = np.asarray([0.4, -1.2])
    overlap0, defect0 = seam_probabilities(a, phases)
    overlap2, defect2 = seam_probabilities(a, phases + 2.0 * math.pi)
    np.testing.assert_allclose(overlap2, overlap0, rtol=0.0, atol=4e-15)
    np.testing.assert_allclose(defect2, defect0, rtol=0.0, atol=4e-15)


def test_full_gluing_operator_has_internal_sign_operator_at_2pi():
    n = 5
    phases = np.asarray([0.1, 0.8, -1.1, 2.3])
    q0 = phase_aware_gluing_coisometry(n, phases)
    q2 = phase_aware_gluing_coisometry(n, phases + 2.0 * math.pi)
    q4 = phase_aware_gluing_coisometry(n, phases + 4.0 * math.pi)

    jg = np.eye(n + 1, dtype=complex)
    jg[1:-1, 1:-1] *= -1.0

    np.testing.assert_allclose(q2, jg @ q0, rtol=0.0, atol=4e-15)
    np.testing.assert_allclose(q4, q0, rtol=0.0, atol=4e-15)
    np.testing.assert_allclose(jg @ jg, np.eye(n + 1), rtol=0.0, atol=0.0)


def test_boundary_half_supports_are_unchanged_by_internal_seam_cycle():
    a = np.asarray([1.0, 0.4j, -0.2, 0.7], dtype=complex)
    phases = np.asarray([0.3, -0.7, 1.4])
    b0 = phase_aware_glued_amplitudes(a, phases)
    b2 = phase_aware_glued_amplitudes(a, phases + 2.0 * math.pi)
    assert abs(b2[0] - b0[0]) < 2e-15
    assert abs(b2[-1] - b0[-1]) < 2e-15
    np.testing.assert_allclose(b2[1:-1], -b0[1:-1], rtol=0.0, atol=4e-15)
