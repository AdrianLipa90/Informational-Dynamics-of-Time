import math

import numpy as np
import pytest

from src.idt.event_memory_kick import (
    EventMemoryKickError,
    apply_derived_memory_event_impulse,
    derived_kick_invariant_changes,
    derived_memory_kick,
    memory_event_action,
)
from src.idt.memory_dynamics import (
    memory_angular_momentum,
    memory_energy,
    projected_imprint,
    projective_event_imprint,
)

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)


def test_event_action_gradient_equals_derived_kick():
    m = 0.7 - 0.2j
    dm = 0.12 + 0.08j
    q = 0.35
    eps = 1e-7
    dS_dx = (memory_event_action(m + eps, dm, q) - memory_event_action(m - eps, dm, q)) / (2 * eps)
    dS_dy = (memory_event_action(m + 1j * eps, dm, q) - memory_event_action(m - 1j * eps, dm, q)) / (2 * eps)
    kick = derived_memory_kick(dm, q)
    assert dS_dx == pytest.approx(kick.real, abs=1e-9)
    assert dS_dy == pytest.approx(kick.imag, abs=1e-9)


def test_zero_event_weight_gives_zero_kick():
    assert derived_memory_kick(0.4 - 0.3j, 0.0) == 0j


def test_zero_projected_imprint_gives_zero_kick():
    assert derived_memory_kick(0j, 0.8) == 0j


def test_kick_scales_with_upstream_event_weight():
    dm = 0.3 + 0.4j
    assert derived_memory_kick(dm, 0.6) == pytest.approx(3.0 * derived_memory_kick(dm, 0.2))


def test_global_phase_invariance_propagates_to_kick():
    state_minus = np.array([1, 0], dtype=complex)
    state_plus = np.array([1, 1j], dtype=complex) / math.sqrt(2)
    d0 = projective_event_imprint(state_minus, state_plus)
    dm0 = projected_imprint(d0, X, Y)
    kick0 = derived_memory_kick(dm0, 0.5)

    d1 = projective_event_imprint(state_minus * np.exp(1.1j), state_plus * np.exp(-0.7j))
    dm1 = projected_imprint(d1, X, Y)
    kick1 = derived_memory_kick(dm1, 0.5)
    assert kick1 == pytest.approx(kick0, abs=1e-14)


def test_exact_energy_and_angular_momentum_jump_formulas():
    m = 1.1 + 0.3j
    v = -0.2 + 0.5j
    dm = 0.08 - 0.04j
    q = 0.7
    mu = 1.3
    kick = q * dm
    _, v_plus = apply_derived_memory_event_impulse(m, v, dm, q)
    dE, dh = derived_kick_invariant_changes(m, v, dm, q, mu)
    expected_dE = (v.conjugate() * kick).real + 0.5 * abs(kick) ** 2
    expected_dh = (m.conjugate() * kick).imag
    assert dE == pytest.approx(expected_dE, abs=1e-14)
    assert dh == pytest.approx(expected_dh, abs=1e-14)
    assert memory_energy(m, v_plus, mu) - memory_energy(m, v, mu) == pytest.approx(expected_dE, abs=1e-14)
    assert memory_angular_momentum(m, v_plus) - memory_angular_momentum(m, v) == pytest.approx(expected_dh, abs=1e-14)


def test_negative_event_weight_fails_closed():
    with pytest.raises(EventMemoryKickError):
        derived_memory_kick(0.1 + 0.2j, -0.1)
