from __future__ import annotations

import math
from dataclasses import dataclass

from .event_memory_kick import derived_memory_kick
from .internal_elapsed import InternalElapsedError, elapsed_increment
from .memory_recall import MemoryEventReceipt


class TransportMemoryBridgeError(ValueError):
    pass


@dataclass(frozen=True)
class TransportMemoryAdmission:
    realized: bool
    structural_signature: float
    wave_activation: float
    realized_now_weight: float
    receipt: MemoryEventReceipt


def _nonnegative_finite(value: float, name: str) -> float:
    x = float(value)
    if not math.isfinite(x) or x < 0.0:
        raise TransportMemoryBridgeError(f"{name} must be finite and non-negative")
    return x


def _finite_complex(value: complex, name: str) -> complex:
    z = complex(value)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise TransportMemoryBridgeError(f"{name} must be finite")
    return z


def transport_memory_admission(
    activity: float,
    delta_lambda: float,
    structural_signature: float,
    wave_activation: float,
    delta_m: complex,
    *,
    reference_activity: float = 1.0,
) -> TransportMemoryAdmission:
    """Build one Memory receipt from the upstream transport/NOW boundary.

    Wave activation is used as a realization-support gate. The pre-existing
    structural signature remains the event amplitude in the normalized Memory
    kick law. This avoids introducing a second multiplicative gain proportional
    to the arbitrary normalization of the wave amplitude.
    """
    q = _nonnegative_finite(structural_signature, "structural_signature")
    eps = _nonnegative_finite(wave_activation, "wave_activation")
    dm = _finite_complex(delta_m, "delta_m")
    try:
        delta_tau = elapsed_increment(
            activity,
            delta_lambda,
            reference_activity=reference_activity,
        )
    except InternalElapsedError as exc:
        raise TransportMemoryBridgeError(str(exc)) from exc

    realized_weight = q * eps
    if not math.isfinite(realized_weight):
        raise TransportMemoryBridgeError("realized NOW weight overflowed")
    realized = q > 0.0 and eps > 0.0
    event_weight = q if realized else 0.0
    receipt = MemoryEventReceipt(delta_tau, event_weight, dm)
    return TransportMemoryAdmission(realized, q, eps, realized_weight, receipt)


def transport_memory_kick(admission: TransportMemoryAdmission) -> complex:
    """Return the normalized Memory kick carried by an admitted bridge receipt."""
    if not isinstance(admission, TransportMemoryAdmission):
        raise TransportMemoryBridgeError("admission must be a TransportMemoryAdmission")
    return derived_memory_kick(
        admission.receipt.delta_m,
        admission.receipt.event_weight,
    )
