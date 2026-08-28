import numpy as np

from idt.zeta_collatz_temporal_fuzziness import is_prime
from idt.zeta_zero_collatz_phase_discriminator import (
    closed_gradient_holonomy,
    closed_gradient_links,
    load_reference_zero_ordinates,
    local_zero_phase_contrast,
    prime_gap_phase_texture,
    prime_vertex_phases,
    reference_zero_phase_ratios,
    symmetric_local_frequency_controls,
)


def _prime_block(start: int, count: int) -> list[int]:
    values: list[int] = []
    candidate = 2
    target = start + count
    while len(values) < target:
        if is_prime(candidate):
            values.append(candidate)
        candidate += 1
    return values[start:target]


def test_reference_zero_fixture_is_frozen_and_strictly_ordered():
    gamma = load_reference_zero_ordinates()
    assert gamma.shape == (20,)
    assert np.all(np.diff(gamma) > 0.0)
    assert abs(float(gamma[0]) - 14.134725141734694) < 1e-14
    assert abs(float(gamma[-1]) - 77.1448400688748) < 1e-13


def test_prime_gap_phase_texture_has_unit_modulus():
    primes = _prime_block(100, 64)
    phase = prime_gap_phase_texture(primes, load_reference_zero_ordinates()[0])
    np.testing.assert_allclose(np.abs(phase), 1.0, rtol=0.0, atol=2e-15)


def test_neighbor_phase_texture_is_exact_vertex_gradient():
    primes = _prime_block(100, 64)
    gamma = load_reference_zero_ordinates()[3]
    vertex = prime_vertex_phases(primes, gamma)
    expected = vertex[1:] * np.conjugate(vertex[:-1])
    np.testing.assert_allclose(prime_gap_phase_texture(primes, gamma), expected, rtol=0.0, atol=2e-15)


def test_closed_exact_gradient_has_trivial_holonomy_for_zero_and_off_zero_frequencies():
    primes = _prime_block(100, 64)
    frequencies = list(load_reference_zero_ordinates()[:5]) + [17.25, 33.0, 71.5]
    for gamma in frequencies:
        links = closed_gradient_links(primes, gamma)
        np.testing.assert_allclose(np.abs(links), 1.0, rtol=0.0, atol=2e-15)
        holonomy = closed_gradient_holonomy(primes, gamma)
        assert abs(holonomy - 1.0) < 5e-13


def test_local_frequency_controls_are_symmetric_and_frozen_before_scoring():
    gamma = load_reference_zero_ordinates()[4]
    controls = symmetric_local_frequency_controls(gamma)
    np.testing.assert_allclose(
        np.sort(controls - gamma),
        np.sort(-(controls - gamma)),
        rtol=0.0,
        atol=2e-15,
    )


def test_zeta_zero_phase_scores_are_locally_neutral_in_bulk_prime_windows():
    # The symmetric off-zero controls remove smooth gamma dependence. Under the
    # present phase-texture statistic the recorded zero ordinates are locally
    # indistinguishable from nearby frequencies in all predeclared bulk windows.
    for start in [50, 100, 250, 500, 1000]:
        ratios = reference_zero_phase_ratios(_prime_block(start, 128))
        assert np.all(np.isfinite(ratios))
        assert abs(float(np.mean(ratios)) - 1.0) < 5e-4
        assert float(np.max(np.abs(ratios - 1.0))) < 2e-3


def test_individual_zero_contrast_uses_no_fitted_frequency_shift():
    primes = _prime_block(250, 128)
    for gamma in load_reference_zero_ordinates()[:5]:
        zero_score, control_mean, ratio = local_zero_phase_contrast(primes, gamma)
        assert zero_score > 0.0
        assert control_mean > 0.0
        assert 0.998 < ratio < 1.002
