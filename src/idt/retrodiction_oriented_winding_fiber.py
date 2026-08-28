from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec
from .retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    sparse_orchorbital_observation,
)
from .retrodiction_orchorbital_residence_conditioning import (
    MemoryORCHORBITALResidenceCell,
    build_memory_orchorbital_residence_cells,
    residence_lineage_signature,
)


class OrientedWindingFiberError(ValueError):
    pass


@dataclass(frozen=True)
class OrientedWindingFiber:
    active_sequence: tuple[str, ...]
    winding_increment_hex: tuple[str, ...]
    winding_increments: tuple[float, ...]
    cumulative_winding: float
    status: str


@dataclass(frozen=True)
class OrientedWindingNullAudit:
    base_residual: float
    latent_separation: float
    winding_fiber_distance: float
    active_sequence_equal: bool
    reference_fiber: OrientedWindingFiber
    alternate_fiber: OrientedWindingFiber
    status: str


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise OrientedWindingFiberError(
            f"{name} must be finite and strictly positive"
        )
    return x


def _finite_kicks(values: Sequence[complex]) -> tuple[complex, ...]:
    if not values:
        raise OrientedWindingFiberError("kicks must be non-empty")
    out: list[complex] = []
    for raw in values:
        value = complex(raw)
        if not (math.isfinite(value.real) and math.isfinite(value.imag)):
            raise OrientedWindingFiberError("kicks must be finite")
        out.append(value)
    return tuple(out)


def _latent_vector(values: Sequence[complex]) -> np.ndarray:
    kicks = _finite_kicks(values)
    out = np.empty(2 * len(kicks), dtype=float)
    for index, kick in enumerate(kicks):
        out[2 * index] = kick.real
        out[2 * index + 1] = kick.imag
    return out


def oriented_winding_fiber_from_cells(
    cells: Sequence[MemoryORCHORBITALResidenceCell],
) -> OrientedWindingFiber:
    """Return the ordered signed winding fiber carried by residence receipts.

    Exact binary64 winding increments are retained through the existing
    ``winding_increment_hex`` receipt field.  The floating tuple is a decoded
    view for numerical separation tests; the hex tuple is the canonical
    persisted representation.
    """
    try:
        signature = residence_lineage_signature(cells)
    except ValueError as exc:
        raise OrientedWindingFiberError(str(exc)) from exc

    hex_values = tuple(
        cell.residence_receipt.winding_increment_hex for cell in cells
    )
    decoded: list[float] = []
    for raw in hex_values:
        if type(raw) is not str:
            raise OrientedWindingFiberError(
                "winding_increment_hex must be an exact float hex string"
            )
        try:
            value = float.fromhex(raw)
        except ValueError as exc:
            raise OrientedWindingFiberError(
                "winding_increment_hex is invalid"
            ) from exc
        if not math.isfinite(value):
            raise OrientedWindingFiberError(
                "winding increments must decode to finite scalars"
            )
        decoded.append(value)

    winding = tuple(decoded)
    if winding != signature.winding_increments:
        raise OrientedWindingFiberError(
            "decoded winding fiber disagrees with residence signature"
        )
    return OrientedWindingFiber(
        active_sequence=signature.active_sequence,
        winding_increment_hex=hex_values,
        winding_increments=winding,
        cumulative_winding=float(math.fsum(winding)),
        status="ORDERED_ORIENTED_WINDING_FIBER",
    )


def oriented_winding_fiber_for_kicks(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
) -> OrientedWindingFiber:
    kick_values = _finite_kicks(kicks)
    if len(delta_taus) != len(kick_values):
        raise OrientedWindingFiberError(
            "delta_taus must match the kick count"
        )
    receipts: list[MemoryEventReceipt] = []
    for raw_dt, kick in zip(delta_taus, kick_values):
        dt = _positive(raw_dt, "delta_tau")
        receipts.append(MemoryEventReceipt(dt, 1.0, kick))
    try:
        cells = build_memory_orchorbital_residence_cells(
            initial_state,
            attractors,
            receipts,
        )
    except ValueError as exc:
        raise OrientedWindingFiberError(str(exc)) from exc
    return oriented_winding_fiber_from_cells(cells)


def winding_fiber_distance(
    reference: OrientedWindingFiber,
    alternate: OrientedWindingFiber,
) -> float:
    if not isinstance(reference, OrientedWindingFiber) or not isinstance(
        alternate, OrientedWindingFiber
    ):
        raise OrientedWindingFiberError(
            "reference and alternate must be OrientedWindingFiber values"
        )
    if len(reference.winding_increments) != len(alternate.winding_increments):
        raise OrientedWindingFiberError(
            "winding fibers must have equal event count"
        )
    ref = np.asarray(reference.winding_increments, dtype=float)
    alt = np.asarray(alternate.winding_increments, dtype=float)
    return float(np.linalg.norm(alt - ref))


def audit_known_null_oriented_winding(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    reference_kicks: Sequence[complex],
    alternate_kicks: Sequence[complex],
    base_observations: Sequence[ScalarCheckpointObservation],
    *,
    base_tolerance: float = 1e-10,
    latent_tolerance: float = 1e-8,
    fiber_tolerance: float = 1e-12,
) -> OrientedWindingNullAudit:
    """Audit ordered signed winding as a fiber coordinate for one base null.

    The decision uses only declared base observations and the ordered winding
    increments.  Content hashes remain provenance commitments and never enter
    the separation metric.
    """
    btol = _positive(base_tolerance, "base_tolerance")
    ltol = _positive(latent_tolerance, "latent_tolerance")
    ftol = _positive(fiber_tolerance, "fiber_tolerance")
    ref = _finite_kicks(reference_kicks)
    alt = _finite_kicks(alternate_kicks)
    if len(ref) != len(alt):
        raise OrientedWindingFiberError(
            "reference and alternate histories must have equal event count"
        )

    latent_separation = float(
        np.linalg.norm(_latent_vector(alt) - _latent_vector(ref))
    )
    if latent_separation <= ltol:
        raise OrientedWindingFiberError(
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
        raise OrientedWindingFiberError(str(exc)) from exc
    base_residual = float(np.linalg.norm(base_alt - base_ref))

    ref_fiber = oriented_winding_fiber_for_kicks(
        initial_state,
        attractors,
        delta_taus,
        ref,
    )
    alt_fiber = oriented_winding_fiber_for_kicks(
        initial_state,
        attractors,
        delta_taus,
        alt,
    )
    fiber_distance = winding_fiber_distance(ref_fiber, alt_fiber)

    if base_residual > btol:
        status = "NOT_A_BASE_NULL"
    elif fiber_distance > ftol:
        status = "BASE_NULL_SEPARATED_BY_ORIENTED_WINDING"
    else:
        status = "BASE_NULL_PERSISTS_UNDER_ORIENTED_WINDING"

    return OrientedWindingNullAudit(
        base_residual=base_residual,
        latent_separation=latent_separation,
        winding_fiber_distance=fiber_distance,
        active_sequence_equal=(
            ref_fiber.active_sequence == alt_fiber.active_sequence
        ),
        reference_fiber=ref_fiber,
        alternate_fiber=alt_fiber,
        status=status,
    )
