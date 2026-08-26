import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.retrodiction_estimation import (
    RetrodictionEstimationError,
    compare_with_reference_nulls,
    estimate_commitment,
    estimate_latent_kicks,
    score_committed_estimate,
)
from src.idt.retrodiction_observability import checkpoint_phase_vector, forward_kick_lineage


def _initial():
    return MemoryPhaseState(
        np.array([1.2, 0.3], dtype=float),
        np.array([-0.1, 0.7], dtype=float),
        0.4,
        -0.2,
    )


def _case():
    dts = [0.03, 0.04, 0.05]
    truth = [0.02 + 0.05j, -0.015 + 0.01j, 0.012 - 0.02j]
    checkpoints = [1, 2, 3]
    states = forward_kick_lineage(_initial(), 1.1, dts, truth)
    observed = checkpoint_phase_vector(states, checkpoints)
    return dts, truth, checkpoints, observed


def test_three_kicks_recover_from_three_retained_phase_checkpoints():
    dts, truth, checkpoints, observed = _case()
    estimate = estimate_latent_kicks(_initial(), 1.1, dts, observed, checkpoints, 3)
    inferred = np.array([[z.real, z.imag] for z in estimate.kicks]).reshape(-1)
    expected = np.array([[z.real, z.imag] for z in truth]).reshape(-1)
    assert estimate.observability.rank == 6
    assert estimate.observability.locally_identifiable
    assert estimate.status == "CONVERGED_RESIDUAL"
    assert estimate.residual_norm < 2e-13
    assert np.max(np.abs(inferred - expected)) < 2e-12


def test_one_final_checkpoint_rejects_three_unknown_kicks_before_optimization():
    dts, truth, _, _ = _case()
    final_states = forward_kick_lineage(_initial(), 1.1, dts, truth)
    final_observed = checkpoint_phase_vector(final_states, [3])
    with pytest.raises(RetrodictionEstimationError, match="observability gate rejected"):
        estimate_latent_kicks(_initial(), 1.1, dts, final_observed, [3], 3)


def test_estimate_commitment_is_verified_before_truth_scoring():
    dts, truth, checkpoints, observed = _case()
    estimate = estimate_latent_kicks(_initial(), 1.1, dts, observed, checkpoints, 3)
    commitment = estimate_commitment(estimate)
    score = score_committed_estimate(estimate, truth, commitment)
    assert score.estimate_commitment == commitment
    assert score.max_abs_kick_error < 2e-12
    assert score.kick_rmse < 1e-12
    with pytest.raises(RetrodictionEstimationError, match="commitment mismatch"):
        score_committed_estimate(estimate, truth, "0" * 64)


def test_reference_estimator_beats_zero_kick_and_checkpoint_shuffle_nulls():
    dts, _, checkpoints, observed = _case()
    estimate = estimate_latent_kicks(_initial(), 1.1, dts, observed, checkpoints, 3)
    comparison = compare_with_reference_nulls(
        estimate,
        _initial(),
        1.1,
        dts,
        observed,
        checkpoints,
    )
    assert comparison.zero_kick_residual > 1e-3
    assert comparison.checkpoint_shuffle_residual > 1e-3
    assert comparison.estimator_residual < 2e-13
    assert comparison.zero_kick_reduction > 0.999999
    assert comparison.checkpoint_shuffle_reduction > 0.999999
    assert comparison.checkpoint_permutation == (2, 1, 0)


def test_randomized_observable_three_kick_cases_recover_at_roundoff_scale():
    rng = np.random.default_rng(20260826)
    max_error = 0.0
    for _ in range(50):
        initial = MemoryPhaseState(
            np.array([1.0 + rng.uniform(0.1, 0.5), rng.uniform(-0.25, 0.25)], dtype=float),
            np.array([rng.uniform(-0.12, 0.12), rng.uniform(0.58, 0.82)], dtype=float),
        )
        mu = float(rng.uniform(0.9, 1.3))
        dts = list(rng.uniform(0.02, 0.05, size=3))
        truth = [complex(*rng.uniform(-0.03, 0.03, size=2)) for _ in range(3)]
        checkpoints = [1, 2, 3]
        observed = checkpoint_phase_vector(forward_kick_lineage(initial, mu, dts, truth), checkpoints)
        estimate = estimate_latent_kicks(initial, mu, dts, observed, checkpoints, 3)
        inferred = np.array([[z.real, z.imag] for z in estimate.kicks]).reshape(-1)
        expected = np.array([[z.real, z.imag] for z in truth]).reshape(-1)
        max_error = max(max_error, float(np.max(np.abs(inferred - expected))))
        assert estimate.observability.rank == 6
        assert estimate.status == "CONVERGED_RESIDUAL"
    assert max_error < 2e-11
