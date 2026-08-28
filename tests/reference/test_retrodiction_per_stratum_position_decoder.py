from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    sparse_orchorbital_observation,
)
from src.idt.retrodiction_orchorbital_residence_conditioning import (
    build_memory_orchorbital_residence_cells,
    residence_lineage_signature,
)
from src.idt.retrodiction_per_stratum_position_decoder import (
    PerStratumPositionDecoderError,
    PositionFiberCoordinate,
    decode_per_stratum_position_lineage,
    missing_position_fiber_labels,
    required_position_labels,
)
from src.idt.retrodiction_stratified_position_lift import (
    retrodict_from_retained_position_lift,
)


def _initial() -> MemoryPhaseState:
    return MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _attractors() -> tuple[AttractorSpec, ...]:
    return (
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    )


def _dts() -> tuple[float, ...]:
    return (0.004, 0.003, 0.005)


def _kicks() -> tuple[complex, ...]:
    return (
        0.034 - 0.023j,
        -0.008 + 0.028j,
        0.012 + 0.006j,
    )


def _receipts() -> tuple[MemoryEventReceipt, ...]:
    return tuple(
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip(_dts(), _kicks())
    )


def _reference_data():
    initial = _initial()
    attractors = _attractors()
    cells = build_memory_orchorbital_residence_cells(initial, attractors, _receipts())
    signature = residence_lineage_signature(cells)
    states, _ = replay_memory_orchorbital_lineage(initial, attractors, _receipts())
    positions = np.asarray([state.position for state in states[1:]], dtype=float)

    base_specs = (
        ScalarCheckpointObservation(3, "rx"),
        ScalarCheckpointObservation(3, "ry"),
        ScalarCheckpointObservation(3, "vx"),
    )
    base_values = sparse_orchorbital_observation(
        initial,
        attractors,
        _dts(),
        _kicks(),
        base_specs,
    )
    fibers = tuple(
        PositionFiberCoordinate(k, axis, positions[k - 1, axis_index])
        for k in (1, 2)
        for axis_index, axis in enumerate(("x", "y"))
    )
    return signature, positions, base_specs, base_values, fibers


def test_required_position_labels_are_ordered_complete_carrier_labels() -> None:
    assert required_position_labels(3) == (
        "r1x", "r1y", "r2x", "r2y", "r3x", "r3y"
    )


def test_missing_fiber_labels_account_for_base_final_position() -> None:
    signature, _, base_specs, base_values, _ = _reference_data()
    assert missing_position_fiber_labels(
        signature.active_sequence, base_specs, base_values
    ) == ("r1x", "r1y", "r2x", "r2y")


@pytest.mark.parametrize("event_count", [1, 2, 3, 5, 8])
def test_final_position_base_schedule_has_exact_2n_minus_2_fiber_budget(
    event_count: int,
) -> None:
    active_sequence = tuple("A" for _ in range(event_count))
    base_specs = (
        ScalarCheckpointObservation(event_count, "rx"),
        ScalarCheckpointObservation(event_count, "ry"),
    )
    missing = missing_position_fiber_labels(
        active_sequence,
        base_specs,
        (0.0, 0.0),
    )
    assert len(missing) == 2 * event_count - 2
    assert missing == tuple(
        f"r{k}{axis}"
        for k in range(1, event_count)
        for axis in ("x", "y")
    )


def test_exact_decoder_assembles_real_ordered_position_lineage() -> None:
    signature, positions, base_specs, base_values, fibers = _reference_data()
    decoded = decode_per_stratum_position_lineage(
        signature.active_sequence,
        base_specs,
        base_values,
        fibers,
    )
    assert decoded.status == "EXACT_PER_STRATUM_POSITION_DECODER"
    assert decoded.event_count == 3
    assert decoded.active_sequence == signature.active_sequence
    assert decoded.base_position_labels == ("r3x", "r3y")
    assert decoded.fiber_position_labels == ("r1x", "r1y", "r2x", "r2y")
    assert np.array_equal(decoded.position_lineage, positions)


def test_exact_decoder_composes_with_07k_to_recover_real_kicks() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    decoded = decode_per_stratum_position_lineage(
        signature.active_sequence,
        base_specs,
        base_values,
        fibers,
    )
    recovered = retrodict_from_retained_position_lift(
        _initial(),
        _attractors(),
        signature,
        _dts(),
        decoded.position_lineage,
        position_tolerance=1e-9,
    )
    assert recovered.status == "CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_RECOVERY"
    assert np.allclose(
        np.asarray(recovered.recovered.kicks, dtype=complex),
        np.asarray(_kicks(), dtype=complex),
        rtol=0.0,
        atol=1e-10,
    )


def test_missing_position_coordinate_fails_closed() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    with pytest.raises(PerStratumPositionDecoderError, match="missing: r2y"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            fibers[:-1],
        )


def test_base_and_fiber_overlap_fails_closed() -> None:
    signature, positions, base_specs, base_values, fibers = _reference_data()
    overlap = fibers + (PositionFiberCoordinate(3, "x", positions[2, 0]),)
    with pytest.raises(PerStratumPositionDecoderError, match="both base record and fiber"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            overlap,
        )


def test_duplicate_fiber_coordinate_fails_closed() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    duplicate = fibers + (fibers[0],)
    with pytest.raises(PerStratumPositionDecoderError, match="duplicate position fiber"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            duplicate,
        )


def test_out_of_range_or_invalid_axis_fails_closed() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    with pytest.raises(PerStratumPositionDecoderError, match=r"\[1,event_count\]"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            fibers + (PositionFiberCoordinate(4, "x", 0.0),),
        )
    with pytest.raises(PerStratumPositionDecoderError, match="axis must be x or y"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            fibers + (PositionFiberCoordinate(1, "z", 0.0),),
        )


def test_nonfinite_coordinate_fails_closed() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    bad = list(fibers)
    bad[0] = PositionFiberCoordinate(1, "x", float("nan"))
    with pytest.raises(PerStratumPositionDecoderError, match="finite scalar"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values,
            bad,
        )


def test_base_vector_length_and_empty_stratum_fail_closed() -> None:
    signature, _, base_specs, base_values, fibers = _reference_data()
    with pytest.raises(PerStratumPositionDecoderError, match="equal length"):
        decode_per_stratum_position_lineage(
            signature.active_sequence,
            base_specs,
            base_values[:-1],
            fibers,
        )
    with pytest.raises(PerStratumPositionDecoderError, match="non-empty"):
        decode_per_stratum_position_lineage(
            (),
            base_specs,
            base_values,
            fibers,
        )
