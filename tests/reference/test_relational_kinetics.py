from __future__ import annotations

import math

from src.idt.relational_kinetics import (
    cycle_drive,
    directed_rates,
    exact_edge_drive,
    pair_mobility,
)


def test_pair_mobility_is_positive_and_swap_symmetric() -> None:
    ab = pair_mobility(2.0, 8.0, 3.0, 5.0)
    ba = pair_mobility(8.0, 2.0, 5.0, 3.0)
    assert ab > 0.0
    assert math.isclose(ab, ba, rel_tol=0.0, abs_tol=1e-14)


def test_edge_drive_sets_affinity_while_mobility_cancels() -> None:
    x = directed_rates(1.0, 4.0, 2.0, 6.0, edge_drive=0.7)
    y = directed_rates(100.0, 400.0, 20.0, 60.0, edge_drive=0.7)
    expected = 0.7 / math.log(2.0)
    assert math.isclose(x.affinity_bits, expected, abs_tol=1e-14)
    assert math.isclose(y.affinity_bits, expected, abs_tol=1e-14)


def test_reversing_drive_swaps_forward_reverse_rates() -> None:
    pos = directed_rates(3.0, 5.0, 2.0, 4.0, edge_drive=0.9)
    neg = directed_rates(3.0, 5.0, 2.0, 4.0, edge_drive=-0.9)
    assert math.isclose(pos.forward, neg.reverse, abs_tol=1e-14)
    assert math.isclose(pos.reverse, neg.forward, abs_tol=1e-14)
    assert math.isclose(pos.affinity_bits, -neg.affinity_bits, abs_tol=1e-14)


def test_exact_state_potential_drive_telescopes_on_cycle() -> None:
    v = [0.2, 1.1, -0.4]
    edges = [
        exact_edge_drive(v[0], v[1]),
        exact_edge_drive(v[1], v[2]),
        exact_edge_drive(v[2], v[0]),
    ]
    assert math.isclose(cycle_drive(edges), 0.0, abs_tol=1e-14)


def test_non_exact_edge_drive_can_have_nonzero_circulation() -> None:
    assert math.isclose(cycle_drive([0.3, 0.5, -0.2]), 0.6, abs_tol=1e-14)
