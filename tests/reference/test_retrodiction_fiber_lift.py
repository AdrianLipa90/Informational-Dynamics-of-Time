from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_fiber_lift import (
    FiberLiftCompositionError,
    audit_finite_fiber_lift,
)
from src.idt.retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    sparse_orchorbital_observation,
)
from src.idt.retrodiction_oriented_winding_fiber import (
    oriented_winding_fiber_for_kicks,
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


def _latent(kicks):
    return np.asarray(
        [component for kick in kicks for component in (complex(kick).real, complex(kick).imag)],
        dtype=float,
    )


def _position_carrier(kicks):
    receipts = tuple(
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip((0.004, 0.003), kicks)
    )
    states, _ = replay_memory_orchorbital_lineage(
        _initial(), _attractors(), receipts
    )
    return np.concatenate(
        [np.asarray(state.position, dtype=float) for state in states[1:]]
    )


def test_exact_composition_pattern_passes_on_simple_finite_domain() -> None:
    audit = audit_finite_fiber_lift(
        latent_records=([0.0], [1.0], [2.0]),
        carrier_records=([10.0], [11.0], [12.0]),
        base_records=([0.0], [0.0], [1.0]),
        fiber_channels={"sheet": ([0.0], [1.0], [0.0])},
        latent_tolerance=1e-12,
        carrier_tolerance=1e-12,
        base_tolerance=1e-12,
        fiber_tolerance=1e-12,
    )
    assert audit.distinct_latent_pair_count == 3
    assert audit.carrier_collision_count == 0
    assert audit.augmented_collision_count == 0
    assert audit.lift_conflict_count == 0
    assert audit.status == "FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS"


def test_functional_lift_conflict_is_detected_separately() -> None:
    audit = audit_finite_fiber_lift(
        latent_records=([0.0], [1.0]),
        carrier_records=([10.0], [11.0]),
        base_records=([0.0], [0.0]),
        fiber_channels={"fiber": ([2.0], [2.0])},
        latent_tolerance=1e-12,
        carrier_tolerance=1e-12,
        base_tolerance=1e-12,
        fiber_tolerance=1e-12,
    )
    assert audit.carrier_collision_count == 0
    assert audit.augmented_collision_count == 1
    assert audit.lift_conflict_count == 1
    assert audit.status == "FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN"


def test_carrier_injectivity_failure_has_priority() -> None:
    audit = audit_finite_fiber_lift(
        latent_records=([0.0], [1.0]),
        carrier_records=([10.0], [10.0]),
        base_records=([0.0], [1.0]),
        fiber_channels={"fiber": ([0.0], [0.0])},
        latent_tolerance=1e-12,
        carrier_tolerance=1e-12,
        base_tolerance=1e-12,
        fiber_tolerance=1e-12,
    )
    assert audit.carrier_collision_count == 1
    assert audit.status == "CARRIER_INJECTIVITY_FAIL_ON_FINITE_DOMAIN"


def test_identical_latent_records_emit_no_distinct_pair_status() -> None:
    audit = audit_finite_fiber_lift(
        latent_records=([1.0], [1.0]),
        carrier_records=([3.0], [3.0]),
        base_records=([4.0], [4.0]),
        fiber_channels={"fiber": ([5.0], [5.0])},
        latent_tolerance=1e-12,
        carrier_tolerance=1e-12,
        base_tolerance=1e-12,
        fiber_tolerance=1e-12,
    )
    assert audit.distinct_latent_pair_count == 0
    assert audit.status == "NO_DISTINCT_LATENT_PAIRS"


def test_07q_winding_plus_base_is_compatible_with_07k_position_carrier_on_reflection_pair() -> None:
    ref = _truth()
    alt = _alternate()
    base_ref = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), ref, _base_specs()
    )
    base_alt = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), alt, _base_specs()
    )
    winding_ref = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), ref
    )
    winding_alt = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), alt
    )

    audit = audit_finite_fiber_lift(
        latent_records=(_latent(ref), _latent(alt)),
        carrier_records=(_position_carrier(ref), _position_carrier(alt)),
        base_records=(base_ref, base_alt),
        fiber_channels={
            "oriented_winding": (
                winding_ref.winding_increments,
                winding_alt.winding_increments,
            )
        },
        latent_tolerance=1e-8,
        carrier_tolerance=1e-12,
        base_tolerance=1e-10,
        fiber_tolerance=1e-12,
    )
    assert audit.distinct_latent_pair_count == 1
    assert audit.carrier_collision_count == 0
    assert audit.augmented_collision_count == 0
    assert audit.lift_conflict_count == 0
    assert audit.minimum_distinct_carrier_distance is not None
    assert audit.minimum_distinct_carrier_distance > 1e-12
    assert audit.status == "FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS"


def test_same_reflection_pair_without_a_separating_fiber_fails_lift_condition() -> None:
    ref = _truth()
    alt = _alternate()
    base_ref = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), ref, _base_specs()
    )
    base_alt = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), alt, _base_specs()
    )
    audit = audit_finite_fiber_lift(
        latent_records=(_latent(ref), _latent(alt)),
        carrier_records=(_position_carrier(ref), _position_carrier(alt)),
        base_records=(base_ref, base_alt),
        fiber_channels={"zero_control": ([0.0], [0.0])},
        latent_tolerance=1e-8,
        carrier_tolerance=1e-12,
        base_tolerance=1e-10,
        fiber_tolerance=1e-12,
    )
    assert audit.augmented_collision_count == 1
    assert audit.lift_conflict_count == 1
    assert audit.status == "FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN"


def test_mismatched_record_count_fails_closed() -> None:
    with pytest.raises(FiberLiftCompositionError, match="equal length"):
        audit_finite_fiber_lift(
            latent_records=([0.0], [1.0]),
            carrier_records=([0.0], [1.0], [2.0]),
            base_records=([0.0], [1.0]),
            fiber_channels={"fiber": ([0.0], [1.0])},
        )


def test_nonfinite_record_fails_closed() -> None:
    with pytest.raises(FiberLiftCompositionError, match="finite"):
        audit_finite_fiber_lift(
            latent_records=([0.0], [1.0]),
            carrier_records=([0.0], [float("nan")]),
            base_records=([0.0], [1.0]),
            fiber_channels={"fiber": ([0.0], [1.0])},
        )
