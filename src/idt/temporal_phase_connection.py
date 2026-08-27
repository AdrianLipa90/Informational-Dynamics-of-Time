from __future__ import annotations

import math
from typing import Sequence
import numpy as np

KAPPA = math.log(2.0)/(24.0*math.pi)

class TemporalPhaseConnectionError(ValueError):
    pass

def _state(v: Sequence[complex]) -> np.ndarray:
    z=np.asarray(v,dtype=complex)
    if z.ndim != 1 or z.size < 2 or not np.all(np.isfinite(z.real)) or not np.all(np.isfinite(z.imag)):
        raise TemporalPhaseConnectionError('state must be a finite complex vector of length >=2')
    n=np.linalg.norm(z)
    if n <= 0:
        raise TemporalPhaseConnectionError('state norm must be positive')
    return z/n

def wrap_phase(x: float) -> float:
    if not math.isfinite(float(x)):
        raise TemporalPhaseConnectionError('phase must be finite')
    return float((float(x)+math.pi)%(2.0*math.pi)-math.pi)

def pancharatnam_link(a: Sequence[complex], b: Sequence[complex]) -> complex:
    za=_state(a); zb=_state(b)
    ov=np.vdot(za,zb)
    mag=abs(ov)
    if mag <= 1e-14:
        raise TemporalPhaseConnectionError('Pancharatnam link undefined for zero overlap')
    return complex(ov/mag)

def temporal_edge_link(a, b, delta_h_bits: float, sigma_bits: float, *, kappa: float=KAPPA) -> complex:
    vals=[delta_h_bits,sigma_bits,kappa]
    if not all(math.isfinite(float(x)) for x in vals):
        raise TemporalPhaseConnectionError('edge data must be finite')
    return pancharatnam_link(a,b)*np.exp(1j*float(kappa)*(float(delta_h_bits)+float(sigma_bits)))

def cycle_phase(links: Sequence[complex]) -> float:
    if len(links) == 0:
        raise TemporalPhaseConnectionError('cycle must be nonempty')
    prod=1+0j
    for z in links:
        c=complex(z)
        if not math.isfinite(c.real) or not math.isfinite(c.imag) or abs(c) <= 0:
            raise TemporalPhaseConnectionError('links must be finite and nonzero')
        prod *= c/abs(c)
    return wrap_phase(float(np.angle(prod)))

def exact_scalar_cycle_sum(values: Sequence[float]) -> float:
    x=np.asarray(values,dtype=float)
    if x.ndim != 1 or x.size < 2 or not np.all(np.isfinite(x)):
        raise TemporalPhaseConnectionError('values must be a finite 1D cycle')
    return float(sum(float(x[(i+1)%x.size]-x[i]) for i in range(x.size)))

def connection_obstruction(holonomy_phase: float, *, atol: float=1e-10) -> bool:
    return abs(wrap_phase(holonomy_phase)) > float(atol)

def gauge_transform(states: Sequence[Sequence[complex]], phases: Sequence[float]):
    if len(states)!=len(phases):
        raise TemporalPhaseConnectionError('state and phase counts must agree')
    out=[]
    for s,p in zip(states,phases):
        if not math.isfinite(float(p)):
            raise TemporalPhaseConnectionError('gauge phases must be finite')
        out.append(_state(s)*np.exp(1j*float(p)))
    return out
