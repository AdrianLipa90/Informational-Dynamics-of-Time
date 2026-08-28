from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .orchorbital import AttractorSpec, winding_increment, wrapped_angle_difference
from .retrodiction_global_null_gate import ScalarCheckpointObservation


class WindingRadiusPositionDecoderError(ValueError):
    pass


@dataclass(frozen=True)
class ActiveRadiusCoordinate:
    checkpoint_index: int
    value: float

    @property
    def label(self) -> str:
        return f"rho{self.checkpoint_index}"


@dataclass(frozen=True)
class PositionFiberCompressionBudget:
    event_count: int
    cartesian_baseline_scalars: int
    radial_scalars: int
    reused_winding_scalars: int
    new_scalar_ratio: float | None
    status: str


@dataclass(frozen=True)
class WindingRadiusPositionDecoderResult:
    active_sequence: tuple[str, ...]
    event_count: int
    position_lineage: np.ndarray
    radial_labels: tuple[str, ...]
    final_position_labels: tuple[str, str]
    final_winding_residual_radians: float
    budget: PositionFiberCompressionBudget
    status: str


def _finite_scalar(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise WindingRadiusPositionDecoderError(f"{name} must be a finite scalar")
    x = float(value)
    if not math.isfinite(x):
        raise WindingRadiusPositionDecoderError(f"{name} must be a finite scalar")
    return x


def _vec2(value: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.shape != (2,) or not np.all(np.isfinite(arr)):
        raise WindingRadiusPositionDecoderError(
            f"{name} must be a finite two-component vector"
        )
    return arr


def _active_sequence(values: Sequence[str]) -> tuple[str, ...]:
    sequence = tuple(str(value).strip() for value in values)
    if not sequence or any(not value for value in sequence):
        raise WindingRadiusPositionDecoderError(
            "active_sequence must contain non-empty attractor labels"
        )
    return sequence


def _attractor_map(
    attractors: Sequence[AttractorSpec],
) -> dict[str, AttractorSpec]:
    if len(attractors) == 0:
        raise WindingRadiusPositionDecoderError("attractors must be non-empty")
    mapping: dict[str, AttractorSpec] = {}
    for raw in attractors:
        if not isinstance(raw, AttractorSpec):
            raise WindingRadiusPositionDecoderError(
                "attractors must contain AttractorSpec values"
            )
        name = str(raw.name).strip()
        if not name or name in mapping:
            raise WindingRadiusPositionDecoderError(
                "attractor names must be non-empty and unique"
            )
        center = _vec2(raw.center, f"center[{name}]")
        mu = _finite_scalar(raw.mu_memory, f"mu_memory[{name}]")
        if mu <= 0.0:
            raise WindingRadiusPositionDecoderError(
                f"mu_memory[{name}] must be strictly positive"
            )
        mapping[name] = AttractorSpec(name, center.copy(), mu)
    return mapping


def _winding_values(values: Sequence[float], event_count: int) -> tuple[float, ...]:
    if len(values) != event_count:
        raise WindingRadiusPositionDecoderError(
            "winding_increments must provide one value per event"
        )
    out: list[float] = []
    for index, raw in enumerate(values, start=1):
        value = _finite_scalar(raw, f"winding[{index}]")
        if abs(value) > 0.5:
            raise WindingRadiusPositionDecoderError(
                "winding increments must lie in the wrapped interval [-0.5,0.5]"
            )
        out.append(value)
    return tuple(out)


def _radial_packet(
    radii: Sequence[ActiveRadiusCoordinate],
    event_count: int,
) -> tuple[dict[int, float], tuple[str, ...]]:
    required_count = max(0, event_count - 1)
    if len(radii) != required_count:
        raise WindingRadiusPositionDecoderError(
            "radial packet must provide exactly one active radius for each checkpoint before the final retained position"
        )
    values: dict[int, float] = {}
    labels: list[str] = []
    for raw in radii:
        if not isinstance(raw, ActiveRadiusCoordinate):
            raise WindingRadiusPositionDecoderError(
                "active_radii must contain ActiveRadiusCoordinate values"
            )
        index = int(raw.checkpoint_index)
        if index < 1 or index >= event_count:
            raise WindingRadiusPositionDecoderError(
                "active radius checkpoint_index must lie in [1,event_count-1]"
            )
        if index in values:
            raise WindingRadiusPositionDecoderError(
                f"duplicate active radius coordinate: rho{index}"
            )
        radius = _finite_scalar(raw.value, f"rho{index}")
        if radius <= 0.0:
            raise WindingRadiusPositionDecoderError(
                f"rho{index} must be strictly positive"
            )
        values[index] = radius
        labels.append(f"rho{index}")
    required = set(range(1, event_count))
    if set(values) != required:
        missing = sorted(required - set(values))
        raise WindingRadiusPositionDecoderError(
            "radial packet does not cover every pre-final checkpoint; missing: "
            + ",".join(f"rho{index}" for index in missing)
        )
    return values, tuple(labels)


def _final_position_from_base(
    observations: Sequence[ScalarCheckpointObservation],
    values: Sequence[float],
    event_count: int,
) -> tuple[np.ndarray, tuple[str, str]]:
    specs = tuple(observations)
    data = np.asarray(values, dtype=float).reshape(-1)
    if len(specs) != data.size:
        raise WindingRadiusPositionDecoderError(
            "base observation specs and values must have equal length"
        )
    if data.size == 0 or not np.all(np.isfinite(data)):
        raise WindingRadiusPositionDecoderError(
            "base observation values must be non-empty and finite"
        )

    coords: dict[str, float] = {}
    for spec, raw_value in zip(specs, data):
        if not isinstance(spec, ScalarCheckpointObservation):
            raise WindingRadiusPositionDecoderError(
                "base observations must contain ScalarCheckpointObservation values"
            )
        if spec.checkpoint_index != event_count or spec.kind not in ("rx", "ry"):
            continue
        if spec.attractor_name is not None:
            raise WindingRadiusPositionDecoderError(
                "final position observations do not accept attractor_name"
            )
        axis = "x" if spec.kind == "rx" else "y"
        label = f"r{event_count}{axis}"
        if label in coords:
            raise WindingRadiusPositionDecoderError(
                f"duplicate final base position coordinate: {label}"
            )
        coords[label] = _finite_scalar(raw_value, label)

    labels = (f"r{event_count}x", f"r{event_count}y")
    missing = tuple(label for label in labels if label not in coords)
    if missing:
        raise WindingRadiusPositionDecoderError(
            "base record must retain the complete final position; missing: "
            + ",".join(missing)
        )
    return np.asarray([coords[labels[0]], coords[labels[1]]], dtype=float), labels


def winding_radius_compression_budget(event_count: int) -> PositionFiberCompressionBudget:
    n = int(event_count)
    if n <= 0:
        raise WindingRadiusPositionDecoderError(
            "event_count must be strictly positive"
        )
    cartesian = 2 * n - 2
    radial = n - 1
    ratio = None if cartesian == 0 else radial / cartesian
    return PositionFiberCompressionBudget(
        event_count=n,
        cartesian_baseline_scalars=cartesian,
        radial_scalars=radial,
        reused_winding_scalars=n,
        new_scalar_ratio=ratio,
        status="POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED" if n > 1 else "NO_PREFINAL_POSITION_FIBER_REQUIRED",
    )


def decode_winding_radius_position_lineage(
    initial_position: Sequence[float],
    attractors: Sequence[AttractorSpec],
    active_sequence: Sequence[str],
    winding_increments: Sequence[float],
    base_observations: Sequence[ScalarCheckpointObservation],
    base_values: Sequence[float],
    active_radii: Sequence[ActiveRadiusCoordinate],
    *,
    final_winding_tolerance_radians: float = 1e-10,
) -> WindingRadiusPositionDecoderResult:
    """Decode the exact 07K position carrier from winding plus active radii.

    For checkpoints 1..N-1, the previous position, fixed active center, signed
    wrapped winding increment and post-segment active radius determine the next
    position. The final position is taken directly from the declared base record
    and the final winding is used as a consistency constraint.
    """
    sequence = _active_sequence(active_sequence)
    n = len(sequence)
    mapping = _attractor_map(attractors)
    unknown = tuple(name for name in sequence if name not in mapping)
    if unknown:
        raise WindingRadiusPositionDecoderError(
            "active_sequence contains an unknown attractor: " + ",".join(unknown)
        )
    windings = _winding_values(winding_increments, n)
    radii, radial_labels = _radial_packet(active_radii, n)
    final_position, final_labels = _final_position_from_base(
        base_observations, base_values, n
    )
    tolerance = _finite_scalar(
        final_winding_tolerance_radians, "final_winding_tolerance_radians"
    )
    if tolerance <= 0.0:
        raise WindingRadiusPositionDecoderError(
            "final_winding_tolerance_radians must be strictly positive"
        )

    previous = _vec2(initial_position, "initial_position").copy()
    positions: list[np.ndarray] = []
    for index in range(1, n):
        active = mapping[sequence[index - 1]]
        center = np.asarray(active.center, dtype=float)
        relative_previous = previous - center
        if float(np.linalg.norm(relative_previous)) <= 0.0:
            raise WindingRadiusPositionDecoderError(
                f"winding-radius decode is singular at the active center before checkpoint {index}"
            )
        theta_before = math.atan2(
            float(relative_previous[1]), float(relative_previous[0])
        )
        theta_after = theta_before + 2.0 * math.pi * windings[index - 1]
        radius = radii[index]
        next_position = center + radius * np.asarray(
            [math.cos(theta_after), math.sin(theta_after)], dtype=float
        )
        if not np.all(np.isfinite(next_position)):
            raise WindingRadiusPositionDecoderError(
                "decoded pre-final position became non-finite"
            )
        positions.append(next_position)
        previous = next_position

    final_active = mapping[sequence[-1]]
    final_center = np.asarray(final_active.center, dtype=float)
    if float(np.linalg.norm(previous - final_center)) <= 0.0:
        raise WindingRadiusPositionDecoderError(
            "final winding is singular at the active center before the final checkpoint"
        )
    if float(np.linalg.norm(final_position - final_center)) <= 0.0:
        raise WindingRadiusPositionDecoderError(
            "final retained position is singular at the active center"
        )
    try:
        actual_final_winding = winding_increment(
            previous, final_position, final_center
        )
    except ValueError as exc:
        raise WindingRadiusPositionDecoderError(str(exc)) from exc
    residual = abs(
        wrapped_angle_difference(
            2.0 * math.pi * actual_final_winding,
            2.0 * math.pi * windings[-1],
        )
    )
    if residual > tolerance:
        raise WindingRadiusPositionDecoderError(
            "final retained position is inconsistent with the declared final winding"
        )

    positions.append(final_position.copy())
    lineage = np.asarray(positions, dtype=float)
    if lineage.shape != (n, 2) or not np.all(np.isfinite(lineage)):
        raise WindingRadiusPositionDecoderError(
            "decoded position lineage must be a finite (N,2) carrier"
        )

    return WindingRadiusPositionDecoderResult(
        active_sequence=sequence,
        event_count=n,
        position_lineage=lineage,
        radial_labels=radial_labels,
        final_position_labels=final_labels,
        final_winding_residual_radians=float(residual),
        budget=winding_radius_compression_budget(n),
        status="EXACT_WINDING_RADIUS_POSITION_DECODER",
    )
