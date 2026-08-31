"""Freeze a source-owned realized event capture into the IDT GSC-2 input contract."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from .global_event_complex_input import (
    EventComplexInputCertificate,
    EventComplexInputError,
    build_input_dataset,
    validate_input_dataset,
)

CAPTURE_SCHEMA = "IDT_REALIZED_EVENT_COMPLEX_CAPTURE_V0_1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class EventComplexFreezeError(ValueError):
    """Raised when a realized-event source capture violates the freeze contract."""


@dataclass(frozen=True)
class FrozenEventComplex:
    dataset: dict[str, Any]
    certificate: EventComplexInputCertificate
    capture_sha256: str
    production_source_admitted: bool
    clock_id: str


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EventComplexFreezeError(f"{label} must be a non-empty string")
    return value.strip()


def _validate_source(source: Any) -> tuple[str, str, str, bool, str | None]:
    if not isinstance(source, Mapping):
        raise EventComplexFreezeError("source must be an object")
    source_id = _require_string(source.get("source_id"), "source.source_id")
    immutable_ref = _require_string(source.get("immutable_ref"), "source.immutable_ref")
    clock_id = _require_string(source.get("clock_id"), "source.clock_id")
    source_class = _require_string(source.get("source_class"), "source.source_class")
    if source_class not in {"PRODUCTION_SOURCE", "REFERENCE_CONTROL", "CANDIDATE_SOURCE"}:
        raise EventComplexFreezeError("unsupported source.source_class")

    receipt = source.get("capture_receipt_sha256")
    if receipt is not None:
        receipt = _require_string(receipt, "source.capture_receipt_sha256")
        if HEX64.fullmatch(receipt) is None:
            raise EventComplexFreezeError("source.capture_receipt_sha256 must be 64 lowercase hex characters")

    production = source_class == "PRODUCTION_SOURCE"
    if production and receipt is None:
        raise EventComplexFreezeError("PRODUCTION_SOURCE requires capture_receipt_sha256")
    return source_id, immutable_ref, clock_id, production, receipt


def freeze_event_capture(capture: Mapping[str, Any]) -> FrozenEventComplex:
    if not isinstance(capture, Mapping):
        raise EventComplexFreezeError("capture must be an object")
    if capture.get("schema") != CAPTURE_SCHEMA:
        raise EventComplexFreezeError(f"capture schema must equal {CAPTURE_SCHEMA}")

    capture_id = _require_string(capture.get("capture_id"), "capture_id")
    source_id, immutable_ref, clock_id, production, receipt = _validate_source(capture.get("source"))

    raw_events = capture.get("events")
    if not isinstance(raw_events, list) or len(raw_events) < 2:
        raise EventComplexFreezeError("events must contain at least two event records")
    events: list[str] = []
    seen_events: set[str] = set()
    for index, raw_event in enumerate(raw_events):
        if not isinstance(raw_event, Mapping):
            raise EventComplexFreezeError(f"events[{index}] must be an object")
        event_id = _require_string(raw_event.get("event_id"), f"events[{index}].event_id")
        if event_id in seen_events:
            raise EventComplexFreezeError(f"duplicate event_id: {event_id}")
        seen_events.add(event_id)
        events.append(event_id)

    raw_edges = capture.get("elapsed_edges")
    if not isinstance(raw_edges, list) or not raw_edges:
        raise EventComplexFreezeError("elapsed_edges must be a non-empty list")
    edges: list[dict[str, Any]] = []
    seen_edges: set[str] = set()
    for index, raw_edge in enumerate(raw_edges):
        if not isinstance(raw_edge, Mapping):
            raise EventComplexFreezeError(f"elapsed_edges[{index}] must be an object")
        edge_id = _require_string(raw_edge.get("edge_id"), f"elapsed_edges[{index}].edge_id")
        if edge_id in seen_edges:
            raise EventComplexFreezeError(f"duplicate edge_id: {edge_id}")
        seen_edges.add(edge_id)
        source = _require_string(raw_edge.get("source"), f"elapsed_edges[{index}].source")
        target = _require_string(raw_edge.get("target"), f"elapsed_edges[{index}].target")
        try:
            dtheta = float(raw_edge.get("dtheta"))
        except (TypeError, ValueError) as exc:
            raise EventComplexFreezeError(f"elapsed_edges[{index}].dtheta must be numeric") from exc
        edges.append({"edge_id": edge_id, "source": source, "target": target, "dtheta": dtheta})

    canonical_capture = {
        "schema": CAPTURE_SCHEMA,
        "capture_id": capture_id,
        "source": dict(capture["source"]),
        "events": [{"event_id": event_id} for event_id in sorted(events)],
        "elapsed_edges": sorted(
            edges,
            key=lambda edge: (edge["edge_id"], edge["source"], edge["target"], format(edge["dtheta"], ".17g")),
        ),
    }
    capture_sha = _sha256(canonical_capture)

    dataset = build_input_dataset(
        dataset_id=capture_id,
        vertices=sorted(events),
        edges=edges,
        source=source_id,
        source_commit_or_digest=immutable_ref,
        production=production,
    )
    dataset["provenance"]["source_class"] = capture["source"]["source_class"]
    dataset["provenance"]["clock_id"] = clock_id
    dataset["provenance"]["capture_sha256"] = capture_sha
    if receipt is not None:
        dataset["provenance"]["capture_receipt_sha256"] = receipt

    try:
        certificate = validate_input_dataset(dataset)
    except EventComplexInputError as exc:
        raise EventComplexFreezeError(str(exc)) from exc

    return FrozenEventComplex(
        dataset=dataset,
        certificate=certificate,
        capture_sha256=capture_sha,
        production_source_admitted=production,
        clock_id=clock_id,
    )
