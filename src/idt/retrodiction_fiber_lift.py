from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


class FiberLiftCompositionError(ValueError):
    pass


@dataclass(frozen=True)
class FiberLiftPairAudit:
    reference_index: int
    candidate_index: int
    latent_distance: float
    carrier_distance: float
    base_distance: float
    fiber_distances: tuple[tuple[str, float], ...]
    augmented_collision: bool
    carrier_collision: bool
    lift_conflict: bool


@dataclass(frozen=True)
class FiniteFiberLiftAudit:
    candidate_count: int
    distinct_latent_pair_count: int
    carrier_collision_count: int
    augmented_collision_count: int
    lift_conflict_count: int
    minimum_distinct_carrier_distance: float | None
    minimum_distinct_augmented_distance: float | None
    pairs: tuple[FiberLiftPairAudit, ...]
    status: str


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise FiberLiftCompositionError(
            f"{name} must be finite and strictly positive"
        )
    return x


def _records(values: Sequence[object], name: str) -> tuple[np.ndarray, ...]:
    if len(values) < 2:
        raise FiberLiftCompositionError(
            f"{name} must contain at least two records"
        )
    out: list[np.ndarray] = []
    width: int | None = None
    for raw in values:
        arr = np.asarray(raw, dtype=float).reshape(-1)
        if arr.size == 0 or not np.all(np.isfinite(arr)):
            raise FiberLiftCompositionError(
                f"{name} must contain non-empty finite records"
            )
        if width is None:
            width = int(arr.size)
        elif arr.size != width:
            raise FiberLiftCompositionError(
                f"{name} records must have equal width"
            )
        out.append(arr)
    return tuple(out)


def _channels(
    channels: Mapping[str, Sequence[object]],
    count: int,
) -> dict[str, tuple[np.ndarray, ...]]:
    if not isinstance(channels, Mapping) or not channels:
        raise FiberLiftCompositionError(
            "fiber_channels must be a non-empty mapping"
        )
    out: dict[str, tuple[np.ndarray, ...]] = {}
    for raw_name in sorted(channels):
        name = str(raw_name).strip()
        if not name:
            raise FiberLiftCompositionError(
                "fiber channel names must be non-empty"
            )
        values = channels[raw_name]
        if len(values) != count:
            raise FiberLiftCompositionError(
                "each fiber channel must match candidate count"
            )
        out[name] = _records(values, f"fiber channel {name}")
    return out


def audit_finite_fiber_lift(
    latent_records: Sequence[object],
    carrier_records: Sequence[object],
    base_records: Sequence[object],
    fiber_channels: Mapping[str, Sequence[object]],
    *,
    latent_tolerance: float = 1e-8,
    carrier_tolerance: float = 1e-10,
    base_tolerance: float = 1e-10,
    fiber_tolerance: float = 1e-10,
) -> FiniteFiberLiftAudit:
    """Audit the finite-domain hypotheses of the fiber-lift composition theorem.

    The mathematical theorem used by 07R is:

        P injective and P = L o A  =>  A injective,

    where A=(Y,F) is the retained augmented observation and P is an injective
    carrier such as the ordered position lineage of 07K.

    This routine does not replace that theorem with numerical evidence.  It
    checks, on a declared finite candidate domain, whether:

    1. P separates every pair of distinct latent candidates; and
    2. A is compatible with a single-valued lift to P, i.e. no equal-A pair
       maps to two different carrier values.

    A PASS therefore certifies the theorem hypotheses only for the supplied
    finite domain and declared tolerances.
    """
    ltol = _positive(latent_tolerance, "latent_tolerance")
    ctol = _positive(carrier_tolerance, "carrier_tolerance")
    btol = _positive(base_tolerance, "base_tolerance")
    ftol = _positive(fiber_tolerance, "fiber_tolerance")

    latent = _records(latent_records, "latent_records")
    carrier = _records(carrier_records, "carrier_records")
    base = _records(base_records, "base_records")
    count = len(latent)
    if len(carrier) != count or len(base) != count:
        raise FiberLiftCompositionError(
            "latent, carrier and base records must have equal length"
        )
    channels = _channels(fiber_channels, count)

    pairs: list[FiberLiftPairAudit] = []
    distinct_pairs = 0
    carrier_collisions = 0
    augmented_collisions = 0
    lift_conflicts = 0
    min_carrier: float | None = None
    min_augmented: float | None = None

    for i in range(count):
        for j in range(i + 1, count):
            latent_distance = float(np.linalg.norm(latent[j] - latent[i]))
            if latent_distance <= ltol:
                continue
            distinct_pairs += 1

            carrier_distance = float(np.linalg.norm(carrier[j] - carrier[i]))
            base_distance = float(np.linalg.norm(base[j] - base[i]))
            fiber_distances = tuple(
                (name, float(np.linalg.norm(records[j] - records[i])))
                for name, records in channels.items()
            )
            augmented_parts = [base[j] - base[i]]
            augmented_parts.extend(
                channels[name][j] - channels[name][i]
                for name in sorted(channels)
            )
            augmented_distance = float(
                np.linalg.norm(np.concatenate(augmented_parts))
            )

            carrier_collision = carrier_distance <= ctol
            augmented_collision = (
                base_distance <= btol
                and all(distance <= ftol for _, distance in fiber_distances)
            )
            lift_conflict = augmented_collision and not carrier_collision

            if carrier_collision:
                carrier_collisions += 1
            if augmented_collision:
                augmented_collisions += 1
            if lift_conflict:
                lift_conflicts += 1

            min_carrier = (
                carrier_distance
                if min_carrier is None
                else min(min_carrier, carrier_distance)
            )
            min_augmented = (
                augmented_distance
                if min_augmented is None
                else min(min_augmented, augmented_distance)
            )
            pairs.append(
                FiberLiftPairAudit(
                    reference_index=i,
                    candidate_index=j,
                    latent_distance=latent_distance,
                    carrier_distance=carrier_distance,
                    base_distance=base_distance,
                    fiber_distances=fiber_distances,
                    augmented_collision=augmented_collision,
                    carrier_collision=carrier_collision,
                    lift_conflict=lift_conflict,
                )
            )

    if distinct_pairs == 0:
        status = "NO_DISTINCT_LATENT_PAIRS"
    elif carrier_collisions:
        status = "CARRIER_INJECTIVITY_FAIL_ON_FINITE_DOMAIN"
    elif lift_conflicts:
        status = "FUNCTIONAL_LIFT_FAIL_ON_FINITE_DOMAIN"
    else:
        status = "FINITE_DOMAIN_FIBER_LIFT_COMPOSITION_PASS"

    return FiniteFiberLiftAudit(
        candidate_count=count,
        distinct_latent_pair_count=distinct_pairs,
        carrier_collision_count=carrier_collisions,
        augmented_collision_count=augmented_collisions,
        lift_conflict_count=lift_conflicts,
        minimum_distinct_carrier_distance=min_carrier,
        minimum_distinct_augmented_distance=min_augmented,
        pairs=tuple(pairs),
        status=status,
    )
