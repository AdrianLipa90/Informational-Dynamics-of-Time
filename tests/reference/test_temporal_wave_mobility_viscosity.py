import math

import numpy as np
import pytest

from idt.temporal_wave import TemporalWaveError, gauge_transform_links
from idt.temporal_wave_dissipation import (
    edge_scalar_damping_ratios,
    mobility_gauge_laplacian,
    operator_damped_wave_rhs,
    operator_wave_energy_derivative,
    scalar_damping_if_edge_factorable,
    viscous_damping_laplacian,
    viscosity_edge_weights,
    zero_drive_rate_generator,
)


def random_ring(seed=2301):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(4, 10))
    edges = [(j, (j + 1) % n) for j in range(n)]
    links = np.exp(1j * rng.uniform(-math.pi, math.pi, len(edges)))
    rho = rng.uniform(0.1, 5.0, n)
    eta = rng.uniform(0.1, 3.0, n)
    return rng, n, edges, links, rho, eta


def test_zero_drive_kinetics_exactly_derives_mobility_dirichlet_operator():
    _, n, edges, _, rho, eta = random_ring()
    G = zero_drive_rate_generator(n, edges, rho, eta)
    K = mobility_gauge_laplacian(n, edges, np.ones(len(edges), dtype=complex), rho, eta)
    assert np.allclose(K, -G, atol=1e-12, rtol=0.0)
    assert np.allclose(np.sum(G, axis=1), 0.0, atol=1e-12, rtol=0.0)


def test_viscosity_weights_reuse_existing_pair_average():
    edges = [(0, 1), (1, 2)]
    eta = [1.0, 3.0, 7.0]
    assert np.allclose(viscosity_edge_weights(edges, eta), [2.0, 5.0], atol=0.0, rtol=0.0)


def test_viscous_damping_operator_is_hermitian_psd_and_gauge_covariant():
    rng, n, edges, links, _, eta = random_ring(2302)
    C = viscous_damping_laplacian(n, edges, links, eta)
    chi = rng.uniform(-math.pi, math.pi, n)
    U = np.diag(np.exp(1j * chi))
    Cg = viscous_damping_laplacian(
        n, edges, gauge_transform_links(edges, links, chi), eta
    )
    assert np.allclose(C, C.conj().T, atol=1e-12, rtol=0.0)
    assert np.min(np.linalg.eigvalsh(C)) >= -1e-11
    assert np.allclose(Cg, U @ C @ U.conj().T, atol=2e-12, rtol=0.0)


def test_operator_damping_has_exact_nonpositive_energy_balance():
    rng, n, edges, links, rho, eta = random_ring(2303)
    K = mobility_gauge_laplacian(n, edges, links, rho, eta)
    C = viscous_damping_laplacian(n, edges, links, eta)
    q = rng.normal(size=n) + 1j * rng.normal(size=n)
    p = rng.normal(size=n) + 1j * rng.normal(size=n)
    qdot, pdot = operator_damped_wave_rhs(q, p, K, C)
    direct = float(np.real(np.vdot(K @ q, qdot) + np.vdot(p, pdot)))
    expected = operator_wave_energy_derivative(p, C)
    assert expected <= 1e-12
    assert abs(direct - expected) < 1e-11


def test_uniform_fields_factor_to_scalar_nu_eta_squared_over_rho():
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    rho0 = 2.5
    eta0 = 1.7
    rho = [rho0] * 4
    eta = [eta0] * 4
    ratios = edge_scalar_damping_ratios(edges, rho, eta)
    expected = eta0 * eta0 / rho0
    assert np.allclose(ratios, expected, atol=1e-12, rtol=0.0)
    assert math.isclose(
        scalar_damping_if_edge_factorable(edges, rho, eta),
        expected,
        abs_tol=1e-12,
        rel_tol=0.0,
    )


def test_heterogeneous_fields_fail_closed_for_one_scalar_nu():
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    rho = [1.0, 1.7, 3.0, 4.2]
    eta = [0.8, 1.1, 1.9, 2.6]
    assert np.ptp(edge_scalar_damping_ratios(edges, rho, eta)) > 1e-3
    with pytest.raises(TemporalWaveError):
        scalar_damping_if_edge_factorable(edges, rho, eta)


def test_randomized_mobility_viscosity_gate_500_cases():
    max_dirichlet = 0.0
    max_gauge_k = 0.0
    max_gauge_c = 0.0
    max_energy = 0.0
    min_k = float("inf")
    min_c = float("inf")
    nonfactorable = 0
    for seed in range(500):
        rng = np.random.default_rng(9000 + seed)
        n = int(rng.integers(3, 13))
        edges = [(j, (j + 1) % n) for j in range(n)]
        rho = rng.uniform(0.05, 9.0, n)
        eta = rng.uniform(0.05, 6.0, n)
        links = np.exp(1j * rng.uniform(-math.pi, math.pi, len(edges)))

        K = mobility_gauge_laplacian(n, edges, links, rho, eta)
        C = viscous_damping_laplacian(n, edges, links, eta)
        min_k = min(min_k, float(np.min(np.linalg.eigvalsh(K))))
        min_c = min(min_c, float(np.min(np.linalg.eigvalsh(C))))

        G = zero_drive_rate_generator(n, edges, rho, eta)
        K0 = mobility_gauge_laplacian(
            n, edges, np.ones(len(edges), dtype=complex), rho, eta
        )
        max_dirichlet = max(max_dirichlet, float(np.max(np.abs(K0 + G))))

        chi = rng.uniform(-math.pi, math.pi, n)
        U = np.diag(np.exp(1j * chi))
        links_g = gauge_transform_links(edges, links, chi)
        Kg = mobility_gauge_laplacian(n, edges, links_g, rho, eta)
        Cg = viscous_damping_laplacian(n, edges, links_g, eta)
        max_gauge_k = max(max_gauge_k, float(np.max(np.abs(Kg - U @ K @ U.conj().T))))
        max_gauge_c = max(max_gauge_c, float(np.max(np.abs(Cg - U @ C @ U.conj().T))))

        q = rng.normal(size=n) + 1j * rng.normal(size=n)
        p = rng.normal(size=n) + 1j * rng.normal(size=n)
        qdot, pdot = operator_damped_wave_rhs(q, p, K, C)
        direct = float(np.real(np.vdot(K @ q, qdot) + np.vdot(p, pdot)))
        expected = operator_wave_energy_derivative(p, C)
        max_energy = max(max_energy, abs(direct - expected))

        try:
            scalar_damping_if_edge_factorable(edges, rho, eta, atol=1e-10, rtol=1e-10)
        except TemporalWaveError:
            nonfactorable += 1

    assert max_dirichlet < 1e-12
    assert max_gauge_k < 1e-11
    assert max_gauge_c < 1e-11
    assert max_energy < 1e-10
    assert min_k >= -1e-10
    assert min_c >= -1e-10
    assert nonfactorable == 500
