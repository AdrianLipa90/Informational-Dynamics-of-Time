from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec, propagate_orchorbital
from src.idt.retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    sparse_orchorbital_observation,
)
from src.idt.retrodiction_orchorbital_residence_conditioning import (
    build_memory_orchorbital_residence_cells,
    residence_lineage_signature,
)
from src.idt.retrodiction_stratified_position_lift import (
    retrodict_from_retained_position_lift,
)
from src.idt.retrodiction_winding_radius_position_decoder import (
    ActiveRadiusCoordinate,
    WindingRadiusPositionDecoderError,
    decode_winding_radius_position_lineage,
    winding_radius_compression_budget,
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
    centers = {spec.name: np.asarray(spec.center, dtype=float) for spec in attractors}
    radii = tuple(
        ActiveRadiusCoordinate(
            k,
            float(np.linalg.norm(positions[k - 1] - centers[signature.active_sequence[k - 1]])),
        )
        for k in range(1, len(signature.active_sequence))
    )
    n = len(signature.active_sequence)
    base_specs = (
        ScalarCheckpointObservation(n, "rx"),
        ScalarCheckpointObservation(n, "ry"),
        ScalarCheckpointObservation(n, "vx"),
    )
    base_values = sparse_orchorbital_observation(
        initial,
        attractors,
        _dts(),
        _kicks(),
        base_specs,
    )
    return initial, attractors, signature, positions, radii, base_specs, base_values


def _decode_reference():
    initial, attractors, signature, positions, radii, base_specs, base_values = _reference_data()
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        signature.active_sequence,
        signature.winding_increments,
        base_specs,
        base_values,
        radii,
        final_winding_tolerance_radians=1e-10,
    )
    return decoded, positions, signature


def test_real_three_event_winding_radius_decoder_recovers_position_carrier() -> None:
    decoded, positions, signature = _decode_reference()
    assert decoded.status == "EXACT_WINDING_RADIUS_POSITION_DECODER"
    assert decoded.active_sequence == signature.active_sequence
    assert decoded.event_count == 3
    assert decoded.radial_labels == ("rho1", "rho2")
    assert decoded.final_position_labels == ("r3x", "r3y")
    assert decoded.final_winding_residual_radians <= 1e-10
    assert np.allclose(decoded.position_lineage, positions, rtol=0.0, atol=2e-12)


def test_winding_radius_decoder_composes_with_07k_to_recover_real_kicks() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        signature.active_sequence,
        signature.winding_increments,
        base_specs,
        base_values,
        radii,
    )
    recovered = retrodict_from_retained_position_lift(
        initial,
        attractors,
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


@pytest.mark.parametrize("event_count", [2, 3, 4, 7, 12])
def test_new_scalar_position_budget_is_exactly_halved(event_count: int) -> None:
    budget = winding_radius_compression_budget(event_count)
    assert budget.cartesian_baseline_scalars == 2 * event_count - 2
    assert budget.radial_scalars == event_count - 1
    assert budget.reused_winding_scalars == event_count
    assert budget.new_scalar_ratio == 0.5
    assert budget.status == "POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED"


def test_single_event_requires_no_prefinal_radial_scalar() -> None:
    initial = MemoryPhaseState(
        np.array([1.0, 0.3], dtype=float),
        np.array([0.0, 0.4], dtype=float),
        0.0,
        0.0,
    )
    attractors = (AttractorSpec("A", np.array([0.0, 0.0]), 2.0),)
    step = propagate_orchorbital(initial, attractors, (0.02,))[0]
    base_specs = (
        ScalarCheckpointObservation(1, "rx"),
        ScalarCheckpointObservation(1, "ry"),
    )
    base_values = (float(step.state_after.position[0]), float(step.state_after.position[1]))
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        (step.active_attractor,),
        (step.winding_increment,),
        base_specs,
        base_values,
        (),
    )
    assert decoded.radial_labels == ()
    assert decoded.budget.cartesian_baseline_scalars == 0
    assert decoded.budget.radial_scalars == 0
    assert decoded.budget.new_scalar_ratio is None
    assert decoded.budget.status == "NO_PREFINAL_POSITION_FIBER_REQUIRED"
    assert np.allclose(decoded.position_lineage[0], step.state_after.position, atol=1e-12)


def test_decoder_remains_exact_across_active_attractor_switch() -> None:
    initial = MemoryPhaseState(
        np.array([1.6, 0.4], dtype=float),
        np.array([1.0, 0.0], dtype=float),
        0.0,
        0.0,
    )
    attractors = (
        AttractorSpec("A", np.array([0.0, 0.0]), 2.0),
        AttractorSpec("B", np.array([4.0, 0.0]), 2.0),
    )
    steps = propagate_orchorbital(initial, attractors, (0.5, 0.005))
    active_sequence = tuple(step.active_attractor for step in steps)
    assert active_sequence == ("A", "B")
    positions = np.asarray([step.state_after.position for step in steps], dtype=float)
    radius1 = float(np.linalg.norm(positions[0] - attractors[0].center))
    base_specs = (
        ScalarCheckpointObservation(2, "rx"),
        ScalarCheckpointObservation(2, "ry"),
    )
    base_values = (float(positions[1, 0]), float(positions[1, 1]))
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        active_sequence,
        tuple(step.winding_increment for step in steps),
        base_specs,
        base_values,
        (ActiveRadiusCoordinate(1, radius1),),
    )
    assert np.allclose(decoded.position_lineage, positions, rtol=0.0, atol=2e-12)


def test_missing_or_duplicate_radius_fails_closed() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    with pytest.raises(WindingRadiusPositionDecoderError, match="exactly one active radius"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            signature.winding_increments,
            base_specs,
            base_values,
            radii[:-1],
        )
    duplicate = (radii[0], ActiveRadiusCoordinate(1, radii[1].value))
    with pytest.raises(WindingRadiusPositionDecoderError, match="duplicate active radius"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            signature.winding_increments,
            base_specs,
            base_values,
            duplicate,
        )


def test_nonpositive_or_nonfinite_radius_fails_closed() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    for value in (0.0, -1.0, float("nan")):
        bad = (ActiveRadiusCoordinate(1, value), radii[1])
        with pytest.raises(WindingRadiusPositionDecoderError):
            decode_winding_radius_position_lineage(
                initial.position,
                attractors,
                signature.active_sequence,
                signature.winding_increments,
                base_specs,
                base_values,
                bad,
            )


def test_winding_count_and_wrapped_range_are_strict() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    with pytest.raises(WindingRadiusPositionDecoderError, match="one value per event"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            signature.winding_increments[:-1],
            base_specs,
            base_values,
            radii,
        )
    bad = list(signature.winding_increments)
    bad[0] = 0.5000001
    with pytest.raises(WindingRadiusPositionDecoderError, match="wrapped interval"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            bad,
            base_specs,
            base_values,
            radii,
        )


def test_unknown_or_duplicate_attractor_fails_closed() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    unknown = ("UNKNOWN",) + signature.active_sequence[1:]
    with pytest.raises(WindingRadiusPositionDecoderError, match="unknown attractor"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            unknown,
            signature.winding_increments,
            base_specs,
            base_values,
            radii,
        )
    duplicate_specs = attractors + (
        AttractorSpec("A", np.array([9.0, 9.0]), 1.0),
    )
    with pytest.raises(WindingRadiusPositionDecoderError, match="unique"):
        decode_winding_radius_position_lineage(
            initial.position,
            duplicate_specs,
            signature.active_sequence,
            signature.winding_increments,
            base_specs,
            base_values,
            radii,
        )


def test_missing_final_base_position_coordinate_fails_closed() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    with pytest.raises(WindingRadiusPositionDecoderError, match="complete final position"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            signature.winding_increments,
            base_specs[:-2] + base_specs[-1:],
            base_values[:-2].tolist() + base_values[-1:].tolist(),
            radii,
        )


def test_singular_previous_position_fails_closed() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    centers = {spec.name: np.asarray(spec.center, dtype=float) for spec in attractors}
    singular_initial = centers[signature.active_sequence[0]].copy()
    with pytest.raises(WindingRadiusPositionDecoderError, match="singular at the active center"):
        decode_winding_radius_position_lineage(
            singular_initial,
            attractors,
            signature.active_sequence,
            signature.winding_increments,
            base_specs,
            base_values,
            radii,
        )


def test_tampered_final_winding_fails_consistency_gate() -> None:
    initial, attractors, signature, _, radii, base_specs, base_values = _reference_data()
    bad = list(signature.winding_increments)
    bad[-1] += 1e-4
    assert abs(bad[-1]) <= 0.5
    with pytest.raises(WindingRadiusPositionDecoderError, match="inconsistent with the declared final winding"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            bad,
            base_specs,
            base_values,
            radii,
            final_winding_tolerance_radians=1e-10,
        )


def test_tampered_final_position_direction_fails_consistency_gate() -> None:
    initial, attractors, signature, positions, radii, base_specs, base_values = _reference_data()
    centers = {spec.name: np.asarray(spec.center, dtype=float) for spec in attractors}
    center = centers[signature.active_sequence[-1]]
    rel = positions[-1] - center
    angle = 1e-3
    rotation = np.asarray(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
        dtype=float,
    )
    tampered_final = center + rotation @ rel
    tampered_values = np.asarray(base_values, dtype=float).copy()
    tampered_values[0] = tampered_final[0]
    tampered_values[1] = tampered_final[1]
    with pytest.raises(WindingRadiusPositionDecoderError, match="inconsistent with the declared final winding"):
        decode_winding_radius_position_lineage(
            initial.position,
            attractors,
            signature.active_sequence,
            signature.winding_increments,
            base_specs,
            tampered_values,
            radii,
            final_winding_tolerance_radians=1e-10,
        )
