from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


class QuotientFiberInjectivityError(ValueError):
    pass


@dataclass(frozen=True)
class FiberCollisionAudit:
    reference_index: int
    candidate_index: int
    base_distance: float
    latent_distance: float
    augmented_distance: float
    separating_channels: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class FiniteFiberInjectivityAudit:
    candidate_count: int
    distinct_latent_pair_count: int
    base_collision_count: int
    separated_collision_count: int
    unresolved_collision_count: int
    minimum_augmented_collision_distance: float | None
    collisions: tuple[FiberCollisionAudit, ...]
    status: str


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise QuotientFiberInjectivityError(
            f"{name} must be finite and strictly positive"
        )
    return x


def _records(values: Sequence[object], name: str) -> tuple[np.ndarray, ...]:
    if len(values) < 2:
        raise QuotientFiberInjectivityError(
            f"{name} must contain at least two records"
        )
    out: list[np.ndarray] = []
    width: int | None = None
    for raw in values:
        arr = np.asarray(raw, dtype=float).reshape(-1)
        if arr.size == 0 or not np.all(np.isfinite(arr)):
            raise QuotientFiberInjectivityError(
                f"{name} must contain non-empty finite records"
            )
        if width is None:
            width = int(arr.size)
        elif arr.size != width:
            raise QuotientFiberInjectivityError(
                f"{name} records must have equal width"
            )
        out.append(arr)
    return tuple(out)


def _fiber_channels(
    channels: Mapping[str, Sequence[object]],
    count: int,
) -> dict[str, tuple[np.ndarray, ...]]:
    if not isinstance(channels, Mapping) or not channels:
        raise QuotientFiberInjectivityError(
            "fiber_channels must be a non-empty mapping"
        )
    out: dict[str, tuple[np.ndarray, ...]] = {}
    for raw_name in sorted(channels):
        name = str(raw_name).strip()
        if not name:
            raise QuotientFiberInjectivityError(
                "fiber channel names must be non-empty"
            )
        values = channels[raw_name]
        if len(values) != count:
            raise QuotientFiberInjectivityError(
                "each fiber channel must match candidate count"
            )
        out[name] = _records(values, f"fiber channel {name}")
    return out


def audit_finite_quotient_fiber_injectivity(
    base_records: Sequence[object],
    latent_records: Sequence[object],
    fiber_channels: Mapping[str, Sequence[object]],
    *,
    base_tolerance: float = 1e-10,
    latent_tolerance: float = 1e-8,
    fiber_tolerance: float = 1e-10,
) -> FiniteFiberInjectivityAudit:
    """Audit declared fiber separation for every base collision on a finite domain.

    For each pair of distinct latent candidates whose base projections agree
    within ``base_tolerance``, at least one declared fiber channel must differ
    by more than ``fiber_tolerance`` for the finite candidate domain to pass.
    """
    btol = _positive(base_tolerance, "base_tolerance")
    ltol = _positive(latent_tolerance, "latent_tolerance")
    ftol = _positive(fiber_tolerance, "fiber_tolerance")
    base = _records(base_records, "base_records")
    latent = _records(latent_records, "latent_records")
    if len(base) != len(latent):
        raise QuotientFiberInjectivityError(
            "base_records and latent_records must have equal length"
        )
    channels = _fiber_channels(fiber_channels, len(base))

    collisions: list[FiberCollisionAudit] = []
    distinct_latent_pairs = 0
    separated = 0
    unresolved = 0
    min_augmented: float | None = None

    for i in range(len(base)):
        for j in range(i + 1, len(base)):
            latent_distance = float(np.linalg.norm(latent[j] - latent[i]))
            if latent_distance <= ltol:
                continue
            distinct_latent_pairs += 1
            base_distance = float(np.linalg.norm(base[j] - base[i]))
            if base_distance > btol:
                continue

            channel_distances: dict[str, float] = {}
            augmented_parts = [base[j] - base[i]]
            for name, records in channels.items():
                delta = records[j] - records[i]
                distance = float(np.linalg.norm(delta))
                channel_distances[name] = distance
                augmented_parts.append(delta)
            augmented = np.concatenate(augmented_parts)
            augmented_distance = float(np.linalg.norm(augmented))
            separating = tuple(
                name
                for name in sorted(channel_distances)
                if channel_distances[name] > ftol
            )
            is_separated = bool(separating)
            if is_separated:
                separated += 1
                status = "COLLISION_FIBER_SEPARATED"
            else:
                unresolved += 1
                status = "COLLISION_PERSISTS_IN_DECLARED_FIBER"
            min_augmented = (
                augmented_distance
                if min_augmented is None
                else min(min_augmented, augmented_distance)
            )
            collisions.append(
                FiberCollisionAudit(
                    reference_index=i,
                    candidate_index=j,
                    base_distance=base_distance,
                    latent_distance=latent_distance,
                    augmented_distance=augmented_distance,
                    separating_channels=separating,
                    status=status,
                )
            )

    if not collisions:
        status = "NO_BASE_COLLISIONS_IN_FINITE_DOMAIN"
    elif unresolved == 0:
        status = "FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER"
    else:
        status = "FINITE_DOMAIN_COLLISIONS_PERSIST"

    return FiniteFiberInjectivityAudit(
        candidate_count=len(base),
        distinct_latent_pair_count=distinct_latent_pairs,
        base_collision_count=len(collisions),
        separated_collision_count=separated,
        unresolved_collision_count=unresolved,
        minimum_augmented_collision_distance=min_augmented,
        collisions=tuple(collisions),
        status=status,
    )
