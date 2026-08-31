"""Fail-closed certification of a regular smooth clock on a declared affine atlas.

Gate 05I consumes a discrete exact event clock from 05H together with an admitted
affine-atlas witness. Local affine clock functions are checked for non-vanishing
differential, exact overlap compatibility, chart connectivity, and agreement with
the discrete event clock up to the single additive constant left free by 05H.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Mapping, Sequence

import numpy as np


class RegularClockExtensionError(ValueError):
    """Raised when the supplied continuum clock witness fails the 05I gate."""


def _finite_scalar(value: float, label: str) -> float:
    result = float(value)
    if not isfinite(result):
        raise RegularClockExtensionError(f"{label} must be finite")
    return result


def _finite_vector(values: Sequence[float], label: str) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if not result:
        raise RegularClockExtensionError(f"{label} must be non-empty")
    if not all(isfinite(value) for value in result):
        raise RegularClockExtensionError(f"{label} must contain only finite values")
    return result


@dataclass(frozen=True)
class AffineClockChart:
    name: str
    gradient: tuple[float, ...]
    offset: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise RegularClockExtensionError("chart name must be a non-empty string")
        object.__setattr__(self, "gradient", _finite_vector(self.gradient, "chart gradient"))
        object.__setattr__(self, "offset", _finite_scalar(self.offset, "chart offset"))

    @property
    def dimension(self) -> int:
        return len(self.gradient)

    def evaluate(self, point: Sequence[float]) -> float:
        coordinates = _finite_vector(point, "chart point")
        if len(coordinates) != self.dimension:
            raise RegularClockExtensionError(
                f"chart {self.name!r} expects dimension {self.dimension}, got {len(coordinates)}"
            )
        return float(np.dot(np.asarray(self.gradient), np.asarray(coordinates)) + self.offset)


@dataclass(frozen=True)
class AffineTransition:
    source: str
    target: str
    matrix: tuple[tuple[float, ...], ...]
    shift: tuple[float, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source:
            raise RegularClockExtensionError("transition source must be a non-empty string")
        if not isinstance(self.target, str) or not self.target:
            raise RegularClockExtensionError("transition target must be a non-empty string")
        if self.source == self.target:
            raise RegularClockExtensionError("transition must connect distinct charts")
        rows = tuple(_finite_vector(row, "transition matrix row") for row in self.matrix)
        if not rows:
            raise RegularClockExtensionError("transition matrix must be non-empty")
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise RegularClockExtensionError("transition matrix rows must have equal length")
        object.__setattr__(self, "matrix", rows)
        object.__setattr__(self, "shift", _finite_vector(self.shift, "transition shift"))


@dataclass(frozen=True)
class EventAnchor:
    event_id: str
    chart: str
    point: tuple[float, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.event_id, str) or not self.event_id:
            raise RegularClockExtensionError("event_id must be a non-empty string")
        if not isinstance(self.chart, str) or not self.chart:
            raise RegularClockExtensionError("anchor chart must be a non-empty string")
        object.__setattr__(self, "point", _finite_vector(self.point, "anchor point"))


@dataclass(frozen=True)
class RegularClockExtensionCertificate:
    regular: bool
    dimension: int
    chart_count: int
    transition_count: int
    anchor_count: int
    connected: bool
    min_gradient_norm: float
    min_transition_singular_value: float
    max_overlap_linear_residual: float
    max_overlap_offset_residual: float
    max_anchor_residual: float
    calibration_offset: float
    scope: str = "DECLARED_AFFINE_ATLAS_WITNESS"
    production_input_status: str = "OPEN_INPUT"


def _close_array(left: np.ndarray, right: np.ndarray, atol: float) -> bool:
    scale = 1.0 + max(float(np.max(np.abs(left))), float(np.max(np.abs(right))))
    return bool(np.max(np.abs(left - right)) <= atol * scale)


def _close_scalar(left: float, right: float, atol: float) -> bool:
    scale = 1.0 + max(abs(left), abs(right))
    return abs(left - right) <= atol * scale


def certify_regular_affine_clock_extension(
    charts: Sequence[AffineClockChart],
    transitions: Sequence[AffineTransition],
    anchors: Sequence[EventAnchor],
    event_potentials: Mapping[str, float],
    *,
    require_connected: bool = True,
    require_all_events_anchored: bool = True,
    atol: float = 1.0e-12,
    regularity_floor: float = 1.0e-12,
    invertibility_floor: float = 1.0e-12,
) -> RegularClockExtensionCertificate:
    """Certify a smooth regular clock on a supplied affine-atlas witness.

    A chart carries ``t_A(x)=g_A.x+b_A``.  A transition ``A -> B`` carries
    ``x_B=M_BA x_A+c_BA``.  Global clock compatibility on that overlap is the
    affine identity ``g_B M_BA=g_A`` and ``g_B.c_BA+b_B=b_A``.

    The event anchors bind this continuum clock to the exact 05H vertex potential.
    Since the 05H potential is unique only up to an additive constant, every anchor
    is required to share one common calibration offset.
    """

    atol = _finite_scalar(atol, "atol")
    regularity_floor = _finite_scalar(regularity_floor, "regularity_floor")
    invertibility_floor = _finite_scalar(invertibility_floor, "invertibility_floor")
    if atol < 0.0 or regularity_floor <= 0.0 or invertibility_floor <= 0.0:
        raise RegularClockExtensionError("tolerances must satisfy atol>=0 and floors>0")

    chart_list = tuple(charts)
    if not chart_list:
        raise RegularClockExtensionError("at least one affine clock chart is required")
    if any(not isinstance(chart, AffineClockChart) for chart in chart_list):
        raise RegularClockExtensionError("all charts must be AffineClockChart instances")

    chart_map: dict[str, AffineClockChart] = {}
    for chart in chart_list:
        if chart.name in chart_map:
            raise RegularClockExtensionError(f"duplicate chart name {chart.name!r}")
        chart_map[chart.name] = chart

    dimensions = {chart.dimension for chart in chart_list}
    if len(dimensions) != 1:
        raise RegularClockExtensionError("all charts in one atlas must have the same dimension")
    dimension = next(iter(dimensions))

    gradient_norms: list[float] = []
    for chart in chart_list:
        norm = float(np.linalg.norm(np.asarray(chart.gradient, dtype=float)))
        gradient_norms.append(norm)
        if norm <= regularity_floor:
            raise RegularClockExtensionError(
                f"chart {chart.name!r} has vanishing/under-resolved clock differential; norm={norm:.17g}"
            )

    adjacency: dict[str, set[str]] = {name: set() for name in chart_map}
    singular_values: list[float] = []
    max_linear_residual = 0.0
    max_offset_residual = 0.0

    transition_list = tuple(transitions)
    for transition in transition_list:
        if not isinstance(transition, AffineTransition):
            raise RegularClockExtensionError("all transitions must be AffineTransition instances")
        if transition.source not in chart_map or transition.target not in chart_map:
            raise RegularClockExtensionError("transition references an unknown chart")

        matrix = np.asarray(transition.matrix, dtype=float)
        shift = np.asarray(transition.shift, dtype=float)
        if matrix.shape != (dimension, dimension):
            raise RegularClockExtensionError(
                f"transition {transition.source!r}->{transition.target!r} matrix must be "
                f"{dimension}x{dimension}"
            )
        if shift.shape != (dimension,):
            raise RegularClockExtensionError(
                f"transition {transition.source!r}->{transition.target!r} shift has wrong dimension"
            )

        svals = np.linalg.svd(matrix, compute_uv=False)
        sigma_min = float(np.min(svals))
        singular_values.append(sigma_min)
        if sigma_min <= invertibility_floor:
            raise RegularClockExtensionError(
                f"transition {transition.source!r}->{transition.target!r} is singular/under-resolved; "
                f"sigma_min={sigma_min:.17g}"
            )

        source_chart = chart_map[transition.source]
        target_chart = chart_map[transition.target]
        g_source = np.asarray(source_chart.gradient, dtype=float)
        g_target = np.asarray(target_chart.gradient, dtype=float)

        transformed_gradient = g_target @ matrix
        linear_residual = float(np.max(np.abs(transformed_gradient - g_source)))
        max_linear_residual = max(max_linear_residual, linear_residual)
        if not _close_array(transformed_gradient, g_source, atol):
            raise RegularClockExtensionError(
                f"clock gradient mismatch on overlap {transition.source!r}->{transition.target!r}; "
                f"residual={linear_residual:.17g}"
            )

        transformed_offset = float(np.dot(g_target, shift) + target_chart.offset)
        offset_residual = abs(transformed_offset - source_chart.offset)
        max_offset_residual = max(max_offset_residual, offset_residual)
        if not _close_scalar(transformed_offset, source_chart.offset, atol):
            raise RegularClockExtensionError(
                f"clock offset mismatch on overlap {transition.source!r}->{transition.target!r}; "
                f"residual={offset_residual:.17g}"
            )

        adjacency[transition.source].add(transition.target)
        adjacency[transition.target].add(transition.source)

    visited: set[str] = set()
    stack = [next(iter(chart_map))]
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        stack.extend(adjacency[current] - visited)
    connected = len(visited) == len(chart_map)
    if require_connected and not connected:
        raise RegularClockExtensionError("connected-domain certificate requested for disconnected chart atlas")

    potentials = {event_id: _finite_scalar(value, f"event potential {event_id!r}") for event_id, value in event_potentials.items()}
    if not potentials:
        raise RegularClockExtensionError("05H event_potentials must contain at least one event")

    anchor_list = tuple(anchors)
    if not anchor_list:
        raise RegularClockExtensionError("at least one event anchor is required")
    if any(not isinstance(anchor, EventAnchor) for anchor in anchor_list):
        raise RegularClockExtensionError("all anchors must be EventAnchor instances")

    anchored_events: set[str] = set()
    calibration_offset: float | None = None
    max_anchor_residual = 0.0
    for anchor in anchor_list:
        if anchor.chart not in chart_map:
            raise RegularClockExtensionError(f"anchor references unknown chart {anchor.chart!r}")
        if anchor.event_id not in potentials:
            raise RegularClockExtensionError(f"anchor references unknown 05H event {anchor.event_id!r}")
        chart_value = chart_map[anchor.chart].evaluate(anchor.point)
        candidate_offset = chart_value - potentials[anchor.event_id]
        if calibration_offset is None:
            calibration_offset = candidate_offset
        residual = abs(candidate_offset - calibration_offset)
        max_anchor_residual = max(max_anchor_residual, residual)
        if not _close_scalar(candidate_offset, calibration_offset, atol):
            raise RegularClockExtensionError(
                f"event anchor {anchor.event_id!r} disagrees with common 05H additive calibration; "
                f"residual={residual:.17g}"
            )
        anchored_events.add(anchor.event_id)

    if require_all_events_anchored:
        missing = sorted(set(potentials) - anchored_events)
        if missing:
            raise RegularClockExtensionError(
                f"global event-clock binding requested but events lack continuum anchors: {missing}"
            )

    return RegularClockExtensionCertificate(
        regular=True,
        dimension=dimension,
        chart_count=len(chart_list),
        transition_count=len(transition_list),
        anchor_count=len(anchor_list),
        connected=connected,
        min_gradient_norm=min(gradient_norms),
        min_transition_singular_value=min(singular_values) if singular_values else float("inf"),
        max_overlap_linear_residual=max_linear_residual,
        max_overlap_offset_residual=max_offset_residual,
        max_anchor_residual=max_anchor_residual,
        calibration_offset=float(calibration_offset),
    )
