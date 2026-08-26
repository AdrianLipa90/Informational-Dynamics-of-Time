import numpy as np

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.retrodiction_checkpoint_selection import (
    audit_checkpoint_subset,
    checkpoint_cardinality_lower_bound,
    minimal_observable_checkpoint_set,
)


def _case():
    initial = MemoryPhaseState(
        np.array([1.2, 0.3], dtype=float),
        np.array([-0.1, 0.7], dtype=float),
        0.4,
        -0.2,
    )
    mu = 1.1
    dts = [0.03, 0.04, 0.05]
    kicks = [0.02 + 0.05j, -0.015 + 0.01j, 0.012 - 0.02j]
    return initial, mu, dts, kicks


def test_three_kicks_have_two_checkpoint_dimensional_lower_bound():
    assert checkpoint_cardinality_lower_bound(3) == 2
    assert checkpoint_cardinality_lower_bound(4) == 2
    assert checkpoint_cardinality_lower_bound(5) == 3


def test_reference_minimal_full_rank_subset_uses_two_checkpoints():
    initial, mu, dts, kicks = _case()
    result = minimal_observable_checkpoint_set(initial, mu, dts, kicks, [1, 2, 3])
    assert result.status == "MINIMAL_ADMISSIBLE_CHECKPOINT_SET"
    assert result.lower_bound_cardinality == 2
    assert result.selected is not None
    assert result.selected.checkpoint_indices == (1, 3)
    assert result.selected.rank == 6
    assert result.selected.observation_dimension == 8
    assert result.full_rank_subsets_at_selected_cardinality == 2
    assert 60.0 < result.selected.condition_number < 70.0


def test_minimum_cardinality_and_numerical_stability_are_distinct_gates():
    initial, mu, dts, kicks = _case()
    minimal = minimal_observable_checkpoint_set(initial, mu, dts, kicks, [1, 2, 3])
    stable = minimal_observable_checkpoint_set(
        initial,
        mu,
        dts,
        kicks,
        [1, 2, 3],
        maximum_condition_number=10.0,
    )
    assert minimal.selected.checkpoint_indices == (1, 3)
    assert stable.selected is not None
    assert stable.selected.checkpoint_indices == (1, 2, 3)
    assert stable.selected.condition_number < 5.0


def test_two_early_checkpoints_are_rank_deficient_for_three_kicks():
    initial, mu, dts, kicks = _case()
    audit = audit_checkpoint_subset(initial, mu, dts, kicks, [1, 2])
    assert audit.observation_dimension == 8
    assert audit.latent_dimension == 6
    assert audit.rank == 4
    assert not audit.full_column_rank
    assert audit.status == "RANK_DEFICIENT"


def test_candidate_pool_without_late_information_returns_no_admissible_set():
    initial, mu, dts, kicks = _case()
    result = minimal_observable_checkpoint_set(initial, mu, dts, kicks, [1, 2])
    assert result.selected is None
    assert result.status == "NO_ADMISSIBLE_CHECKPOINT_SET"
