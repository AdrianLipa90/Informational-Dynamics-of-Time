from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec, evaluate_attractor_field
from .retrodiction_orchorbital_observability import (
    ORCHORBITALRetrodictionError,
    orchorbital_kick_sensitivity_matrix,
)


class ORCHORBITALEstimationError(ValueError):
    pass


@dataclass(frozen=True)
class ORCHORBITALEstimate:
    kicks: tuple[complex, ...]
    residual_norm: float
    iterations: int
    converged: bool
    local_rank: int
    unknown_dimension: int
    regime: tuple


_COMPONENTS = {
    "rx": ("position", 0),
    "ry": ("position", 1),
    "vx": ("velocity", 0),
    "vy": ("velocity", 1),
}


def _kick_matrix(kicks: Sequence[complex]) -> np.ndarray:
    if not kicks:
        raise ORCHORBITALEstimationError("kicks must be non-empty")
    out = np.empty((len(kicks), 2), dtype=float)
    for idx, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ORCHORBITALEstimationError("kicks must be finite")
        out[idx] = (z.real, z.imag)
    return out


def _kick_tuple(matrix: np.ndarray) -> tuple[complex, ...]:
    return tuple(complex(float(row[0]), float(row[1])) for row in np.asarray(matrix, dtype=float))


def _components(values: Sequence[str]) -> tuple[str, ...]:
    out = tuple(str(x) for x in values)
    if not out or len(set(out)) != len(out) or any(x not in _COMPONENTS for x in out):
        raise ORCHORBITALEstimationError(
            "components must be a non-empty unique subset of rx, ry, vx, vy"
        )
    return out


def _indices(count: int, checkpoint_indices: Sequence[int]) -> tuple[int, ...]:
    out = tuple(int(i) for i in checkpoint_indices)
    if not out or len(set(out)) != len(out) or any(i <= 0 or i > count for i in out):
        raise ORCHORBITALEstimationError(
            "checkpoint_indices must be unique post-event indices in [1,N]"
        )
    return out


def _observation_and_regime(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    include_weights: bool,
) -> tuple[np.ndarray, tuple]:
    kick_values = _kick_matrix(kicks)
    dts = [float(x) for x in delta_taus]
    if len(dts) != len(kick_values) or not dts:
        raise ORCHORBITALEstimationError(
            "delta_taus must match kicks and contain at least one event"
        )
    if any((not math.isfinite(x) or x <= 0.0) for x in dts):
        raise ORCHORBITALEstimationError(
            "delta_taus must be finite and strictly positive"
        )
    indices = _indices(len(kick_values), checkpoint_indices)
    comps = _components(components)
    receipts = [
        MemoryEventReceipt(
            dt,
            1.0,
            complex(float(kick[0]), float(kick[1])),
        )
        for dt, kick in zip(dts, kick_values)
    ]
    try:
        states, cells = replay_memory_orchorbital_lineage(
            initial_state,
            attractors,
            receipts,
        )
    except ValueError as exc:
        raise ORCHORBITALEstimationError(str(exc)) from exc

    values: list[float] = []
    checkpoint_regime = []
    for idx in indices:
        state = states[idx]
        for component in comps:
            field_name, axis = _COMPONENTS[component]
            values.append(float(getattr(state, field_name)[axis]))
        field = evaluate_attractor_field(state, attractors)
        if field.leak_mode:
            raise ORCHORBITALEstimationError(
                "observed checkpoint entered LEAK_MODE"
            )
        support = tuple(bool(ev.weight > 0.0) for ev in field.evaluations)
        checkpoint_regime.append((field.active_attractor, support))
        if include_weights:
            values.extend(float(ev.weight) for ev in field.evaluations)

    observation = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(observation)):
        raise ORCHORBITALEstimationError("observation must be finite")
    regime = (
        tuple(cell.active_attractor for cell in cells),
        tuple(checkpoint_regime),
    )
    return observation, regime


def orchorbital_checkpoint_observation(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    include_weights: bool = True,
) -> np.ndarray:
    observation, _ = _observation_and_regime(
        initial_state,
        attractors,
        delta_taus,
        kicks,
        checkpoint_indices,
        components,
        include_weights=include_weights,
    )
    return observation


def _matrix_rank(matrix: np.ndarray, relative_rank_tolerance: float) -> int:
    tol = float(relative_rank_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise ORCHORBITALEstimationError(
            "relative_rank_tolerance must be finite and strictly positive"
        )
    singular = np.linalg.svd(np.asarray(matrix, dtype=float), compute_uv=False)
    if singular.size == 0:
        return 0
    threshold = tol * max(1.0, float(singular[0]))
    return int(np.sum(singular > threshold))


def estimate_local_orchorbital_kicks(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    target_observation: Sequence[float],
    initial_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    components: Sequence[str],
    *,
    include_weights: bool = True,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-7,
    residual_tolerance: float = 1e-10,
    max_iterations: int = 20,
    line_search_halvings: int = 14,
) -> ORCHORBITALEstimate:
    """Same-regime local Gauss-Newton retrodiction after an explicit rank gate."""
    kick_matrix = _kick_matrix(initial_kicks)
    target = np.asarray(target_observation, dtype=float)
    if target.ndim != 1 or not np.all(np.isfinite(target)):
        raise ORCHORBITALEstimationError(
            "target_observation must be a finite one-dimensional vector"
        )
    residual_tol = float(residual_tolerance)
    if not math.isfinite(residual_tol) or residual_tol <= 0.0:
        raise ORCHORBITALEstimationError(
            "residual_tolerance must be finite and strictly positive"
        )
    if not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ORCHORBITALEstimationError("max_iterations must be a positive integer")
    if not isinstance(line_search_halvings, int) or line_search_halvings < 0:
        raise ORCHORBITALEstimationError(
            "line_search_halvings must be a non-negative integer"
        )

    current_observation, regime0 = _observation_and_regime(
        initial_state,
        attractors,
        delta_taus,
        _kick_tuple(kick_matrix),
        checkpoint_indices,
        components,
        include_weights=include_weights,
    )
    if target.shape != current_observation.shape:
        raise ORCHORBITALEstimationError(
            "target_observation dimension must match the declared checkpoint observation"
        )

    unknown_dimension = int(kick_matrix.size)
    last_rank = 0

    for iteration in range(max_iterations + 1):
        current_kicks = _kick_tuple(kick_matrix)
        current_observation, current_regime = _observation_and_regime(
            initial_state,
            attractors,
            delta_taus,
            current_kicks,
            checkpoint_indices,
            components,
            include_weights=include_weights,
        )
        if current_regime != regime0:
            raise ORCHORBITALEstimationError(
                "local estimator left the initial attractor/support regime"
            )
        try:
            jacobian = orchorbital_kick_sensitivity_matrix(
                initial_state,
                attractors,
                delta_taus,
                current_kicks,
                checkpoint_indices,
                components,
                include_weights=include_weights,
                finite_difference_step=finite_difference_step,
            )
        except ORCHORBITALRetrodictionError as exc:
            raise ORCHORBITALEstimationError(str(exc)) from exc

        last_rank = _matrix_rank(jacobian, relative_rank_tolerance)
        if last_rank < unknown_dimension:
            raise ORCHORBITALEstimationError(
                "local observability rank deficient for the declared measurement"
            )

        residual = target - current_observation
        residual_norm = float(np.linalg.norm(residual))
        if residual_norm <= residual_tol:
            return ORCHORBITALEstimate(
                current_kicks,
                residual_norm,
                iteration,
                True,
                last_rank,
                unknown_dimension,
                regime0,
            )
        if iteration == max_iterations:
            break

        delta_flat, *_ = np.linalg.lstsq(jacobian, residual, rcond=None)
        if not np.all(np.isfinite(delta_flat)):
            raise ORCHORBITALEstimationError(
                "Gauss-Newton update became non-finite"
            )
        delta = delta_flat.reshape(kick_matrix.shape)

        accepted = False
        alpha = 1.0
        for _ in range(line_search_halvings + 1):
            candidate = kick_matrix + alpha * delta
            try:
                candidate_observation, candidate_regime = _observation_and_regime(
                    initial_state,
                    attractors,
                    delta_taus,
                    _kick_tuple(candidate),
                    checkpoint_indices,
                    components,
                    include_weights=include_weights,
                )
            except ORCHORBITALEstimationError:
                candidate_observation = None
                candidate_regime = None
            if candidate_observation is not None and candidate_regime == regime0:
                candidate_norm = float(np.linalg.norm(target - candidate_observation))
                if candidate_norm < residual_norm:
                    kick_matrix = candidate
                    accepted = True
                    break
            alpha *= 0.5

        if not accepted:
            raise ORCHORBITALEstimationError(
                "same-regime line search found no descending update"
            )

    final_kicks = _kick_tuple(kick_matrix)
    final_observation, final_regime = _observation_and_regime(
        initial_state,
        attractors,
        delta_taus,
        final_kicks,
        checkpoint_indices,
        components,
        include_weights=include_weights,
    )
    final_residual = float(np.linalg.norm(target - final_observation))
    return ORCHORBITALEstimate(
        final_kicks,
        final_residual,
        max_iterations,
        final_residual <= residual_tol,
        last_rank,
        unknown_dimension,
        final_regime,
    )
