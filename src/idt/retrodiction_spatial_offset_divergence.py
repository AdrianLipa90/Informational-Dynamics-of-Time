from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class SpatialOffsetDivergenceError(ValueError):
    pass


@dataclass(frozen=True)
class SpatialOffsetDivergenceAudit:
    observation_distance: float
    latent_distance: float
    offsets: np.ndarray
    sod_l2: float
    sod_max_checkpoint: float
    first_divergent_checkpoint: int | None
    separating_components: tuple[str, ...]
    status: str


def _finite_vector(value, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size == 0 or not np.all(np.isfinite(arr)):
        raise SpatialOffsetDivergenceError(f"{name} must be a non-empty finite vector")
    return arr


def _finite_positions(value, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.ndim != 2 or arr.shape[0] == 0 or arr.shape[1] != 2:
        raise SpatialOffsetDivergenceError(f"{name} must have shape (N,2) with N>=1")
    if not np.all(np.isfinite(arr)):
        raise SpatialOffsetDivergenceError(f"{name} must be finite")
    return arr


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise SpatialOffsetDivergenceError(f"{name} must be finite and strictly positive")
    return x


def spatial_offset_lineage(reference_positions, candidate_positions) -> np.ndarray:
    reference = _finite_positions(reference_positions, "reference_positions")
    candidate = _finite_positions(candidate_positions, "candidate_positions")
    if reference.shape != candidate.shape:
        raise SpatialOffsetDivergenceError("position lineages must have the same shape")
    return candidate - reference


def separating_spatial_components(offsets, *, spatial_tolerance: float = 1e-9) -> tuple[str, ...]:
    delta = np.asarray(offsets, dtype=float)
    if delta.ndim != 2 or delta.shape[0] == 0 or delta.shape[1] != 2 or not np.all(np.isfinite(delta)):
        raise SpatialOffsetDivergenceError("offsets must be a finite (N,2) matrix")
    tol = _positive(spatial_tolerance, "spatial_tolerance")
    labels: list[str] = []
    axes = ("x", "y")
    for i, row in enumerate(delta, start=1):
        for axis, value in zip(axes, row):
            if abs(float(value)) > tol:
                labels.append(f"r{i}{axis}")
    return tuple(labels)


def audit_sparse_preimage_pair(
    reference_record,
    candidate_record,
    reference_positions,
    candidate_positions,
    reference_latent,
    candidate_latent,
    *,
    observation_tolerance: float = 1e-10,
    latent_tolerance: float = 1e-8,
    spatial_tolerance: float = 1e-9,
) -> SpatialOffsetDivergenceAudit:
    """Classify a pair of retrodiction preimages against one sparse record.

    Spatial Offset Divergence (SOD) is present when two distinct latent
    preimages agree within the declared sparse-observation tolerance while
    their Memory/ORCHORBITAL position lineages differ above the spatial
    tolerance at one or more checkpoints.
    """
    y0 = _finite_vector(reference_record, "reference_record")
    y1 = _finite_vector(candidate_record, "candidate_record")
    if y0.shape != y1.shape:
        raise SpatialOffsetDivergenceError("observation records must have the same shape")
    z0 = _finite_vector(reference_latent, "reference_latent")
    z1 = _finite_vector(candidate_latent, "candidate_latent")
    if z0.shape != z1.shape:
        raise SpatialOffsetDivergenceError("latent vectors must have the same shape")
    obs_tol = _positive(observation_tolerance, "observation_tolerance")
    latent_tol = _positive(latent_tolerance, "latent_tolerance")
    spatial_tol = _positive(spatial_tolerance, "spatial_tolerance")

    offsets = spatial_offset_lineage(reference_positions, candidate_positions)
    observation_distance = float(np.linalg.norm(y1 - y0))
    latent_distance = float(np.linalg.norm(z1 - z0))
    checkpoint_norms = np.linalg.norm(offsets, axis=1)
    sod_l2 = float(np.linalg.norm(offsets))
    sod_max = float(np.max(checkpoint_norms))
    divergent = np.flatnonzero(checkpoint_norms > spatial_tol)
    first = int(divergent[0] + 1) if divergent.size else None
    separators = separating_spatial_components(offsets, spatial_tolerance=spatial_tol)

    if observation_distance > obs_tol:
        status = "OBSERVATION_DISTINGUISHABLE"
    elif latent_distance <= latent_tol:
        status = "SAME_LATENT_PREIMAGE"
    elif sod_l2 > spatial_tol:
        status = "SPATIAL_OFFSET_DIVERGENCE"
    else:
        status = "NONSPATIAL_GLOBAL_NULL"

    return SpatialOffsetDivergenceAudit(
        observation_distance=observation_distance,
        latent_distance=latent_distance,
        offsets=offsets,
        sod_l2=sod_l2,
        sod_max_checkpoint=sod_max,
        first_divergent_checkpoint=first,
        separating_components=separators,
        status=status,
    )
