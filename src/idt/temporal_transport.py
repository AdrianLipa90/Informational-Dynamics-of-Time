from __future__ import annotations
from typing import Iterable, Sequence
import numpy as np


class TemporalTransportError(ValueError):
    pass


def _square_operator(op, dimension=None):
    arr = np.asarray(op, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise TemporalTransportError("transport operators must be non-empty square matrices")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise TemporalTransportError("transport operators must be finite")
    if dimension is not None and arr.shape != (dimension, dimension):
        raise TemporalTransportError("all transport operators must have one common dimension")
    return arr


def ordered_event_product(event_operators, *, dimension=None):
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
        total = _square_operator(raw, dim) @ total
    return total


def interrupted_temporal_propagator(smooth_segments, event_operators):
    if len(smooth_segments) != len(event_operators) + 1:
        raise TemporalTransportError("interrupted propagation requires one more smooth segment than events")
    u0 = _square_operator(smooth_segments[0])
    dim = u0.shape[0]
    total = u0
    for event, segment in zip(event_operators, smooth_segments[1:]):
        total = _square_operator(segment, dim) @ _square_operator(event, dim) @ total
    return total


def spectral_norm(op):
    return float(np.linalg.norm(_square_operator(op), ord=2))


def interrupted_norm_bound(smooth_segments, event_operators):
    total = interrupted_temporal_propagator(smooth_segments, event_operators)
    factors = [spectral_norm(x) for x in smooth_segments] + [spectral_norm(x) for x in event_operators]
    bound = float(np.prod(factors))
    return spectral_norm(total), bound


def transport_condition_number(op):
    return float(np.linalg.cond(_square_operator(op)))


def cut_interrupted_temporal_propagator(smooth_segments, event_operators, cut_events):
    if len(smooth_segments) != len(event_operators) + 1:
        raise TemporalTransportError("interrupted propagation requires one more smooth segment than events")
    n = len(event_operators)
    c = int(cut_events)
    if c < 0 or c > n:
        raise TemporalTransportError("cut_events must lie in [0, number_of_events]")
    dim = _square_operator(smooth_segments[0]).shape[0]
    early = interrupted_temporal_propagator(smooth_segments[: c + 1], event_operators[:c])
    late = np.eye(dim, dtype=complex)
    for idx in range(c, n):
        b = _square_operator(event_operators[idx], dim)
        u = _square_operator(smooth_segments[idx + 1], dim)
        late = u @ b @ late
    return early, late
