import math

import numpy as np
import pytest

from idt.fuzzy_temporal_front import (
    FuzzyTemporalFrontError,
    expected_interface_orders,
    expected_leading_path_products,
    front_total_and_barycenter,
    fuzzy_interface_mass,
    interface_identity_residual,
    locked_front_leading_coefficients,
    path_power_certificate,
    sharp_boundary_locked_front,
)
from idt.zeta_collatz_frame_continuum import (
    first_merge_edge_mobilities,
    weighted_path_laplacian,
    zeta_ordered_first_merge_distances,
)


def _path_adjacency(n: int) -> np.ndarray:
    h = np.zeros((n, n), dtype=float)
    for i in range(n - 1):
        h[i, i + 1] = 1.0
        h[i + 1, i] = 1.0
    return h


def test_raw_interface_mass_exact_identity():
    left = 0.7 * np.exp(0.2j)
    right = 0.4 * np.exp(1.1j)
    seam = 0.35
    assert interface_identity_residual(left, right, seam) < 1e-14


def test_interface_mass_sharp_and_antiphase_controls():
    assert fuzzy_interface_mass(1.0 + 0.0j, 0.0 + 0.0j, 0.0) == 0.0
    left = 1.0 / math.sqrt(2.0)
    right = -1.0 / math.sqrt(2.0)
    assert fuzzy_interface_mass(left, right, 0.0) < 1e-15


def test_locked_equal_pair_has_unit_interface_mass_for_normalized_two_frame_state():
    left = 1.0 / math.sqrt(2.0)
    right = 1.0 / math.sqrt(2.0)
    assert math.isclose(fuzzy_interface_mass(left, right, 0.0), 1.0, rel_tol=0.0, abs_tol=1e-14)


def test_path_power_distance_theorem_and_leading_product():
    h = _path_adjacency(5)
    cert = path_power_certificate(h)
    assert cert.lower_power_max_abs < 1e-15
    assert cert.frame_orders == (0, 1, 2, 3, 4)
    assert cert.interface_orders == (1, 3, 5, 7)

    products = expected_leading_path_products(h)
    for target in range(5):
        matrix_value = np.linalg.matrix_power(h, target)[target, 0]
        assert np.allclose(matrix_value, products[target], rtol=0.0, atol=1e-14)


def test_expected_fuzzy_front_orders_are_odd():
    np.testing.assert_array_equal(expected_interface_orders(6), [1, 3, 5, 7, 9])


def test_locked_front_leading_coefficients_are_positive_on_connected_path():
    coeffs = locked_front_leading_coefficients(_path_adjacency(5))
    assert coeffs.shape == (4,)
    assert np.all(coeffs > 0.0)


def test_finite_unitary_front_matches_short_time_power_ratios():
    h = _path_adjacency(4)
    _, j1 = sharp_boundary_locked_front(h, 0.02)
    _, j2 = sharp_boundary_locked_front(h, 0.04)
    ratios = j2 / j1
    targets = 2.0 ** expected_interface_orders(4)
    np.testing.assert_allclose(ratios, targets, rtol=2e-3, atol=0.0)


def test_zeta_ordered_first_merge_collatz_path_satisfies_front_certificate():
    primes = [2, 3, 5, 7, 11]
    distances = zeta_ordered_first_merge_distances(primes, require_primes=True)
    mobilities = first_merge_edge_mobilities(distances)
    lap = weighted_path_laplacian(mobilities, normalized_interval=False)
    logp = np.log(np.asarray(primes, dtype=float))
    zeta = np.diag(logp - np.mean(logp))
    h = zeta + 0.7 * lap

    cert = path_power_certificate(h)
    assert cert.lower_power_max_abs < 1e-12
    assert all(abs(c) > 0.0 for c in cert.leading_coefficients)
    np.testing.assert_array_equal(cert.interface_orders, [1, 3, 5, 7])


def test_front_total_and_barycenter():
    total, bary = front_total_and_barycenter([0.4, 0.2, 0.0])
    assert math.isclose(total, 0.6, abs_tol=1e-15)
    assert math.isclose(bary, 4.0 / 3.0, abs_tol=1e-15)
    zero_total, zero_bary = front_total_and_barycenter([0.0, 0.0])
    assert zero_total == 0.0
    assert math.isnan(zero_bary)


@pytest.mark.parametrize(
    "call",
    [
        lambda: expected_interface_orders(1),
        lambda: path_power_certificate(np.eye(3)),
        lambda: front_total_and_barycenter([-0.1, 0.2]),
    ],
)
def test_front_gate_fails_closed(call):
    with pytest.raises(FuzzyTemporalFrontError):
        call()
