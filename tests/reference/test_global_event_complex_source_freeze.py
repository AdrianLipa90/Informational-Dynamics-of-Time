from copy import deepcopy

import pytest

from src.idt.global_event_complex_source_freeze import (
    CAPTURE_SCHEMA,
    EventComplexFreezeError,
    freeze_event_capture,
)


RECEIPT = "a" * 64


def capture(*, exact=True, source_class="REFERENCE_CONTROL", receipt=None, reverse=False):
    direct = 3.0 if exact else 4.0
    events = [{"event_id": "a"}, {"event_id": "b"}, {"event_id": "c"}]
    edges = [
        {"edge_id": "ab", "source": "a", "target": "b", "dtheta": 1.0},
        {"edge_id": "bc", "source": "b", "target": "c", "dtheta": 2.0},
        {"edge_id": "ac", "source": "a", "target": "c", "dtheta": direct},
    ]
    if reverse:
        events = list(reversed(events))
        edges = list(reversed(edges))
    source = {
        "source_id": "UNIT_TEST_REALIZED_EVENT_STREAM",
        "source_class": source_class,
        "immutable_ref": "unit-test-event-capture-v1",
        "clock_id": "clock-unit-test-1",
    }
    if receipt is not None:
        source["capture_receipt_sha256"] = receipt
    return {
        "schema": CAPTURE_SCHEMA,
        "capture_id": "unit-test-event-complex",
        "source": source,
        "events": events,
        "elapsed_edges": edges,
    }


def test_reference_capture_freezes_and_05h_exactness_passes_without_promotion():
    frozen = freeze_event_capture(capture())
    assert frozen.certificate.input_valid
    assert frozen.certificate.integrity_valid
    assert frozen.certificate.exact_clock_certified
    assert not frozen.production_source_admitted
    assert not frozen.certificate.promotion_eligible
    assert frozen.dataset["provenance"]["clock_id"] == "clock-unit-test-1"


def test_freeze_is_order_invariant():
    normal = freeze_event_capture(capture())
    reversed_capture = freeze_event_capture(capture(reverse=True))
    assert normal.capture_sha256 == reversed_capture.capture_sha256
    assert normal.dataset["incidence_sha256"] == reversed_capture.dataset["incidence_sha256"]


def test_structurally_valid_temporal_holonomy_defect_remains_exactness_failure():
    frozen = freeze_event_capture(capture(exact=False))
    assert frozen.certificate.input_valid
    assert frozen.certificate.integrity_valid
    assert not frozen.certificate.exact_clock_certified
    assert frozen.certificate.exactness_failure is not None
    assert not frozen.certificate.promotion_eligible


def test_production_source_requires_capture_receipt():
    with pytest.raises(EventComplexFreezeError):
        freeze_event_capture(capture(source_class="PRODUCTION_SOURCE"))


def test_production_source_rejects_malformed_receipt():
    with pytest.raises(EventComplexFreezeError):
        freeze_event_capture(capture(source_class="PRODUCTION_SOURCE", receipt="bad"))


def test_in_memory_production_path_still_requires_05h_exactness():
    exact = freeze_event_capture(
        capture(source_class="PRODUCTION_SOURCE", receipt=RECEIPT, exact=True)
    )
    defect = freeze_event_capture(
        capture(source_class="PRODUCTION_SOURCE", receipt=RECEIPT, exact=False)
    )
    assert exact.production_source_admitted
    assert exact.certificate.promotion_eligible
    assert defect.production_source_admitted
    assert not defect.certificate.promotion_eligible


def test_duplicate_event_id_is_rejected():
    data = capture()
    data["events"][2]["event_id"] = "a"
    with pytest.raises(EventComplexFreezeError):
        freeze_event_capture(data)


def test_duplicate_edge_id_is_rejected():
    data = capture()
    data["elapsed_edges"][2]["edge_id"] = "ab"
    with pytest.raises(EventComplexFreezeError):
        freeze_event_capture(data)


def test_undeclared_event_reference_is_rejected_by_gsc2_input_contract():
    data = capture()
    data["elapsed_edges"][0]["source"] = "missing"
    with pytest.raises(EventComplexFreezeError):
        freeze_event_capture(data)


def test_capture_sha_changes_when_clock_lineage_changes():
    first = freeze_event_capture(capture())
    second_data = deepcopy(capture())
    second_data["source"]["clock_id"] = "clock-unit-test-2"
    second = freeze_event_capture(second_data)
    assert first.capture_sha256 != second.capture_sha256
    assert first.dataset["incidence_sha256"] == second.dataset["incidence_sha256"]
