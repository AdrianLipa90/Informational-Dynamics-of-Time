from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .zeta_collatz_temporal_fuzziness import (
    ZetaCollatzFuzzinessError,
    collatz_orbit,
    is_prime,
)


@dataclass(frozen=True)
class FirstMergeWitness:
    seed_left: int
    seed_right: int
    merge_value: int
    steps_left: int
    steps_right: int

    @property
    def distance(self) -> int:
        return self.steps_left + self.steps_right


@dataclass(frozen=True)
class PathContinuumDiagnostics:
    seeds: tuple[int, ...]
    first_merge_distances: tuple[int, ...]
    edge_mobilities: tuple[float, ...]
    effective_mobility: float
    low_eigenvalues: tuple[float, ...]
    continuum_targets: tuple[float, ...]
    mode_ratios: tuple[float, ...]
    mean_absolute_relative_error: float


def _validated_seed(seed: int) -> int:
    if not isinstance(seed, int) or isinstance(seed, bool) or seed <= 0:
        raise ZetaCollatzFuzzinessError("Collatz frame seed must be a positive integer")
    return seed


def first_merge_witness(
    seed_left: int,
    seed_right: int,
    *,
    max_steps: int = 10000,
) -> FirstMergeWitness:
    """Return the earliest common Collatz descendant in total path length.

    The distance is the tree/path distance to the first shared descendant:
        d_C(a,b) = min_{r,s : C^r(a)=C^s(b)} (r+s).

    Because the verified trajectories terminate at 1, a witness always exists
    inside the admitted finite-orbit domain.
    """

    a = _validated_seed(seed_left)
    b = _validated_seed(seed_right)
    orbit_a = collatz_orbit(a, max_steps=max_steps)
    orbit_b = collatz_orbit(b, max_steps=max_steps)

    positions_a = {value: idx for idx, value in enumerate(orbit_a)}
    best: tuple[int, int, int, int] | None = None
    for steps_b, value in enumerate(orbit_b):
        steps_a = positions_a.get(value)
        if steps_a is None:
            continue
        candidate = (steps_a + steps_b, steps_a, steps_b, value)
        if best is None or candidate < best:
            best = candidate

    if best is None:
        raise ZetaCollatzFuzzinessError("verified Collatz trajectories have no common descendant")

    _, steps_a, steps_b, value = best
    return FirstMergeWitness(
        seed_left=a,
        seed_right=b,
        merge_value=value,
        steps_left=steps_a,
        steps_right=steps_b,
    )


def zeta_ordered_first_merge_distances(
    seeds: Sequence[int],
    *,
    require_primes: bool = True,
    max_steps: int = 10000,
) -> np.ndarray:
    """Distances between consecutive frames in the canonical increasing seed order.

    For the Zeta-prime carrier, increasing prime order is equivalent to increasing
    log-prime spectral frequency. Composite/non-prime seeds are accepted only for
    explicit null controls when ``require_primes=False``.
    """

    values = tuple(_validated_seed(seed) for seed in seeds)
    if len(values) < 3:
        raise ZetaCollatzFuzzinessError("at least three ordered frame seeds are required")
    if len(set(values)) != len(values):
        raise ZetaCollatzFuzzinessError("frame seeds must be unique")
    if any(b <= a for a, b in zip(values, values[1:])):
        raise ZetaCollatzFuzzinessError("frame seeds must be strictly increasing")
    if require_primes and any(not is_prime(seed) for seed in values):
        raise ZetaCollatzFuzzinessError("Zeta frame carrier requires prime labels")

    distances = [
        first_merge_witness(a, b, max_steps=max_steps).distance
        for a, b in zip(values, values[1:])
    ]
    return np.asarray(distances, dtype=float)


def first_merge_edge_mobilities(distances: Sequence[float]) -> np.ndarray:
    """Map first-merge distance to a bounded positive nearest-frame mobility.

    M_e = 1/(1+d_C) keeps every admitted edge strictly positive and suppresses
    distant first merges without introducing a fitted length scale.
    """

    d = np.asarray(distances, dtype=float)
    if d.ndim != 1 or d.size < 2 or not np.all(np.isfinite(d)) or np.any(d < 0.0):
        raise ZetaCollatzFuzzinessError("first-merge distances must be a finite non-negative vector")
    return 1.0 / (1.0 + d)


def weighted_path_laplacian(
    mobilities: Sequence[float],
    *,
    normalized_interval: bool = True,
) -> np.ndarray:
    """Hermitian nearest-neighbour stiffness for a finite frame path.

    With N vertices and N-1 edge mobilities, normalized_interval=True uses
    h=1/(N-1), giving the standard Neumann-path long-wave scaling on [0,1].
    """

    m = np.asarray(mobilities, dtype=float)
    if m.ndim != 1 or m.size < 2 or not np.all(np.isfinite(m)) or np.any(m <= 0.0):
        raise ZetaCollatzFuzzinessError("path mobilities must be finite and strictly positive")

    n_vertices = m.size + 1
    h = 1.0 / m.size if normalized_interval else 1.0
    weights = m / (h * h)
    lap = np.zeros((n_vertices, n_vertices), dtype=float)
    for edge, weight in enumerate(weights):
        i = edge
        j = edge + 1
        lap[i, i] += weight
        lap[j, j] += weight
        lap[i, j] -= weight
        lap[j, i] -= weight
    return lap


def effective_path_mobility(mobilities: Sequence[float]) -> float:
    m = np.asarray(mobilities, dtype=float)
    if m.ndim != 1 or m.size < 2 or not np.all(np.isfinite(m)) or np.any(m <= 0.0):
        raise ZetaCollatzFuzzinessError("path mobilities must be finite and strictly positive")
    return float(1.0 / np.mean(1.0 / m))


def continuum_diagnostics_from_mobilities(
    mobilities: Sequence[float],
    *,
    modes: int = 5,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, float]:
    """Compare low path modes with the 1D homogenized Neumann target.

    The asymptotic target is
        lambda_m -> M_eff * (pi*m)^2,  m=1,2,...
    on the normalized interval.
    """

    m = np.asarray(mobilities, dtype=float)
    if not isinstance(modes, int) or modes <= 0:
        raise ZetaCollatzFuzzinessError("modes must be a positive integer")
    if m.ndim != 1 or m.size < modes:
        raise ZetaCollatzFuzzinessError("not enough path edges for requested low modes")

    lap = weighted_path_laplacian(m, normalized_interval=True)
    eigenvalues = np.linalg.eigvalsh(lap)
    if eigenvalues[0] < -1e-9:
        raise ZetaCollatzFuzzinessError("path Laplacian is not positive semidefinite")

    low = np.asarray(eigenvalues[1 : modes + 1], dtype=float)
    m_eff = effective_path_mobility(m)
    indices = np.arange(1, modes + 1, dtype=float)
    targets = m_eff * (math.pi * indices) ** 2
    ratios = low / targets
    error = float(np.mean(np.abs(ratios - 1.0)))
    return m_eff, low, targets, ratios, error


def zeta_collatz_path_continuum_diagnostics(
    seeds: Sequence[int],
    *,
    modes: int = 5,
    require_primes: bool = True,
    max_steps: int = 10000,
) -> PathContinuumDiagnostics:
    values = tuple(_validated_seed(seed) for seed in seeds)
    distances = zeta_ordered_first_merge_distances(
        values,
        require_primes=require_primes,
        max_steps=max_steps,
    )
    mobilities = first_merge_edge_mobilities(distances)
    m_eff, low, targets, ratios, error = continuum_diagnostics_from_mobilities(
        mobilities,
        modes=modes,
    )
    return PathContinuumDiagnostics(
        seeds=values,
        first_merge_distances=tuple(int(x) for x in distances),
        edge_mobilities=tuple(float(x) for x in mobilities),
        effective_mobility=m_eff,
        low_eigenvalues=tuple(float(x) for x in low),
        continuum_targets=tuple(float(x) for x in targets),
        mode_ratios=tuple(float(x) for x in ratios),
        mean_absolute_relative_error=error,
    )
