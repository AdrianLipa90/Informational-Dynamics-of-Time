from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .seam_phase_offset_intrinsic_duration import KAPPA


class TemporalOffsetReferenceClockError(ValueError):
    pass


@dataclass(frozen=True)
class ReferenceClockCocycleAudit:
    direct_target_rate: np.ndarray
    transformed_target_rate: np.ndarray
    neutral_curvature_from_source: np.ndarray
    neutral_curvature_from_target: np.ndarray
    max_rate_residual: float
    max_neutral_residual: float


def _positive_rate(value: float, *, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise TemporalOffsetReferenceClockError(f"{name} must be positive and finite")
    return x


def _finite_vector(values: Sequence[float], *, name: str) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise TemporalOffsetReferenceClockError(f"{name} must be a finite non-empty vector")
    return x


def reference_change_factor(source_phase_rate: float, target_phase_rate: float) -> float:
    omega_source = _positive_rate(source_phase_rate, name="source_phase_rate")
    omega_target = _positive_rate(target_phase_rate, name="target_phase_rate")
    return omega_source / omega_target


def transform_offset_rate(
    source_offset_rate: Sequence[float],
    source_phase_rate: float,
    target_phase_rate: float,
) -> np.ndarray:
    eta_source = _finite_vector(source_offset_rate, name="source_offset_rate")
    return reference_change_factor(source_phase_rate, target_phase_rate) * eta_source


def neutral_curvature_rate(
    offset_rate: Sequence[float], reference_phase_rate: float
) -> np.ndarray:
    eta = _finite_vector(offset_rate, name="offset_rate")
    omega = _positive_rate(reference_phase_rate, name="reference_phase_rate")
    return omega * eta


def compose_reference_factors(
    source_phase_rate: float,
    middle_phase_rate: float,
    target_phase_rate: float,
) -> tuple[float, float]:
    direct = reference_change_factor(source_phase_rate, target_phase_rate)
    composed = reference_change_factor(source_phase_rate, middle_phase_rate) * reference_change_factor(
        middle_phase_rate, target_phase_rate
    )
    return direct, composed


def pointwise_reference_change(
    source_offset_rates: Sequence[Sequence[float]],
    source_phase_rates: Sequence[float],
    target_phase_rates: Sequence[float],
) -> np.ndarray:
    eta = np.asarray(source_offset_rates, dtype=float)
    if eta.ndim != 2 or eta.shape[0] == 0 or not np.all(np.isfinite(eta)):
        raise TemporalOffsetReferenceClockError("source_offset_rates must be a finite non-empty 2D array")
    count = eta.shape[0]
    source = np.asarray(source_phase_rates, dtype=float)
    target = np.asarray(target_phase_rates, dtype=float)
    if source.shape != (count,) or target.shape != (count,):
        raise TemporalOffsetReferenceClockError("phase-rate arrays must match the sample count")
    if not np.all(np.isfinite(source)) or not np.all(np.isfinite(target)):
        raise TemporalOffsetReferenceClockError("phase-rate arrays must be finite")
    if np.any(source <= 0.0) or np.any(target <= 0.0):
        raise TemporalOffsetReferenceClockError("phase-rate arrays must be positive")
    return eta * (source / target)[:, None]


def accumulated_offset_from_rate(
    offset_rates: Sequence[Sequence[float]], delta_theta: Sequence[float]
) -> np.ndarray:
    eta = np.asarray(offset_rates, dtype=float)
    if eta.ndim != 2 or eta.shape[0] == 0 or not np.all(np.isfinite(eta)):
        raise TemporalOffsetReferenceClockError("offset_rates must be a finite non-empty 2D array")
    steps = np.asarray(delta_theta, dtype=float)
    if steps.shape != (eta.shape[0],) or not np.all(np.isfinite(steps)) or np.any(steps <= 0.0):
        raise TemporalOffsetReferenceClockError("delta_theta must be positive and match the sample count")
    return np.sum(eta * steps[:, None], axis=0)


def information_reference_change_factor(
    source_information_rate: float,
    target_information_rate: float,
) -> float:
    gamma_source = _positive_rate(source_information_rate, name="source_information_rate")
    gamma_target = _positive_rate(target_information_rate, name="target_information_rate")
    return gamma_source / gamma_target


def information_rate_from_phase_rate(phase_rate: float, *, kappa: float = KAPPA) -> float:
    omega = _positive_rate(phase_rate, name="phase_rate")
    k = _positive_rate(kappa, name="kappa")
    return k * omega


def winding_locked_reference_factor(source_winding: int, target_winding: int) -> float:
    if not isinstance(source_winding, int) or isinstance(source_winding, bool) or source_winding <= 0:
        raise TemporalOffsetReferenceClockError("source_winding must be a positive integer")
    if not isinstance(target_winding, int) or isinstance(target_winding, bool) or target_winding <= 0:
        raise TemporalOffsetReferenceClockError("target_winding must be a positive integer")
    return source_winding / target_winding


def calibrated_reference_factor(
    source_phase_rate: float,
    target_phase_rate: float,
    source_clock_scale: float,
    target_clock_scale: float,
) -> float:
    omega_source = _positive_rate(source_phase_rate, name="source_phase_rate")
    omega_target = _positive_rate(target_phase_rate, name="target_phase_rate")
    t_source = _positive_rate(source_clock_scale, name="source_clock_scale")
    t_target = _positive_rate(target_clock_scale, name="target_clock_scale")
    return (t_target * omega_source) / (t_source * omega_target)


def audit_reference_clock_change(
    curvature_rate: Sequence[float],
    source_phase_rate: float,
    target_phase_rate: float,
) -> ReferenceClockCocycleAudit:
    curvature = _finite_vector(curvature_rate, name="curvature_rate")
    omega_source = _positive_rate(source_phase_rate, name="source_phase_rate")
    omega_target = _positive_rate(target_phase_rate, name="target_phase_rate")

    eta_source = curvature / omega_source
    eta_target_direct = curvature / omega_target
    eta_target_transformed = transform_offset_rate(eta_source, omega_source, omega_target)
    neutral_source = neutral_curvature_rate(eta_source, omega_source)
    neutral_target = neutral_curvature_rate(eta_target_direct, omega_target)

    return ReferenceClockCocycleAudit(
        direct_target_rate=eta_target_direct,
        transformed_target_rate=eta_target_transformed,
        neutral_curvature_from_source=neutral_source,
        neutral_curvature_from_target=neutral_target,
        max_rate_residual=float(np.max(np.abs(eta_target_direct - eta_target_transformed))),
        max_neutral_residual=float(np.max(np.abs(neutral_source - neutral_target))),
    )
