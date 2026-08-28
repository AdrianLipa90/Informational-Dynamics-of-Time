import cmath
import math


def test_spin_connection_integrates_to_primitive_two_pi():
    kappa_h = 0.77
    beta_h = 2.0 * math.pi / kappa_h
    holonomy_angle = kappa_h * beta_h
    assert math.isclose(holonomy_angle, 2.0 * math.pi, rel_tol=1e-12, abs_tol=1e-12)


def test_integer_spin_representation_is_periodic():
    for m in range(-3, 4):
        W = cmath.exp(1j * 2.0 * math.pi * m)
        assert abs(W - 1.0) < 1e-12


def test_spin_half_representation_is_antiperiodic():
    W_half = cmath.exp(1j * math.pi)
    assert abs(W_half + 1.0) < 1e-12


def test_bosonic_matsubara_spacing_uses_integer_kappa_h():
    kappa_h = 0.63
    beta_h = 2.0 * math.pi / kappa_h
    for n in range(-4, 5):
        omega = 2.0 * math.pi * n / beta_h
        assert math.isclose(omega, n * kappa_h, rel_tol=1e-12, abs_tol=1e-12)


def test_fermionic_matsubara_spacing_uses_half_integer_kappa_h():
    kappa_h = 0.63
    beta_h = 2.0 * math.pi / kappa_h
    for n in range(-4, 5):
        omega = (2 * n + 1) * math.pi / beta_h
        expected = (n + 0.5) * kappa_h
        assert math.isclose(omega, expected, rel_tol=1e-12, abs_tol=1e-12)


def test_two_spin_half_turns_restore_plus_one():
    W_half = cmath.exp(1j * math.pi)
    assert abs(W_half * W_half - 1.0) < 1e-12
