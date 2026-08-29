import math

import pytest

from idt.neutrino_conserved_quadrupole import phase_quadrupole_source
from idt.neutrino_physical_stress import integrated_massless_stress
from idt.neutrino_tt_observable_lambda import (
    require_01ao_lambda_bound,
    spin2_phase_residual_rad,
    transverse_tt_observable_z,
)


def test_01ao_source_inverts_exactly_to_lambda_and_phase():
    energy = 40.0
    lam = 0.3
    amp = lam * energy / 4.0
    for phi in (-2.4, -0.8, 0.0, 0.37, 1.2, 2.8):
        source = phase_quadrupole_source(energy, amp, phi).source
        obs = transverse_tt_observable_z(source)
        assert obs.amplitude_joule == pytest.approx(amp, rel=1e-13, abs=1e-13)
        assert obs.lambda_amplitude_fraction == pytest.approx(lam, rel=1e-13)
        assert abs(spin2_phase_residual_rad(obs.phase_rad_mod_pi, phi)) < 1e-13
        assert require_01ao_lambda_bound(obs) == pytest.approx(lam)


def test_lambda_inversion_is_invariant_under_total_energy_scaling():
    phi = 0.51
    lam = 0.72
    source_a = phase_quadrupole_source(10.0, lam * 10.0 / 4.0, phi).source
    source_b = phase_quadrupole_source(1.0e6, lam * 1.0e6 / 4.0, phi).source
    obs_a = transverse_tt_observable_z(source_a)
    obs_b = transverse_tt_observable_z(source_b)
    assert obs_a.lambda_amplitude_fraction == pytest.approx(lam)
    assert obs_b.lambda_amplitude_fraction == pytest.approx(lam)
    assert abs(spin2_phase_residual_rad(obs_a.phase_rad_mod_pi, obs_b.phase_rad_mod_pi)) < 1e-13


def test_isotropic_tetrahedral_control_has_zero_transverse_lambda():
    s3 = 1.0 / math.sqrt(3.0)
    dirs = [
        (s3, s3, s3),
        (s3, -s3, -s3),
        (-s3, s3, -s3),
        (-s3, -s3, s3),
    ]
    source = integrated_massless_stress(dirs, [1.0, 1.0, 1.0, 1.0])
    obs = transverse_tt_observable_z(source, zero_tolerance_joule=1e-12)
    assert obs.amplitude_joule < 1e-12
    assert obs.lambda_amplitude_fraction < 1e-12
    assert obs.phase_rad_mod_pi == 0.0


def test_generic_source_outside_01ao_bound_is_exposed_not_clipped():
    # Two x-directed packets have E=2 and T_xx=2, hence A_obs=1 and Lambda_A=2.
    source = integrated_massless_stress([(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)], [1.0, 1.0])
    obs = transverse_tt_observable_z(source)
    assert obs.lambda_amplitude_fraction == pytest.approx(2.0)
    with pytest.raises(ValueError):
        require_01ao_lambda_bound(obs)


def test_spin2_phase_residual_respects_pi_periodicity():
    for phi in (-3.0, -0.5, 0.4, 2.7):
        assert abs(spin2_phase_residual_rad(phi + math.pi, phi)) < 1e-13
        assert abs(spin2_phase_residual_rad(phi - math.pi, phi)) < 1e-13


def test_observable_validation_fails_closed():
    source = phase_quadrupole_source(10.0, 1.0, 0.2).source
    with pytest.raises(ValueError):
        transverse_tt_observable_z(source, zero_tolerance_joule=-1.0)
    with pytest.raises(ValueError):
        spin2_phase_residual_rad(float("nan"), 0.0)
