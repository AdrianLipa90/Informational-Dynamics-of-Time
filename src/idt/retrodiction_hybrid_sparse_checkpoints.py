from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec, evaluate_attractor_field


class HybridSparseRetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class HybridSparseCheckpointAudit:
    base_jacobian: np.ndarray
    hybrid_jacobian: np.ndarray
    base_rank: int
    hybrid_rank: int
    latent_dimension: int
    orientation_channels: int
    base_observation_dimension: int
    hybrid_observation_dimension: int
    status: str


def _kick_matrix(kicks: Sequence[complex]) -> np.ndarray:
    if len(kicks) < 2:
        raise HybridSparseRetrodictionError("at least two latent kicks are required")
    out = np.empty((len(kicks), 2), dtype=float)
    for i, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise HybridSparseRetrodictionError("kicks must be finite")
        out[i] = (z.real, z.imag)
    return out


def _validated_attractors(attractors: Sequence[AttractorSpec]) -> tuple[tuple[AttractorSpec, ...], dict[str, AttractorSpec]]:
    if not attractors:
        raise HybridSparseRetrodictionError("attractors must be non-empty")
    specs: list[AttractorSpec] = []
    mapping: dict[str, AttractorSpec] = {}
    for raw in attractors:
        name = str(raw.name).strip()
        center = np.asarray(raw.center, dtype=float)
        mu = float(raw.mu_memory)
        if not name or name in mapping:
            raise HybridSparseRetrodictionError("attractor names must be non-empty and unique")
        if center.shape != (2,) or not np.all(np.isfinite(center)):
            raise HybridSparseRetrodictionError("attractor centers must be finite two-component vectors")
        if not math.isfinite(mu) or mu <= 0.0:
            raise HybridSparseRetrodictionError("attractor mu_memory must be finite and strictly positive")
        spec = AttractorSpec(name, center.copy(), mu)
        specs.append(spec)
        mapping[name] = spec
    return tuple(specs), mapping


def _forward(initial_state: MemoryPhaseState, specs: Sequence[AttractorSpec], delta_taus: Sequence[float], kick_matrix: np.ndarray):
    dts = tuple(float(x) for x in delta_taus)
    if len(dts) != len(kick_matrix) or any((not math.isfinite(x) or x <= 0.0) for x in dts):
        raise HybridSparseRetrodictionError("delta_taus must be positive finite and match kicks")
    receipts = [
        MemoryEventReceipt(dt, 1.0, complex(float(kick[0]), float(kick[1])))
        for dt, kick in zip(dts, kick_matrix)
    ]
    try:
        return replay_memory_orchorbital_lineage(initial_state, specs, receipts)
    except ValueError as exc:
        raise HybridSparseRetrodictionError(str(exc)) from exc


def _observation(initial_state: MemoryPhaseState, attractors: Sequence[AttractorSpec], delta_taus: Sequence[float], kick_matrix: np.ndarray, *, include_orientation: bool, basin_weight_index: int):
    specs, mapping = _validated_attractors(attractors)
    states, cells = _forward(initial_state, specs, delta_taus, kick_matrix)
    n = len(kick_matrix)
    index = int(basin_weight_index)
    if index < 0 or index >= len(specs):
        raise HybridSparseRetrodictionError("basin_weight_index is outside the attractor list")

    fields = []
    for state in states[1:]:
        field = evaluate_attractor_field(state, specs)
        if field.leak_mode:
            raise HybridSparseRetrodictionError("checkpoint entered LEAK_MODE")
        fields.append(field)

    final = states[-1]
    values = [float(final.position[0]), float(final.position[1]), float(final.velocity[0])]
    values.extend(float(ev.weight) for ev in fields[-1].evaluations)
    values.extend(float(fields[i].evaluations[index].weight) for i in range(n - 1))

    orientation_count = max(0, n - 3) if include_orientation else 0
    for i in range(orientation_count):
        active = mapping[cells[i].active_attractor]
        rel = np.asarray(states[i + 1].position, dtype=float) - np.asarray(active.center, dtype=float)
        vel = np.asarray(states[i + 1].velocity, dtype=float)
        values.append(float(rel[0] * vel[1] - rel[1] * vel[0]))

    regime = (
        tuple(cell.active_attractor for cell in cells),
        tuple(
            (field.active_attractor, tuple(ev.weight > 0.0 for ev in field.evaluations))
            for field in fields
        ),
    )
    observation = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(observation)):
        raise HybridSparseRetrodictionError("observation became non-finite")
    return observation, regime, orientation_count


def hybrid_sparse_sensitivity_matrix(initial_state: MemoryPhaseState, attractors: Sequence[AttractorSpec], delta_taus: Sequence[float], nominal_kicks: Sequence[complex], *, include_orientation: bool = True, basin_weight_index: int = 0, finite_difference_step: float = 1e-7) -> np.ndarray:
    kicks = _kick_matrix(nominal_kicks)
    eps = float(finite_difference_step)
    if not math.isfinite(eps) or eps <= 0.0:
        raise HybridSparseRetrodictionError("finite_difference_step must be finite and strictly positive")
    y0, regime0, _ = _observation(
        initial_state, attractors, delta_taus, kicks,
        include_orientation=include_orientation,
        basin_weight_index=basin_weight_index,
    )
    jacobian = np.empty((y0.size, kicks.size), dtype=float)
    for column in range(kicks.size):
        plus = kicks.copy()
        minus = kicks.copy()
        plus.flat[column] += eps
        minus.flat[column] -= eps
        yp, regime_p, _ = _observation(
            initial_state, attractors, delta_taus, plus,
            include_orientation=include_orientation,
            basin_weight_index=basin_weight_index,
        )
        ym, regime_m, _ = _observation(
            initial_state, attractors, delta_taus, minus,
            include_orientation=include_orientation,
            basin_weight_index=basin_weight_index,
        )
        if regime_p != regime0 or regime_m != regime0:
            raise HybridSparseRetrodictionError("finite difference crossed an attractor/support boundary")
        jacobian[:, column] = (yp - ym) / (2.0 * eps)
    if not np.all(np.isfinite(jacobian)):
        raise HybridSparseRetrodictionError("sensitivity matrix became non-finite")
    return jacobian


def _rank(matrix: np.ndarray, relative_rank_tolerance: float) -> int:
    tol = float(relative_rank_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise HybridSparseRetrodictionError("relative_rank_tolerance must be finite and strictly positive")
    singular = np.linalg.svd(matrix, compute_uv=False)
    if singular.size == 0:
        return 0
    threshold = tol * max(1.0, float(singular[0]))
    return int(np.sum(singular > threshold))


def audit_hybrid_sparse_checkpoints(initial_state: MemoryPhaseState, attractors: Sequence[AttractorSpec], delta_taus: Sequence[float], nominal_kicks: Sequence[complex], *, basin_weight_index: int = 0, finite_difference_step: float = 1e-7, relative_rank_tolerance: float = 1e-7) -> HybridSparseCheckpointAudit:
    kicks = _kick_matrix(nominal_kicks)
    n = len(kicks)
    latent_dimension = 2 * n
    base = hybrid_sparse_sensitivity_matrix(
        initial_state, attractors, delta_taus, nominal_kicks,
        include_orientation=False,
        basin_weight_index=basin_weight_index,
        finite_difference_step=finite_difference_step,
    )
    hybrid = hybrid_sparse_sensitivity_matrix(
        initial_state, attractors, delta_taus, nominal_kicks,
        include_orientation=True,
        basin_weight_index=basin_weight_index,
        finite_difference_step=finite_difference_step,
    )
    base_rank = _rank(base, relative_rank_tolerance)
    hybrid_rank = _rank(hybrid, relative_rank_tolerance)
    added = max(0, n - 3)
    status = (
        "LOCAL_FULL_RANK_HYBRID_REFERENCE"
        if hybrid_rank == latent_dimension
        else "LOCAL_RANK_DEFICIENT_HYBRID_REFERENCE"
    )
    return HybridSparseCheckpointAudit(
        base,
        hybrid,
        base_rank,
        hybrid_rank,
        latent_dimension,
        added,
        int(base.shape[0]),
        int(hybrid.shape[0]),
        status,
    )
