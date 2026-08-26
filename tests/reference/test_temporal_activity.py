from __future__ import annotations

import math

from src.idt.relational_kinetics import directed_rates, pair_mobility
from src.idt.temporal_activity import (
    activity_current_from_fields,
    activity_current_from_rates,
    atomic_support,
    image_support,
    positive_activity_measure,
    pushforward_positive_measure,
)


def test_activity_current_has_hyperbolic_decomposition() -> None:
    rho_a, rho_b, eta_a, eta_b, A = 2.0, 8.0, 3.0, 5.0, 0.7
    M = pair_mobility(rho_a, rho_b, eta_a, eta_b)
    ac = activity_current_from_fields(rho_a, rho_b, eta_a, eta_b, A)
    assert math.isclose(ac.activity, 2.0 * M * math.cosh(A / 2.0), rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(ac.current, 2.0 * M * math.sinh(A / 2.0), rel_tol=0.0, abs_tol=1e-14)


def test_drive_reversal_preserves_activity_and_flips_current() -> None:
    pos = activity_current_from_fields(3.0, 5.0, 2.0, 4.0, 0.9)
    neg = activity_current_from_fields(3.0, 5.0, 2.0, 4.0, -0.9)
    assert math.isclose(pos.activity, neg.activity, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pos.current, -neg.current, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pos.affinity_bits, -neg.affinity_bits, rel_tol=0.0, abs_tol=1e-14)


def test_activity_current_recovers_drive_and_affinity() -> None:
    rates = directed_rates(2.0, 7.0, 1.5, 4.0, -0.63)
    ac = activity_current_from_rates(rates.forward, rates.reverse)
    assert math.isclose(ac.drive, -0.63, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(ac.affinity_bits, rates.affinity_bits, rel_tol=0.0, abs_tol=1e-14)
    assert abs(ac.current) < ac.activity


def test_positive_activity_atoms_aggregate_without_cancellation() -> None:
    measure = positive_activity_measure(["a", "a", "b"], [0.3, 0.7, 0.5])
    assert measure == {"a": 1.0, "b": 0.5}
    assert atomic_support(measure) == {"a", "b"}


def test_positive_pushforward_support_equals_image_without_injectivity() -> None:
    measure = positive_activity_measure(["a", "b", "c"], [0.2, 0.4, 0.8])
    mapping = {"a": "x", "b": "x", "c": "y"}
    pushed = pushforward_positive_measure(measure, mapping)
    assert math.isclose(pushed["x"], 0.6, rel_tol=0.0, abs_tol=1e-14)
    assert math.isclose(pushed["y"], 0.8, rel_tol=0.0, abs_tol=1e-14)
    assert atomic_support(pushed) == image_support(atomic_support(measure), mapping)
