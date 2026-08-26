from __future__ import annotations

import math
import numpy as np
import pytest

from src.idt.bifurcation import BifurcationError, bifurcation_from_activity_current, bifurcation_parameter_from_activity_current, contractive_event_operator, polar_bifurcation_from_event, polar_bifurcation_operator, unitary_bifurcation_operator
from src.idt.kahler_time import kappa
from src.idt.relational_kinetics import directed_rates
from src.idt.temporal_activity import activity_current_from_rates

SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
D_DIAG = np.diag([0.25, 0.8]).astype(complex)


def test_zero_current_has_zero_directional_phase_and_identity_operator():
    p, b = bifurcation_from_activity_current(2.0, 0.0, SIGMA_Y)
    assert math.isclose(p.phase_increment_rad, 0.0, abs_tol=1e-15)
    assert np.allclose(b, np.eye(2), atol=1e-14, rtol=0.0)


def test_reversal_flips_phase_and_gives_inverse_operator():
    p_plus, b_plus = bifurcation_from_activity_current(3.0, 1.2, SIGMA_Y)
    p_minus, b_minus = bifurcation_from_activity_current(3.0, -1.2, SIGMA_Y)
    assert math.isclose(p_minus.phase_increment_rad, -p_plus.phase_increment_rad, abs_tol=1e-15)
    assert np.allclose(b_minus, b_plus.conj().T, atol=1e-14, rtol=0.0)


def test_phase_parameter_matches_relational_rate_affinity():
    rates = directed_rates(4.0, 9.0, 2.0, 3.0, edge_drive=0.73)
    ac = activity_current_from_rates(rates.forward, rates.reverse)
    p = bifurcation_parameter_from_activity_current(ac.activity, ac.current)
    assert math.isclose(p.edge_drive, rates.edge_drive, abs_tol=1e-14)
    assert math.isclose(p.affinity_bits, rates.affinity_bits, abs_tol=1e-14)
    assert math.isclose(p.phase_increment_rad, kappa() * rates.affinity_bits, abs_tol=1e-14)


def test_canonical_kappa_simplifies_beta_to_atanh_ratio_over_12pi():
    p = bifurcation_parameter_from_activity_current(5.0, 2.0)
    assert math.isclose(p.phase_increment_rad, math.atanh(0.4)/(12.0*math.pi), abs_tol=1e-15)


def test_reference_operator_is_unitary():
    b = unitary_bifurcation_operator(0.47, SIGMA_Y)
    assert np.allclose(b.conj().T @ b, np.eye(2), atol=1e-14, rtol=0.0)


def test_positive_dissipator_generates_contraction():
    c = contractive_event_operator(0.9, D_DIAG)
    singular = np.linalg.svd(c, compute_uv=False)
    assert np.max(singular) <= 1.0 + 1e-14
    assert np.min(singular) > 0.0


def test_polar_bifurcation_separates_even_magnitude_and_odd_orientation():
    p_plus, b_plus = polar_bifurcation_from_event(0.7, 3.0, 1.2, D_DIAG, SIGMA_Z)
    p_minus, b_minus = polar_bifurcation_from_event(0.7, 3.0, -1.2, D_DIAG, SIGMA_Z)
    assert math.isclose(p_minus.phase_increment_rad, -p_plus.phase_increment_rad, abs_tol=1e-15)
    assert np.allclose(b_minus.contraction, b_plus.contraction, atol=1e-14, rtol=0.0)
    assert np.allclose(np.linalg.svd(b_minus.operator, compute_uv=False), np.linalg.svd(b_plus.operator, compute_uv=False), atol=1e-14, rtol=0.0)
    assert np.allclose(b_minus.operator, b_plus.operator.conj().T, atol=1e-14, rtol=0.0)


def test_zero_dissipator_reduces_polar_operator_to_unitary():
    bif = polar_bifurcation_operator(1.4, 0.33, np.zeros((2,2), dtype=complex), SIGMA_Z)
    assert np.allclose(bif.operator, bif.unitary, atol=1e-14, rtol=0.0)


def test_commuting_polar_subclass_composes_additively():
    b1 = polar_bifurcation_operator(0.2, 0.11, D_DIAG, SIGMA_Z).operator
    b2 = polar_bifurcation_operator(0.35, -0.04, D_DIAG, SIGMA_Z).operator
    total = polar_bifurcation_operator(0.55, 0.07, D_DIAG, SIGMA_Z).operator
    assert np.allclose(b2 @ b1, total, atol=1e-13, rtol=0.0)


def test_noncommuting_polar_factors_make_order_visible():
    bif = polar_bifurcation_operator(0.8, 0.41, D_DIAG, SIGMA_Y)
    assert not np.allclose(bif.operator, bif.unitary @ bif.contraction, atol=1e-10, rtol=0.0)


def test_negative_dissipator_fails_closed():
    with pytest.raises(BifurcationError):
        contractive_event_operator(0.5, np.diag([0.2, -0.1]))


def test_negative_event_strength_fails_closed():
    with pytest.raises(BifurcationError):
        contractive_event_operator(-0.1, D_DIAG)


def test_invalid_current_fraction_fails_closed():
    with pytest.raises(BifurcationError):
        bifurcation_parameter_from_activity_current(1.0, 1.0)
