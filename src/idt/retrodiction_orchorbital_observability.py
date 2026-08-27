from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec, evaluate_attractor_field


class ORCHORBITALRetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class ORCHORBITALObservabilityAudit:
    base_jacobian: np.ndarray
    augmented_jacobian: np.ndarray
    base_rank: int
    augmented_rank: int
    unknown_dimension: int
    base_observation_dimension: int
    augmented_observation_dimension: int


_COMPONENTS = {"rx": ("position", 0), "ry": ("position", 1), "vx": ("velocity", 0), "vy": ("velocity", 1)}


def _kick_matrix(kicks: Sequence[complex]) -> np.ndarray:
    if not kicks:
        raise ORCHORBITALRetrodictionError("nominal_kicks must be non-empty")
    out = np.empty((len(kicks), 2), dtype=float)
    for i, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ORCHORBITALRetrodictionError("nominal_kicks must be finite")
        out[i] = (z.real, z.imag)
    return out


def _components(values: Sequence[str]) -> tuple[str, ...]:
    out = tuple(str(x) for x in values)
    if not out or len(set(out)) != len(out) or any(x not in _COMPONENTS for x in out):
        raise ORCHORBITALRetrodictionError("components must be a non-empty unique subset of rx, ry, vx, vy")
    return out


def _indices(count: int, checkpoint_indices: Sequence[int]) -> tuple[int, ...]:
    out = tuple(int(i) for i in checkpoint_indices)
    if not out or len(set(out)) != len(out) or any(i <= 0 or i > count for i in out):
        raise ORCHORBITALRetrodictionError("checkpoint_indices must be unique post-event indices in [1,N]")
    return out


def _forward(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kick_matrix: np.ndarray,
):
    dts = [float(x) for x in delta_taus]
    if len(dts) != len(kick_matrix) or not dts or any((not math.isfinite(x) or x <= 0.0) for x in dts):
        raise ORCHORBITALRetrodictionError("delta_taus must be positive finite and match nominal_kicks")
    receipts = [
        MemoryEventReceipt(dt, 1.0, complex(float(kick[0]), float(kick[1])))
        for dt, kick in zip(dts, kick_matrix)
    ]
    try:
        states, cells = replay_memory_orchorbital_lineage(initial_state, attractors, receipts)
    except ValueError as exc:
        raise ORCHORBITALRetrodictionError(str(exc)) from exc
    return states, cells


def _observe(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kick_matrix: np.ndarray,
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    include_weights: bool,
) -> tuple[np.ndarray, tuple]:
    states, cells = _forward(initial_state, attractors, delta_taus, kick_matrix)
    indices = _indices(len(kick_matrix), checkpoint_indices)
    comps = _components(components)
    values: list[float] = []
    checkpoint_regime = []
    for idx in indices:
        state = states[idx]
        for comp in comps:
            field_name, axis = _COMPONENTS[comp]
            arr = getattr(state, field_name)
            values.append(float(arr[axis]))
        field = evaluate_attractor_field(state, attractors)
        if field.leak_mode:
            raise ORCHORBITALRetrodictionError("observed checkpoint entered LEAK_MODE")
        support = tuple(ev.weight > 0.0 for ev in field.evaluations)
        checkpoint_regime.append((field.active_attractor, support))
        if include_weights:
            values.extend(float(ev.weight) for ev in field.evaluations)
    regime = (tuple(cell.active_attractor for cell in cells), tuple(checkpoint_regime))
    return np.asarray(values, dtype=float), regime


def orchorbital_kick_sensitivity_matrix(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    include_weights: bool,
    finite_difference_step: float = 1e-7,
) -> np.ndarray:
    kicks = _kick_matrix(nominal_kicks)
    eps = float(finite_difference_step)
    if not math.isfinite(eps) or eps <= 0.0:
        raise ORCHORBITALRetrodictionError("finite_difference_step must be finite and strictly positive")
    y0, regime0 = _observe(
        initial_state, attractors, delta_taus, kicks, checkpoint_indices, components,
        include_weights=include_weights,
    )
    jac = np.empty((y0.size, kicks.size), dtype=float)
    for column in range(kicks.size):
        plus = kicks.copy()
        minus = kicks.copy()
        plus.flat[column] += eps
        minus.flat[column] -= eps
        yp, regime_p = _observe(
            initial_state, attractors, delta_taus, plus, checkpoint_indices, components,
            include_weights=include_weights,
        )
        ym, regime_m = _observe(
            initial_state, attractors, delta_taus, minus, checkpoint_indices, components,
            include_weights=include_weights,
        )
        if regime_p != regime0 or regime_m != regime0:
            raise ORCHORBITALRetrodictionError("finite difference crossed an attractor/support boundary")
        jac[:, column] = (yp - ym) / (2.0 * eps)
    if not np.all(np.isfinite(jac)):
        raise ORCHORBITALRetrodictionError("non-finite ORCHORBITAL sensitivity matrix")
    return jac


def _rank(matrix: np.ndarray, relative_rank_tolerance: float) -> int:
    tol = float(relative_rank_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise ORCHORBITALRetrodictionError("relative_rank_tolerance must be finite and strictly positive")
    singular = np.linalg.svd(matrix, compute_uv=False)
    if singular.size == 0:
        return 0
    threshold = tol * max(1.0, float(singular[0]))
    return int(np.sum(singular > threshold))


def audit_orchorbital_augmented_observability(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-7,
) -> ORCHORBITALObservabilityAudit:
    base = orchorbital_kick_sensitivity_matrix(
        initial_state, attractors, delta_taus, nominal_kicks, checkpoint_indices, components,
        include_weights=False, finite_difference_step=finite_difference_step,
    )
    augmented = orchorbital_kick_sensitivity_matrix(
        initial_state, attractors, delta_taus, nominal_kicks, checkpoint_indices, components,
        include_weights=True, finite_difference_step=finite_difference_step,
    )
    return ORCHORBITALObservabilityAudit(
        base,
        augmented,
        _rank(base, relative_rank_tolerance),
        _rank(augmented, relative_rank_tolerance),
        2 * len(nominal_kicks),
        int(base.shape[0]),
        int(augmented.shape[0]),
    )
