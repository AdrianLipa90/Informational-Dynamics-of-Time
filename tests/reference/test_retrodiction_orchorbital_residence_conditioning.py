from __future__ import annotations

from dataclasses import replace

import math
import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_global_null_gate import ScalarCheckpointObservation
from src.idt.retrodiction_orchorbital_residence_conditioning import (
    RetrodictionResidenceConditioningError,
    audit_known_null_residence_conditioning,
    build_memory_orchorbital_residence_cells,
    residence_lineage_signature,
    verify_memory_orchorbital_residence_cells,
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


def _truth():
    return [0.034 - 0.023j, -0.008 + 0.028j]


def _alternate():
    return [
        complex(0.03399999999998063, 0.34071654937113033),
        complex(-0.00802729491823317, -0.8206629500579328),
    ]


def _base_specs():
    return [
        ScalarCheckpointObservation(2, "rx"),
        ScalarCheckpointObservation(2, "ry"),
        ScalarCheckpointObservation(2, "vx"),
        ScalarCheckpointObservation(2, "weight", "A"),
        ScalarCheckpointObservation(2, "weight", "B"),
        ScalarCheckpointObservation(2, "weight", "C"),
    ]


def _receipts(kicks):
    return tuple(
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip((0.004, 0.003), kicks)
    )


def test_event_aware_bridge_chains_pre_event_states_across_memory_kicks() -> None:
    cells = build_memory_orchorbital_residence_cells(
        _initial(), _attractors(), _receipts(_truth())
    )
    verify_memory_orchorbital_residence_cells(cells)
    assert len(cells) == 2
    assert cells[0].residence_receipt.state_after_sha256 == cells[1].state_before_event_sha256
    assert cells[1].state_before_event_sha256 != cells[1].residence_receipt.state_before_sha256
    assert cells[1].previous_cell_sha256 == cells[0].cell_sha256


def test_event_aware_bridge_reuses_genesis_residence_receipt_per_smooth_segment() -> None:
    cells = build_memory_orchorbital_residence_cells(
        _initial(), _attractors(), _receipts(_truth())
    )
    for cell in cells:
        assert cell.residence_receipt.index == 0
        assert cell.residence_receipt.previous_receipt_sha256 is None
        assert cell.residence_receipt.delta_tau_hex == cell.memory_delta_tau_hex


def test_event_residence_cell_tamper_breaks_content_commitment() -> None:
    cells = build_memory_orchorbital_residence_cells(
        _initial(), _attractors(), _receipts(_truth())
    )
    tampered = replace(
        cells[0],
        memory_delta_m_imag_hex=float.fromhex(cells[0].memory_delta_m_imag_hex).__add__(0.001).hex(),
    )
    with pytest.raises(RetrodictionResidenceConditioningError, match="content hash mismatch"):
        verify_memory_orchorbital_residence_cells((tampered,))


def test_known_reflection_null_keeps_same_active_residence_labels() -> None:
    audit = audit_known_null_residence_conditioning(
        _initial(),
        _attractors(),
        (0.004, 0.003),
        _truth(),
        _alternate(),
        _base_specs(),
        equivalence_tolerance=1e-10,
    )
    assert audit.base_residual < 1e-12
    assert audit.latent_separation > 0.9
    assert audit.active_labels_equivalent
    assert audit.reference_signature.active_sequence == audit.alternate_signature.active_sequence


def test_known_reflection_null_residence_status_excludes_provenance_hash_oracle() -> None:
    audit = audit_known_null_residence_conditioning(
        _initial(),
        _attractors(),
        (0.004, 0.003),
        _truth(),
        _alternate(),
        _base_specs(),
        equivalence_tolerance=1e-10,
    )
    assert not audit.provenance_heads_equal
    assert audit.switch_lineage_equivalent
    assert audit.status == "KNOWN_NULL_PERSISTS_UNDER_RESIDENCE_LABELS"


def test_winding_is_reported_as_independent_continuous_diagnostic() -> None:
    audit = audit_known_null_residence_conditioning(
        _initial(),
        _attractors(),
        (0.004, 0.003),
        _truth(),
        _alternate(),
        _base_specs(),
        equivalence_tolerance=1e-10,
    )
    assert math.isfinite(audit.winding_residual)
    assert audit.winding_residual >= 0.0


def test_identical_latent_history_is_rejected_before_residence_conditioning() -> None:
    with pytest.raises(RetrodictionResidenceConditioningError, match="distinct"):
        audit_known_null_residence_conditioning(
            _initial(),
            _attractors(),
            (0.004, 0.003),
            _truth(),
            _truth(),
            _base_specs(),
        )


def test_empty_memory_event_lineage_fails_closed() -> None:
    with pytest.raises(RetrodictionResidenceConditioningError, match="non-empty"):
        build_memory_orchorbital_residence_cells(_initial(), _attractors(), ())


def test_mismatched_delta_tau_and_kick_count_fails_closed() -> None:
    with pytest.raises(RetrodictionResidenceConditioningError, match="match the kick count"):
        audit_known_null_residence_conditioning(
            _initial(),
            _attractors(),
            (0.004,),
            _truth(),
            _alternate(),
            _base_specs(),
        )
