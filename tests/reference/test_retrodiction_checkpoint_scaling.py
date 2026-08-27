from __future__ import annotations

import pytest

from src.idt.retrodiction_checkpoint_scaling import (
    RetrodictionCheckpointScalingError,
    minimum_extra_scalars_for_declared_schedule,
    one_weight_per_earlier_checkpoint_bound,
)


def test_declared_schedule_rank_bound_is_n_plus_three():
    for n in range(1, 12):
        audit = one_weight_per_earlier_checkpoint_bound(n)
        assert audit.latent_dimension == 2 * n
        assert audit.rank_upper_bound == n + 3


def test_n_three_is_last_dimensionally_possible_event_count():
    assert one_weight_per_earlier_checkpoint_bound(3).dimensionally_possible
    assert not one_weight_per_earlier_checkpoint_bound(4).dimensionally_possible


def test_n_ge_four_minimum_deficit_is_n_minus_three():
    for n in range(4, 12):
        audit = one_weight_per_earlier_checkpoint_bound(n)
        assert audit.minimum_rank_deficit == n - 3
        assert minimum_extra_scalars_for_declared_schedule(n) == n - 3


def test_reference_n4_n5_n6_match_probe_rank_ceiling():
    observed = {4: 7, 5: 8, 6: 9}
    for n, rank in observed.items():
        assert rank == one_weight_per_earlier_checkpoint_bound(n).rank_upper_bound


def test_invalid_event_count_fails_closed():
    with pytest.raises(RetrodictionCheckpointScalingError):
        one_weight_per_earlier_checkpoint_bound(0)
