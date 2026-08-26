from __future__ import annotations
import math
from typing import Sequence
import numpy as np


class MemoryDynamicsError(ValueError):
    pass


def _finite_state(state: Sequence[complex], name: str = "state") -> np.ndarray:
    v = np.asarray(state, dtype=complex)
    if v.ndim != 1 or v.size == 0:
        raise MemoryDynamicsError(f"{name} must be a non-empty vector")
    if not np.all(np.isfinite(v.real)) or not np.all(np.isfinite(v.imag)):
        raise MemoryDynamicsError(f"{name} must be finite")
    if float(np.vdot(v, v).real) <= 0:
        raise MemoryDynamicsError(f"{name} must have positive norm")
    return v


def rank_one_state_operator(state):
    v = _finite_state(state)
    return np.outer(v, v.conj())


def normalized_state_operator(state):
    v = _finite_state(state)
    w = float(np.vdot(v, v).real)
    return np.outer(v, v.conj()) / w


def raw_event_imprint(state_minus, state_plus):
    return rank_one_state_operator(state_plus) - rank_one_state_operator(state_minus)


def projective_event_imprint(state_minus, state_plus):
    return normalized_state_operator(state_plus) - normalized_state_operator(state_minus)


def event_weight_change(state_minus, state_plus):
    vm = _finite_state(state_minus, "state_minus")
    vp = _finite_state(state_plus, "state_plus")
    return float(np.vdot(vp, vp).real - np.vdot(vm, vm).real)


def _hermitian(obs, name):
    a = np.asarray(obs, dtype=complex)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] == 0:
        raise MemoryDynamicsError(f"{name} must be square")
    if not np.all(np.isfinite(a.real)) or not np.all(np.isfinite(a.imag)):
        raise MemoryDynamicsError(f"{name} must be finite")
    if not np.allclose(a, a.conj().T, atol=1e-12, rtol=0.0):
        raise MemoryDynamicsError(f"{name} must be Hermitian")
    return a


def memory_plane_projection(state_or_rho, Q_M, P_M, *, state_input=True):
    rho = normalized_state_operator(state_or_rho) if state_input else np.asarray(state_or_rho, dtype=complex)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise MemoryDynamicsError("rho must be square")
    q = _hermitian(Q_M, "Q_M")
    p = _hermitian(P_M, "P_M")
    if q.shape != rho.shape or p.shape != rho.shape:
        raise MemoryDynamicsError("observable dimension mismatch")
    x = np.trace(rho @ q)
    y = np.trace(rho @ p)
    if abs(x.imag) > 1e-10 or abs(y.imag) > 1e-10:
        raise MemoryDynamicsError("Hermitian expectation must be real")
    return complex(float(x.real), float(y.real))


def projected_imprint(delta_M, Q_M, P_M):
    d = np.asarray(delta_M, dtype=complex)
    if d.ndim != 2 or d.shape[0] != d.shape[1] or not np.allclose(d, d.conj().T, atol=1e-12, rtol=0.0):
        raise MemoryDynamicsError("delta_M must be Hermitian square")
    q = _hermitian(Q_M, "Q_M")
    p = _hermitian(P_M, "P_M")
    if q.shape != d.shape or p.shape != d.shape:
        raise MemoryDynamicsError("observable dimension mismatch")
    dx = np.trace(d @ q)
    dy = np.trace(d @ p)
    return complex(float(dx.real), float(dy.real))


def _finite_complex(z, name="m"):
    z = complex(z)
    if not (math.isfinite(z.real) and math.isfinite(z.imag)):
        raise MemoryDynamicsError(f"{name} must be finite")
    return z


def central_memory_acceleration(m, mu):
    z = _finite_complex(m)
    mu = float(mu)
    r = abs(z)
    if not math.isfinite(mu) or mu <= 0:
        raise MemoryDynamicsError("mu must be finite and positive")
    if r <= 0:
        raise MemoryDynamicsError("central state excludes r=0")
    return -mu * z / (r**3)


def memory_energy(m, v, mu):
    z = _finite_complex(m)
    vel = _finite_complex(v, "v")
    mu = float(mu)
    r = abs(z)
    if not math.isfinite(mu) or mu <= 0 or r <= 0:
        raise MemoryDynamicsError("valid positive mu and nonzero radius required")
    return float(0.5 * abs(vel)**2 - mu / r)


def memory_angular_momentum(m, v):
    z = _finite_complex(m)
    vel = _finite_complex(v, "v")
    return float((z.conjugate() * vel).imag)


def memory_areal_rate(m, v):
    return 0.5 * memory_angular_momentum(m, v)


def memory_circulation_rate(h, area, coupling, coupling_rate=0.0):
    vals = [float(h), float(area), float(coupling), float(coupling_rate)]
    if not all(math.isfinite(x) for x in vals):
        raise MemoryDynamicsError("rate inputs must be finite")
    return vals[2] * vals[0] + 2.0 * vals[3] * vals[1]


def action_area_momentum(m, coupling):
    z = _finite_complex(m)
    lam = float(coupling)
    if not math.isfinite(lam):
        raise MemoryDynamicsError("coupling must be finite")
    return float(lam * abs(z)**2)


def berry_darboux_momentum(radius):
    r = float(radius)
    if not math.isfinite(r) or r < 0:
        raise MemoryDynamicsError("Berry radius must be finite and non-negative")
    return float(r*r / (1.0 + r*r))


def memory_to_berry_patch(m, coupling):
    z = _finite_complex(m)
    lam = float(coupling)
    if not math.isfinite(lam):
        raise MemoryDynamicsError("coupling must be finite")
    if lam == 0:
        return 0j
    p = abs(lam) * abs(z)**2
    if not (0.0 <= p < 1.0):
        raise MemoryDynamicsError("Berry pullback patch requires |lambda| r^2 < 1")
    R = math.sqrt(p / (1.0 - p)) if p > 0 else 0.0
    theta = math.atan2(z.imag, z.real)
    phi = math.copysign(1.0, lam) * theta
    return R * complex(math.cos(phi), math.sin(phi))


def berry_pullback_connection_coefficient(m, coupling):
    z = _finite_complex(m)
    lam = float(coupling)
    if lam == 0:
        return 0.0
    zb = memory_to_berry_patch(z, lam)
    pB = berry_darboux_momentum(abs(zb))
    return float(math.copysign(1.0, lam) * pB)


def berry_pullback_curvature_polar(radius, coupling):
    r = float(radius)
    lam = float(coupling)
    if not (math.isfinite(r) and r >= 0 and math.isfinite(lam)):
        raise MemoryDynamicsError("finite radial inputs required")
    if abs(lam) * r*r >= 1.0 and lam != 0:
        raise MemoryDynamicsError("Berry pullback patch requires |lambda| r^2 < 1")
    return float(2.0 * lam * r)


def apply_memory_event_impulse(m, v, delta_m, gain=1.0):
    z = _finite_complex(m)
    vel = _finite_complex(v, "v")
    dm = _finite_complex(delta_m, "delta_m")
    g = float(gain)
    if not math.isfinite(g):
        raise MemoryDynamicsError("gain must be finite")
    return z, vel + g * dm
