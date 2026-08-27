from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.temporal_transport import TemporalTransportError
from src.idt.temporal_transport_wave import (
    cayley_wave_segment,
    energy_metric_defect,
    generator_energy_identity,
    maximum_energy_growth_eigenvalue,
    q_compatible_unitary_bifurcation,
    wave_energy_metric,
    wave_interrupted_transport,
)
from src.idt.temporal_wave import gauge_laplacian


def _gapped_ring(n=7, phase=0.71, mobility=1.4, viscosity=0.3):
    edges = [(i, (i + 1) % n) for i in range(n)]
    links = np.full(n, np.exp(1j * phase / n), dtype=complex)
    K = gauge_laplacian(n, edges, links, np.full(n, mobility))
    C = gauge_laplacian(n, edges, links, np.full(n, viscosity))
    return K, C


def test_wave_generator_has_exact_energy_identity() -> None:
    K, C = _gapped_ring()
    actual, target = generator_energy_identity(K, C)
    assert np.allclose(actual, target, atol=1e-12, rtol=0.0)


def test_cayley_wave_segment_is_energy_contractive_200_cases() -> None:
    rng = np.random.default_rng(41)
    worst = 0.0
    for _ in range(200):
        phase = float(rng.uniform(0.1, 2.8))
        mobility = float(rng.uniform(0.05, 4.0))
        viscosity = float(rng.uniform(0.0, 1.0)) + 1e-6
        K, C = _gapped_ring(
            n=int(rng.integers(3, 10)),
            phase=phase,
            mobility=mobility,
            viscosity=viscosity,
        )
        Q = wave_energy_metric(K)
        U = cayley_wave_segment(K, C, float(rng.uniform(1e-4, 0.2)))
        worst = max(worst, maximum_energy_growth_eigenvalue(U, Q))
    assert worst < 1e-10


def test_zero_damping_cayley_is_Q_unitary() -> None:
    K, _ = _gapped_ring()
    C = np.zeros_like(K)
    Q = wave_energy_metric(K)
    U = cayley_wave_segment(K, C, 0.07)
    assert np.allclose(energy_metric_defect(U, Q), 0.0, atol=2e-12, rtol=0.0)


def test_cayley_reverse_step_is_exact_inverse_when_constructed_algebraically() -> None:
    K, C = _gapped_ring()
    h = 0.04
    U = cayley_wave_segment(K, C, h)
    n2 = U.shape[0]
    # Cayley(-h) is formed directly from the same generator for the inverse check.
    from src.idt.temporal_transport_wave import wave_phase_space_generator

    A = wave_phase_space_generator(K, C)
    ident = np.eye(n2, dtype=complex)
    U_reverse = np.linalg.solve(ident + 0.5 * h * A, ident - 0.5 * h * A)
    assert np.allclose(U_reverse @ U, ident, atol=2e-12, rtol=0.0)


def test_Q_compatible_bifurcation_is_Q_unitary() -> None:
    K, _ = _gapped_ring(n=5)
    Q = wave_energy_metric(K)
    n = K.shape[0]
    z = np.zeros_like(K)
    ident = np.eye(n, dtype=complex)
    G = np.block([[K, z], [z, 2.0 * ident]])
    B = q_compatible_unitary_bifurcation(0.13, G, Q)
    assert np.allclose(energy_metric_defect(B, Q), 0.0, atol=2e-11, rtol=0.0)


def test_interrupted_product_remains_Q_contractive_for_compatible_events() -> None:
    K, C = _gapped_ring(n=6)
    Q = wave_energy_metric(K)
    n = K.shape[0]
    z = np.zeros_like(K)
    ident = np.eye(n, dtype=complex)
    G = np.block([[K, z], [z, ident]])
    smooth = [
        cayley_wave_segment(K, C, 0.02),
        cayley_wave_segment(K, C, 0.03),
        cayley_wave_segment(K, C, 0.01),
    ]
    events = [
        q_compatible_unitary_bifurcation(0.05, G, Q),
        q_compatible_unitary_bifurcation(-0.08, G, Q),
    ]
    total = wave_interrupted_transport(smooth, events)
    assert maximum_energy_growth_eigenvalue(total, Q) < 2e-10


def test_Q_incompatible_event_generator_fails_closed() -> None:
    K, _ = _gapped_ring(n=4)
    Q = wave_energy_metric(K)
    rng = np.random.default_rng(42)
    raw = rng.normal(size=Q.shape) + 1j * rng.normal(size=Q.shape)
    G = 0.5 * (raw + raw.conj().T)
    with pytest.raises(TemporalTransportError):
        q_compatible_unitary_bifurcation(0.1, G, Q, commutator_tol=1e-12)


def test_invalid_cayley_inputs_fail_closed() -> None:
    K, C = _gapped_ring()
    with pytest.raises(TemporalTransportError):
        cayley_wave_segment(K, C, 0.0)
    bad = K.copy()
    bad[0, 0] = -100.0
    with pytest.raises(TemporalTransportError):
        cayley_wave_segment(bad, C, 0.1)
