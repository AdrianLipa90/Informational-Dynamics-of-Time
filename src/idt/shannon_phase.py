from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .kahler_time import kappa


class ShannonPhaseError(ValueError):
    pass


def _probability_vector(p: Sequence[float]) -> np.ndarray:
    arr = np.asarray(p, dtype=float)
    if arr.ndim != 1 or arr.size == 0:
        raise ShannonPhaseError("probability vector must be one-dimensional and non-empty")
    if not np.all(np.isfinite(arr)):
        raise ShannonPhaseError("probability vector must be finite")
    if np.any(arr < 0.0):
        raise ShannonPhaseError("probabilities must be non-negative")
    total = float(arr.sum())
    if total <= 0.0:
        raise ShannonPhaseError("probability vector must have positive total mass")
    arr = arr / total
    return arr


def shannon_entropy(p: Sequence[float], *, base: float = 2.0) -> float:
    """Shannon entropy of a relational state distribution.

    Zero-probability terms contribute zero. The default unit is bits.
    """
    if base <= 0.0 or math.isclose(base, 1.0):
        raise ShannonPhaseError("logarithm base must be positive and different from one")
    arr = _probability_vector(p)
    nz = arr[arr > 0.0]
    return float(-np.sum(nz * (np.log(nz) / math.log(base))))


def entropy_difference(p_a: Sequence[float], p_b: Sequence[float], *, base: float = 2.0) -> float:
    return shannon_entropy(p_b, base=base) - shannon_entropy(p_a, base=base)


def _normalized_state(psi: Sequence[complex]) -> np.ndarray:
    arr = np.asarray(psi, dtype=complex)
    if arr.ndim != 1 or arr.size == 0:
        raise ShannonPhaseError("state vector must be one-dimensional and non-empty")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise ShannonPhaseError("state vector must be finite")
    norm = float(np.linalg.norm(arr))
    if norm <= 0.0:
        raise ShannonPhaseError("state vector must have non-zero norm")
    return arr / norm


def pancharatnam_link(psi_a: Sequence[complex], psi_b: Sequence[complex], *, overlap_tol: float = 1e-14) -> complex:
    """Return the unit U(1) transporter from the normalized overlap.

    The link is gauge-covariant. A closed product of links is gauge-invariant.
    """
    a = _normalized_state(psi_a)
    b = _normalized_state(psi_b)
    overlap = np.vdot(a, b)
    mag = abs(overlap)
    if mag <= overlap_tol:
        raise ShannonPhaseError("Pancharatnam link is undefined for vanishing overlap")
    return complex(overlap / mag)


def wrap_phase(theta: float) -> float:
    return float(math.atan2(math.sin(theta), math.cos(theta)))


@dataclass(frozen=True)
class TransitionLink:
    geometric_link: complex
    entropy_difference_bits: float
    entropy_production_bits: float
    composite_link: complex
    phase_rad: float


def temporal_transition_link(
    psi_a: Sequence[complex],
    psi_b: Sequence[complex],
    p_a: Sequence[float],
    p_b: Sequence[float],
    *,
    entropy_production_bits: float = 0.0,
    kappa_value: float | None = None,
) -> TransitionLink:
    """Candidate Shannon-Pancharatnam transition link.

    L_ab = G_ab exp(i κ [ΔH_ab + σ_ab]).

    ΔH is an exact state-function difference. σ is a transition-associated
    non-exact information-production increment carried explicitly on the edge.
    """
    if not math.isfinite(entropy_production_bits):
        raise ShannonPhaseError("entropy production increment must be finite")
    kap = kappa() if kappa_value is None else float(kappa_value)
    if not math.isfinite(kap):
        raise ShannonPhaseError("kappa must be finite")
    geom = pancharatnam_link(psi_a, psi_b)
    dH = entropy_difference(p_a, p_b, base=2.0)
    phase_factor = cmath.exp(1j * kap * (dH + entropy_production_bits))
    composite = geom * phase_factor
    return TransitionLink(
        geometric_link=geom,
        entropy_difference_bits=dH,
        entropy_production_bits=float(entropy_production_bits),
        composite_link=composite,
        phase_rad=wrap_phase(cmath.phase(composite)),
    )


def closed_cycle_link(
    states: Sequence[Sequence[complex]],
    probabilities: Sequence[Sequence[float]],
    *,
    entropy_production_bits: Iterable[float] | None = None,
    kappa_value: float | None = None,
) -> complex:
    """Return the closed product over the cycle s_0→...→s_n→s_0."""
    if len(states) != len(probabilities):
        raise ShannonPhaseError("states and probabilities must have the same length")
    if len(states) < 2:
        raise ShannonPhaseError("closed cycle needs at least two vertices")
    n = len(states)
    sigmas = [0.0] * n if entropy_production_bits is None else [float(x) for x in entropy_production_bits]
    if len(sigmas) != n:
        raise ShannonPhaseError("one entropy-production increment is required per directed cycle edge")
    product = 1.0 + 0.0j
    for i in range(n):
        j = (i + 1) % n
        product *= temporal_transition_link(
            states[i],
            states[j],
            probabilities[i],
            probabilities[j],
            entropy_production_bits=sigmas[i],
            kappa_value=kappa_value,
        ).composite_link
    return complex(product / abs(product))


def closed_geometric_link(states: Sequence[Sequence[complex]]) -> complex:
    if len(states) < 2:
        raise ShannonPhaseError("closed cycle needs at least two vertices")
    product = 1.0 + 0.0j
    for i in range(len(states)):
        product *= pancharatnam_link(states[i], states[(i + 1) % len(states)])
    return complex(product / abs(product))


def transition_affinity_bits(p_forward: float, p_reverse: float) -> float:
    """Directed path affinity sigma = log2(P_fwd / P_rev).

    Both transition probabilities/rates must be finite and strictly positive.
    The function is deliberately agnostic about whether the supplied positive
    quantities are normalized conditional probabilities or proportional rates;
    only their declared forward/reverse ratio is used.
    """
    pf = float(p_forward)
    pr = float(p_reverse)
    if not (math.isfinite(pf) and math.isfinite(pr)):
        raise ShannonPhaseError("forward and reverse transition weights must be finite")
    if pf <= 0.0 or pr <= 0.0:
        raise ShannonPhaseError("forward and reverse transition weights must be strictly positive")
    return float(math.log2(pf / pr))


def cycle_affinity_bits(forward: Sequence[float], reverse: Sequence[float]) -> float:
    """Sum the directed affinities around one declared cycle."""
    if len(forward) != len(reverse):
        raise ShannonPhaseError("forward and reverse cycle arrays must have the same length")
    if len(forward) == 0:
        raise ShannonPhaseError("cycle affinity requires at least one directed edge")
    return float(sum(transition_affinity_bits(pf, pr) for pf, pr in zip(forward, reverse)))


def transition_link_from_affinity(
    psi_a: Sequence[complex],
    psi_b: Sequence[complex],
    p_a: Sequence[float],
    p_b: Sequence[float],
    *,
    p_forward: float,
    p_reverse: float,
    kappa_value: float | None = None,
) -> TransitionLink:
    """Close the candidate edge sigma from a forward/reverse path asymmetry."""
    sigma = transition_affinity_bits(p_forward, p_reverse)
    return temporal_transition_link(
        psi_a,
        psi_b,
        p_a,
        p_b,
        entropy_production_bits=sigma,
        kappa_value=kappa_value,
    )
