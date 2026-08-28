from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState, memory_gravity
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec


class PositionLineageRetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class PositionLineageRetrodictionResult:
    kicks: tuple[complex, ...]
    states: tuple[MemoryPhaseState, ...]
    status: str
    observation_dimension: int
    latent_dimension: int
    max_position_residual: float


def _state_vectors(state: MemoryPhaseState, name: str) -> tuple[np.ndarray, np.ndarray]:
    r = np.asarray(state.position, dtype=float)
    v = np.asarray(state.velocity, dtype=float)
    if r.shape != (2,) or v.shape != (2,):
        raise PositionLineageRetrodictionError(
            f"{name} position and velocity must be two-component vectors"
        )
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(v)):
        raise PositionLineageRetrodictionError(f"{name} must be finite")
    return r, v


def _attractor_map(attractors: Sequence[AttractorSpec]) -> tuple[tuple[AttractorSpec, ...], dict[str, AttractorSpec]]:
    if not attractors:
        raise PositionLineageRetrodictionError("attractors must be non-empty")
    specs: list[AttractorSpec] = []
    mapping: dict[str, AttractorSpec] = {}
    for raw in attractors:
        name = str(raw.name).strip()
        center = np.asarray(raw.center, dtype=float)
        mu = float(raw.mu_memory)
        if not name or name in mapping:
            raise PositionLineageRetrodictionError(
                "attractor names must be non-empty and unique"
            )
        if center.shape != (2,) or not np.all(np.isfinite(center)):
            raise PositionLineageRetrodictionError(
                "attractor centers must be finite two-component vectors"
            )
        if not math.isfinite(mu) or mu <= 0.0:
            raise PositionLineageRetrodictionError(
                "attractor mu_memory values must be finite and strictly positive"
            )
        spec = AttractorSpec(name, center.copy(), mu)
        specs.append(spec)
        mapping[name] = spec
    return tuple(specs), mapping


def _positions(values: Sequence[Sequence[float]]) -> tuple[np.ndarray, ...]:
    if len(values) == 0:
        raise PositionLineageRetrodictionError(
            "checkpoint_positions must be non-empty"
        )
    out: list[np.ndarray] = []
    for raw in values:
        arr = np.asarray(raw, dtype=float)
        if arr.shape != (2,) or not np.all(np.isfinite(arr)):
            raise PositionLineageRetrodictionError(
                "checkpoint positions must be finite two-component vectors"
            )
        out.append(arr.copy())
    return tuple(out)


def retrodict_kicks_from_position_lineage(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    active_sequence: Sequence[str],
    delta_taus: Sequence[float],
    checkpoint_positions: Sequence[Sequence[float]],
    *,
    position_tolerance: float = 1e-9,
) -> PositionLineageRetrodictionResult:
    """Recover an N-event kick lineage exactly from ordered post-segment positions.

    The active-attractor sequence is treated as retained ORCHORBITAL lineage.
    Each two-component position checkpoint supplies exactly two scalar constraints
    for the corresponding two-component event kick.
    """
    r0, v0 = _state_vectors(initial_state, "initial_state")
    specs, mapping = _attractor_map(attractors)
    positions = _positions(checkpoint_positions)
    names = tuple(str(name) for name in active_sequence)
    dts = tuple(float(value) for value in delta_taus)
    n = len(positions)
    if len(names) != n or len(dts) != n:
        raise PositionLineageRetrodictionError(
            "active_sequence, delta_taus and checkpoint_positions must have equal length"
        )
    if any(name not in mapping for name in names):
        raise PositionLineageRetrodictionError(
            "active_sequence contains an unknown attractor"
        )
    if any((not math.isfinite(dt) or dt <= 0.0) for dt in dts):
        raise PositionLineageRetrodictionError(
            "delta_taus must be finite and strictly positive"
        )
    tol = float(position_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise PositionLineageRetrodictionError(
            "position_tolerance must be finite and strictly positive"
        )

    current_r = r0.copy()
    current_v = v0.copy()
    kicks: list[complex] = []
    for name, dt, next_r in zip(names, dts, positions):
        spec = mapping[name]
        rel0 = current_r - np.asarray(spec.center, dtype=float)
        rel1 = next_r - np.asarray(spec.center, dtype=float)
        try:
            a0 = memory_gravity(rel0, spec.mu_memory)
            a1 = memory_gravity(rel1, spec.mu_memory)
        except ValueError as exc:
            raise PositionLineageRetrodictionError(str(exc)) from exc
        velocity_after_kick = (
            rel1 - rel0 - 0.5 * a0 * dt * dt
        ) / dt
        kick = velocity_after_kick - current_v
        next_v = velocity_after_kick + 0.5 * (a0 + a1) * dt
        if not np.all(np.isfinite(kick)) or not np.all(np.isfinite(next_v)):
            raise PositionLineageRetrodictionError(
                "reconstructed kick or velocity became non-finite"
            )
        kicks.append(complex(float(kick[0]), float(kick[1])))
        current_r = next_r.copy()
        current_v = next_v

    receipts = tuple(
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip(dts, kicks)
    )
    try:
        states, cells = replay_memory_orchorbital_lineage(
            initial_state,
            specs,
            receipts,
        )
    except ValueError as exc:
        raise PositionLineageRetrodictionError(str(exc)) from exc
    replay_names = tuple(cell.active_attractor for cell in cells)
    if replay_names != names:
        raise PositionLineageRetrodictionError(
            "reconstructed lineage does not reproduce the declared active-attractor sequence"
        )

    residuals = [
        float(np.linalg.norm(np.asarray(state.position, dtype=float) - target))
        for state, target in zip(states[1:], positions)
    ]
    max_residual = max(residuals, default=0.0)
    if max_residual > tol:
        raise PositionLineageRetrodictionError(
            "reconstructed lineage exceeds the declared position tolerance"
        )
    return PositionLineageRetrodictionResult(
        tuple(kicks),
        tuple(states),
        "EXACT_POSITION_LINEAGE_RECOVERY",
        2 * n,
        2 * n,
        max_residual,
    )
