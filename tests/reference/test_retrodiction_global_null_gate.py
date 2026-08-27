from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_global_null_gate import (
    RetrodictionGlobalNullError,
    ScalarCheckpointObservation,
    audit_known_global_null_separation,
    sparse_orchorbital_observation,
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


def test_final_only_partial_augmented_measurement_contains_explicit_null() -> None:
    truth = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003], _truth(), _base_specs()
    )
    alternate = sparse_orchorbital_observation(
        _initial(), _attractors(), [0.004, 0.003], _alternate(), _base_specs()
    )
    assert np.linalg.norm(truth - alternate) < 1e-12
    assert np.linalg.norm(np.asarray(_truth()) - np.asarray(_alternate())) > 0.5


def test_one_earlier_basin_weight_separates_declared_reflection_null() -> None:
    audit = audit_known_global_null_separation(
        _initial(),
        _attractors(),
        [0.004, 0.003],
        _truth(),
        _alternate(),
        _base_specs(),
        [ScalarCheckpointObservation(1, "weight", "A")],
        equivalence_tolerance=1e-10,
    )
    assert audit.base_equivalent
    assert not audit.augmented_equivalent
    assert audit.status == "KNOWN_NULL_SEPARATED"
    assert audit.base_residual < 1e-12
    assert audit.augmented_residual > 1e-2


def test_earlier_rx_negative_control_leaves_declared_null_unseparated() -> None:
    audit = audit_known_global_null_separation(
        _initial(),
        _attractors(),
        [0.004, 0.003],
        _truth(),
        _alternate(),
        _base_specs(),
        [ScalarCheckpointObservation(1, "rx")],
        equivalence_tolerance=1e-12,
    )
    assert audit.base_equivalent
    assert audit.augmented_equivalent
    assert audit.status == "KNOWN_NULL_PERSISTS"


def test_sparse_weight_observation_matches_reference_value() -> None:
    value = sparse_orchorbital_observation(
        _initial(),
        _attractors(),
        [0.004, 0.003],
        _truth(),
        [ScalarCheckpointObservation(1, "weight", "A")],
    )
    assert value.shape == (1,)
    assert value[0] == pytest.approx(0.5838364569736161, abs=2e-14)


def test_invalid_weight_attractor_fails_closed() -> None:
    with pytest.raises(RetrodictionGlobalNullError, match="absent"):
        sparse_orchorbital_observation(
            _initial(),
            _attractors(),
            [0.004, 0.003],
            _truth(),
            [ScalarCheckpointObservation(1, "weight", "missing")],
        )


def test_identical_latent_histories_are_rejected_as_known_null_candidates() -> None:
    with pytest.raises(RetrodictionGlobalNullError, match="distinct"):
        audit_known_global_null_separation(
            _initial(),
            _attractors(),
            [0.004, 0.003],
            _truth(),
            _truth(),
            _base_specs(),
            [ScalarCheckpointObservation(1, "weight", "A")],
        )
