import math

import numpy as np
import pytest

from idt.eb_bec_madelung_bridge import (
    BECPhysicalBridge,
    EBBECBridgeError,
    acoustic_metric,
    dilute_3d_contact_coupling,
    effective_winding,
    holonomy_radial_balance_residual,
    holonomy_radius_one_over_r,
    information_sound_speed_shift,
    intrinsic_bogoliubov_omega_sq,
    nonlinear_characteristic_coefficients,
    nonlinear_mode_roots,
    orbital_k_decomposition,
    physical_bogoliubov_omega_sq,
    thomas_fermi_density,
    thomas_fermi_sound_speed_sq,
)


def test_lambda_zero_recovers_02jn_characteristic_polynomial():
    k = 1.7
    mobility = 0.8
    rho0 = 1.4
    mu = 0.35
    coefficients = nonlinear_characteristic_coefficients(
        k,
        mobility,
        rho0,
        mu,
        nonlinear_coupling=0.0,
    )
    assert coefficients == pytest.approx(
        (
            1.0,
            2.0 * mu * mobility * rho0 * k**2,
            mobility**2 * k**4,
        )
    )


def test_nonlinear_characteristic_polynomial_has_declared_eos_term():
    k = 0.9
    mobility = 1.2
    rho0 = 2.1
    mu = 0.4
    lam = 0.7
    a, b, c = nonlinear_characteristic_coefficients(
        k,
        mobility,
        rho0,
        mu,
        lam,
    )
    assert a == 1.0
    assert b == pytest.approx(2.0 * mu * mobility * rho0 * k**2)
    assert c == pytest.approx(
        2.0 * mobility * lam * rho0 * k**2 + mobility**2 * k**4
    )

    roots = nonlinear_mode_roots(k, mobility, rho0, mu, lam)
    for root in roots:
        assert abs(a * root**2 + b * root + c) < 2e-14
        assert root.real <= 1e-14


@pytest.mark.parametrize(
    "mass,hbar,gamma,ell,zrho,g,rho0,k_phys",
    [
        (1.7, 0.8, 2.3, 3.2, 4.1, 0.6, 1.2, 0.4),
        (2.0, 1.0, 1.0, 1.0, 1.0, 1.3, 0.9, 2.1),
        (0.7, 1.4, 0.25, 5.0, 0.3, 2.2, 3.0, 0.08),
    ],
)
def test_intrinsic_to_physical_bogoliubov_roundtrip_is_exact(
    mass,
    hbar,
    gamma,
    ell,
    zrho,
    g,
    rho0,
    k_phys,
):
    bridge = BECPhysicalBridge(
        mass=mass,
        hbar=hbar,
        dtheta_dt=gamma,
        spatial_scale=ell,
        density_scale=zrho,
    )
    m_idt = bridge.idt_mobility
    lam = bridge.idt_nonlinear_coupling(g)
    k_idt = bridge.intrinsic_wave_number(k_phys)

    intrinsic = intrinsic_bogoliubov_omega_sq(
        k_idt,
        m_idt,
        rho0,
        lam,
    )
    mapped_physical = gamma**2 * intrinsic
    direct_physical = physical_bogoliubov_omega_sq(
        k_phys,
        mass,
        hbar,
        g,
        bridge.physical_density(rho0),
    )
    assert mapped_physical == pytest.approx(direct_physical, rel=2e-15, abs=2e-15)


def test_bridge_sound_speed_and_velocity_scalings():
    bridge = BECPhysicalBridge(
        mass=2.4,
        hbar=1.1,
        dtheta_dt=0.7,
        spatial_scale=3.5,
        density_scale=1.8,
    )
    g = 0.9
    rho0 = 1.3
    expected_cs2 = g * bridge.physical_density(rho0) / bridge.mass
    assert bridge.physical_sound_speed_sq(g, rho0) == pytest.approx(
        expected_cs2
    )
    assert bridge.physical_velocity(0.4) == pytest.approx(3.5 * 0.7 * 0.4)
    assert bridge.physical_connection(0.25) == pytest.approx(1.1 * 0.25 / 3.5)


def test_dilute_3d_contact_coupling_keeps_scattering_length_sign():
    hbar = 1.3
    mass = 2.2
    for scattering_length in (0.4, -0.15):
        expected = 4.0 * math.pi * hbar**2 * scattering_length / mass
        assert dilute_3d_contact_coupling(
            hbar, mass, scattering_length
        ) == pytest.approx(expected)


def test_orbital_decomposition_recovers_gremlin_central_kernel():
    result = orbital_k_decomposition(
        radius=4.0,
        mass=2.0,
        source_strength=7.5,
        source_coupling=3.0,
        information_coupling=5.0,
        information_gradient=0.0,
        contact_coupling=2.0,
        density_gradient=0.0,
        quantum_pressure_gradient=0.0,
    )
    expected = 7.5 * (3.0 / 2.0)
    assert result.central == pytest.approx(expected)
    assert result.total == pytest.approx(expected)


def test_orbital_decomposition_separates_all_radial_sources():
    result = orbital_k_decomposition(
        radius=2.0,
        mass=4.0,
        source_strength=3.0,
        source_coupling=2.0,
        information_coupling=5.0,
        information_gradient=-0.2,
        contact_coupling=1.5,
        density_gradient=0.4,
        quantum_pressure_gradient=-0.7,
    )
    factor = 2.0**2 / 4.0
    assert result.central == pytest.approx(3.0 * 2.0 / 4.0)
    assert result.information == pytest.approx(factor * 5.0 * -0.2)
    assert result.mean_field == pytest.approx(factor * 1.5 * 0.4)
    assert result.quantum_pressure == pytest.approx(factor * -0.7)
    assert result.total == pytest.approx(
        result.central
        + result.information
        + result.mean_field
        + result.quantum_pressure
    )


def test_holonomy_shifted_one_over_r_shell_closes_radial_balance():
    hbar = 1.2
    mass = 2.5
    q_g = 1.7
    mu_s = 3.4
    n = 3
    tau = 0.8

    radius = holonomy_radius_one_over_r(
        hbar,
        mass,
        q_g,
        mu_s,
        n,
        tau,
    )
    nu = effective_winding(n, tau)
    assert radius == pytest.approx(
        hbar**2 * nu**2 / (mass * q_g * mu_s)
    )

    potential_gradient = q_g * mu_s / radius**2
    residual = holonomy_radial_balance_residual(
        hbar,
        mass,
        radius,
        n,
        tau,
        potential_gradient,
    )
    assert abs(residual) < 2e-13


def test_thomas_fermi_density_sound_speed_and_information_shift():
    chemical = 8.0
    external = 1.5
    information = 0.7
    g = 2.0
    mass = 3.0

    rho = thomas_fermi_density(chemical, external, information, g)
    assert rho == pytest.approx((chemical - external - information) / g)

    cs2 = thomas_fermi_sound_speed_sq(
        chemical,
        external,
        information,
        mass,
    )
    assert cs2 == pytest.approx((chemical - external - information) / mass)
    assert cs2 == pytest.approx(g * rho / mass)

    delta_u = 0.2
    shifted = thomas_fermi_sound_speed_sq(
        chemical,
        external,
        information + delta_u,
        mass,
    )
    assert shifted - cs2 == pytest.approx(
        information_sound_speed_shift(delta_u, mass)
    )


def test_acoustic_metric_is_symmetric_and_has_one_negative_eigenvalue():
    metric = acoustic_metric(
        density=1.8,
        sound_speed=2.3,
        velocity=[0.4, -0.2, 0.1],
    )
    np.testing.assert_allclose(metric, metric.T, rtol=0.0, atol=0.0)
    eigenvalues = np.linalg.eigvalsh(metric)
    assert np.count_nonzero(eigenvalues < 0.0) == 1
    assert np.count_nonzero(eigenvalues > 0.0) == 3


@pytest.mark.parametrize(
    "call",
    [
        lambda: BECPhysicalBridge(0.0, 1.0, 1.0),
        lambda: BECPhysicalBridge(1.0, 1.0, -1.0),
        lambda: BECPhysicalBridge(1.0, 1.0, 1.0, spatial_scale=0.0),
        lambda: nonlinear_characteristic_coefficients(
            1.0, 0.0, 1.0, 0.1, 0.2
        ),
        lambda: orbital_k_decomposition(
            0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0
        ),
        lambda: holonomy_radius_one_over_r(
            1.0, 1.0, 1.0, 1.0, 0, 0.0
        ),
        lambda: thomas_fermi_density(1.0, 2.0, 0.0, 1.0),
        lambda: acoustic_metric(1.0, 0.0, [0.0, 0.0]),
    ],
)
def test_eb_bec_bridge_fails_closed(call):
    with pytest.raises(EBBECBridgeError):
        call()
