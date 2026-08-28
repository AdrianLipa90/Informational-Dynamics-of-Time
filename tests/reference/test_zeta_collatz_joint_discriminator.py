import numpy as np

from idt.zeta_collatz_frame_continuum import (
    first_merge_edge_mobilities,
    zeta_ordered_first_merge_distances,
)
from idt.zeta_collatz_joint_discriminator import (
    balanced_joint_hamiltonian,
    centred_log_frequency_operator,
    centred_path_operator_from_mobilities,
    empirical_lower_tail_fraction,
    joint_alignment_diagnostics,
    permuted_mobility_commutator_scores,
)
from idt.zeta_collatz_temporal_fuzziness import is_prime


def _prime_block(start: int, count: int) -> list[int]:
    values: list[int] = []
    candidate = 2
    target = start + count
    while len(values) < target:
        if is_prime(candidate):
            values.append(candidate)
        candidate += 1
    return values[start:target]


def _mobility(primes: list[int]) -> np.ndarray:
    distances = zeta_ordered_first_merge_distances(primes)
    return first_merge_edge_mobilities(distances)


def _alignment_percentile(primes: list[int]) -> tuple[float, float, np.ndarray]:
    mobility = _mobility(primes)
    diagnostic = joint_alignment_diagnostics(primes)
    null = permuted_mobility_commutator_scores(
        primes,
        mobility,
        permutations=128,
        rng_seed=20260828,
    )
    percentile = empirical_lower_tail_fraction(diagnostic.commutator_score, null)
    return diagnostic.commutator_score, percentile, null


def test_balanced_joint_operator_is_hermitian_and_finite():
    primes = _prime_block(0, 32)
    mobility = _mobility(primes)
    d = centred_log_frequency_operator(primes)
    k = centred_path_operator_from_mobilities(mobility)
    h = balanced_joint_hamiltonian(d, k)
    np.testing.assert_allclose(h, h.T, rtol=0.0, atol=1e-14)
    assert np.all(np.isfinite(np.linalg.eigvalsh(h)))


def test_low_prime_window_has_extreme_joint_alignment_against_mobility_permutation_null():
    primes = _prime_block(0, 64)
    score, percentile, null = _alignment_percentile(primes)
    assert score > float(np.max(null))
    assert percentile == 1.0


def test_joint_alignment_extremeness_does_not_persist_across_bulk_prime_windows():
    starts = [10, 50, 100, 250, 500]
    percentiles = []
    for start in starts:
        _, percentile, _ = _alignment_percentile(_prime_block(start, 64))
        percentiles.append(percentile)

    central = [p for p in percentiles if 0.10 <= p <= 0.90]
    assert len(central) >= 3
    assert min(percentiles) < 0.10
    assert max(percentiles) < 0.95


def test_low_prime_extremeness_is_a_boundary_sector_control_not_a_bulk_promotion_gate():
    _, low_percentile, _ = _alignment_percentile(_prime_block(0, 64))
    _, bulk_percentile, _ = _alignment_percentile(_prime_block(100, 64))
    assert low_percentile > 0.99
    assert 0.10 < bulk_percentile < 0.90
