from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "IDT_OCCURRENCE_TERMINAL_STATE_INPUT_V0_1"


class OccurrenceTerminalStateInputError(ValueError):
    """Raised when a supplied 00F occurrence/state witness violates the contract."""


@dataclass(frozen=True)
class OccurrenceTerminalStateCertificate:
    input_valid: bool
    integrity_valid: bool
    occurrence_coverage_valid: bool
    event_complex_binding_valid: bool
    production_input: bool
    promotion_review_eligible: bool
    canon_allowed: bool
    dataset_id: str
    table_sha256: str
    event_complex_incidence_sha256: str
    occurrence_count: int
    distinct_terminal_state_count: int
    repeated_terminal_state_count: int
    occurrence_to_terminal_state: dict[str, str]


def _id(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OccurrenceTerminalStateInputError(f"{name} must be a non-empty string")
    return value.strip()


def _normalized_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise OccurrenceTerminalStateInputError(f"row {index} must be an object")
        out.append({
            "occurrence_id": _id(row.get("occurrence_id"), f"row {index} occurrence_id"),
            "prefix_id_or_digest": _id(row.get("prefix_id_or_digest"), f"row {index} prefix_id_or_digest"),
            "terminal_state_id": _id(row.get("terminal_state_id"), f"row {index} terminal_state_id"),
        })
    if not out:
        raise OccurrenceTerminalStateInputError("rows must be non-empty")
    return out


def table_sha256(rows: Sequence[Mapping[str, Any]]) -> str:
    normalized = _normalized_rows(rows)
    payload = sorted(
        normalized,
        key=lambda row: (row["occurrence_id"], row["prefix_id_or_digest"], row["terminal_state_id"]),
    )
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_input_dataset(
    *,
    dataset_id: str,
    rows: Sequence[Mapping[str, Any]],
    source: str,
    source_commit_or_digest: str,
    event_complex_incidence_sha256: str,
    production: bool,
) -> dict[str, Any]:
    normalized = _normalized_rows(rows)
    return {
        "schema": SCHEMA,
        "dataset_id": _id(dataset_id, "dataset_id"),
        "production": bool(production),
        "provenance": {
            "source": _id(source, "provenance.source"),
            "source_commit_or_digest": _id(
                source_commit_or_digest,
                "provenance.source_commit_or_digest",
            ),
            "event_complex_incidence_sha256": _id(
                event_complex_incidence_sha256,
                "provenance.event_complex_incidence_sha256",
            ),
        },
        "rows": normalized,
        "table_sha256": table_sha256(normalized),
    }


def certify_input_dataset(
    data: Mapping[str, Any],
    *,
    expected_occurrence_ids: Iterable[str],
    expected_event_complex_incidence_sha256: str,
) -> OccurrenceTerminalStateCertificate:
    if not isinstance(data, Mapping):
        raise OccurrenceTerminalStateInputError("dataset must be an object")
    if data.get("schema") != SCHEMA:
        raise OccurrenceTerminalStateInputError(f"schema must equal {SCHEMA}")
    dataset_id = _id(data.get("dataset_id"), "dataset_id")
    if type(data.get("production")) is not bool:
        raise OccurrenceTerminalStateInputError("production must be a boolean")

    provenance = data.get("provenance")
    if not isinstance(provenance, Mapping):
        raise OccurrenceTerminalStateInputError("provenance must be an object")
    _id(provenance.get("source"), "provenance.source")
    _id(provenance.get("source_commit_or_digest"), "provenance.source_commit_or_digest")
    bound_event_digest = _id(
        provenance.get("event_complex_incidence_sha256"),
        "provenance.event_complex_incidence_sha256",
    )
    expected_digest = _id(
        expected_event_complex_incidence_sha256,
        "expected_event_complex_incidence_sha256",
    )
    if bound_event_digest != expected_digest:
        raise OccurrenceTerminalStateInputError("event-complex incidence digest mismatch")

    raw_rows = data.get("rows")
    if not isinstance(raw_rows, list):
        raise OccurrenceTerminalStateInputError("rows must be a list")
    rows = _normalized_rows(raw_rows)
    occurrence_ids = [row["occurrence_id"] for row in rows]
    prefix_ids = [row["prefix_id_or_digest"] for row in rows]
    if len(set(occurrence_ids)) != len(occurrence_ids):
        raise OccurrenceTerminalStateInputError("occurrence_id values must be unique")
    if len(set(prefix_ids)) != len(prefix_ids):
        raise OccurrenceTerminalStateInputError("prefix_id_or_digest values must be unique")

    expected = tuple(_id(item, "expected occurrence id") for item in expected_occurrence_ids)
    if not expected or len(set(expected)) != len(expected):
        raise OccurrenceTerminalStateInputError(
            "expected_occurrence_ids must be non-empty and unique"
        )
    if set(occurrence_ids) != set(expected):
        missing = sorted(set(expected) - set(occurrence_ids))
        extra = sorted(set(occurrence_ids) - set(expected))
        raise OccurrenceTerminalStateInputError(
            f"occurrence coverage mismatch: missing={missing}, extra={extra}"
        )

    supplied_table_digest = _id(data.get("table_sha256"), "table_sha256")
    computed = table_sha256(rows)
    if supplied_table_digest != computed:
        raise OccurrenceTerminalStateInputError("table_sha256 mismatch")

    mapping = dict(
        sorted((row["occurrence_id"], row["terminal_state_id"]) for row in rows)
    )
    counts: dict[str, int] = {}
    for state in mapping.values():
        counts[state] = counts.get(state, 0) + 1
    repeated = sum(1 for count in counts.values() if count > 1)
    production = bool(data["production"])

    return OccurrenceTerminalStateCertificate(
        input_valid=True,
        integrity_valid=True,
        occurrence_coverage_valid=True,
        event_complex_binding_valid=True,
        production_input=production,
        promotion_review_eligible=production,
        canon_allowed=False,
        dataset_id=dataset_id,
        table_sha256=computed,
        event_complex_incidence_sha256=bound_event_digest,
        occurrence_count=len(rows),
        distinct_terminal_state_count=len(counts),
        repeated_terminal_state_count=repeated,
        occurrence_to_terminal_state=mapping,
    )


def reference_recurrent_state_table(
    *, event_complex_incidence_sha256: str, production: bool = False
) -> dict[str, Any]:
    rows = [
        {"occurrence_id": "a0", "prefix_id_or_digest": "P0", "terminal_state_id": "A"},
        {"occurrence_id": "b0", "prefix_id_or_digest": "P1", "terminal_state_id": "B"},
        {"occurrence_id": "a2", "prefix_id_or_digest": "P2", "terminal_state_id": "A"},
    ]
    return build_input_dataset(
        dataset_id="reference-recurrent-state-control",
        rows=rows,
        source="IDT 00G reference control only",
        source_commit_or_digest="REFERENCE_CONTROL_NOT_PRODUCTION",
        event_complex_incidence_sha256=event_complex_incidence_sha256,
        production=production,
    )
