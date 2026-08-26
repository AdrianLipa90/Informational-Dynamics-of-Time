from __future__ import annotations

import cmath
import math

import numpy as np

from src.idt.kahler_time import kappa
from src.idt.shannon_phase import (
    closed_cycle_link,
    closed_geometric_link,
    entropy_difference,
    pancharatnam_link,
    shannon_entropy,
    temporal_transition_link,
    transition_affinity_bits,
    cycle_affinity_bits,
    transition_link_from_affinity,
    wrap_phase,
)


def test_shannon_entropy_reference_values() -> None:
    assert math.isclose(shannon_entropy([1.0, 0.0]), 0.0, abs_tol=1e-14)
    assert math.isclose(shannon_entropy([0.5, 0.5]), 1.0, abs_tol=1e-14)


def test_entropy_difference_telescopes_on_closed_cycle() -> None:
    ps = ([0.8, 0.2], [0.5, 0.5], [0.1, 0.9], [0.8, 0.2])
    total = sum(entropy_difference(ps[i], ps[i + 1]) for i in range(len(ps) - 1))
    assert math.isclose(total, 0.0, abs_tol=1e-14)


def test_pancharatnam_closed_product_is_gauge_invariant() -> None:
    states = [
        np.array([1.0 + 0.0j, 0.2 + 0.4j]),
        np.array([0.7 + 0.1j, 0.5 - 0.2j]),
        np.array([0.4 - 0.3j, 0.9 + 0.2j]),
    ]
    base = closed_geometric_link(states)
    phases = [0.31, -1.2, 2.1]
    gauged = [cmath.exp(1j * c) * s for c, s in zip(phases, states)]
    transformed = closed_geometric_link(gauged)
    assert abs(base - transformed) < 1e-12


def test_exact_entropy_channel_cannot_change_closed_cycle_phase() -> None:
    states = [
        [1.0 + 0.0j, 0.2j],
        [0.8 + 0.1j, 0.4 - 0.2j],
        [0.3 - 0.2j, 0.9 + 0.1j],
    ]
    probs = ([0.9, 0.1], [0.5, 0.5], [0.2, 0.8])
    geom = closed_geometric_link(states)
    composite = closed_cycle_link(states, probs, entropy_production_bits=[0.0, 0.0, 0.0])
    assert abs(geom - composite) < 1e-12


def test_non_exact_entropy_production_adds_cycle_phase() -> None:
    states = [
        [1.0 + 0.0j, 0.2j],
        [0.8 + 0.1j, 0.4 - 0.2j],
        [0.3 - 0.2j, 0.9 + 0.1j],
    ]
    probs = ([0.9, 0.1], [0.5, 0.5], [0.2, 0.8])
    sigmas = [0.3, 0.2, 0.4]
    geom = closed_geometric_link(states)
    composite = closed_cycle_link(states, probs, entropy_production_bits=sigmas)
    measured = wrap_phase(cmath.phase(composite) - cmath.phase(geom))
    expected = wrap_phase(kappa() * sum(sigmas))
    assert math.isclose(measured, expected, rel_tol=0.0, abs_tol=1e-12)


def test_transition_link_binds_entropy_and_geometric_phase() -> None:
    link = temporal_transition_link(
        [1.0 + 0.0j, 0.0 + 0.0j],
        [1.0 + 0.0j, 1.0j],
        [1.0, 0.0],
        [0.5, 0.5],
        entropy_production_bits=0.25,
    )
    assert math.isclose(link.entropy_difference_bits, 1.0, abs_tol=1e-14)
    assert math.isclose(abs(link.composite_link), 1.0, abs_tol=1e-14)
    assert math.isfinite(link.phase_rad)


def test_transition_affinity_is_antisymmetric() -> None:
    ab = transition_affinity_bits(0.7, 0.2)
    ba = transition_affinity_bits(0.2, 0.7)
    assert math.isclose(ab, -ba, rel_tol=0.0, abs_tol=1e-14)


def test_symmetric_transition_has_zero_affinity() -> None:
    assert math.isclose(transition_affinity_bits(0.4, 0.4), 0.0, abs_tol=1e-14)


def test_cycle_affinity_matches_log_product_ratio() -> None:
    fwd = [0.7, 0.5, 0.9]
    rev = [0.2, 0.4, 0.3]
    measured = cycle_affinity_bits(fwd, rev)
    expected = math.log2(np.prod(fwd) / np.prod(rev))
    assert math.isclose(measured, expected, rel_tol=0.0, abs_tol=1e-14)


def test_detailed_balance_form_telescopes_cycle_affinity() -> None:
    pi = [0.2, 0.5, 0.3]
    fwd = [pi[1] / pi[0], pi[2] / pi[1], pi[0] / pi[2]]
    rev = [1.0, 1.0, 1.0]
    assert math.isclose(cycle_affinity_bits(fwd, rev), 0.0, abs_tol=1e-14)


def test_transition_link_can_close_sigma_from_path_affinity() -> None:
    link = transition_link_from_affinity(
        [1.0 + 0.0j, 0.0j],
        [0.8 + 0.1j, 0.4 - 0.2j],
        [0.8, 0.2],
        [0.5, 0.5],
        p_forward=0.8,
        p_reverse=0.2,
    )
    assert math.isclose(link.entropy_production_bits, 2.0, abs_tol=1e-14)
    assert math.isclose(abs(link.composite_link), 1.0, abs_tol=1e-14)
