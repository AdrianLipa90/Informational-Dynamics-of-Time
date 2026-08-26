import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import (
    AttractorSpec,
    ORCHORBITALError,
    centered_kepler_step,
    evaluate_attractor_field,
    orchorbital_step,
    phase_space_closure_defect,
    winding_increment,
)


def _state(x, y, vx, vy):
    return MemoryPhaseState(
        np.array([x, y], dtype=float),
        np.array([vx, vy], dtype=float),
        0.0,
        0.0,
    )


def _attractors():
    return [
        AttractorSpec("A", np.array([0.0, 0.0], dtype=float), 1.0),
        AttractorSpec("B", np.array([5.0, 0.0], dtype=float), 0.8),
    ]


def test_binding_weights_normalize_and_select_strongest_attractor():
    field = evaluate_attractor_field(_state(1.0, 0.0, 0.0, 0.7), _attractors())
    assert not field.leak_mode
    assert field.active_attractor == "A"
    assert abs(sum(item.weight for item in field.evaluations) - 1.0) < 1e-12
    assert 0.0 <= field.attractor_coherence <= 1.0


def test_symmetric_two_attractor_state_has_one_bit_entropy_and_zero_coherence():
    attractors = [
        AttractorSpec("A", np.array([0.0, 0.0], dtype=float), 1.0),
        AttractorSpec("B", np.array([2.0, 0.0], dtype=float), 1.0),
    ]
    field = evaluate_attractor_field(_state(1.0, 0.0, 0.0, 0.0), attractors)
    assert field.active_attractor == "A"
    assert abs(field.evaluations[0].weight - 0.5) < 1e-12
    assert abs(field.evaluations[1].weight - 0.5) < 1e-12
    assert abs(field.attractor_entropy_bits - 1.0) < 1e-12
    assert abs(field.attractor_coherence) < 1e-12


def test_leak_mode_when_no_attractor_has_negative_specific_energy():
    field = evaluate_attractor_field(_state(2.5, 8.0, 10.0, 10.0), _attractors())
    assert field.leak_mode
    assert field.active_attractor is None
    assert all(item.weight == 0.0 for item in field.evaluations)
    assert field.attractor_entropy_bits is None
    assert field.attractor_coherence is None


def test_centered_kepler_translation_covariance():
    shifted = _state(3.0, 2.0, -0.2, 0.5)
    shifted_attractor = AttractorSpec("C", np.array([2.0, 2.0], dtype=float), 1.2)
    shifted_out = centered_kepler_step(shifted, shifted_attractor, 0.01)

    origin = _state(1.0, 0.0, -0.2, 0.5)
    origin_attractor = AttractorSpec("O", np.array([0.0, 0.0], dtype=float), 1.2)
    origin_out = centered_kepler_step(origin, origin_attractor, 0.01)

    assert np.allclose(shifted_out.position - shifted_attractor.center, origin_out.position, atol=1e-13)
    assert np.allclose(shifted_out.velocity, origin_out.velocity, atol=1e-13)


def test_winding_increment_for_quarter_turn():
    result = winding_increment([1.0, 0.0], [0.0, 1.0], [0.0, 0.0])
    assert abs(result - 0.25) < 1e-12


def test_orchorbital_step_uses_one_active_center_and_tracks_winding():
    result = orchorbital_step(_state(1.0, 0.0, 0.0, 0.8), _attractors(), 0.02)
    assert result.active_attractor == "A"
    assert result.state_after.tau_internal > 0.0
    assert result.winding_increment > 0.0


def test_leak_mode_fails_closed_before_orbital_propagation():
    with pytest.raises(ORCHORBITALError, match="LEAK_MODE"):
        orchorbital_step(_state(2.5, 8.0, 10.0, 10.0), _attractors(), 0.02)


def test_phase_space_closure_defect_is_zero_for_identical_states():
    state = _state(1.0, 2.0, 3.0, 4.0)
    assert phase_space_closure_defect(
        state,
        state,
        position_scale=1.0,
        velocity_scale=1.0,
    ) == 0.0
