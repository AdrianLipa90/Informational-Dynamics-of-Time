from __future__ import annotations

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec, evaluate_attractor_field
from src.idt.retrodiction_sparse_completion import (
    SparseCheckpointCompletionError,
    minimal_position_completion,
    numerical_rank,
    position_lineage_rank_certificate,
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


def _forward(kicks, dts):
    receipts = [MemoryEventReceipt(float(dt), 1.0, complex(kick)) for dt, kick in zip(dts, kicks)]
    return replay_memory_orchorbital_lineage(_initial(), _attractors(), receipts)


def _regime(states, cells):
    checkpoints = []
    for state in states[1:]:
        field = evaluate_attractor_field(state, _attractors())
        if field.leak_mode:
            raise ValueError("LEAK_MODE")
        checkpoints.append(
            (field.active_attractor, tuple(ev.weight > 0.0 for ev in field.evaluations))
        )
    return tuple(cell.active_attractor for cell in cells), tuple(checkpoints)


def _sparse_observation(kicks, dts):
    states, cells = _forward(kicks, dts)
    values = []
    for state in states[1:-1]:
        field = evaluate_attractor_field(state, _attractors())
        values.append(float(field.evaluations[0].weight))
    final = states[-1]
    values.extend([float(final.position[0]), float(final.position[1]), float(final.velocity[0])])
    field = evaluate_attractor_field(final, _attractors())
    values.extend(float(ev.weight) for ev in field.evaluations)
    return np.asarray(values, dtype=float), _regime(states, cells)


def _position_observation(kicks, dts):
    states, cells = _forward(kicks, dts)
    values = np.concatenate([np.asarray(state.position, dtype=float) for state in states[1:]])
    return values, _regime(states, cells)


def _jacobian(observe, kicks, dts, eps=1e-7):
    matrix = np.asarray([[complex(k).real, complex(k).imag] for k in kicks], dtype=float)
    y0, regime0 = observe([complex(*row) for row in matrix], dts)
    jac = np.empty((y0.size, matrix.size), dtype=float)
    for column in range(matrix.size):
        plus = matrix.copy()
        minus = matrix.copy()
        plus.flat[column] += eps
        minus.flat[column] -= eps
        yp, regime_p = observe([complex(*row) for row in plus], dts)
        ym, regime_m = observe([complex(*row) for row in minus], dts)
        if regime_p != regime0 or regime_m != regime0:
            raise ValueError("finite difference crossed a fixed-regime boundary")
        jac[:, column] = (yp - ym) / (2.0 * eps)
    return jac


def _position_labels(n):
    return tuple(label for i in range(1, n + 1) for label in (f"r{i}x", f"r{i}y"))


def test_position_lineage_certificate_has_exact_2n_rank_budget():
    cert = position_lineage_rank_certificate([0.004, 0.003, 0.005, 0.0025])
    assert cert.event_count == 4
    assert cert.latent_dimension == 8
    assert cert.status == "FULL_RANK_BY_BLOCK_LOWER_TRIANGULAR_DIAGONAL"
    assert np.isfinite(cert.log_abs_block_diagonal_determinant)


def test_07j_07k_synthesis_selects_exactly_n_minus_three_position_scalars():
    rng = np.random.default_rng(20260827)
    for n in range(4, 9):
        dts = rng.uniform(0.0015, 0.007, size=n)
        kicks = [complex(*rng.normal(scale=0.035, size=2)) for _ in range(n)]
        base = _jacobian(_sparse_observation, kicks, dts)
        pool = _jacobian(_position_observation, kicks, dts)
        assert numerical_rank(base, relative_rank_tolerance=1e-7) == n + 3
        result = minimal_position_completion(
            base,
            pool,
            position_labels=_position_labels(n),
            relative_rank_tolerance=1e-7,
        )
        assert result.minimum_additional_scalars == n - 3
        assert result.completed_rank == result.latent_dimension == 2 * n
        assert len(result.selected_row_indices) == n - 3
        assert result.selected_labels == tuple(f"r{i}x" for i in range(1, n - 2))


def test_random_fixed_regime_reference_cases_close_with_the_exact_rank_deficit():
    rng = np.random.default_rng(2026082707)
    accepted = 0
    attempts = 0
    while accepted < 40 and attempts < 80:
        attempts += 1
        n = int(rng.integers(4, 9))
        dts = rng.uniform(0.001, 0.008, size=n)
        kicks = [complex(*rng.normal(scale=0.04, size=2)) for _ in range(n)]
        try:
            base = _jacobian(_sparse_observation, kicks, dts)
            pool = _jacobian(_position_observation, kicks, dts)
        except ValueError:
            continue
        result = minimal_position_completion(
            base,
            pool,
            position_labels=_position_labels(n),
            relative_rank_tolerance=1e-7,
        )
        assert result.base_rank == n + 3
        assert result.position_pool_rank == 2 * n
        assert result.minimum_additional_scalars == n - 3
        assert result.completed_rank == 2 * n
        accepted += 1
    assert accepted == 40


def test_base_already_full_rank_requires_zero_additional_scalars():
    base = np.eye(4)
    pool = np.eye(4)
    result = minimal_position_completion(base, pool)
    assert result.minimum_additional_scalars == 0
    assert result.selected_row_indices == ()
    assert result.status == "BASE_ALREADY_FULL_RANK"


def test_rank_deficient_position_pool_fails_closed():
    base = np.array([[1.0, 0.0, 0.0, 0.0]])
    pool = np.array([[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]])
    with pytest.raises(SparseCheckpointCompletionError, match="full latent dimension"):
        minimal_position_completion(base, pool)


def test_shape_and_delta_tau_validation_fail_closed():
    with pytest.raises(SparseCheckpointCompletionError):
        minimal_position_completion(np.eye(3), np.eye(4))
    with pytest.raises(SparseCheckpointCompletionError):
        position_lineage_rank_certificate([0.01, 0.0])
