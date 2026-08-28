from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .kepler_memory import MemoryPhaseState
from .orchorbital import AttractorSpec
from .retrodiction_orchorbital_residence_conditioning import ResidenceLineageSignature
from .retrodiction_position_lineage_exact import (
    PositionLineageRetrodictionResult,
    retrodict_kicks_from_position_lineage,
)
from .retrodiction_sparse_completion import position_lineage_rank_certificate


class StratifiedPositionLiftError(ValueError):
    pass


@dataclass(frozen=True)
class StratifiedGlobalReductionCertificate:
    active_sequence: tuple[str, ...]
    event_count: int
    latent_dimension: int
    position_lineage_dimension: int
    cross_sequence_separator: str
    fixed_sequence_inverse: str
    remaining_requirement: str
    status: str


@dataclass(frozen=True)
class ConstructivePositionLiftRecovery:
    active_sequence: tuple[str, ...]
    position_lineage_dimension: int
    recovered: PositionLineageRetrodictionResult
    status: str


def _active_sequence(values: Sequence[str]) -> tuple[str, ...]:
    sequence = tuple(str(value).strip() for value in values)
    if not sequence or any(not value for value in sequence):
        raise StratifiedPositionLiftError(
            "active_sequence must contain non-empty attractor labels"
        )
    return sequence


def active_sequence_stratum_key(values: Sequence[str]) -> tuple[str, ...]:
    """Return the exact retained active-sequence stratum key.

    ResidenceLineageSignature records the active attractor of every smooth cell,
    so unequal keys are unequal retained observation coordinates.
    """
    return _active_sequence(values)


def active_sequences_are_cross_stratum_separated(
    left: Sequence[str],
    right: Sequence[str],
) -> bool:
    """Exact cross-stratum separator induced by retained residence labels."""
    return active_sequence_stratum_key(left) != active_sequence_stratum_key(right)


def certify_stratified_global_reduction(
    active_sequence: Sequence[str],
    delta_taus: Sequence[float],
) -> StratifiedGlobalReductionCertificate:
    """Certify the exact reduction of global injectivity to a fixed-sequence lift.

    Because the retained residence signature contains the exact active sequence,
    histories with different active sequences cannot share the same augmented
    observation. Within one fixed sequence, the complete ordered post-segment
    position lineage has an exact constructive inverse to the event kicks (07K).
    Together with the 07R fiber-lift composition theorem, global injectivity is
    therefore reduced to reconstructing that position lineage from the retained
    augmented observation inside every fixed-sequence stratum.
    """
    sequence = _active_sequence(active_sequence)
    dts = tuple(float(value) for value in delta_taus)
    if len(dts) != len(sequence):
        raise StratifiedPositionLiftError(
            "active_sequence and delta_taus must have equal length"
        )
    if any((not math.isfinite(dt) or dt <= 0.0) for dt in dts):
        raise StratifiedPositionLiftError(
            "delta_taus must be finite and strictly positive"
        )
    rank_certificate = position_lineage_rank_certificate(dts)
    if rank_certificate.latent_dimension != 2 * len(sequence):
        raise StratifiedPositionLiftError(
            "position-lineage rank certificate dimension mismatch"
        )
    return StratifiedGlobalReductionCertificate(
        active_sequence=sequence,
        event_count=len(sequence),
        latent_dimension=rank_certificate.latent_dimension,
        position_lineage_dimension=rank_certificate.latent_dimension,
        cross_sequence_separator="RETAINED_ACTIVE_SEQUENCE_EXACT",
        fixed_sequence_inverse="07K_EXACT_POSITION_LINEAGE_RECOVERY",
        remaining_requirement="Y_AUG_TO_ORDERED_POSITION_LINEAGE_LIFT_PER_FIXED_SEQUENCE_STRATUM",
        status="GLOBAL_INJECTIVITY_REDUCED_TO_FIXED_SEQUENCE_POSITION_LIFT",
    )


def retrodict_from_retained_position_lift(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    residence_signature: ResidenceLineageSignature,
    delta_taus: Sequence[float],
    lifted_checkpoint_positions: Sequence[Sequence[float]],
    *,
    position_tolerance: float = 1e-9,
) -> ConstructivePositionLiftRecovery:
    """Compose a retained residence stratum with a decoded position-lineage lift.

    This function is the executable constructive part of the 07R implication.
    It accepts an already-decoded ordered position lineage and invokes the exact
    07K inverse using the active sequence retained by the residence layer. It
    keeps the remaining Y_aug -> position-lineage decoder as a separate gate.
    """
    if not isinstance(residence_signature, ResidenceLineageSignature):
        raise StratifiedPositionLiftError(
            "residence_signature must be a ResidenceLineageSignature"
        )
    sequence = _active_sequence(residence_signature.active_sequence)
    certificate = certify_stratified_global_reduction(sequence, delta_taus)
    if len(lifted_checkpoint_positions) != certificate.event_count:
        raise StratifiedPositionLiftError(
            "lifted_checkpoint_positions must match the retained active-sequence length"
        )
    try:
        recovered = retrodict_kicks_from_position_lineage(
            initial_state,
            attractors,
            sequence,
            delta_taus,
            lifted_checkpoint_positions,
            position_tolerance=position_tolerance,
        )
    except ValueError as exc:
        raise StratifiedPositionLiftError(str(exc)) from exc
    if recovered.status != "EXACT_POSITION_LINEAGE_RECOVERY":
        raise StratifiedPositionLiftError(
            "07K position-lineage inverse did not return its exact recovery status"
        )
    if recovered.observation_dimension != certificate.position_lineage_dimension:
        raise StratifiedPositionLiftError(
            "decoded position-lineage dimension does not match the stratified certificate"
        )
    return ConstructivePositionLiftRecovery(
        active_sequence=sequence,
        position_lineage_dimension=certificate.position_lineage_dimension,
        recovered=recovered,
        status="CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_RECOVERY",
    )
