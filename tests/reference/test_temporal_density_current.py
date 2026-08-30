import math

import numpy as np
import pytest

from idt.temporal_density_current import (
    TemporalDensityCurrentError,
    continuity_residual,
    covariant_path_hamiltonian,
    edge_currents,
    gauge_transform,
    phase_only_density_derivative,
    schrodinger_density_derivative,
    seam_quadratures,
)


def _smooth_current_sample(n: int):
    x = np.linspace(0.0, 1.0, n)
    h = float(x[1] - x[0])

    def radius(z):
        return 1.0 + 0.2 * np.sin(2.0 * np.pi * z)

    def phase(z):
        return 0.3 * np.sin(2.0 * np.pi * z)

    def phase_prime(z):
        return 0.6 * np.pi * np.cos(2.0 * np.pi * z)

    def connection(z):
        return 0.1 * np.cos(2.0 * np.pi * z)

    def mobility(z):
        return 1.2 + 0.3 * np.cos(2.0 * np.pi * z)

    amplitudes = np.sqrt(h) * radius(x) * np.exp(1j * phase(x))
    seams = 0.1 / (2.0 * np.pi) * (
        np.sin(2.0 * np.pi * x[1:]) - np.sin(2.0 * np.pi * x[:-1])
    )
    mids = 0.5 * (x[:-1] + x[1:])
    edge_mobility = mobility(mids)
    target = 2.0 * edge_mobility * radius(mids) ** 2 * (
        phase_prime(mids) - connection(mids)
    )
    return x, h, amplitudes, seams, edge_mobility, target


def test_exact_finite_path_continuity_for_complex_state():
    rng = np.random.default_rng(20260829)
    state = rng.normal(size=6) + 1j * rng.normal(size=6)
    mobility = np.asarray([1.1, 0.8, 1.4, 0.9, 1.2])
    seams = np.asarray([0.2, -0.5, 0.3, 0.7, -0.1])
    assert continuity_residual(state, mobility, seams, 0.17) < 2e-12


def test_real_diagonal_potential_preserves_continuity_identity():
    state = np.asarray([1.0 + 0.2j, -0.3 + 0.7j, 0.5 - 0.8j, 0.4 + 0.1j])
    mobility = [1.0, 1.3, 0.7]
    seams = [0.2, -0.4, 0.3]
    potential = [2.0, -1.0, 0.5, 4.0]
    assert continuity_residual(state, mobility, seams, 0.23, potential=potential) < 2e-12


def test_boundary_telescope_gives_exact_total_norm_conservation():
    state = np.asarray([0.4 + 0.2j, -0.1 + 0.6j, 0.7 - 0.3j, -0.2 + 0.1j])
    mobility = [1.2, 0.9, 1.4]
    seams = [0.1, -0.2, 0.4]
    hamiltonian = covariant_path_hamiltonian(mobility, seams, 0.2)
    derivative = schrodinger_density_derivative(state, hamiltonian)
    assert abs(float(np.sum(derivative))) < 2e-12


def test_edge_current_is_gauge_invariant():
    state = np.asarray([0.8 + 0.1j, -0.3 + 0.5j, 0.6 - 0.2j, 0.2 + 0.4j])
    seams = np.asarray([0.3, -0.7, 0.2])
    mobility = np.asarray([1.1, 0.85, 1.25])
    chi = np.asarray([0.4, -0.2, 0.7, -0.5])
    transformed_state, transformed_seams = gauge_transform(state, seams, chi)
    before = edge_currents(state, mobility, seams, 0.15)
    after = edge_currents(transformed_state, mobility, transformed_seams, 0.15)
    np.testing.assert_allclose(after, before, rtol=0.0, atol=2e-13)


def test_seam_quadrature_circle_and_control_points():
    r0 = 0.7
    r1 = 0.5
    pair_scale = r0 * r1
    mobility = 1.3
    h = 0.2

    q0 = seam_quadratures(r0, r1, 0.0, mobility, h)
    assert math.isclose(q0.fuzzy_mass, 2.0 * pair_scale, abs_tol=1e-15)
    assert abs(q0.current) < 1e-15
    assert q0.circle_residual < 1e-15

    q90 = seam_quadratures(r0, r1 * 1j, 0.0, mobility, h)
    assert math.isclose(q90.coherence, 0.0, abs_tol=1e-15)
    assert math.isclose(abs(q90.transport), pair_scale, abs_tol=1e-15)
    assert math.isclose(
        abs(q90.current), 2.0 * mobility * pair_scale / h**2, rel_tol=0.0, abs_tol=1e-13
    )
    assert q90.circle_residual < 1e-15

    qpi = seam_quadratures(r0, -r1, 0.0, mobility, h)
    assert abs(qpi.fuzzy_mass) < 1e-15
    assert abs(qpi.current) < 1e-13
    assert qpi.circle_residual < 1e-15


def test_phase_only_tangent_preserves_every_vertex_occupation():
    state = np.asarray([0.8 + 0.1j, -0.2 + 0.5j, 0.3 - 0.7j, 0.4 + 0.2j])
    rates = np.asarray([1.2, -0.7, 3.0, 0.4])
    derivative = phase_only_density_derivative(state, rates)
    np.testing.assert_allclose(derivative, 0.0, rtol=0.0, atol=2e-15)


def test_continuum_edge_current_converges_second_order():
    errors = []
    for n in (33, 65, 129, 257):
        _, h, state, seams, mobility, target = _smooth_current_sample(n)
        current = edge_currents(state, mobility, seams, h)
        errors.append(float(np.max(np.abs(current - target))))
    ratios = np.asarray(errors[:-1]) / np.asarray(errors[1:])
    assert np.all(ratios > 3.8)
    assert errors[-1] < 2.8e-4


@pytest.mark.parametrize(
    "call",
    [
        lambda: covariant_path_hamiltonian([1.0], [0.0], 0.0),
        lambda: edge_currents([1.0, 2.0], [0.0], [0.0], 0.1),
        lambda: phase_only_density_derivative([1.0, 2.0], [1.0]),
        lambda: seam_quadratures(1.0, 1.0, 0.0, -1.0, 0.1),
    ],
)
def test_temporal_density_current_fails_closed(call):
    with pytest.raises(TemporalDensityCurrentError):
        call()
