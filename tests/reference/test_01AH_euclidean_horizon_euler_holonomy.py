import cmath
import math


def test_primitive_euclidean_horizon_period_closes_at_two_pi():
    kappa_h = 0.37
    beta_h = 2.0 * math.pi / kappa_h
    phi_h = kappa_h * beta_h
    assert math.isclose(phi_h, 2.0 * math.pi, rel_tol=1e-12, abs_tol=1e-12)


def test_primitive_horizon_holonomy_is_unity():
    kappa_h = 0.91
    beta_h = 2.0 * math.pi / kappa_h
    W = cmath.exp(1j * kappa_h * beta_h)
    assert abs(W - 1.0) < 1e-12


def test_hawking_temperature_is_inverse_primitive_period():
    kappa_h = 1.23
    beta_h = 2.0 * math.pi / kappa_h
    T_h = 1.0 / beta_h
    assert math.isclose(T_h, kappa_h / (2.0 * math.pi), rel_tol=1e-12, abs_tol=1e-12)


def test_detuned_period_has_nonzero_conical_defect():
    kappa_h = 0.8
    beta_h = 2.0 * math.pi / kappa_h
    beta_bad = 1.07 * beta_h
    delta_cone = 2.0 * math.pi - kappa_h * beta_bad
    assert abs(delta_cone) > 1e-3


def test_detuned_period_has_nontrivial_holonomy():
    kappa_h = 0.8
    beta_h = 2.0 * math.pi / kappa_h
    beta_bad = 0.93 * beta_h
    W_bad = cmath.exp(1j * kappa_h * beta_bad)
    assert abs(W_bad - 1.0) > 1e-3


def test_integer_multicovers_close_holonomy():
    kappa_h = 0.44
    for n in range(1, 6):
        beta_n = 2.0 * math.pi * n / kappa_h
        W = cmath.exp(1j * kappa_h * beta_n)
        assert abs(W - 1.0) < 1e-12


def test_ab_and_horizon_maps_share_u1_exponential_structure():
    # Structural isomorphism only: two separately typed loop phases enter exp(i Phi).
    phi_ab = 1.7
    phi_h = 1.7
    assert cmath.exp(1j * phi_ab) == cmath.exp(1j * phi_h)
