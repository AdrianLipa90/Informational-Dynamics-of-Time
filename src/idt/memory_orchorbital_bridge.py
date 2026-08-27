from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_recall import (
    MemoryEventReceipt,
    apply_receipt_kick,
    kepler_memory_inverse_step,
    remove_receipt_kick,
)
from .orchorbital import (
    AttractorSpec,
    ORCHORBITALError,
    ORCHORBITALStep,
    orchorbital_step,
    relative_state,
)


class MemoryORCHORBITALBridgeError(ValueError):
    pass


@dataclass(frozen=True)
class ORCHORBITALMemoryCellReceipt:
    memory_receipt: MemoryEventReceipt
    active_attractor: str
    active_center: tuple[float, float]
    active_mu_memory: float


def _active_spec_by_name(
    attractors: Sequence[AttractorSpec],
    name: str,
) -> AttractorSpec:
    target = str(name)
    for spec in attractors:
        if spec.name == target:
            return spec
    raise MemoryORCHORBITALBridgeError("active attractor is absent from attractor specification")


def _snapshot_spec(cell: ORCHORBITALMemoryCellReceipt) -> AttractorSpec:
    if not isinstance(cell, ORCHORBITALMemoryCellReceipt):
        raise MemoryORCHORBITALBridgeError("cell must be an ORCHORBITALMemoryCellReceipt")
    name = str(cell.active_attractor).strip()
    center = np.asarray(cell.active_center, dtype=float)
    mu = float(cell.active_mu_memory)
    if not name:
        raise MemoryORCHORBITALBridgeError("persisted active attractor name must be non-empty")
    if center.shape != (2,) or not np.all(np.isfinite(center)):
        raise MemoryORCHORBITALBridgeError("persisted active attractor center must be finite two-component")
    if not math.isfinite(mu) or mu <= 0.0:
        raise MemoryORCHORBITALBridgeError("persisted active mu_memory must be finite and strictly positive")
    return AttractorSpec(name, center.copy(), mu)


def memory_orchorbital_cycle_forward(
    state_before_event: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    receipt: MemoryEventReceipt,
) -> tuple[ORCHORBITALMemoryCellReceipt, ORCHORBITALStep]:
    """Apply the persisted Memory event first, then one active-centre ORCHORBITAL segment."""
    try:
        kicked = apply_receipt_kick(state_before_event, receipt)
        step = orchorbital_step(kicked, attractors, receipt.delta_tau)
    except (ValueError, ORCHORBITALError) as exc:
        raise MemoryORCHORBITALBridgeError(str(exc)) from exc
    active = _active_spec_by_name(attractors, step.active_attractor)
    cell = ORCHORBITALMemoryCellReceipt(
        memory_receipt=receipt,
        active_attractor=active.name,
        active_center=(float(active.center[0]), float(active.center[1])),
        active_mu_memory=float(active.mu_memory),
    )
    return cell, step


def centered_kepler_inverse_step(
    state_after: MemoryPhaseState,
    attractor: AttractorSpec,
    delta_tau: float,
) -> MemoryPhaseState:
    """Exact algebraic inverse of the repository centred velocity-Verlet segment."""
    try:
        relative_after = relative_state(state_after, attractor)
        relative_before = kepler_memory_inverse_step(
            relative_after,
            attractor.mu_memory,
            delta_tau,
        )
    except (ValueError, ORCHORBITALError) as exc:
        raise MemoryORCHORBITALBridgeError(str(exc)) from exc
    center = np.asarray(attractor.center, dtype=float)
    return MemoryPhaseState(
        relative_before.position + center,
        relative_before.velocity,
        relative_before.tau_internal,
        relative_before.swept_area,
    )


def memory_orchorbital_cycle_inverse(
    state_after_segment: MemoryPhaseState,
    cell: ORCHORBITALMemoryCellReceipt,
) -> MemoryPhaseState:
    """Reverse one persisted active-centre segment, then remove its Memory kick."""
    active = _snapshot_spec(cell)
    try:
        kicked = centered_kepler_inverse_step(
            state_after_segment,
            active,
            cell.memory_receipt.delta_tau,
        )
        return remove_receipt_kick(kicked, cell.memory_receipt)
    except ValueError as exc:
        raise MemoryORCHORBITALBridgeError(str(exc)) from exc


def replay_memory_orchorbital_lineage(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    receipts: Sequence[MemoryEventReceipt],
) -> tuple[list[MemoryPhaseState], tuple[ORCHORBITALMemoryCellReceipt, ...]]:
    states = [initial_state]
    cells: list[ORCHORBITALMemoryCellReceipt] = []
    current = initial_state
    for receipt in receipts:
        cell, step = memory_orchorbital_cycle_forward(current, attractors, receipt)
        cells.append(cell)
        current = step.state_after
        states.append(current)
    return states, tuple(cells)


def recall_memory_orchorbital_lineage(
    final_state: MemoryPhaseState,
    cells: Sequence[ORCHORBITALMemoryCellReceipt],
) -> list[MemoryPhaseState]:
    states = [final_state]
    current = final_state
    for cell in reversed(list(cells)):
        current = memory_orchorbital_cycle_inverse(current, cell)
        states.append(current)
    return states
