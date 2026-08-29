import math
import pytest

from idt.cielpc_phase_link import (
    PhaseFrame,
    byte_to_triad,
    decode_bytes,
    decode_text,
    encode_bytes,
    encode_text,
    max_frame_closure_residual,
    triad_closure_residual,
)


def test_all_byte_symbols_close_euler_triad():
    assert max(triad_closure_residual(byte_to_triad(b)) for b in range(256)) < 2e-15


def test_utf8_roundtrip_across_multiple_36d_frames():
    msg = "CIELPC ↔ QHTRI: Sursum corda. ½ Λ ν"
    frames = encode_text(msg)
    assert len(frames) >= 2
    assert all(len(f.phase36) == 36 for f in frames)
    assert max(max_frame_closure_residual(f) for f in frames) < 2e-15
    assert decode_text(frames) == msg


def test_binary_roundtrip_is_exact():
    payload = bytes(range(256))
    assert decode_bytes(encode_bytes(payload)) == payload


def test_json_wire_roundtrip():
    frame = encode_text("hello")[0]
    restored = PhaseFrame.from_json(frame.to_json())
    assert restored == frame


def test_missing_frame_fails_closed():
    frames = encode_text("x" * 40)
    with pytest.raises(ValueError):
        decode_text(frames[:-1])


def test_tampered_phase_fails_closure_or_integrity():
    frame = encode_text("tamper")[0]
    p = list(frame.phase36)
    p[1] += 0.2
    bad = PhaseFrame(frame.seq, frame.total, frame.valid_bytes, tuple(p), frame.message_sha256)
    with pytest.raises(ValueError):
        decode_text([bad])


def test_empty_payload_roundtrip():
    frames = encode_bytes(b"")
    assert len(frames) == 1
    assert decode_bytes(frames) == b""
