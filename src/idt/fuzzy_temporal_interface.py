from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class FuzzyTemporalInterfaceError(ValueError):
    pass


@dataclass(frozen=True)
class SeamInterfaceAudit:
    pair_weight: float
    amplitude_roughness: float
    phase_mismatch_defect: float
    defect_probability: float
    overlap_probability: float
    amplitude_balance: float
    overlap_fraction: float
    defect_fraction: float
    fuzzy_strength: float
    mismatch: float


def _complex(value: complex, name: str) -> complex:
    out = complex(value)
    if not math.isfinite(out.real) or not math.isfinite(out.imag):
        raise FuzzyTemporalInterfaceError(f"{name} must be finite")
    return out


def _real(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise FuzzyTemporalInterfaceError(f"{name} must be finite")
    return out


def principal_phase(value: float) -> float:
    x = _real(value, "phase")
    return math.atan2(math.sin(x), math.cos(x))


def gauge_invariant_mismatch(left: complex, right: complex, seam_phase: float) -> float:
    a0 = _complex(left, "left")
    a1 = _complex(right, "right")
    phi = _real(seam_phase, "seam_phase")
    r0 = abs(a0)
    r1 = abs(a1)
    if r0 == 0.0 or r1 == 0.0:
        return 0.0
    relative = np.exp(-1j * phi) * a1 * np.conj(a0)
    return principal_phase(math.atan2(float(relative.imag), float(relative.real)))


def overlap_and_defect(left: complex, right: complex, seam_phase: float) -> tuple[complex, complex]:
    a0 = _complex(left, "left")
    a1 = _complex(right, "right")
    phi = _real(seam_phase, "seam_phase")
    hp = np.exp(0.5j * phi)
    hm = np.exp(-0.5j * phi)
    overlap = 0.5 * (hp * a0 + hm * a1)
    defect = 0.5 * (hp * a0 - hm * a1)
    return complex(overlap), complex(defect)


def amplitude_balance(left: complex, right: complex) -> float:
    r0 = abs(_complex(left, "left"))
    r1 = abs(_complex(right, "right"))
    denom = r0 * r0 + r1 * r1
    if denom == 0.0:
        return 0.0
    return float(2.0 * r0 * r1 / denom)


def fuzzy_interface_strength(left: complex, right: complex, seam_phase: float) -> float:
    a0 = _complex(left, "left")
    a1 = _complex(right, "right")
    r0 = abs(a0)
    r1 = abs(a1)
    if r0 == 0.0 or r1 == 0.0:
        return 0.0
    g = amplitude_balance(a0, a1)
    delta = gauge_invariant_mismatch(a0, a1, seam_phase)
    value = g * math.cos(0.5 * delta) ** 2
    if value < 0.0 and value > -1e-14:
        value = 0.0
    if value > 1.0 and value < 1.0 + 1e-14:
        value = 1.0
    return float(value)


def audit_seam_interface(left: complex, right: complex, seam_phase: float) -> SeamInterfaceAudit:
    a0 = _complex(left, "left")
    a1 = _complex(right, "right")
    r0 = abs(a0)
    r1 = abs(a1)
    pair_weight = r0 * r0 + r1 * r1
    overlap, defect = overlap_and_defect(a0, a1, seam_phase)
    overlap_probability = float(abs(overlap) ** 2)
    defect_probability = float(abs(defect) ** 2)
    g = amplitude_balance(a0, a1)
    delta = gauge_invariant_mismatch(a0, a1, seam_phase)
    amp = 0.25 * (r1 - r0) ** 2
    phase = r0 * r1 * math.sin(0.5 * delta) ** 2
    fuzzy = fuzzy_interface_strength(a0, a1, seam_phase)
    if pair_weight > 0.0:
        overlap_fraction = 2.0 * overlap_probability / pair_weight
        defect_fraction = 2.0 * defect_probability / pair_weight
    else:
        overlap_fraction = 0.0
        defect_fraction = 0.0
    return SeamInterfaceAudit(
        pair_weight=float(pair_weight),
        amplitude_roughness=float(amp),
        phase_mismatch_defect=float(phase),
        defect_probability=defect_probability,
        overlap_probability=overlap_probability,
        amplitude_balance=float(g),
        overlap_fraction=float(overlap_fraction),
        defect_fraction=float(defect_fraction),
        fuzzy_strength=float(fuzzy),
        mismatch=float(delta),
    )


def fuzzy_interface_profile(
    amplitudes: Sequence[complex], seam_phases: Sequence[float]
) -> np.ndarray:
    state = np.asarray(amplitudes, dtype=complex)
    phases = np.asarray(seam_phases, dtype=float)
    if state.ndim != 1 or state.size < 2 or not np.all(np.isfinite(state)):
        raise FuzzyTemporalInterfaceError("amplitudes must be a finite one-dimensional vector with N>=2")
    if float(np.linalg.norm(state)) <= 0.0:
        raise FuzzyTemporalInterfaceError("amplitudes must have positive norm")
    if phases.ndim != 1 or phases.size != state.size - 1 or not np.all(np.isfinite(phases)):
        raise FuzzyTemporalInterfaceError("seam_phases must be finite with N-1 entries")
    return np.asarray(
        [fuzzy_interface_strength(state[i], state[i + 1], phases[i]) for i in range(state.size - 1)],
        dtype=float,
    )


def chain_fuzzy_coherence(
    amplitudes: Sequence[complex], seam_phases: Sequence[float]
) -> float:
    state = np.asarray(amplitudes, dtype=complex)
    profile = fuzzy_interface_profile(state, seam_phases)
    weights = np.abs(state[:-1]) ** 2 + np.abs(state[1:]) ** 2
    denom = float(np.sum(weights))
    if not math.isfinite(denom) or denom <= 0.0:
        raise FuzzyTemporalInterfaceError("chain pair-weight denominator must be positive")
    return float(np.dot(weights, profile) / denom)


def one_seam_onsager_fuzzy_rate(
    left: complex,
    right: complex,
    seam_phase: float,
    mobility: float,
) -> float:
    a0 = _complex(left, "left")
    a1 = _complex(right, "right")
    mu = _real(mobility, "mobility")
    if mu <= 0.0:
        raise FuzzyTemporalInterfaceError("mobility must be positive")
    r0 = abs(a0)
    r1 = abs(a1)
    if r0 == 0.0 or r1 == 0.0:
        return 0.0
    delta = gauge_invariant_mismatch(a0, a1, seam_phase)
    g = amplitude_balance(a0, a1)
    k = 0.5 * mu * r0 * r1
    return float(0.5 * g * k * math.sin(delta) ** 2)


def decomposition_residual(left: complex, right: complex, seam_phase: float) -> float:
    audit = audit_seam_interface(left, right, seam_phase)
    return abs(
        audit.defect_probability
        - audit.amplitude_roughness
        - audit.phase_mismatch_defect
    )


def normalized_fraction_residual(left: complex, right: complex, seam_phase: float) -> float:
    audit = audit_seam_interface(left, right, seam_phase)
    if audit.pair_weight == 0.0:
        return 0.0
    return abs(audit.overlap_fraction + audit.defect_fraction - 1.0)


def baseline_subtraction_residual(left: complex, right: complex, seam_phase: float) -> float:
    audit = audit_seam_interface(left, right, seam_phase)
    if audit.pair_weight == 0.0:
        return 0.0
    rhs = audit.overlap_fraction - 0.5 * (1.0 - audit.amplitude_balance)
    return abs(audit.fuzzy_strength - rhs)
