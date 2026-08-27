import math

import numpy as np

from idt.temporal_wave_homogenization import (
    acoustic_coefficient_estimate,
    effective_long_wave_coefficients,
    harmonic_viscosity_candidate,
    periodic_bloch_operators,
    periodic_relational_edge_fields,
    relational_effective_long_wave_coefficients,
)


def test_uniform_relational_fields_reduce_to_previous_coefficients():
    rho0 = 2.5
    eta0 = 1.7
    rho = [rho0] * 6
    eta = [eta0] * 6
    coeff = relational_effective_long_wave_coefficients(rho, eta)
    expected_mobility = rho0 / eta0
    assert math.isclose(coeff.mobility_eff, expected_mobility, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(coeff.wave_speed, math.sqrt(expected_mobility), rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(coeff.damping_eff, eta0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(coeff.attenuation, 0.5 * eta0, rel_tol=0.0, abs_tol=1e-12)


def test_relational_substitution_matches_edge_formula():
    rho = np.asarray([0.8, 1.4, 2.7, 3.2, 1.1], dtype=float)
    eta = np.asarray([0.7, 1.2, 1.9, 0.9, 1.5], dtype=float)
    mobility, viscosity = periodic_relational_edge_fields(rho, eta)
    coeff = effective_long_wave_coefficients(mobility, viscosity)
    expected_m = 1.0 / np.mean(viscosity / np.sqrt(rho * np.roll(rho, -1)))
    expected_beta = expected_m**2 * np.mean(viscosity**3 / (rho * np.roll(rho, -1)))
    assert math.isclose(coeff.mobility_eff, expected_m, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(coeff.damping_eff, expected_beta, rel_tol=0.0, abs_tol=1e-12)


def test_bloch_operators_are_hermitian_positive_semidefinite():
    rng = np.random.default_rng(2026082701)
    rho = rng.uniform(0.2, 5.0, 8)
    eta = rng.uniform(0.2, 3.0, 8)
    mobility, viscosity = periodic_relational_edge_fields(rho, eta)
    K, C = periodic_bloch_operators(mobility, viscosity, 0.31)
    assert np.allclose(K, K.conj().T, atol=1e-12, rtol=0.0)
    assert np.allclose(C, C.conj().T, atol=1e-12, rtol=0.0)
    assert np.min(np.linalg.eigvalsh(K)) >= -1e-11
    assert np.min(np.linalg.eigvalsh(C)) >= -1e-11


def test_edge_spacing_preserves_effective_coefficients():
    rng = np.random.default_rng(2026082702)
    rho = rng.uniform(0.2, 5.0, 7)
    eta = rng.uniform(0.2, 3.0, 7)
    mobility, viscosity = periodic_relational_edge_fields(rho, eta)
    target = effective_long_wave_coefficients(mobility, viscosity)
    # This gate tests the asymptotic long-wave coefficient, not finite-phase
    # dispersion.  Use a sufficiently small Bloch phase so the O(theta^2)
    # correction stays below the declared tolerance for every spacing probe.
    for spacing in [0.2, 0.7, 1.0, 2.3]:
        c_est, beta_est = acoustic_coefficient_estimate(
            mobility, viscosity, 0.005, edge_spacing=spacing
        )
        assert abs(c_est - target.wave_speed) / target.wave_speed < 5e-5
        assert abs(beta_est - target.damping_eff) / target.damping_eff < 5e-5


def test_heterogeneous_periodic_acoustic_homogenization_500_cases():
    rng = np.random.default_rng(20260827)
    max_c_rel = 0.0
    max_beta_rel = 0.0
    c_orders = []
    beta_orders = []
    naive_relative_errors = []

    for _ in range(500):
        n = int(rng.integers(3, 11))
        rho = rng.uniform(0.2, 5.0, n)
        eta = rng.uniform(0.2, 3.0, n)
        mobility, viscosity = periodic_relational_edge_fields(rho, eta)
        target = effective_long_wave_coefficients(mobility, viscosity)

        errors = []
        for phase in [0.08, 0.04, 0.02]:
            c_est, beta_est = acoustic_coefficient_estimate(mobility, viscosity, phase)
            errors.append((
                abs(c_est - target.wave_speed),
                abs(beta_est - target.damping_eff),
            ))

        max_c_rel = max(max_c_rel, errors[-1][0] / target.wave_speed)
        max_beta_rel = max(max_beta_rel, errors[-1][1] / target.damping_eff)
        c_orders.append(math.log(errors[1][0] / errors[2][0], 2.0))
        beta_orders.append(math.log(errors[1][1] / errors[2][1], 2.0))

        naive = harmonic_viscosity_candidate(viscosity)
        naive_relative_errors.append(abs(naive - target.damping_eff) / target.damping_eff)

    assert max_c_rel < 1e-4
    assert max_beta_rel < 1e-4
    assert 1.9 < float(np.median(c_orders)) < 2.1
    assert 1.9 < float(np.median(beta_orders)) < 2.1

    naive_relative_errors = np.asarray(naive_relative_errors)
    assert float(np.median(naive_relative_errors)) > 0.1
    assert int(np.sum(naive_relative_errors > 0.01)) > 490
    assert int(np.sum(naive_relative_errors > 0.05)) > 480
