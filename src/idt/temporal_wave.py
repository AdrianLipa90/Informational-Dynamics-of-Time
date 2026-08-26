from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .relational_kinetics import pair_mobility


class TemporalWaveError(ValueError):
    pass


def _finite_complex_vector(values, *, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=complex)
    if arr.ndim != 1 or arr.size == 0:
        raise TemporalWaveError(f"{name} must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise TemporalWaveError(f"{name} must be finite")
    return arr


def _finite_nonnegative(x: float, *, name: str) -> float:
    value = float(x)
    if not math.isfinite(value) or value < 0.0:
        raise TemporalWaveError(f"{name} must be finite and non-negative")
    return value


def _validate_edges(n_nodes: int, edges: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    n = int(n_nodes)
    if n <= 0:
        raise TemporalWaveError("n_nodes must be positive")
    out: list[tuple[int, int]] = []
    for raw_a, raw_b in edges:
        a, b = int(raw_a), int(raw_b)
        if a == b or a < 0 or b < 0 or a >= n or b >= n:
            raise TemporalWaveError("edges must connect two distinct admitted node indices")
        out.append((a, b))
    if not out:
        raise TemporalWaveError("at least one edge is required")
    return out


def _unit_links(links: Sequence[complex], n_edges: int, *, atol: float = 1e-12) -> np.ndarray:
    arr = _finite_complex_vector(links, name="links")
    if arr.size != n_edges:
        raise TemporalWaveError("one U(1) link is required per edge")
    if not np.allclose(np.abs(arr), 1.0, atol=atol, rtol=0.0):
        raise TemporalWaveError("links must lie on U(1)")
    return arr / np.abs(arr)


def _positive_weights(weights: Sequence[float], n_edges: int) -> np.ndarray:
    arr = np.asarray(weights, dtype=float)
    if arr.ndim != 1 or arr.size != n_edges:
        raise TemporalWaveError("one edge weight is required per edge")
    if not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise TemporalWaveError("edge weights must be finite and strictly positive")
    return arr


def gauge_incidence_matrix(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
) -> np.ndarray:
    """Return D_L with (D_L q)_e = q_b - L_ab q_a for each oriented edge a->b."""
    edge_list = _validate_edges(n_nodes, edges)
    link_arr = _unit_links(links, len(edge_list))
    D = np.zeros((len(edge_list), int(n_nodes)), dtype=complex)
    for idx, ((a, b), link) in enumerate(zip(edge_list, link_arr)):
        D[idx, a] = -link
        D[idx, b] = 1.0
    return D


def gauge_laplacian(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    weights: Sequence[float],
) -> np.ndarray:
    """Hermitian positive-semidefinite K_L = D_L^† W D_L."""
    edge_list = _validate_edges(n_nodes, edges)
    link_arr = _unit_links(links, len(edge_list))
    weight_arr = _positive_weights(weights, len(edge_list))
    D = gauge_incidence_matrix(n_nodes, edge_list, link_arr)
    K = D.conj().T @ (weight_arr[:, None] * D)
    return 0.5 * (K + K.conj().T)


def mobility_edge_weights(
    edges: Sequence[tuple[int, int]],
    rho: Sequence[float],
    eta: Sequence[float],
) -> np.ndarray:
    """Candidate edge weights w_ab=M_ab from the existing relational-mobility primitive."""
    rho_arr = np.asarray(rho, dtype=float)
    eta_arr = np.asarray(eta, dtype=float)
    if rho_arr.ndim != 1 or eta_arr.ndim != 1 or rho_arr.size != eta_arr.size or rho_arr.size == 0:
        raise TemporalWaveError("rho and eta must be non-empty one-dimensional arrays of equal length")
    edge_list = _validate_edges(rho_arr.size, edges)
    return np.asarray(
        [pair_mobility(rho_arr[a], rho_arr[b], eta_arr[a], eta_arr[b]) for a, b in edge_list],
        dtype=float,
    )


def gauge_transform_links(
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    node_phases: Sequence[float],
) -> np.ndarray:
    """Apply L_ab -> exp(i(chi_b-chi_a)) L_ab."""
    phases = np.asarray(node_phases, dtype=float)
    if phases.ndim != 1 or phases.size == 0 or not np.all(np.isfinite(phases)):
        raise TemporalWaveError("node_phases must be a finite non-empty one-dimensional array")
    edge_list = _validate_edges(phases.size, edges)
    link_arr = _unit_links(links, len(edge_list))
    return np.asarray(
        [np.exp(1j * (phases[b] - phases[a])) * link for (a, b), link in zip(edge_list, link_arr)],
        dtype=complex,
    )


def damped_wave_rhs(q, p, K, *, damping: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    """First-order Kähler-form candidate: qdot=-p, pdot=Kq-nu Kp."""
    qv = _finite_complex_vector(q, name="q")
    pv = _finite_complex_vector(p, name="p")
    if qv.shape != pv.shape:
        raise TemporalWaveError("q and p must have the same shape")
    op = np.asarray(K, dtype=complex)
    if op.shape != (qv.size, qv.size):
        raise TemporalWaveError("K must be square with dimension matching q and p")
    if not np.all(np.isfinite(op.real)) or not np.all(np.isfinite(op.imag)):
        raise TemporalWaveError("K must be finite")
    if not np.allclose(op, op.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalWaveError("K must be Hermitian")
    nu = _finite_nonnegative(damping, name="damping")
    return -pv, op @ qv - nu * (op @ pv)


def wave_energy(q, p, K) -> float:
    qv = _finite_complex_vector(q, name="q")
    pv = _finite_complex_vector(p, name="p")
    op = np.asarray(K, dtype=complex)
    if qv.shape != pv.shape or op.shape != (qv.size, qv.size):
        raise TemporalWaveError("wave energy dimensions are inconsistent")
    value = 0.5 * (np.vdot(pv, pv) + np.vdot(qv, op @ qv))
    if abs(value.imag) > 1e-10:
        raise TemporalWaveError("wave energy must be real for an admitted Hermitian operator")
    return float(value.real)


def wave_energy_derivative(p, K, *, damping: float) -> float:
    pv = _finite_complex_vector(p, name="p")
    op = np.asarray(K, dtype=complex)
    if op.shape != (pv.size, pv.size):
        raise TemporalWaveError("K dimension must match p")
    nu = _finite_nonnegative(damping, name="damping")
    value = -nu * np.vdot(pv, op @ pv)
    return float(value.real)


def modal_frequencies(eigenvalues: Sequence[float], *, damping: float = 0.0) -> np.ndarray:
    """Positive-frequency branch for q¨ + nu K q˙ + K q = 0."""
    lam = np.asarray(eigenvalues, dtype=float)
    if lam.ndim != 1 or not np.all(np.isfinite(lam)) or np.any(lam < -1e-12):
        raise TemporalWaveError("eigenvalues must be finite and non-negative")
    lam = np.maximum(lam, 0.0)
    nu = _finite_nonnegative(damping, name="damping")
    radicand = lam - 0.25 * (nu * lam) ** 2
    return np.sqrt(radicand.astype(complex)) - 0.5j * nu * lam


def uniform_ring(
    n_nodes: int,
    *,
    diffusivity: float,
    holonomy_phase: float = 0.0,
) -> tuple[list[tuple[int, int]], np.ndarray, np.ndarray]:
    """Uniform N-cycle with total link holonomy exp(i*phi) and continuum scaling w=D N^2."""
    n = int(n_nodes)
    if n < 3:
        raise TemporalWaveError("uniform ring requires at least three nodes")
    D = float(diffusivity)
    phi = float(holonomy_phase)
    if not math.isfinite(D) or D <= 0.0 or not math.isfinite(phi):
        raise TemporalWaveError("diffusivity must be positive finite and holonomy_phase finite")
    edges = [(j, (j + 1) % n) for j in range(n)]
    links = np.full(n, np.exp(1j * phi / n), dtype=complex)
    weights = np.full(n, D * n * n, dtype=float)
    return edges, links, weights


def analytic_ring_spectrum(
    n_nodes: int,
    *,
    diffusivity: float,
    holonomy_phase: float = 0.0,
) -> np.ndarray:
    n = int(n_nodes)
    if n < 3:
        raise TemporalWaveError("analytic ring requires at least three nodes")
    D = float(diffusivity)
    phi = float(holonomy_phase)
    if not math.isfinite(D) or D <= 0.0 or not math.isfinite(phi):
        raise TemporalWaveError("diffusivity must be positive finite and holonomy_phase finite")
    m = np.arange(n, dtype=float)
    return 4.0 * D * n * n * np.sin((2.0 * math.pi * m - phi) / (2.0 * n)) ** 2
