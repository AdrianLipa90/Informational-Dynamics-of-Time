import math


def calibrated_omega(dphi_dtau, dt_dtau):
    assert dt_dtau > 0.0
    return dphi_dtau / dt_dtau


def phase_length(c, omega):
    assert abs(omega) > 0.0
    return c / abs(omega)


def test_clock_chain_rule():
    dphi_dtau = 12.0
    dt_dtau = 3.0
    assert calibrated_omega(dphi_dtau, dt_dtau) == 4.0


def test_phase_length_energy_equivalence():
    hbar = 1.054_571_817e-34
    c = 299_792_458.0
    omega = 2.5e15
    energy = hbar * abs(omega)
    ell_omega = phase_length(c, omega)
    ell_energy = hbar * c / energy
    assert math.isclose(ell_omega, ell_energy, rel_tol=1e-15)


def test_spinorial_cycle_ratio():
    ell = 3.25
    l_2pi = 2.0 * math.pi * ell
    l_4pi = 4.0 * math.pi * ell
    assert math.isclose(l_2pi / l_4pi, 0.5, rel_tol=0.0, abs_tol=1e-15)


def test_constant_cell_information_curvature_forms_agree():
    info_bits = 0.7
    kappa = math.log(2.0) / (24.0 * math.pi)
    a_fs = 0.8
    omega = 4.2
    c = 7.3
    j_nats = math.log(2.0) * info_bits
    xi_direct = (j_nats / a_fs) * (omega / c) ** 2
    xi_kappa = (24.0 * math.pi * kappa * info_bits / a_fs) * (omega / c) ** 2
    assert math.isclose(xi_direct, xi_kappa, rel_tol=1e-15)


def test_full_cp1_reduction():
    info_bits = 0.4
    kappa = math.log(2.0) / (24.0 * math.pi)
    omega = 1.7
    c = 2.3
    xi_general = (24.0 * math.pi * kappa * info_bits / math.pi) * (omega / c) ** 2
    xi_full = 24.0 * kappa * info_bits * (omega / c) ** 2
    assert math.isclose(xi_general, xi_full, rel_tol=1e-15)
