import math

import numpy as np
import pytest

from src.idt.event_memory_kick import derived_memory_kick
from src.idt.kahler_memory_frame import (
    fs_distance_cp1,
    initial_cp1_memory_frame,
    parallel_transport_cp1_frame,
    project_cp1_event,
    qubit_bloch,
)
from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_recall import MemoryEventReceipt, recall_memory_lineage, replay_memory_lineage


def _qubit(polar_angle, phase=0.0):
    return np.array(
        [
            math.cos(polar_angle / 2.0),
            np.exp(1j * phase) * math.sin(polar_angle / 2.0),
        ],
        dtype=complex,
    )


def _memory_state():
    return MemoryPhaseState(
        position=np.array([1.0, 0.0], dtype=float),
        velocity=np.array([0.0, 1.0], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _assert_state_close(a, b, atol=1e-12):
    assert np.allclose(a.position, b.position, atol=atol, rtol=0.0)
    assert np.allclose(a.velocity, b.velocity, atol=atol, rtol=0.0)
    assert a.tau_internal == pytest.approx(b.tau_internal, abs=atol)
    assert a.swept_area == pytest.approx(b.swept_area, abs=atol)


def _two_cp1_receipts():
    psi_a = _qubit(0.0)
    psi_b = _qubit(0.4)
    psi_c = _qubit(0.55, 0.35)

    n_a = qubit_bloch(psi_a)
    n_b = qubit_bloch(psi_b)
    n_c = qubit_bloch(psi_c)

    frame_a = initial_cp1_memory_frame(n_a, n_b)
    delta_m_1 = project_cp1_event(frame_a, n_b)

    frame_b = parallel_transport_cp1_frame(frame_a, n_b)
    delta_m_2 = project_cp1_event(frame_b, n_c)

    receipts = [
        MemoryEventReceipt(0.011, 0.08, delta_m_1),
        MemoryEventReceipt(0.013, 0.06, delta_m_2),
    ]
    return (psi_a, psi_b, psi_c), (n_a, n_b, n_c), (frame_a, frame_b), receipts


def test_cp1_geometry_to_memory_receipt_preserves_fs_normalization():
    _, (n_a, n_b, n_c), (_, frame_b), receipts = _two_cp1_receipts()
    assert abs(receipts[0].delta_m) == pytest.approx(fs_distance_cp1(n_a, n_b), abs=1e-13)
    assert abs(receipts[1].delta_m) == pytest.approx(fs_distance_cp1(n_b, n_c), abs=1e-13)


def test_upstream_event_weight_sets_kick_magnitude_without_extra_gain():
    _, (n_a, n_b, _), _, receipts = _two_cp1_receipts()
    rec = receipts[0]
    kick = derived_memory_kick(rec.delta_m, rec.event_weight)
    assert abs(kick) == pytest.approx(rec.event_weight * fs_distance_cp1(n_a, n_b), abs=1e-13)
    assert kick == pytest.approx(rec.event_weight * rec.delta_m, abs=1e-13)


def test_cp1_event_to_kepler_lineage_to_recall_is_end_to_end_reversible():
    _, _, _, receipts = _two_cp1_receipts()
    initial = _memory_state()
    forward = replay_memory_lineage(initial, 1.0, receipts)
    reconstructed = recall_memory_lineage(forward[-1], 1.0, receipts)
    _assert_state_close(reconstructed[-1], initial, atol=1e-12)
    for reverse_state, forward_state in zip(reconstructed, reversed(forward)):
        _assert_state_close(reverse_state, forward_state, atol=1e-12)


def test_tampered_event_receipt_breaks_reconstruction_negative_control():
    _, _, _, receipts = _two_cp1_receipts()
    initial = _memory_state()
    final_state = replay_memory_lineage(initial, 1.0, receipts)[-1]
    tampered = [
        MemoryEventReceipt(receipts[0].delta_tau, 1.1 * receipts[0].event_weight, receipts[0].delta_m),
        receipts[1],
    ]
    reconstructed = recall_memory_lineage(final_state, 1.0, tampered)[-1]
    mismatch = np.linalg.norm(reconstructed.position - initial.position) + np.linalg.norm(reconstructed.velocity - initial.velocity)
    assert mismatch > 1e-6


def test_global_phase_change_upstream_leaves_admitted_cp1_receipt_geometry_unchanged():
    (psi_a, psi_b, _), (n_a, n_b, _), _, receipts = _two_cp1_receipts()
    n_a_phase = qubit_bloch(psi_a * np.exp(0.73j))
    n_b_phase = qubit_bloch(psi_b * np.exp(-1.21j))
    frame_phase = initial_cp1_memory_frame(n_a_phase, n_b_phase)
    delta_m_phase = project_cp1_event(frame_phase, n_b_phase)
    assert np.allclose(n_a_phase, n_a, atol=1e-13, rtol=0.0)
    assert np.allclose(n_b_phase, n_b, atol=1e-13, rtol=0.0)
    assert delta_m_phase == pytest.approx(receipts[0].delta_m, abs=1e-13)


def test_zero_weight_event_keeps_smooth_lineage_reversible():
    _, _, _, receipts = _two_cp1_receipts()
    initial = _memory_state()
    zero_event = MemoryEventReceipt(0.007, 0.0, receipts[0].delta_m)
    forward = replay_memory_lineage(initial, 1.0, [zero_event])
    reconstructed = recall_memory_lineage(forward[-1], 1.0, [zero_event])
    _assert_state_close(reconstructed[-1], initial, atol=1e-12)
