import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.retrodiction_estimation import estimate_latent_kicks
from src.idt.retrodiction_observability import checkpoint_phase_vector, forward_kick_lineage
from src.idt.retrodiction_uncertainty import (
    RetrodictionUncertaintyError,
    isotropic_checkpoint_covariance,
    weighted_retrodiction_uncertainty,
)


def _reference_estimate():
    initial = MemoryPhaseState(
        np.array([1.2, 0.3], dtype=float),
        np.array([-0.1, 0.7], dtype=float),
        0.4,
        -0.2,
    )
    mu = 1.1
    dts = [0.03, 0.04, 0.05]
    truth = [0.02 + 0.05j, -0.015 + 0.01j, 0.012 - 0.02j]
    checkpoints = [1, 2, 3]
    observed = checkpoint_phase_vector(forward_kick_lineage(initial, mu, dts, truth), checkpoints)
    estimate = estimate_latent_kicks(initial, mu, dts, observed, checkpoints, 3)
    return initial, mu, dts, checkpoints, estimate


def test_isotropic_checkpoint_noise_produces_full_rank_fisher_geometry():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    covariance = isotropic_checkpoint_covariance(12, 1e-5)
    audit = weighted_retrodiction_uncertainty(
        estimate,
        initial,
        mu,
        dts,
        checkpoints,
        covariance,
    )
    assert audit.status == "WEIGHTED_IDENTIFIABLE_REFERENCE"
    assert audit.rank == 6
    assert audit.latent_dimension == 6
    assert audit.observation_dimension == 12
    assert 3.5 < audit.condition_number < 4.5
    assert audit.latent_covariance is not None
    assert audit.standard_errors is not None
    assert np.all(audit.standard_errors > 0.0)
    assert np.max(audit.standard_errors) < 1.6e-5
    assert audit.degrees_of_freedom == 6


def test_isotropic_noise_scale_propagates_quadratically_into_latent_covariance():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    a = weighted_retrodiction_uncertainty(
        estimate, initial, mu, dts, checkpoints, isotropic_checkpoint_covariance(12, 1e-5)
    )
    b = weighted_retrodiction_uncertainty(
        estimate, initial, mu, dts, checkpoints, isotropic_checkpoint_covariance(12, 2e-5)
    )
    assert a.latent_covariance is not None
    assert b.latent_covariance is not None
    assert np.allclose(b.latent_covariance, 4.0 * a.latent_covariance, rtol=2e-6, atol=1e-20)
    assert np.allclose(b.standard_errors, 2.0 * a.standard_errors, rtol=2e-6, atol=1e-20)


def test_fisher_covariance_is_inverse_on_the_full_rank_reference_subspace():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    audit = weighted_retrodiction_uncertainty(
        estimate, initial, mu, dts, checkpoints, isotropic_checkpoint_covariance(12, 1e-5)
    )
    identity = audit.fisher_information @ audit.latent_covariance
    assert np.allclose(identity, np.eye(6), rtol=1e-8, atol=1e-8)


def test_explicit_condition_limit_can_gate_a_full_rank_but_weak_reference_geometry():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    audit = weighted_retrodiction_uncertainty(
        estimate,
        initial,
        mu,
        dts,
        checkpoints,
        isotropic_checkpoint_covariance(12, 1e-5),
        maximum_condition_number=2.0,
    )
    assert audit.rank == 6
    assert audit.condition_number > 2.0
    assert audit.status == "WEIGHTED_ILL_CONDITIONED"


def test_invalid_observation_covariance_fails_closed():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    bad = np.eye(12)
    bad[-1, -1] = 0.0
    with pytest.raises(RetrodictionUncertaintyError, match="positive definite"):
        weighted_retrodiction_uncertainty(estimate, initial, mu, dts, checkpoints, bad)


def test_covariance_dimension_mismatch_fails_closed():
    initial, mu, dts, checkpoints, estimate = _reference_estimate()
    with pytest.raises(RetrodictionUncertaintyError, match="incompatible shape"):
        weighted_retrodiction_uncertainty(estimate, initial, mu, dts, checkpoints, np.eye(8))
