"""Fail-closed source-owned input contract for IDT GSC-2.

The contract validates provenance and canonical event incidence first, then hands the
realized event graph to the existing 05H exactness certifier.  Structural/integrity
failure is distinguished from a valid dataset whose elapsed one-cochain carries a
temporal-holonomy defect.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any, Mapping, Sequence

from .global_event_clock_exactness import (
    EventEdge,
    TemporalExactnessError,
    certify_event_clock,
)

SCHEMA = "IDT_GLOBAL_EVENT_COMPLEX_INPUT_V0_1"


class EventComplexInputError(ValueError):
    """Raised when a supplied event-complex dataset violates the input contract."""


@dataclass(frozen=True)
class EventComplexInputCertificate:
    input_valid: bool
    integrity_valid: bool
    exact_clock_certified: bool
    production_input: bool
    promotion_eligible: bool
    dataset_id: str
    incidence_sha256: str
    event_count: int
    edge_count: int
    event_potentials: dict[str, float]
    max_residual: float | None
    exactness_failure: str | None


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EventComplexInputError(f"{label} must be a non-empty string")
    return value.strip()


def _finite_positive(value: Any, label: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise EventComplexInputError(f"{label} must be a finite positive number") from exc
    if not isfinite(out) or out <= 0.0:
        raise EventComplexInputError(f"{label} must be a finite positive number")
    return out


def _canonical_edge(edge: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "edge_id": str(edge["edge_id"]),
        "source": str(edge["source"]),
        "target": str(edge["target"]),
        "dtheta": format(float(edge["dtheta"]), ".17g"),
    }


def canonical_incidence_payload(vertices: Sequence[str], edges: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "vertices": sorted(vertices),
        "edges": sorted(
            (_canonical_edge(edge) for edge in edges),
            key=lambda item: (item["edge_id"], item["source"], item["target"], item["dtheta"]),
        ),
    }


def incidence_sha256(vertices: Sequence[str], edges: Sequence[Mapping[str, Any]]) -> str:
    payload = canonical_incidence_payload(vertices, edges)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_input_dataset(
    *,
    dataset_id: str,
    vertices: Sequence[str],
    edges: Sequence[Mapping[str, Any]],
    source: str,
    source_commit_or_digest: str,
    production: bool,
) -> dict[str, Any]:
    normalized_edges = [
        {
            "edge_id": str(edge["edge_id"]),
            "source": str(edge["source"]),
            "target": str(edge["target"]),
            "dtheta": float(edge["dtheta"]),
        }
        for edge in edges
    ]
    return {
        "schema": SCHEMA,
        "dataset_id": dataset_id,
        "representation": "connected_directed_event_complex_with_elapsed_edges",
        "production": bool(production),
        "provenance": {
            "source": source,
            "source_commit_or_digest": source_commit_or_digest,
        },
        "vertices": list(vertices),
        "edges": normalized_edges,
        "incidence_sha256": incidence_sha256(vertices, normalized_edges),
    }


def validate_input_dataset(data: Mapping[str, Any]) -> EventComplexInputCertificate:
    if not isinstance(data, Mapping):
        raise EventComplexInputError("dataset must be a JSON object")
    if data.get("schema") != SCHEMA:
        raise EventComplexInputError(f"schema must equal {SCHEMA}")
    dataset_id = _require_nonempty_string(data.get("dataset_id"), "dataset_id")
    if data.get("representation") != "connected_directed_event_complex_with_elapsed_edges":
        raise EventComplexInputError("unexpected event-complex representation")
    if type(data.get("production")) is not bool:
        raise EventComplexInputError("production must be a boolean")

    provenance = data.get("provenance")
    if not isinstance(provenance, Mapping):
        raise EventComplexInputError("provenance must be an object")
    _require_nonempty_string(provenance.get("source"), "provenance.source")
    _require_nonempty_string(
        provenance.get("source_commit_or_digest"),
        "provenance.source_commit_or_digest",
    )

    raw_vertices = data.get("vertices")
    if not isinstance(raw_vertices, list) or len(raw_vertices) < 2:
        raise EventComplexInputError("vertices must contain at least two event ids")
    vertices = [_require_nonempty_string(value, "event id") for value in raw_vertices]
    if len(set(vertices)) != len(vertices):
        raise EventComplexInputError("event ids must be unique")
    vertex_set = set(vertices)

    raw_edges = data.get("edges")
    if not isinstance(raw_edges, list) or not raw_edges:
        raise EventComplexInputError("edges must be a non-empty list")

    normalized_edges: list[dict[str, Any]] = []
    edge_ids: set[str] = set()
    event_edges: list[EventEdge] = []
    used_vertices: set[str] = set()
    for index, raw_edge in enumerate(raw_edges):
        if not isinstance(raw_edge, Mapping):
            raise EventComplexInputError(f"edge {index} must be an object")
        edge_id = _require_nonempty_string(raw_edge.get("edge_id"), f"edge {index}.edge_id")
        if edge_id in edge_ids:
            raise EventComplexInputError(f"duplicate edge_id {edge_id!r}")
        edge_ids.add(edge_id)
        source = _require_nonempty_string(raw_edge.get("source"), f"edge {index}.source")
        target = _require_nonempty_string(raw_edge.get("target"), f"edge {index}.target")
        missing = {source, target} - vertex_set
        if missing:
            raise EventComplexInputError(
                f"edge {edge_id!r} references undeclared events: {sorted(missing)}"
            )
        dtheta = _finite_positive(raw_edge.get("dtheta"), f"edge {edge_id!r}.dtheta")
        try:
            event_edge = EventEdge(source, target, dtheta)
        except TemporalExactnessError as exc:
            raise EventComplexInputError(f"edge {edge_id!r} violates 05H edge typing: {exc}") from exc
        normalized_edges.append(
            {"edge_id": edge_id, "source": source, "target": target, "dtheta": dtheta}
        )
        event_edges.append(event_edge)
        used_vertices.update((source, target))

    unused = vertex_set - used_vertices
    if unused:
        raise EventComplexInputError(f"declared events are isolated/unused: {sorted(unused)}")

    supplied_digest = _require_nonempty_string(data.get("incidence_sha256"), "incidence_sha256")
    computed_digest = incidence_sha256(vertices, normalized_edges)
    if supplied_digest != computed_digest:
        raise EventComplexInputError(
            f"incidence_sha256 mismatch: supplied={supplied_digest}, computed={computed_digest}"
        )

    exact = False
    potentials: dict[str, float] = {}
    residual: float | None = None
    exactness_failure: str | None = None
    try:
        exactness = certify_event_clock(event_edges, vertices=vertices, require_connected=True)
        exact = bool(exactness.exact)
        potentials = exactness.potentials
        residual = exactness.max_residual
    except TemporalExactnessError as exc:
        exactness_failure = str(exc)

    production = bool(data["production"])
    return EventComplexInputCertificate(
        input_valid=True,
        integrity_valid=True,
        exact_clock_certified=exact,
        production_input=production,
        promotion_eligible=bool(production and exact),
        dataset_id=dataset_id,
        incidence_sha256=computed_digest,
        event_count=len(vertices),
        edge_count=len(normalized_edges),
        event_potentials=dict(sorted(potentials.items())),
        max_residual=residual,
        exactness_failure=exactness_failure,
    )


def minimal_cycle_reference_dataset(*, exact: bool = True, production: bool = False) -> dict[str, Any]:
    """Three-event acyclic orientation of the smallest nontrivial undirected cycle."""
    direct = 3.0 if exact else 4.0
    return build_input_dataset(
        dataset_id="reference-minimal-cycle-exact" if exact else "reference-minimal-cycle-defect",
        vertices=["a", "b", "c"],
        edges=[
            {"edge_id": "ab", "source": "a", "target": "b", "dtheta": 1.0},
            {"edge_id": "bc", "source": "b", "target": "c", "dtheta": 2.0},
            {"edge_id": "ac", "source": "a", "target": "c", "dtheta": direct},
        ],
        source="IDT 05H minimal-cycle reference control",
        source_commit_or_digest="REFERENCE_CONTROL_NOT_PRODUCTION",
        production=production,
    )


def validation_receipt() -> dict[str, Any]:
    positive = validate_input_dataset(minimal_cycle_reference_dataset(exact=True, production=False))
    negative = validate_input_dataset(minimal_cycle_reference_dataset(exact=False, production=False))
    return {
        "schema": "IDT_GLOBAL_EVENT_COMPLEX_INPUT_CONTRACT_VALIDATION_V0_1",
        "technical_status": "PASS"
        if positive.exact_clock_certified
        and not positive.promotion_eligible
        and not negative.exact_clock_certified
        and negative.exactness_failure is not None
        else "FAIL",
        "verdict": "PASS_IDT_GSC2_EVENT_COMPLEX_INPUT_CONTRACT_WITH_PRODUCTION_INPUT_OPEN",
        "production_event_complex": "OPEN_INPUT",
        "minimal_nontrivial_cycle_witness": {
            "vertices": 3,
            "edges": 3,
            "condition": "theta_ab + theta_bc = theta_ac",
        },
        "positive_control": asdict(positive),
        "negative_control": asdict(negative),
    }
