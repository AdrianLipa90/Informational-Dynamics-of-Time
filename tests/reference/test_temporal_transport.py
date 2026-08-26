from __future__ import annotations

import numpy as np
import pytest

from src.idt.bifurcation import polar_bifurcation_operator
from src.idt.temporal_transport import TemporalTransportError, interrupted_temporal_propagator, ordered_event_product

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
D = np.diag([0.1, 0.7]).astype(complex)


def test_empty_event_sequence_is_identity_when_dimension_declared():
    assert np.allclose(ordered_event_product([], dimension=2), I2, atol=1e-14, rtol=0.0)


def test_ordered_event_product_keeps_declared_event_order():
    b1 = polar_bifurcation_operator(0.2, 0.3, D, SIGMA_X).operator
    b2 = polar_bifurcation_operator(0.4, -0.2, D, SIGMA_Y).operator
    measured = ordered_event_product([b1, b2])
    assert np.allclose(measured, b2 @ b1, atol=1e-14, rtol=0.0)
    assert not np.allclose(measured, b1 @ b2, atol=1e-10, rtol=0.0)


def test_interrupted_propagator_matches_explicit_product():
    u0 = np.array([[1.0,0.0],[0.0,1.0j]], dtype=complex)
    u1 = np.array([[0.0,1.0],[1.0,0.0]], dtype=complex)
    u2 = np.array([[1.0j,0.0],[0.0,1.0]], dtype=complex)
    b1 = polar_bifurcation_operator(0.2, 0.1, D, SIGMA_X).operator
    b2 = polar_bifurcation_operator(0.3, -0.15, D, SIGMA_Y).operator
    assert np.allclose(interrupted_temporal_propagator([u0,u1,u2],[b1,b2]), u2 @ b2 @ u1 @ b1 @ u0, atol=1e-14, rtol=0.0)


def test_interrupted_propagator_fails_on_bad_segment_count():
    with pytest.raises(TemporalTransportError):
        interrupted_temporal_propagator([I2], [I2])
