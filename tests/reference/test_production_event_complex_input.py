import copy

import pytest

from idt.production_event_complex_input import (
    EventComplexInputError,
    incidence_sha256,
    reference_diamond,
    validate_input_dataset,
)


def test_reference_diamond_has_explicit_merger_and_exact_clock():
    data = reference_diamond(production=False)
    cert = validate_input_dataset(data)
    merger = next(item for item in data["event_classes"] if item["event_id"] == "d")
    assert merger["members"] == ["d_left", "d_right"]
    assert cert.input_valid
    assert cert.integrity_valid
    assert cert.quotient_valid
    assert cert.exact_clock_certified
    assert not cert.production_input
    assert not cert.promotion_eligible


def test_explicit_production_flag_is_required_for_promotion_eligibility():
    cert = validate_input_dataset(reference_diamond(production=True))
    assert cert.exact_clock_certified
    assert cert.production_input
    assert cert.promotion_eligible


def test_temporal_holonomy_is_retained_as_certificate_failure_not_parse_failure():
    data = reference_diamond(production=True)
    data["edges"][-1]["dtheta"] = 1.7
    data["incidence_sha256"] = incidence_sha256(
        data["occurrences"], data["event_classes"], data["edges"]
    )
    cert = validate_input_dataset(data)
    assert cert.input_valid
    assert cert.integrity_valid
    assert cert.quotient_valid
    assert not cert.exact_clock_certified
    assert not cert.promotion_eligible
    assert "temporal holonomy defect" in cert.temporal_receipt["reason"]


def test_digest_tampering_fails_closed():
    data = reference_diamond(production=False)
    data["edges"][0]["dtheta"] = 1.1
    with pytest.raises(EventComplexInputError, match="incidence_sha256 mismatch"):
        validate_input_dataset(data)


def test_occurrence_classes_must_form_a_partition():
    data = reference_diamond(production=False)
    data["event_classes"][1]["members"].append("c0")
    with pytest.raises(EventComplexInputError, match="more than one event class"):
        validate_input_dataset(data)


def test_unknown_event_endpoint_fails_closed():
    data = reference_diamond(production=False)
    data["edges"][0]["target_event"] = "missing"
    data["incidence_sha256"] = incidence_sha256(
        data["occurrences"], data["event_classes"], data["edges"]
    )
    with pytest.raises(EventComplexInputError, match="unknown event id"):
        validate_input_dataset(data)


def test_duplicate_relation_provenance_id_fails_closed():
    data = reference_diamond(production=False)
    data["edges"][1]["source_relation_id"] = data["edges"][0]["source_relation_id"]
    data["incidence_sha256"] = incidence_sha256(
        data["occurrences"], data["event_classes"], data["edges"]
    )
    with pytest.raises(EventComplexInputError, match="source_relation_id values must be unique"):
        validate_input_dataset(data)


def test_missing_provenance_fails_closed():
    data = copy.deepcopy(reference_diamond(production=False))
    data["provenance"]["source"] = ""
    with pytest.raises(EventComplexInputError, match="provenance.source"):
        validate_input_dataset(data)
