"""Material temporal-offset binding for IDT 02JM."""
from __future__ import annotations

from dataclasses import dataclass
import math


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return value


@dataclass(frozen=True)
class MaterialOffsetState:
    dtheta: float
    dtheta_offset: float
    dt: float
    dt_offset: float
    dtau: float
    dtau_offset: float
    seam_ratio: float
    gamma_t: float
    gamma_tau: float
    gamma_tau_offset: float


def material_offset_state(
    *,
    curvature: float,
    omega_ref: float,
    dtheta_ref: float,
    lapse: float,
    calibration: float,
    activity_ref: float,
    activity_local: float,
) -> MaterialOffsetState:
    """Compose the intrinsic seam offset with a positive material clock/lapse carrier.

    The caller supplies the already-admitted IDT quantities on one common ordering patch.
    `activity_local/activity_ref` must agree with `lapse` to deterministic tolerance.
    """
    curvature = _finite("curvature", curvature)
    omega_ref = _positive("omega_ref", omega_ref)
    dtheta_ref = _finite("dtheta_ref", dtheta_ref)
    lapse = _positive("lapse", lapse)
    calibration = _positive("calibration", calibration)
    activity_ref = _positive("activity_ref", activity_ref)
    activity_local = _positive("activity_local", activity_local)

    expected_lapse = activity_local / activity_ref
    if not math.isclose(lapse, expected_lapse, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("lapse must equal activity_local/activity_ref on the shared patch")

    eta = curvature / omega_ref
    dtheta_offset = eta * dtheta_ref
    dt = calibration * dtheta_ref
    dt_offset = calibration * dtheta_offset
    dtau = lapse * dt
    dtau_offset = lapse * dt_offset

    gamma_t = calibration * activity_ref
    gamma_tau = calibration * activity_local
    gamma_tau_offset = gamma_tau * eta

    return MaterialOffsetState(
        dtheta=dtheta_ref,
        dtheta_offset=dtheta_offset,
        dt=dt,
        dt_offset=dt_offset,
        dtau=dtau,
        dtau_offset=dtau_offset,
        seam_ratio=eta,
        gamma_t=gamma_t,
        gamma_tau=gamma_tau,
        gamma_tau_offset=gamma_tau_offset,
    )


def reference_change_factor(omega_r: float, omega_s: float) -> float:
    return _positive("omega_r", omega_r) / _positive("omega_s", omega_s)


def transform_material_offset(dtau_offset_r: float, omega_r: float, omega_s: float) -> float:
    dtau_offset_r = _finite("dtau_offset_r", dtau_offset_r)
    return reference_change_factor(omega_r, omega_s) * dtau_offset_r


def fractional_material_offset(state: MaterialOffsetState) -> float:
    if state.dtau == 0.0:
        raise ZeroDivisionError("material elapsed interval is zero")
    return state.dtau_offset / state.dtau
