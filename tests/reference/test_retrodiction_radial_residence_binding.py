from __future__ import annotations

from dataclasses import replace

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
from src.idt.retrodiction_radial_residence_binding import (
    RadialResidenceBindingError,
    build_radial_residence_binding,
    verify_radial_residence_binding,
)
from src.idt.retrodiction_stratified_position_lift import (
    retrodict_from_retained_position_lift,
)
from src.idt.retrodiction_winding_radius_position_decoder import (
    decode_winding_radius_position_lineage,
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


def _reference():
    initial = _initial()
    attractors = _attractors()
    receipts = _receipts()
    cells = build_memory_orchorbital_residence_cells(initial, attractors, receipts)
    signature = residence_lineage_signature(cells)
    states, _ = replay_memory_orchorbital_lineage(initial, attractors, receipts)
    positions = np.asarray([state.position for state in states[1:]], dtype=float)
    n = len(receipts)
    base_specs = (
        ScalarCheckpointObservation(n, "rx"),
        ScalarCheckpointObservation(n, "ry"),
        ScalarCheckpointObservation(n, "vx"),
    )
    base_values = sparse_orchorbital_observation(
        initial, attractors, _dts(), _kicks(), base_specs
    )
    return initial, attractors, receipts, cells, signature, positions, base_specs, base_values


def test_radial_packet_is_content_bound_to_exact_residence_lineage() -> None:
    initial, attractors, receipts, cells, signature, positions, _, _ = _reference()
    result = build_radial_residence_binding(initial, attractors, receipts, cells)
    assert result.status == "RADIAL_PACKET_RESIDENCE_BINDING_PASS"
    assert result.event_count == 3
    assert result.residence_head_sha256 == cells[-1].cell_sha256
    assert result.radial_head_sha256 == result.coordinates[-1].coordinate_sha256
    assert tuple(item.active_attractor for item in result.coordinates) == signature.active_sequence
    assert tuple(item.source_cell_sha256 for item in result.coordinates) == tuple(
        cell.cell_sha256 for cell in cells
    )
    centers = {spec.name: np.asarray(spec.center, dtype=float) for spec in attractors}
    expected = tuple(
        float(np.linalg.norm(position - centers[active]))
        for position, active in zip(positions, signature.active_sequence)
    )
    assert np.allclose(
        np.asarray([item.radius for item in result.coordinates]),
        np.asarray(expected),
        rtol=0.0,
        atol=0.0,
    )


def test_binding_exports_exact_07u_prefinal_packet() -> None:
    initial, attractors, receipts, cells, signature, positions, base_specs, base_values = _reference()
    binding = build_radial_residence_binding(initial, attractors, receipts, cells)
    assert tuple(item.label for item in binding.active_radii) == ("rho1", "rho2")
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        signature.active_sequence,
        signature.winding_increments,
        base_specs,
        base_values,
        binding.active_radii,
    )
    assert np.allclose(decoded.position_lineage, positions, rtol=0.0, atol=2e-12)


def test_residence_bound_packet_composes_with_07k_exact_inverse() -> None:
    initial, attractors, receipts, cells, signature, _, base_specs, base_values = _reference()
    binding = build_radial_residence_binding(initial, attractors, receipts, cells)
    decoded = decode_winding_radius_position_lineage(
        initial.position,
        attractors,
        signature.active_sequence,
        signature.winding_increments,
        base_specs,
        base_values,
        binding.active_radii,
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


def test_tampered_radial_coordinate_fails_content_hash_gate() -> None:
    initial, attractors, receipts, cells, _, _, _, _ = _reference()
    result = build_radial_residence_binding(initial, attractors, receipts, cells)
    tampered = list(result.coordinates)
    tampered[0] = replace(tampered[0], radius_hex=float(result.coordinates[0].radius * 1.01).hex())
    with pytest.raises(RadialResidenceBindingError, match="content hash mismatch"):
        verify_radial_residence_binding(tampered, cells)


def test_wrong_residence_lineage_fails_closed() -> None:
    initial, attractors, receipts, cells, _, _, _, _ = _reference()
    result = build_radial_residence_binding(initial, attractors, receipts, cells)
    with pytest.raises(RadialResidenceBindingError):
        verify_radial_residence_binding(result.coordinates[:-1], cells)


def test_binding_tracks_active_attractor_switch() -> None:
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
    receipts = (
        MemoryEventReceipt(0.5, 1.0, 0.0j),
        MemoryEventReceipt(0.005, 1.0, 0.0j),
    )
    cells = build_memory_orchorbital_residence_cells(initial, attractors, receipts)
    signature = residence_lineage_signature(cells)
    assert signature.active_sequence == ("A", "B")
    result = build_radial_residence_binding(initial, attractors, receipts, cells)
    assert tuple(item.active_attractor for item in result.coordinates) == ("A", "B")
    assert tuple(item.label for item in result.active_radii) == ("rho1",)
