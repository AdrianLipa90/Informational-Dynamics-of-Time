import math


C = 299_792_458.0


def euler_intention_phase(*, D, epsilon_eb, phi_ab, phi_berry, phi_euler, theta_prior=0.0):
    return 2.0 * math.pi * (D + epsilon_eb) - phi_ab - phi_berry - phi_euler - theta_prior


def euler_action_charge(*, hbar, theta_i):
    return hbar * theta_i


def rotor_phase_energy(*, j_total, j_i, i_phi):
    if i_phi <= 0.0:
        raise ValueError("i_phi must be positive")
    return (j_total - j_i) ** 2 / (2.0 * i_phi)


def epsilon_after_euler(*, h_phi, j_i):
    if j_i <= 0.0 or h_phi <= 0.0:
        raise ValueError("positive non-degenerate sector required")
    return h_phi / j_i


def test_euler_closure_residual_fixes_next_intention_phase():
    theta_i = euler_intention_phase(
        D=1,
        epsilon_eb=0.0,
        phi_ab=math.pi / 2.0,
        phi_berry=math.pi / 4.0,
        phi_euler=math.pi / 4.0,
    )
    assert math.isclose(theta_i, math.pi, rel_tol=0.0, abs_tol=1e-15)


def test_euler_phase_fixes_action_charge_before_energy_normalization():
    theta_i = math.pi
    hbar = 2.0
    j_i = euler_action_charge(hbar=hbar, theta_i=theta_i)
    assert math.isclose(j_i, 2.0 * math.pi, rel_tol=0.0, abs_tol=1e-15)


def test_rotor_energy_is_derived_without_assuming_floquet_time_step():
    j_i = math.pi
    j_total = 2.0 * math.pi
    i_phi = 2.0
    h_phi = rotor_phase_energy(j_total=j_total, j_i=j_i, i_phi=i_phi)
    assert math.isclose(h_phi, math.pi**2 / 4.0, rel_tol=0.0, abs_tol=1e-15)


def test_epsilon_is_derived_after_euler_and_rotor_then_fixes_effective_time_step():
    j_i = math.pi
    h_phi = math.pi**2 / 4.0
    epsilon_i = epsilon_after_euler(h_phi=h_phi, j_i=j_i)
    delta_tau_eff = 1.0 / epsilon_i
    assert math.isclose(epsilon_i, math.pi / 4.0, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(delta_tau_eff, 4.0 / math.pi, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(delta_tau_eff * h_phi, j_i, rel_tol=1e-15, abs_tol=0.0)


def test_mass_coordinate_equals_euler_closed_rotor_energy_over_c2():
    j_i = math.pi
    h_phi = math.pi**2 / 4.0
    epsilon_i = epsilon_after_euler(h_phi=h_phi, j_i=j_i)
    m_from_charge = epsilon_i * j_i / (C * C)
    m_from_energy = h_phi / (C * C)
    assert math.isclose(m_from_charge, m_from_energy, rel_tol=1e-15, abs_tol=0.0)


def test_ratio_gate_fails_closed_for_zero_charge_or_zero_rotor_energy():
    for h_phi, j_i in ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0)):
        try:
            epsilon_after_euler(h_phi=h_phi, j_i=j_i)
        except ValueError:
            pass
        else:
            raise AssertionError("degenerate sector must fail closed before epsilon ratio")


def test_rotor_inertia_must_be_positive():
    try:
        rotor_phase_energy(j_total=2.0, j_i=1.0, i_phi=0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("non-positive rotor inertia must fail closed")
