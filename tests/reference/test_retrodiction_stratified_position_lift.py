from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_orchorbital_residence_conditioning import (
    build_memory_orchorbital_residence_cells,
    residence_lineage_signature,
)
from src.idt.retrodiction_stratified_position_lift import (
    StratifiedPositionLiftError,
    active_sequence_stratum_key,
    active_sequences_are_cross_stratum_separated,
    certify_stratified_global_reduction,
    retrodict_from_retained_position_lift,
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


def _kicks():
    return (0.034 - 0.023j, -0.008 + 0.028j)


def _receipts():
    return tuple(
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip((0.004, 0.003), _kicks())
    )


def _signature_and_positions():
    cells = build_memory_orchorbital_residence_cells(
        _initial(), _attractors(), _receipts()
    )
    signature = residence_lineage_signature(cells)
    states, _ = replay_memory_orchorbital_lineage(
        _initial(), _attractors(), _receipts()
    )
    positions = tuple(np.asarray(state.position, dtype=float) for state in states[1:])
    return signature, positions


def test_active_sequence_is_an_exact_stratum_key() -> None:
    assert active_sequence_stratum_key(("A", "B", "A")) == ("A", "B", "A")
    assert active_sequence_stratum_key((" A ", "B")) == ("A", "B")


def test_unequal_active_sequences_are_cross_stratum_separated() -> None:
    assert active_sequences_are_cross_stratum_separated(("A", "B"), ("A", "C"))
    assert not active_sequences_are_cross_stratum_separated(("A", "B"), ("A", "B"))


def test_stratified_certificate_reduces_global_problem_to_fixed_sequence_lift() -> None:
    certificate = certify_stratified_global_reduction(("A", "B", "A"), (0.1, 0.2, 0.3))
    assert certificate.event_count == 3
    assert certificate.latent_dimension == 6
    assert certificate.position_lineage_dimension == 6
    assert certificate.cross_sequence_separator == "RETAINED_ACTIVE_SEQUENCE_EXACT"
    assert certificate.fixed_sequence_inverse == "07K_EXACT_POSITION_LINEAGE_RECOVERY"
    assert certificate.remaining_requirement == "Y_AUG_TO_ORDERED_POSITION_LINEAGE_LIFT_PER_FIXED_SEQUENCE_STRATUM"
    assert certificate.status == "GLOBAL_INJECTIVITY_REDUCED_TO_FIXED_SEQUENCE_POSITION_LIFT"


def test_constructive_composition_recovers_real_kicks_from_retained_stratum_and_position_lift() -> None:
    signature, positions = _signature_and_positions()
    result = retrodict_from_retained_position_lift(
        _initial(),
        _attractors(),
        signature,
        (0.004, 0.003),
        positions,
        position_tolerance=1e-9,
    )
    assert result.active_sequence == signature.active_sequence
    assert result.position_lineage_dimension == 4
    assert result.recovered.status == "EXACT_POSITION_LINEAGE_RECOVERY"
    assert result.recovered.observation_dimension == 4
    assert result.recovered.latent_dimension == 4
    assert result.recovered.max_position_residual <= 1e-9
    assert np.allclose(
        np.asarray(result.recovered.kicks, dtype=complex),
        np.asarray(_kicks(), dtype=complex),
        rtol=0.0,
        atol=1e-10,
    )
    assert result.status == "CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_RECOVERY"


def test_tampered_position_lineage_decodes_to_a_different_same_stratum_history() -> None:
    signature, positions = _signature_and_positions()
    tampered = [np.array(value, dtype=float, copy=True) for value in positions]
    tampered[-1][0] += 1e-4
    result = retrodict_from_retained_position_lift(
        _initial(),
        _attractors(),
        signature,
        (0.004, 0.003),
        tampered,
        position_tolerance=1e-10,
    )
    assert result.active_sequence == signature.active_sequence
    assert result.recovered.status == "EXACT_POSITION_LINEAGE_RECOVERY"
    assert result.recovered.max_position_residual <= 1e-10
    assert not np.allclose(
        np.asarray(result.recovered.kicks, dtype=complex),
        np.asarray(_kicks(), dtype=complex),
        rtol=0.0,
        atol=1e-10,
    )


def test_sequence_elapsed_length_mismatch_fails_closed() -> None:
    with pytest.raises(StratifiedPositionLiftError, match="equal length"):
        certify_stratified_global_reduction(("A", "B"), (0.1,))


def test_nonpositive_elapsed_increment_fails_closed() -> None:
    with pytest.raises(StratifiedPositionLiftError, match="strictly positive"):
        certify_stratified_global_reduction(("A", "B"), (0.1, 0.0))


def test_empty_attractor_label_fails_closed() -> None:
    with pytest.raises(StratifiedPositionLiftError, match="non-empty"):
        active_sequence_stratum_key(("A", " "))
