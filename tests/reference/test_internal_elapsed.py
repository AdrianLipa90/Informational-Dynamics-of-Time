from __future__ import annotations

import math

import numpy as np

from src.idt.internal_elapsed import cumulative_elapsed_activity, elapsed_increment, reparameterize_activity
from src.idt.temporal_activity import activity_current_from_fields


def test_elapsed_activity_is_strictly_monotone_for_positive_activity() -> None:
    tau = cumulative_elapsed_activity([1.0, 2.0, 0.5], [0.2, 0.3, 0.4], reference_activity=1.0)
    assert np.all(np.diff(tau) > 0.0)


def test_reparameterization_covariance_of_elapsed_increment() -> None:
    a = 2.4
    dl = 0.15
    jac = 3.5
    base = elapsed_increment(a, dl, reference_activity=1.2)
    transformed = elapsed_increment(
        reparameterize_activity(a, jac),
        jac * dl,
        reference_activity=1.2,
    )
    assert math.isclose(base, transformed, rel_tol=0.0, abs_tol=1e-14)


def test_density_scales_internal_activity_pace() -> None:
    low = activity_current_from_fields(1.0, 1.0, 2.0, 2.0, 0.4).activity
    high = activity_current_from_fields(4.0, 4.0, 2.0, 2.0, 0.4).activity
    assert math.isclose(high, 4.0 * low, rel_tol=0.0, abs_tol=1e-14)


def test_viscosity_reduces_internal_activity_pace() -> None:
    low_eta = activity_current_from_fields(2.0, 2.0, 1.0, 1.0, 0.4).activity
    high_eta = activity_current_from_fields(2.0, 2.0, 4.0, 4.0, 0.4).activity
    assert math.isclose(high_eta, 0.25 * low_eta, rel_tol=0.0, abs_tol=1e-14)


def test_drive_reversal_keeps_elapsed_pace_but_flips_current() -> None:
    pos = activity_current_from_fields(2.0, 3.0, 1.0, 1.5, 0.8)
    neg = activity_current_from_fields(2.0, 3.0, 1.0, 1.5, -0.8)
    assert math.isclose(pos.activity, neg.activity, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pos.current, -neg.current, rel_tol=0.0, abs_tol=1e-14)
