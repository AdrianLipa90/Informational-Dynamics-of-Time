from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState, memory_gravity
from .memory_orchorbital_bridge import centered_kepler_inverse_step
from .orchorbital import AttractorSpec, centered_kepler_step, evaluate_attractor_field


class FiniteBranchRetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class KineticWeightInversion:
    kinetic_energy: float
    support_indices: tuple[int, ...]
    pivot_index: int
    reconstructed_weights: np.ndarray
    max_weight_residual: float


@dataclass(frozen=True)
class TwoEventBranchCandidate:
    final_velocity_y: float
    kick_first: complex
    kick_second: complex
    earlier_weight: float
    earlier_weight_residual: float
    forward_residual: float
    active_first_ok: bool
    active_second_ok: bool


@dataclass(frozen=True)
class TwoEventFiniteBranchResult:
    status: str
    kinetic_inversion: KineticWeightInversion
    regular_candidates: tuple[TwoEventBranchCandidate, ...]
    matching_candidates: tuple[TwoEventBranchCandidate, ...]


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise FiniteBranchRetrodictionError(f"{name} must be finite and strictly positive")
    return x


def _vec2(value: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (2,) or not np.all(np.isfinite(arr)):
        raise FiniteBranchRetrodictionError(f"{name} must be finite two-component")
    return arr


def _weights(values: Sequence[float]) -> np.ndarray:
    w = np.asarray(values, dtype=float)
    if w.ndim != 1 or w.size < 2 or not np.all(np.isfinite(w)) or np.any(w < 0.0):
        raise FiniteBranchRetrodictionError("basin_weights must be a finite non-negative vector of length >=2")
    if abs(float(np.sum(w)) - 1.0) > 1e-9:
        raise FiniteBranchRetrodictionError("basin_weights must sum to one")
    return w


def _attractors(attractors: Sequence[AttractorSpec], expected: int | None = None) -> tuple[AttractorSpec, ...]:
    specs = tuple(attractors)
    if not specs or (expected is not None and len(specs) != expected):
        raise FiniteBranchRetrodictionError("attractor count must match basin_weights")
    names: set[str] = set()
    for spec in specs:
        name = str(spec.name)
        if not name or name in names:
            raise FiniteBranchRetrodictionError("attractor names must be non-empty and unique")
        names.add(name)
        _vec2(spec.center, f"center[{name}]")
        _positive(spec.mu_memory, f"mu_memory[{name}]")
    return specs


def kinetic_energy_from_basin_weights(
    position: Sequence[float],
    basin_weights: Sequence[float],
    attractors: Sequence[AttractorSpec],
    *,
    support_tolerance: float = 1e-12,
    degeneracy_tolerance: float = 1e-10,
    consistency_tolerance: float = 1e-9,
) -> KineticWeightInversion:
    """Invert fixed-support ORCHORBITAL basin weights to T=|v|^2/2."""
    r = _vec2(position, "position")
    w = _weights(basin_weights)
    specs = _attractors(attractors, expected=w.size)
    st = _positive(support_tolerance, "support_tolerance")
    dt = _positive(degeneracy_tolerance, "degeneracy_tolerance")
    ct = _positive(consistency_tolerance, "consistency_tolerance")

    potentials = np.asarray(
        [float(spec.mu_memory) / float(np.linalg.norm(r - np.asarray(spec.center, dtype=float))) for spec in specs],
        dtype=float,
    )
    if not np.all(np.isfinite(potentials)):
        raise FiniteBranchRetrodictionError("non-finite attractor potential")
    support = tuple(int(i) for i in np.flatnonzero(w > st))
    if len(support) < 2:
        raise FiniteBranchRetrodictionError("WEIGHT_KINETIC_CHANNEL_DEGENERATE: support size must be at least two")

    m = len(support)
    ws = w[list(support)]
    us = potentials[list(support)]
    total_potential = float(np.sum(us))
    denominators = 1.0 - m * ws
    local_pivot = int(np.argmax(np.abs(denominators)))
    if abs(float(denominators[local_pivot])) <= dt:
        raise FiniteBranchRetrodictionError("WEIGHT_KINETIC_CHANNEL_DEGENERATE: supported weights are uniform")

    kinetic = float(
        (us[local_pivot] - ws[local_pivot] * total_potential)
        / denominators[local_pivot]
    )
    if not math.isfinite(kinetic) or kinetic < -ct:
        raise FiniteBranchRetrodictionError("reconstructed kinetic energy must be finite and non-negative")
    kinetic = max(0.0, kinetic)

    binding = np.maximum(0.0, potentials - kinetic)
    total_binding = float(np.sum(binding))
    if total_binding <= 0.0:
        raise FiniteBranchRetrodictionError("reconstructed state entered LEAK_MODE")
    reconstructed = binding / total_binding
    reconstructed_support = tuple(int(i) for i in np.flatnonzero(reconstructed > st))
    if reconstructed_support != support:
        raise FiniteBranchRetrodictionError("reconstructed kinetic energy changed the declared basin support")
    residual = float(np.max(np.abs(reconstructed - w)))
    if residual > ct:
        raise FiniteBranchRetrodictionError("basin weights are inconsistent with one fixed-support kinetic scalar")

    return KineticWeightInversion(
        kinetic,
        support,
        support[local_pivot],
        reconstructed,
        residual,
    )


def final_velocity_y_branches(
    velocity_x: float,
    kinetic_energy: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[float, ...]:
    vx = float(velocity_x)
    kinetic = float(kinetic_energy)
    tol = _positive(tolerance, "tolerance")
    if not (math.isfinite(vx) and math.isfinite(kinetic) and kinetic >= 0.0):
        raise FiniteBranchRetrodictionError("velocity_x and kinetic_energy must be finite with T>=0")
    radicand = 2.0 * kinetic - vx * vx
    if radicand < -tol:
        raise FiniteBranchRetrodictionError("retained velocity_x exceeds reconstructed kinetic speed")
    if abs(radicand) <= tol:
        return (0.0,)
    vy = math.sqrt(radicand)
    return (vy, -vy)


def _attractor_by_name(attractors: Sequence[AttractorSpec], name: str) -> AttractorSpec:
    for spec in attractors:
        if spec.name == name:
            return spec
    raise FiniteBranchRetrodictionError(f"attractor {name!r} is absent")


def first_kick_from_intermediate_position(
    initial_state: MemoryPhaseState,
    intermediate_position: Sequence[float],
    active_first: AttractorSpec,
    delta_tau_first: float,
) -> np.ndarray:
    dt = _positive(delta_tau_first, "delta_tau_first")
    r0 = _vec2(initial_state.position, "initial_state.position")
    v0 = _vec2(initial_state.velocity, "initial_state.velocity")
    r1 = _vec2(intermediate_position, "intermediate_position")
    center = _vec2(active_first.center, "active_first.center")
    try:
        a0 = memory_gravity(r0 - center, active_first.mu_memory)
    except ValueError as exc:
        raise FiniteBranchRetrodictionError(str(exc)) from exc
    kicked_velocity = (r1 - r0 - 0.5 * a0 * dt * dt) / dt
    return kicked_velocity - v0


def _branch_candidate(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    active_first: AttractorSpec,
    active_second: AttractorSpec,
    delta_tau_first: float,
    delta_tau_second: float,
    final_position: np.ndarray,
    final_velocity_x: float,
    final_velocity_y: float,
    earlier_weight_attractor: str,
    earlier_weight_observed: float,
) -> TwoEventBranchCandidate:
    dt1 = _positive(delta_tau_first, "delta_tau_first")
    dt2 = _positive(delta_tau_second, "delta_tau_second")
    final_state = MemoryPhaseState(
        final_position.copy(),
        np.asarray([final_velocity_x, final_velocity_y], dtype=float),
        float(initial_state.tau_internal) + dt1 + dt2,
        0.0,
    )
    try:
        pre_second = centered_kepler_inverse_step(final_state, active_second, dt2)
    except ValueError as exc:
        raise FiniteBranchRetrodictionError(str(exc)) from exc

    kick1 = first_kick_from_intermediate_position(
        initial_state,
        pre_second.position,
        active_first,
        dt1,
    )
    kicked0 = MemoryPhaseState(
        np.asarray(initial_state.position, dtype=float).copy(),
        np.asarray(initial_state.velocity, dtype=float) + kick1,
        float(initial_state.tau_internal),
        float(initial_state.swept_area),
    )
    field0 = evaluate_attractor_field(kicked0, attractors)
    active_first_ok = not field0.leak_mode and field0.active_attractor == active_first.name

    state1 = centered_kepler_step(kicked0, active_first, dt1)
    kick2 = np.asarray(pre_second.velocity, dtype=float) - np.asarray(state1.velocity, dtype=float)
    kicked1 = MemoryPhaseState(
        np.asarray(state1.position, dtype=float).copy(),
        np.asarray(state1.velocity, dtype=float) + kick2,
        float(state1.tau_internal),
        float(state1.swept_area),
    )
    field1_kicked = evaluate_attractor_field(kicked1, attractors)
    active_second_ok = not field1_kicked.leak_mode and field1_kicked.active_attractor == active_second.name

    earlier_field = evaluate_attractor_field(state1, attractors)
    if earlier_field.leak_mode:
        raise FiniteBranchRetrodictionError("earlier checkpoint entered LEAK_MODE")
    names = [ev.name for ev in earlier_field.evaluations]
    if earlier_weight_attractor not in names:
        raise FiniteBranchRetrodictionError("earlier weight attractor is absent")
    earlier_weight = float(
        earlier_field.evaluations[names.index(earlier_weight_attractor)].weight
    )

    replay = centered_kepler_step(kicked1, active_second, dt2)
    forward_residual = float(
        np.linalg.norm(np.asarray(replay.position) - final_state.position)
        + np.linalg.norm(np.asarray(replay.velocity) - final_state.velocity)
    )
    return TwoEventBranchCandidate(
        float(final_velocity_y),
        complex(float(kick1[0]), float(kick1[1])),
        complex(float(kick2[0]), float(kick2[1])),
        earlier_weight,
        abs(earlier_weight - float(earlier_weight_observed)),
        forward_residual,
        active_first_ok,
        active_second_ok,
    )


def retrodict_two_event_finite_branches(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    active_first_name: str,
    active_second_name: str,
    delta_tau_first: float,
    delta_tau_second: float,
    final_position: Sequence[float],
    final_velocity_x: float,
    final_basin_weights: Sequence[float],
    earlier_weight_attractor: str,
    earlier_weight_observed: float,
    *,
    equivalence_tolerance: float = 1e-9,
) -> TwoEventFiniteBranchResult:
    specs = _attractors(attractors)
    r2 = _vec2(final_position, "final_position")
    vx2 = float(final_velocity_x)
    earlier_weight = float(earlier_weight_observed)
    tol = _positive(equivalence_tolerance, "equivalence_tolerance")
    if not (math.isfinite(vx2) and math.isfinite(earlier_weight) and 0.0 <= earlier_weight <= 1.0):
        raise FiniteBranchRetrodictionError("retained final velocity and earlier weight must be finite")

    active_first = _attractor_by_name(specs, str(active_first_name))
    active_second = _attractor_by_name(specs, str(active_second_name))
    inversion = kinetic_energy_from_basin_weights(r2, final_basin_weights, specs)
    branches = final_velocity_y_branches(vx2, inversion.kinetic_energy)

    candidates = tuple(
        _branch_candidate(
            initial_state,
            specs,
            active_first,
            active_second,
            delta_tau_first,
            delta_tau_second,
            r2,
            vx2,
            vy,
            str(earlier_weight_attractor),
            earlier_weight,
        )
        for vy in branches
    )
    regular = tuple(
        candidate
        for candidate in candidates
        if candidate.active_first_ok
        and candidate.active_second_ok
        and candidate.forward_residual <= 10.0 * tol
    )
    matching = tuple(
        candidate
        for candidate in regular
        if candidate.earlier_weight_residual <= tol
    )

    if len(matching) == 1:
        status = "UNIQUE_FIXED_REGIME_TWO_EVENT"
    elif len(matching) == 0:
        status = "INCONSISTENT_OBSERVATION"
    else:
        status = "GLOBAL_BRANCH_AMBIGUITY"
    return TwoEventFiniteBranchResult(status, inversion, regular, matching)
