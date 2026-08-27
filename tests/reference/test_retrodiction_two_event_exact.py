from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_two_event_exact import (
    TwoEventExactRetrodictionError,
    retrodict_two_event_full_checkpoint,
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
    receipts = [
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip(dts, kicks)
    ]
    return replay_memory_orchorbital_lineage(initial, _attractors(), receipts)


def test_exact_two_event_reference_recovers_generating_kicks() -> None:
    dts = [0.004, 0.003]
    truth = [0.034 - 0.023j, -0.008 + 0.028j]
    states, cells = _forward(_initial(), dts, truth)
    audit = retrodict_two_event_full_checkpoint(
        _initial(), states[-1], _attractors(), dts
    )
    assert audit.status == "EXACT_UNIQUE_REFERENCE_BRANCH"
    assert audit.attractor_count == 3
    assert audit.enumerated_sequences == 9
    assert len(audit.candidates) == 1
    candidate = audit.candidates[0]
    assert candidate.active_sequence == tuple(cell.active_attractor for cell in cells)
    assert np.linalg.norm(np.asarray(candidate.kicks) - np.asarray(truth)) < 1e-11
    assert candidate.final_phase_residual < 1e-12


def test_exact_branch_enumeration_recovers_100_random_admitted_cases() -> None:
    rng = np.random.default_rng(20260827)
    recovered = 0
    attempts = 0
    while recovered < 100 and attempts < 200:
        attempts += 1
        initial = MemoryPhaseState(
            position=np.array([-0.8, 0.4]) + rng.normal(scale=0.25, size=2),
            velocity=np.array([0.05, 0.2]) + rng.normal(scale=0.12, size=2),
            tau_internal=0.0,
            swept_area=0.0,
        )
        dts = [float(rng.uniform(0.001, 0.012)), float(rng.uniform(0.001, 0.012))]
        kicks = [
            complex(*rng.normal(scale=0.08, size=2)),
            complex(*rng.normal(scale=0.08, size=2)),
        ]
        try:
            states, _ = _forward(initial, dts, kicks)
        except ValueError:
            continue
        audit = retrodict_two_event_full_checkpoint(
            initial,
            states[-1],
            _attractors(),
            dts,
            residual_tolerance=1e-8,
        )
        assert audit.status == "EXACT_UNIQUE_REFERENCE_BRANCH"
        assert len(audit.candidates) == 1
        assert np.linalg.norm(
            np.asarray(audit.candidates[0].kicks) - np.asarray(kicks)
        ) < 1e-8
        recovered += 1
    assert recovered == 100


def test_full_final_checkpoint_rejects_07g_reflection_branch() -> None:
    dts = [0.004, 0.003]
    truth = [0.034 - 0.023j, -0.008 + 0.028j]
    alternate = [
        complex(0.03399999999998063, 0.34071654937113033),
        complex(-0.00802729491823317, -0.8206629500579328),
    ]
    states, _ = _forward(_initial(), dts, truth)
    audit = retrodict_two_event_full_checkpoint(
        _initial(), states[-1], _attractors(), dts
    )
    recovered = np.asarray(audit.candidates[0].kicks)
    assert np.linalg.norm(recovered - np.asarray(truth)) < 1e-11
    assert np.linalg.norm(recovered - np.asarray(alternate)) > 0.5


def test_two_event_exact_gate_requires_exactly_two_positive_steps() -> None:
    with pytest.raises(TwoEventExactRetrodictionError, match="exactly two"):
        retrodict_two_event_full_checkpoint(
            _initial(), _initial(), _attractors(), [0.01]
        )
    with pytest.raises(TwoEventExactRetrodictionError, match="positive"):
        retrodict_two_event_full_checkpoint(
            _initial(), _initial(), _attractors(), [0.01, 0.0]
        )


def test_duplicate_attractor_names_fail_closed() -> None:
    bad = [
        AttractorSpec("A", np.array([-1.0, 0.0]), 2.0),
        AttractorSpec("A", np.array([1.0, 0.0]), 2.0),
    ]
    with pytest.raises(TwoEventExactRetrodictionError, match="unique"):
        retrodict_two_event_full_checkpoint(
            _initial(), _initial(), bad, [0.01, 0.01]
        )
