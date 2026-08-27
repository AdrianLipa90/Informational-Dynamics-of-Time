from __future__ import annotations

import numpy as np

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    audit_known_global_null_separation,
    sparse_orchorbital_observation,
)


def _initial():
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
    return [0.034 - 0.023j, -0.008 + 0.028j, 0.020 - 0.015j]


def _alternate():
    return [
        complex(0.02171604910786055, -0.01997647522522139),
        complex(0.02066339813510957, 0.02094610600551937),
        complex(0.00362139881046886, -0.01096863363360488),
    ]


def _base_specs():
    return [
        ScalarCheckpointObservation(1, "weight", "A"),
        ScalarCheckpointObservation(2, "weight", "A"),
        ScalarCheckpointObservation(3, "rx"),
        ScalarCheckpointObservation(3, "ry"),
        ScalarCheckpointObservation(3, "vx"),
        ScalarCheckpointObservation(3, "weight", "A"),
        ScalarCheckpointObservation(3, "weight", "B"),
        ScalarCheckpointObservation(3, "weight", "C"),
    ]


def test_declared_n3_schedule_contains_explicit_distinct_history_collision():
    truth = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003, 0.0035], _truth(), _base_specs()
    )
    alternate = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003, 0.0035], _alternate(), _base_specs()
    )
    assert np.linalg.norm(truth - alternate) < 1e-12
    assert np.linalg.norm(np.asarray(_truth()) - np.asarray(_alternate())) > 1e-2


def test_second_earlier_basin_weight_separates_declared_n3_collision():
    audit = audit_known_global_null_separation(
        _initial(),
        _attractors(),
        [0.004, 0.003, 0.0035],
        _truth(),
        _alternate(),
        _base_specs(),
        [ScalarCheckpointObservation(1, "weight", "B")],
        equivalence_tolerance=1e-10,
    )
    assert audit.base_equivalent
    assert not audit.augmented_equivalent
    assert audit.status == "KNOWN_NULL_SEPARATED"
    assert audit.augmented_residual > 1e-7


def test_original_earlier_weight_is_exact_negative_control_for_declared_pair():
    left = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003, 0.0035], _truth(),
        [ScalarCheckpointObservation(1, "weight", "A")],
    )
    right = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003, 0.0035], _alternate(),
        [ScalarCheckpointObservation(1, "weight", "A")],
    )
    assert np.linalg.norm(left - right) < 1e-12
