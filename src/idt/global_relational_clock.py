from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from typing import Hashable, Iterable


class GlobalClockCocycleError(ValueError):
    pass


@dataclass(frozen=True)
class GlobalClockCertificate:
    reference: Hashable
    relative_rates: dict[Hashable, float]
    max_relative_residual: float


def reconstruct_global_clock_potential(
    edges: Iterable[tuple[Hashable, Hashable, float]],
    *,
    reference: Hashable | None = None,
    tolerance: float = 1e-10,
) -> GlobalClockCertificate:
    """Reconstruct positive rates from edges (x, y, N_x_given_y)."""
    edge_list = list(edges)
    if not edge_list:
        raise GlobalClockCocycleError("at least one clock-ratio edge is required")
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise GlobalClockCocycleError("tolerance must be finite and positive")

    nodes: set[Hashable] = set()
    adjacency: dict[Hashable, list[tuple[Hashable, float]]] = {}
    clean_edges: list[tuple[Hashable, Hashable, float]] = []

    for x, y, ratio_raw in edge_list:
        ratio = float(ratio_raw)
        if not math.isfinite(ratio) or ratio <= 0.0:
            raise GlobalClockCocycleError("clock ratios must be finite and strictly positive")
        nodes.update((x, y))
        adjacency.setdefault(x, [])
        adjacency.setdefault(y, [])
        clean_edges.append((x, y, ratio))

        if x == y:
            if abs(ratio - 1.0) > tolerance:
                raise GlobalClockCocycleError("self-ratio must equal one")
            continue

        # N_x|y = a_x/a_y.  From y to x multiply by ratio;
        # from x to y multiply by its reciprocal.
        adjacency[y].append((x, ratio))
        adjacency[x].append((y, 1.0 / ratio))

    if reference is None:
        reference = sorted(nodes, key=lambda value: str(value))[0]
    if reference not in nodes:
        raise GlobalClockCocycleError("reference clock must occur in the graph")

    rates: dict[Hashable, float] = {reference: 1.0}
    queue = deque([reference])
    max_residual = 0.0

    while queue:
        source = queue.popleft()
        source_rate = rates[source]
        for target, factor in adjacency[source]:
            candidate = source_rate * factor
            if target not in rates:
                rates[target] = candidate
                queue.append(target)
                continue

            scale = max(1.0, abs(rates[target]), abs(candidate))
            residual = abs(rates[target] - candidate) / scale
            max_residual = max(max_residual, residual)
            if residual > tolerance:
                raise GlobalClockCocycleError("multiplicative cycle closure failed")

    if len(rates) != len(nodes):
        raise GlobalClockCocycleError("clock graph is disconnected")

    for x, y, ratio in clean_edges:
        predicted = rates[x] / rates[y]
        scale = max(1.0, abs(predicted), abs(ratio))
        residual = abs(predicted - ratio) / scale
        max_residual = max(max_residual, residual)
        if residual > tolerance:
            raise GlobalClockCocycleError("edge ratio is incompatible with global potential")

    if any((not math.isfinite(rate) or rate <= 0.0) for rate in rates.values()):
        raise GlobalClockCocycleError("reconstructed global clock rates lost positive orientation")

    return GlobalClockCertificate(reference, rates, max_residual)


def ratio_from_certificate(certificate: GlobalClockCertificate, x: Hashable, y: Hashable) -> float:
    return certificate.relative_rates[x] / certificate.relative_rates[y]


def log_potential(certificate: GlobalClockCertificate) -> dict[Hashable, float]:
    return {node: math.log(rate) for node, rate in certificate.relative_rates.items()}


def common_rate_rescaling(certificate: GlobalClockCertificate, scale: float) -> dict[Hashable, float]:
    scale = float(scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise GlobalClockCocycleError("common scale must be finite and positive")
    return {node: scale * rate for node, rate in certificate.relative_rates.items()}
