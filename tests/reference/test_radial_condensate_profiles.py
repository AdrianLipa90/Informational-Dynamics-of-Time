import math

import pytest

from idt.radial_condensate_profiles import (
    RadialCondensateError,
    RadialObservables,
    central_consistency_residual,
    condensate_subtracted_residual,
    epicyclic_sq,
    holonomy_shell_susceptibility_nu,
    holonomy_shell_susceptibility_tau,
    k_obs,
    k_obs_gradient_from_epicycle,
    mean_field_inverse_density,
    power_law_epicyclic_sq,
    power_law_potential,
    quantum_pressure_inverse_ode_coefficient,
    transverse_phase_curvature,
    transverse_phase_gradient,
)


@pytest.mark.parametrize(
    ("q", "ratio"),
    [(0.0, 4.0), (2.0, 2.0), (3.0, 1.0), (4.0, 0.0)],
)
def test_power_law_classifier(q, ratio):
    r = 2.3
    amplitude = 1.7
    omega_sq = amplitude * r ** (-q)
    d_omega_sq_dr = -q * amplitude * r ** (-q - 1.0)
    kappa_sq = epicyclic_sq(r, omega_sq, d_omega_sq_dr)
    assert kappa_sq == pytest.approx(ratio * omega_sq)
    assert kappa_sq == pytest.approx(power_law_epicyclic_sq(omega_sq, q))


def test_kobs_epicycle_identity_for_power_law():
    r = 3.1
    q = 2.4
    amplitude = 0.8
    omega_sq = amplitude * r ** (-q)
    kappa_sq = (4.0 - q) * omega_sq
    expected = (3.0 - q) * amplitude * r ** (2.0 - q)
    assert k_obs_gradient_from_epicycle(r, omega_sq, kappa_sq) == pytest.approx(
        expected
    )


def test_central_consistency_residual_vanishes():
    r = 4.2
    omega_sq = 0.37
    derivative = -0.11
    measured = 4.0 * omega_sq + r * derivative
    assert central_consistency_residual(r, omega_sq, derivative, measured) == pytest.approx(
        0.0
    )


def test_power_law_potential_derivative_recovers_circular_law():
    r = 2.0
    h = 1e-6
    for q in (0.0, 1.5, 2.0, 3.0):
        amplitude = 0.9
        fp = power_law_potential(r + h, amplitude, q)
        fm = power_law_potential(r - h, amplitude, q)
        derivative = (fp - fm) / (2.0 * h)
        assert derivative / r == pytest.approx(amplitude * r ** (-q), rel=1e-8)


@pytest.mark.parametrize("q", [0.0, 2.0, 3.0])
def test_mean_field_inverse_density_recovers_target_power_law(q):
    r = 2.0
    h = 1e-6
    mobility = 0.7
    coupling = 1.2
    amplitude = 0.8

    def rho(x):
        return mean_field_inverse_density(
            x,
            rho0=5.0,
            amplitude=amplitude,
            exponent_q=q,
            mobility=mobility,
            coupling_g=coupling,
        )

    rho_prime = (rho(r + h) - rho(r - h)) / (2.0 * h)
    recovered = 2.0 * mobility * coupling * rho_prime / r
    assert recovered == pytest.approx(amplitude * r ** (-q), rel=2e-8)


def test_quantum_pressure_inverse_ode_coefficient():
    assert quantum_pressure_inverse_ode_coefficient(3.0, 2.0) == pytest.approx(3.0 / 8.0)


def test_holonomy_susceptibility_chain_rule():
    r = 4.0
    lam = 2.0
    nu = 3.0
    kappa_sq = 5.0
    dr_dnu = holonomy_shell_susceptibility_nu(
        r,
        circulation_scale=lam,
        effective_winding=nu,
        kappa_sq=kappa_sq,
    )
    dr_dtau = holonomy_shell_susceptibility_tau(
        r,
        circulation_scale=lam,
        effective_winding=nu,
        kappa_sq=kappa_sq,
    )
    assert dr_dtau == pytest.approx(-dr_dnu / (2.0 * math.pi))


def test_holonomy_susceptibility_increases_near_marginal_stability():
    common = dict(radius=3.0, circulation_scale=1.7, effective_winding=2.0)
    stable = abs(holonomy_shell_susceptibility_tau(kappa_sq=1.0, **common))
    near = abs(holonomy_shell_susceptibility_tau(kappa_sq=0.1, **common))
    assert near == pytest.approx(10.0 * stable)


def test_transverse_phase_bridge_axis_and_off_axis():
    r = 5.0
    omega_sq = 2.0
    kappa_sq = 3.0
    assert transverse_phase_gradient(r, 0.0, omega_sq) == 0.0
    assert transverse_phase_curvature(r, 0.0, omega_sq, kappa_sq) == pytest.approx(
        omega_sq
    )

    b = 3.0
    beta2 = (b / r) ** 2
    expected = beta2 * kappa_sq + (1.0 - 4.0 * beta2) * omega_sq
    assert transverse_phase_gradient(r, b, omega_sq) == pytest.approx(b * omega_sq)
    assert transverse_phase_curvature(r, b, omega_sq, kappa_sq) == pytest.approx(
        expected
    )


def test_radial_observables_hessian_eigenvalues():
    obs = RadialObservables(radius=2.0, omega_sq=3.0, kappa_sq=4.0)
    assert obs.k_obs == pytest.approx(24.0)
    assert obs.hessian_radial == pytest.approx(-5.0)
    assert obs.hessian_tangential == pytest.approx(3.0)


def test_condensate_subtracted_residual_zero_for_constructed_balance():
    r = 2.0
    mobility = 0.5
    coupling = 1.25
    k_orb = 3.0
    rho_p = -0.2
    q_p = 0.1
    omega_sq = (
        k_orb / r**2
        + 2.0 * mobility * coupling * rho_p
        - 2.0 * mobility**2 * q_p
    ) / r
    assert condensate_subtracted_residual(
        r,
        omega_sq,
        k_orb=k_orb,
        mobility=mobility,
        coupling_g=coupling,
        density_gradient=rho_p,
        q_density_gradient=q_p,
    ) == pytest.approx(0.0)


@pytest.mark.parametrize(
    "call",
    [
        lambda: epicyclic_sq(0.0, 1.0, 0.0),
        lambda: mean_field_inverse_density(
            1.0,
            rho0=1.0,
            amplitude=1.0,
            exponent_q=2.0,
            mobility=1.0,
            coupling_g=0.0,
        ),
        lambda: holonomy_shell_susceptibility_tau(
            1.0, circulation_scale=1.0, effective_winding=1.0, kappa_sq=0.0
        ),
        lambda: transverse_phase_curvature(1.0, 2.0, 1.0, 1.0),
    ],
)
def test_fail_closed_domains(call):
    with pytest.raises(RadialCondensateError):
        call()
