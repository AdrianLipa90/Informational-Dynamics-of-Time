import math

import numpy as np
import pytest

from idt.temporal_wave import (
    TemporalWaveError,
    analytic_ring_spectrum,
    damped_wave_rhs,
    gauge_incidence_matrix,
    gauge_laplacian,
    gauge_transform_links,
    mobility_edge_weights,
    modal_frequencies,
    uniform_ring,
    wave_energy_derivative,
)


def random_graph(seed=7):
    rng = np.random.default_rng(seed)
    n = 7
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,0),(1,5),(2,6)]
    links = np.exp(1j * rng.uniform(-math.pi, math.pi, len(edges)))
    weights = rng.uniform(0.2, 2.0, len(edges))
    return rng, n, edges, links, weights


def test_gauge_laplacian_is_hermitian_psd_and_factorized():
    _, n, edges, links, weights = random_graph()
    D = gauge_incidence_matrix(n, edges, links)
    K = gauge_laplacian(n, edges, links, weights)
    expected = D.conj().T @ (weights[:, None] * D)
    assert np.allclose(K, K.conj().T, atol=1e-12, rtol=0.0)
    assert np.allclose(K, expected, atol=1e-12, rtol=0.0)
    assert np.min(np.linalg.eigvalsh(K)) >= -1e-11


def test_local_u1_gauge_covariance_and_spectral_invariance():
    rng, n, edges, links, weights = random_graph(11)
    chi = rng.uniform(-math.pi, math.pi, n)
    U = np.diag(np.exp(1j * chi))
    K = gauge_laplacian(n, edges, links, weights)
    links_g = gauge_transform_links(edges, links, chi)
    Kg = gauge_laplacian(n, edges, links_g, weights)
    assert np.allclose(Kg, U @ K @ U.conj().T, atol=2e-12, rtol=0.0)
    assert np.allclose(np.linalg.eigvalsh(Kg), np.linalg.eigvalsh(K), atol=2e-12, rtol=0.0)


def test_exact_state_function_edge_phase_is_pure_gauge_for_spectrum():
    rng = np.random.default_rng(13)
    n = 8
    edges = [(j, (j+1)%n) for j in range(n)] + [(0,4),(2,6)]
    weights = rng.uniform(0.5, 1.5, len(edges))
    links = np.ones(len(edges), dtype=complex)
    V = rng.normal(size=n)
    exact_links = gauge_transform_links(edges, links, V)
    K0 = gauge_laplacian(n, edges, links, weights)
    K1 = gauge_laplacian(n, edges, exact_links, weights)
    assert np.allclose(np.linalg.eigvalsh(K0), np.linalg.eigvalsh(K1), atol=3e-12, rtol=0.0)


def test_uniform_ring_numeric_spectrum_matches_holonomy_formula():
    n, D, phi = 37, 0.73, 0.91
    edges, links, weights = uniform_ring(n, diffusivity=D, holonomy_phase=phi)
    numeric = np.linalg.eigvalsh(gauge_laplacian(n, edges, links, weights))
    analytic = np.sort(analytic_ring_spectrum(n, diffusivity=D, holonomy_phase=phi))
    assert np.allclose(numeric, analytic, atol=2e-10, rtol=1e-12)


def test_zero_holonomy_continuum_mode_is_second_order():
    D = 0.61
    target = D * (2.0 * math.pi) ** 2
    errors = []
    for n in (32, 64, 128, 256):
        edges, links, weights = uniform_ring(n, diffusivity=D)
        eig = np.linalg.eigvalsh(gauge_laplacian(n, edges, links, weights))
        errors.append(abs(eig[1] - target))
    orders = [math.log(errors[i] / errors[i+1], 2.0) for i in range(len(errors)-1)]
    assert min(orders[-2:]) > 1.98
    assert errors[-1] < 1e-2


def test_holonomy_opens_gap_with_second_order_continuum_convergence():
    D, phi = 0.8, 0.7
    target = D * phi * phi
    errors = []
    gaps = []
    for n in (32, 64, 128, 256):
        edges, links, weights = uniform_ring(n, diffusivity=D, holonomy_phase=phi)
        gap = float(np.min(np.linalg.eigvalsh(gauge_laplacian(n, edges, links, weights))))
        gaps.append(gap)
        errors.append(abs(gap - target))
    orders = [math.log(errors[i] / errors[i+1], 2.0) for i in range(len(errors)-1)]
    assert all(g > 0.0 for g in gaps)
    assert min(orders[-2:]) > 1.98
    assert errors[-1] < 1e-5


def test_damped_kahler_wave_has_nonincreasing_energy():
    rng, n, edges, links, weights = random_graph(17)
    K = gauge_laplacian(n, edges, links, weights)
    q = rng.normal(size=n) + 1j * rng.normal(size=n)
    p = rng.normal(size=n) + 1j * rng.normal(size=n)
    nu = 0.23
    qdot, pdot = damped_wave_rhs(q, p, K, damping=nu)
    direct = float(np.real(np.vdot(K @ q, qdot) + np.vdot(p, pdot)))
    expected = wave_energy_derivative(p, K, damping=nu)
    assert expected <= 1e-12
    assert abs(direct - expected) < 2e-11


def test_low_k_damped_dispersion_has_linear_real_and_quadratic_imaginary_parts():
    D, nu = 0.9, 0.37
    ks = np.asarray([0.4, 0.2, 0.1, 0.05], dtype=float)
    lam = D * ks**2
    omega = modal_frequencies(lam, damping=nu)
    real_ratio_error = np.abs(omega.real / ks - math.sqrt(D))
    orders = [math.log(real_ratio_error[i] / real_ratio_error[i+1], 2.0) for i in range(3)]
    assert min(orders[-2:]) > 1.99
    assert np.allclose(omega.imag / ks**2, -0.5 * nu * D, atol=2e-14, rtol=0.0)


def test_mobility_weights_reuse_existing_relational_primitive():
    edges = [(0,1),(1,2)]
    rho = [1.0, 4.0, 9.0]
    eta = [2.0, 2.0, 4.0]
    w = mobility_edge_weights(edges, rho, eta)
    expected = np.asarray([1.0, 2.0])
    assert np.allclose(w, expected, atol=1e-12, rtol=0.0)


def test_invalid_links_and_weights_fail_closed():
    with pytest.raises(TemporalWaveError):
        gauge_laplacian(2, [(0,1)], [0.5+0j], [1.0])
    with pytest.raises(TemporalWaveError):
        gauge_laplacian(2, [(0,1)], [1.0+0j], [0.0])
    with pytest.raises(TemporalWaveError):
        gauge_laplacian(2, [(0,0)], [1.0+0j], [1.0])
