from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.bifurcation import BifurcationError
from src.idt.now_bifurcation_bridge import (
    activity_current_from_wave_bifurcation,
    canonical_activity_current_from_wave_bifurcation,
    realized_event_weight,
    wave_active_bifurcation_operator,
    wave_bifurcation_coordinates,
)


def test_canonical_pair_roundtrip_10000_cases() -> None:
    rng = np.random.default_rng(270827)
    max_m_rel = 0.0
    max_a_rel = 0.0
    max_j_rel = 0.0
    for _ in range(10_000):
        mobility = float(np.exp(rng.uniform(math.log(1e-4), math.log(50.0))))
        drive = float(rng.uniform(-8.0, 8.0))
        activity = 2.0 * mobility * math.cosh(drive / 2.0)
        current = 2.0 * mobility * math.sinh(drive / 2.0)
        coords = wave_bifurcation_coordinates(activity, current)
        a2, j2 = canonical_activity_current_from_wave_bifurcation(
            coords.mobility, coords.phase_increment_rad
        )
        max_m_rel = max(max_m_rel, abs(coords.mobility - mobility) / mobility)
        max_a_rel = max(max_a_rel, abs(a2 - activity) / activity)
        max_j_rel = max(max_j_rel, abs(j2 - current) / max(abs(current), 1e-12))
        assert math.isclose(coords.edge_drive, 24.0 * math.pi * coords.phase_increment_rad, rel_tol=0.0, abs_tol=1e-11)
    assert max_m_rel < 1e-10
    assert max_a_rel < 1e-10
    assert max_j_rel < 1e-10


def test_general_kappa_roundtrip() -> None:
    kap = 0.031
    activity, current = activity_current_from_wave_bifurcation(
        1.8, -0.007, kappa_value=kap
    )
    coords = wave_bifurcation_coordinates(activity, current, kappa_value=kap)
    assert math.isclose(coords.mobility, 1.8, rel_tol=0.0, abs_tol=1e-13)
    assert math.isclose(coords.phase_increment_rad, -0.007, rel_tol=0.0, abs_tol=1e-13)


def test_current_reversal_preserves_wave_channel_and_flips_orientation() -> None:
    pos = wave_bifurcation_coordinates(5.0, 3.0)
    neg = wave_bifurcation_coordinates(5.0, -3.0)
    assert math.isclose(pos.mobility, neg.mobility, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pos.edge_drive, -neg.edge_drive, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pos.phase_increment_rad, -neg.phase_increment_rad, rel_tol=0.0, abs_tol=1e-14)


def test_realization_weight_is_positive_product_gate() -> None:
    assert realized_event_weight(2.0, 3.0) == 6.0
    assert realized_event_weight(0.0, 3.0) == 0.0
    assert realized_event_weight(2.0, 0.0) == 0.0


def test_zero_realization_returns_identity_even_with_directed_current() -> None:
    generator = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    gated = wave_active_bifurcation_operator(0.0, 4.0, 5.0, 2.0, generator)
    assert not gated.realized
    assert gated.realization_weight == 0.0
    assert np.allclose(gated.operator, np.eye(2), atol=0.0, rtol=0.0)


def test_positive_realization_applies_unitary_directional_operator() -> None:
    generator = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    gated = wave_active_bifurcation_operator(2.0, 4.0, 5.0, 2.0, generator)
    assert gated.realized
    assert gated.realization_weight == 8.0
    assert np.allclose(gated.operator.conj().T @ gated.operator, np.eye(2), atol=1e-12, rtol=0.0)


def test_current_reversal_inverts_realized_unitary() -> None:
    generator = np.asarray([[0.3, 0.4j], [-0.4j, -0.2]], dtype=complex)
    pos = wave_active_bifurcation_operator(1.0, 2.0, 4.0, 1.3, generator)
    neg = wave_active_bifurcation_operator(1.0, 2.0, 4.0, -1.3, generator)
    assert pos.realized and neg.realized
    assert np.allclose(neg.operator, pos.operator.conj().T, atol=1e-12, rtol=0.0)


def test_fail_closed_invalid_pair_and_event_weight() -> None:
    with pytest.raises(BifurcationError):
        wave_bifurcation_coordinates(1.0, 1.0)
    with pytest.raises(BifurcationError):
        activity_current_from_wave_bifurcation(-1.0, 0.1)
    with pytest.raises(BifurcationError):
        realized_event_weight(-1.0, 1.0)
