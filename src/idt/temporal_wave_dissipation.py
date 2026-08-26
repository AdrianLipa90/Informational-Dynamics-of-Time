from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .relational_kinetics import pair_mobility
from .temporal_wave import TemporalWaveError, gauge_laplacian, mobility_edge_weights


def _edges(n_nodes: int, edges: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    n = int(n_nodes)
    if n <= 0:
        raise TemporalWaveError("n_nodes must be positive")
    out: list[tuple[int, int]] = []
    for raw_a, raw_b in edges:
        a, b = int(raw_a), int(raw_b)
        if a == b or a < 0 or b < 0 or a >= n or b >= n:
            raise TemporalWaveError("edges must connect distinct admitted node indices")
        out.append((a, b))
    if not out:
        raise TemporalWaveError("at least one edge is required")
    return out


def _positive_field(values: Sequence[float], n_nodes: int, *, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size != int(n_nodes):
        raise TemporalWaveError(f"{name} must be a one-dimensional field matching n_nodes")
    if not np.all(np.isfinite(arr)) or np.any(arr <= 0.0):
        raise TemporalWaveError(f"{name} must be finite and strictly positive")
    return arr


def mobility_gauge_laplacian(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    rho: Sequence[float],
    eta: Sequence[float],
) -> np.ndarray:
    """Gauge-covariant Dirichlet operator with the existing pair mobility M_ab."""
    edge_list = _edges(n_nodes, edges)
    rho_arr = _positive_field(rho, n_nodes, name="rho")
    eta_arr = _positive_field(eta, n_nodes, name="eta")
    weights = mobility_edge_weights(edge_list, rho_arr, eta_arr)
    return gauge_laplacian(n_nodes, edge_list, links, weights)


def zero_drive_rate_generator(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    rho: Sequence[float],
    eta: Sequence[float],
) -> np.ndarray:
    """Symmetric continuous-time kinetic generator implied by A_ab=0.

    EQ-T009D gives W_a->b=W_b->a=M_ab when the antisymmetric edge drive is zero.
    Each undirected edge is supplied once.
    """
    edge_list = _edges(n_nodes, edges)
    rho_arr = _positive_field(rho, n_nodes, name="rho")
    eta_arr = _positive_field(eta, n_nodes, name="eta")
    G = np.zeros((int(n_nodes), int(n_nodes)), dtype=float)
    for a, b in edge_list:
        rate = pair_mobility(rho_arr[a], rho_arr[b], eta_arr[a], eta_arr[b])
        G[a, b] += rate
        G[b, a] += rate
        G[a, a] -= rate
        G[b, b] -= rate
    return G


def viscosity_edge_weights(
    edges: Sequence[tuple[int, int]],
    eta: Sequence[float],
) -> np.ndarray:
    """Reuse the symmetric pair viscosity eta_bar_ab=(eta_a+eta_b)/2 from EQ-T009C."""
    eta_arr = np.asarray(eta, dtype=float)
    if eta_arr.ndim != 1 or eta_arr.size == 0:
        raise TemporalWaveError("eta must be a non-empty one-dimensional field")
    if not np.all(np.isfinite(eta_arr)) or np.any(eta_arr <= 0.0):
        raise TemporalWaveError("eta must be finite and strictly positive")
    edge_list = _edges(eta_arr.size, edges)
    return np.asarray([0.5 * (eta_arr[a] + eta_arr[b]) for a, b in edge_list], dtype=float)


def viscous_damping_laplacian(
    n_nodes: int,
    edges: Sequence[tuple[int, int]],
    links: Sequence[complex],
    eta: Sequence[float],
) -> np.ndarray:
    """Candidate C_eta=D_L^dagger diag(eta_bar_ab) D_L."""
    edge_list = _edges(n_nodes, edges)
    eta_arr = _positive_field(eta, n_nodes, name="eta")
    return gauge_laplacian(n_nodes, edge_list, links, viscosity_edge_weights(edge_list, eta_arr))


def edge_scalar_damping_ratios(
    edges: Sequence[tuple[int, int]],
    rho: Sequence[float],
    eta: Sequence[float],
) -> np.ndarray:
    """Return local ratios eta_bar_ab/M_ab for C_edge=nu K_edge factorization."""
    rho_arr = np.asarray(rho, dtype=float)
    eta_arr = np.asarray(eta, dtype=float)
    if rho_arr.ndim != 1 or eta_arr.ndim != 1 or rho_arr.size != eta_arr.size or rho_arr.size == 0:
        raise TemporalWaveError("rho and eta must be non-empty fields of equal length")
    edge_list = _edges(rho_arr.size, edges)
    mobility = mobility_edge_weights(edge_list, rho_arr, eta_arr)
    viscous = viscosity_edge_weights(edge_list, eta_arr)
    return viscous / mobility


def scalar_damping_if_edge_factorable(
    edges: Sequence[tuple[int, int]],
    rho: Sequence[float],
    eta: Sequence[float],
    *,
    atol: float = 1e-12,
    rtol: float = 1e-12,
) -> float:
    """Return one nu only when eta_bar_ab=nu M_ab on every declared edge."""
    ratios = edge_scalar_damping_ratios(edges, rho, eta)
    if not np.allclose(ratios, ratios[0], atol=atol, rtol=rtol):
        raise TemporalWaveError("heterogeneous edge damping cannot be represented by one scalar nu")
    return float(ratios[0])


def _psd_operator(op, dimension: int, *, name: str) -> np.ndarray:
    arr = np.asarray(op, dtype=complex)
    if arr.shape != (dimension, dimension):
        raise TemporalWaveError(f"{name} must match q and p dimensions")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise TemporalWaveError(f"{name} must be finite")
    if not np.allclose(arr, arr.conj().T, atol=1e-12, rtol=0.0):
        raise TemporalWaveError(f"{name} must be Hermitian")
    if float(np.min(np.linalg.eigvalsh(arr))) < -1e-11:
        raise TemporalWaveError(f"{name} must be positive semidefinite")
    return arr


def operator_damped_wave_rhs(q, p, K, C) -> tuple[np.ndarray, np.ndarray]:
    """Operator-damped candidate qdot=-p, pdot=Kq-Cp."""
    qv = np.asarray(q, dtype=complex)
    pv = np.asarray(p, dtype=complex)
    if qv.ndim != 1 or pv.ndim != 1 or qv.size == 0 or qv.shape != pv.shape:
        raise TemporalWaveError("q and p must be finite non-empty vectors of equal shape")
    if not np.all(np.isfinite(qv.real)) or not np.all(np.isfinite(qv.imag)):
        raise TemporalWaveError("q must be finite")
    if not np.all(np.isfinite(pv.real)) or not np.all(np.isfinite(pv.imag)):
        raise TemporalWaveError("p must be finite")
    stiffness = _psd_operator(K, qv.size, name="K")
    damping = _psd_operator(C, qv.size, name="C")
    return -pv, stiffness @ qv - damping @ pv


def operator_wave_energy_derivative(p, C) -> float:
    """Return dH/dlambda=-p^dagger C p <= 0 for admitted C."""
    pv = np.asarray(p, dtype=complex)
    if pv.ndim != 1 or pv.size == 0 or not np.all(np.isfinite(pv.real)) or not np.all(np.isfinite(pv.imag)):
        raise TemporalWaveError("p must be a finite non-empty vector")
    damping = _psd_operator(C, pv.size, name="C")
    return float((-np.vdot(pv, damping @ pv)).real)
