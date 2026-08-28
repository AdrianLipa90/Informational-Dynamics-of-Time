from __future__ import annotations

import numpy as np

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.memory_recall import MemoryEventReceipt
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_orchorbital_residence_conditioning import (
    build_memory_orchorbital_residence_cells,
    verify_memory_orchorbital_residence_cells,
)


def test_large_internal_time_binds_schedule_to_observed_binary64_increment() -> None:
    initial = MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=36.0,
        swept_area=0.0,
    )
    attractors = (
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    )
    event = MemoryEventReceipt(1.0e-8, 1.0, 0.001 - 0.002j)
    cells = build_memory_orchorbital_residence_cells(initial, attractors, (event,))
    verify_memory_orchorbital_residence_cells(cells)

    cell = cells[0]
    scheduled = float.fromhex(cell.memory_delta_tau_hex)
    tau_before = float.fromhex(cell.tau_before_event_hex)
    observed = (tau_before + scheduled) - tau_before

    assert observed != scheduled
    assert cell.residence_receipt.delta_tau_hex == observed.hex()
