import math

import pytest

from idt.temporal_material_front import (
    TemporalMaterialFrontError,
    logistic_density_at_quantile,
    logistic_quantile,
    logistic_quantile_velocity,
    material_front_velocity,
    no_flux_material_front_velocity,
    phase_diffusion_coefficient,
    phase_diffusion_green,
    phase_diffusion_sigma,
    phase_diffusion_variance,
    total_mass_rate,
)


def test_total_mass_rate_is_boundary_flux_difference():
    assert total_mass_rate(0.7, 0.2) == pytest.approx(0.5)
    assert total_mass_rate(0.0, 0.0) == 0.0


def test_fixed_material_quantile_moves_with_current_velocity_under_no_flux_boundaries():
    audit = no_flux_material_front_velocity(
        p=0.37,
        density_at_front=0.25,
        current_at_front=-0.075,
        total_mass=1.0,
        selector_rate=0.0,
    )
    assert audit.current_transport_velocity == pytest.approx(-0.3)
    assert audit.selector_drift_velocity == 0.0
    assert audit.boundary_flux_correction == 0.0
    assert audit.total_velocity == pytest.approx(-0.3)


def test_dynamic_now_selector_adds_exact_selector_drift():
    audit = no_flux_material_front_velocity(
        p=0.4,
        density_at_front=0.2,
        current_at_front=0.06,
        total_mass=1.5,
        selector_rate=0.04,
    )
    assert audit.current_transport_velocity == pytest.approx(0.3)
    assert audit.selector_drift_velocity == pytest.approx(0.3)
    assert audit.total_velocity == pytest.approx(0.6)


def test_general_boundary_flux_correction_matches_differentiated_quantile_identity():
    p = 0.3
    rho = 0.5
    current = 0.8
    j_left = 0.2
    j_right = -0.1
    mass = 2.0
    p_dot = 0.05
    audit = material_front_velocity(
        p=p,
        density_at_front=rho,
        current_at_front=current,
        total_mass=mass,
        selector_rate=p_dot,
        left_flux=j_left,
        right_flux=j_right,
    )
    expected = (current - (1.0 - p) * j_left - p * j_right + mass * p_dot) / rho
    assert audit.total_velocity == pytest.approx(expected)


def test_translating_logistic_fixed_quantiles_move_with_declared_velocity():
    v = 1.25
    s = 0.7
    theta = 0.9
    eps = 1e-6
    for p in (0.1, 0.25, 0.5, 0.8, 0.95):
        xp = logistic_quantile(p, theta + eps, velocity=v, scale=s)
        xm = logistic_quantile(p, theta - eps, velocity=v, scale=s)
        numeric = (xp - xm) / (2.0 * eps)
        rho = logistic_density_at_quantile(p, scale=s)
        audit = no_flux_material_front_velocity(
            p=p,
            density_at_front=rho,
            current_at_front=v * rho,
            total_mass=1.0,
        )
        assert numeric == pytest.approx(v, abs=2e-10)
        assert audit.total_velocity == pytest.approx(v, abs=2e-15)


def test_dynamic_logistic_selector_matches_transport_plus_selector_theorem():
    p = 0.35
    p_dot = 0.012
    v = -0.4
    s = 1.1
    rho = logistic_density_at_quantile(p, scale=s)
    direct = logistic_quantile_velocity(
        p,
        velocity=v,
        scale=s,
        selector_rate=p_dot,
    )
    audit = no_flux_material_front_velocity(
        p=p,
        density_at_front=rho,
        current_at_front=v * rho,
        total_mass=1.0,
        selector_rate=p_dot,
    )
    assert direct == pytest.approx(audit.total_velocity, abs=2e-15)


def test_material_front_law_is_invariant_under_common_density_current_rescaling():
    base = no_flux_material_front_velocity(
        p=0.6,
        density_at_front=0.4,
        current_at_front=0.12,
        total_mass=1.0,
        selector_rate=0.0,
    )
    scale = 7.3
    rescaled = no_flux_material_front_velocity(
        p=0.6,
        density_at_front=scale * 0.4,
        current_at_front=scale * 0.12,
        total_mass=scale,
        selector_rate=0.0,
    )
    assert rescaled.total_velocity == pytest.approx(base.total_velocity, abs=2e-15)


def test_phase_diffusion_green_function_has_derived_variance_and_sigma():
    mu = 0.3
    c = 1.7
    dt = 2.5
    diffusion = phase_diffusion_coefficient(mu, c)
    variance = phase_diffusion_variance(dt, onsager_mobility=mu, coefficient=c)
    sigma = phase_diffusion_sigma(dt, onsager_mobility=mu, coefficient=c)
    assert diffusion == pytest.approx(2.0 * mu * c)
    assert variance == pytest.approx(4.0 * mu * c * dt)
    assert sigma == pytest.approx(2.0 * math.sqrt(mu * c * dt))

    g0 = phase_diffusion_green(0.0, dt, onsager_mobility=mu, coefficient=c)
    expected_g0 = 1.0 / math.sqrt(8.0 * math.pi * mu * c * dt)
    assert g0 == pytest.approx(expected_g0, rel=1e-15)


def test_phase_diffusion_kernel_scales_with_sqrt_intrinsic_elapsed_interval():
    mu = 0.4
    c = 0.9
    sigma1 = phase_diffusion_sigma(1.0, onsager_mobility=mu, coefficient=c)
    sigma4 = phase_diffusion_sigma(4.0, onsager_mobility=mu, coefficient=c)
    assert sigma4 == pytest.approx(2.0 * sigma1)


@pytest.mark.parametrize(
    "call",
    [
        lambda: no_flux_material_front_velocity(p=0.0, density_at_front=1.0, current_at_front=0.0, total_mass=1.0),
        lambda: no_flux_material_front_velocity(p=1.0, density_at_front=1.0, current_at_front=0.0, total_mass=1.0),
        lambda: no_flux_material_front_velocity(p=0.5, density_at_front=0.0, current_at_front=0.0, total_mass=1.0),
        lambda: no_flux_material_front_velocity(p=0.5, density_at_front=1.0, current_at_front=0.0, total_mass=0.0),
        lambda: logistic_quantile(0.5, 0.0, velocity=1.0, scale=0.0),
        lambda: phase_diffusion_green(0.0, 0.0, onsager_mobility=1.0, coefficient=1.0),
        lambda: phase_diffusion_green(0.0, 1.0, onsager_mobility=0.0, coefficient=1.0),
    ],
)
def test_temporal_material_front_fails_closed(call):
    with pytest.raises(TemporalMaterialFrontError):
        call()
