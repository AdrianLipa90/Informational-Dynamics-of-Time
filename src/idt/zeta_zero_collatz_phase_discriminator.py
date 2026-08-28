from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Sequence

import numpy as np

from .zeta_collatz_frame_continuum import (
    first_merge_edge_mobilities,
    zeta_ordered_first_merge_distances,
)
from .zeta_collatz_temporal_fuzziness import ZetaCollatzFuzzinessError, is_prime


REFERENCE_ZERO_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "reference"
    / "riemann_zeta_zeros_first20_v0_1.csv"
)


def load_reference_zero_ordinates(path: Path | None = None) -> np.ndarray:
    source = Path(path) if path is not None else REFERENCE_ZERO_FILE
    values: list[float] = []
    with source.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            real = float(row["real_part"])
            gamma = float(row["imaginary_part"])
            if not math.isfinite(real) or not math.isfinite(gamma):
                raise ZetaCollatzFuzzinessError("zeta-zero fixture must be finite")
            if not math.isclose(real, 0.5, rel_tol=0.0, abs_tol=1e-15):
                raise ZetaCollatzFuzzinessError("reference zero fixture must remain on its recorded critical line")
            values.append(gamma)
    if not values or any(b <= a for a, b in zip(values, values[1:])):
        raise ZetaCollatzFuzzinessError("zeta-zero ordinates must be non-empty and strictly increasing")
    return np.asarray(values, dtype=float)


def _ordered_primes(primes: Sequence[int]) -> tuple[int, ...]:
    values = tuple(primes)
    if len(values) < 4:
        raise ZetaCollatzFuzzinessError("phase discriminator requires at least four primes")
    if len(set(values)) != len(values) or any(b <= a for a, b in zip(values, values[1:])):
        raise ZetaCollatzFuzzinessError("prime window must be unique and strictly increasing")
    if any(not is_prime(v) for v in values):
        raise ZetaCollatzFuzzinessError("phase discriminator requires prime labels")
    return values


def prime_gap_phase_texture(primes: Sequence[int], gamma: float) -> np.ndarray:
    """Exact neighboring Euler-factor phase texture at a fixed ordinate.

    For z_p(sigma,tau)=p^{-sigma} exp(-i tau ln p), neighboring prime-factor
    phase difference is exp[-i gamma (ln p_{k+1}-ln p_k)].
    """

    values = _ordered_primes(primes)
    gamma_f = float(gamma)
    if not math.isfinite(gamma_f):
        raise ZetaCollatzFuzzinessError("gamma must be finite")
    logp = np.log(np.asarray(values, dtype=float))
    return np.exp(-1j * gamma_f * np.diff(logp))


def centred_collatz_mobility(primes: Sequence[int]) -> np.ndarray:
    values = _ordered_primes(primes)
    distances = zeta_ordered_first_merge_distances(values)
    mobility = first_merge_edge_mobilities(distances)
    centred = mobility - float(np.mean(mobility))
    std = float(np.std(centred))
    if not math.isfinite(std) or std <= 0.0:
        raise ZetaCollatzFuzzinessError("Collatz mobility window has zero variance")
    return centred / std


def zeta_phase_collatz_coherence(primes: Sequence[int], gamma: float) -> float:
    mobility = centred_collatz_mobility(primes)
    phase = prime_gap_phase_texture(primes, gamma)
    if phase.shape != mobility.shape:
        raise ZetaCollatzFuzzinessError("phase texture and mobility must have equal shape")
    return float(abs(np.mean(mobility * phase)))


def symmetric_local_frequency_controls(
    gamma: float,
    *,
    offsets: Sequence[float] = (-1.0, -0.5, -0.25, -0.125, 0.125, 0.25, 0.5, 1.0),
) -> np.ndarray:
    gamma_f = float(gamma)
    delta = np.asarray(tuple(offsets), dtype=float)
    if delta.ndim != 1 or delta.size == 0 or not np.all(np.isfinite(delta)):
        raise ZetaCollatzFuzzinessError("frequency-control offsets must be finite and non-empty")
    if np.any(delta == 0.0):
        raise ZetaCollatzFuzzinessError("frequency-control offsets must exclude zero")
    if not np.allclose(np.sort(delta), np.sort(-delta), rtol=0.0, atol=1e-15):
        raise ZetaCollatzFuzzinessError("frequency controls must be symmetric around gamma")
    controls = gamma_f + delta
    if np.any(controls <= 0.0):
        raise ZetaCollatzFuzzinessError("frequency controls must remain positive")
    return controls


def local_zero_phase_contrast(
    primes: Sequence[int],
    gamma: float,
    *,
    offsets: Sequence[float] = (-1.0, -0.5, -0.25, -0.125, 0.125, 0.25, 0.5, 1.0),
) -> tuple[float, float, float]:
    """Return zero score, local-control mean, and their ratio.

    Symmetric nearby frequency controls remove the smooth frequency dependence
    of the phase-coherence statistic without fitting offsets to any target zero.
    """

    zero_score = zeta_phase_collatz_coherence(primes, gamma)
    controls = symmetric_local_frequency_controls(gamma, offsets=offsets)
    control_scores = np.asarray(
        [zeta_phase_collatz_coherence(primes, value) for value in controls],
        dtype=float,
    )
    control_mean = float(np.mean(control_scores))
    if control_mean <= 0.0:
        raise ZetaCollatzFuzzinessError("local control mean must be positive")
    return zero_score, control_mean, float(zero_score / control_mean)


def reference_zero_phase_ratios(primes: Sequence[int]) -> np.ndarray:
    zeros = load_reference_zero_ordinates()
    return np.asarray([local_zero_phase_contrast(primes, gamma)[2] for gamma in zeros], dtype=float)
