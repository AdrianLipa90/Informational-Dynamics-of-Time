from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec, evaluate_attractor_field
from src.idt.retrodiction_spatial_offset_divergence import (
    SpatialOffsetDivergenceError,
    audit_sparse_preimage_pair,
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


def _observe(kicks, dts):
    receipts = [MemoryEventReceipt(float(dt), 1.0, complex(*row)) for dt, row in zip(dts, kicks)]
    states, cells = replay_memory_orchorbital_lineage(_initial(), _attractors(), receipts)
    n = len(kicks)
    values = []
    fields = []
    for state in states[1:]:
        field = evaluate_attractor_field(state, _attractors())
        if field.leak_mode:
            raise ValueError("LEAK_MODE")
        fields.append(field)
    for field in fields[:-1]:
        values.append(float(field.evaluations[0].weight))
    final = states[-1]
    values.extend([float(final.position[0]), float(final.position[1]), float(final.velocity[0])])
    values.extend(float(ev.weight) for ev in fields[-1].evaluations)
    for i in range(max(0, n - 3)):
        values.append(float(states[i + 1].position[0]))
    regime = tuple(cell.active_attractor for cell in cells)
    positions = np.asarray([state.position for state in states[1:]], dtype=float)
    return np.asarray(values, dtype=float), positions, regime


def _witness():
    dts = np.array([0.004, 0.003, 0.005, 0.0025], dtype=float)
    reference = np.array([
        [0.034, -0.023],
        [-0.008, 0.028],
        [0.011, 0.006],
        [-0.017, -0.009],
    ], dtype=float)
    candidate = np.array([
        [0.034000000000006206, -0.023000000000003372],
        [-0.0070342409020097, 0.027823047855073037],
        [0.009454724712228744, 0.006283057597947288],
        [-0.01642054454155759, -0.009106171287051467],
    ], dtype=float)
    return dts, reference, candidate


def test_07l_reference_has_a_spatial_offset_divergence_witness() -> None:
    dts, reference, candidate = _witness()
    y0, r0, regime0 = _observe(reference, dts)
    y1, r1, regime1 = _observe(candidate, dts)
    assert regime0 == regime1 == ("A", "A", "A", "A")
    audit = audit_sparse_preimage_pair(
        y0, y1, r0, r1, reference.reshape(-1), candidate.reshape(-1),
        observation_tolerance=1e-10,
        latent_tolerance=1e-8,
        spatial_tolerance=1e-9,
    )
    assert audit.status == "SPATIAL_OFFSET_DIVERGENCE"
    assert audit.observation_distance < 3e-13
    assert audit.latent_distance > 1e-3
    assert audit.sod_l2 > 2e-6
    assert audit.first_divergent_checkpoint == 2
    assert "r2x" in audit.separating_components
    assert "r2y" in audit.separating_components


def test_unretained_r2x_scalar_separates_the_known_sod_pair() -> None:
    dts, reference, candidate = _witness()
    _, r0, _ = _observe(reference, dts)
    _, r1, _ = _observe(candidate, dts)
    assert abs(float(r1[1, 0] - r0[1, 0])) > 2e-6


def test_same_preimage_is_not_classified_as_sod() -> None:
    record = np.array([1.0, 2.0])
    positions = np.array([[0.0, 0.0], [1.0, 1.0]])
    latent = np.array([0.1, -0.2])
    audit = audit_sparse_preimage_pair(record, record, positions, positions, latent, latent)
    assert audit.status == "SAME_LATENT_PREIMAGE"
    assert audit.first_divergent_checkpoint is None


def test_distinguishable_records_are_classified_before_spatial_divergence() -> None:
    audit = audit_sparse_preimage_pair(
        [0.0], [1.0], [[0.0, 0.0]], [[1.0, 0.0]], [0.0], [2.0],
        observation_tolerance=1e-6,
    )
    assert audit.status == "OBSERVATION_DISTINGUISHABLE"


def test_nonspatial_global_null_is_kept_distinct() -> None:
    audit = audit_sparse_preimage_pair(
        [0.0], [0.0], [[0.0, 0.0]], [[0.0, 0.0]], [0.0], [1.0],
        spatial_tolerance=1e-8,
    )
    assert audit.status == "NONSPATIAL_GLOBAL_NULL"


def test_invalid_shapes_and_tolerances_fail_closed() -> None:
    with pytest.raises(SpatialOffsetDivergenceError):
        audit_sparse_preimage_pair([0.0], [0.0, 1.0], [[0.0, 0.0]], [[0.0, 0.0]], [0.0], [1.0])
    with pytest.raises(SpatialOffsetDivergenceError):
        audit_sparse_preimage_pair([0.0], [0.0], [[0.0, 0.0]], [[0.0, 0.0]], [0.0], [1.0], spatial_tolerance=0.0)
