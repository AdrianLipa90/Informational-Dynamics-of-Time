import math


C = 299_792_458.0


def intention_charge(hbar, rhythm, intention):
    return hbar * rhythm * intention


def phase_energy(hbar, delta_tau, rhythm, intention):
    return (hbar / delta_tau) * rhythm * intention


def test_floquet_charge_energy_identity_is_exact_for_reference_scalars():
    hbar = 1.25
    delta_tau = 0.2
    rhythm = 1.7
    intention = -0.4
    j_i = intention_charge(hbar, rhythm, intention)
    h_phi = phase_energy(hbar, delta_tau, rhythm, intention)
    assert delta_tau * h_phi == j_i
    assert h_phi == (1.0 / delta_tau) * j_i


def test_epsilon_i_is_independent_of_shared_rhythm_and_intention_factor():
    hbar = 3.0
    delta_tau = 0.125
    for rhythm, intention in [(0.3, 2.0), (4.5, -0.7), (9.0, 0.25)]:
        j_i = intention_charge(hbar, rhythm, intention)
        h_phi = phase_energy(hbar, delta_tau, rhythm, intention)
        assert math.isclose(h_phi / j_i, 1.0 / delta_tau, rel_tol=0.0, abs_tol=1e-15)


def test_zero_charge_sector_preserves_operator_identity_without_division():
    hbar = 1.0
    delta_tau = 0.5
    j_i = intention_charge(hbar, 2.0, 0.0)
    h_phi = phase_energy(hbar, delta_tau, 2.0, 0.0)
    assert j_i == 0.0
    assert h_phi == 0.0
    assert delta_tau * h_phi == j_i


def test_action_charge_to_mass_coordinate_matches_phase_energy_over_c2():
    hbar = 2.0
    delta_tau = 0.25
    rhythm = 1.5
    intention = 0.8
    j_i = intention_charge(hbar, rhythm, intention)
    h_phi = phase_energy(hbar, delta_tau, rhythm, intention)
    m_from_charge = j_i / (C * C * delta_tau)
    m_from_energy = h_phi / (C * C)
    assert math.isclose(m_from_charge, m_from_energy, rel_tol=1e-15, abs_tol=0.0)


def test_positive_time_step_is_required_for_finite_energy_per_action_charge():
    for delta_tau in (1.0, 0.5, 0.01):
        epsilon_i = 1.0 / delta_tau
        assert math.isfinite(epsilon_i)
        assert epsilon_i > 0.0
