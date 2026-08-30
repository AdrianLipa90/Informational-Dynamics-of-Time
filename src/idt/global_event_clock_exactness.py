"""Exact discrete event-clock reconstruction from positive elapsed edge weights.

This module implements the 05H graph-cohomology gate. It reconstructs a scalar
potential t on event vertices when the signed elapsed one-cochain has zero period
on every cycle. Conflicting path integrals fail closed as temporal holonomy.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence


class TemporalExactnessError(ValueError):
    """Raised when an event graph cannot support one exact scalar clock."""


@dataclass(frozen=True)
class EventEdge:
    source: str
    target: str
    dtheta: float

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source:
            raise TemporalExactnessError("edge source must be a non-empty string")
        if not isinstance(self.target, str) or not self.target:
            raise TemporalExactnessError("edge target must be a non-empty string")
        if self.source == self.target:
            raise TemporalExactnessError("positive elapsed self-loop is inconsistent")
        value = float(self.dtheta)
        if not isfinite(value) or value <= 0.0:
            raise TemporalExactnessError("elapsed edge weight must be finite and positive")
        object.__setattr__(self, "dtheta", value)


@dataclass(frozen=True)
class ExactnessCertificate:
    exact: bool
    potentials: dict[str, float]
    component_count: int
    max_residual: float
    production_input_status: str = "OPEN_INPUT"


def _close(a: float, b: float, atol: float) -> bool:
    scale = 1.0 + max(abs(a), abs(b))
    return abs(a - b) <= atol * scale


def _normalize_vertices(edges: Sequence[EventEdge], vertices: Iterable[str] | None) -> tuple[str, ...]:
    names: set[str] = set()
    if vertices is not None:
        for vertex in vertices:
            if not isinstance(vertex, str) or not vertex:
                raise TemporalExactnessError("vertices must be non-empty strings")
            names.add(vertex)
    for edge in edges:
        names.add(edge.source)
        names.add(edge.target)
    if not names:
        raise TemporalExactnessError("event graph must contain at least one vertex")
    return tuple(sorted(names))


def certify_event_clock(
    edges: Sequence[EventEdge],
    *,
    vertices: Iterable[str] | None = None,
    require_connected: bool = True,
    atol: float = 1.0e-12,
) -> ExactnessCertificate:
    """Reconstruct an exact scalar event clock or fail on temporal holonomy.

    Every directed edge ``u -> v`` imposes ``t[v] - t[u] = dtheta > 0``.
    The traversal uses the underlying undirected graph and therefore compares all
    alternative path integrals. Potentials are rooted at zero independently on
    each connected component; on a connected graph the result is unique up to one
    additive constant.
    """

    if not isfinite(float(atol)) or atol < 0.0:
        raise TemporalExactnessError("atol must be finite and non-negative")

    edge_list = tuple(edges)
    for edge in edge_list:
        if not isinstance(edge, EventEdge):
            raise TemporalExactnessError("all edges must be EventEdge instances")

    vertex_list = _normalize_vertices(edge_list, vertices)
    adjacency: dict[str, list[tuple[str, float]]] = {vertex: [] for vertex in vertex_list}
    for edge in edge_list:
        adjacency[edge.source].append((edge.target, edge.dtheta))
        adjacency[edge.target].append((edge.source, -edge.dtheta))

    potentials: dict[str, float] = {}
    component_count = 0

    for root in vertex_list:
        if root in potentials:
            continue
        component_count += 1
        potentials[root] = 0.0
        queue: deque[str] = deque([root])

        while queue:
            current = queue.popleft()
            t_current = potentials[current]
            for neighbor, signed_increment in adjacency[current]:
                candidate = t_current + signed_increment
                if neighbor not in potentials:
                    potentials[neighbor] = candidate
                    queue.append(neighbor)
                    continue
                if not _close(potentials[neighbor], candidate, atol):
                    defect = candidate - potentials[neighbor]
                    raise TemporalExactnessError(
                        "temporal holonomy defect: conflicting path integral for "
                        f"vertex {neighbor!r}; defect={defect:.17g}"
                    )

    if require_connected and component_count != 1:
        raise TemporalExactnessError(
            f"connected-domain certificate requested for {component_count} components"
        )

    max_residual = 0.0
    for edge in edge_list:
        residual = (potentials[edge.target] - potentials[edge.source]) - edge.dtheta
        max_residual = max(max_residual, abs(residual))
        if not _close(residual, 0.0, atol):
            raise TemporalExactnessError(
                "reconstructed scalar violates directed edge equation: "
                f"{edge.source!r}->{edge.target!r}, residual={residual:.17g}"
            )

    return ExactnessCertificate(
        exact=True,
        potentials=dict(sorted(potentials.items())),
        component_count=component_count,
        max_residual=max_residual,
    )
