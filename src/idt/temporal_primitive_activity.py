from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class TemporalPrimitiveError(ValueError):
    pass


@dataclass(frozen=True)
class DirectedKinetics:
    mobility: float
    drive: float
    forward: float
    reverse: float
    activity: float
    current: float
    orientation: float
    shannon_affinity_bits: float


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise TemporalPrimitiveError(f"{name} must be finite")
    return out


def relational_mobility(
    rho_a: float,
    rho_b: float,
    eta_a: float,
    eta_b: float,
) -> float:
    ra = _finite(rho_a, "rho_a")
    rb = _finite(rho_b, "rho_b")
    ea = _finite(eta_a, "eta_a")
    eb = _finite(eta_b, "eta_b")
    if min(ra, rb, ea, eb) <= 0.0:
        raise TemporalPrimitiveError("relational density and viscosity must be positive")
    return math.sqrt(ra * rb) / (0.5 * (ea + eb))


def directed_kinetics(mobility: float, drive: float) -> DirectedKinetics:
    m = _finite(mobility, "mobility")
    a = _finite(drive, "drive")
    if m <= 0.0:
        raise TemporalPrimitiveError("mobility must be positive")

    forward = m * math.exp(0.5 * a)
    reverse = m * math.exp(-0.5 * a)
    activity = forward + reverse
    current = forward - reverse
    orientation = current / activity
    sigma_bits = a / math.log(2.0)

    return DirectedKinetics(
        mobility=m,
        drive=a,
        forward=forward,
        reverse=reverse,
        activity=activity,
        current=current,
        orientation=orientation,
        shannon_affinity_bits=sigma_bits,
    )


def activity_increment(activity: float, d_lambda: float) -> float:
    a = _finite(activity, "activity")
    dl = _finite(d_lambda, "d_lambda")
    if a <= 0.0:
        raise TemporalPrimitiveError("activity must be positive")
    if dl <= 0.0:
        raise TemporalPrimitiveError("d_lambda must be positive")
    return a * dl


def activity_path_measure(
    mobilities: Sequence[float],
    drives: Sequence[float],
    d_lambda: Sequence[float],
) -> float:
    m = np.asarray(mobilities, dtype=float)
    a = np.asarray(drives, dtype=float)
    dl = np.asarray(d_lambda, dtype=float)
    if m.ndim != 1 or a.ndim != 1 or dl.ndim != 1:
        raise TemporalPrimitiveError("path inputs must be one-dimensional")
    if m.size == 0 or m.shape != a.shape or m.shape != dl.shape:
        raise TemporalPrimitiveError("path inputs must have the same non-empty shape")
    if not np.all(np.isfinite(m)) or not np.all(np.isfinite(a)) or not np.all(np.isfinite(dl)):
        raise TemporalPrimitiveError("path inputs must be finite")
    if np.any(m <= 0.0) or np.any(dl <= 0.0):
        raise TemporalPrimitiveError("mobilities and ordering increments must be positive")

    activities = 2.0 * m * np.cosh(0.5 * a)
    return float(np.dot(activities, dl))


def reparameterize_transition_density(weight: float, d_lambda_d_lambda_prime: float) -> float:
    w = _finite(weight, "weight")
    jac = _finite(d_lambda_d_lambda_prime, "d_lambda_d_lambda_prime")
    if w <= 0.0:
        raise TemporalPrimitiveError("transition weight must be positive")
    if jac <= 0.0:
        raise TemporalPrimitiveError("reparameterization Jacobian must be positive")
    return w * jac


def relational_lapse_from_activity(activity_x: float, activity_ref: float) -> float:
    ax = _finite(activity_x, "activity_x")
    ar = _finite(activity_ref, "activity_ref")
    if ax <= 0.0 or ar <= 0.0:
        raise TemporalPrimitiveError("clock activities must be positive")
    return ax / ar


def calibrated_elapsed_increment(
    activity_x: float,
    activity_ref: float,
    dt_ref: float,
) -> float:
    dt = _finite(dt_ref, "dt_ref")
    if dt <= 0.0:
        raise TemporalPrimitiveError("reference elapsed increment must be positive")
    return relational_lapse_from_activity(activity_x, activity_ref) * dt


def drive_from_shannon_affinity_bits(sigma_bits: float) -> float:
    sigma = _finite(sigma_bits, "sigma_bits")
    return math.log(2.0) * sigma


def temporal_primitive_from_information(
    mobility: float,
    sigma_bits: float,
    d_lambda: float,
) -> tuple[float, float]:
    drive = drive_from_shannon_affinity_bits(sigma_bits)
    kinetics = directed_kinetics(mobility, drive)
    return activity_increment(kinetics.activity, d_lambda), kinetics.orientation
