from __future__ import annotations

from dataclasses import dataclass


class RetrodictionCheckpointScalingError(ValueError):
    pass


@dataclass(frozen=True)
class CheckpointScalingBound:
    event_count: int
    latent_dimension: int
    rank_upper_bound: int
    minimum_rank_deficit: int
    minimum_additional_independent_scalars: int
    dimensionally_possible: bool


def one_weight_per_earlier_checkpoint_bound(event_count: int) -> CheckpointScalingBound:
    """Rank budget for final (rx,ry,vx)+final basin weights + one earlier weight/checkpoint.

    Final position plus vx supplies three channels. In a fixed basin-support
    regime all final basin weights add at most the one kinetic scalar T, so the
    final block contributes at most four independent rows. The N-1 earlier
    scalar weights add at most N-1 further rows.
    """
    n = int(event_count)
    if n <= 0:
        raise RetrodictionCheckpointScalingError("event_count must be a positive integer")
    latent = 2 * n
    rank_bound = n + 3
    deficit = max(0, latent - rank_bound)
    return CheckpointScalingBound(
        event_count=n,
        latent_dimension=latent,
        rank_upper_bound=rank_bound,
        minimum_rank_deficit=deficit,
        minimum_additional_independent_scalars=deficit,
        dimensionally_possible=(rank_bound >= latent),
    )


def minimum_extra_scalars_for_declared_schedule(event_count: int) -> int:
    return one_weight_per_earlier_checkpoint_bound(event_count).minimum_additional_independent_scalars
