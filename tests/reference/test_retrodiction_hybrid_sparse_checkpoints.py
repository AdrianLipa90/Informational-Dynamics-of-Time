from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_hybrid_sparse_checkpoints import (
    HybridSparseRetrodictionError,
    audit_hybrid_sparse_checkpoints,
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


def _audit(n: int):
    dts = [0.0025 + 0.0002 * i for i in range(n)]
    kicks = [complex(0.02 * np.cos(i + 1), 0.02 * np.sin(i + 1)) for i in range(n)]
    return audit_hybrid_sparse_checkpoints(_initial(), _attractors(), dts, kicks)


def test_n4_closes_one_missing_channel() -> None:
    audit = _audit(4)
    assert audit.base_rank == 7
    assert audit.hybrid_rank == audit.latent_dimension == 8
    assert audit.orientation_channels == 1
    assert audit.status == "LOCAL_FULL_RANK_HYBRID_REFERENCE"


def test_n5_closes_two_missing_channels() -> None:
    audit = _audit(5)
    assert audit.base_rank == 8
    assert audit.hybrid_rank == audit.latent_dimension == 10
    assert audit.orientation_channels == 2


def test_n6_closes_three_missing_channels() -> None:
    audit = _audit(6)
    assert audit.base_rank == 9
    assert audit.hybrid_rank == audit.latent_dimension == 12
    assert audit.orientation_channels == 3


def test_n3_needs_zero_extra_orientation_channels() -> None:
    audit = _audit(3)
    assert audit.base_rank == audit.hybrid_rank == 6
    assert audit.orientation_channels == 0


def test_random_30_each_n4_to_n6_reaches_full_local_rank() -> None:
    rng = np.random.default_rng(20260827)
    for n in (4, 5, 6):
        accepted = 0
        attempts = 0
        while accepted < 30 and attempts < 100:
            attempts += 1
            initial = MemoryPhaseState(
                position=np.array([-0.8, 0.4]) + rng.normal(scale=0.10, size=2),
                velocity=np.array([0.05, 0.2]) + rng.normal(scale=0.05, size=2),
                tau_internal=0.0,
                swept_area=0.0,
            )
            dts = [float(rng.uniform(0.0015, 0.006)) for _ in range(n)]
            kicks = [complex(*rng.normal(scale=0.035, size=2)) for _ in range(n)]
            try:
                audit = audit_hybrid_sparse_checkpoints(initial, _attractors(), dts, kicks)
            except HybridSparseRetrodictionError:
                continue
            assert audit.base_rank == n + 3
            assert audit.hybrid_rank == 2 * n
            assert audit.orientation_channels == n - 3
            accepted += 1
        assert accepted == 30


def test_invalid_basin_index_fails_closed() -> None:
    with pytest.raises(HybridSparseRetrodictionError, match="basin_weight_index"):
        audit_hybrid_sparse_checkpoints(
            _initial(),
            _attractors(),
            [0.003, 0.003],
            [0.01 + 0.01j, 0.02 - 0.01j],
            basin_weight_index=9,
        )
