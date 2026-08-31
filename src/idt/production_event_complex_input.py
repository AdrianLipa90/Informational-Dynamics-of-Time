"""Fail-closed 05J contract for a supplied production event complex."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any

from .global_event_clock_exactness import EventEdge, TemporalExactnessError, certify_event_clock

SCHEMA = "IDT_PRODUCTION_EVENT_COMPLEX_INPUT_V0_1"


class EventComplexInputError(ValueError):
    """Raised when the supplied 05J dataset violates the input contract."""


@dataclass(frozen=True)
class EventComplexInputCertificate:
    input_valid: bool
    integrity_valid: bool
    quotient_valid: bool
    exact_clock_certified: bool
    production_input: bool
    promotion_eligible: bool
    dataset_id: str
    incidence_sha256: str
    event_count: int
    occurrence_count: int
    edge_count: int
    temporal_receipt: dict[str, Any]


def _require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EventComplexInputError(f"{name} must be a non-empty string")
    return value.strip()


def _canonical_payload(occurrences, event_classes, edges):
    classes = sorted(
        [
            {
                "event_id": item["event_id"],
                "members": sorted(item["members"]),
            }
            for item in event_classes
        ],
        key=lambda item: item["event_id"],
    )
    canonical_edges = sorted(
        [
            {
                "source_event": edge["source_event"],
                "target_event": edge["target_event"],
                "dtheta": float(edge["dtheta"]),
                "source_relation_id": edge["source_relation_id"],
            }
            for edge in edges
        ],
        key=lambda edge: (
            edge["source_event"],
            edge["target_event"],
            edge["source_relation_id"],
            edge["dtheta"],
        ),
    )
    return {
        "occurrences": sorted(occurrences),
        "event_classes": classes,
        "edges": canonical_edges,
    }


def incidence_sha256(occurrences, event_classes, edges):
    payload = _canonical_payload(occurrences, event_classes, edges)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_input_dataset(*, dataset_id, occurrences, event_classes, edges, source, source_commit_or_digest, production):
    return {
        "schema": SCHEMA,
        "dataset_id": dataset_id,
        "production": bool(production),
        "provenance": {
            "source": source,
            "source_commit_or_digest": source_commit_or_digest,
        },
        "occurrences": list(occurrences),
        "event_classes": [dict(item) for item in event_classes],
        "edges": [dict(edge) for edge in edges],
        "incidence_sha256": incidence_sha256(occurrences, event_classes, edges),
    }


def validate_input_dataset(data):
    if not isinstance(data, dict):
        raise EventComplexInputError("dataset must be a JSON object")
    if data.get("schema") != SCHEMA:
        raise EventComplexInputError(f"schema must equal {SCHEMA}")
    dataset_id = _require_nonempty_string(data.get("dataset_id"), "dataset_id")
    if type(data.get("production")) is not bool:
        raise EventComplexInputError("production must be a boolean")

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise EventComplexInputError("provenance must be an object")
    _require_nonempty_string(provenance.get("source"), "provenance.source")
    _require_nonempty_string(
        provenance.get("source_commit_or_digest"),
        "provenance.source_commit_or_digest",
    )

    raw_occurrences = data.get("occurrences")
    if not isinstance(raw_occurrences, list) or not raw_occurrences:
        raise EventComplexInputError("occurrences must be a non-empty list")
    occurrences = [_require_nonempty_string(item, "occurrence id") for item in raw_occurrences]
    if len(set(occurrences)) != len(occurrences):
        raise EventComplexInputError("occurrence ids must be unique")
    occurrence_set = set(occurrences)

    raw_classes = data.get("event_classes")
    if not isinstance(raw_classes, list) or not raw_classes:
        raise EventComplexInputError("event_classes must be a non-empty list")
    event_ids = []
    assigned_members = []
    normalized_classes = []
    for index, item in enumerate(raw_classes):
        if not isinstance(item, dict):
            raise EventComplexInputError(f"event class {index} must be an object")
        event_id = _require_nonempty_string(item.get("event_id"), f"event class {index} event_id")
        members = item.get("members")
        if not isinstance(members, list) or not members:
            raise EventComplexInputError(f"event class {event_id} must have non-empty members")
        normalized_members = [_require_nonempty_string(m, f"event class {event_id} member") for m in members]
        if len(set(normalized_members)) != len(normalized_members):
            raise EventComplexInputError(f"event class {event_id} repeats an occurrence")
        unknown = set(normalized_members) - occurrence_set
        if unknown:
            raise EventComplexInputError(f"event class {event_id} contains unknown occurrences: {sorted(unknown)}")
        event_ids.append(event_id)
        assigned_members.extend(normalized_members)
        normalized_classes.append({"event_id": event_id, "members": normalized_members})

    if len(set(event_ids)) != len(event_ids):
        raise EventComplexInputError("event ids must be unique")
    if len(set(assigned_members)) != len(assigned_members):
        raise EventComplexInputError("an occurrence belongs to more than one event class")
    if set(assigned_members) != occurrence_set:
        missing = occurrence_set - set(assigned_members)
        raise EventComplexInputError(f"event classes do not partition all occurrences: missing={sorted(missing)}")
    event_set = set(event_ids)

    raw_edges = data.get("edges")
    if not isinstance(raw_edges, list) or not raw_edges:
        raise EventComplexInputError("edges must be a non-empty list")
    normalized_edges = []
    relation_ids = []
    event_edges = []
    for index, edge in enumerate(raw_edges):
        if not isinstance(edge, dict):
            raise EventComplexInputError(f"edge {index} must be an object")
        source = _require_nonempty_string(edge.get("source_event"), f"edge {index} source_event")
        target = _require_nonempty_string(edge.get("target_event"), f"edge {index} target_event")
        relation_id = _require_nonempty_string(edge.get("source_relation_id"), f"edge {index} source_relation_id")
        if source not in event_set or target not in event_set:
            raise EventComplexInputError(f"edge {index} references an unknown event id")
        try:
            dtheta = float(edge.get("dtheta"))
        except (TypeError, ValueError) as exc:
            raise EventComplexInputError(f"edge {index} dtheta must be numeric") from exc
        if not isfinite(dtheta) or dtheta <= 0.0:
            raise EventComplexInputError(f"edge {index} dtheta must be finite and positive")
        relation_ids.append(relation_id)
        normalized = {
            "source_event": source,
            "target_event": target,
            "dtheta": dtheta,
            "source_relation_id": relation_id,
        }
        normalized_edges.append(normalized)
        try:
            event_edges.append(EventEdge(source, target, dtheta))
        except TemporalExactnessError as exc:
            raise EventComplexInputError(f"edge {index} violates EventEdge contract: {exc}") from exc

    if len(set(relation_ids)) != len(relation_ids):
        raise EventComplexInputError("source_relation_id values must be unique")

    supplied_digest = _require_nonempty_string(data.get("incidence_sha256"), "incidence_sha256")
    computed_digest = incidence_sha256(occurrences, normalized_classes, normalized_edges)
    if supplied_digest != computed_digest:
        raise EventComplexInputError(
            f"incidence_sha256 mismatch: supplied={supplied_digest}, computed={computed_digest}"
        )

    try:
        exactness = certify_event_clock(event_edges, vertices=event_ids, require_connected=True)
        exact_ok = bool(exactness.exact)
        temporal_receipt = asdict(exactness)
    except TemporalExactnessError as exc:
        exact_ok = False
        temporal_receipt = {"exact": False, "reason": str(exc)}

    production = data["production"]
    return EventComplexInputCertificate(
        input_valid=True,
        integrity_valid=True,
        quotient_valid=True,
        exact_clock_certified=exact_ok,
        production_input=production,
        promotion_eligible=bool(production and exact_ok),
        dataset_id=dataset_id,
        incidence_sha256=computed_digest,
        event_count=len(event_ids),
        occurrence_count=len(occurrences),
        edge_count=len(event_edges),
        temporal_receipt=temporal_receipt,
    )


def reference_diamond(*, production=False):
    occurrences = ["a0", "b0", "c0", "d_left", "d_right"]
    event_classes = [
        {"event_id": "a", "members": ["a0"]},
        {"event_id": "b", "members": ["b0"]},
        {"event_id": "c", "members": ["c0"]},
        {"event_id": "d", "members": ["d_left", "d_right"]},
    ]
    edges = [
        {"source_event": "a", "target_event": "b", "dtheta": 1.0, "source_relation_id": "r_ab"},
        {"source_event": "b", "target_event": "d", "dtheta": 2.0, "source_relation_id": "r_bd"},
        {"source_event": "a", "target_event": "c", "dtheta": 1.5, "source_relation_id": "r_ac"},
        {"source_event": "c", "target_event": "d", "dtheta": 1.5, "source_relation_id": "r_cd"},
    ]
    return build_input_dataset(
        dataset_id="reference-exact-diamond-with-explicit-merger",
        occurrences=occurrences,
        event_classes=event_classes,
        edges=edges,
        source="IDT 05J reference control only",
        source_commit_or_digest="REFERENCE_CONTROL_NOT_PRODUCTION",
        production=production,
    )
