from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState, memory_gravity
from .memory_orchorbital_bridge import (
    centered_kepler_inverse_step,
    replay_memory_orchorbital_lineage,
)
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec


class TwoEventExactRetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class TwoEventRetrodictionCandidate:
    active_sequence: tuple[str, str]
    kicks: tuple[complex, complex]
    final_phase_residual: float


@dataclass(frozen=True)
class TwoEventRetrodictionAudit:
    candidates: tuple[TwoEventRetrodictionCandidate, ...]
    status: str
    attractor_count: int
    enumerated_sequences: int


def _state_vectors(state: MemoryPhaseState, name: str) -> tuple[np.ndarray, np.ndarray]:
    r = np.asarray(state.position, dtype=float)
    v = np.asarray(state.velocity, dtype=float)
    if r.shape != (2,) or v.shape != (2,):
        raise TwoEventExactRetrodictionError(
            f"{name} position and velocity must be two-component vectors"
        )
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(v)):
        raise TwoEventExactRetrodictionError(f"{name} must be finite")
    return r, v


def _attractors(values: Sequence[AttractorSpec]) -> tuple[AttractorSpec, ...]:
    if not values:
        raise TwoEventExactRetrodictionError("attractors must be non-empty")
    out: list[AttractorSpec] = []
    names: set[str] = set()
    for raw in values:
        name = str(raw.name).strip()
        center = np.asarray(raw.center, dtype=float)
        mu = float(raw.mu_memory)
        if not name or name in names:
            raise TwoEventExactRetrodictionError(
                "attractor names must be non-empty and unique"
            )
        if center.shape != (2,) or not np.all(np.isfinite(center)):
            raise TwoEventExactRetrodictionError(
                "attractor centers must be finite two-component vectors"
            )
        if not math.isfinite(mu) or mu <= 0.0:
            raise TwoEventExactRetrodictionError(
                "attractor mu_memory values must be finite and strictly positive"
            )
        names.add(name)
        out.append(AttractorSpec(name, center.copy(), mu))
    return tuple(out)


def _two_positive_steps(delta_taus: Sequence[float]) -> tuple[float, float]:
    values = tuple(float(x) for x in delta_taus)
    if len(values) != 2:
        raise TwoEventExactRetrodictionError(
            "two-event exact retrodiction requires exactly two delta_taus"
        )
    if any((not math.isfinite(x) or x <= 0.0) for x in values):
        raise TwoEventExactRetrodictionError(
            "delta_taus must be finite and strictly positive"
        )
    return values


def _phase_residual(left: MemoryPhaseState, right: MemoryPhaseState) -> float:
    lr, lv = _state_vectors(left, "left state")
    rr, rv = _state_vectors(right, "right state")
    return float(np.linalg.norm(np.concatenate((lr - rr, lv - rv))))


def _candidate_for_sequence(
    initial_state: MemoryPhaseState,
    final_state: MemoryPhaseState,
    attractors: tuple[AttractorSpec, ...],
    first: AttractorSpec,
    second: AttractorSpec,
    delta_taus: tuple[float, float],
    *,
    residual_tolerance: float,
) -> TwoEventRetrodictionCandidate | None:
    r0, v0 = _state_vectors(initial_state, "initial_state")
    _state_vectors(final_state, "final_state")
    dt1, dt2 = delta_taus
    try:
        state_after_second_kick = centered_kepler_inverse_step(
            final_state,
            second,
            dt2,
        )
    except ValueError:
        return None

    r1 = np.asarray(state_after_second_kick.position, dtype=float)
    rel0 = r0 - np.asarray(first.center, dtype=float)
    rel1 = r1 - np.asarray(first.center, dtype=float)
    try:
        a0 = memory_gravity(rel0, first.mu_memory)
        a1 = memory_gravity(rel1, first.mu_memory)
    except ValueError:
        return None

    velocity_after_first_kick = (
        rel1 - rel0 - 0.5 * a0 * dt1 * dt1
    ) / dt1
    kick1 = velocity_after_first_kick - v0
    velocity_after_first_segment = (
        velocity_after_first_kick + 0.5 * (a0 + a1) * dt1
    )
    kick2 = (
        np.asarray(state_after_second_kick.velocity, dtype=float)
        - velocity_after_first_segment
    )
    kicks = (
        complex(float(kick1[0]), float(kick1[1])),
        complex(float(kick2[0]), float(kick2[1])),
    )
    if not all(math.isfinite(z.real) and math.isfinite(z.imag) for z in kicks):
        return None

    receipts = (
        MemoryEventReceipt(dt1, 1.0, kicks[0]),
        MemoryEventReceipt(dt2, 1.0, kicks[1]),
    )
    try:
        states, cells = replay_memory_orchorbital_lineage(
            initial_state,
            attractors,
            receipts,
        )
    except ValueError:
        return None
    active_sequence = tuple(cell.active_attractor for cell in cells)
    if active_sequence != (first.name, second.name):
        return None
    residual = _phase_residual(states[-1], final_state)
    if residual > residual_tolerance:
        return None
    return TwoEventRetrodictionCandidate(
        (first.name, second.name),
        kicks,
        residual,
    )


def retrodict_two_event_full_checkpoint(
    initial_state: MemoryPhaseState,
    final_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    *,
    residual_tolerance: float = 1e-9,
) -> TwoEventRetrodictionAudit:
    """Enumerate exact two-event ORCHORBITAL branches from a full final checkpoint.

    For every ordered active-attractor pair, the discrete velocity-Verlet equations
    determine at most one continuous kick pair. A candidate is admitted only when
    forward replay selects the same active sequence and reproduces the final phase
    checkpoint within the declared tolerance.
    """
    specs = _attractors(attractors)
    steps = _two_positive_steps(delta_taus)
    _state_vectors(initial_state, "initial_state")
    _state_vectors(final_state, "final_state")
    tol = float(residual_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise TwoEventExactRetrodictionError(
            "residual_tolerance must be finite and strictly positive"
        )

    candidates: list[TwoEventRetrodictionCandidate] = []
    for first, second in itertools.product(specs, repeat=2):
        candidate = _candidate_for_sequence(
            initial_state,
            final_state,
            specs,
            first,
            second,
            steps,
            residual_tolerance=tol,
        )
        if candidate is not None:
            candidates.append(candidate)
    candidates.sort(key=lambda item: item.active_sequence)
    if not candidates:
        status = "NO_ADMISSIBLE_BRANCH"
    elif len(candidates) == 1:
        status = "EXACT_UNIQUE_REFERENCE_BRANCH"
    else:
        status = "FINITE_BRANCH_AMBIGUITY"
    return TwoEventRetrodictionAudit(
        tuple(candidates),
        status,
        len(specs),
        len(specs) ** 2,
    )
