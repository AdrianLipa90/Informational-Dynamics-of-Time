from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .zeta_collatz_frame_continuum import (
    first_merge_edge_mobilities,
    weighted_path_laplacian,
    zeta_ordered_first_merge_distances,
)
from .zeta_collatz_temporal_fuzziness import ZetaCollatzFuzzinessError, is_prime


@dataclass(frozen=True)
class JointAlignmentDiagnostics:
    seeds: tuple[int, ...]
    frequencies: tuple[float, ...]
    edge_mobilities: tuple[float, ...]
    commutator_score: float
    hamiltonian_eigenvalues: tuple[float, ...]


def _ordered_seed_tuple(seeds: Sequence[int], *, require_primes: bool) -> tuple[int, ...]:
    values = tuple(seeds)
    if len(values) < 4:
        raise ZetaCollatzFuzzinessError("joint discriminator requires at least four ordered seeds")
    if any(not isinstance(v, int) or isinstance(v, bool) or v <= 0 for v in values):
        raise ZetaCollatzFuzzinessError("joint discriminator seeds must be positive integers")
    if len(set(values)) != len(values) or any(b <= a for a, b in zip(values, values[1:])):
        raise ZetaCollatzFuzzinessError("joint discriminator seeds must be unique and strictly increasing")
    if require_primes and any(not is_prime(v) for v in values):
        raise ZetaCollatzFuzzinessError("Zeta joint discriminator requires prime labels")
    return values


def centred_log_frequency_operator(seeds: Sequence[int], *, require_primes: bool = True) -> np.ndarray:
    values = _ordered_seed_tuple(seeds, require_primes=require_primes)
    frequencies = np.log(np.asarray(values, dtype=float))
    frequencies = frequencies - float(np.mean(frequencies))
    return np.diag(frequencies)


def centred_path_operator_from_mobilities(mobilities: Sequence[float]) -> np.ndarray:
    lap = weighted_path_laplacian(mobilities, normalized_interval=False)
    n = lap.shape[0]
    return lap - (float(np.trace(lap)) / n) * np.eye(n)


def _frobenius_unit(operator: np.ndarray, *, name: str) -> np.ndarray:
    op = np.asarray(operator, dtype=float)
    norm = float(np.linalg.norm(op, ord="fro"))
    if not math.isfinite(norm) or norm <= 0.0:
        raise ZetaCollatzFuzzinessError(f"{name} must have positive finite Frobenius norm")
    return op / norm


def normalized_commutator_score(
    frequency_operator: np.ndarray,
    path_operator: np.ndarray,
) -> float:
    d = _frobenius_unit(frequency_operator, name="frequency operator")
    k = _frobenius_unit(path_operator, name="path operator")
    if d.shape != k.shape:
        raise ZetaCollatzFuzzinessError("frequency and path operators must have the same shape")
    commutator = d @ k - k @ d
    return float(np.linalg.norm(commutator, ord="fro"))


def balanced_joint_hamiltonian(
    frequency_operator: np.ndarray,
    path_operator: np.ndarray,
) -> np.ndarray:
    d = _frobenius_unit(frequency_operator, name="frequency operator")
    k = _frobenius_unit(path_operator, name="path operator")
    if d.shape != k.shape:
        raise ZetaCollatzFuzzinessError("frequency and path operators must have the same shape")
    h = d + k
    if not np.allclose(h, h.T, rtol=0.0, atol=1e-13):
        raise ZetaCollatzFuzzinessError("balanced joint Hamiltonian must be Hermitian")
    return h


def joint_alignment_diagnostics(
    seeds: Sequence[int],
    *,
    require_primes: bool = True,
    max_steps: int = 10000,
) -> JointAlignmentDiagnostics:
    values = _ordered_seed_tuple(seeds, require_primes=require_primes)
    distances = zeta_ordered_first_merge_distances(
        values,
        require_primes=require_primes,
        max_steps=max_steps,
    )
    mobilities = first_merge_edge_mobilities(distances)
    d = centred_log_frequency_operator(values, require_primes=require_primes)
    k = centred_path_operator_from_mobilities(mobilities)
    score = normalized_commutator_score(d, k)
    h = balanced_joint_hamiltonian(d, k)
    eigenvalues = np.linalg.eigvalsh(h)
    return JointAlignmentDiagnostics(
        seeds=values,
        frequencies=tuple(float(math.log(v)) for v in values),
        edge_mobilities=tuple(float(v) for v in mobilities),
        commutator_score=score,
        hamiltonian_eigenvalues=tuple(float(v) for v in eigenvalues),
    )


def permuted_mobility_commutator_scores(
    seeds: Sequence[int],
    mobilities: Sequence[float],
    *,
    permutations: int = 128,
    rng_seed: int = 20260828,
    require_primes: bool = True,
) -> np.ndarray:
    values = _ordered_seed_tuple(seeds, require_primes=require_primes)
    mobility = np.asarray(mobilities, dtype=float)
    if mobility.ndim != 1 or mobility.size != len(values) - 1:
        raise ZetaCollatzFuzzinessError("mobility vector must have one entry per neighboring frame pair")
    if not np.all(np.isfinite(mobility)) or np.any(mobility <= 0.0):
        raise ZetaCollatzFuzzinessError("mobility vector must be finite and strictly positive")
    if not isinstance(permutations, int) or permutations <= 0:
        raise ZetaCollatzFuzzinessError("permutations must be a positive integer")

    d = centred_log_frequency_operator(values, require_primes=require_primes)
    rng = np.random.default_rng(int(rng_seed))
    scores = np.empty(permutations, dtype=float)
    for idx in range(permutations):
        shuffled = mobility.copy()
        rng.shuffle(shuffled)
        k = centred_path_operator_from_mobilities(shuffled)
        scores[idx] = normalized_commutator_score(d, k)
    return scores


def empirical_lower_tail_fraction(value: float, null_values: Sequence[float]) -> float:
    x = float(value)
    null = np.asarray(null_values, dtype=float)
    if not math.isfinite(x) or null.ndim != 1 or null.size == 0 or not np.all(np.isfinite(null)):
        raise ZetaCollatzFuzzinessError("alignment percentile inputs must be finite")
    return float(np.mean(null <= x))
