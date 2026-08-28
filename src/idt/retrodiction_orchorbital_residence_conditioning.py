from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, replace
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import memory_orchorbital_cycle_forward
from .memory_recall import MemoryEventReceipt, apply_receipt_kick
from .orchorbital import AttractorSpec, ORCHORBITALError
from .orchorbital_residence_ledger import (
    ORCHORBITALResidenceReceipt,
    receipt_to_dict,
    residence_receipt_from_step,
    state_sha256,
    verify_residence_receipts,
)
from .retrodiction_global_null_gate import ScalarCheckpointObservation, sparse_orchorbital_observation


BRIDGE_SCHEMA = "idt.memory-orchorbital-residence-cell/v1"


class RetrodictionResidenceConditioningError(ValueError):
    pass


@dataclass(frozen=True)
class MemoryORCHORBITALResidenceCell:
    index: int
    tau_before_event_hex: str
    memory_delta_tau_hex: str
    memory_event_weight_hex: str
    memory_delta_m_real_hex: str
    memory_delta_m_imag_hex: str
    state_before_event_sha256: str
    residence_receipt: ORCHORBITALResidenceReceipt
    previous_cell_sha256: str | None
    cell_sha256: str

    @property
    def memory_receipt(self) -> MemoryEventReceipt:
        return MemoryEventReceipt(
            float.fromhex(self.memory_delta_tau_hex),
            float.fromhex(self.memory_event_weight_hex),
            complex(
                float.fromhex(self.memory_delta_m_real_hex),
                float.fromhex(self.memory_delta_m_imag_hex),
            ),
        )


@dataclass(frozen=True)
class ResidenceLineageSignature:
    active_sequence: tuple[str, ...]
    next_sequence: tuple[str | None, ...]
    switch_indices: tuple[int, ...]
    leak_indices: tuple[int, ...]
    winding_increments: tuple[float, ...]
    bridge_head_sha256: str


@dataclass(frozen=True)
class ResidenceConditioningAudit:
    base_residual: float
    latent_separation: float
    active_labels_equivalent: bool
    switch_lineage_equivalent: bool
    winding_residual: float
    provenance_heads_equal: bool
    reference_signature: ResidenceLineageSignature
    alternate_signature: ResidenceLineageSignature
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


def _finite_hex(
    value: float,
    name: str,
    *,
    positive: bool = False,
    nonnegative: bool = False,
) -> str:
    if isinstance(value, (bool, np.bool_)):
        raise RetrodictionResidenceConditioningError(
            f"{name} must be a finite scalar"
        )
    x = float(value)
    if not math.isfinite(x):
        raise RetrodictionResidenceConditioningError(
            f"{name} must be a finite scalar"
        )
    if positive and x <= 0.0:
        raise RetrodictionResidenceConditioningError(
            f"{name} must be strictly positive"
        )
    if nonnegative and x < 0.0:
        raise RetrodictionResidenceConditioningError(
            f"{name} must be non-negative"
        )
    return x.hex()


def _decode_finite_hex(value: str, name: str) -> float:
    if type(value) is not str:
        raise RetrodictionResidenceConditioningError(
            f"{name} must be an exact float hex string"
        )
    try:
        x = float.fromhex(value)
    except ValueError as exc:
        raise RetrodictionResidenceConditioningError(
            f"{name} is invalid"
        ) from exc
    if not math.isfinite(x):
        raise RetrodictionResidenceConditioningError(
            f"{name} must decode to a finite scalar"
        )
    return x


def _event_fields(
    state_before_event: MemoryPhaseState,
    receipt: MemoryEventReceipt,
) -> tuple[str, str, str, str, str]:
    if not isinstance(receipt, MemoryEventReceipt):
        raise RetrodictionResidenceConditioningError(
            "memory receipt must be a MemoryEventReceipt"
        )
    delta_m = complex(receipt.delta_m)
    return (
        _finite_hex(state_before_event.tau_internal, "tau_before_event"),
        _finite_hex(receipt.delta_tau, "delta_tau", positive=True),
        _finite_hex(receipt.event_weight, "event_weight", nonnegative=True),
        _finite_hex(delta_m.real, "delta_m.real"),
        _finite_hex(delta_m.imag, "delta_m.imag"),
    )


def _cell_payload(
    cell: MemoryORCHORBITALResidenceCell,
) -> dict[str, object]:
    return {
        "schema": BRIDGE_SCHEMA,
        "index": cell.index,
        "tau_before_event_hex": cell.tau_before_event_hex,
        "memory_delta_tau_hex": cell.memory_delta_tau_hex,
        "memory_event_weight_hex": cell.memory_event_weight_hex,
        "memory_delta_m_real_hex": cell.memory_delta_m_real_hex,
        "memory_delta_m_imag_hex": cell.memory_delta_m_imag_hex,
        "state_before_event_sha256": cell.state_before_event_sha256,
        "residence_receipt": receipt_to_dict(cell.residence_receipt),
        "previous_cell_sha256": cell.previous_cell_sha256,
    }


def _cell_hash(cell: MemoryORCHORBITALResidenceCell) -> str:
    return _sha256(_canonical_json(_cell_payload(cell)))


def _validate_cell(cell: MemoryORCHORBITALResidenceCell) -> None:
    if not isinstance(cell, MemoryORCHORBITALResidenceCell):
        raise RetrodictionResidenceConditioningError(
            "cell must be a MemoryORCHORBITALResidenceCell"
        )
    if type(cell.index) is not int or cell.index < 0:
        raise RetrodictionResidenceConditioningError(
            "cell index must be a non-negative integer"
        )

    tau_before = _decode_finite_hex(
        cell.tau_before_event_hex,
        "tau_before_event_hex",
    )
    event_dt = _decode_finite_hex(
        cell.memory_delta_tau_hex,
        "memory_delta_tau_hex",
    )
    event_weight = _decode_finite_hex(
        cell.memory_event_weight_hex,
        "memory_event_weight_hex",
    )
    _decode_finite_hex(
        cell.memory_delta_m_real_hex,
        "memory_delta_m_real_hex",
    )
    _decode_finite_hex(
        cell.memory_delta_m_imag_hex,
        "memory_delta_m_imag_hex",
    )
    if event_dt <= 0.0:
        raise RetrodictionResidenceConditioningError(
            "memory delta_tau must be strictly positive"
        )
    if event_weight < 0.0:
        raise RetrodictionResidenceConditioningError(
            "memory event_weight must be non-negative"
        )
    if not _is_sha256(cell.state_before_event_sha256):
        raise RetrodictionResidenceConditioningError(
            "state_before_event_sha256 must be lowercase SHA-256"
        )
    if (
        cell.previous_cell_sha256 is not None
        and not _is_sha256(cell.previous_cell_sha256)
    ):
        raise RetrodictionResidenceConditioningError(
            "previous_cell_sha256 must be null or lowercase SHA-256"
        )
    if not _is_sha256(cell.cell_sha256):
        raise RetrodictionResidenceConditioningError(
            "cell_sha256 must be lowercase SHA-256"
        )

    try:
        verify_residence_receipts((cell.residence_receipt,))
    except ORCHORBITALError as exc:
        raise RetrodictionResidenceConditioningError(str(exc)) from exc
    if (
        cell.residence_receipt.index != 0
        or cell.residence_receipt.previous_receipt_sha256 is not None
    ):
        raise RetrodictionResidenceConditioningError(
            "event-local residence receipt must be a genesis segment"
        )

    expected_observed_dt = (tau_before + event_dt) - tau_before
    if cell.residence_receipt.delta_tau_hex != expected_observed_dt.hex():
        raise RetrodictionResidenceConditioningError(
            "memory event schedule and smooth-segment elapsed increment disagree"
        )
    if _cell_hash(cell) != cell.cell_sha256:
        raise RetrodictionResidenceConditioningError(
            "event-residence cell content hash mismatch"
        )


def build_memory_orchorbital_residence_cells(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    memory_receipts: Sequence[MemoryEventReceipt],
) -> tuple[MemoryORCHORBITALResidenceCell, ...]:
    if not memory_receipts:
        raise RetrodictionResidenceConditioningError(
            "memory_receipts must be non-empty"
        )
    cells: list[MemoryORCHORBITALResidenceCell] = []
    current = initial_state
    previous_hash: str | None = None
    for index, event in enumerate(memory_receipts):
        event_fields = _event_fields(current, event)
        before_event_hash = state_sha256(current)
        try:
            bridge_cell, step = memory_orchorbital_cycle_forward(
                current,
                attractors,
                event,
            )
            kicked = apply_receipt_kick(current, event)
            residence = residence_receipt_from_step(
                step,
                index=0,
                previous_receipt_sha256=None,
            )
        except (ValueError, ORCHORBITALError) as exc:
            raise RetrodictionResidenceConditioningError(str(exc)) from exc
        if bridge_cell.active_attractor != residence.active_attractor:
            raise RetrodictionResidenceConditioningError(
                "Memory/ORCH active snapshot disagrees with residence segment"
            )
        if state_sha256(kicked) != residence.state_before_sha256:
            raise RetrodictionResidenceConditioningError(
                "Memory event does not bridge to the committed smooth-segment state"
            )

        draft = MemoryORCHORBITALResidenceCell(
            index=index,
            tau_before_event_hex=event_fields[0],
            memory_delta_tau_hex=event_fields[1],
            memory_event_weight_hex=event_fields[2],
            memory_delta_m_real_hex=event_fields[3],
            memory_delta_m_imag_hex=event_fields[4],
            state_before_event_sha256=before_event_hash,
            residence_receipt=residence,
            previous_cell_sha256=previous_hash,
            cell_sha256="0" * 64,
        )
        cell = replace(draft, cell_sha256=_cell_hash(draft))
        _validate_cell(cell)
        cells.append(cell)
        current = step.state_after
        previous_hash = cell.cell_sha256

    verify_memory_orchorbital_residence_cells(cells)
    return tuple(cells)


def verify_memory_orchorbital_residence_cells(
    cells: Sequence[MemoryORCHORBITALResidenceCell],
) -> None:
    if not cells:
        raise RetrodictionResidenceConditioningError(
            "cells must be non-empty"
        )
    previous_hash: str | None = None
    previous_state_after: str | None = None
    for index, cell in enumerate(cells):
        _validate_cell(cell)
        if cell.index != index:
            raise RetrodictionResidenceConditioningError(
                "cell indices must be contiguous from zero"
            )
        if cell.previous_cell_sha256 != previous_hash:
            raise RetrodictionResidenceConditioningError(
                "event-residence cell hash chain is broken"
            )
        if (
            previous_state_after is not None
            and cell.state_before_event_sha256 != previous_state_after
        ):
            raise RetrodictionResidenceConditioningError(
                "event-residence pre-event state lineage is discontinuous"
            )
        previous_hash = cell.cell_sha256
        previous_state_after = cell.residence_receipt.state_after_sha256


def residence_lineage_signature(
    cells: Sequence[MemoryORCHORBITALResidenceCell],
) -> ResidenceLineageSignature:
    verify_memory_orchorbital_residence_cells(cells)
    return ResidenceLineageSignature(
        active_sequence=tuple(
            cell.residence_receipt.active_attractor for cell in cells
        ),
        next_sequence=tuple(
            cell.residence_receipt.next_attractor for cell in cells
        ),
        switch_indices=tuple(
            cell.index
            for cell in cells
            if cell.residence_receipt.switched_after_segment
        ),
        leak_indices=tuple(
            cell.index
            for cell in cells
            if cell.residence_receipt.post_segment_leak
        ),
        winding_increments=tuple(
            cell.residence_receipt.winding_increment for cell in cells
        ),
        bridge_head_sha256=cells[-1].cell_sha256,
    )


def _finite_kicks(kicks: Sequence[complex]) -> tuple[complex, ...]:
    if not kicks:
        raise RetrodictionResidenceConditioningError(
            "kicks must be non-empty"
        )
    out: list[complex] = []
    for raw in kicks:
        value = complex(raw)
        if not (math.isfinite(value.real) and math.isfinite(value.imag)):
            raise RetrodictionResidenceConditioningError(
                "kicks must be finite"
            )
        out.append(value)
    return tuple(out)


def _latent_vector(kicks: Sequence[complex]) -> np.ndarray:
    values = _finite_kicks(kicks)
    out = np.empty(2 * len(values), dtype=float)
    for index, value in enumerate(values):
        out[2 * index] = value.real
        out[2 * index + 1] = value.imag
    return out


def _cells_for_kicks(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
) -> tuple[MemoryORCHORBITALResidenceCell, ...]:
    kick_values = _finite_kicks(kicks)
    if len(delta_taus) != len(kick_values):
        raise RetrodictionResidenceConditioningError(
            "delta_taus must match the kick count"
        )
    receipts: list[MemoryEventReceipt] = []
    for delta_tau, kick in zip(delta_taus, kick_values):
        dt = float(delta_tau)
        if not math.isfinite(dt) or dt <= 0.0:
            raise RetrodictionResidenceConditioningError(
                "delta_taus must be finite and strictly positive"
            )
        receipts.append(MemoryEventReceipt(dt, 1.0, kick))
    return build_memory_orchorbital_residence_cells(
        initial_state,
        attractors,
        receipts,
    )


def audit_known_null_residence_conditioning(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    reference_kicks: Sequence[complex],
    alternate_kicks: Sequence[complex],
    base_observations: Sequence[ScalarCheckpointObservation],
    *,
    equivalence_tolerance: float = 1e-10,
) -> ResidenceConditioningAudit:
    """Audit discrete residence/switch conditioning for one declared null pair.

    Semantic status uses retained active labels and switch/leak lineage. Content
    hashes remain provenance commitments and are excluded from the separation
    decision. Winding is reported independently as a continuous diagnostic.
    """
    tol = float(equivalence_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise RetrodictionResidenceConditioningError(
            "equivalence_tolerance must be finite and strictly positive"
        )
    ref = _finite_kicks(reference_kicks)
    alt = _finite_kicks(alternate_kicks)
    if len(ref) != len(alt):
        raise RetrodictionResidenceConditioningError(
            "reference and alternate histories must have equal event count"
        )
    latent_separation = float(
        np.linalg.norm(_latent_vector(ref) - _latent_vector(alt))
    )
    if latent_separation <= tol:
        raise RetrodictionResidenceConditioningError(
            "known-null candidates must be distinct in latent coordinates"
        )

    try:
        base_ref = sparse_orchorbital_observation(
            initial_state,
            attractors,
            delta_taus,
            ref,
            base_observations,
        )
        base_alt = sparse_orchorbital_observation(
            initial_state,
            attractors,
            delta_taus,
            alt,
            base_observations,
        )
    except ValueError as exc:
        raise RetrodictionResidenceConditioningError(str(exc)) from exc
    base_residual = float(np.linalg.norm(base_ref - base_alt))

    ref_signature = residence_lineage_signature(
        _cells_for_kicks(
            initial_state,
            attractors,
            delta_taus,
            ref,
        )
    )
    alt_signature = residence_lineage_signature(
        _cells_for_kicks(
            initial_state,
            attractors,
            delta_taus,
            alt,
        )
    )
    active_equal = (
        ref_signature.active_sequence == alt_signature.active_sequence
    )
    switch_equal = (
        ref_signature.next_sequence == alt_signature.next_sequence
        and ref_signature.switch_indices == alt_signature.switch_indices
        and ref_signature.leak_indices == alt_signature.leak_indices
    )
    winding_residual = float(
        np.linalg.norm(
            np.asarray(ref_signature.winding_increments, dtype=float)
            - np.asarray(alt_signature.winding_increments, dtype=float)
        )
    )

    if base_residual > tol:
        status = "NOT_A_BASE_NULL"
    elif not active_equal:
        status = "KNOWN_NULL_SEPARATED_BY_ACTIVE_RESIDENCE_LABELS"
    elif not switch_equal:
        status = "KNOWN_NULL_SEPARATED_BY_SWITCH_LINEAGE"
    else:
        status = "KNOWN_NULL_PERSISTS_UNDER_RESIDENCE_LABELS"

    return ResidenceConditioningAudit(
        base_residual=base_residual,
        latent_separation=latent_separation,
        active_labels_equivalent=active_equal,
        switch_lineage_equivalent=switch_equal,
        winding_residual=winding_residual,
        provenance_heads_equal=(
            ref_signature.bridge_head_sha256
            == alt_signature.bridge_head_sha256
        ),
        reference_signature=ref_signature,
        alternate_signature=alt_signature,
        status=status,
    )
