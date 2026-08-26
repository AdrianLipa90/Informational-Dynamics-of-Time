from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .retrodiction_observability import RetrodictionObservabilityError, kick_sensitivity_matrix


class RetrodictionCheckpointSelectionError(ValueError):
    pass


@dataclass(frozen=True)
class CheckpointSubsetAudit:
    checkpoint_indices: tuple[int, ...]
    observation_dimension: int
    latent_dimension: int
    rank: int
    singular_values: np.ndarray
    condition_number: float
    full_column_rank: bool
    condition_admitted: bool
    status: str


@dataclass(frozen=True)
class CheckpointSelectionResult:
    selected: CheckpointSubsetAudit | None
    tested_subsets: int
    lower_bound_cardinality: int
    candidate_indices: tuple[int, ...]
    full_rank_subsets_at_selected_cardinality: int
    status: str


def checkpoint_cardinality_lower_bound(number_of_unknown_kicks: int) -> int:
    n = int(number_of_unknown_kicks)
    if isinstance(number_of_unknown_kicks, bool) or n != number_of_unknown_kicks or n <= 0:
        raise RetrodictionCheckpointSelectionError("number_of_unknown_kicks must be a positive integer")
    return int(math.ceil((2 * n) / 4.0))


def _candidate_indices(candidate_checkpoint_indices: Sequence[int], number_of_events: int) -> tuple[int, ...]:
    if not candidate_checkpoint_indices:
        raise RetrodictionCheckpointSelectionError("candidate_checkpoint_indices must be non-empty")
    values = tuple(int(i) for i in candidate_checkpoint_indices)
    if len(values) != len(set(values)):
        raise RetrodictionCheckpointSelectionError("candidate checkpoint indices must be unique")
    if any(i <= 0 or i > number_of_events for i in values):
        raise RetrodictionCheckpointSelectionError("candidate checkpoint indices must lie in [1, N]")
    return tuple(sorted(values))


def audit_checkpoint_subset(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    maximum_condition_number: float | None = None,
) -> CheckpointSubsetAudit:
    tol = float(relative_rank_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise RetrodictionCheckpointSelectionError("relative_rank_tolerance must be finite and strictly positive")
    if maximum_condition_number is not None:
        max_cond = float(maximum_condition_number)
        if not math.isfinite(max_cond) or max_cond <= 1.0:
            raise RetrodictionCheckpointSelectionError("maximum_condition_number must be finite and greater than one")
    else:
        max_cond = None

    try:
        jac = kick_sensitivity_matrix(
            initial_state,
            mu_memory,
            delta_taus,
            nominal_kicks,
            checkpoint_indices,
            finite_difference_step=finite_difference_step,
        )
    except RetrodictionObservabilityError as exc:
        raise RetrodictionCheckpointSelectionError(str(exc)) from exc

    singular = np.linalg.svd(jac, compute_uv=False)
    latent_dim = int(jac.shape[1])
    observation_dim = int(jac.shape[0])
    threshold = tol * max(1.0, float(singular[0]))
    rank = int(np.sum(singular > threshold))
    full_rank = rank == latent_dim
    if full_rank:
        condition = float(singular[0] / singular[latent_dim - 1])
    else:
        condition = math.inf

    condition_admitted = full_rank and (max_cond is None or condition <= max_cond)
    if observation_dim < latent_dim:
        status = "UNDERDETERMINED_DIMENSION"
    elif not full_rank:
        status = "RANK_DEFICIENT"
    elif max_cond is not None and condition > max_cond:
        status = "FULL_RANK_CONDITION_REJECTED"
    else:
        status = "ADMISSIBLE_CHECKPOINT_SUBSET"

    return CheckpointSubsetAudit(
        checkpoint_indices=tuple(int(i) for i in checkpoint_indices),
        observation_dimension=observation_dim,
        latent_dimension=latent_dim,
        rank=rank,
        singular_values=singular,
        condition_number=condition,
        full_column_rank=full_rank,
        condition_admitted=condition_admitted,
        status=status,
    )


def minimal_observable_checkpoint_set(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    candidate_checkpoint_indices: Sequence[int],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    maximum_condition_number: float | None = None,
    maximum_subsets: int = 10000,
) -> CheckpointSelectionResult:
    """Find the smallest retained checkpoint subset admitted by rank and optional conditioning.

    Cardinality is minimized first. Within the first admitted cardinality, the deterministic
    tie-break minimizes condition number and then uses lexicographic checkpoint order.
    """
    n = len(nominal_kicks)
    if n <= 0:
        raise RetrodictionCheckpointSelectionError("nominal_kicks must be non-empty")
    dts = list(delta_taus)
    if len(dts) != n:
        raise RetrodictionCheckpointSelectionError("delta_taus and nominal_kicks must have one common length")
    candidates = _candidate_indices(candidate_checkpoint_indices, n)
    limit = int(maximum_subsets)
    if isinstance(maximum_subsets, bool) or limit != maximum_subsets or limit <= 0:
        raise RetrodictionCheckpointSelectionError("maximum_subsets must be a positive integer")

    lower = checkpoint_cardinality_lower_bound(n)
    tested = 0
    for cardinality in range(lower, len(candidates) + 1):
        admitted: list[CheckpointSubsetAudit] = []
        full_rank_count = 0
        for subset in itertools.combinations(candidates, cardinality):
            tested += 1
            if tested > limit:
                raise RetrodictionCheckpointSelectionError("checkpoint subset search exceeded maximum_subsets")
            audit = audit_checkpoint_subset(
                initial_state,
                mu_memory,
                dts,
                nominal_kicks,
                subset,
                finite_difference_step=finite_difference_step,
                relative_rank_tolerance=relative_rank_tolerance,
                maximum_condition_number=maximum_condition_number,
            )
            if audit.full_column_rank:
                full_rank_count += 1
            if audit.condition_admitted:
                admitted.append(audit)
        if admitted:
            admitted.sort(key=lambda item: (item.condition_number, item.checkpoint_indices))
            return CheckpointSelectionResult(
                selected=admitted[0],
                tested_subsets=tested,
                lower_bound_cardinality=lower,
                candidate_indices=candidates,
                full_rank_subsets_at_selected_cardinality=full_rank_count,
                status="MINIMAL_ADMISSIBLE_CHECKPOINT_SET",
            )

    return CheckpointSelectionResult(
        selected=None,
        tested_subsets=tested,
        lower_bound_cardinality=lower,
        candidate_indices=candidates,
        full_rank_subsets_at_selected_cardinality=0,
        status="NO_ADMISSIBLE_CHECKPOINT_SET",
    )
