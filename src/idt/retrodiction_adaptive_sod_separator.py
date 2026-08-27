from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .retrodiction_spatial_offset_divergence import spatial_offset_lineage


class AdaptiveSODSeparatorError(ValueError):
    pass


@dataclass(frozen=True)
class AdaptiveSODSeparator:
    label: str
    checkpoint_index: int
    axis_index: int
    signed_offset: float
    magnitude: float
    status: str


def _positive(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise AdaptiveSODSeparatorError(f"{name} must be finite and strictly positive")
    return x


def select_max_sod_separator(reference_positions, candidate_positions, *, spatial_tolerance: float = 1e-9) -> AdaptiveSODSeparator:
    """Select the largest retained-coordinate separator from an SOD witness."""
    tol = _positive(spatial_tolerance, "spatial_tolerance")
    try:
        offsets = spatial_offset_lineage(reference_positions, candidate_positions)
    except ValueError as exc:
        raise AdaptiveSODSeparatorError(str(exc)) from exc
    magnitudes = np.abs(offsets).reshape(-1)
    if not np.all(np.isfinite(magnitudes)):
        raise AdaptiveSODSeparatorError("SOD offsets must be finite")
    max_value = float(np.max(magnitudes))
    if max_value <= tol:
        raise AdaptiveSODSeparatorError("no spatial component exceeds the declared tolerance")
    flat_index = int(np.flatnonzero(magnitudes == max_value)[0])
    checkpoint_index = flat_index // 2
    axis_index = flat_index % 2
    axis = "x" if axis_index == 0 else "y"
    signed = float(offsets[checkpoint_index, axis_index])
    return AdaptiveSODSeparator(
        label=f"r{checkpoint_index + 1}{axis}",
        checkpoint_index=checkpoint_index + 1,
        axis_index=axis_index,
        signed_offset=signed,
        magnitude=abs(signed),
        status="KNOWN_SOD_SEPARATOR_SELECTED",
    )


def augment_sparse_record(record, positions, separator: AdaptiveSODSeparator) -> np.ndarray:
    values = np.asarray(record, dtype=float).reshape(-1)
    pos = np.asarray(positions, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)):
        raise AdaptiveSODSeparatorError("record must be a non-empty finite vector")
    if pos.ndim != 2 or pos.shape[1] != 2 or not np.all(np.isfinite(pos)):
        raise AdaptiveSODSeparatorError("positions must be a finite (N,2) matrix")
    if not isinstance(separator, AdaptiveSODSeparator):
        raise AdaptiveSODSeparatorError("separator must be AdaptiveSODSeparator")
    idx = int(separator.checkpoint_index) - 1
    axis = int(separator.axis_index)
    if idx < 0 or idx >= pos.shape[0] or axis not in (0, 1):
        raise AdaptiveSODSeparatorError("separator is outside the position lineage")
    return np.concatenate((values, [float(pos[idx, axis])]))
