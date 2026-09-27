from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class SpatialTemporalHolonomyError(ValueError):
    pass


@dataclass(frozen=True)
class SpatialOnlyTransportAudit:
    spatial_displacement: np.ndarray
    spatial_distance: float
    tau_before: float
    tau_after_transport: float
    transport_temporal_offset: float


@dataclass(frozen=True)
class TemporalHolonomyAudit:
    temporal_offset: float
    classification: str
    segment_count: int


def _finite_scalar(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise SpatialTemporalHolonomyError(f"{name} must be finite")
    return out


def _finite_vector(value: Sequence[float], name: str) -> np.ndarray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 1 or out.size == 0:
        raise SpatialTemporalHolonomyError(f"{name} must be a non-empty one-dimensional vector")
    if not np.all(np.isfinite(out)):
        raise SpatialTemporalHolonomyError(f"{name} must be finite")
    return out


def spatial_only_transport(
    x_start: Sequence[float],
    x_end: Sequence[float],
    tau: float,
) -> SpatialOnlyTransportAudit:
    """Candidate 09B transport: change spatial address while holding the foliation label fixed."""
    start = _finite_vector(x_start, "x_start")
    end = _finite_vector(x_end, "x_end")
    if start.shape != end.shape:
        raise SpatialTemporalHolonomyError("x_start and x_end must have the same shape")
    t = _finite_scalar(tau, "tau")
    dx = end - start
    return SpatialOnlyTransportAudit(
        spatial_displacement=dx.copy(),
        spatial_distance=float(np.linalg.norm(dx)),
        tau_before=t,
        tau_after_transport=t,
        transport_temporal_offset=0.0,
    )


def temporal_holonomy(
    segment_displacements: Sequence[Sequence[float]],
    temporal_connection_samples: Sequence[Sequence[float]],
) -> TemporalHolonomyAudit:
    """Discrete line integral Delta tau_H = sum_k A_tau,k . Delta x_k."""
    dx = np.asarray(segment_displacements, dtype=float)
    a = np.asarray(temporal_connection_samples, dtype=float)
    if dx.ndim != 2 or a.ndim != 2 or dx.shape != a.shape or dx.shape[0] == 0 or dx.shape[1] == 0:
        raise SpatialTemporalHolonomyError(
            "segment_displacements and temporal_connection_samples must be equal non-empty 2D arrays"
        )
    if not np.all(np.isfinite(dx)) or not np.all(np.isfinite(a)):
        raise SpatialTemporalHolonomyError("holonomy inputs must be finite")
    offset = float(np.sum(dx * a))
    tol = 1e-15 * max(1.0, abs(offset))
    if offset < -tol:
        classification = "NEGATIVE_TEMPORAL_OFFSET_MODEL_COORDINATE"
    elif offset > tol:
        classification = "POSITIVE_TEMPORAL_OFFSET_MODEL_COORDINATE"
    else:
        classification = "ZERO_TEMPORAL_OFFSET"
    return TemporalHolonomyAudit(offset, classification, int(dx.shape[0]))


def round_trip_temporal_offset(
    forward_displacements: Sequence[Sequence[float]],
    forward_connection_samples: Sequence[Sequence[float]],
    return_displacements: Sequence[Sequence[float]],
    return_connection_samples: Sequence[Sequence[float]],
) -> TemporalHolonomyAudit:
    forward = temporal_holonomy(forward_displacements, forward_connection_samples)
    backward = temporal_holonomy(return_displacements, return_connection_samples)
    offset = forward.temporal_offset + backward.temporal_offset
    tol = 1e-15 * max(1.0, abs(offset))
    if offset < -tol:
        classification = "NEGATIVE_TEMPORAL_OFFSET_MODEL_COORDINATE"
    elif offset > tol:
        classification = "POSITIVE_TEMPORAL_OFFSET_MODEL_COORDINATE"
    else:
        classification = "ZERO_TEMPORAL_OFFSET"
    return TemporalHolonomyAudit(
        temporal_offset=offset,
        classification=classification,
        segment_count=forward.segment_count + backward.segment_count,
    )


def exact_temporal_potential_offset(potential_start: float, potential_end: float) -> float:
    """If A_tau=dT on one chart, the path integral depends only on endpoint potential."""
    t0 = _finite_scalar(potential_start, "potential_start")
    t1 = _finite_scalar(potential_end, "potential_end")
    return t1 - t0
