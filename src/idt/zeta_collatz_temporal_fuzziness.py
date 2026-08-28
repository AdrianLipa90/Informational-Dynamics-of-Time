from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class ZetaCollatzFuzzinessError(ValueError):
    pass


@dataclass(frozen=True)
class PrimeFrame:
    prime: int
    collatz_orbit: tuple[int, ...]
    log_prime: float

    @property
    def collatz_edges(self) -> frozenset[tuple[int, int]]:
        return frozenset(zip(self.collatz_orbit[:-1], self.collatz_orbit[1:]))


def is_prime(n: int) -> bool:
    if not isinstance(n, int) or isinstance(n, bool):
        return False
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    d = 3
    while d <= limit:
        if n % d == 0:
            return False
        d += 2
    return True


def collatz_orbit(n: int, *, max_steps: int = 10000) -> tuple[int, ...]:
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        raise ZetaCollatzFuzzinessError("Collatz seed must be a positive integer")
    if not isinstance(max_steps, int) or max_steps <= 0:
        raise ZetaCollatzFuzzinessError("max_steps must be a positive integer")

    orbit = [n]
    current = n
    for _ in range(max_steps):
        if current == 1:
            return tuple(orbit)
        current = current // 2 if current % 2 == 0 else 3 * current + 1
        orbit.append(current)
    raise ZetaCollatzFuzzinessError("Collatz orbit did not reach terminal anchor inside max_steps")


def build_prime_frames(primes: Sequence[int], *, max_steps: int = 10000) -> tuple[PrimeFrame, ...]:
    values = tuple(primes)
    if not values:
        raise ZetaCollatzFuzzinessError("at least one prime frame is required")
    if len(set(values)) != len(values):
        raise ZetaCollatzFuzzinessError("prime frame labels must be unique")

    frames: list[PrimeFrame] = []
    for p in values:
        if not is_prime(p):
            raise ZetaCollatzFuzzinessError(f"frame label {p!r} is not prime")
        orbit = collatz_orbit(p, max_steps=max_steps)
        frames.append(PrimeFrame(prime=p, collatz_orbit=orbit, log_prime=math.log(p)))
    return tuple(frames)


def prime_factor_amplitude(prime: int, sigma: float, tau: float) -> complex:
    if not is_prime(prime):
        raise ZetaCollatzFuzzinessError("prime must be prime")
    sigma_f = float(sigma)
    tau_f = float(tau)
    if not math.isfinite(sigma_f) or not math.isfinite(tau_f):
        raise ZetaCollatzFuzzinessError("sigma and tau must be finite")
    return complex(prime ** (-sigma_f)) * np.exp(-1j * tau_f * math.log(prime))


def collatz_overlap_matrix(frames: Sequence[PrimeFrame]) -> np.ndarray:
    frames = tuple(frames)
    if not frames:
        raise ZetaCollatzFuzzinessError("at least one frame is required")
    edge_sets = [frame.collatz_edges for frame in frames]
    if any(len(edges) == 0 for edges in edge_sets):
        raise ZetaCollatzFuzzinessError("every frame must carry at least one Collatz edge")

    n = len(frames)
    weights = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            intersection = len(edge_sets[i].intersection(edge_sets[j]))
            denom = math.sqrt(len(edge_sets[i]) * len(edge_sets[j]))
            value = intersection / denom
            weights[i, j] = value
            weights[j, i] = value
    return weights


def collatz_frame_laplacian(frames: Sequence[PrimeFrame]) -> np.ndarray:
    weights = collatz_overlap_matrix(frames)
    degree = np.sum(weights, axis=1)
    return np.diag(degree) - weights


def zeta_prime_generator(frames: Sequence[PrimeFrame], *, centred: bool = True) -> np.ndarray:
    frames = tuple(frames)
    if not frames:
        raise ZetaCollatzFuzzinessError("at least one frame is required")
    values = np.asarray([frame.log_prime for frame in frames], dtype=float)
    if centred:
        values = values - float(np.mean(values))
    return np.diag(values)


def zeta_collatz_hamiltonian(
    frames: Sequence[PrimeFrame],
    *,
    zeta_scale: float = 1.0,
    collatz_coupling: float = 1.0,
    centred_zeta: bool = True,
) -> np.ndarray:
    zeta_scale_f = float(zeta_scale)
    coupling_f = float(collatz_coupling)
    if not math.isfinite(zeta_scale_f) or not math.isfinite(coupling_f):
        raise ZetaCollatzFuzzinessError("Hamiltonian scales must be finite")

    dz = zeta_prime_generator(frames, centred=centred_zeta)
    lc = collatz_frame_laplacian(frames)
    h = zeta_scale_f * dz + coupling_f * lc
    if not np.allclose(h, h.conj().T, rtol=0.0, atol=1e-12):
        raise ZetaCollatzFuzzinessError("constructed Hamiltonian is not Hermitian")
    return h.astype(complex)


def unitary_propagator(hamiltonian: np.ndarray, delta_theta: float) -> np.ndarray:
    h = np.asarray(hamiltonian, dtype=complex)
    dt = float(delta_theta)
    if h.ndim != 2 or h.shape[0] != h.shape[1] or h.size == 0:
        raise ZetaCollatzFuzzinessError("hamiltonian must be a non-empty square matrix")
    if not np.all(np.isfinite(h)):
        raise ZetaCollatzFuzzinessError("hamiltonian must be finite")
    if not math.isfinite(dt):
        raise ZetaCollatzFuzzinessError("delta_theta must be finite")
    if not np.allclose(h, h.conj().T, rtol=0.0, atol=1e-12):
        raise ZetaCollatzFuzzinessError("hamiltonian must be Hermitian")

    eigenvalues, eigenvectors = np.linalg.eigh(h)
    phases = np.exp(-1j * eigenvalues * dt)
    return (eigenvectors * phases) @ eigenvectors.conj().T


def propagate_frame_amplitudes(
    amplitudes: Sequence[complex],
    hamiltonian: np.ndarray,
    delta_theta: float,
) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    h = np.asarray(hamiltonian, dtype=complex)
    if psi.ndim != 1 or psi.size == 0:
        raise ZetaCollatzFuzzinessError("amplitudes must be a non-empty one-dimensional vector")
    if h.shape != (psi.size, psi.size):
        raise ZetaCollatzFuzzinessError("hamiltonian dimension must match amplitude dimension")
    norm = float(np.linalg.norm(psi))
    if not math.isfinite(norm) or norm <= 0.0:
        raise ZetaCollatzFuzzinessError("amplitudes must have positive finite norm")
    psi = psi / norm
    u = unitary_propagator(h, delta_theta)
    out = u @ psi
    return out / np.linalg.norm(out)


def frame_probabilities(amplitudes: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(amplitudes, dtype=complex)
    if psi.ndim != 1 or psi.size == 0 or not np.all(np.isfinite(psi)):
        raise ZetaCollatzFuzzinessError("amplitudes must be a finite non-empty vector")
    norm2 = float(np.vdot(psi, psi).real)
    if norm2 <= 0.0:
        raise ZetaCollatzFuzzinessError("amplitudes must have positive norm")
    return (np.abs(psi) ** 2) / norm2


def frame_participation_number(amplitudes: Sequence[complex]) -> float:
    probabilities = frame_probabilities(amplitudes)
    return float(1.0 / np.sum(probabilities**2))


def temporal_fuzzy_field(
    theta_grid: Sequence[float],
    theta_anchors: Sequence[float],
    amplitudes: Sequence[complex],
    *,
    width: float,
) -> tuple[np.ndarray, np.ndarray]:
    grid = np.asarray(theta_grid, dtype=float)
    anchors = np.asarray(theta_anchors, dtype=float)
    psi = np.asarray(amplitudes, dtype=complex)
    width_f = float(width)

    if grid.ndim != 1 or grid.size < 2 or not np.all(np.isfinite(grid)):
        raise ZetaCollatzFuzzinessError("theta_grid must be a finite one-dimensional grid")
    if np.any(np.diff(grid) <= 0.0):
        raise ZetaCollatzFuzzinessError("theta_grid must be strictly increasing")
    if anchors.ndim != 1 or anchors.shape != psi.shape or anchors.size == 0:
        raise ZetaCollatzFuzzinessError("theta_anchors and amplitudes must have equal non-empty shape")
    if not np.all(np.isfinite(anchors)) or not np.all(np.diff(anchors) > 0.0):
        raise ZetaCollatzFuzzinessError("theta_anchors must be finite and strictly increasing")
    if not np.all(np.isfinite(psi)):
        raise ZetaCollatzFuzzinessError("amplitudes must be finite")
    if not math.isfinite(width_f) or width_f <= 0.0:
        raise ZetaCollatzFuzzinessError("width must be positive and finite")

    probabilities = frame_probabilities(psi)
    psi = psi / math.sqrt(float(np.vdot(psi, psi).real))

    prefactor = (math.pi * width_f**2) ** (-0.25)
    basis = prefactor * np.exp(-((grid[:, None] - anchors[None, :]) ** 2) / (2.0 * width_f**2))
    field = basis @ psi
    density = np.abs(field) ** 2
    integral = float(np.trapezoid(density, grid))
    if not math.isfinite(integral) or integral <= 0.0:
        raise ZetaCollatzFuzzinessError("continuous field normalization failed")
    field = field / math.sqrt(integral)
    density = np.abs(field) ** 2

    # Keep a separately normalized incoherent frame occupancy for diagnostics.
    _ = probabilities
    return field, density


def temporal_fuzziness_moments(theta_grid: Sequence[float], density: Sequence[float]) -> tuple[float, float]:
    grid = np.asarray(theta_grid, dtype=float)
    rho = np.asarray(density, dtype=float)
    if grid.ndim != 1 or rho.ndim != 1 or grid.shape != rho.shape or grid.size < 2:
        raise ZetaCollatzFuzzinessError("grid and density must have equal one-dimensional shape")
    if np.any(np.diff(grid) <= 0.0) or not np.all(np.isfinite(grid)) or not np.all(np.isfinite(rho)):
        raise ZetaCollatzFuzzinessError("grid and density must be finite with increasing grid")
    if np.any(rho < -1e-15):
        raise ZetaCollatzFuzzinessError("density must be non-negative")

    normalization = float(np.trapezoid(rho, grid))
    if normalization <= 0.0:
        raise ZetaCollatzFuzzinessError("density must have positive integral")
    rho = rho / normalization
    mean = float(np.trapezoid(grid * rho, grid))
    variance = float(np.trapezoid(((grid - mean) ** 2) * rho, grid))
    return mean, max(0.0, variance)
