from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.bifurcation import (
    BifurcationError,
    bifurcation_from_activity_current,
    bifurcation_parameter_from_activity_current,
    unitary_bifurcation_operator,
)
from src.idt.kahler_time import kappa
from src.idt.relational_kinetics import directed_rates
from src.idt.temporal_activity import activity_current_from_rates


SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)


def test_zero_current_has_zero_directional_phase_and_identity_operator() -> None:
    p, b = bifurcation_from_activity_current(2.0, 0.0, SIGMA_Y)
    assert math.isclose(p.phase_increment_rad, 0.0, abs_tol=1e-15)
    assert np.allclose(b, np.eye(2), atol=1e-14, rtol=0.0)


def test_reversal_flips_phase_and_gives_inverse_operator() -> None:
    p_plus, b_plus = bifurcation_from_activity_current(3.0, 1.2, SIGMA_Y)
    p_minus, b_minus = bifurcation_from_activity_current(3.0, -1.2, SIGMA_Y)
    assert math.isclose(p_minus.phase_increment_rad, -p_plus.phase_increment_rad, abs_tol=1e-15)
    assert np.allclose(b_minus, b_plus.conj().T, atol=1e-14, rtol=0.0)
    assert np.allclose(b_minus @ b_plus, np.eye(2), atol=1e-14, rtol=0.0)


def test_phase_parameter_matches_relational_rate_affinity() -> None:
    rates = directed_rates(4.0, 9.0, 2.0, 3.0, edge_drive=0.73)
    ac = activity_current_from_rates(rates.forward, rates.reverse)
    p = bifurcation_parameter_from_activity_current(ac.activity, ac.current)
    assert math.isclose(p.edge_drive, rates.edge_drive, abs_tol=1e-14)
    assert math.isclose(p.affinity_bits, rates.affinity_bits, abs_tol=1e-14)
    assert math.isclose(p.phase_increment_rad, kappa() * rates.affinity_bits, abs_tol=1e-14)


def test_canonical_kappa_simplifies_beta_to_atanh_ratio_over_12pi() -> None:
    p = bifurcation_parameter_from_activity_current(5.0, 2.0)
    expected = math.atanh(2.0 / 5.0) / (12.0 * math.pi)
    assert math.isclose(p.phase_increment_rad, expected, abs_tol=1e-15)


def test_reference_operator_is_unitary() -> None:
    b = unitary_bifurcation_operator(0.47, SIGMA_Y)
    assert np.allclose(b.conj().T @ b, np.eye(2), atol=1e-14, rtol=0.0)


def test_same_generator_composes_by_phase_addition() -> None:
    b1 = unitary_bifurcation_operator(0.17, SIGMA_Y)
    b2 = unitary_bifurcation_operator(-0.09, SIGMA_Y)
    combined = unitary_bifurcation_operator(0.08, SIGMA_Y)
    assert np.allclose(b2 @ b1, combined, atol=1e-14, rtol=0.0)


def test_invalid_current_fraction_fails_closed() -> None:
    with pytest.raises(BifurcationError):
        bifurcation_parameter_from_activity_current(1.0, 1.0)
