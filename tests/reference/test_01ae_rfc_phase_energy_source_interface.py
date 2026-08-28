import math


def omega_q(d_t_chi, n_r):
    if n_r <= 0:
        raise ValueError("N_R must be positive")
    return d_t_chi / n_r


def j_theta(amplitude, omega):
    return 2.0 * amplitude**2 * omega


def e_theta(amplitude, omega):
    return amplitude**2 * omega**2


def test_energy_per_carrier_handoff():
    amplitude, omega = 1.3, 2.4
    epsilon_n = omega / 2.0
    assert math.isclose(e_theta(amplitude, omega), epsilon_n * j_theta(amplitude, omega), rel_tol=1e-15)


def test_mass_density_consumer_coordinate():
    amplitude, omega, c = 0.8, 3.1, 299792458.0
    rho_energy = e_theta(amplitude, omega) / c**2
    rho_carrier = (omega / 2.0) * j_theta(amplitude, omega) / c**2
    assert math.isclose(rho_energy, rho_carrier, rel_tol=1e-15)


def test_lapse_rate_export():
    d_t_chi, n_r = 7.2, 1.8
    omega = omega_q(d_t_chi, n_r)
    assert math.isclose(omega, 4.0, rel_tol=1e-15)
    assert math.isclose(omega / 2.0, d_t_chi / (2.0 * n_r), rel_tol=1e-15)


def test_nonuniform_local_factorization():
    data = [(0.5, 1.2), (1.1, 2.0), (0.9, 3.3)]
    for amplitude, omega in data:
        assert math.isclose(
            e_theta(amplitude, omega),
            (omega / 2.0) * j_theta(amplitude, omega),
            rel_tol=1e-15,
        )
