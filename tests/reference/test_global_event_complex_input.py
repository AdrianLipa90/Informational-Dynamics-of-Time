import copy

import pytest

from idt.global_event_complex_input import (
    EventComplexInputError,
    incidence_sha256,
    minimal_cycle_reference_dataset,
    validate_input_dataset,
    validation_receipt,
)


def test_minimal_three_event_cycle_exactness_passes_without_reference_promotion():
    data = minimal_cycle_reference_dataset(exact=True, production=False)
    cert = validate_input_dataset(data)
    assert cert.input_valid is True
    assert cert.integrity_valid is True
    assert cert.exact_clock_certified is True
    assert cert.production_input is False
    assert cert.promotion_eligible is False
    assert cert.event_count == 3
    assert cert.edge_count == 3
    assert cert.event_potentials == pytest.approx({"a": 0.0, "b": 1.0, "c": 3.0})
    assert cert.max_residual == pytest.approx(0.0)


def test_same_minimal_incidence_with_wrong_direct_elapsed_edge_reports_holonomy():
    data = minimal_cycle_reference_dataset(exact=False, production=False)
    cert = validate_input_dataset(data)
    assert cert.input_valid is True
    assert cert.integrity_valid is True
    assert cert.exact_clock_certified is False
    assert cert.promotion_eligible is False
    assert cert.event_potentials == {}
    assert cert.exactness_failure is not None
    assert "temporal holonomy defect" in cert.exactness_failure


def test_integrity_digest_tamper_fails_before_exactness():
    data = minimal_cycle_reference_dataset(exact=True, production=False)
    data["edges"][0]["dtheta"] = 9.0
    with pytest.raises(EventComplexInputError, match="incidence_sha256 mismatch"):
        validate_input_dataset(data)


def test_duplicate_edge_ids_fail_input_contract():
    data = minimal_cycle_reference_dataset(exact=True, production=False)
    data["edges"][1]["edge_id"] = data["edges"][0]["edge_id"]
    data["incidence_sha256"] = incidence_sha256(data["vertices"], data["edges"])
    with pytest.raises(EventComplexInputError, match="duplicate edge_id"):
        validate_input_dataset(data)


def test_undeclared_event_reference_fails_input_contract():
    data = minimal_cycle_reference_dataset(exact=True, production=False)
    data["edges"][0]["target"] = "missing"
    data["incidence_sha256"] = incidence_sha256(data["vertices"], data["edges"])
    with pytest.raises(EventComplexInputError, match="undeclared events"):
        validate_input_dataset(data)


def test_exact_production_flag_is_required_for_promotion_eligibility():
    data = minimal_cycle_reference_dataset(exact=True, production=True)
    cert = validate_input_dataset(data)
    assert cert.production_input is True
    assert cert.exact_clock_certified is True
    assert cert.promotion_eligible is True


def test_validation_receipt_keeps_production_input_open():
    receipt = validation_receipt()
    assert receipt["technical_status"] == "PASS"
    assert receipt["production_event_complex"] == "OPEN_INPUT"
    assert receipt["minimal_nontrivial_cycle_witness"] == {
        "vertices": 3,
        "edges": 3,
        "condition": "theta_ab + theta_bc = theta_ac",
    }
