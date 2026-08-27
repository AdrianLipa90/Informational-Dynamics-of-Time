from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class SparseCheckpointCompletionError(ValueError):
    pass


@dataclass(frozen=True)
class PositionLineageRankCertificate:
    event_count: int
    latent_dimension: int
    log_abs_block_diagonal_determinant: float
    status: str


@dataclass(frozen=True)
class SparseCheckpointCompletion:
    selected_row_indices: tuple[int, ...]
    selected_labels: tuple[str, ...]
    base_rank: int
    position_pool_rank: int
    completed_rank: int
    latent_dimension: int
    minimum_additional_scalars: int
    status: str


def _finite_matrix(value, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.ndim != 2 or arr.shape[1] <= 0:
        raise SparseCheckpointCompletionError(f"{name} must be a two-dimensional matrix with at least one column")
    if not np.all(np.isfinite(arr)):
        raise SparseCheckpointCompletionError(f"{name} must be finite")
    return arr


def _positive_tolerance(value: float) -> float:
    tol = float(value)
    if not math.isfinite(tol) or tol <= 0.0:
        raise SparseCheckpointCompletionError(
            "relative_rank_tolerance must be finite and strictly positive"
        )
    return tol


def numerical_rank(matrix, *, relative_rank_tolerance: float = 1e-9) -> int:
    arr = _finite_matrix(matrix, "matrix")
    tol = _positive_tolerance(relative_rank_tolerance)
    singular = np.linalg.svd(arr, compute_uv=False)
    if singular.size == 0:
        return 0
    threshold = tol * max(1.0, float(singular[0]))
    return int(np.sum(singular > threshold))


def position_lineage_rank_certificate(
    delta_taus: Sequence[float],
) -> PositionLineageRankCertificate:
    """Certify the 2N local rank of the ordered post-segment position map.

    Conditional on the retained active-attractor sequence, the k-th position
    checkpoint has local derivative dt_k I_2 with respect to the k-th kick.
    The complete sensitivity matrix is therefore block lower triangular with
    diagonal blocks dt_k I_2.
    """
    dts = tuple(float(value) for value in delta_taus)
    if not dts:
        raise SparseCheckpointCompletionError("delta_taus must be non-empty")
    if any((not math.isfinite(dt) or dt <= 0.0) for dt in dts):
        raise SparseCheckpointCompletionError(
            "delta_taus must be finite and strictly positive"
        )
    log_abs_det = 2.0 * sum(math.log(dt) for dt in dts)
    n = len(dts)
    return PositionLineageRankCertificate(
        event_count=n,
        latent_dimension=2 * n,
        log_abs_block_diagonal_determinant=log_abs_det,
        status="FULL_RANK_BY_BLOCK_LOWER_TRIANGULAR_DIAGONAL",
    )


def minimal_position_completion(
    base_jacobian,
    position_jacobian,
    *,
    position_labels: Sequence[str] | None = None,
    relative_rank_tolerance: float = 1e-9,
) -> SparseCheckpointCompletion:
    """Select a rank-minimal subset of position rows that closes a base schedule.

    Each selected scalar row is admitted only when it increases numerical rank
    by exactly one.  If the position pool spans the complete latent space, the
    selector therefore terminates after exactly latent_dimension-base_rank rows.
    """
    base = _finite_matrix(base_jacobian, "base_jacobian")
    pool = _finite_matrix(position_jacobian, "position_jacobian")
    tol = _positive_tolerance(relative_rank_tolerance)
    if base.shape[1] != pool.shape[1]:
        raise SparseCheckpointCompletionError(
            "base_jacobian and position_jacobian must have the same column count"
        )
    latent = int(base.shape[1])
    labels = (
        tuple(f"position_row_{i}" for i in range(pool.shape[0]))
        if position_labels is None
        else tuple(str(label) for label in position_labels)
    )
    if len(labels) != pool.shape[0] or any(not label for label in labels):
        raise SparseCheckpointCompletionError(
            "position_labels must provide one non-empty label per position row"
        )

    base_rank = numerical_rank(base, relative_rank_tolerance=tol)
    pool_rank = numerical_rank(pool, relative_rank_tolerance=tol)
    if pool_rank < latent:
        raise SparseCheckpointCompletionError(
            "position_jacobian must span the full latent dimension"
        )

    current = base.copy()
    current_rank = base_rank
    selected: list[int] = []
    for row_index, row in enumerate(pool):
        candidate = np.vstack((current, row.reshape(1, -1)))
        candidate_rank = numerical_rank(candidate, relative_rank_tolerance=tol)
        if candidate_rank > current_rank:
            if candidate_rank != current_rank + 1:
                raise SparseCheckpointCompletionError(
                    "a scalar position row produced an invalid rank increment"
                )
            selected.append(row_index)
            current = candidate
            current_rank = candidate_rank
            if current_rank == latent:
                break

    if current_rank != latent:
        raise SparseCheckpointCompletionError(
            "position pool failed to complete the base schedule at the declared tolerance"
        )
    deficit = latent - base_rank
    if len(selected) != deficit:
        raise SparseCheckpointCompletionError(
            "selected row count must equal the rank deficit"
        )
    status = (
        "BASE_ALREADY_FULL_RANK" if deficit == 0
        else "RANK_MINIMAL_POSITION_COMPLETION"
    )
    return SparseCheckpointCompletion(
        selected_row_indices=tuple(selected),
        selected_labels=tuple(labels[i] for i in selected),
        base_rank=base_rank,
        position_pool_rank=pool_rank,
        completed_rank=current_rank,
        latent_dimension=latent,
        minimum_additional_scalars=deficit,
        status=status,
    )
