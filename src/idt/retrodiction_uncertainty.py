from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .retrodiction_estimation import RetrodictionEstimate
from .retrodiction_observability import RetrodictionObservabilityError, kick_sensitivity_matrix


class RetrodictionUncertaintyError(ValueError):
    pass


@dataclass(frozen=True)
class RetrodictionUncertaintyAudit:
    observation_covariance: np.ndarray
    whitened_jacobian: np.ndarray
    singular_values: np.ndarray
    rank: int
    latent_dimension: int
    observation_dimension: int
    condition_number: float
    fisher_information: np.ndarray
    latent_covariance: np.ndarray | None
    standard_errors: np.ndarray | None
    weighted_residual_quadratic: float
    degrees_of_freedom: int
    reduced_weighted_residual: float | None
    status: str


def isotropic_checkpoint_covariance(observation_dimension: int, standard_deviation: float) -> np.ndarray:
    m = int(observation_dimension)
    if m <= 0:
        raise RetrodictionUncertaintyError("observation_dimension must be a positive integer")
    sigma = float(standard_deviation)
    if not math.isfinite(sigma) or sigma <= 0.0:
        raise RetrodictionUncertaintyError("standard_deviation must be finite and strictly positive")
    return (sigma * sigma) * np.eye(m, dtype=float)


def _validated_covariance(covariance: Sequence[Sequence[float]], dimension: int) -> tuple[np.ndarray, np.ndarray]:
    cov = np.asarray(covariance, dtype=float)
    if cov.shape != (dimension, dimension):
        raise RetrodictionUncertaintyError("observation covariance has incompatible shape")
    if not np.all(np.isfinite(cov)):
        raise RetrodictionUncertaintyError("observation covariance must be finite")
    scale = max(1.0, float(np.max(np.abs(cov))))
    if not np.allclose(cov, cov.T, rtol=0.0, atol=1e-12 * scale):
        raise RetrodictionUncertaintyError("observation covariance must be symmetric")
    try:
        chol = np.linalg.cholesky(cov)
    except np.linalg.LinAlgError as exc:
        raise RetrodictionUncertaintyError("observation covariance must be positive definite") from exc
    return cov, chol


def weighted_retrodiction_uncertainty(
    estimate: RetrodictionEstimate,
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    checkpoint_indices: Sequence[int],
    observation_covariance: Sequence[Sequence[float]],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
    maximum_condition_number: float | None = None,
) -> RetrodictionUncertaintyAudit:
    """Local Gaussian uncertainty geometry around a committed Retrodiction estimate.

    For observation covariance Sigma_Y and sensitivity J, the whitened sensitivity is
    L^{-1}J for Sigma_Y = L L^T. The local Fisher matrix is J^T Sigma_Y^{-1} J.
    """
    eps = float(finite_difference_step)
    rank_tol = float(relative_rank_tolerance)
    if not math.isfinite(eps) or eps <= 0.0:
        raise RetrodictionUncertaintyError("finite_difference_step must be finite and strictly positive")
    if not math.isfinite(rank_tol) or rank_tol <= 0.0:
        raise RetrodictionUncertaintyError("relative_rank_tolerance must be finite and strictly positive")
    if maximum_condition_number is not None:
        max_cond = float(maximum_condition_number)
        if not math.isfinite(max_cond) or max_cond <= 1.0:
            raise RetrodictionUncertaintyError("maximum_condition_number must be finite and greater than one")
    else:
        max_cond = None

    predicted = np.asarray(estimate.predicted_observation, dtype=float)
    residual = np.asarray(estimate.residual, dtype=float)
    if predicted.ndim != 1 or residual.shape != predicted.shape or predicted.size == 0:
        raise RetrodictionUncertaintyError("estimate observation and residual vectors must have one common non-empty shape")
    if not np.all(np.isfinite(predicted)) or not np.all(np.isfinite(residual)):
        raise RetrodictionUncertaintyError("estimate observation and residual vectors must be finite")

    cov, chol = _validated_covariance(observation_covariance, predicted.size)
    try:
        jac = kick_sensitivity_matrix(
            initial_state,
            mu_memory,
            delta_taus,
            estimate.kicks,
            checkpoint_indices,
            finite_difference_step=eps,
        )
    except RetrodictionObservabilityError as exc:
        raise RetrodictionUncertaintyError(str(exc)) from exc
    if jac.shape[0] != predicted.size:
        raise RetrodictionUncertaintyError("sensitivity observation dimension does not match estimate")

    whitened_jac = np.linalg.solve(chol, jac)
    singular = np.linalg.svd(whitened_jac, compute_uv=False)
    latent_dim = int(jac.shape[1])
    observation_dim = int(jac.shape[0])
    threshold = rank_tol * max(1.0, float(singular[0]))
    rank = int(np.sum(singular > threshold))

    fisher = whitened_jac.T @ whitened_jac
    whitened_residual = np.linalg.solve(chol, residual)
    weighted_quadratic = float(whitened_residual @ whitened_residual)
    dof = observation_dim - latent_dim
    reduced = float(weighted_quadratic / dof) if dof > 0 else None

    if rank < latent_dim:
        condition = math.inf
        latent_cov = None
        std = None
        status = "WEIGHTED_RANK_DEFICIENT"
    else:
        smallest = float(singular[latent_dim - 1])
        condition = float(singular[0] / smallest)
        try:
            latent_cov = np.linalg.inv(fisher)
        except np.linalg.LinAlgError as exc:
            raise RetrodictionUncertaintyError("full-rank Fisher matrix inversion failed") from exc
        latent_cov = 0.5 * (latent_cov + latent_cov.T)
        diagonal = np.diag(latent_cov)
        numerical_scale = max(1.0, float(np.max(np.abs(latent_cov))))
        if np.any(diagonal < -1e-12 * numerical_scale):
            raise RetrodictionUncertaintyError("latent covariance has a negative diagonal beyond numerical tolerance")
        std = np.sqrt(np.maximum(diagonal, 0.0))
        if max_cond is not None and condition > max_cond:
            status = "WEIGHTED_ILL_CONDITIONED"
        else:
            status = "WEIGHTED_IDENTIFIABLE_REFERENCE"

    return RetrodictionUncertaintyAudit(
        observation_covariance=cov,
        whitened_jacobian=whitened_jac,
        singular_values=singular,
        rank=rank,
        latent_dimension=latent_dim,
        observation_dimension=observation_dim,
        condition_number=condition,
        fisher_information=fisher,
        latent_covariance=latent_cov,
        standard_errors=std,
        weighted_residual_quadratic=weighted_quadratic,
        degrees_of_freedom=dof,
        reduced_weighted_residual=reduced,
        status=status,
    )
