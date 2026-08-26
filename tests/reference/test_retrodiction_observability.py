import math

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.retrodiction_observability import (
    RetrodictionObservabilityError,
    audit_kick_observability,
    final_checkpoint_dimension_bound,
    kick_sensitivity_matrix,
)


def _initial_state():
    return MemoryPhaseState(
        np.array([1.2, 0.3], dtype=float),
        np.array([-0.1, 0.7], dtype=float),
        0.4,
        -0.2,
    )


def test_one_unknown_kick_is_locally_identifiable_from_final_phase_state():
    audit = audit_kick_observability(
        _initial_state(), 1.1, [0.03], [0.01 - 0.006j], [1]
    )
    assert audit.jacobian.shape == (4, 2)
    assert audit.rank == 2
    assert audit.locally_identifiable
    assert audit.status == "LOCALLY_IDENTIFIABLE_REFERENCE"
    assert math.isfinite(audit.condition_number)


def test_two_unknown_kicks_are_generically_full_rank_from_final_phase_state_reference_case():
    audit = audit_kick_observability(
        _initial_state(),
        1.1,
        [0.03, 0.035],
        [0.01 - 0.006j, 0.02 - 0.012j],
        [2],
    )
    assert audit.jacobian.shape == (4, 4)
    assert audit.rank == 4
    assert audit.locally_identifiable


def test_three_unknown_kicks_cannot_be_identified_from_one_final_4d_checkpoint_by_dimension():
    audit = audit_kick_observability(
        _initial_state(),
        1.1,
        [0.03, 0.035, 0.04],
        [0.01 - 0.006j, 0.02 - 0.012j, 0.03 - 0.018j],
        [3],
    )
    assert audit.jacobian.shape == (4, 6)
    assert audit.rank <= 4
    assert not audit.locally_identifiable
    assert audit.status == "UNDERDETERMINED_DIMENSION"
    assert math.isinf(audit.condition_number)


def test_intermediate_checkpoints_restore_full_column_rank_for_three_kicks_reference_case():
    audit = audit_kick_observability(
        _initial_state(),
        1.1,
        [0.03, 0.035, 0.04],
        [0.01 - 0.006j, 0.02 - 0.012j, 0.03 - 0.018j],
        [1, 2, 3],
    )
    assert audit.jacobian.shape == (12, 6)
    assert audit.rank == 6
    assert audit.locally_identifiable
    assert audit.status == "LOCALLY_IDENTIFIABLE_REFERENCE"


def test_final_checkpoint_dimension_bound_is_exact_before_dynamics_are_considered():
    assert final_checkpoint_dimension_bound(1) == (2, 4, True)
    assert final_checkpoint_dimension_bound(2) == (4, 4, True)
    assert final_checkpoint_dimension_bound(3) == (6, 4, False)


def test_duplicate_or_initial_checkpoint_indices_fail_closed():
    kwargs = dict(
        initial_state=_initial_state(),
        mu_memory=1.1,
        delta_taus=[0.03, 0.035],
        nominal_kicks=[0.01j, 0.02j],
    )
    with pytest.raises(RetrodictionObservabilityError, match="unique"):
        kick_sensitivity_matrix(**kwargs, checkpoint_indices=[1, 1])
    with pytest.raises(RetrodictionObservabilityError, match="post-event"):
        kick_sensitivity_matrix(**kwargs, checkpoint_indices=[0, 2])


def test_invalid_finite_difference_or_rank_tolerance_fails_closed():
    with pytest.raises(RetrodictionObservabilityError, match="finite_difference_step"):
        kick_sensitivity_matrix(
            _initial_state(), 1.1, [0.03], [0.01j], [1], finite_difference_step=0.0
        )
    with pytest.raises(RetrodictionObservabilityError, match="relative_rank_tolerance"):
        audit_kick_observability(
            _initial_state(), 1.1, [0.03], [0.01j], [1], relative_rank_tolerance=0.0
        )
