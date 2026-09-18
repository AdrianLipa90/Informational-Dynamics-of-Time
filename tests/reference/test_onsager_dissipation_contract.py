import math

import numpy as np
import pytest

from idt.schrodinger_onsager_seam_balance import (
    SchrodingerOnsagerBalanceError,
    node_phase_gradient,
    onsager_dissipation,
    onsager_phase_velocity,
)


def _state():
    psi = np.array([1.0 + 0.4j, -0.3 + 0.8j, 0.7 - 0.2j, 0.2 + 0.6j], dtype=complex)
    return psi / np.linalg.norm(psi)


PHI = np.array([0.2, -0.35, 0.5])


def test_scalar_mobility_is_isotropic_onsager_matrix():
    psi = _state()
    mobility = 1.7
    scalar = onsager_dissipation(psi, PHI, mobility)
    matrix = onsager_dissipation(psi, PHI, mobility * np.eye(psi.size))
    gradient = node_phase_gradient(psi, PHI)
    expected = mobility * float(gradient @ gradient)
    assert math.isclose(scalar, matrix, rel_tol=0.0, abs_tol=2e-15)
    assert math.isclose(scalar, expected, rel_tol=0.0, abs_tol=2e-15)


def test_matrix_dissipation_matches_phase_velocity_quadratic_form():
    psi = _state()
    g = np.array(
        [
            [1.2, 0.1, 0.0, 0.0],
            [0.1, 1.0, 0.1, 0.0],
            [0.0, 0.1, 0.9, 0.05],
            [0.0, 0.0, 0.05, 0.7],
        ]
    )
    direct = onsager_dissipation(psi, PHI, g)
    _, _, from_velocity = onsager_phase_velocity(psi, PHI, g)
    assert direct >= 0.0
    assert math.isclose(direct, from_velocity, rel_tol=0.0, abs_tol=2e-15)


def test_scalar_phase_velocity_uses_same_isotropic_operator():
    psi = _state()
    mobility = 0.8
    alpha_scalar, state_scalar, diss_scalar = onsager_phase_velocity(psi, PHI, mobility)
    alpha_matrix, state_matrix, diss_matrix = onsager_phase_velocity(
        psi,
        PHI,
        mobility * np.eye(psi.size),
    )
    np.testing.assert_allclose(alpha_scalar, alpha_matrix, atol=0.0, rtol=0.0)
    np.testing.assert_allclose(state_scalar, state_matrix, atol=0.0, rtol=0.0)
    assert diss_scalar == diss_matrix


@pytest.mark.parametrize("bad", [-1.0, math.nan, math.inf, -math.inf, True])
def test_invalid_scalar_mobility_fails_closed(bad):
    with pytest.raises(SchrodingerOnsagerBalanceError):
        onsager_dissipation(_state(), PHI, bad)


def test_nonsymmetric_matrix_mobility_fails_closed():
    bad = np.eye(4)
    bad[0, 1] = 0.5
    with pytest.raises(SchrodingerOnsagerBalanceError, match="symmetric"):
        onsager_dissipation(_state(), PHI, bad)


def test_non_psd_matrix_mobility_fails_closed():
    bad = np.diag([1.0, 1.0, 1.0, -0.01])
    with pytest.raises(SchrodingerOnsagerBalanceError, match="positive semidefinite"):
        onsager_dissipation(_state(), PHI, bad)
