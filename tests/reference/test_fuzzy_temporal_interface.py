from __future__ import annotations

import math

import numpy as np
import pytest

from idt.fuzzy_temporal_interface import (
    FuzzyTemporalInterfaceError,
    amplitude_balance,
    audit_seam_interface,
    baseline_subtraction_residual,
    chain_fuzzy_coherence,
    decomposition_residual,
    fuzzy_interface_profile,
    fuzzy_interface_strength,
    gauge_invariant_mismatch,
    normalized_fraction_residual,
    one_seam_onsager_fuzzy_rate,
)
from idt.onsager_half_seam_phase_locking import integrate_single_seam
from idt.zeta_collatz_temporal_fuzziness import (
    build_prime_frames,
    propagate_frame_amplitudes,
    zeta_collatz_hamiltonian,
)


def test_exact_defect_decomposition_and_pair_fraction_identity():
    left = 0.7 * np.exp(0.4j)
    right = 0.3 * np.exp(1.1j)
    phi = -0.25
    audit = audit_seam_interface(left, right, phi)
    assert decomposition_residual(left, right, phi) < 1e-14
    assert normalized_fraction_residual(left, right, phi) < 1e-14
    assert baseline_subtraction_residual(left, right, phi) < 1e-14
    assert math.isclose(audit.overlap_fraction + audit.defect_fraction, 1.0, abs_tol=1e-14)


def test_fuzzy_strength_is_bounded_and_gauge_invariant():
    left = 0.6 * np.exp(0.3j)
    right = 0.8 * np.exp(-0.7j)
    phi = 0.2
    base = fuzzy_interface_strength(left, right, phi)
    assert 0.0 <= base <= 1.0

    chi0 = 0.91
    chi1 = -0.44
    transformed = fuzzy_interface_strength(
        np.exp(1j * chi0) * left,
        np.exp(1j * chi1) * right,
        phi + chi1 - chi0,
    )
    assert math.isclose(base, transformed, rel_tol=0.0, abs_tol=1e-14)


def test_sharp_frame_has_no_genuine_neighboring_fuzziness():
    assert fuzzy_interface_strength(1.0 + 0.0j, 0.0 + 0.0j, 0.0) == 0.0
    assert amplitude_balance(1.0 + 0.0j, 0.0 + 0.0j) == 0.0


def test_equal_in_phase_neighbors_are_maximally_fuzzy_interface():
    left = np.exp(0.2j) / math.sqrt(2.0)
    right = np.exp(0.2j) / math.sqrt(2.0)
    audit = audit_seam_interface(left, right, 0.0)
    assert math.isclose(audit.amplitude_balance, 1.0, abs_tol=1e-14)
    assert math.isclose(audit.fuzzy_strength, 1.0, abs_tol=1e-14)
    assert math.isclose(audit.defect_probability, 0.0, abs_tol=1e-14)


def test_equal_antiphase_neighbors_are_interface_null_control():
    left = 1.0 / math.sqrt(2.0)
    right = -1.0 / math.sqrt(2.0)
    audit = audit_seam_interface(left, right, 0.0)
    assert math.isclose(audit.amplitude_balance, 1.0, abs_tol=1e-14)
    assert math.isclose(audit.fuzzy_strength, 0.0, abs_tol=1e-14)
    assert math.isclose(audit.overlap_probability, 0.0, abs_tol=1e-14)


def test_one_seam_onsager_locking_increases_fuzzy_strength_at_analytic_rate():
    r0 = 0.6
    r1 = 0.8
    delta = 1.1
    mobility = 1.7
    left = complex(r0)
    right = r1 * np.exp(1j * delta)

    analytic = one_seam_onsager_fuzzy_rate(left, right, 0.0, mobility)
    assert analytic > 0.0

    eps = 1e-6
    trajectory = integrate_single_seam(delta, r0, r1, mobility, eps, steps=20)
    delta_next = float(trajectory[-1])
    f0 = fuzzy_interface_strength(left, right, 0.0)
    f1 = fuzzy_interface_strength(complex(r0), r1 * np.exp(1j * delta_next), 0.0)
    finite_rate = (f1 - f0) / eps
    assert f1 > f0
    assert math.isclose(finite_rate, analytic, rel_tol=2e-6, abs_tol=2e-8)


def test_profile_and_chain_coherence_for_fully_locked_equal_chain():
    state = np.ones(4, dtype=complex) / 2.0
    phases = np.zeros(3)
    profile = fuzzy_interface_profile(state, phases)
    assert np.allclose(profile, np.ones(3), rtol=0.0, atol=1e-14)
    assert math.isclose(chain_fuzzy_coherence(state, phases), 1.0, abs_tol=1e-14)


def test_zeta_schrodinger_spreading_then_locking_creates_joint_interface():
    frames = build_prime_frames([2, 3])
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.35, collatz_coupling=1.0)
    sharp = np.asarray([1.0 + 0.0j, 0.0 + 0.0j])
    assert fuzzy_interface_strength(sharp[0], sharp[1], 0.0) == 0.0

    spread = propagate_frame_amplitudes(sharp, h, 0.4)
    assert abs(spread[0]) > 1e-8
    assert abs(spread[1]) > 1e-8
    assert amplitude_balance(spread[0], spread[1]) > 0.0

    delta = gauge_invariant_mismatch(spread[0], spread[1], 0.0)
    before = fuzzy_interface_strength(spread[0], spread[1], 0.0)
    locked = integrate_single_seam(delta, abs(spread[0]), abs(spread[1]), 2.0, 0.8, steps=2000)
    after_state_left = complex(abs(spread[0]))
    after_state_right = abs(spread[1]) * np.exp(1j * locked[-1])
    after = fuzzy_interface_strength(after_state_left, after_state_right, 0.0)
    assert after >= before - 1e-12
    if abs(math.sin(delta)) > 1e-6:
        assert after > before


@pytest.mark.parametrize(
    "call",
    [
        lambda: fuzzy_interface_profile([1.0 + 0.0j], []),
        lambda: fuzzy_interface_profile([1.0 + 0.0j, 0.0 + 0.0j], [0.0, 1.0]),
        lambda: fuzzy_interface_profile([complex(float('nan'), 0.0), 1.0 + 0.0j], [0.0]),
        lambda: one_seam_onsager_fuzzy_rate(1.0 + 0.0j, 1.0 + 0.0j, 0.0, 0.0),
    ],
)
def test_fuzzy_interface_gate_fails_closed(call):
    with pytest.raises(FuzzyTemporalInterfaceError):
        call()
