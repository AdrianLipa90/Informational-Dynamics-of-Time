from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .retrodiction_global_null_gate import ScalarCheckpointObservation


class PerStratumPositionDecoderError(ValueError):
    pass


@dataclass(frozen=True)
class PositionFiberCoordinate:
    checkpoint_index: int
    axis: str
    value: float

    @property
    def label(self) -> str:
        return f"r{self.checkpoint_index}{self.axis}"


@dataclass(frozen=True)
class PerStratumPositionDecoderResult:
    active_sequence: tuple[str, ...]
    event_count: int
    position_lineage: np.ndarray
    base_position_labels: tuple[str, ...]
    fiber_position_labels: tuple[str, ...]
    required_position_labels: tuple[str, ...]
    status: str


def _active_sequence(values: Sequence[str]) -> tuple[str, ...]:
    sequence = tuple(str(value).strip() for value in values)
    if not sequence or any(not value for value in sequence):
        raise PerStratumPositionDecoderError(
            "active_sequence must contain non-empty attractor labels"
        )
    return sequence


def _finite_scalar(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise PerStratumPositionDecoderError(f"{name} must be a finite scalar")
    x = float(value)
    if not math.isfinite(x):
        raise PerStratumPositionDecoderError(f"{name} must be a finite scalar")
    return x


def _position_label(checkpoint_index: int, axis: str, event_count: int) -> str:
    idx = int(checkpoint_index)
    ax = str(axis).strip().lower()
    if idx <= 0 or idx > event_count:
        raise PerStratumPositionDecoderError(
            "position checkpoint_index must lie in [1,event_count]"
        )
    if ax not in ("x", "y"):
        raise PerStratumPositionDecoderError("position axis must be x or y")
    return f"r{idx}{ax}"


def required_position_labels(event_count: int) -> tuple[str, ...]:
    n = int(event_count)
    if n <= 0:
        raise PerStratumPositionDecoderError("event_count must be strictly positive")
    return tuple(
        f"r{k}{axis}"
        for k in range(1, n + 1)
        for axis in ("x", "y")
    )


def _base_position_coordinates(
    observations: Sequence[ScalarCheckpointObservation],
    values: Sequence[float],
    event_count: int,
) -> tuple[dict[str, float], tuple[str, ...]]:
    specs = tuple(observations)
    data = np.asarray(values, dtype=float).reshape(-1)
    if len(specs) != data.size:
        raise PerStratumPositionDecoderError(
            "base observation specs and values must have equal length"
        )
    if data.size == 0 or not np.all(np.isfinite(data)):
        raise PerStratumPositionDecoderError(
            "base observation values must be non-empty and finite"
        )

    coordinates: dict[str, float] = {}
    labels: list[str] = []
    for spec, raw_value in zip(specs, data):
        if not isinstance(spec, ScalarCheckpointObservation):
            raise PerStratumPositionDecoderError(
                "base observations must contain ScalarCheckpointObservation values"
            )
        kind = str(spec.kind).strip()
        if kind not in ("rx", "ry"):
            continue
        if spec.attractor_name is not None:
            raise PerStratumPositionDecoderError(
                "position observations do not accept attractor_name"
            )
        axis = "x" if kind == "rx" else "y"
        label = _position_label(spec.checkpoint_index, axis, event_count)
        if label in coordinates:
            raise PerStratumPositionDecoderError(
                f"duplicate base position coordinate: {label}"
            )
        coordinates[label] = _finite_scalar(raw_value, label)
        labels.append(label)
    return coordinates, tuple(labels)


def _fiber_position_coordinates(
    fibers: Sequence[PositionFiberCoordinate],
    event_count: int,
) -> tuple[dict[str, float], tuple[str, ...]]:
    coordinates: dict[str, float] = {}
    labels: list[str] = []
    for fiber in fibers:
        if not isinstance(fiber, PositionFiberCoordinate):
            raise PerStratumPositionDecoderError(
                "position_fibers must contain PositionFiberCoordinate values"
            )
        label = _position_label(fiber.checkpoint_index, fiber.axis, event_count)
        if label in coordinates:
            raise PerStratumPositionDecoderError(
                f"duplicate position fiber coordinate: {label}"
            )
        coordinates[label] = _finite_scalar(fiber.value, label)
        labels.append(label)
    return coordinates, tuple(labels)


def missing_position_fiber_labels(
    active_sequence: Sequence[str],
    base_observations: Sequence[ScalarCheckpointObservation],
    base_values: Sequence[float],
) -> tuple[str, ...]:
    """Return the exact absolute position coordinates absent from the base record."""
    sequence = _active_sequence(active_sequence)
    base, _ = _base_position_coordinates(
        base_observations, base_values, len(sequence)
    )
    return tuple(
        label for label in required_position_labels(len(sequence)) if label not in base
    )


def decode_per_stratum_position_lineage(
    active_sequence: Sequence[str],
    base_observations: Sequence[ScalarCheckpointObservation],
    base_values: Sequence[float],
    position_fibers: Sequence[PositionFiberCoordinate],
) -> PerStratumPositionDecoderResult:
    """Assemble the exact ordered position carrier from retained coordinates.

    The active sequence fixes the 07S stratum. Position coordinates already
    retained by the base observation and explicitly retained absolute position
    fiber coordinates are combined by label. Exact coverage of every r_kx/r_ky
    coordinate is required before the 07K carrier is emitted.
    """
    sequence = _active_sequence(active_sequence)
    n = len(sequence)
    required = required_position_labels(n)
    base, base_labels = _base_position_coordinates(
        base_observations, base_values, n
    )
    fibers, fiber_labels = _fiber_position_coordinates(position_fibers, n)

    overlap = tuple(label for label in fiber_labels if label in base)
    if overlap:
        raise PerStratumPositionDecoderError(
            "position coordinate supplied by both base record and fiber packet: "
            + ",".join(overlap)
        )

    combined = dict(base)
    combined.update(fibers)
    missing = tuple(label for label in required if label not in combined)
    if missing:
        raise PerStratumPositionDecoderError(
            "position fiber packet does not cover the complete 07K carrier; missing: "
            + ",".join(missing)
        )
    extras = tuple(label for label in combined if label not in required)
    if extras:
        raise PerStratumPositionDecoderError(
            "position coordinate lies outside the declared stratum carrier"
        )

    positions = np.empty((n, 2), dtype=float)
    for k in range(1, n + 1):
        positions[k - 1, 0] = combined[f"r{k}x"]
        positions[k - 1, 1] = combined[f"r{k}y"]
    if not np.all(np.isfinite(positions)):
        raise PerStratumPositionDecoderError(
            "decoded position lineage must be finite"
        )

    return PerStratumPositionDecoderResult(
        active_sequence=sequence,
        event_count=n,
        position_lineage=positions,
        base_position_labels=base_labels,
        fiber_position_labels=fiber_labels,
        required_position_labels=required,
        status="EXACT_PER_STRATUM_POSITION_DECODER",
    )
