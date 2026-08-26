from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .retrodiction_observability import (
    RetrodictionObservabilityError,
    checkpoint_phase_vector,
    forward_kick_lineage,
    kick_sensitivity_matrix,
)


class RetrodictionWeightedError(ValueError):
    pass


@dataclass(frozen=True)
class WeightedRetrodictionEstimate:
    kicks: tuple[complex, ...]
    predicted_observation: np.ndarray
    residual: np.ndarray
    weighted_residual_quadratic: float
    iterations: int
    status: str
    weighted_rank: int
    latent_dimension: int
    condition_number: float


@dataclass(frozen=True)
class PermutationNullEntry:
    permutation: tuple[int, ...]
    weighted_residual_quadratic: float
    iterations: int
    status: str


@dataclass(frozen=True)
class PermutationNullEnsemble:
    observed_weighted_residual_quadratic: float
    entries: tuple[PermutationNullEntry, ...]
    null_minimum: float
    null_median: float
    null_maximum: float
    null_margin: float
    null_better_or_equal_count: int
    null_rank_fraction: float
    status: str


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool):
        raise RetrodictionWeightedError(f"{name} must be a positive integer")
    n = int(value)
    if n != value or n <= 0:
        raise RetrodictionWeightedError(f"{name} must be a positive integer")
    return n


def _positive_float(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise RetrodictionWeightedError(f"{name} must be finite and strictly positive")
    return x


def _nonnegative_float(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x < 0.0:
        raise RetrodictionWeightedError(f"{name} must be finite and non-negative")
    return x


def _kick_vector(kicks: Sequence[complex]) -> np.ndarray:
    if not kicks:
        raise RetrodictionWeightedError("kicks must be non-empty")
    out = np.empty(2 * len(kicks), dtype=float)
    for index, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise RetrodictionWeightedError("kicks must be finite")
        out[2 * index:2 * index + 2] = (z.real, z.imag)
    return out


def _vector_kicks(vector: Sequence[float]) -> tuple[complex, ...]:
    arr = np.asarray(vector, dtype=float)
    if arr.ndim != 1 or arr.size == 0 or arr.size % 2:
        raise RetrodictionWeightedError("latent kick vector must have positive even length")
    if not np.all(np.isfinite(arr)):
        raise RetrodictionWeightedError("latent kick vector must be finite")
    return tuple(complex(float(arr[i]), float(arr[i + 1])) for i in range(0, arr.size, 2))


def _validated_covariance(covariance: Sequence[Sequence[float]], dimension: int) -> tuple[np.ndarray, np.ndarray]:
    cov = np.asarray(covariance, dtype=float)
    if cov.shape != (dimension, dimension):
        raise RetrodictionWeightedError("observation covariance has incompatible shape")
    if not np.all(np.isfinite(cov)):
        raise RetrodictionWeightedError("observation covariance must be finite")
    scale = max(1.0, float(np.max(np.abs(cov))))
    if not np.allclose(cov, cov.T, rtol=0.0, atol=1e-12 * scale):
        raise RetrodictionWeightedError("observation covariance must be symmetric")
    try:
        chol = np.linalg.cholesky(cov)
    except np.linalg.LinAlgError as exc:
        raise RetrodictionWeightedError("observation covariance must be positive definite") from exc
    return cov, chol


def _observation(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
) -> np.ndarray:
    try:
        states = forward_kick_lineage(initial_state, mu_memory, delta_taus, kicks)
        return checkpoint_phase_vector(states, checkpoint_indices)
    except RetrodictionObservabilityError as exc:
        raise RetrodictionWeightedError(str(exc)) from exc


def estimate_latent_kicks_weighted(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    observed_checkpoint_vector: Sequence[float],
    checkpoint_indices: Sequence[int],
    number_of_unknown_kicks: int,
    observation_covariance: Sequence[Sequence[float]],
    *,
    initial_kicks: Sequence[complex] | None = None,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    damping: float = 1e-8,
    weighted_residual_tolerance: float = 1e-8,
    step_tolerance: float = 1e-12,
    maximum_iterations: int = 32,
    maximum_line_search_halvings: int = 12,
) -> WeightedRetrodictionEstimate:
    """Covariance-weighted latent-kick estimator with rank admission and strict descent."""
    n = _positive_int(number_of_unknown_kicks, "number_of_unknown_kicks")
    max_iterations = _positive_int(maximum_iterations, "maximum_iterations")
    max_halvings = _positive_int(maximum_line_search_halvings, "maximum_line_search_halvings")
    eps = _positive_float(finite_difference_step, "finite_difference_step")
    rank_tol = _positive_float(relative_rank_tolerance, "relative_rank_tolerance")
    lam = _nonnegative_float(damping, "damping")
    q_tol = _nonnegative_float(weighted_residual_tolerance, "weighted_residual_tolerance")
    dz_tol = _nonnegative_float(step_tolerance, "step_tolerance")

    observed = np.asarray(observed_checkpoint_vector, dtype=float)
    if observed.ndim != 1 or observed.size == 0 or not np.all(np.isfinite(observed)):
        raise RetrodictionWeightedError("observed_checkpoint_vector must be a non-empty finite vector")
    _, chol = _validated_covariance(observation_covariance, observed.size)

    if initial_kicks is None:
        kicks = tuple(0.0j for _ in range(n))
    else:
        if len(initial_kicks) != n:
            raise RetrodictionWeightedError("initial_kicks length must equal number_of_unknown_kicks")
        kicks = _vector_kicks(_kick_vector(initial_kicks))

    x = _kick_vector(kicks)
    predicted = _observation(initial_state, mu_memory, delta_taus, kicks, checkpoint_indices)
    if predicted.shape != observed.shape:
        raise RetrodictionWeightedError("observed checkpoint vector has incompatible dimension")

    def weighted_geometry(kick_tuple: Sequence[complex]) -> tuple[np.ndarray, np.ndarray, int, float]:
        try:
            jac = kick_sensitivity_matrix(
                initial_state,
                mu_memory,
                delta_taus,
                kick_tuple,
                checkpoint_indices,
                finite_difference_step=eps,
            )
        except RetrodictionObservabilityError as exc:
            raise RetrodictionWeightedError(str(exc)) from exc
        jw = np.linalg.solve(chol, jac)
        singular = np.linalg.svd(jw, compute_uv=False)
        threshold = rank_tol * max(1.0, float(singular[0]))
        rank = int(np.sum(singular > threshold))
        latent_dimension = int(jac.shape[1])
        condition = float(singular[0] / singular[latent_dimension - 1]) if rank == latent_dimension else math.inf
        return jac, jw, rank, condition

    _, jw0, rank0, condition0 = weighted_geometry(kicks)
    if jw0.shape[1] != 2 * n:
        raise RetrodictionWeightedError("weighted sensitivity latent dimension does not match requested kick count")
    if rank0 < 2 * n:
        raise RetrodictionWeightedError("weighted observability gate rejected estimation")

    residual = observed - predicted
    whitened_residual = np.linalg.solve(chol, residual)
    q = float(whitened_residual @ whitened_residual)
    status = "MAX_ITERATIONS"
    iterations = 0
    current_rank = rank0
    current_condition = condition0

    if q <= q_tol:
        status = "CONVERGED_WEIGHTED_RESIDUAL"
    else:
        for iteration in range(1, max_iterations + 1):
            iterations = iteration
            kicks = _vector_kicks(x)
            _, jw, current_rank, current_condition = weighted_geometry(kicks)
            if current_rank < x.size:
                raise RetrodictionWeightedError("weighted sensitivity lost full column rank during estimation")

            whitened_residual = np.linalg.solve(chol, residual)
            normal = jw.T @ jw + lam * np.eye(x.size)
            rhs = jw.T @ whitened_residual
            try:
                delta = np.linalg.solve(normal, rhs)
            except np.linalg.LinAlgError as exc:
                raise RetrodictionWeightedError("weighted damped normal equations are singular") from exc

            if float(np.linalg.norm(delta)) <= dz_tol:
                status = "CONVERGED_STEP"
                break

            accepted = False
            for half in range(max_halvings):
                alpha = 0.5 ** half
                trial_x = x + alpha * delta
                trial_kicks = _vector_kicks(trial_x)
                trial_prediction = _observation(
                    initial_state,
                    mu_memory,
                    delta_taus,
                    trial_kicks,
                    checkpoint_indices,
                )
                trial_residual = observed - trial_prediction
                trial_whitened = np.linalg.solve(chol, trial_residual)
                trial_q = float(trial_whitened @ trial_whitened)
                if trial_q < q:
                    x = trial_x
                    predicted = trial_prediction
                    residual = trial_residual
                    q = trial_q
                    accepted = True
                    break

            if not accepted:
                status = "STALLED_NO_WEIGHTED_DESCENT"
                break
            if q <= q_tol:
                status = "CONVERGED_WEIGHTED_RESIDUAL"
                break

    final_kicks = _vector_kicks(x)
    _, _, current_rank, current_condition = weighted_geometry(final_kicks)
    return WeightedRetrodictionEstimate(
        kicks=final_kicks,
        predicted_observation=np.asarray(predicted, dtype=float),
        residual=np.asarray(residual, dtype=float),
        weighted_residual_quadratic=float(q),
        iterations=iterations,
        status=status,
        weighted_rank=current_rank,
        latent_dimension=2 * n,
        condition_number=current_condition,
    )


def _block_permutation_matrix(number_of_blocks: int, permutation: Sequence[int], block_size: int = 4) -> np.ndarray:
    perm = tuple(int(i) for i in permutation)
    if sorted(perm) != list(range(number_of_blocks)):
        raise RetrodictionWeightedError("permutation must contain each checkpoint block exactly once")
    matrix = np.zeros((number_of_blocks * block_size, number_of_blocks * block_size), dtype=float)
    eye = np.eye(block_size, dtype=float)
    for target, source in enumerate(perm):
        matrix[target * block_size:(target + 1) * block_size, source * block_size:(source + 1) * block_size] = eye
    return matrix


def checkpoint_permutation_null_ensemble(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    observed_checkpoint_vector: Sequence[float],
    checkpoint_indices: Sequence[int],
    number_of_unknown_kicks: int,
    observation_covariance: Sequence[Sequence[float]],
    *,
    include_identity: bool = False,
    maximum_permutations: int = 720,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    damping: float = 1e-8,
) -> PermutationNullEnsemble:
    """Fit the same weighted model to a deterministic checkpoint-order permutation ensemble.

    Observation blocks and their covariance blocks are permuted together. The returned
    null_rank_fraction is a finite reference-ensemble diagnostic, not a p-value.
    """
    observed = np.asarray(observed_checkpoint_vector, dtype=float)
    if observed.ndim != 1 or observed.size == 0 or observed.size % 4:
        raise RetrodictionWeightedError("observed checkpoint vector must contain complete 4D checkpoint blocks")
    n_blocks = observed.size // 4
    if n_blocks < 2:
        raise RetrodictionWeightedError("permutation ensemble requires at least two retained checkpoints")
    if len(checkpoint_indices) != n_blocks:
        raise RetrodictionWeightedError("checkpoint_indices length must equal observation block count")
    cov, _ = _validated_covariance(observation_covariance, observed.size)
    limit = _positive_int(maximum_permutations, "maximum_permutations")

    observed_fit = estimate_latent_kicks_weighted(
        initial_state,
        mu_memory,
        delta_taus,
        observed,
        checkpoint_indices,
        number_of_unknown_kicks,
        cov,
        finite_difference_step=finite_difference_step,
        relative_rank_tolerance=relative_rank_tolerance,
        damping=damping,
    )

    identity = tuple(range(n_blocks))
    permutations = list(itertools.permutations(range(n_blocks)))
    if not include_identity:
        permutations = [p for p in permutations if p != identity]
    if len(permutations) > limit:
        raise RetrodictionWeightedError("checkpoint permutation ensemble exceeds maximum_permutations")
    if not permutations:
        raise RetrodictionWeightedError("checkpoint permutation ensemble is empty")

    entries: list[PermutationNullEntry] = []
    for permutation in permutations:
        pmat = _block_permutation_matrix(n_blocks, permutation)
        permuted_observed = pmat @ observed
        permuted_covariance = pmat @ cov @ pmat.T
        fit = estimate_latent_kicks_weighted(
            initial_state,
            mu_memory,
            delta_taus,
            permuted_observed,
            checkpoint_indices,
            number_of_unknown_kicks,
            permuted_covariance,
            finite_difference_step=finite_difference_step,
            relative_rank_tolerance=relative_rank_tolerance,
            damping=damping,
        )
        entries.append(
            PermutationNullEntry(
                permutation=tuple(permutation),
                weighted_residual_quadratic=float(fit.weighted_residual_quadratic),
                iterations=fit.iterations,
                status=fit.status,
            )
        )

    values = np.asarray([entry.weighted_residual_quadratic for entry in entries], dtype=float)
    observed_q = float(observed_fit.weighted_residual_quadratic)
    better_or_equal = int(np.sum(values <= observed_q))
    return PermutationNullEnsemble(
        observed_weighted_residual_quadratic=observed_q,
        entries=tuple(entries),
        null_minimum=float(np.min(values)),
        null_median=float(np.median(values)),
        null_maximum=float(np.max(values)),
        null_margin=float(np.min(values) - observed_q),
        null_better_or_equal_count=better_or_equal,
        null_rank_fraction=float(better_or_equal / len(entries)),
        status="PERMUTATION_REFERENCE_ENSEMBLE_COMPLETE",
    )
