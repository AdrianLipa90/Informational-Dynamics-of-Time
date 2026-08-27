import numpy as np
import pytest
from src.idt.phase_connection_forcing import *


def _states(seed=7, n=5, d=3):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        z = rng.normal(size=d) + 1j * rng.normal(size=d)
        out.append(z / np.linalg.norm(z))
    return out


def test_any_exact_scalar_cycle_telescopes():
    assert abs(float(np.sum(exact_cycle_edges([.2, 1.4, -.6, 2.1])))) < 1e-15


def test_composite_cycle_identity_is_berry_plus_affinity():
    states = _states()
    H = np.array([.2, 1.1, -.4, .8, 1.7])
    sigma = np.array([.3, -.2, .4, .1, .25])
    berry = cycle_pancharatnam_links(states)
    links = composite_temporal_links(states, H, sigma)
    expected = cycle_holonomy_phase(berry) + KAPPA * float(np.sum(sigma))
    assert abs(principal_phase_difference(cycle_holonomy_phase(links), expected)) < 1e-12


def test_closed_holonomy_is_gauge_invariant():
    states = _states(seed=9)
    H = np.linspace(-1, 1, 5)
    sigma = np.array([.2, .1, -.05, .4, .3])
    links = composite_temporal_links(states, H, sigma)
    chi = np.array([.7, -.2, 1.4, .3, -1.1])
    links2 = composite_temporal_links(rephase_states(states, chi), H, sigma)
    assert abs(principal_phase_difference(cycle_holonomy_phase(links2), cycle_holonomy_phase(links))) < 1e-12


def test_link_gauge_law_matches_temporal_wave_covariant_difference():
    states = _states(seed=11, n=4, d=2)
    H = [.1, .2, .5, -.3]
    sigma = [.2, -.1, .05, .4]
    L = composite_temporal_links(states, H, sigma)
    chi = np.array([.4, -.7, .8, 1.2])
    Lp = transform_links(L, chi)
    q = np.array([1 + .2j, -.3 + .8j, .7 - .1j, -.5 - .4j])
    qp = np.exp(1j * chi) * q
    d = covariant_cycle_difference(q, L)
    dp = covariant_cycle_difference(qp, Lp)
    expected = np.exp(1j * np.roll(chi, -1)) * d
    assert np.linalg.norm(dp - expected) < 1e-12


def test_exact_scalar_reweighting_cannot_change_closed_cycle_phase():
    states = _states(seed=13, n=4, d=3)
    sigma = np.zeros(4)
    L1 = composite_temporal_links(states, [0, 0, 0, 0], sigma)
    L2 = composite_temporal_links(states, [2, -1, 5, .5], sigma)
    assert abs(principal_phase_difference(cycle_holonomy_phase(L1), cycle_holonomy_phase(L2))) < 1e-12


def test_invalid_inputs_fail_closed():
    with pytest.raises(PhaseConnectionError):
        composite_temporal_links(_states(n=3), [1, 2], [1, 2, 3])
