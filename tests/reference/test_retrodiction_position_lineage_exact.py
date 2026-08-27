from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_position_lineage_exact import (
    PositionLineageRetrodictionError,
    retrodict_kicks_from_position_lineage,
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


def _forward(initial, dts, kicks):
    receipts = [MemoryEventReceipt(dt, 1.0, kick) for dt, kick in zip(dts, kicks)]
    return replay_memory_orchorbital_lineage(initial, _attractors(), receipts)


def test_position_lineage_exactly_recovers_four_event_reference() -> None:
    initial = _initial()
    dts = [0.004, 0.003, 0.005, 0.0025]
    truth = [
        0.034 - 0.023j,
        -0.008 + 0.028j,
        0.011 + 0.006j,
        -0.017 - 0.009j,
    ]
    states, cells = _forward(initial, dts, truth)
    positions = [state.position for state in states[1:]]
    active = [cell.active_attractor for cell in cells]
    result = retrodict_kicks_from_position_lineage(
        initial,
        _attractors(),
        active,
        dts,
        positions,
    )
    assert result.status == "EXACT_POSITION_LINEAGE_RECOVERY"
    assert result.observation_dimension == result.latent_dimension == 2 * len(truth)
    assert np.linalg.norm(np.asarray(result.kicks) - np.asarray(truth)) < 1e-10
    assert result.max_position_residual < 1e-12
    for recovered, expected in zip(result.states, states):
        assert np.allclose(recovered.position, expected.position, atol=1e-11, rtol=0.0)
        assert np.allclose(recovered.velocity, expected.velocity, atol=1e-10, rtol=0.0)


def test_position_lineage_recovers_100_random_admitted_cases_up_to_six_events() -> None:
    rng = np.random.default_rng(20260827)
    recovered = 0
    attempts = 0
    while recovered < 100 and attempts < 240:
        attempts += 1
        n = int(rng.integers(1, 7))
        initial = MemoryPhaseState(
            position=np.array([-0.8, 0.4]) + rng.normal(scale=0.22, size=2),
            velocity=np.array([0.05, 0.2]) + rng.normal(scale=0.10, size=2),
            tau_internal=0.0,
            swept_area=0.0,
        )
        dts = [float(rng.uniform(0.001, 0.010)) for _ in range(n)]
        truth = [complex(*rng.normal(scale=0.065, size=2)) for _ in range(n)]
        try:
            states, cells = _forward(initial, dts, truth)
        except ValueError:
            continue
        result = retrodict_kicks_from_position_lineage(
            initial,
            _attractors(),
            [cell.active_attractor for cell in cells],
            dts,
            [state.position for state in states[1:]],
            position_tolerance=1e-8,
        )
        assert result.observation_dimension == result.latent_dimension == 2 * n
        assert np.linalg.norm(np.asarray(result.kicks) - np.asarray(truth)) < 1e-8
        assert result.max_position_residual < 1e-8
        recovered += 1
    assert recovered == 100


def test_wrong_active_sequence_fails_closed() -> None:
    initial = _initial()
    dts = [0.004, 0.003, 0.005]
    truth = [0.02 - 0.01j, -0.01 + 0.02j, 0.015 + 0.004j]
    states, cells = _forward(initial, dts, truth)
    active = [cell.active_attractor for cell in cells]
    replacements = [name for name in ("A", "B", "C") if name != active[0]]
    active[0] = replacements[0]
    with pytest.raises(PositionLineageRetrodictionError, match="active-attractor sequence"):
        retrodict_kicks_from_position_lineage(
            initial,
            _attractors(),
            active,
            dts,
            [state.position for state in states[1:]],
        )


def test_position_lineage_length_mismatch_fails_closed() -> None:
    with pytest.raises(PositionLineageRetrodictionError, match="equal length"):
        retrodict_kicks_from_position_lineage(
            _initial(),
            _attractors(),
            ["A", "A"],
            [0.01],
            [np.array([-0.69, 0.41]), np.array([-0.68, 0.42])],
        )


def test_nonpositive_delta_tau_fails_closed() -> None:
    with pytest.raises(PositionLineageRetrodictionError, match="strictly positive"):
        retrodict_kicks_from_position_lineage(
            _initial(),
            _attractors(),
            ["A"],
            [0.0],
            [np.array([-0.69, 0.41])],
        )


def test_unknown_active_attractor_fails_closed() -> None:
    with pytest.raises(PositionLineageRetrodictionError, match="unknown attractor"):
        retrodict_kicks_from_position_lineage(
            _initial(),
            _attractors(),
            ["missing"],
            [0.01],
            [np.array([-0.69, 0.41])],
        )
