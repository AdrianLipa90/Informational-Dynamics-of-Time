import math

import numpy as np

from idt.zeta_collatz_frame_continuum import (
    continuum_diagnostics_from_mobilities,
    first_merge_edge_mobilities,
    first_merge_witness,
    weighted_path_laplacian,
    zeta_collatz_path_continuum_diagnostics,
    zeta_ordered_first_merge_distances,
)
from idt.zeta_collatz_temporal_fuzziness import is_prime


def _first_primes(count: int) -> list[int]:
    values: list[int] = []
    candidate = 2
    while len(values) < count:
        if is_prime(candidate):
            values.append(candidate)
        candidate += 1
    return values


def _first_odd_composites(count: int) -> list[int]:
    values: list[int] = []
    candidate = 9
    while len(values) < count:
        if candidate % 2 == 1 and not is_prime(candidate):
            values.append(candidate)
        candidate += 2
    return values


def test_first_merge_distance_uses_earliest_shared_descendant_not_terminal_tail_length():
    witness = first_merge_witness(3, 5)
    assert witness.merge_value == 5
    assert witness.steps_left == 2
    assert witness.steps_right == 0
    assert witness.distance == 2

    reverse = first_merge_witness(5, 3)
    assert reverse.merge_value == witness.merge_value
    assert reverse.distance == witness.distance
    assert reverse.steps_left == witness.steps_right
    assert reverse.steps_right == witness.steps_left


def test_zeta_ordered_first_merge_geometry_is_non_degenerate_and_local_path_is_sparse():
    primes = _first_primes(64)
    distances = zeta_ordered_first_merge_distances(primes)
    assert distances.shape == (63,)
    assert np.min(distances) > 0.0
    assert np.unique(distances).size > 10

    mobilities = first_merge_edge_mobilities(distances)
    lap = weighted_path_laplacian(mobilities)
    np.testing.assert_allclose(lap, lap.T, rtol=0.0, atol=0.0)
    assert np.min(np.linalg.eigvalsh(lap)) > -1e-10

    off_diagonal = lap.copy()
    np.fill_diagonal(off_diagonal, 0.0)
    undirected_edges = int(np.count_nonzero(np.triu(off_diagonal, 1)))
    assert undirected_edges == len(primes) - 1


def test_prime_first_merge_path_low_modes_converge_toward_one_dimensional_continuum():
    small = zeta_collatz_path_continuum_diagnostics(_first_primes(64), modes=5)
    large = zeta_collatz_path_continuum_diagnostics(_first_primes(256), modes=5)

    assert small.mean_absolute_relative_error < 0.10
    assert large.mean_absolute_relative_error < 0.03
    assert large.mean_absolute_relative_error < 0.4 * small.mean_absolute_relative_error
    assert all(0.90 < ratio < 1.03 for ratio in large.mode_ratios)


def test_composite_seed_null_also_homogenizes_so_continuum_is_not_prime_specific_by_itself():
    prime_diag = zeta_collatz_path_continuum_diagnostics(_first_primes(256), modes=5)
    composite_diag = zeta_collatz_path_continuum_diagnostics(
        _first_odd_composites(256),
        modes=5,
        require_primes=False,
    )

    assert prime_diag.mean_absolute_relative_error < 0.03
    assert composite_diag.mean_absolute_relative_error < 0.06
    # The low-mode continuum follows from positive local heterogeneous path
    # coarse-graining; this null prevents promotion of prime specificity from
    # continuum emergence alone.
    assert composite_diag.mean_absolute_relative_error < 2.5 * prime_diag.mean_absolute_relative_error


def test_randomized_mobility_order_null_can_match_or_beat_prime_order_finite_size_error():
    primes = _first_primes(256)
    distances = zeta_ordered_first_merge_distances(primes)
    mobilities = first_merge_edge_mobilities(distances)
    _, _, _, _, prime_error = continuum_diagnostics_from_mobilities(mobilities, modes=5)

    rng = np.random.default_rng(20260828)
    randomized_errors = []
    for _ in range(32):
        shuffled = mobilities.copy()
        rng.shuffle(shuffled)
        _, _, _, _, error = continuum_diagnostics_from_mobilities(shuffled, modes=5)
        randomized_errors.append(error)

    assert min(randomized_errors) < prime_error
    assert max(randomized_errors) > prime_error


def test_first_merge_mobility_has_no_fitted_length_scale():
    distances = np.array([0.0, 1.0, 3.0, 9.0])
    mobility = first_merge_edge_mobilities(distances)
    np.testing.assert_allclose(mobility, [1.0, 0.5, 0.25, 0.1], rtol=0.0, atol=0.0)
    assert math.isclose(float(mobility[0]), 1.0, rel_tol=0.0, abs_tol=0.0)
