from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec, centered_kepler_step, evaluate_attractor_field
from src.idt.retrodiction_finite_branch import (
    FiniteBranchRetrodictionError,
    kinetic_energy_from_basin_weights,
    retrodict_two_event_finite_branches,
)


def _initial() -> MemoryPhaseState:
    return MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _attractors():
    return [
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    ]


def _weights(state: MemoryPhaseState) -> np.ndarray:
    field = evaluate_attractor_field(state, _attractors())
    assert not field.leak_mode
    return np.asarray([ev.weight for ev in field.evaluations], dtype=float)


def _forward(kicks, dts=(0.004, 0.003), initial=None):
    current = _initial() if initial is None else initial
    states = [current]
    active = []
    for kick, dt in zip(kicks, dts):
        kicked = MemoryPhaseState(
            current.position.copy(),
            current.velocity + np.array([kick.real, kick.imag], dtype=float),
            current.tau_internal,
            current.swept_area,
        )
        field = evaluate_attractor_field(kicked, _attractors())
        assert not field.leak_mode
        spec = next(a for a in _attractors() if a.name == field.active_attractor)
        active.append(spec.name)
        current = centered_kepler_step(kicked, spec, dt)
        states.append(current)
    return states, active


def test_explicit_07h_reflection_pair_is_exhausted_and_earlier_weight_selects_truth():
    truth = [0.034 - 0.023j, -0.008 + 0.028j]
    states, active = _forward(truth)
    result = retrodict_two_event_finite_branches(
        _initial(), _attractors(), active[0], active[1], 0.004, 0.003,
        states[2].position, states[2].velocity[0], _weights(states[2]),
        "A", _weights(states[1])[0], equivalence_tolerance=1e-10,
    )
    assert result.status == "UNIQUE_FIXED_REGIME_TWO_EVENT"
    assert len(result.regular_candidates) == 2
    assert len(result.matching_candidates) == 1
    candidate = result.matching_candidates[0]
    assert abs(candidate.kick_first - truth[0]) < 1e-10
    assert abs(candidate.kick_second - truth[1]) < 1e-10
    alternate = next(c for c in result.regular_candidates if c != candidate)
    assert alternate.earlier_weight_residual > 1e-2


def test_final_basin_weights_reconstruct_final_kinetic_energy():
    states, _ = _forward([0.034 - 0.023j, -0.008 + 0.028j])
    inversion = kinetic_energy_from_basin_weights(
        states[2].position, _weights(states[2]), _attractors()
    )
    expected = 0.5 * float(np.dot(states[2].velocity, states[2].velocity))
    assert inversion.kinetic_energy == pytest.approx(expected, abs=1e-13)
    assert inversion.max_weight_residual < 1e-13


def test_500_nearby_cases_recover_one_exact_generating_branch():
    rng = np.random.default_rng(202608271141)
    for _ in range(500):
        initial = MemoryPhaseState(
            np.array([-0.7, 0.4]) + rng.normal(scale=0.05, size=2),
            np.array([0.05, 0.25]) + rng.normal(scale=0.04, size=2),
            0.0,
            0.0,
        )
        dts = (float(rng.uniform(0.002, 0.007)), float(rng.uniform(0.002, 0.007)))
        kicks = [
            complex(*rng.normal(scale=0.06, size=2)),
            complex(*rng.normal(scale=0.06, size=2)),
        ]
        states, active = _forward(kicks, dts, initial)
        result = retrodict_two_event_finite_branches(
            initial, _attractors(), active[0], active[1], dts[0], dts[1],
            states[2].position, states[2].velocity[0], _weights(states[2]),
            "A", _weights(states[1])[0], equivalence_tolerance=1e-8,
        )
        assert result.status == "UNIQUE_FIXED_REGIME_TWO_EVENT"
        candidate = result.matching_candidates[0]
        assert abs(candidate.kick_first - kicks[0]) < 1e-7
        assert abs(candidate.kick_second - kicks[1]) < 1e-7


def test_inconsistent_earlier_weight_is_fail_closed():
    truth = [0.034 - 0.023j, -0.008 + 0.028j]
    states, active = _forward(truth)
    result = retrodict_two_event_finite_branches(
        _initial(), _attractors(), active[0], active[1], 0.004, 0.003,
        states[2].position, states[2].velocity[0], _weights(states[2]),
        "A", 0.1, equivalence_tolerance=1e-10,
    )
    assert result.status == "INCONSISTENT_OBSERVATION"


def test_uniform_supported_weights_fail_closed_as_kinetic_degeneracy():
    with pytest.raises(FiniteBranchRetrodictionError, match="DEGENERATE"):
        kinetic_energy_from_basin_weights(
            [0.0, 0.2], [1.0 / 3.0] * 3, _attractors()
        )
