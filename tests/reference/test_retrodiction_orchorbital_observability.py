from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_orchorbital_observability import (
    ORCHORBITALRetrodictionError,
    audit_orchorbital_augmented_observability,
)


def _initial():
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


def _kwargs():
    return dict(
        initial_state=_initial(),
        attractors=_attractors(),
        delta_taus=[0.004, 0.003],
        nominal_kicks=[0.03 - 0.02j, -0.01 + 0.025j],
        checkpoint_indices=[2],
    )


def test_full_checkpoint_orchorbital_weights_do_not_increase_rank() -> None:
    audit = audit_orchorbital_augmented_observability(
        **_kwargs(),
        components=["rx", "ry", "vx", "vy"],
    )
    assert audit.base_rank == 4
    assert audit.augmented_rank == 4
    weights_jac = audit.augmented_jacobian[4:, :]
    residual = weights_jac - (weights_jac @ np.linalg.pinv(audit.base_jacobian)) @ audit.base_jacobian
    assert np.linalg.norm(residual) < 1e-10


def test_partial_checkpoint_position_and_vx_gains_one_orchorbital_rank_channel() -> None:
    audit = audit_orchorbital_augmented_observability(
        **_kwargs(),
        components=["rx", "ry", "vx"],
    )
    assert audit.base_rank == 3
    assert audit.augmented_rank == 4
    assert audit.unknown_dimension == 4


def test_position_only_checkpoint_gains_one_but_not_all_missing_channels() -> None:
    audit = audit_orchorbital_augmented_observability(
        **_kwargs(),
        components=["rx", "ry"],
    )
    assert audit.base_rank == 2
    assert audit.augmented_rank == 3
    assert audit.augmented_rank < audit.unknown_dimension


def test_local_rank_restoration_is_stable_over_100_reference_perturbations() -> None:
    rng = np.random.default_rng(20260827)
    for _ in range(100):
        initial = _initial()
        initial = MemoryPhaseState(
            position=initial.position + rng.normal(scale=0.05, size=2),
            velocity=initial.velocity + rng.normal(scale=0.04, size=2),
            tau_internal=0.0,
            swept_area=0.0,
        )
        kicks = [
            complex(0.03, -0.02) + complex(*rng.normal(scale=0.006, size=2)),
            complex(-0.01, 0.025) + complex(*rng.normal(scale=0.006, size=2)),
        ]
        audit = audit_orchorbital_augmented_observability(
            initial,
            _attractors(),
            [0.004, 0.003],
            kicks,
            [2],
            ["rx", "ry", "vx"],
        )
        assert audit.base_rank == 3
        assert audit.augmented_rank == 4


def test_invalid_component_selection_fails_closed() -> None:
    with pytest.raises(ORCHORBITALRetrodictionError):
        audit_orchorbital_augmented_observability(
            **_kwargs(),
            components=["rx", "bad"],
        )
