import math

import numpy as np
import pytest

from idt.zeta_collatz_temporal_fuzziness import (
    ZetaCollatzFuzzinessError,
    build_prime_frames,
    collatz_frame_laplacian,
    collatz_orbit,
    collatz_overlap_matrix,
    frame_participation_number,
    frame_probabilities,
    prime_factor_amplitude,
    propagate_frame_amplitudes,
    temporal_fuzziness_moments,
    temporal_fuzzy_field,
    unitary_propagator,
    zeta_collatz_hamiltonian,
    zeta_prime_generator,
)


PRIMES = [3, 5, 7, 11, 13]


def test_prime_frames_carry_verified_collatz_lineages():
    frames = build_prime_frames(PRIMES)
    assert [f.prime for f in frames] == PRIMES
    assert all(f.collatz_orbit[0] == f.prime for f in frames)
    assert all(f.collatz_orbit[-1] == 1 for f in frames)
    assert all(len(f.collatz_edges) > 0 for f in frames)


def test_prime_factor_has_exact_log_prime_spectral_generator():
    p = 11
    sigma = 0.73
    tau = 4.2
    eps = 1e-6
    z0 = prime_factor_amplitude(p, sigma, tau)
    zp = prime_factor_amplitude(p, sigma, tau + eps)
    zm = prime_factor_amplitude(p, sigma, tau - eps)
    derivative = (zp - zm) / (2.0 * eps)
    lhs = 1j * derivative
    rhs = math.log(p) * z0
    assert abs(lhs - rhs) < 2e-9


def test_collatz_overlap_is_symmetric_bounded_and_zero_diagonal():
    frames = build_prime_frames(PRIMES)
    w = collatz_overlap_matrix(frames)
    np.testing.assert_allclose(w, w.T, rtol=0.0, atol=0.0)
    np.testing.assert_allclose(np.diag(w), 0.0, rtol=0.0, atol=0.0)
    assert np.min(w) >= 0.0
    assert np.max(w) <= 1.0
    assert np.count_nonzero(w) > 0


def test_collatz_frame_laplacian_is_hermitian_psd():
    frames = build_prime_frames(PRIMES)
    lap = collatz_frame_laplacian(frames)
    np.testing.assert_allclose(lap, lap.T, rtol=0.0, atol=1e-14)
    eigenvalues = np.linalg.eigvalsh(lap)
    assert np.min(eigenvalues) > -1e-12
    assert abs(float(eigenvalues[0])) < 1e-12


def test_centred_zeta_prime_generator_preserves_relative_log_frequencies():
    frames = build_prime_frames(PRIMES)
    dz = zeta_prime_generator(frames, centred=True)
    diag = np.diag(dz)
    assert abs(float(np.sum(diag))) < 1e-14
    expected = math.log(13) - math.log(3)
    actual = float(diag[-1] - diag[0])
    assert math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-14)


def test_zeta_collatz_hamiltonian_is_hermitian():
    frames = build_prime_frames(PRIMES)
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.7, collatz_coupling=1.3)
    np.testing.assert_allclose(h, h.conj().T, rtol=0.0, atol=1e-13)
    assert np.all(np.isreal(np.linalg.eigvalsh(h)))


def test_intrinsic_theta_propagator_is_unitary():
    frames = build_prime_frames(PRIMES)
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.9, collatz_coupling=0.8)
    u = unitary_propagator(h, 0.37)
    np.testing.assert_allclose(u.conj().T @ u, np.eye(len(frames)), rtol=0.0, atol=2e-14)


def test_zero_collatz_coupling_keeps_a_sharp_frame_population_sharp():
    frames = build_prime_frames(PRIMES)
    h = zeta_collatz_hamiltonian(frames, zeta_scale=1.0, collatz_coupling=0.0)
    psi0 = np.zeros(len(frames), dtype=complex)
    psi0[0] = 1.0
    psi = propagate_frame_amplitudes(psi0, h, 3.1)
    p = frame_probabilities(psi)
    np.testing.assert_allclose(p, [1.0, 0.0, 0.0, 0.0, 0.0], rtol=0.0, atol=2e-14)
    assert math.isclose(frame_participation_number(psi), 1.0, rel_tol=0.0, abs_tol=2e-14)


def test_connected_collatz_coupling_spreads_a_sharp_frame():
    frames = build_prime_frames(PRIMES)
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.6, collatz_coupling=1.0)
    psi0 = np.zeros(len(frames), dtype=complex)
    psi0[0] = 1.0
    psi = propagate_frame_amplitudes(psi0, h, 0.8)
    p = frame_probabilities(psi)
    assert p[0] < 0.999
    assert float(np.max(p[1:])) > 1e-4
    assert frame_participation_number(psi) > 1.0
    assert math.isclose(float(np.sum(p)), 1.0, rel_tol=0.0, abs_tol=2e-14)


def test_frame_permutation_preserves_hamiltonian_spectrum():
    frames = build_prime_frames(PRIMES)
    permuted = tuple(frames[i] for i in [2, 4, 0, 3, 1])
    h0 = zeta_collatz_hamiltonian(frames, zeta_scale=0.4, collatz_coupling=1.2)
    h1 = zeta_collatz_hamiltonian(permuted, zeta_scale=0.4, collatz_coupling=1.2)
    np.testing.assert_allclose(
        np.sort(np.linalg.eigvalsh(h0)),
        np.sort(np.linalg.eigvalsh(h1)),
        rtol=0.0,
        atol=2e-13,
    )


def test_continuous_fuzzy_field_is_normalized_and_finite():
    frames = build_prime_frames(PRIMES)
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.5, collatz_coupling=1.0)
    psi0 = np.zeros(len(frames), dtype=complex)
    psi0[2] = 1.0
    psi = propagate_frame_amplitudes(psi0, h, 0.65)

    anchors = np.array([0.0, 0.7, 1.5, 2.4, 3.6])
    grid = np.linspace(-1.0, 4.6, 4001)
    field, density = temporal_fuzzy_field(grid, anchors, psi, width=0.18)
    assert np.all(np.isfinite(field))
    assert np.all(np.isfinite(density))
    assert np.min(density) >= 0.0
    integral = float(np.trapezoid(density, grid))
    assert math.isclose(integral, 1.0, rel_tol=0.0, abs_tol=2e-12)
    mean, variance = temporal_fuzziness_moments(grid, density)
    assert math.isfinite(mean)
    assert variance > 0.0


def test_packet_width_controls_continuous_fuzziness_for_one_frame():
    anchors = np.array([0.0, 1.0, 2.0])
    psi = np.array([0.0, 1.0, 0.0], dtype=complex)
    grid = np.linspace(-1.0, 3.0, 6001)

    _, narrow = temporal_fuzzy_field(grid, anchors, psi, width=0.08)
    _, broad = temporal_fuzzy_field(grid, anchors, psi, width=0.25)
    _, var_narrow = temporal_fuzziness_moments(grid, narrow)
    _, var_broad = temporal_fuzziness_moments(grid, broad)
    assert var_broad > var_narrow


def test_unverified_or_invalid_frame_inputs_fail_closed():
    with pytest.raises(ZetaCollatzFuzzinessError):
        build_prime_frames([3, 9, 11])
    with pytest.raises(ZetaCollatzFuzzinessError):
        build_prime_frames([3, 3, 5])
    with pytest.raises(ZetaCollatzFuzzinessError):
        collatz_orbit(27, max_steps=1)
    with pytest.raises(ZetaCollatzFuzzinessError):
        temporal_fuzzy_field([0.0, 1.0], [1.0, 0.0], [1.0, 0.0], width=0.1)
