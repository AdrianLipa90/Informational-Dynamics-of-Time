from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, replace
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec
from .orchorbital_residence_ledger import state_sha256
from .retrodiction_orchorbital_residence_conditioning import (
    MemoryORCHORBITALResidenceCell,
    build_memory_orchorbital_residence_cells,
    verify_memory_orchorbital_residence_cells,
)
from .retrodiction_winding_radius_position_decoder import ActiveRadiusCoordinate


RADIAL_BINDING_SCHEMA = "idt.retrodiction-radial-residence-binding/v1"


class RadialResidenceBindingError(ValueError):
    pass


@dataclass(frozen=True)
class RadialResidenceCoordinate:
    checkpoint_index: int
    active_attractor: str
    radius_hex: str
    source_cell_sha256: str
    state_after_sha256: str
    previous_coordinate_sha256: str | None
    coordinate_sha256: str

    @property
    def radius(self) -> float:
        return float.fromhex(self.radius_hex)


@dataclass(frozen=True)
class RadialResidenceBindingResult:
    coordinates: tuple[RadialResidenceCoordinate, ...]
    active_radii: tuple[ActiveRadiusCoordinate, ...]
    event_count: int
    residence_head_sha256: str
    radial_head_sha256: str
    status: str


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _is_sha256(value: str) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _finite_positive(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise RadialResidenceBindingError(f"{name} must be a finite positive scalar")
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise RadialResidenceBindingError(f"{name} must be a finite positive scalar")
    return x


def _attractor_centers(attractors: Sequence[AttractorSpec]) -> dict[str, np.ndarray]:
    if not attractors:
        raise RadialResidenceBindingError("attractors must be non-empty")
    out: dict[str, np.ndarray] = {}
    for raw in attractors:
        if not isinstance(raw, AttractorSpec):
            raise RadialResidenceBindingError("attractors must contain AttractorSpec values")
        name = str(raw.name).strip()
        center = np.asarray(raw.center, dtype=float)
        if not name or name in out:
            raise RadialResidenceBindingError("attractor names must be non-empty and unique")
        if center.shape != (2,) or not np.all(np.isfinite(center)):
            raise RadialResidenceBindingError(f"center[{name}] must be finite two-component")
        out[name] = center.copy()
    return out


def _payload(value: RadialResidenceCoordinate) -> dict[str, object]:
    return {
        "schema": RADIAL_BINDING_SCHEMA,
        "checkpoint_index": value.checkpoint_index,
        "active_attractor": value.active_attractor,
        "radius_hex": value.radius_hex,
        "source_cell_sha256": value.source_cell_sha256,
        "state_after_sha256": value.state_after_sha256,
        "previous_coordinate_sha256": value.previous_coordinate_sha256,
    }


def _coordinate_hash(value: RadialResidenceCoordinate) -> str:
    return _sha256(_canonical_json(_payload(value)))


def _validate_coordinate(value: RadialResidenceCoordinate) -> None:
    if not isinstance(value, RadialResidenceCoordinate):
        raise RadialResidenceBindingError("radial lineage must contain RadialResidenceCoordinate values")
    if type(value.checkpoint_index) is not int or value.checkpoint_index <= 0:
        raise RadialResidenceBindingError("checkpoint_index must be a strictly positive integer")
    if type(value.active_attractor) is not str or not value.active_attractor.strip():
        raise RadialResidenceBindingError("active_attractor must be a non-empty string")
    try:
        radius = float.fromhex(value.radius_hex)
    except (TypeError, ValueError) as exc:
        raise RadialResidenceBindingError("radius_hex must be an exact float hex string") from exc
    _finite_positive(radius, "radius")
    if not _is_sha256(value.source_cell_sha256):
        raise RadialResidenceBindingError("source_cell_sha256 must be lowercase SHA-256")
    if not _is_sha256(value.state_after_sha256):
        raise RadialResidenceBindingError("state_after_sha256 must be lowercase SHA-256")
    if value.previous_coordinate_sha256 is not None and not _is_sha256(value.previous_coordinate_sha256):
        raise RadialResidenceBindingError("previous_coordinate_sha256 must be null or lowercase SHA-256")
    if not _is_sha256(value.coordinate_sha256):
        raise RadialResidenceBindingError("coordinate_sha256 must be lowercase SHA-256")
    if _coordinate_hash(value) != value.coordinate_sha256:
        raise RadialResidenceBindingError("radial coordinate content hash mismatch")


def verify_radial_residence_binding(
    coordinates: Sequence[RadialResidenceCoordinate],
    residence_cells: Sequence[MemoryORCHORBITALResidenceCell],
) -> None:
    if not coordinates:
        raise RadialResidenceBindingError("coordinates must be non-empty")
    try:
        verify_memory_orchorbital_residence_cells(residence_cells)
    except ValueError as exc:
        raise RadialResidenceBindingError(str(exc)) from exc
    if len(coordinates) != len(residence_cells):
        raise RadialResidenceBindingError("radial coordinate count must match residence cell count")

    previous_hash: str | None = None
    for expected_index, (coordinate, cell) in enumerate(zip(coordinates, residence_cells), start=1):
        _validate_coordinate(coordinate)
        if coordinate.checkpoint_index != expected_index:
            raise RadialResidenceBindingError("radial checkpoint indices must be contiguous from one")
        if coordinate.previous_coordinate_sha256 != previous_hash:
            raise RadialResidenceBindingError("radial coordinate hash chain is broken")
        if coordinate.source_cell_sha256 != cell.cell_sha256:
            raise RadialResidenceBindingError("radial coordinate source cell binding mismatch")
        receipt = cell.residence_receipt
        if coordinate.state_after_sha256 != receipt.state_after_sha256:
            raise RadialResidenceBindingError("radial coordinate state-after binding mismatch")
        if coordinate.active_attractor != receipt.active_attractor:
            raise RadialResidenceBindingError("radial coordinate active-attractor binding mismatch")
        previous_hash = coordinate.coordinate_sha256


def build_radial_residence_binding(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    memory_receipts: Sequence[MemoryEventReceipt],
    residence_cells: Sequence[MemoryORCHORBITALResidenceCell] | None = None,
) -> RadialResidenceBindingResult:
    """Bind the 07U radial coordinates to the persisted event-residence lineage.

    The historical residence receipt schema remains unchanged.  This companion
    content-addressed lineage commits each post-segment active-attractor radius
    to the source event-residence cell and to its state-after commitment.
    """
    receipts = tuple(memory_receipts)
    if not receipts:
        raise RadialResidenceBindingError("memory_receipts must be non-empty")
    cells = (
        tuple(residence_cells)
        if residence_cells is not None
        else build_memory_orchorbital_residence_cells(initial_state, attractors, receipts)
    )
    try:
        verify_memory_orchorbital_residence_cells(cells)
        states, bridge_cells = replay_memory_orchorbital_lineage(initial_state, attractors, receipts)
    except ValueError as exc:
        raise RadialResidenceBindingError(str(exc)) from exc
    if len(cells) != len(receipts) or len(bridge_cells) != len(receipts) or len(states) != len(receipts) + 1:
        raise RadialResidenceBindingError("residence and replay lineage lengths disagree")

    centers = _attractor_centers(attractors)
    coordinates: list[RadialResidenceCoordinate] = []
    previous_hash: str | None = None
    for checkpoint_index, (cell, bridge_cell, state_after) in enumerate(
        zip(cells, bridge_cells, states[1:]), start=1
    ):
        receipt = cell.residence_receipt
        active = receipt.active_attractor
        if bridge_cell.active_attractor != active:
            raise RadialResidenceBindingError("replayed active attractor disagrees with residence cell")
        if active not in centers:
            raise RadialResidenceBindingError("residence cell names an unknown active attractor")
        committed_state = state_sha256(state_after)
        if committed_state != receipt.state_after_sha256:
            raise RadialResidenceBindingError("replayed state-after hash disagrees with residence commitment")
        position = np.asarray(state_after.position, dtype=float)
        if position.shape != (2,) or not np.all(np.isfinite(position)):
            raise RadialResidenceBindingError("replayed state position must be finite two-component")
        radius = _finite_positive(
            float(np.linalg.norm(position - centers[active])),
            f"rho{checkpoint_index}",
        )
        draft = RadialResidenceCoordinate(
            checkpoint_index=checkpoint_index,
            active_attractor=active,
            radius_hex=radius.hex(),
            source_cell_sha256=cell.cell_sha256,
            state_after_sha256=receipt.state_after_sha256,
            previous_coordinate_sha256=previous_hash,
            coordinate_sha256="0" * 64,
        )
        coordinate = replace(draft, coordinate_sha256=_coordinate_hash(draft))
        _validate_coordinate(coordinate)
        coordinates.append(coordinate)
        previous_hash = coordinate.coordinate_sha256

    verify_radial_residence_binding(coordinates, cells)
    prefinal = tuple(
        ActiveRadiusCoordinate(value.checkpoint_index, value.radius)
        for value in coordinates[:-1]
    )
    return RadialResidenceBindingResult(
        coordinates=tuple(coordinates),
        active_radii=prefinal,
        event_count=len(coordinates),
        residence_head_sha256=cells[-1].cell_sha256,
        radial_head_sha256=coordinates[-1].coordinate_sha256,
        status="RADIAL_PACKET_RESIDENCE_BINDING_PASS",
    )
