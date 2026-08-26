import numpy as np
import pytest

from idt.kepler_memory import MemoryPhaseState
from idt.retrodiction_observability import checkpoint_phase_vector, forward_kick_lineage
from idt.retrodiction_weighted_nulls import (
    RetrodictionWeightedError,
    checkpoint_permutation_null_ensemble,
    estimate_latent_kicks_weighted,
)


def reference_case():
    state = MemoryPhaseState(
        position=np.array([1.2, 0.1], dtype=float),
        velocity=np.array([-0.05, 0.85], dtype=float),
    )
    mu = 1.0
    delta_taus = [0.03, 0.04, 0.035]
    truth = [0.012 - 0.006j, -0.008 + 0.011j, 0.006 + 0.004j]
    checkpoints = [1, 2, 3]
    states = forward_kick_lineage(state, mu, delta_taus, truth)
    observed = checkpoint_phase_vector(states, checkpoints)
    covariance = np.eye(observed.size, dtype=float) * 1e-8
    return state, mu, delta_taus, truth, checkpoints, observed, covariance


def test_weighted_estimator_recovers_exact_three_kick_lineage():
    state, mu, delta_taus, truth, checkpoints, observed, covariance = reference_case()
    fit = estimate_latent_kicks_weighted(state, mu, delta_taus, observed, checkpoints, 3, covariance)
    assert fit.status == "CONVERGED_WEIGHTED_RESIDUAL"
    assert fit.weighted_rank == 6
    assert fit.latent_dimension == 6
    assert fit.weighted_residual_quadratic < 1e-12
    assert fit.condition_number < 10.0
    assert np.max(np.abs(np.asarray(fit.kicks) - np.asarray(truth))) < 1e-12


def test_permutation_ensemble_uses_all_five_nonidentity_orders_and_observed_wins():
    state, mu, delta_taus, _, checkpoints, observed, covariance = reference_case()
    ensemble = checkpoint_permutation_null_ensemble(state, mu, delta_taus, observed, checkpoints, 3, covariance)
    assert ensemble.status == "PERMUTATION_REFERENCE_ENSEMBLE_COMPLETE"
    assert len(ensemble.entries) == 5
    assert ensemble.observed_weighted_residual_quadratic < 1e-12
    assert ensemble.null_minimum > ensemble.observed_weighted_residual_quadratic
    assert ensemble.null_margin > 0.0
    assert ensemble.null_better_or_equal_count == 0
    assert ensemble.null_rank_fraction == 0.0


def test_covariance_scaling_rescales_weighted_quadratic_not_exact_solution():
    state, mu, delta_taus, _, checkpoints, observed, covariance = reference_case()
    noisy = observed.copy()
    noisy[0] += 2e-5
    fit1 = estimate_latent_kicks_weighted(state, mu, delta_taus, noisy, checkpoints, 3, covariance)
    fit2 = estimate_latent_kicks_weighted(state, mu, delta_taus, noisy, checkpoints, 3, 4.0 * covariance)
    assert np.max(np.abs(np.asarray(fit1.kicks) - np.asarray(fit2.kicks))) < 1e-9
    assert fit2.weighted_residual_quadratic == pytest.approx(fit1.weighted_residual_quadratic / 4.0, rel=5e-4, abs=1e-12)


def test_non_positive_definite_covariance_fails_closed():
    state, mu, delta_taus, _, checkpoints, observed, covariance = reference_case()
    covariance[0, 0] = -1.0
    with pytest.raises(RetrodictionWeightedError, match="positive definite"):
        estimate_latent_kicks_weighted(state, mu, delta_taus, observed, checkpoints, 3, covariance)


def test_permutation_limit_fails_closed_before_partial_ensemble():
    state, mu, delta_taus, _, checkpoints, observed, covariance = reference_case()
    with pytest.raises(RetrodictionWeightedError, match="exceeds maximum_permutations"):
        checkpoint_permutation_null_ensemble(
            state, mu, delta_taus, observed, checkpoints, 3, covariance,
            maximum_permutations=4,
        )
