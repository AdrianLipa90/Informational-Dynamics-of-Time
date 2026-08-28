import math
import numpy as np

from idt.half_frame_temporal_gluing import (
    antisymmetric_seam_basis,
    audit_half_frame_state,
    conditional_glued_probabilities,
    glued_amplitudes,
    glued_support_labels,
    glued_temporal_measures,
    gluing_coisometry,
    modular_phase_budget,
    norm_decomposition,
    seam_defect_amplitudes,
    split_isometry,
    temporal_path_incidence,
    temporal_support_laplacian,
    whole_to_glued_operator,
)


def test_declared_modular_patterns():
    assert glued_support_labels(1) == ("1", "1")
    assert glued_support_labels(2) == ("1", "12", "2")
    assert glued_support_labels(3) == ("1", "12", "23", "3")
    assert glued_support_labels(4) == ("1", "12", "23", "34", "4")
    for n in range(1, 5):
        assert len(glued_support_labels(n)) == n + 1
        assert math.isclose(modular_phase_budget(n), 2.0 * math.pi * n)


def test_split_and_gluing_operator_identities():
    for n in (1, 2, 5, 9):
        s = split_isometry(n)
        q = gluing_coisometry(n)
        np.testing.assert_allclose(s.conj().T @ s, np.eye(n), atol=2e-15)
        np.testing.assert_allclose(q @ q.conj().T, np.eye(n + 1), atol=2e-15)


def test_antisymmetric_seams_are_gluing_kernel_modes():
    for n in (2, 3, 7):
        q = gluing_coisometry(n)
        a = antisymmetric_seam_basis(n)
        np.testing.assert_allclose(a.conj().T @ a, np.eye(n - 1), atol=2e-15)
        np.testing.assert_allclose(q @ a, 0.0, atol=2e-15)
        assert 2 * n - np.linalg.matrix_rank(q) == n - 1


def test_neighbor_sum_formula_and_norm_decomposition():
    a = np.asarray([1.0 + 2.0j, -0.5 + 0.3j, 0.7 - 1.1j])
    a = a / np.linalg.norm(a)
    b = whole_to_glued_operator(3) @ a
    expected = np.asarray([
        a[0] / math.sqrt(2.0),
        (a[0] + a[1]) / 2.0,
        (a[1] + a[2]) / 2.0,
        a[2] / math.sqrt(2.0),
    ])
    np.testing.assert_allclose(b, expected, atol=2e-15)
    gw, dw, residual = norm_decomposition(a)
    assert abs(gw + dw - 1.0) < 3e-14
    assert residual < 3e-14


def test_uniform_chain_is_exactly_glued():
    for n in (2, 3, 4, 8):
        a = np.ones(n, dtype=complex) / math.sqrt(n)
        audit = audit_half_frame_state(a)
        np.testing.assert_allclose(audit.seam_defects, 0.0, atol=2e-15)
        assert abs(audit.glued_weight - 1.0) < 2e-14
        p = conditional_glued_probabilities(a)
        expected = np.full(n + 1, 1.0 / n)
        expected[0] = expected[-1] = 1.0 / (2.0 * n)
        np.testing.assert_allclose(p, expected, atol=2e-14)


def test_opposite_neighbor_phase_is_interface_null():
    a = np.asarray([1.0, -1.0], dtype=complex) / math.sqrt(2.0)
    b = glued_amplitudes(a)
    d = seam_defect_amplitudes(a)
    assert abs(b[1]) < 2e-15
    assert math.isclose(abs(d[0]) ** 2, 0.5, abs_tol=2e-15)
    gw, dw, residual = norm_decomposition(a)
    assert math.isclose(gw, 0.5, abs_tol=2e-15)
    assert math.isclose(dw, 0.5, abs_tol=2e-15)
    assert residual < 2e-15


def test_single_frame_is_two_equal_half_supports():
    audit = audit_half_frame_state([1.0])
    assert audit.support_labels == ("1", "1")
    np.testing.assert_allclose(conditional_glued_probabilities([1.0]), [0.5, 0.5], atol=2e-15)


def test_uniform_elapsed_measure_patterns_match_half_frame_picture():
    np.testing.assert_allclose(glued_temporal_measures([2.0]), [1.0, 1.0], atol=0.0)
    np.testing.assert_allclose(glued_temporal_measures([2.0, 2.0]), [1.0, 2.0, 1.0], atol=0.0)
    np.testing.assert_allclose(glued_temporal_measures([2.0, 2.0, 2.0]), [1.0, 2.0, 2.0, 1.0], atol=0.0)
    np.testing.assert_allclose(glued_temporal_measures([2.0, 2.0, 2.0, 2.0]), [1.0, 2.0, 2.0, 2.0, 1.0], atol=0.0)


def test_nonuniform_elapsed_measure_is_exactly_conserved():
    theta = np.asarray([0.17, 0.83, 1.4, 0.26, 2.11])
    glued = glued_temporal_measures(theta)
    assert glued.size == theta.size + 1
    assert np.all(glued > 0.0)
    assert math.isclose(float(np.sum(glued)), float(np.sum(theta)), rel_tol=0.0, abs_tol=2e-15)
    np.testing.assert_allclose(glued[1:-1], 0.5 * (theta[:-1] + theta[1:]), atol=0.0)


def test_half_frame_quotient_induces_path_incidence():
    for n in (1, 2, 4, 9):
        d = temporal_path_incidence(n)
        assert d.shape == (n + 1, n)
        np.testing.assert_allclose(np.sum(d, axis=0), 0.0, atol=0.0)
        assert np.linalg.matrix_rank(d) == n
        for edge in range(n):
            column = d[:, edge]
            assert np.count_nonzero(column == -1.0) == 1
            assert np.count_nonzero(column == 1.0) == 1
            assert np.count_nonzero(column) == 2


def test_weighted_support_laplacian_is_psd_with_constant_zero_mode():
    weights = np.asarray([0.2, 1.1, 0.7, 2.3, 0.4])
    lap = temporal_support_laplacian(weights)
    np.testing.assert_allclose(lap, lap.T, atol=0.0)
    np.testing.assert_allclose(lap @ np.ones(weights.size + 1), 0.0, atol=2e-15)
    eig = np.linalg.eigvalsh(lap)
    assert eig[0] > -2e-14
    assert eig[1] > 0.0


def test_uniform_path_spectrum_matches_exact_formula():
    n = 12
    weight = 0.73
    lap = temporal_support_laplacian(np.full(n, weight))
    actual = np.linalg.eigvalsh(lap)
    k = np.arange(n + 1, dtype=float)
    expected = 2.0 * weight * (1.0 - np.cos(k * math.pi / (n + 1)))
    np.testing.assert_allclose(actual, expected, rtol=0.0, atol=2e-14)


def test_low_path_modes_approach_quadratic_continuum():
    weight = 1.4
    errors = []
    for n in (32, 64, 128):
        eig = np.linalg.eigvalsh(temporal_support_laplacian(np.full(n, weight)))
        k = np.arange(1, 5, dtype=float)
        target = weight * (k * math.pi / (n + 1)) ** 2
        errors.append(float(np.max(np.abs(eig[1:5] / target - 1.0))))
    assert errors[2] < errors[1] < errors[0]
    assert errors[-1] < 1e-3
