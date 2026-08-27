from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.now_wave_activation import (
    mobility_from_activity_current,
    mobility_from_activity_current_arrays,
    realized_now_support,
    structural_transition_signature,
    total_wave_activation,
    wave_edge_activation,
    wave_edge_activation_from_activity_current,
)
from src.idt.temporal_wave import TemporalWaveError, gauge_incidence_matrix


def _rates(mobility: float, drive: float) -> tuple[float, float]:
    return mobility * math.exp(drive / 2.0), mobility * math.exp(-drive / 2.0)


def test_structural_signature_zero_iff_all_components_zero() -> None:
    kap = math.log(2.0) / (24.0 * math.pi)
    assert structural_transition_signature(0.0, 0.0, 0.0, kappa_value=kap) == 0.0
    assert structural_transition_signature(0.2, 0.0, 0.0, kappa_value=kap) > 0.0
    assert structural_transition_signature(0.0, 1.0, 0.0, kappa_value=kap) > 0.0
    assert structural_transition_signature(0.0, 0.0, 1.0, kappa_value=kap) > 0.0


def test_hyperbolic_invariant_recovers_mobility_500_cases() -> None:
    max_error = 0.0
    for seed in range(500):
        rng = np.random.default_rng(1000 + seed)
        mobility = float(rng.uniform(0.02, 8.0))
        drive = float(rng.uniform(-5.0, 5.0))
        forward, reverse = _rates(mobility, drive)
        activity = forward + reverse
        current = forward - reverse
        max_error = max(
            max_error,
            abs(mobility_from_activity_current(activity, current) - mobility),
        )
    assert max_error < 1e-12


def test_activation_from_activity_current_equals_direct_mobility() -> None:
    rng = np.random.default_rng(2)
    n = 9
    edges = [(i, (i + 1) % n) for i in range(n)]
    mobility = rng.uniform(0.1, 3.0, n)
    drive = rng.uniform(-2.0, 2.0, n)
    forward = mobility * np.exp(drive / 2.0)
    reverse = mobility * np.exp(-drive / 2.0)
    activity = forward + reverse
    current = forward - reverse
    links = np.exp(1j * rng.uniform(-math.pi, math.pi, n))
    wave = rng.normal(size=n) + 1j * rng.normal(size=n)
    direct = wave_edge_activation(n, edges, links, wave, mobility)
    reconstructed = wave_edge_activation_from_activity_current(
        n, edges, links, wave, activity, current
    )
    assert np.allclose(direct, reconstructed, atol=1e-12, rtol=0.0)


def test_wave_activation_is_local_u1_gauge_invariant() -> None:
    rng = np.random.default_rng(3)
    n = 10
    edges = [(i, (i + 1) % n) for i in range(n)]
    mobility = rng.uniform(0.1, 4.0, n)
    links = np.exp(1j * rng.uniform(-math.pi, math.pi, n))
    wave = rng.normal(size=n) + 1j * rng.normal(size=n)
    activation = wave_edge_activation(n, edges, links, wave, mobility)
    chi = rng.uniform(-math.pi, math.pi, n)
    wave_g = np.exp(1j * chi) * wave
    links_g = np.asarray(
        [
            np.exp(1j * (chi[b] - chi[a])) * link
            for (a, b), link in zip(edges, links)
        ],
        dtype=complex,
    )
    activation_g = wave_edge_activation(n, edges, links_g, wave_g, mobility)
    assert np.allclose(activation, activation_g, atol=2e-12, rtol=0.0)


def test_covariantly_parallel_pure_gauge_state_has_zero_activation() -> None:
    rng = np.random.default_rng(4)
    n = 12
    edges = [(i, (i + 1) % n) for i in range(n)]
    chi = rng.uniform(-math.pi, math.pi, n)
    links = np.asarray(
        [np.exp(1j * (chi[b] - chi[a])) for a, b in edges],
        dtype=complex,
    )
    wave = 1.7 * np.exp(1j * chi)
    activation = wave_edge_activation(n, edges, links, wave, np.ones(n))
    assert np.max(activation) < 1e-28


def test_realized_now_support_is_intersection_of_positive_supports() -> None:
    points = list("abcdef")
    signatures = np.asarray([1.0, 0.0, 2.0, 3.0, 0.0, 4.0])
    activation = np.asarray([0.0, 2.0, 3.0, 0.0, 5.0, 6.0])
    assert realized_now_support(points, signatures, activation) == {"c", "f"}


def test_nontrivial_ring_holonomy_opens_positive_wave_activation_gap() -> None:
    for n in (4, 7, 16):
        phase = 0.7
        mobility = 1.3
        edges = [(i, (i + 1) % n) for i in range(n)]
        links = np.full(n, np.exp(1j * phase / n), dtype=complex)
        D = gauge_incidence_matrix(n, edges, links)
        K = D.conj().T @ (mobility * D)
        gap = float(np.min(np.linalg.eigvalsh(K)))
        exact = 4.0 * mobility * math.sin(phase / (2.0 * n)) ** 2
        assert abs(gap - exact) < 1e-12
        rng = np.random.default_rng(n)
        wave = rng.normal(size=n) + 1j * rng.normal(size=n)
        activation = wave_edge_activation(
            n, edges, links, wave, np.full(n, mobility)
        )
        quadratic = float(np.vdot(wave, K @ wave).real)
        assert abs(total_wave_activation(activation) - quadratic) < 1e-10
        assert total_wave_activation(activation) > 0.0


def test_fail_closed_invalid_hyperbolic_pair() -> None:
    with pytest.raises(TemporalWaveError):
        mobility_from_activity_current(1.0, 1.0)
    with pytest.raises(TemporalWaveError):
        mobility_from_activity_current_arrays([1.0], [2.0])
