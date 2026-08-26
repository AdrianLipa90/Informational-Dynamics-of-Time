from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import KeplerMemoryError, MemoryPhaseState, kepler_memory_step, specific_memory_energy


class ORCHORBITALError(ValueError):
    pass


@dataclass(frozen=True)
class AttractorSpec:
    name: str
    center: np.ndarray
    mu_memory: float


@dataclass(frozen=True)
class AttractorEvaluation:
    name: str
    radius: float
    specific_energy: float
    binding_margin: float
    weight: float


@dataclass(frozen=True)
class AttractorFieldState:
    evaluations: tuple[AttractorEvaluation, ...]
    active_attractor: str | None
    leak_mode: bool
    attractor_entropy_bits: float | None
    attractor_coherence: float | None


@dataclass(frozen=True)
class ORCHORBITALStep:
    state_before: MemoryPhaseState
    state_after: MemoryPhaseState
    field_before: AttractorFieldState
    field_after: AttractorFieldState
    active_attractor: str
    winding_increment: float
    switched_after_segment: bool


def _vec2(value: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (2,) or not np.all(np.isfinite(arr)):
        raise ORCHORBITALError(f"{name} must be a finite two-component vector")
    return arr


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise ORCHORBITALError(f"{name} must be finite and strictly positive")
    return x


def _validated_attractors(attractors: Sequence[AttractorSpec]) -> tuple[AttractorSpec, ...]:
    if not attractors:
        raise ORCHORBITALError("attractors must be non-empty")
    out: list[AttractorSpec] = []
    names: set[str] = set()
    for raw in attractors:
        name = str(raw.name).strip()
        if not name:
            raise ORCHORBITALError("attractor names must be non-empty")
        if name in names:
            raise ORCHORBITALError("attractor names must be unique")
        names.add(name)
        out.append(
            AttractorSpec(
                name,
                _vec2(raw.center, f"center[{name}]").copy(),
                _positive(raw.mu_memory, f"mu_memory[{name}]"),
            )
        )
    return tuple(out)


def relative_state(state: MemoryPhaseState, attractor: AttractorSpec) -> MemoryPhaseState:
    return MemoryPhaseState(
        _vec2(state.position, "state.position") - _vec2(attractor.center, "attractor.center"),
        _vec2(state.velocity, "state.velocity").copy(),
        float(state.tau_internal),
        float(state.swept_area),
    )


def evaluate_attractor_field(state: MemoryPhaseState, attractors: Sequence[AttractorSpec]) -> AttractorFieldState:
    specs = _validated_attractors(attractors)
    position = _vec2(state.position, "state.position")
    velocity = _vec2(state.velocity, "state.velocity")
    raw: list[tuple[str, float, float, float]] = []
    for spec in specs:
        relative_position = position - spec.center
        radius = float(np.linalg.norm(relative_position))
        if radius <= 0.0:
            raise ORCHORBITALError(f"state is singular at attractor center {spec.name}")
        try:
            energy = specific_memory_energy(relative_position, velocity, spec.mu_memory)
        except KeplerMemoryError as exc:
            raise ORCHORBITALError(str(exc)) from exc
        binding = max(0.0, -float(energy))
        raw.append((spec.name, radius, float(energy), binding))

    total_binding = float(sum(item[3] for item in raw))
    if total_binding <= 0.0:
        evaluations = tuple(
            AttractorEvaluation(name, radius, energy, binding, 0.0)
            for name, radius, energy, binding in raw
        )
        return AttractorFieldState(evaluations, None, True, None, None)

    evaluations = tuple(
        AttractorEvaluation(name, radius, energy, binding, binding / total_binding)
        for name, radius, energy, binding in raw
    )
    active = min(evaluations, key=lambda item: (-item.weight, item.name)).name
    weights = np.asarray([item.weight for item in evaluations if item.weight > 0.0], dtype=float)
    entropy = float(-np.sum(weights * np.log2(weights)))
    if len(evaluations) <= 1:
        coherence = 1.0
    else:
        coherence = float(1.0 - entropy / math.log2(len(evaluations)))
        coherence = min(1.0, max(0.0, coherence))
    return AttractorFieldState(evaluations, active, False, entropy, coherence)


def active_attractor_spec(field: AttractorFieldState, attractors: Sequence[AttractorSpec]) -> AttractorSpec:
    specs = _validated_attractors(attractors)
    if field.leak_mode or field.active_attractor is None:
        raise ORCHORBITALError("LEAK_MODE: no bound attractor admitted for orbital propagation")
    for spec in specs:
        if spec.name == field.active_attractor:
            return spec
    raise ORCHORBITALError("active attractor is absent from attractor specification")


def centered_kepler_step(state: MemoryPhaseState, attractor: AttractorSpec, delta_tau: float) -> MemoryPhaseState:
    relative = relative_state(state, attractor)
    try:
        relative_next = kepler_memory_step(relative, attractor.mu_memory, delta_tau)
    except KeplerMemoryError as exc:
        raise ORCHORBITALError(str(exc)) from exc
    return MemoryPhaseState(
        relative_next.position + attractor.center,
        relative_next.velocity,
        relative_next.tau_internal,
        relative_next.swept_area,
    )


def wrapped_angle_difference(theta_after: float, theta_before: float) -> float:
    delta = float(theta_after) - float(theta_before)
    if not math.isfinite(delta):
        raise ORCHORBITALError("angles must be finite")
    return float(math.atan2(math.sin(delta), math.cos(delta)))


def winding_increment(
    position_before: Sequence[float],
    position_after: Sequence[float],
    center: Sequence[float],
) -> float:
    attractor_center = _vec2(center, "center")
    r0 = _vec2(position_before, "position_before") - attractor_center
    r1 = _vec2(position_after, "position_after") - attractor_center
    if float(np.linalg.norm(r0)) <= 0.0 or float(np.linalg.norm(r1)) <= 0.0:
        raise ORCHORBITALError("winding is singular at attractor center")
    theta0 = math.atan2(float(r0[1]), float(r0[0]))
    theta1 = math.atan2(float(r1[1]), float(r1[0]))
    return wrapped_angle_difference(theta1, theta0) / (2.0 * math.pi)


def orchorbital_step(
    state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_tau: float,
) -> ORCHORBITALStep:
    field_before = evaluate_attractor_field(state, attractors)
    active = active_attractor_spec(field_before, attractors)
    next_state = centered_kepler_step(state, active, delta_tau)
    delta_winding = winding_increment(state.position, next_state.position, active.center)
    field_after = evaluate_attractor_field(next_state, attractors)
    return ORCHORBITALStep(
        state_before=state,
        state_after=next_state,
        field_before=field_before,
        field_after=field_after,
        active_attractor=active.name,
        winding_increment=delta_winding,
        switched_after_segment=(field_after.active_attractor != active.name),
    )


def phase_space_closure_defect(
    initial_state: MemoryPhaseState,
    final_state: MemoryPhaseState,
    *,
    position_scale: float,
    velocity_scale: float,
) -> float:
    rs = _positive(position_scale, "position_scale")
    vs = _positive(velocity_scale, "velocity_scale")
    delta_position = _vec2(final_state.position, "final_state.position") - _vec2(
        initial_state.position,
        "initial_state.position",
    )
    delta_velocity = _vec2(final_state.velocity, "final_state.velocity") - _vec2(
        initial_state.velocity,
        "initial_state.velocity",
    )
    return float(
        math.sqrt(
            (float(np.linalg.norm(delta_position)) / rs) ** 2
            + (float(np.linalg.norm(delta_velocity)) / vs) ** 2
        )
    )
