import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState, specific_memory_energy, memory_angular_momentum
from src.idt.memory_recall import (
    MemoryEventReceipt,
    MemoryRecallError,
    apply_receipt_kick,
    event_invariant_signature,
    kepler_memory_inverse_step,
    memory_cycle_forward,
    memory_cycle_inverse,
    recall_memory_lineage,
    replay_memory_lineage,
)


def _state():
    return MemoryPhaseState(
        position=np.array([1.0, 0.0], dtype=float),
        velocity=np.array([0.0, 1.0], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _receipts():
    return [
        MemoryEventReceipt(0.011, 0.08, 0.030 + 0.010j),
        MemoryEventReceipt(0.013, 0.05, -0.020 + 0.015j),
        MemoryEventReceipt(0.009, 0.07, 0.010 - 0.025j),
    ]


def _assert_state_close(a, b, atol=2e-13):
    assert np.allclose(a.position, b.position, atol=atol, rtol=0.0)
    assert np.allclose(a.velocity, b.velocity, atol=atol, rtol=0.0)
    assert a.tau_internal == pytest.approx(b.tau_internal, abs=atol)
    assert a.swept_area == pytest.approx(b.swept_area, abs=atol)


def test_inverse_velocity_verlet_restores_state_and_bookkeeping():
    s0 = _state()
    receipt = _receipts()[0]
    s1 = memory_cycle_forward(s0, 1.0, receipt)
    kicked = apply_receipt_kick(s0, receipt)
    recovered_kicked = kepler_memory_inverse_step(s1, 1.0, receipt.delta_tau)
    _assert_state_close(recovered_kicked, kicked)


def test_one_memory_cycle_is_exactly_reconstructed_by_recorded_inverse():
    s0 = _state()
    receipt = _receipts()[0]
    s1 = memory_cycle_forward(s0, 1.0, receipt)
    recovered = memory_cycle_inverse(s1, 1.0, receipt)
    _assert_state_close(recovered, s0)


def test_multi_event_ledger_recall_reconstructs_initial_state():
    s0 = _state()
    receipts = _receipts()
    forward = replay_memory_lineage(s0, 1.0, receipts)
    recalled = recall_memory_lineage(forward[-1], 1.0, receipts)
    _assert_state_close(recalled[-1], s0, atol=5e-13)
    assert len(forward) == len(receipts) + 1
    assert len(recalled) == len(receipts) + 1


def test_recall_reconstructs_every_forward_checkpoint_in_reverse_order():
    s0 = _state()
    receipts = _receipts()
    forward = replay_memory_lineage(s0, 1.0, receipts)
    recalled = recall_memory_lineage(forward[-1], 1.0, receipts)
    for reverse_state, forward_state in zip(recalled, reversed(forward)):
        _assert_state_close(reverse_state, forward_state, atol=5e-13)


def test_ledger_order_is_structural_negative_control():
    s0 = _state()
    receipts = _receipts()
    final_state = replay_memory_lineage(s0, 1.0, receipts)[-1]
    wrongly_ordered = recall_memory_lineage(final_state, 1.0, list(reversed(receipts)))[-1]
    displacement = np.linalg.norm(wrongly_ordered.position - s0.position) + np.linalg.norm(wrongly_ordered.velocity - s0.velocity)
    assert displacement > 1e-6


def test_event_invariant_signature_matches_direct_before_after_values():
    s0 = _state()
    receipt = _receipts()[1]
    sig = event_invariant_signature(s0, 1.0, receipt)
    s1 = apply_receipt_kick(s0, receipt)
    assert sig.energy_before == pytest.approx(specific_memory_energy(s0.position, s0.velocity, 1.0))
    assert sig.energy_after == pytest.approx(specific_memory_energy(s1.position, s1.velocity, 1.0))
    assert sig.angular_momentum_before == pytest.approx(memory_angular_momentum(s0.position, s0.velocity))
    assert sig.angular_momentum_after == pytest.approx(memory_angular_momentum(s1.position, s1.velocity))


def test_empty_ledger_is_identity_reconstruction():
    s0 = _state()
    recalled = recall_memory_lineage(s0, 1.0, [])
    assert len(recalled) == 1
    _assert_state_close(recalled[0], s0)


def test_invalid_receipts_fail_closed():
    s0 = _state()
    with pytest.raises(MemoryRecallError):
        memory_cycle_forward(s0, 1.0, MemoryEventReceipt(0.0, 0.1, 0.1 + 0j))
    with pytest.raises(MemoryRecallError):
        memory_cycle_forward(s0, 1.0, MemoryEventReceipt(0.01, -0.1, 0.1 + 0j))
    with pytest.raises(MemoryRecallError):
        memory_cycle_forward(s0, 1.0, MemoryEventReceipt(0.01, 0.1, complex(float('nan'), 0.0)))
