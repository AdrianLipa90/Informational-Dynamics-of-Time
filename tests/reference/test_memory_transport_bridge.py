from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_recall import recall_memory_lineage, replay_memory_lineage
from src.idt.memory_transport_bridge import (
    TransportMemoryBridgeError,
    transport_memory_admission,
    transport_memory_kick,
)


def _state() -> MemoryPhaseState:
    return MemoryPhaseState(
        position=np.array([1.3, -0.2], dtype=float),
        velocity=np.array([0.1, 0.75], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def test_active_transport_event_builds_memory_receipt_without_new_gain() -> None:
    admission = transport_memory_admission(
        activity=2.4,
        delta_lambda=0.01,
        structural_signature=0.3,
        wave_activation=1.7,
        delta_m=0.4 - 0.2j,
        reference_activity=1.2,
    )
    assert admission.realized
    assert admission.receipt.delta_tau == pytest.approx(0.02, abs=1e-15)
    assert admission.receipt.event_weight == pytest.approx(0.3, abs=0.0)
    assert transport_memory_kick(admission) == pytest.approx(0.3 * (0.4 - 0.2j), abs=1e-15)


def test_wave_inactive_event_keeps_smooth_duration_but_zero_kick() -> None:
    admission = transport_memory_admission(
        activity=1.8,
        delta_lambda=0.02,
        structural_signature=0.5,
        wave_activation=0.0,
        delta_m=0.2 + 0.1j,
    )
    assert not admission.realized
    assert admission.receipt.delta_tau == pytest.approx(0.036, abs=1e-15)
    assert admission.receipt.event_weight == 0.0
    assert transport_memory_kick(admission) == 0j


def test_wave_rescaling_preserves_admission_and_memory_kick() -> None:
    base = transport_memory_admission(2.0, 0.01, 0.4, 0.7, 0.3 + 0.2j)
    scaled = transport_memory_admission(2.0, 0.01, 0.4, 49.0 * 0.7, 0.3 + 0.2j)
    assert base.realized and scaled.realized
    assert scaled.receipt.event_weight == base.receipt.event_weight
    assert transport_memory_kick(scaled) == pytest.approx(transport_memory_kick(base), abs=0.0)
    assert scaled.realized_now_weight != base.realized_now_weight


def test_internal_elapsed_is_invariant_under_increasing_reparameterization() -> None:
    rng = np.random.default_rng(12)
    for _ in range(1000):
        activity = float(np.exp(rng.uniform(-3.0, 3.0)))
        delta_lambda = float(np.exp(rng.uniform(-6.0, -1.0)))
        reference = float(np.exp(rng.uniform(-2.0, 2.0)))
        jacobian = float(np.exp(rng.uniform(-3.0, 3.0)))
        a = transport_memory_admission(activity, delta_lambda, 0.4, 0.9, 0.2j, reference_activity=reference)
        b = transport_memory_admission(activity / jacobian, delta_lambda * jacobian, 0.4, 0.9, 0.2j, reference_activity=reference)
        assert b.receipt.delta_tau == pytest.approx(a.receipt.delta_tau, rel=0.0, abs=2e-14)


def test_transport_derived_receipts_replay_and_recall_existing_memory_cell() -> None:
    specs = [
        (1.7, 0.004, 0.08, 0.9, 0.12 + 0.04j),
        (2.1, 0.003, 0.06, 1.3, -0.03 + 0.09j),
        (1.4, 0.005, 0.11, 0.0, 0.07 - 0.02j),
    ]
    receipts = [transport_memory_admission(*spec).receipt for spec in specs]
    initial = _state()
    forward = replay_memory_lineage(initial, 1.0, receipts)
    reverse = recall_memory_lineage(forward[-1], 1.0, receipts)
    recovered = reverse[-1]
    assert np.allclose(recovered.position, initial.position, atol=2e-12, rtol=0.0)
    assert np.allclose(recovered.velocity, initial.velocity, atol=2e-12, rtol=0.0)
    assert recovered.tau_internal == pytest.approx(initial.tau_internal, abs=2e-12)
    assert recovered.swept_area == pytest.approx(initial.swept_area, abs=2e-12)


def test_product_realized_weight_is_normalization_sensitive_negative_control() -> None:
    q = 0.4
    eps = 0.3
    scale = 5.0
    base = transport_memory_admission(1.0, 0.01, q, eps, 0.2 + 0.1j)
    scaled = transport_memory_admission(1.0, 0.01, q, scale * scale * eps, 0.2 + 0.1j)
    assert scaled.realized_now_weight == pytest.approx(scale * scale * base.realized_now_weight)
    assert transport_memory_kick(scaled) == pytest.approx(transport_memory_kick(base), abs=0.0)


def test_fail_closed_invalid_bridge_inputs() -> None:
    with pytest.raises(TransportMemoryBridgeError):
        transport_memory_admission(1.0, 0.01, -0.1, 1.0, 0j)
    with pytest.raises(TransportMemoryBridgeError):
        transport_memory_admission(1.0, 0.01, 0.1, -1.0, 0j)
    with pytest.raises(TransportMemoryBridgeError):
        transport_memory_admission(0.0, 0.01, 0.1, 1.0, 0j)
    with pytest.raises(TransportMemoryBridgeError):
        transport_memory_admission(1.0, 0.0, 0.1, 1.0, 0j)
    with pytest.raises(TransportMemoryBridgeError):
        transport_memory_admission(1.0, 0.01, 0.1, 1.0, complex(math.inf, 0.0))
