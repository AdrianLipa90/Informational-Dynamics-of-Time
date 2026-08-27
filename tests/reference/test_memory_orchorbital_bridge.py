from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import (
    MemoryORCHORBITALBridgeError,
    ORCHORBITALMemoryCellReceipt,
    memory_orchorbital_cycle_inverse,
    recall_memory_orchorbital_lineage,
    replay_memory_orchorbital_lineage,
)
from src.idt.memory_recall import MemoryEventReceipt, apply_receipt_kick
from src.idt.orchorbital import AttractorSpec, evaluate_attractor_field


def _attractors():
    return [
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    ]


def _state():
    return MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _assert_state_close(a, b, atol=2e-12):
    assert np.allclose(a.position, b.position, atol=atol, rtol=0.0)
    assert np.allclose(a.velocity, b.velocity, atol=atol, rtol=0.0)
    assert a.tau_internal == pytest.approx(b.tau_internal, abs=atol)
    assert a.swept_area == pytest.approx(b.swept_area, abs=atol)


def test_velocity_only_memory_kick_preserves_active_attractor_until_leak() -> None:
    rng = np.random.default_rng(42)
    comparable = 0
    for _ in range(1000):
        state = MemoryPhaseState(
            position=np.array([-0.8, 0.3]) + rng.normal(scale=0.15, size=2),
            velocity=rng.normal(scale=0.2, size=2),
            tau_internal=0.0,
            swept_area=0.0,
        )
        before = evaluate_attractor_field(state, _attractors())
        receipt = MemoryEventReceipt(0.002, float(rng.uniform(0.0, 0.12)), complex(*rng.normal(scale=0.2, size=2)))
        after_state = apply_receipt_kick(state, receipt)
        after = evaluate_attractor_field(after_state, _attractors())
        if before.leak_mode or after.leak_mode:
            continue
        comparable += 1
        assert after.active_attractor == before.active_attractor
    assert comparable > 900


def test_memory_orchorbital_cell_roundtrip_uses_persisted_active_snapshot() -> None:
    receipt = MemoryEventReceipt(0.004, 0.08, 0.3 - 0.2j)
    states, cells = replay_memory_orchorbital_lineage(_state(), _attractors(), [receipt])
    reconstructed = memory_orchorbital_cycle_inverse(states[-1], cells[0])
    _assert_state_close(reconstructed, states[0])
    assert cells[0].active_attractor == "A"
    assert cells[0].active_center == pytest.approx((-1.5, 0.0), abs=0.0)
    assert cells[0].active_mu_memory == pytest.approx(3.2, abs=0.0)


def test_multicell_memory_orchorbital_lineage_recall_is_exact() -> None:
    receipts = [
        MemoryEventReceipt(0.002, 0.04, 0.05 + 0.02j),
        MemoryEventReceipt(0.003, 0.02, -0.03 + 0.04j),
        MemoryEventReceipt(0.0025, 0.05, 0.01 - 0.02j),
        MemoryEventReceipt(0.0015, 0.0, 0.07 + 0.03j),
    ]
    forward, cells = replay_memory_orchorbital_lineage(_state(), _attractors(), receipts)
    reverse = recall_memory_orchorbital_lineage(forward[-1], cells)
    _assert_state_close(reverse[-1], forward[0])
    for reverse_state, forward_state in zip(reverse, reversed(forward)):
        _assert_state_close(reverse_state, forward_state)


def test_zero_weight_receipt_propagates_smooth_orchorbital_segment() -> None:
    receipt = MemoryEventReceipt(0.003, 0.0, 1.2 - 0.7j)
    forward, cells = replay_memory_orchorbital_lineage(_state(), _attractors(), [receipt])
    reverse = recall_memory_orchorbital_lineage(forward[-1], cells)
    _assert_state_close(reverse[-1], forward[0])


def test_tampered_active_attractor_snapshot_breaks_inverse_negative_control() -> None:
    receipt = MemoryEventReceipt(0.004, 0.08, 0.3 - 0.2j)
    forward, cells = replay_memory_orchorbital_lineage(_state(), _attractors(), [receipt])
    good = cells[0]
    tampered = ORCHORBITALMemoryCellReceipt(
        memory_receipt=good.memory_receipt,
        active_attractor="B",
        active_center=(1.5, 0.0),
        active_mu_memory=2.7,
    )
    wrong = memory_orchorbital_cycle_inverse(forward[-1], tampered)
    mismatch = np.linalg.norm(wrong.position - forward[0].position) + np.linalg.norm(wrong.velocity - forward[0].velocity)
    assert mismatch > 1e-6


def test_large_velocity_kick_can_enter_leak_mode_fail_closed() -> None:
    state = MemoryPhaseState(
        position=np.array([0.0, 0.5]),
        velocity=np.array([0.0, 0.0]),
        tau_internal=0.0,
        swept_area=0.0,
    )
    receipt = MemoryEventReceipt(0.002, 20.0, 1.0 + 1.0j)
    with pytest.raises(MemoryORCHORBITALBridgeError):
        replay_memory_orchorbital_lineage(state, _attractors(), [receipt])


def test_invalid_persisted_snapshot_fails_closed() -> None:
    receipt = MemoryEventReceipt(0.002, 0.0, 0j)
    bad = ORCHORBITALMemoryCellReceipt(receipt, "A", (float("nan"), 0.0), 3.2)
    with pytest.raises(MemoryORCHORBITALBridgeError):
        memory_orchorbital_cycle_inverse(_state(), bad)
