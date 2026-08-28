from __future__ import annotations

import math
from dataclasses import dataclass


KAPPA = math.log(2.0) / (24.0 * math.pi)


class TIRTemporalNormalizationError(ValueError):
    pass


@dataclass(frozen=True)
class PhaseClockBridge:
    intrinsic_phase_rate: float
    intrinsic_information_rate: float
    relational_lapse: float
    coordinate_phase_rate: float
    local_calibrated_phase_rate: float


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise TIRTemporalNormalizationError(f"{name} must be finite")
    return out


def intrinsic_phase_rate(phase_rate_lambda: float, activity: float) -> float:
    omega = _finite(phase_rate_lambda, "phase_rate_lambda")
    a = _finite(activity, "activity")
    if a <= 0.0:
        raise TIRTemporalNormalizationError("activity must be positive")
    return omega / a


def intrinsic_information_rate(
    phase_rate_lambda: float,
    activity: float,
    *,
    kappa: float = KAPPA,
) -> float:
    kap = _finite(kappa, "kappa")
    return kap * intrinsic_phase_rate(phase_rate_lambda, activity)


def reparameterize_rate_and_activity(
    phase_rate_lambda: float,
    activity: float,
    d_lambda_d_lambda_prime: float,
) -> tuple[float, float]:
    omega = _finite(phase_rate_lambda, "phase_rate_lambda")
    a = _finite(activity, "activity")
    jac = _finite(d_lambda_d_lambda_prime, "d_lambda_d_lambda_prime")
    if a <= 0.0:
        raise TIRTemporalNormalizationError("activity must be positive")
    if jac <= 0.0:
        raise TIRTemporalNormalizationError("reparameterization Jacobian must be positive")
    return omega * jac, a * jac


def relational_lapse(activity_x: float, activity_ref: float) -> float:
    ax = _finite(activity_x, "activity_x")
    ar = _finite(activity_ref, "activity_ref")
    if ax <= 0.0 or ar <= 0.0:
        raise TIRTemporalNormalizationError("clock activities must be positive")
    return ax / ar


def phase_clock_bridge(
    phase_rate_lambda: float,
    activity_x: float,
    activity_ref: float,
    reference_time_scale: float,
    *,
    kappa: float = KAPPA,
) -> PhaseClockBridge:
    omega = _finite(phase_rate_lambda, "phase_rate_lambda")
    ax = _finite(activity_x, "activity_x")
    ar = _finite(activity_ref, "activity_ref")
    t_ref = _finite(reference_time_scale, "reference_time_scale")
    if ax <= 0.0 or ar <= 0.0:
        raise TIRTemporalNormalizationError("clock activities must be positive")
    if t_ref <= 0.0:
        raise TIRTemporalNormalizationError("reference_time_scale must be positive")

    omega_theta = omega / ax
    n_r = ax / ar
    local_rate = omega_theta / t_ref
    coordinate_rate = omega / (t_ref * ar)
    return PhaseClockBridge(
        intrinsic_phase_rate=omega_theta,
        intrinsic_information_rate=float(kappa) * omega_theta,
        relational_lapse=n_r,
        coordinate_phase_rate=coordinate_rate,
        local_calibrated_phase_rate=local_rate,
    )


def common_cycle_average_rates(
    winding_i: int,
    winding_j: int,
    delta_theta: float,
) -> tuple[float, float, float]:
    if not isinstance(winding_i, int) or isinstance(winding_i, bool):
        raise TIRTemporalNormalizationError("winding_i must be an integer")
    if not isinstance(winding_j, int) or isinstance(winding_j, bool):
        raise TIRTemporalNormalizationError("winding_j must be an integer")
    if winding_j == 0:
        raise TIRTemporalNormalizationError("winding_j must be nonzero for a ratio")
    theta = _finite(delta_theta, "delta_theta")
    if theta <= 0.0:
        raise TIRTemporalNormalizationError("delta_theta must be positive")

    omega_i = 2.0 * math.pi * winding_i / theta
    omega_j = 2.0 * math.pi * winding_j / theta
    return omega_i, omega_j, omega_i / omega_j


def modular_support_count_from_winding(frame_winding: int) -> int:
    if not isinstance(frame_winding, int) or isinstance(frame_winding, bool) or frame_winding <= 0:
        raise TIRTemporalNormalizationError("frame_winding must be a positive integer")
    return frame_winding + 1
