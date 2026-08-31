from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from src.idt.global_relational_clock import (
    GlobalClockCocycleError,
    reconstruct_global_clock_potential,
)

SCHEMA = "IDT_GLOBAL_LAPSE_PRODUCTION_CAPTURE_V0_1"


class GlobalLapseCaptureError(ValueError):
    """Raised when a supplied W5 lapse capture violates the source contract."""


@dataclass(frozen=True)
class GlobalLapseCaptureCertificate:
    input_valid: bool
    integrity_valid: bool
    cocycle_valid: bool
    patch_coverage_valid: bool
    production_input: bool
    promotion_review_eligible: bool
    canon_allowed: bool
    dataset_id: str
    realization_id: str
    clock_id: str
    reference_patch_id: str
    dataset_sha256: str
    max_relative_residual: float
    patch_count: int
    edge_count: int
    patch_lapse: dict[str, float]


def _id(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GlobalLapseCaptureError(f"{name} must be a non-empty string")
    return value.strip()


def _positive(value: Any, name: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise GlobalLapseCaptureError(f"{name} must be numeric") from exc
    if not math.isfinite(out) or out <= 0.0:
        raise GlobalLapseCaptureError(f"{name} must be finite and strictly positive")
    return out


def _normalized_patches(patches: Sequence[Any]) -> list[str]:
    if not isinstance(patches, Sequence) or isinstance(patches, (str, bytes)):
        raise GlobalLapseCaptureError("patch_ids must be a sequence")
    out = [_id(item, "patch_id") for item in patches]
    if not out:
        raise GlobalLapseCaptureError("patch_ids must be non-empty")
    if len(set(out)) != len(out):
        raise GlobalLapseCaptureError("patch_ids must be unique")
    return out


def _normalized_edges(edges: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(edges, Sequence) or isinstance(edges, (str, bytes)):
        raise GlobalLapseCaptureError("clock_ratio_edges must be a sequence")
    out: list[dict[str, Any]] = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, Mapping):
            raise GlobalLapseCaptureError(f"edge {index} must be an object")
        out.append(
            {
                "x_patch_id": _id(edge.get("x_patch_id"), f"edge {index} x_patch_id"),
                "y_patch_id": _id(edge.get("y_patch_id"), f"edge {index} y_patch_id"),
                "N_x_given_y": _positive(edge.get("N_x_given_y"), f"edge {index} N_x_given_y"),
            }
        )
    if not out:
        raise GlobalLapseCaptureError("clock_ratio_edges must be non-empty")
    return out


def _normalized_provenance(provenance: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(provenance, Mapping):
        raise GlobalLapseCaptureError("provenance must be an object")
    return {
        "source_owner": _id(provenance.get("source_owner"), "provenance.source_owner"),
        "source_reference": _id(provenance.get("source_reference"), "provenance.source_reference"),
        "source_commit_or_digest": _id(
            provenance.get("source_commit_or_digest"),
            "provenance.source_commit_or_digest",
        ),
    }


def capture_sha256(
    *,
    dataset_id: str,
    realization_id: str,
    clock_id: str,
    reference_patch_id: str,
    patch_ids: Sequence[Any],
    clock_ratio_edges: Sequence[Mapping[str, Any]],
    provenance: Mapping[str, Any],
    production: bool,
) -> str:
    patches = sorted(_normalized_patches(patch_ids))
    edges = sorted(
        _normalized_edges(clock_ratio_edges),
        key=lambda edge: (
            edge["x_patch_id"],
            edge["y_patch_id"],
            edge["N_x_given_y"],
        ),
    )
    prov = _normalized_provenance(provenance)
    payload = {
        "schema": SCHEMA,
        "dataset_id": _id(dataset_id, "dataset_id"),
        "realization_id": _id(realization_id, "realization_id"),
        "clock_id": _id(clock_id, "clock_id"),
        "reference_patch_id": _id(reference_patch_id, "reference_patch_id"),
        "patch_ids": patches,
        "clock_ratio_edges": edges,
        "provenance": prov,
        "production": bool(production),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_capture_dataset(
    *,
    dataset_id: str,
    realization_id: str,
    clock_id: str,
    reference_patch_id: str,
    patch_ids: Sequence[Any],
    clock_ratio_edges: Sequence[Mapping[str, Any]],
    source_owner: str,
    source_reference: str,
    source_commit_or_digest: str,
    production: bool,
) -> dict[str, Any]:
    patches = _normalized_patches(patch_ids)
    edges = _normalized_edges(clock_ratio_edges)
    provenance = _normalized_provenance(
        {
            "source_owner": source_owner,
            "source_reference": source_reference,
            "source_commit_or_digest": source_commit_or_digest,
        }
    )
    data = {
        "schema": SCHEMA,
        "dataset_id": _id(dataset_id, "dataset_id"),
        "realization_id": _id(realization_id, "realization_id"),
        "clock_id": _id(clock_id, "clock_id"),
        "reference_patch_id": _id(reference_patch_id, "reference_patch_id"),
        "patch_ids": patches,
        "clock_ratio_edges": edges,
        "provenance": provenance,
        "production": bool(production),
    }
    data["dataset_sha256"] = capture_sha256(
        dataset_id=data["dataset_id"],
        realization_id=data["realization_id"],
        clock_id=data["clock_id"],
        reference_patch_id=data["reference_patch_id"],
        patch_ids=patches,
        clock_ratio_edges=edges,
        provenance=provenance,
        production=bool(production),
    )
    return data


def certify_capture_dataset(
    data: Mapping[str, Any],
    *,
    expected_patch_ids: Iterable[str] | None = None,
    tolerance: float = 1e-10,
) -> GlobalLapseCaptureCertificate:
    if not isinstance(data, Mapping):
        raise GlobalLapseCaptureError("dataset must be an object")
    if data.get("schema") != SCHEMA:
        raise GlobalLapseCaptureError(f"schema must equal {SCHEMA}")
    if type(data.get("production")) is not bool:
        raise GlobalLapseCaptureError("production must be a boolean")

    dataset_id = _id(data.get("dataset_id"), "dataset_id")
    realization_id = _id(data.get("realization_id"), "realization_id")
    clock_id = _id(data.get("clock_id"), "clock_id")
    reference_patch_id = _id(data.get("reference_patch_id"), "reference_patch_id")

    raw_patches = data.get("patch_ids")
    raw_edges = data.get("clock_ratio_edges")
    if not isinstance(raw_patches, list):
        raise GlobalLapseCaptureError("patch_ids must be a list")
    if not isinstance(raw_edges, list):
        raise GlobalLapseCaptureError("clock_ratio_edges must be a list")
    patches = _normalized_patches(raw_patches)
    edges = _normalized_edges(raw_edges)
    provenance = _normalized_provenance(data.get("provenance"))

    patch_set = set(patches)
    if reference_patch_id not in patch_set:
        raise GlobalLapseCaptureError("reference_patch_id must belong to patch_ids")
    for edge in edges:
        if edge["x_patch_id"] not in patch_set or edge["y_patch_id"] not in patch_set:
            raise GlobalLapseCaptureError("clock-ratio edge endpoint is outside patch_ids")

    if expected_patch_ids is not None:
        expected = [_id(item, "expected patch id") for item in expected_patch_ids]
        if not expected or len(set(expected)) != len(expected):
            raise GlobalLapseCaptureError("expected_patch_ids must be non-empty and unique")
        if set(expected) != patch_set:
            missing = sorted(set(expected) - patch_set)
            extra = sorted(patch_set - set(expected))
            raise GlobalLapseCaptureError(
                f"patch coverage mismatch: missing={missing}, extra={extra}"
            )

    supplied_digest = _id(data.get("dataset_sha256"), "dataset_sha256")
    computed_digest = capture_sha256(
        dataset_id=dataset_id,
        realization_id=realization_id,
        clock_id=clock_id,
        reference_patch_id=reference_patch_id,
        patch_ids=patches,
        clock_ratio_edges=edges,
        provenance=provenance,
        production=bool(data["production"]),
    )
    if supplied_digest != computed_digest:
        raise GlobalLapseCaptureError("dataset_sha256 mismatch")

    cocycle_edges = [
        (edge["x_patch_id"], edge["y_patch_id"], edge["N_x_given_y"])
        for edge in edges
    ]
    try:
        certificate = reconstruct_global_clock_potential(
            cocycle_edges,
            reference=reference_patch_id,
            tolerance=tolerance,
        )
    except GlobalClockCocycleError as exc:
        raise GlobalLapseCaptureError(f"global clock cocycle failed: {exc}") from exc

    if set(certificate.relative_rates) != patch_set:
        missing = sorted(patch_set - set(certificate.relative_rates))
        extra = sorted(set(certificate.relative_rates) - patch_set)
        raise GlobalLapseCaptureError(
            f"reconstructed lapse patch coverage mismatch: missing={missing}, extra={extra}"
        )

    patch_lapse = {
        patch_id: float(certificate.relative_rates[patch_id])
        for patch_id in sorted(patch_set)
    }
    if any((not math.isfinite(value) or value <= 0.0) for value in patch_lapse.values()):
        raise GlobalLapseCaptureError("reconstructed lapse lost positive orientation")

    production = bool(data["production"])
    return GlobalLapseCaptureCertificate(
        input_valid=True,
        integrity_valid=True,
        cocycle_valid=True,
        patch_coverage_valid=True,
        production_input=production,
        promotion_review_eligible=production,
        canon_allowed=False,
        dataset_id=dataset_id,
        realization_id=realization_id,
        clock_id=clock_id,
        reference_patch_id=reference_patch_id,
        dataset_sha256=computed_digest,
        max_relative_residual=float(certificate.max_relative_residual),
        patch_count=len(patches),
        edge_count=len(edges),
        patch_lapse=patch_lapse,
    )


def reference_triangle_capture(*, production: bool = False) -> dict[str, Any]:
    return build_capture_dataset(
        dataset_id="reference-global-lapse-triangle",
        realization_id="reference-realization",
        clock_id="reference-clock",
        reference_patch_id="p0",
        patch_ids=["p0", "p1", "p2"],
        clock_ratio_edges=[
            {"x_patch_id": "p1", "y_patch_id": "p0", "N_x_given_y": 2.0},
            {"x_patch_id": "p2", "y_patch_id": "p1", "N_x_given_y": 3.0},
            {"x_patch_id": "p2", "y_patch_id": "p0", "N_x_given_y": 6.0},
        ],
        source_owner="IDT reference control",
        source_reference="05K/reference-triangle",
        source_commit_or_digest="REFERENCE_CONTROL_NOT_PRODUCTION",
        production=production,
    )
