from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_recall import (
    MemoryEventReceipt,
    MemoryRecallError,
    kepler_memory_inverse_step,
)


class RetrodictionError(ValueError):
    pass


@dataclass(frozen=True)
class MissingKickInference:
    delta_velocity: complex
    checkpoint_residual: float


@dataclass(frozen=True)
class RetrodictedReceipt:
    receipt: MemoryEventReceipt
    delta_velocity: complex
    factorization_residual: float
    mode: str


def _finite_complex(value, name: str) -> complex:
    z = complex(value)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise RetrodictionError(f"{name} must be finite")
    return z


def _state_copy(state: MemoryPhaseState) -> MemoryPhaseState:
    r = np.asarray(state.position, dtype=float)
    v = np.asarray(state.velocity, dtype=float)
    if r.shape != (2,) or v.shape != (2,):
        raise RetrodictionError("memory state position and velocity must be two-component vectors")
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(v)):
        raise RetrodictionError("memory state must be finite")
    tau = float(state.tau_internal)
    area = float(state.swept_area)
    if not (math.isfinite(tau) and math.isfinite(area)):
        raise RetrodictionError("memory state tau_internal and swept_area must be finite")
    return MemoryPhaseState(r.copy(), v.copy(), tau, area)


def _checkpoint_residual(before: MemoryPhaseState, inferred_kicked: MemoryPhaseState) -> float:
    position_error = float(np.max(np.abs(np.asarray(before.position) - np.asarray(inferred_kicked.position))))
    tau_error = abs(float(before.tau_internal) - float(inferred_kicked.tau_internal))
    area_error = abs(float(before.swept_area) - float(inferred_kicked.swept_area))
    return max(position_error, tau_error, area_error)


def infer_missing_kick(
    state_before_event: MemoryPhaseState,
    state_after_segment: MemoryPhaseState,
    mu_memory: float,
    delta_tau: float,
    *,
    checkpoint_tol: float = 1e-10,
) -> MissingKickInference:
    """Infer the event velocity jump by reversing only the known smooth Kepler segment."""
    before = _state_copy(state_before_event)
    after = _state_copy(state_after_segment)
    tol = float(checkpoint_tol)
    if not math.isfinite(tol) or tol < 0.0:
        raise RetrodictionError("checkpoint_tol must be finite and non-negative")
    try:
        inferred_kicked = kepler_memory_inverse_step(after, mu_memory, delta_tau)
    except MemoryRecallError as exc:
        raise RetrodictionError(str(exc)) from exc
    residual = _checkpoint_residual(before, inferred_kicked)
    if residual > tol:
        raise RetrodictionError(
            f"before-event checkpoint is inconsistent with the reversed smooth segment: residual={residual}"
        )
    delta_v = np.asarray(inferred_kicked.velocity, dtype=float) - np.asarray(before.velocity, dtype=float)
    return MissingKickInference(complex(float(delta_v[0]), float(delta_v[1])), residual)


def infer_event_weight_from_known_imprint(
    delta_velocity: complex,
    delta_m: complex,
    *,
    residual_tol: float = 1e-10,
) -> tuple[float, float]:
    """Infer q from Delta v = q delta_m, failing closed on directional inconsistency."""
    dv = _finite_complex(delta_velocity, "delta_velocity")
    dm = _finite_complex(delta_m, "delta_m")
    tol = float(residual_tol)
    if not math.isfinite(tol) or tol < 0.0:
        raise RetrodictionError("residual_tol must be finite and non-negative")

    denom = abs(dm) ** 2
    if denom == 0.0:
        if abs(dv) <= tol:
            return 0.0, abs(dv)
        raise RetrodictionError("nonzero kick cannot be factorized through a zero memory imprint")

    q = float((dv * dm.conjugate()).real / denom)
    scale = max(1.0, abs(dv), abs(q * dm))
    if q < -tol * scale:
        raise RetrodictionError("inferred event weight is negative")
    q = max(0.0, q)
    residual = abs(dv - q * dm)
    if residual > tol * scale:
        raise RetrodictionError(
            f"kick is not collinear with the supplied memory imprint: residual={residual}"
        )
    return q, residual


def infer_imprint_from_known_event_weight(delta_velocity: complex, event_weight: float) -> complex:
    """Infer delta_m from Delta v = q delta_m when q is independently known."""
    dv = _finite_complex(delta_velocity, "delta_velocity")
    q = float(event_weight)
    if not math.isfinite(q) or q < 0.0:
        raise RetrodictionError("event_weight must be finite and non-negative")
    if q == 0.0:
        if abs(dv) == 0.0:
            return 0.0j
        raise RetrodictionError("nonzero kick is incompatible with zero event weight")
    return dv / q


def retrodict_single_missing_receipt(
    state_before_event: MemoryPhaseState,
    state_after_segment: MemoryPhaseState,
    mu_memory: float,
    delta_tau: float,
    *,
    known_delta_m: complex | None = None,
    known_event_weight: float | None = None,
    checkpoint_tol: float = 1e-10,
    residual_tol: float = 1e-10,
) -> RetrodictedReceipt:
    """Retrodict one withheld receipt factor when the complementary factor is independently known.

    Exactly one of known_delta_m or known_event_weight must be supplied. If neither is
    supplied, only the product q * delta_m is identifiable from the two checkpoints.
    """
    if (known_delta_m is None) == (known_event_weight is None):
        if known_delta_m is None:
            raise RetrodictionError(
                "product-only ambiguity: provide either the memory imprint or the event weight"
            )
        raise RetrodictionError("provide exactly one independently known receipt factor")

    missing = infer_missing_kick(
        state_before_event,
        state_after_segment,
        mu_memory,
        delta_tau,
        checkpoint_tol=checkpoint_tol,
    )

    if known_delta_m is not None:
        dm = _finite_complex(known_delta_m, "known_delta_m")
        q, residual = infer_event_weight_from_known_imprint(
            missing.delta_velocity,
            dm,
            residual_tol=residual_tol,
        )
        mode = "EVENT_WEIGHT_FROM_KNOWN_IMPRINT"
    else:
        q = float(known_event_weight)
        dm = infer_imprint_from_known_event_weight(missing.delta_velocity, q)
        residual = 0.0
        mode = "IMPRINT_FROM_KNOWN_EVENT_WEIGHT"

    receipt = MemoryEventReceipt(float(delta_tau), q, dm)
    return RetrodictedReceipt(receipt, missing.delta_velocity, residual, mode)


def equivalent_kick_factorization(event_weight: float, delta_m: complex, scale: float) -> tuple[float, complex]:
    """Return a positive rescaling that preserves the kick product q * delta_m."""
    q = float(event_weight)
    dm = _finite_complex(delta_m, "delta_m")
    c = float(scale)
    if not (math.isfinite(q) and q >= 0.0):
        raise RetrodictionError("event_weight must be finite and non-negative")
    if not (math.isfinite(c) and c > 0.0):
        raise RetrodictionError("scale must be finite and strictly positive")
    return c * q, dm / c
