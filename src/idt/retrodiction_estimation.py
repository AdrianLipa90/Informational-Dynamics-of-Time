from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .retrodiction_observability import (
    RetrodictionObservabilityAudit,
    RetrodictionObservabilityError,
    audit_kick_observability,
    checkpoint_phase_vector,
    forward_kick_lineage,
    kick_sensitivity_matrix,
)


class RetrodictionEstimationError(ValueError):
    pass


@dataclass(frozen=True)
class RetrodictionEstimate:
    kicks: tuple[complex, ...]
    predicted_observation: np.ndarray
    residual: np.ndarray
    residual_norm: float
    iterations: int
    status: str
    observability: RetrodictionObservabilityAudit


@dataclass(frozen=True)
class RetrodictionNullComparison:
    estimator_residual: float
    zero_kick_residual: float
    checkpoint_shuffle_residual: float
    zero_kick_reduction: float
    checkpoint_shuffle_reduction: float
    checkpoint_permutation: tuple[int, ...]


@dataclass(frozen=True)
class RetrodictionTruthScore:
    estimate_commitment: str
    max_abs_kick_error: float
    kick_rmse: float


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool):
        raise RetrodictionEstimationError(f"{name} must be a positive integer")
    n = int(value)
    if n != value or n <= 0:
        raise RetrodictionEstimationError(f"{name} must be a positive integer")
    return n


def _finite_nonnegative(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x < 0.0:
        raise RetrodictionEstimationError(f"{name} must be finite and non-negative")
    return x


def _finite_positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise RetrodictionEstimationError(f"{name} must be finite and strictly positive")
    return x


def _kick_vector(kicks: Sequence[complex]) -> np.ndarray:
    if not kicks:
        raise RetrodictionEstimationError("kicks must be non-empty")
    out = np.empty(2 * len(kicks), dtype=float)
    for idx, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise RetrodictionEstimationError("kicks must be finite")
        out[2 * idx] = z.real
        out[2 * idx + 1] = z.imag
    return out


def _vector_kicks(vector: Sequence[float]) -> tuple[complex, ...]:
    arr = np.asarray(vector, dtype=float)
    if arr.ndim != 1 or arr.size == 0 or arr.size % 2:
        raise RetrodictionEstimationError("latent kick vector must have positive even length")
    if not np.all(np.isfinite(arr)):
        raise RetrodictionEstimationError("latent kick vector must be finite")
    return tuple(complex(float(arr[i]), float(arr[i + 1])) for i in range(0, arr.size, 2))


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
        raise RetrodictionEstimationError(str(exc)) from exc


def estimate_latent_kicks(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    observed_checkpoint_vector: Sequence[float],
    checkpoint_indices: Sequence[int],
    number_of_unknown_kicks: int,
    *,
    initial_kicks: Sequence[complex] | None = None,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    damping: float = 1e-8,
    residual_tolerance: float = 1e-10,
    step_tolerance: float = 1e-12,
    maximum_iterations: int = 32,
    maximum_line_search_halvings: int = 10,
) -> RetrodictionEstimate:
    """Estimate latent direct event kicks only after passing the local observability gate.

    The estimator consumes only declared public model inputs and the retained checkpoint
    vector. Hidden truth values are intentionally absent from this API.
    """
    n = _positive_int(number_of_unknown_kicks, "number_of_unknown_kicks")
    max_iter = _positive_int(maximum_iterations, "maximum_iterations")
    max_halvings = _positive_int(maximum_line_search_halvings, "maximum_line_search_halvings")
    eps = _finite_positive(finite_difference_step, "finite_difference_step")
    rank_tol = _finite_positive(relative_rank_tolerance, "relative_rank_tolerance")
    lam = _finite_nonnegative(damping, "damping")
    residual_tol = _finite_nonnegative(residual_tolerance, "residual_tolerance")
    step_tol = _finite_nonnegative(step_tolerance, "step_tolerance")

    observed = np.asarray(observed_checkpoint_vector, dtype=float)
    if observed.ndim != 1 or observed.size == 0 or not np.all(np.isfinite(observed)):
        raise RetrodictionEstimationError("observed_checkpoint_vector must be a non-empty finite vector")

    if initial_kicks is None:
        current_kicks = tuple(0.0j for _ in range(n))
    else:
        if len(initial_kicks) != n:
            raise RetrodictionEstimationError("initial_kicks length must equal number_of_unknown_kicks")
        current_kicks = _vector_kicks(_kick_vector(initial_kicks))

    try:
        gate = audit_kick_observability(
            initial_state,
            mu_memory,
            delta_taus,
            current_kicks,
            checkpoint_indices,
            finite_difference_step=eps,
            relative_rank_tolerance=rank_tol,
        )
    except RetrodictionObservabilityError as exc:
        raise RetrodictionEstimationError(str(exc)) from exc

    if gate.unknown_dimension != 2 * n:
        raise RetrodictionEstimationError("observability gate dimension does not match requested latent kick count")
    if not gate.locally_identifiable:
        raise RetrodictionEstimationError(f"observability gate rejected estimation: {gate.status}")

    predicted = _observation(initial_state, mu_memory, delta_taus, current_kicks, checkpoint_indices)
    if predicted.shape != observed.shape:
        raise RetrodictionEstimationError("observed checkpoint vector has incompatible dimension")

    x = _kick_vector(current_kicks)
    residual = observed - predicted
    residual_norm = float(np.linalg.norm(residual))
    status = "MAX_ITERATIONS"
    iterations = 0

    if residual_norm <= residual_tol:
        status = "CONVERGED_RESIDUAL"
    else:
        for iteration in range(1, max_iter + 1):
            iterations = iteration
            current_kicks = _vector_kicks(x)
            try:
                jac = kick_sensitivity_matrix(
                    initial_state,
                    mu_memory,
                    delta_taus,
                    current_kicks,
                    checkpoint_indices,
                    finite_difference_step=eps,
                )
            except RetrodictionObservabilityError as exc:
                raise RetrodictionEstimationError(str(exc)) from exc

            singular = np.linalg.svd(jac, compute_uv=False)
            threshold = rank_tol * max(1.0, float(singular[0]))
            local_rank = int(np.sum(singular > threshold))
            if local_rank < x.size:
                raise RetrodictionEstimationError("local sensitivity matrix lost full column rank during estimation")

            normal = jac.T @ jac + lam * np.eye(x.size)
            rhs = jac.T @ residual
            try:
                delta = np.linalg.solve(normal, rhs)
            except np.linalg.LinAlgError as exc:
                raise RetrodictionEstimationError("damped normal equations are singular") from exc

            if float(np.linalg.norm(delta)) <= step_tol:
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
                trial_norm = float(np.linalg.norm(trial_residual))
                if trial_norm < residual_norm:
                    x = trial_x
                    predicted = trial_prediction
                    residual = trial_residual
                    residual_norm = trial_norm
                    accepted = True
                    break

            if not accepted:
                status = "STALLED_NO_DESCENT"
                break
            if residual_norm <= residual_tol:
                status = "CONVERGED_RESIDUAL"
                break

    return RetrodictionEstimate(
        kicks=_vector_kicks(x),
        predicted_observation=np.asarray(predicted, dtype=float),
        residual=np.asarray(residual, dtype=float),
        residual_norm=float(residual_norm),
        iterations=iterations,
        status=status,
        observability=gate,
    )


def estimate_commitment(estimate: RetrodictionEstimate) -> str:
    """Content commitment frozen before hidden truth is released to the scorer."""
    kick_bytes = np.asarray(_kick_vector(estimate.kicks), dtype="<f8").tobytes()
    observation_bytes = np.asarray(estimate.predicted_observation, dtype="<f8").tobytes()
    residual_bytes = np.asarray(estimate.residual, dtype="<f8").tobytes()
    metadata = f"{estimate.status}|{estimate.iterations}|{estimate.residual_norm:.17g}".encode("utf-8")
    return hashlib.sha256(kick_bytes + observation_bytes + residual_bytes + metadata).hexdigest()


def score_committed_estimate(
    estimate: RetrodictionEstimate,
    sealed_truth_kicks: Sequence[complex],
    expected_commitment: str,
) -> RetrodictionTruthScore:
    """Score against sealed truth only after verifying the pre-truth estimate commitment."""
    actual_commitment = estimate_commitment(estimate)
    if actual_commitment != str(expected_commitment):
        raise RetrodictionEstimationError("estimate commitment mismatch")
    truth = _kick_vector(sealed_truth_kicks)
    inferred = _kick_vector(estimate.kicks)
    if truth.shape != inferred.shape:
        raise RetrodictionEstimationError("sealed truth dimension does not match estimate")
    error = inferred - truth
    return RetrodictionTruthScore(
        estimate_commitment=actual_commitment,
        max_abs_kick_error=float(np.max(np.abs(error))),
        kick_rmse=float(math.sqrt(float(np.mean(error * error)))),
    )


def _checkpoint_block_permute(observation: np.ndarray, permutation: Sequence[int]) -> np.ndarray:
    arr = np.asarray(observation, dtype=float)
    if arr.ndim != 1 or arr.size == 0 or arr.size % 4:
        raise RetrodictionEstimationError("checkpoint observation must contain complete four-component phase-state blocks")
    n_blocks = arr.size // 4
    perm = tuple(int(i) for i in permutation)
    if sorted(perm) != list(range(n_blocks)):
        raise RetrodictionEstimationError("checkpoint permutation must contain each checkpoint block exactly once")
    return np.concatenate([arr[4 * i:4 * (i + 1)] for i in perm])


def compare_with_reference_nulls(
    estimate: RetrodictionEstimate,
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    observed_checkpoint_vector: Sequence[float],
    checkpoint_indices: Sequence[int],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
) -> RetrodictionNullComparison:
    """Compare the committed estimator residual against capacity-matched reference nulls."""
    observed = np.asarray(observed_checkpoint_vector, dtype=float)
    n = len(estimate.kicks)
    zero_prediction = _observation(
        initial_state,
        mu_memory,
        delta_taus,
        tuple(0.0j for _ in range(n)),
        checkpoint_indices,
    )
    zero_residual = float(np.linalg.norm(observed - zero_prediction))

    n_blocks = observed.size // 4
    if n_blocks < 2:
        raise RetrodictionEstimationError("checkpoint-shuffle null requires at least two retained checkpoints")
    permutation = tuple(reversed(range(n_blocks)))
    shuffled = _checkpoint_block_permute(observed, permutation)
    shuffled_estimate = estimate_latent_kicks(
        initial_state,
        mu_memory,
        delta_taus,
        shuffled,
        checkpoint_indices,
        n,
        finite_difference_step=finite_difference_step,
        relative_rank_tolerance=relative_rank_tolerance,
    )
    shuffle_residual = float(shuffled_estimate.residual_norm)

    def reduction(null_residual: float) -> float:
        if null_residual == 0.0:
            return 0.0 if estimate.residual_norm == 0.0 else -math.inf
        return 1.0 - float(estimate.residual_norm) / null_residual

    return RetrodictionNullComparison(
        estimator_residual=float(estimate.residual_norm),
        zero_kick_residual=zero_residual,
        checkpoint_shuffle_residual=shuffle_residual,
        zero_kick_reduction=reduction(zero_residual),
        checkpoint_shuffle_reduction=reduction(shuffle_residual),
        checkpoint_permutation=permutation,
    )
