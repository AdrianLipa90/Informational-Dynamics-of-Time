from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np


class TemporalTransportError(ValueError):
    pass


def _square_operator(op: Sequence[Sequence[complex]], dimension: int | None = None) -> np.ndarray:
    arr = np.asarray(op, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise TemporalTransportError("transport operators must be non-empty square matrices")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise TemporalTransportError("transport operators must be finite")
    if dimension is not None and arr.shape != (dimension, dimension):
        raise TemporalTransportError("all transport operators must have one common dimension")
    return arr


def ordered_event_product(event_operators: Iterable[Sequence[Sequence[complex]]], *, dimension: int | None = None) -> np.ndarray:
    ops = list(event_operators)
    if not ops:
        if dimension is None or dimension <= 0:
            raise TemporalTransportError("empty event sequence requires a positive dimension")
        return np.eye(dimension, dtype=complex)
    first = _square_operator(ops[0])
    dim = first.shape[0]
    if dimension is not None and dim != dimension:
        raise TemporalTransportError("declared dimension does not match event operators")
    total = np.eye(dim, dtype=complex)
    for raw in ops:
        op = _square_operator(raw, dim)
        total = op @ total
    return total


def interrupted_temporal_propagator(smooth_segments: Sequence[Sequence[Sequence[complex]]], event_operators: Sequence[Sequence[Sequence[complex]]]) -> np.ndarray:
    if len(smooth_segments) != len(event_operators) + 1:
        raise TemporalTransportError("interrupted propagation requires one more smooth segment than events")
    u0 = _square_operator(smooth_segments[0])
    dim = u0.shape[0]
    total = u0
    for event, segment in zip(event_operators, smooth_segments[1:]):
        b = _square_operator(event, dim)
        u = _square_operator(segment, dim)
        total = u @ b @ total
    return total
