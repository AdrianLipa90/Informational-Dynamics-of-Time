from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

KAPPA = math.log(2.0) / (24.0 * math.pi)


class SeamPhaseOffsetDurationError(ValueError):
    pass


@dataclass(frozen=True)
class TemporalOffsetAudit:
    intrinsic_offset: np.ndarray
    coordinate_offset: np.ndarray
    proper_offset: np.ndarray
    information_identity_residual: float


def _edge_samples(values: Sequence[Sequence[float]], *, name: str) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[0] == 0 or not np.all(np.isfinite(x)):
        raise SeamPhaseOffsetDurationError(f"{name} must be a finite non-empty 2D array")
    return x


def _sample_vector(values: Sequence[float], count: int, *, name: str, positive: bool = False) -> np.ndarray:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.shape != (count,) or not np.all(np.isfinite(x)):
        raise SeamPhaseOffsetDurationError(f"{name} must be finite with one entry per sample")
    if positive and np.any(x <= 0.0):
        raise SeamPhaseOffsetDurationError(f"{name} entries must be positive")
    return x


def intrinsic_offset_rate(
    temporal_seam_curvature: Sequence[float], reference_phase_rate: float
) -> np.ndarray:
    curvature = np.asarray(temporal_seam_curvature, dtype=float)
    if curvature.ndim != 1 or not np.all(np.isfinite(curvature)):
        raise SeamPhaseOffsetDurationError("temporal_seam_curvature must be a finite edge vector")
    omega = float(reference_phase_rate)
    if not math.isfinite(omega) or omega <= 0.0:
        raise SeamPhaseOffsetDurationError("reference_phase_rate must be positive and finite")
    return curvature / omega


def intrinsic_duration_offset(
    curvature_samples: Sequence[Sequence[float]],
    reference_phase_rates: Sequence[float],
    delta_theta: Sequence[float],
) -> np.ndarray:
    curvature = _edge_samples(curvature_samples, name="curvature_samples")
    count = int(curvature.shape[0])
    omega = _sample_vector(
        reference_phase_rates, count, name="reference_phase_rates", positive=True
    )
    steps = _sample_vector(delta_theta, count, name="delta_theta", positive=True)
    return np.sum(curvature * (steps / omega)[:, None], axis=0)


def constant_reference_phase_offset(delta_phi_curv: Sequence[float], reference_phase_rate: float) -> np.ndarray:
    phase = np.asarray(delta_phi_curv, dtype=float)
    if phase.ndim != 1 or not np.all(np.isfinite(phase)):
        raise SeamPhaseOffsetDurationError("delta_phi_curv must be a finite edge vector")
    omega = float(reference_phase_rate)
    if not math.isfinite(omega) or omega <= 0.0:
        raise SeamPhaseOffsetDurationError("reference_phase_rate must be positive and finite")
    return phase / omega


def intrinsic_information_rate(reference_phase_rate: float, *, kappa: float = KAPPA) -> float:
    omega = float(reference_phase_rate)
    k = float(kappa)
    if not math.isfinite(omega) or omega <= 0.0:
        raise SeamPhaseOffsetDurationError("reference_phase_rate must be positive and finite")
    if not math.isfinite(k) or k <= 0.0:
        raise SeamPhaseOffsetDurationError("kappa must be positive and finite")
    return k * omega


def intrinsic_offset_rate_from_information(
    temporal_seam_curvature: Sequence[float],
    reference_information_rate: float,
    *,
    kappa: float = KAPPA,
) -> np.ndarray:
    curvature = np.asarray(temporal_seam_curvature, dtype=float)
    if curvature.ndim != 1 or not np.all(np.isfinite(curvature)):
        raise SeamPhaseOffsetDurationError("temporal_seam_curvature must be a finite edge vector")
    gamma = float(reference_information_rate)
    k = float(kappa)
    if not math.isfinite(gamma) or gamma <= 0.0:
        raise SeamPhaseOffsetDurationError("reference_information_rate must be positive and finite")
    if not math.isfinite(k) or k <= 0.0:
        raise SeamPhaseOffsetDurationError("kappa must be positive and finite")
    return k * curvature / gamma


def calibrated_coordinate_offset(
    curvature_samples: Sequence[Sequence[float]],
    reference_phase_rates: Sequence[float],
    reference_clock_scales: Sequence[float],
    delta_theta: Sequence[float],
) -> np.ndarray:
    curvature = _edge_samples(curvature_samples, name="curvature_samples")
    count = int(curvature.shape[0])
    omega = _sample_vector(
        reference_phase_rates, count, name="reference_phase_rates", positive=True
    )
    scale = _sample_vector(
        reference_clock_scales, count, name="reference_clock_scales", positive=True
    )
    steps = _sample_vector(delta_theta, count, name="delta_theta", positive=True)
    return np.sum(curvature * (scale * steps / omega)[:, None], axis=0)


def calibrated_proper_offset(
    curvature_samples: Sequence[Sequence[float]],
    reference_phase_rates: Sequence[float],
    reference_clock_scales: Sequence[float],
    relational_lapse: Sequence[float],
    delta_theta: Sequence[float],
) -> np.ndarray:
    curvature = _edge_samples(curvature_samples, name="curvature_samples")
    count = int(curvature.shape[0])
    omega = _sample_vector(
        reference_phase_rates, count, name="reference_phase_rates", positive=True
    )
    scale = _sample_vector(
        reference_clock_scales, count, name="reference_clock_scales", positive=True
    )
    lapse = _sample_vector(relational_lapse, count, name="relational_lapse", positive=True)
    steps = _sample_vector(delta_theta, count, name="delta_theta", positive=True)
    return np.sum(curvature * (lapse * scale * steps / omega)[:, None], axis=0)


def reference_phase_period(reference_phase_rate: float) -> float:
    omega = float(reference_phase_rate)
    if not math.isfinite(omega) or omega <= 0.0:
        raise SeamPhaseOffsetDurationError("reference_phase_rate must be positive and finite")
    return 2.0 * math.pi / omega


def winding_offset_control(winding: int, reference_phase_rate: float) -> float:
    if not isinstance(winding, int) or isinstance(winding, bool):
        raise SeamPhaseOffsetDurationError("winding must be an integer")
    return winding * reference_phase_period(reference_phase_rate)


def audit_temporal_offset_map(
    curvature_samples: Sequence[Sequence[float]],
    reference_phase_rates: Sequence[float],
    reference_clock_scales: Sequence[float],
    relational_lapse: Sequence[float],
    delta_theta: Sequence[float],
) -> TemporalOffsetAudit:
    curvature = _edge_samples(curvature_samples, name="curvature_samples")
    count = int(curvature.shape[0])
    omega = _sample_vector(reference_phase_rates, count, name="reference_phase_rates", positive=True)
    steps = _sample_vector(delta_theta, count, name="delta_theta", positive=True)

    intrinsic = intrinsic_duration_offset(curvature, omega, steps)
    coordinate = calibrated_coordinate_offset(
        curvature, omega, reference_clock_scales, steps
    )
    proper = calibrated_proper_offset(
        curvature, omega, reference_clock_scales, relational_lapse, steps
    )

    gamma = KAPPA * omega
    info_integrand = KAPPA * curvature / gamma[:, None]
    direct_integrand = curvature / omega[:, None]
    residual = float(np.max(np.abs(info_integrand - direct_integrand)))

    return TemporalOffsetAudit(
        intrinsic_offset=intrinsic,
        coordinate_offset=coordinate,
        proper_offset=proper,
        information_identity_residual=residual,
    )
