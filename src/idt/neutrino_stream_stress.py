"""Normalized ultrarelativistic neutrino-stream stress-shape helpers.

The returned spatial tensor is a dimensionless anisotropy shape
    S_ij = sum_a w_a n_i^(a) n_j^(a) / sum_a w_a,
with positive stream weights.  Physical energy-density normalization is a
separate binding.
"""

from __future__ import annotations

import math
from typing import Sequence

from .qhtri_neutrino_gravity import normalize_direction


Matrix3 = tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]


def normalized_stream_stress(
    directions: Sequence[Sequence[float]],
    weights: Sequence[float],
) -> Matrix3:
    if len(directions) == 0 or len(directions) != len(weights):
        raise ValueError("directions and weights must have equal non-zero length")
    ws = tuple(float(w) for w in weights)
    if not all(math.isfinite(w) and w >= 0.0 for w in ws):
        raise ValueError("stream weights must be finite and non-negative")
    total = sum(ws)
    if total <= 0.0:
        raise ValueError("at least one stream weight must be positive")
    ns = tuple(normalize_direction(d) for d in directions)
    return tuple(
        tuple(sum(w * n[i] * n[j] for w, n in zip(ws, ns)) / total for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def flavour_resolved_stream_stress(
    directions: Sequence[Sequence[float]],
    flavour_weights: Sequence[Sequence[float]],
) -> Matrix3:
    """Collapse non-negative per-flavour stream weights to total stream stress.

    Each row of ``flavour_weights`` belongs to one momentum direction.  The
    number of flavour columns may be arbitrary but must be common to all rows.
    """

    if len(directions) == 0 or len(directions) != len(flavour_weights):
        raise ValueError("directions and flavour_weights must have equal non-zero length")
    width = len(flavour_weights[0])
    if width == 0 or any(len(row) != width for row in flavour_weights):
        raise ValueError("flavour weight rows must have one common non-zero width")
    totals = []
    for row in flavour_weights:
        values = tuple(float(x) for x in row)
        if not all(math.isfinite(x) and x >= 0.0 for x in values):
            raise ValueError("flavour weights must be finite and non-negative")
        totals.append(sum(values))
    return normalized_stream_stress(directions, totals)


def tetrahedral_directions() -> tuple[tuple[float, float, float], ...]:
    """Four unit directions to regular-tetrahedron vertices."""

    s = 1.0 / math.sqrt(3.0)
    return (
        (s, s, s),
        (s, -s, -s),
        (-s, s, -s),
        (-s, -s, s),
    )
