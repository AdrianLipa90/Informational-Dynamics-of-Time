from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .event_memory_kick import derived_memory_kick
from .kepler_memory import (
    KeplerMemoryError,
    MemoryPhaseState,
    kepler_memory_step,
    memory_angular_momentum,
    memory_gravity,
    specific_memory_energy,
)


class MemoryRecallError(ValueError):
    pass


@dataclass(frozen=True)
class MemoryEventReceipt:
    delta_tau: float
    event_weight: float
    delta_m: complex


@dataclass(frozen=True)
class MemoryInvariantSignature:
    energy_before: float
    energy_after: float
    angular_momentum_before: float
    angular_momentum_after: float

    @property
    def delta_energy(self) -> float:
        return self.energy_after - self.energy_before

    @property
    def delta_angular_momentum(self) -> float:
        return self.angular_momentum_after - self.angular_momentum_before


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise MemoryRecallError(f"{name} must be finite and strictly positive")
    return x


def _receipt(receipt: MemoryEventReceipt) -> MemoryEventReceipt:
    dt = _positive(receipt.delta_tau, "delta_tau")
    q = float(receipt.event_weight)
    dm = complex(receipt.delta_m)
    if not math.isfinite(q) or q < 0.0:
        raise MemoryRecallError("event_weight must be finite and non-negative")
    if not (math.isfinite(dm.real) and math.isfinite(dm.imag)):
        raise MemoryRecallError("delta_m must be finite")
    return MemoryEventReceipt(dt, q, dm)


def _state_copy(state: MemoryPhaseState) -> MemoryPhaseState:
    r = np.asarray(state.position, dtype=float)
    v = np.asarray(state.velocity, dtype=float)
    if r.shape != (2,) or v.shape != (2,):
        raise MemoryRecallError("memory state position and velocity must be two-component vectors")
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(v)):
        raise MemoryRecallError("memory state must be finite")
    tau = float(state.tau_internal)
    area = float(state.swept_area)
    if not (math.isfinite(tau) and math.isfinite(area)):
        raise MemoryRecallError("memory state tau_internal and swept_area must be finite")
    return MemoryPhaseState(r.copy(), v.copy(), tau, area)


def receipt_kick_vector(receipt: MemoryEventReceipt) -> np.ndarray:
    rec = _receipt(receipt)
    kick = derived_memory_kick(rec.delta_m, rec.event_weight)
    return np.array([kick.real, kick.imag], dtype=float)


def apply_receipt_kick(state: MemoryPhaseState, receipt: MemoryEventReceipt) -> MemoryPhaseState:
    s = _state_copy(state)
    dv = receipt_kick_vector(receipt)
    return MemoryPhaseState(s.position.copy(), s.velocity + dv, s.tau_internal, s.swept_area)


def remove_receipt_kick(state: MemoryPhaseState, receipt: MemoryEventReceipt) -> MemoryPhaseState:
    s = _state_copy(state)
    dv = receipt_kick_vector(receipt)
    return MemoryPhaseState(s.position.copy(), s.velocity - dv, s.tau_internal, s.swept_area)


def kepler_memory_inverse_step(state: MemoryPhaseState, mu_memory: float, delta_tau: float) -> MemoryPhaseState:
    """Exact algebraic inverse of the repository velocity-Verlet reference step."""
    s1 = _state_copy(state)
    dt = _positive(delta_tau, "delta_tau")
    r1 = s1.position
    v1 = s1.velocity
    try:
        a1 = memory_gravity(r1, mu_memory)
        r0 = r1 - v1 * dt + 0.5 * a1 * dt * dt
        a0 = memory_gravity(r0, mu_memory)
    except KeplerMemoryError as exc:
        raise MemoryRecallError(str(exc)) from exc
    v0 = v1 - 0.5 * (a0 + a1) * dt
    swept = 0.5 * float(r0[0] * r1[1] - r0[1] * r1[0])
    return MemoryPhaseState(r0, v0, s1.tau_internal - dt, s1.swept_area - swept)


def memory_cycle_forward(state_before_event: MemoryPhaseState, mu_memory: float, receipt: MemoryEventReceipt) -> MemoryPhaseState:
    """One lineage cell: localized event kick, then one smooth Kepler segment."""
    rec = _receipt(receipt)
    kicked = apply_receipt_kick(state_before_event, rec)
    try:
        return kepler_memory_step(kicked, mu_memory, rec.delta_tau)
    except KeplerMemoryError as exc:
        raise MemoryRecallError(str(exc)) from exc


def memory_cycle_inverse(state_after_segment: MemoryPhaseState, mu_memory: float, receipt: MemoryEventReceipt) -> MemoryPhaseState:
    """Inverse lineage cell: reverse smooth segment, then remove its recorded kick."""
    rec = _receipt(receipt)
    kicked = kepler_memory_inverse_step(state_after_segment, mu_memory, rec.delta_tau)
    return remove_receipt_kick(kicked, rec)


def replay_memory_lineage(initial_state: MemoryPhaseState, mu_memory: float, receipts: Iterable[MemoryEventReceipt]) -> list[MemoryPhaseState]:
    states = [_state_copy(initial_state)]
    current = states[0]
    for receipt in receipts:
        current = memory_cycle_forward(current, mu_memory, receipt)
        states.append(current)
    return states


def recall_memory_lineage(final_state: MemoryPhaseState, mu_memory: float, receipts: Sequence[MemoryEventReceipt]) -> list[MemoryPhaseState]:
    """Ledger-assisted reverse reconstruction in reverse chronological order."""
    current = _state_copy(final_state)
    states = [current]
    for receipt in reversed(list(receipts)):
        current = memory_cycle_inverse(current, mu_memory, receipt)
        states.append(current)
    return states


def event_invariant_signature(state_before_event: MemoryPhaseState, mu_memory: float, receipt: MemoryEventReceipt) -> MemoryInvariantSignature:
    """Invariant jump written by one event before the subsequent smooth segment."""
    before = _state_copy(state_before_event)
    after = apply_receipt_kick(before, receipt)
    try:
        e0 = specific_memory_energy(before.position, before.velocity, mu_memory)
        e1 = specific_memory_energy(after.position, after.velocity, mu_memory)
    except KeplerMemoryError as exc:
        raise MemoryRecallError(str(exc)) from exc
    h0 = memory_angular_momentum(before.position, before.velocity)
    h1 = memory_angular_momentum(after.position, after.velocity)
    return MemoryInvariantSignature(e0, e1, h0, h1)
