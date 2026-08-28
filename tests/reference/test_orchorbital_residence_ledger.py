from dataclasses import replace

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import (
    AttractorFieldState,
    AttractorSpec,
    ORCHORBITALError,
    ORCHORBITALStep,
    propagate_orchorbital,
)
from src.idt.orchorbital_residence_ledger import (
    append_residence_steps,
    build_residence_receipts,
    dwell_time_statistics,
    read_residence_ledger,
    residence_episodes,
    transition_counts_from_receipts,
    verify_residence_receipts,
)


def _state(tau, x=1.0):
    return MemoryPhaseState(
        np.array([x, 0.0], dtype=float),
        np.array([0.0, 0.5], dtype=float),
        float(tau),
        0.0,
    )


def _synthetic_steps(labels, delta_taus):
    if len(labels) != len(delta_taus):
        raise ValueError("labels and delta_taus must have equal length")
    out = []
    current = _state(0.0)
    for index, (active, delta_tau) in enumerate(zip(labels, delta_taus)):
        next_active = labels[index + 1] if index + 1 < len(labels) else active
        after = MemoryPhaseState(
            current.position + np.array([0.01, 0.0], dtype=float),
            current.velocity.copy(),
            current.tau_internal + float(delta_tau),
            current.swept_area,
        )
        out.append(
            ORCHORBITALStep(
                state_before=current,
                state_after=after,
                field_before=AttractorFieldState((), active, False, 0.0, 1.0),
                field_after=AttractorFieldState((), next_active, False, 0.0, 1.0),
                active_attractor=active,
                winding_increment=0.01 * (index + 1),
                switched_after_segment=(next_active != active),
            )
        )
        current = after
    return out


def test_real_orchorbital_trajectory_builds_verified_deterministic_hash_chain():
    attractors = [
        AttractorSpec("A", np.array([0.0, 0.0], dtype=float), 1.0),
        AttractorSpec("B", np.array([5.0, 0.0], dtype=float), 0.8),
    ]
    steps = propagate_orchorbital(_state(0.0), attractors, [0.01, 0.02, 0.03])
    first = build_residence_receipts(steps)
    second = build_residence_receipts(steps)
    verify_residence_receipts(first)
    assert first == second
    assert [receipt.index for receipt in first] == [0, 1, 2]
    assert first[0].previous_receipt_sha256 is None
    assert first[1].previous_receipt_sha256 == first[0].receipt_sha256
    assert first[2].previous_receipt_sha256 == first[1].receipt_sha256


def test_receipt_content_tamper_breaks_hash_validation():
    receipts = list(build_residence_receipts(_synthetic_steps(["A", "A"], [0.1, 0.2])))
    receipts[1] = replace(receipts[1], delta_tau_hex=(99.0).hex())
    with pytest.raises(ORCHORBITALError, match="content hash mismatch"):
        verify_residence_receipts(receipts)


def test_append_only_ledger_preserves_prior_bytes_and_continues_hash_chain(tmp_path):
    steps = _synthetic_steps(["A", "A", "B", "B", "A"], [1.0, 1.0, 4.0, 1.0, 3.0])
    path = tmp_path / "residence.jsonl"

    first_append = append_residence_steps(path, steps[:2])
    prefix = path.read_bytes()
    second_append = append_residence_steps(path, steps[2:])

    assert path.read_bytes().startswith(prefix)
    persisted = read_residence_ledger(path)
    assert persisted[:2] == first_append
    assert persisted[2:] == second_append
    assert persisted[2].previous_receipt_sha256 == persisted[1].receipt_sha256


def test_append_rejects_state_discontinuity_without_mutating_existing_bytes(tmp_path):
    path = tmp_path / "residence.jsonl"
    steps = _synthetic_steps(["A", "A"], [0.1, 0.2])
    append_residence_steps(path, steps[:1])
    before = path.read_bytes()

    broken = replace(
        steps[1],
        state_before=MemoryPhaseState(
            np.array([99.0, 0.0], dtype=float),
            steps[1].state_before.velocity.copy(),
            steps[1].state_before.tau_internal,
            steps[1].state_before.swept_area,
        ),
    )
    with pytest.raises(ORCHORBITALError, match="discontinuous with ledger tail"):
        append_residence_steps(path, [broken])
    assert path.read_bytes() == before


def test_existing_empty_ledger_fails_loud_instead_of_becoming_a_new_seed(tmp_path):
    path = tmp_path / "residence.jsonl"
    path.write_bytes(b"")
    with pytest.raises(ORCHORBITALError, match="existing residence ledger is empty"):
        append_residence_steps(path, _synthetic_steps(["A"], [0.1]))
    assert path.read_bytes() == b""


def test_residence_episodes_and_dwell_statistics_use_contiguous_attractor_runs():
    receipts = build_residence_receipts(
        _synthetic_steps(["A", "A", "B", "B", "A"], [1.0, 1.0, 4.0, 1.0, 3.0])
    )
    episodes = residence_episodes(receipts)
    assert [(e.name, e.segments, e.dwell_tau) for e in episodes] == [
        ("A", 2, 2.0),
        ("B", 2, 5.0),
        ("A", 1, 3.0),
    ]

    stats = {item.name: item for item in dwell_time_statistics(receipts)}
    assert stats["A"].episodes == 2
    assert stats["A"].segments == 3
    assert stats["A"].total_dwell_tau == 5.0
    assert stats["A"].mean_dwell_tau == 2.5
    assert stats["A"].median_dwell_tau == 2.5
    assert stats["A"].min_dwell_tau == 2.0
    assert stats["A"].max_dwell_tau == 3.0
    assert stats["A"].variance_dwell_tau == 0.25
    assert stats["B"].episodes == 1
    assert stats["B"].total_dwell_tau == 5.0


def test_transition_counts_are_derived_from_persisted_residence_lineage():
    receipts = build_residence_receipts(
        _synthetic_steps(["A", "A", "B", "B", "A"], [0.1, 0.1, 0.1, 0.1, 0.1])
    )
    assert transition_counts_from_receipts(receipts) == {("A", "B"): 1, ("B", "A"): 1}


def test_post_segment_leak_is_persisted_as_terminal_switch_candidate():
    before = _state(0.0)
    after = _state(0.2, x=1.1)
    step = ORCHORBITALStep(
        state_before=before,
        state_after=after,
        field_before=AttractorFieldState((), "A", False, 0.0, 1.0),
        field_after=AttractorFieldState((), None, True, None, None),
        active_attractor="A",
        winding_increment=0.02,
        switched_after_segment=True,
    )
    receipt = build_residence_receipts([step])[0]
    assert receipt.active_attractor == "A"
    assert receipt.next_attractor is None
    assert receipt.post_segment_leak
    assert receipt.switched_after_segment
