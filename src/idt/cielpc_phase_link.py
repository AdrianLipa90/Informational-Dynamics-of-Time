"""01AU: transport-agnostic CIELPC phase-link framing.

This is the executable protocol layer between a semantic payload and a 36D
Euler-closed phase frame.  It does not claim a physical neutrino TX/RX channel;
the carrier backend is deliberately external to this module.

Each byte b is encoded as a common rotation s=2*pi*b/256 of an Euler triad
(s, s+2*pi/3, s+4*pi/3).  Twelve bytes therefore fill one 36D frame while each
triad satisfies sum(exp(i*gamma_k))=0 up to floating-point error.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable, Sequence

TAU = 2.0 * math.pi
TRIAD = TAU / 3.0
BYTES_PER_FRAME = 12
DIMS = 36
PROTOCOL = "CIELPC-PHASE/1"


def _wrap(x: float) -> float:
    y = float(x) % TAU
    return 0.0 if abs(y - TAU) < 1e-15 else y


def byte_to_triad(value: int) -> tuple[float, float, float]:
    if not 0 <= int(value) <= 255:
        raise ValueError("byte must be in [0,255]")
    s = TAU * int(value) / 256.0
    return (_wrap(s), _wrap(s + TRIAD), _wrap(s + 2.0 * TRIAD))


def triad_closure_residual(triad: Sequence[float]) -> float:
    if len(triad) != 3:
        raise ValueError("expected three phases")
    z = sum(complex(math.cos(float(p)), math.sin(float(p))) for p in triad)
    return abs(z)


def triad_to_byte(triad: Sequence[float]) -> int:
    if len(triad) != 3:
        raise ValueError("expected three phases")
    # The first phase is the encoded common rotation.  Decode to the nearest
    # one of 256 phase bins.  The other two phases are checked for Euler closure.
    if triad_closure_residual(triad) > 1e-9:
        raise ValueError("Euler triad closure failed")
    s = _wrap(float(triad[0]))
    return int(round((s / TAU) * 256.0)) % 256


@dataclass(frozen=True)
class PhaseFrame:
    seq: int
    total: int
    valid_bytes: int
    phase36: tuple[float, ...]
    message_sha256: str

    def to_json(self) -> str:
        return json.dumps({
            "protocol": PROTOCOL,
            "seq": self.seq,
            "total": self.total,
            "valid_bytes": self.valid_bytes,
            "phase36": list(self.phase36),
            "message_sha256": self.message_sha256,
        }, separators=(",", ":"), sort_keys=True)

    @staticmethod
    def from_json(line: str) -> "PhaseFrame":
        obj = json.loads(line)
        if obj.get("protocol") != PROTOCOL:
            raise ValueError("unsupported phase-link protocol")
        phase = tuple(float(x) for x in obj["phase36"])
        if len(phase) != DIMS or not all(math.isfinite(x) for x in phase):
            raise ValueError("phase36 must contain 36 finite values")
        return PhaseFrame(
            seq=int(obj["seq"]),
            total=int(obj["total"]),
            valid_bytes=int(obj["valid_bytes"]),
            phase36=phase,
            message_sha256=str(obj["message_sha256"]),
        )


def encode_bytes(payload: bytes) -> tuple[PhaseFrame, ...]:
    raw = bytes(payload)
    digest = hashlib.sha256(raw).hexdigest()
    total = max(1, math.ceil(len(raw) / BYTES_PER_FRAME))
    frames = []
    for seq in range(total):
        chunk = raw[seq * BYTES_PER_FRAME:(seq + 1) * BYTES_PER_FRAME]
        valid = len(chunk)
        padded = chunk + bytes(BYTES_PER_FRAME - valid)
        phase = tuple(p for b in padded for p in byte_to_triad(b))
        frames.append(PhaseFrame(seq, total, valid, phase, digest))
    return tuple(frames)


def encode_text(message: str) -> tuple[PhaseFrame, ...]:
    return encode_bytes(message.encode("utf-8"))


def decode_bytes(frames: Iterable[PhaseFrame]) -> bytes:
    ordered = sorted(tuple(frames), key=lambda f: f.seq)
    if not ordered:
        raise ValueError("no frames")
    total = ordered[0].total
    digest = ordered[0].message_sha256
    if total != len(ordered) or [f.seq for f in ordered] != list(range(total)):
        raise ValueError("incomplete or duplicate frame sequence")
    if any(f.total != total or f.message_sha256 != digest for f in ordered):
        raise ValueError("frame metadata mismatch")
    out = bytearray()
    for frame in ordered:
        if not 0 <= frame.valid_bytes <= BYTES_PER_FRAME:
            raise ValueError("invalid valid_bytes")
        vals = []
        for i in range(BYTES_PER_FRAME):
            triad = frame.phase36[3*i:3*i+3]
            vals.append(triad_to_byte(triad))
        out.extend(vals[:frame.valid_bytes])
    raw = bytes(out)
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError("message integrity check failed")
    return raw


def decode_text(frames: Iterable[PhaseFrame]) -> str:
    return decode_bytes(frames).decode("utf-8")


def max_frame_closure_residual(frame: PhaseFrame) -> float:
    return max(triad_closure_residual(frame.phase36[i:i+3]) for i in range(0, DIMS, 3))
