import pytest

from src.idt.occurrence_terminal_state_input import (
    OccurrenceTerminalStateInputError,
    build_input_dataset,
    certify_input_dataset,
    reference_recurrent_state_table,
)

DIGEST = "evt-digest"


def test_recurrent_state_labels_are_legal_across_distinct_prefix_occurrences():
    data = reference_recurrent_state_table(event_complex_incidence_sha256=DIGEST)
    cert = certify_input_dataset(
        data,
        expected_occurrence_ids=["a0", "b0", "a2"],
        expected_event_complex_incidence_sha256=DIGEST,
    )
    assert cert.repeated_terminal_state_count == 1
    assert cert.occurrence_to_terminal_state["a0"] == "A"
    assert cert.occurrence_to_terminal_state["a2"] == "A"
    assert cert.production_input is False
    assert cert.canon_allowed is False


def test_missing_occurrence_fails_closed():
    data = reference_recurrent_state_table(event_complex_incidence_sha256=DIGEST)
    with pytest.raises(OccurrenceTerminalStateInputError, match="coverage mismatch"):
        certify_input_dataset(
            data,
            expected_occurrence_ids=["a0", "b0", "a2", "c0"],
            expected_event_complex_incidence_sha256=DIGEST,
        )


def test_event_complex_digest_mismatch_fails_closed():
    data = reference_recurrent_state_table(event_complex_incidence_sha256=DIGEST)
    with pytest.raises(OccurrenceTerminalStateInputError, match="incidence digest mismatch"):
        certify_input_dataset(
            data,
            expected_occurrence_ids=["a0", "b0", "a2"],
            expected_event_complex_incidence_sha256="other",
        )


def test_duplicate_prefix_identity_fails_closed():
    rows = [
        {"occurrence_id": "o1", "prefix_id_or_digest": "P", "terminal_state_id": "A"},
        {"occurrence_id": "o2", "prefix_id_or_digest": "P", "terminal_state_id": "A"},
    ]
    data = build_input_dataset(
        dataset_id="x",
        rows=rows,
        source="s",
        source_commit_or_digest="c",
        event_complex_incidence_sha256=DIGEST,
        production=False,
    )
    with pytest.raises(
        OccurrenceTerminalStateInputError,
        match="prefix_id_or_digest values must be unique",
    ):
        certify_input_dataset(
            data,
            expected_occurrence_ids=["o1", "o2"],
            expected_event_complex_incidence_sha256=DIGEST,
        )


def test_table_digest_tampering_fails_closed():
    data = reference_recurrent_state_table(event_complex_incidence_sha256=DIGEST)
    data["rows"][0]["terminal_state_id"] = "Z"
    with pytest.raises(OccurrenceTerminalStateInputError, match="table_sha256 mismatch"):
        certify_input_dataset(
            data,
            expected_occurrence_ids=["a0", "b0", "a2"],
            expected_event_complex_incidence_sha256=DIGEST,
        )


def test_production_flag_only_makes_contract_review_eligible_not_canonical():
    data = reference_recurrent_state_table(
        event_complex_incidence_sha256=DIGEST,
        production=True,
    )
    cert = certify_input_dataset(
        data,
        expected_occurrence_ids=["a0", "b0", "a2"],
        expected_event_complex_incidence_sha256=DIGEST,
    )
    assert cert.promotion_review_eligible is True
    assert cert.canon_allowed is False
