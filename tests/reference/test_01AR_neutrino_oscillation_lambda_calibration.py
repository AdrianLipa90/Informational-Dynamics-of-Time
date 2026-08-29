import math

import pytest

from idt.neutrino_oscillation_lambda_calibration import (
    C_SI,
    HBAR_EV_S,
    calibrated_lambda_board,
    lambda_amplitude_fraction,
    lambda_phase_gain_from_rotor_rate,
    neutrino_oscillation_length_m,
    neutrino_probability_phase_rad,
    neutrino_probability_phase_rate_rad_s,
    neutrino_relative_state_phase_rate_rad_s,
)
from idt.qhtri_rotor_lambda_neutrino import rotor_lambda_neutrino_drive


def test_state_phase_rate_is_exactly_twice_probability_phase_rate():
    dm2 = 2.5e-3
    energy = 1.0e9
    omega_prob = neutrino_probability_phase_rate_rad_s(dm2, energy)
    omega_state = neutrino_relative_state_phase_rate_rad_s(dm2, energy)
    assert omega_state == pytest.approx(2.0 * omega_prob, rel=0.0, abs=1e-18)


def test_standard_km_gev_probability_phase_coefficient():
    # delta_prob = K * Delta m^2[eV^2] * L[km] / E[GeV]
    k = 1000.0 / (4.0 * 1.0e9 * HBAR_EV_S * C_SI)
    assert k == pytest.approx(1.2669326791370843, rel=1e-13)


def test_oscillation_length_advances_probability_phase_by_pi():
    dm2 = 7.5e-5
    energy = 5.0e6
    losc = neutrino_oscillation_length_m(dm2, energy)
    phase = neutrino_probability_phase_rad(dm2, energy, losc)
    assert phase == pytest.approx(math.pi, rel=1e-13)


def test_lambda_phase_gain_maps_rotor_chi_rate_to_probability_phase_rate():
    dm2 = 2.45e-3
    energy = 8.0e8
    chi_rate = 17.0
    gain = lambda_phase_gain_from_rotor_rate(dm2, energy, chi_rate)
    assert gain * chi_rate == pytest.approx(
        neutrino_probability_phase_rate_rad_s(dm2, energy), rel=1e-13
    )


def test_lambda_amplitude_fraction_inverts_A_equals_lambda_E_over_four():
    energy = 40.0
    amp = 3.0
    lam = lambda_amplitude_fraction(energy, amp)
    assert lam == pytest.approx(0.3)
    assert lam * energy / 4.0 == pytest.approx(amp)


def test_calibrated_board_binds_rotor_rate_to_neutrino_phase_and_spin2_double():
    dm2 = 2.5e-3
    energy_ev = 1.0e9
    chi_rate = 11.0
    total_j = 20.0
    amp_j = 1.0
    cal = calibrated_lambda_board(
        dm2,
        energy_ev,
        chi_rate,
        total_j,
        amp_j,
    )
    # Choose pure counter-rotation: tau_dot=0 and chi_dot=chi_rate.
    drive = rotor_lambda_neutrino_drive(
        theta_plus_rad=0.4,
        theta_minus_rad=-0.4,
        omega_plus_rad_s=chi_rate,
        omega_minus_rad_s=-chi_rate,
        total_energy_joule=total_j,
        board=cal.board,
    )
    assert drive.rotor.tau_rate_rad_s == pytest.approx(0.0)
    assert drive.rotor.chi_rate_rad_s == pytest.approx(chi_rate)
    assert drive.carrier_phase_rate_rad_s == pytest.approx(
        cal.probability_phase_rate_rad_s, rel=1e-13
    )
    assert 2.0 * drive.carrier_phase_rate_rad_s == pytest.approx(
        cal.relative_state_phase_rate_rad_s, rel=1e-13
    )
    assert drive.modulation_joule == pytest.approx(amp_j)
    assert max(abs(x) for x in drive.collision_four_moment_power_watt) < 1e-12


def test_calibration_fails_closed_on_invalid_inputs():
    with pytest.raises(ValueError):
        neutrino_probability_phase_rate_rad_s(0.0, 1.0e9)
    with pytest.raises(ValueError):
        neutrino_probability_phase_rate_rad_s(2.5e-3, 0.0)
    with pytest.raises(ValueError):
        lambda_phase_gain_from_rotor_rate(2.5e-3, 1.0e9, 0.0)
    with pytest.raises(ValueError):
        lambda_amplitude_fraction(10.0, 3.0)
