from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_orchorbital_estimation import (
    ORCHORBITALEstimationError,
    estimate_local_orchorbital_kicks,
    orchorbital_checkpoint_observation,
)


def _initial() -> MemoryPhaseState:
    return MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _attractors():
    return [
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    ]


def _delta_taus():
    return [0.004, 0.003]


def _nominal():
    return [0.03 - 0.02j, -0.01 + 0.025j]


def _truth():
    return [0.034 - 0.023j, -0.008 + 0.028j]


def _target(kicks, *, components=("rx", "ry", "vx"), include_weights=True):
    return orchorbital_checkpoint_observation(
        _initial(),
        _attractors(),
        _delta_taus(),
        kicks,
        [2],
        list(components),
        include_weights=include_weights,
    )


def test_augmented_local_estimator_recovers_reference_two_kick_lineage() -> None:
    target = _target(_truth())
    estimate = estimate_local_orchorbital_kicks(
        _initial(),
        _attractors(),
        _delta_taus(),
        target,
        _nominal(),
        [2],
        ["rx", "ry", "vx"],
        include_weights=True,
    )
    assert estimate.converged
    assert estimate.local_rank == 4
    assert estimate.unknown_dimension == 4
    assert estimate.residual_norm < 1e-10
    assert np.linalg.norm(np.asarray(estimate.kicks) - np.asarray(_truth())) < 1e-7


def test_augmented_local_estimator_recovers_40_nearby_cases() -> None:
    rng = np.random.default_rng(20260827)
    nominal = np.asarray(_nominal(), dtype=complex)
    for _ in range(40):
        perturb = rng.normal(scale=0.008, size=(2, 2))
        truth = [
            complex(nominal[i].real + perturb[i, 0], nominal[i].imag + perturb[i, 1])
            for i in range(2)
        ]
        target = _target(truth)
        estimate = estimate_local_orchorbital_kicks(
            _initial(),
            _attractors(),
            _delta_taus(),
            target,
            _nominal(),
            [2],
            ["rx", "ry", "vx"],
            include_weights=True,
        )
        assert estimate.converged
        assert estimate.residual_norm < 1e-9
        assert np.linalg.norm(np.asarray(estimate.kicks) - np.asarray(truth)) < 1e-6


def test_partial_only_rank_deficiency_fails_closed() -> None:
    target = _target(_truth(), include_weights=False)
    with pytest.raises(ORCHORBITALEstimationError, match="rank deficient"):
        estimate_local_orchorbital_kicks(
            _initial(),
            _attractors(),
            _delta_taus(),
            target,
            _nominal(),
            [2],
            ["rx", "ry", "vx"],
            include_weights=False,
        )


def test_global_reflection_null_is_distinct_from_local_rank_pass() -> None:
    alternate = [
        complex(0.03399999999998063, 0.34071654937113033),
        complex(-0.00802729491823317, -0.8206629500579328),
    ]
    target_truth = _target(_truth())
    target_alternate = _target(alternate)
    assert np.allclose(target_truth, target_alternate, atol=5e-12, rtol=0.0)

    full_truth = _target(
        _truth(),
        components=("rx", "ry", "vx", "vy"),
        include_weights=False,
    )
    full_alternate = _target(
        alternate,
        components=("rx", "ry", "vx", "vy"),
        include_weights=False,
    )
    assert np.allclose(full_truth[:3], full_alternate[:3], atol=5e-12, rtol=0.0)
    assert full_truth[3] * full_alternate[3] < 0.0
    assert np.linalg.norm(np.asarray(alternate) - np.asarray(_truth())) > 0.5

    near_truth = estimate_local_orchorbital_kicks(
        _initial(),
        _attractors(),
        _delta_taus(),
        target_truth,
        _nominal(),
        [2],
        ["rx", "ry", "vx"],
        include_weights=True,
    )
    near_alternate = estimate_local_orchorbital_kicks(
        _initial(),
        _attractors(),
        _delta_taus(),
        target_truth,
        alternate,
        [2],
        ["rx", "ry", "vx"],
        include_weights=True,
    )
    assert near_truth.converged and near_alternate.converged
    assert near_truth.residual_norm < 1e-10
    assert near_alternate.residual_norm < 1e-10
    assert np.linalg.norm(
        np.asarray(near_truth.kicks) - np.asarray(near_alternate.kicks)
    ) > 0.5


def test_target_dimension_mismatch_fails_closed() -> None:
    with pytest.raises(ORCHORBITALEstimationError, match="dimension"):
        estimate_local_orchorbital_kicks(
            _initial(),
            _attractors(),
            _delta_taus(),
            [1.0, 2.0],
            _nominal(),
            [2],
            ["rx", "ry", "vx"],
            include_weights=True,
        )
