import math

import numpy as np

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec, propagate_orchorbital
from src.idt.orchorbital_residence_ledger import (
    build_residence_receipts,
    dwell_time_statistics,
    residence_episodes,
    transition_counts_from_receipts,
    verify_residence_receipts,
)


def _state(x, y, vx, vy):
    return MemoryPhaseState(
        np.array([x, y], dtype=float),
        np.array([vx, vy], dtype=float),
        0.0,
        0.0,
    )


def test_long_boundary_crossing_profile_has_replayable_residence_statistics():
    attractors = [
        AttractorSpec("A", np.array([0.0, 0.0], dtype=float), 2.0),
        AttractorSpec("B", np.array([4.0, 0.0], dtype=float), 2.0),
    ]
    delta_taus = [0.5] + [0.005] * 100
    steps = propagate_orchorbital(
        _state(1.6, 0.4, 1.0, 0.0),
        attractors,
        delta_taus,
    )
    receipts = build_residence_receipts(steps)
    verify_residence_receipts(receipts)

    assert len(steps) == 101
    assert len(receipts) == 101
    assert receipts[0].active_attractor == "A"
    assert receipts[1].active_attractor == "B"
    assert transition_counts_from_receipts(receipts).get(("A", "B"), 0) >= 1

    episodes = residence_episodes(receipts)
    stats = dwell_time_statistics(receipts)
    assert len(episodes) >= 2
    assert {item.name for item in stats}.issuperset({"A", "B"})

    total_dwell = sum(item.dwell_tau for item in episodes)
    assert math.isclose(total_dwell, sum(delta_taus), rel_tol=0.0, abs_tol=2e-12)
    assert all(item.segments > 0 and item.dwell_tau > 0.0 for item in episodes)
    assert all(
        math.isfinite(item.total_dwell_tau)
        and math.isfinite(item.mean_dwell_tau)
        and math.isfinite(item.median_dwell_tau)
        and math.isfinite(item.variance_dwell_tau)
        for item in stats
    )
