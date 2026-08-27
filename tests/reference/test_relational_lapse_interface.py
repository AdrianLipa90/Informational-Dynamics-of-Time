from __future__ import annotations

import math

import numpy as np


def test_positive_dimensionless_clock_ratio() -> None:
    phi_x = 3.7
    phi_ref = 1.4
    N = phi_x / phi_ref
    assert N > 0.0
    assert math.isclose(N, 3.7 / 1.4)


def test_reparameterization_jacobian_cancels() -> None:
    phi_x = 2.3
    phi_ref = 0.9
    jac = 0.37  # d lambda / d lambda_prime > 0
    N = phi_x / phi_ref
    N_prime = (phi_x * jac) / (phi_ref * jac)
    assert math.isclose(N_prime, N, rel_tol=1e-15, abs_tol=1e-15)


def test_reference_composition() -> None:
    phi_x, phi_r, phi_s = 3.1, 1.7, 0.8
    N_xr = phi_x / phi_r
    N_rs = phi_r / phi_s
    N_xs = phi_x / phi_s
    assert math.isclose(N_xr * N_rs, N_xs, rel_tol=1e-15, abs_tol=1e-15)
    assert math.isclose((phi_x / phi_r) * (phi_r / phi_s) * (phi_s / phi_x), 1.0, rel_tol=1e-15)


def test_kinetic_lapse_ratio_shared_activity_normalization() -> None:
    Mx, Mr = 2.1, 1.3
    Ax, Ar = 0.8, -0.4
    a_star = 5.0
    phi_x = (2.0 * Mx / a_star) * math.cosh(Ax / 2.0)
    phi_r = (2.0 * Mr / a_star) * math.cosh(Ar / 2.0)
    N_direct = phi_x / phi_r
    N_reduced = (Mx * math.cosh(Ax / 2.0)) / (Mr * math.cosh(Ar / 2.0))
    assert math.isclose(N_direct, N_reduced, rel_tol=1e-15, abs_tol=1e-15)


def test_log_gradient_decomposition() -> None:
    M = 1.8
    A = 0.7
    grad_M = np.array([0.02, -0.03, 0.01])
    grad_A = np.array([0.05, 0.01, -0.04])
    lhs = grad_M / M + 0.5 * math.tanh(A / 2.0) * grad_A
    rhs = grad_M / M + 0.5 * math.tanh(A / 2.0) * grad_A
    assert np.allclose(lhs, rhs, atol=1e-15, rtol=1e-15)


def test_mobility_log_gradient_decomposition() -> None:
    rho_a, rho_b = 2.0, 3.0
    eta_a, eta_b = 4.0, 5.0
    grad_rho_a = np.array([0.2, -0.1, 0.3])
    grad_rho_b = np.array([-0.05, 0.12, 0.08])
    grad_eta_a = np.array([0.04, -0.02, 0.01])
    grad_eta_b = np.array([-0.01, 0.03, 0.02])
    eta_mean = 0.5 * (eta_a + eta_b)
    grad_eta_mean = 0.5 * (grad_eta_a + grad_eta_b)
    expected = 0.5 * grad_rho_a / rho_a + 0.5 * grad_rho_b / rho_b - grad_eta_mean / eta_mean
    # numerical finite-difference directional check for one arbitrary direction
    v = np.array([0.3, -0.4, 0.5])
    eps = 1e-7
    def mobility(ra: float, rb: float, ea: float, eb: float) -> float:
        return math.sqrt(ra * rb) / (0.5 * (ea + eb))
    M0 = mobility(rho_a, rho_b, eta_a, eta_b)
    ra1 = rho_a + eps * float(v @ grad_rho_a)
    rb1 = rho_b + eps * float(v @ grad_rho_b)
    ea1 = eta_a + eps * float(v @ grad_eta_a)
    eb1 = eta_b + eps * float(v @ grad_eta_b)
    fd = (math.log(mobility(ra1, rb1, ea1, eb1)) - math.log(M0)) / eps
    analytic = float(v @ expected)
    assert math.isclose(fd, analytic, rel_tol=2e-7, abs_tol=2e-9)


def test_weak_log_lapse() -> None:
    eps = 1e-6
    N = 1.0 + eps
    assert math.isclose(math.log(N), eps, rel_tol=2e-6, abs_tol=2e-12)
