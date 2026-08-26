import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_recall import MemoryEventReceipt, memory_cycle_forward
from src.idt.retrodiction import (
    RetrodictionError,
    equivalent_kick_factorization,
    infer_event_weight_from_known_imprint,
    infer_imprint_from_known_event_weight,
    infer_missing_kick,
    retrodict_single_missing_receipt,
)


def _state():
    return MemoryPhaseState(
        np.array([1.2, 0.3], dtype=float),
        np.array([-0.1, 0.7], dtype=float),
        0.4,
        -0.2,
    )


def _receipt():
    return MemoryEventReceipt(0.03, 0.4, 0.02 + 0.05j)


def test_missing_kick_is_recovered_by_reversing_only_smooth_segment():
    s0 = _state()
    rec = _receipt()
    s1 = memory_cycle_forward(s0, 1.1, rec)
    inferred = infer_missing_kick(s0, s1, 1.1, rec.delta_tau)
    assert abs(inferred.delta_velocity - rec.event_weight * rec.delta_m) < 1e-13
    assert inferred.checkpoint_residual < 1e-13


def test_event_weight_is_identifiable_when_nonzero_imprint_is_known():
    s0 = _state()
    rec = _receipt()
    s1 = memory_cycle_forward(s0, 1.1, rec)
    inferred = retrodict_single_missing_receipt(
        s0,
        s1,
        1.1,
        rec.delta_tau,
        known_delta_m=rec.delta_m,
    )
    assert inferred.mode == "EVENT_WEIGHT_FROM_KNOWN_IMPRINT"
    assert abs(inferred.receipt.event_weight - rec.event_weight) < 1e-13
    assert abs(inferred.receipt.delta_m - rec.delta_m) < 1e-15
    assert inferred.factorization_residual < 1e-13


def test_imprint_is_identifiable_when_positive_event_weight_is_known():
    s0 = _state()
    rec = _receipt()
    s1 = memory_cycle_forward(s0, 1.1, rec)
    inferred = retrodict_single_missing_receipt(
        s0,
        s1,
        1.1,
        rec.delta_tau,
        known_event_weight=rec.event_weight,
    )
    assert inferred.mode == "IMPRINT_FROM_KNOWN_EVENT_WEIGHT"
    assert abs(inferred.receipt.delta_m - rec.delta_m) < 1e-13
    assert abs(inferred.receipt.event_weight - rec.event_weight) < 1e-15


def test_product_only_ambiguity_fails_closed_without_independent_factor():
    s0 = _state()
    rec = _receipt()
    s1 = memory_cycle_forward(s0, 1.1, rec)
    with pytest.raises(RetrodictionError, match="product-only ambiguity"):
        retrodict_single_missing_receipt(s0, s1, 1.1, rec.delta_tau)


def test_wrong_imprint_direction_fails_collinearity_control():
    dv = 0.02 + 0.04j
    with pytest.raises(RetrodictionError, match="not collinear"):
        infer_event_weight_from_known_imprint(dv, 0.03 - 0.01j, residual_tol=1e-12)


def test_zero_weight_and_zero_kick_have_unique_zero_reference_imprint():
    assert infer_imprint_from_known_event_weight(0.0j, 0.0) == 0.0j
    with pytest.raises(RetrodictionError, match="incompatible with zero event weight"):
        infer_imprint_from_known_event_weight(0.01j, 0.0)


def test_checkpoint_tampering_fails_closed():
    s0 = _state()
    rec = _receipt()
    s1 = memory_cycle_forward(s0, 1.1, rec)
    tampered = MemoryPhaseState(s0.position + np.array([1e-3, 0.0]), s0.velocity, s0.tau_internal, s0.swept_area)
    with pytest.raises(RetrodictionError, match="checkpoint is inconsistent"):
        infer_missing_kick(tampered, s1, 1.1, rec.delta_tau, checkpoint_tol=1e-8)


def test_product_factorization_scale_family_preserves_the_kick():
    rec = _receipt()
    q_alt, dm_alt = equivalent_kick_factorization(rec.event_weight, rec.delta_m, 3.7)
    assert abs(q_alt * dm_alt - rec.event_weight * rec.delta_m) < 1e-15
