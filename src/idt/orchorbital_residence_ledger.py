from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path
from statistics import median, pvariance
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .orchorbital import ORCHORBITALError, ORCHORBITALStep


RECEIPT_SCHEMA = "idt.orchorbital-residence-receipt/v1"


@dataclass(frozen=True)
class ORCHORBITALResidenceReceipt:
    index: int
    active_attractor: str
    next_attractor: str | None
    post_segment_leak: bool
    delta_tau_hex: str
    winding_increment_hex: str
    switched_after_segment: bool
    state_before_sha256: str
    state_after_sha256: str
    previous_receipt_sha256: str | None
    receipt_sha256: str

    @property
    def delta_tau(self) -> float:
        return float.fromhex(self.delta_tau_hex)

    @property
    def winding_increment(self) -> float:
        return float.fromhex(self.winding_increment_hex)


@dataclass(frozen=True)
class AttractorResidenceEpisode:
    name: str
    start_index: int
    end_index: int
    segments: int
    dwell_tau: float
    winding: float


@dataclass(frozen=True)
class AttractorDwellStatistics:
    name: str
    episodes: int
    segments: int
    total_dwell_tau: float
    mean_dwell_tau: float
    median_dwell_tau: float
    min_dwell_tau: float
    max_dwell_tau: float
    variance_dwell_tau: float


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def _finite_state_bytes(state: MemoryPhaseState) -> bytes:
    position = np.asarray(state.position, dtype="<f8")
    velocity = np.asarray(state.velocity, dtype="<f8")
    if position.shape != (2,) or velocity.shape != (2,):
        raise ORCHORBITALError("ORCHORBITAL ledger requires exact two-component memory state")
    values = np.concatenate(
        [
            position,
            velocity,
            np.asarray([state.tau_internal, state.swept_area], dtype="<f8"),
        ]
    )
    if values.shape != (6,) or not np.all(np.isfinite(values)):
        raise ORCHORBITALError("ORCHORBITAL ledger memory state must be finite")
    return values.astype("<f8", copy=False).tobytes(order="C")


def state_sha256(state: MemoryPhaseState) -> str:
    return _sha256(_finite_state_bytes(state))


def _receipt_payload(receipt: ORCHORBITALResidenceReceipt) -> dict[str, object]:
    return {
        "schema": RECEIPT_SCHEMA,
        "index": receipt.index,
        "active_attractor": receipt.active_attractor,
        "next_attractor": receipt.next_attractor,
        "post_segment_leak": receipt.post_segment_leak,
        "delta_tau_hex": receipt.delta_tau_hex,
        "winding_increment_hex": receipt.winding_increment_hex,
        "switched_after_segment": receipt.switched_after_segment,
        "state_before_sha256": receipt.state_before_sha256,
        "state_after_sha256": receipt.state_after_sha256,
        "previous_receipt_sha256": receipt.previous_receipt_sha256,
    }


def _receipt_hash(receipt: ORCHORBITALResidenceReceipt) -> str:
    return _sha256(_canonical_json(_receipt_payload(receipt)))


def _validate_receipt_fields(receipt: ORCHORBITALResidenceReceipt) -> None:
    if receipt.index < 0:
        raise ORCHORBITALError("receipt index must be non-negative")
    if not receipt.active_attractor.strip():
        raise ORCHORBITALError("receipt active attractor must be non-empty")
    if receipt.next_attractor is not None and not receipt.next_attractor.strip():
        raise ORCHORBITALError("receipt next attractor must be non-empty when present")
    try:
        delta_tau = receipt.delta_tau
        winding = receipt.winding_increment
    except ValueError as exc:
        raise ORCHORBITALError("receipt float encoding is invalid") from exc
    if not math.isfinite(delta_tau) or delta_tau <= 0.0:
        raise ORCHORBITALError("receipt delta_tau must be finite and positive")
    if not math.isfinite(winding):
        raise ORCHORBITALError("receipt winding must be finite")
    if not _is_sha256(receipt.state_before_sha256) or not _is_sha256(receipt.state_after_sha256):
        raise ORCHORBITALError("receipt state hashes must be lowercase SHA-256")
    if receipt.previous_receipt_sha256 is not None and not _is_sha256(receipt.previous_receipt_sha256):
        raise ORCHORBITALError("receipt previous hash must be lowercase SHA-256")
    if not _is_sha256(receipt.receipt_sha256):
        raise ORCHORBITALError("receipt hash must be lowercase SHA-256")
    if receipt.post_segment_leak:
        if receipt.next_attractor is not None:
            raise ORCHORBITALError("LEAK_MODE receipt cannot name a next attractor")
    elif receipt.next_attractor is None:
        raise ORCHORBITALError("bound post-segment receipt requires a next attractor")
    expected_switch = receipt.next_attractor != receipt.active_attractor
    if receipt.switched_after_segment != expected_switch:
        raise ORCHORBITALError("receipt switch flag disagrees with attractor lineage")


def residence_receipt_from_step(
    step: ORCHORBITALStep,
    *,
    index: int,
    previous_receipt_sha256: str | None,
) -> ORCHORBITALResidenceReceipt:
    if index < 0:
        raise ORCHORBITALError("receipt index must be non-negative")
    if index == 0 and previous_receipt_sha256 is not None:
        raise ORCHORBITALError("genesis receipt cannot have a previous hash")
    if index > 0 and (previous_receipt_sha256 is None or not _is_sha256(previous_receipt_sha256)):
        raise ORCHORBITALError("non-genesis receipt requires a valid previous hash")

    active = str(step.active_attractor).strip()
    if not active:
        raise ORCHORBITALError("step active attractor must be non-empty")
    delta_tau = float(step.state_after.tau_internal - step.state_before.tau_internal)
    winding = float(step.winding_increment)
    if not math.isfinite(delta_tau) or delta_tau <= 0.0:
        raise ORCHORBITALError("step internal elapsed increment must be finite and positive")
    if not math.isfinite(winding):
        raise ORCHORBITALError("step winding increment must be finite")

    post_leak = bool(step.field_after.leak_mode)
    next_attractor = None if post_leak else step.field_after.active_attractor
    if next_attractor is not None:
        next_attractor = str(next_attractor).strip()
        if not next_attractor:
            raise ORCHORBITALError("step next attractor must be non-empty when bound")
    expected_switch = next_attractor != active
    if bool(step.switched_after_segment) != expected_switch:
        raise ORCHORBITALError("step switch flag disagrees with evaluated field lineage")

    draft = ORCHORBITALResidenceReceipt(
        index=index,
        active_attractor=active,
        next_attractor=next_attractor,
        post_segment_leak=post_leak,
        delta_tau_hex=delta_tau.hex(),
        winding_increment_hex=winding.hex(),
        switched_after_segment=expected_switch,
        state_before_sha256=state_sha256(step.state_before),
        state_after_sha256=state_sha256(step.state_after),
        previous_receipt_sha256=previous_receipt_sha256,
        receipt_sha256="0" * 64,
    )
    receipt = ORCHORBITALResidenceReceipt(
        **{**draft.__dict__, "receipt_sha256": _receipt_hash(draft)}
    )
    _validate_receipt_fields(receipt)
    return receipt


def build_residence_receipts(steps: Sequence[ORCHORBITALStep]) -> tuple[ORCHORBITALResidenceReceipt, ...]:
    if not steps:
        raise ORCHORBITALError("steps must be non-empty")
    receipts: list[ORCHORBITALResidenceReceipt] = []
    previous_hash: str | None = None
    previous_state_after: str | None = None
    for index, step in enumerate(steps):
        before_hash = state_sha256(step.state_before)
        if previous_state_after is not None and before_hash != previous_state_after:
            raise ORCHORBITALError("ORCHORBITAL step sequence is state-discontinuous")
        receipt = residence_receipt_from_step(
            step,
            index=index,
            previous_receipt_sha256=previous_hash,
        )
        receipts.append(receipt)
        previous_hash = receipt.receipt_sha256
        previous_state_after = receipt.state_after_sha256
    verify_residence_receipts(receipts)
    return tuple(receipts)


def verify_residence_receipts(receipts: Sequence[ORCHORBITALResidenceReceipt]) -> None:
    if not receipts:
        raise ORCHORBITALError("receipts must be non-empty")
    previous_hash: str | None = None
    previous_state_after: str | None = None
    for expected_index, receipt in enumerate(receipts):
        _validate_receipt_fields(receipt)
        if receipt.index != expected_index:
            raise ORCHORBITALError("receipt indices must be contiguous from zero")
        if receipt.previous_receipt_sha256 != previous_hash:
            raise ORCHORBITALError("receipt hash chain is broken")
        if previous_state_after is not None and receipt.state_before_sha256 != previous_state_after:
            raise ORCHORBITALError("receipt state lineage is discontinuous")
        if _receipt_hash(receipt) != receipt.receipt_sha256:
            raise ORCHORBITALError("receipt content hash mismatch")
        previous_hash = receipt.receipt_sha256
        previous_state_after = receipt.state_after_sha256


def receipt_to_dict(receipt: ORCHORBITALResidenceReceipt) -> dict[str, object]:
    _validate_receipt_fields(receipt)
    return {**_receipt_payload(receipt), "receipt_sha256": receipt.receipt_sha256}


def receipt_from_dict(value: dict[str, object]) -> ORCHORBITALResidenceReceipt:
    if value.get("schema") != RECEIPT_SCHEMA:
        raise ORCHORBITALError("unsupported ORCHORBITAL residence receipt schema")
    try:
        receipt = ORCHORBITALResidenceReceipt(
            index=int(value["index"]),
            active_attractor=str(value["active_attractor"]),
            next_attractor=None if value["next_attractor"] is None else str(value["next_attractor"]),
            post_segment_leak=bool(value["post_segment_leak"]),
            delta_tau_hex=str(value["delta_tau_hex"]),
            winding_increment_hex=str(value["winding_increment_hex"]),
            switched_after_segment=bool(value["switched_after_segment"]),
            state_before_sha256=str(value["state_before_sha256"]),
            state_after_sha256=str(value["state_after_sha256"]),
            previous_receipt_sha256=(
                None
                if value["previous_receipt_sha256"] is None
                else str(value["previous_receipt_sha256"])
            ),
            receipt_sha256=str(value["receipt_sha256"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ORCHORBITALError("malformed ORCHORBITAL residence receipt") from exc
    _validate_receipt_fields(receipt)
    return receipt


def read_residence_ledger(path: str | os.PathLike[str]) -> tuple[ORCHORBITALResidenceReceipt, ...]:
    ledger_path = Path(path)
    if not ledger_path.is_file():
        raise ORCHORBITALError("residence ledger file is absent")
    raw = ledger_path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ORCHORBITALError("existing residence ledger is empty")
    receipts: list[ORCHORBITALResidenceReceipt] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ORCHORBITALError(f"invalid residence ledger JSON at line {line_number}") from exc
        if not isinstance(value, dict):
            raise ORCHORBITALError(f"residence ledger line {line_number} must be an object")
        receipts.append(receipt_from_dict(value))
    verify_residence_receipts(receipts)
    return tuple(receipts)


def append_residence_steps(
    path: str | os.PathLike[str],
    steps: Sequence[ORCHORBITALStep],
) -> tuple[ORCHORBITALResidenceReceipt, ...]:
    if not steps:
        raise ORCHORBITALError("steps must be non-empty")
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    existing: tuple[ORCHORBITALResidenceReceipt, ...] = ()
    if ledger_path.exists():
        existing = read_residence_ledger(ledger_path)

    start_index = len(existing)
    previous_hash = existing[-1].receipt_sha256 if existing else None
    previous_state_after = existing[-1].state_after_sha256 if existing else None
    new_receipts: list[ORCHORBITALResidenceReceipt] = []

    for offset, step in enumerate(steps):
        before_hash = state_sha256(step.state_before)
        if previous_state_after is not None and before_hash != previous_state_after:
            raise ORCHORBITALError("appended trajectory is discontinuous with ledger tail")
        receipt = residence_receipt_from_step(
            step,
            index=start_index + offset,
            previous_receipt_sha256=previous_hash,
        )
        new_receipts.append(receipt)
        previous_hash = receipt.receipt_sha256
        previous_state_after = receipt.state_after_sha256

    candidate = (*existing, *new_receipts)
    verify_residence_receipts(candidate)
    encoded = "".join(
        json.dumps(receipt_to_dict(receipt), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for receipt in new_receipts
    )

    mode = "a" if existing else "x"
    with ledger_path.open(mode, encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())

    persisted = read_residence_ledger(ledger_path)
    if persisted != candidate:
        raise ORCHORBITALError("persisted residence ledger differs from validated candidate")
    return tuple(new_receipts)


def residence_episodes(
    receipts: Sequence[ORCHORBITALResidenceReceipt],
) -> tuple[AttractorResidenceEpisode, ...]:
    verify_residence_receipts(receipts)
    episodes: list[AttractorResidenceEpisode] = []
    start = 0
    current = receipts[0].active_attractor
    dwell = 0.0
    winding = 0.0
    segments = 0

    for offset, receipt in enumerate(receipts):
        if receipt.active_attractor != current:
            episodes.append(
                AttractorResidenceEpisode(current, start, offset - 1, segments, dwell, winding)
            )
            current = receipt.active_attractor
            start = offset
            dwell = 0.0
            winding = 0.0
            segments = 0
        dwell += receipt.delta_tau
        winding += receipt.winding_increment
        segments += 1

    episodes.append(
        AttractorResidenceEpisode(current, start, len(receipts) - 1, segments, dwell, winding)
    )
    return tuple(episodes)


def dwell_time_statistics(
    receipts: Sequence[ORCHORBITALResidenceReceipt],
) -> tuple[AttractorDwellStatistics, ...]:
    episodes = residence_episodes(receipts)
    order: list[str] = []
    dwell_by_name: dict[str, list[float]] = {}
    segments_by_name: dict[str, int] = {}
    for episode in episodes:
        if episode.name not in dwell_by_name:
            order.append(episode.name)
            dwell_by_name[episode.name] = []
            segments_by_name[episode.name] = 0
        dwell_by_name[episode.name].append(float(episode.dwell_tau))
        segments_by_name[episode.name] += int(episode.segments)

    out: list[AttractorDwellStatistics] = []
    for name in order:
        values = dwell_by_name[name]
        out.append(
            AttractorDwellStatistics(
                name=name,
                episodes=len(values),
                segments=segments_by_name[name],
                total_dwell_tau=float(sum(values)),
                mean_dwell_tau=float(sum(values) / len(values)),
                median_dwell_tau=float(median(values)),
                min_dwell_tau=float(min(values)),
                max_dwell_tau=float(max(values)),
                variance_dwell_tau=float(pvariance(values)),
            )
        )
    return tuple(out)


def transition_counts_from_receipts(
    receipts: Sequence[ORCHORBITALResidenceReceipt],
) -> dict[tuple[str, str], int]:
    verify_residence_receipts(receipts)
    counts: dict[tuple[str, str], int] = {}
    for left, right in zip(receipts, receipts[1:]):
        if left.active_attractor == right.active_attractor:
            continue
        edge = (left.active_attractor, right.active_attractor)
        counts[edge] = counts.get(edge, 0) + 1
    return counts
