from __future__ import annotations

import math

from .memory_dynamics import MemoryDynamicsError, memory_angular_momentum, memory_energy


class EventMemoryKickError(MemoryDynamicsError):
    pass


def _finite_complex(value, name: str) -> complex:
    z = complex(value)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise EventMemoryKickError(f"{name} must be finite")
    return z


def _event_weight(value: float) -> float:
    q = float(value)
    if not math.isfinite(q) or q < 0.0:
        raise EventMemoryKickError("event_weight q must be finite and non-negative")
    return q


def memory_event_action(m, delta_m, event_weight: float) -> float:
    """Minimal normalized event action S_n^M = q_n Re(delta_m_n^* m)."""
    z = _finite_complex(m, "m")
    dm = _finite_complex(delta_m, "delta_m")
    q = _event_weight(event_weight)
    return float(q * (dm.conjugate() * z).real)


def derived_memory_kick(delta_m, event_weight: float) -> complex:
    """Gradient of the minimal linear event action in the memory plane."""
    dm = _finite_complex(delta_m, "delta_m")
    q = _event_weight(event_weight)
    return q * dm


def apply_derived_memory_event_impulse(m, v, delta_m, event_weight: float) -> tuple[complex, complex]:
    """Apply the event-action jump law v_M^+ = v_M^- + q_n delta_m_n."""
    z = _finite_complex(m, "m")
    vel = _finite_complex(v, "v")
    kick = derived_memory_kick(delta_m, event_weight)
    return z, vel + kick


def derived_kick_invariant_changes(m, v, delta_m, event_weight: float, mu_memory: float) -> tuple[float, float]:
    """Return exact Delta E_M and Delta h_M produced by the derived kick."""
    z = _finite_complex(m, "m")
    vel = _finite_complex(v, "v")
    kick = derived_memory_kick(delta_m, event_weight)
    _, v_plus = apply_derived_memory_event_impulse(z, vel, delta_m, event_weight)
    d_energy = memory_energy(z, v_plus, mu_memory) - memory_energy(z, vel, mu_memory)
    d_h = memory_angular_momentum(z, v_plus) - memory_angular_momentum(z, vel)
    return float(d_energy), float(d_h)
