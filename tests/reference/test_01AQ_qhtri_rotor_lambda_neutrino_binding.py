import math

import numpy as np
import pytest

from idt.neutrino_conserved_quadrupole import phase_quadrupole_source
from idt.neutrino_phase_transport import phase_quadrupole_stream_power_rates
from idt.qhtri_rotor_lambda_neutrino import (
    LambdaBoard,
    minkowski_rotor_state,
    relative_neutrino_metronome_drive,
    rotor_lambda_neutrino_drive,
)


def test_two_rotors_give_exact_common_spin_decomposition_and_minkowski_form_identity():
    state = minkowski_rotor_state(1.7, -0.4, 3.2, -1.1)
    assert state.tau_rad == pytest.approx((1.7 - 0.4) / 2.0)
    assert state.chi_rad == pytest.approx((1.7 + 0.4) / 2.0)
    assert state.tau_rate_rad_s == pytest.approx((3.2 - 1.1) / 2.0)
    assert state.chi_rate_rad_s == pytest.approx((3.2 + 1.1) / 2.0)
    assert state.interval_like_rad2 == pytest.approx(1.7 * -0.4, abs=1e-15)


def test_counter_rotation_changes_spin_coordinate_without_changing_common_coordinate():
    base = minkowski_rotor_state(0.8, -0.2, 2.5, -2.5)
    shifted = minkowski_rotor_state(0.8 + 0.37, -0.2 - 0.37, 2.5, -2.5)
    assert shifted.tau_rad == pytest.approx(base.tau_rad, abs=1e-15)
    assert shifted.chi_rad - base.chi_rad == pytest.approx(0.37, abs=1e-15)
    assert base.tau_rate_rad_s == pytest.approx(0.0, abs=1e-15)
    assert base.chi_rate_rad_s == pytest.approx(2.5, abs=1e-15)


def test_lambda_board_maps_spin_coordinate_to_relative_not_global_flavour_phase():
    board = LambdaBoard(
        coupling_fraction=0.6,
        common_gain=0.0,
        spin_gain=1.25,
        phase_bias_rad=0.2,
        flavour_gains=(1.0, -0.25, -0.75),
    )
    drive = rotor_lambda_neutrino_drive(
        theta_plus_rad=1.1,
        theta_minus_rad=-0.3,
        omega_plus_rad_s=4.0,
        omega_minus_rad_s=-2.0,
        total_energy_joule=80.0,
        board=board,
    )
    expected_phi = 0.2 + 1.25 * drive.rotor.chi_rad
    expected_phidot = 1.25 * drive.rotor.chi_rate_rad_s
    assert drive.carrier_phase_rad == pytest.approx(expected_phi)
    assert drive.carrier_phase_rate_rad_s == pytest.approx(expected_phidot)
    assert sum(drive.flavour_phase_shifts_rad) == pytest.approx(0.0, abs=1e-12)
    assert sum(drive.flavour_phase_rates_rad_s) == pytest.approx(0.0, abs=1e-12)
    assert drive.flavour_phase_shifts_rad[0] != drive.flavour_phase_shifts_rad[1]


def test_lambda_strength_is_exact_quadrupole_amplitude_fraction():
    energy = 120.0
    for lam in np.linspace(0.0, 1.0, 9):
        drive = rotor_lambda_neutrino_drive(
            0.9,
            -0.1,
            1.0,
            -1.0,
            energy,
            LambdaBoard(coupling_fraction=float(lam)),
        )
        assert drive.modulation_joule == pytest.approx(float(lam) * energy / 4.0)
        assert min(drive.quadrupole.pair_energies_joule) >= -1e-12


def test_01AQ_exactly_reproduces_01AO_source_and_01AP_transport():
    board = LambdaBoard(
        coupling_fraction=0.4,
        common_gain=0.3,
        spin_gain=1.2,
        phase_bias_rad=-0.17,
    )
    drive = rotor_lambda_neutrino_drive(
        theta_plus_rad=1.4,
        theta_minus_rad=-0.6,
        omega_plus_rad_s=5.0,
        omega_minus_rad_s=-1.0,
        total_energy_joule=64.0,
        board=board,
    )
    direct_source = phase_quadrupole_source(
        drive.total_energy_joule,
        drive.modulation_joule,
        drive.carrier_phase_rad,
    )
    direct_rates = phase_quadrupole_stream_power_rates(
        drive.modulation_joule,
        drive.carrier_phase_rad,
        drive.carrier_phase_rate_rad_s,
    )
    assert drive.quadrupole.pair_energies_joule == pytest.approx(
        direct_source.pair_energies_joule
    )
    assert np.allclose(
        drive.quadrupole.source.tensor_joule,
        direct_source.source.tensor_joule,
        rtol=0.0,
        atol=1e-12,
    )
    assert drive.stream_power_rates_watt == pytest.approx(direct_rates, abs=1e-12)
    assert max(abs(x) for x in drive.collision_four_moment_power_watt) < 1e-12


def test_default_pure_spin_board_recovers_spin2_tt_coordinates():
    energy = 40.0
    lam = 0.5
    amp = lam * energy / 4.0
    for chi in np.linspace(-math.pi, math.pi, 13):
        # theta_+=chi, theta_-=-chi gives tau=0 and differential coordinate chi.
        drive = rotor_lambda_neutrino_drive(
            float(chi),
            float(-chi),
            0.0,
            0.0,
            energy,
            LambdaBoard(coupling_fraction=lam),
        )
        s = drive.quadrupole.source.spatial_stress_joule
        plus = 0.5 * (s[0][0] - s[1][1])
        cross = s[0][1]
        assert plus == pytest.approx(amp * math.cos(2.0 * chi), abs=1e-12)
        assert cross == pytest.approx(amp * math.sin(2.0 * chi), abs=1e-12)


def test_relative_metronome_and_lambda_validation_fail_closed():
    with pytest.raises(ValueError):
        relative_neutrino_metronome_drive(0.0, 1.0, (1.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        LambdaBoard(coupling_fraction=1.1)
    with pytest.raises(ValueError):
        LambdaBoard(flavour_gains=(1.0, -1.0, 0.1))
    with pytest.raises(ValueError):
        minkowski_rotor_state(float("nan"), 0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        rotor_lambda_neutrino_drive(0.0, 0.0, 0.0, 0.0, 0.0)
