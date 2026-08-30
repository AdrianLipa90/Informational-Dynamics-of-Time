import math

import numpy as np
import pytest

from idt.bound_now_bifurcation import (
    BoundNowBifurcationError,
    apply_bound_bifurcation,
    bind_now_bifurcation,
)
from idt.now_bifurcation_bridge import wave_active_bifurcation_operator
from idt.now_material_quantile_binding import bind_serial_now_to_quantile
from idt.relational_precedence import RelationalEdge, unfold_serial_history


def _history(final_weight: float = 0.6):
    edges = [
        RelationalEdge("e1", "A", "B", 0.2, 0.4),
        RelationalEdge("e2", "B", "A", 0.3, 0.5),
        RelationalEdge("e3", "A", "C", 0.4, final_weight),
    ]
    return unfold_serial_history("A", edges)


def _material(center: float, velocity: float = 0.7):
    x = np.linspace(-10.0, 10.0, 5001)
    rho = np.exp(-0.5 * (x - center) ** 2)
    current = velocity * rho
    return x, rho, current


def _bound_marker(center: float = 1.25, velocity: float = 0.7):
    x, rho, current = _material(center, velocity)
    return bind_serial_now_to_quantile(_history(), x, rho, current)


def _generator():
    return np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def _bind(center: float = 1.25, current: float = 1.0):
    return bind_now_bifurcation(
        _bound_marker(center),
        material_theta=0.9,
        structural_signature=0.75,
        wave_activation=0.8,
        activity=4.0,
        current=current,
        generator=_generator(),
    )


def test_bound_packet_targets_realized_prefix_and_material_half_marker():
    bound = _bind()
    assert bound.occurrence_prefix == ("e1", "e2", "e3")
    assert bound.terminal_edge_id == "e3"
    assert bound.theta == pytest.approx(0.9)
    assert bound.material_position == pytest.approx(1.25, abs=2e-12)
    assert bound.material_velocity == pytest.approx(0.7, abs=2e-12)
    assert bound.realization_weight == pytest.approx(0.6)


def test_bound_operator_matches_existing_now_bifurcation_bridge_exactly():
    bound = _bind()
    direct = wave_active_bifurcation_operator(
        0.75,
        0.8,
        4.0,
        1.0,
        _generator(),
    )
    assert bound.mobility == pytest.approx(direct.coordinates.mobility)
    assert bound.phase_increment_rad == pytest.approx(direct.coordinates.phase_increment_rad)
    np.testing.assert_allclose(bound.operator, direct.operator, atol=1e-15, rtol=0.0)


def test_material_translation_changes_localization_but_preserves_operator():
    left = _bind(center=-2.0)
    right = _bind(center=3.0)
    assert left.material_position == pytest.approx(-2.0, abs=2e-12)
    assert right.material_position == pytest.approx(3.0, abs=2e-12)
    assert left.occurrence_prefix == right.occurrence_prefix
    assert left.phase_increment_rad == pytest.approx(right.phase_increment_rad)
    np.testing.assert_allclose(left.operator, right.operator, atol=1e-15, rtol=0.0)


def test_current_reversal_preserves_location_and_mobility_and_adjoins_operator():
    plus = _bind(current=1.0)
    minus = _bind(current=-1.0)
    assert plus.material_position == pytest.approx(minus.material_position, abs=1e-14)
    assert plus.mobility == pytest.approx(minus.mobility)
    assert plus.phase_increment_rad == pytest.approx(-minus.phase_increment_rad)
    np.testing.assert_allclose(minus.operator, plus.operator.conj().T, atol=1e-15, rtol=0.0)


def test_state_recurrence_is_targeted_by_occurrence_prefix():
    bound = _bind()
    assert _history()[0].state == "A"
    assert _history()[2].state == "A"
    assert bound.occurrence_prefix == ("e1", "e2", "e3")
    assert bound.terminal_edge_id == "e3"


def test_bound_bifurcation_applies_unitary_update_and_preserves_norm():
    bound = _bind()
    state = np.array([1.0, 1.0j], dtype=complex) / math.sqrt(2.0)
    after = apply_bound_bifurcation(state, bound)
    assert np.linalg.norm(after) == pytest.approx(np.linalg.norm(state), abs=1e-14)
    np.testing.assert_allclose(after, bound.operator @ state, atol=1e-15, rtol=0.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(material_theta=0.91, structural_signature=0.75, wave_activation=0.8),
        dict(material_theta=0.9, structural_signature=0.5, wave_activation=0.8),
        dict(material_theta=0.9, structural_signature=0.75, wave_activation=0.0),
    ],
)
def test_bound_bifurcation_fails_closed_on_temporal_or_realization_mismatch(kwargs):
    with pytest.raises(BoundNowBifurcationError):
        bind_now_bifurcation(
            _bound_marker(),
            activity=4.0,
            current=1.0,
            generator=_generator(),
            **kwargs,
        )


def test_bound_bifurcation_fails_closed_for_invalid_kinetic_pair():
    with pytest.raises(BoundNowBifurcationError):
        bind_now_bifurcation(
            _bound_marker(),
            material_theta=0.9,
            structural_signature=0.75,
            wave_activation=0.8,
            activity=1.0,
            current=1.0,
            generator=_generator(),
        )
