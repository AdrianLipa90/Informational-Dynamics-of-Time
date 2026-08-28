from copy import deepcopy

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorFieldState, ORCHORBITALError, ORCHORBITALStep
from src.idt.orchorbital_residence_ledger import (
    build_residence_receipts,
    receipt_from_dict,
    receipt_to_dict,
)


def _state(tau, x):
    return MemoryPhaseState(
        np.array([x, 0.0], dtype=float),
        np.array([0.0, 0.5], dtype=float),
        float(tau),
        0.0,
    )


def _valid_payload():
    step = ORCHORBITALStep(
        state_before=_state(0.0, 1.0),
        state_after=_state(0.1, 1.01),
        field_before=AttractorFieldState((), "A", False, 0.0, 1.0),
        field_after=AttractorFieldState((), "A", False, 0.0, 1.0),
        active_attractor="A",
        winding_increment=0.01,
        switched_after_segment=False,
    )
    return receipt_to_dict(build_residence_receipts([step])[0])


def test_strict_schema_roundtrip_accepts_exact_json_types():
    payload = _valid_payload()
    receipt = receipt_from_dict(payload)
    assert receipt_to_dict(receipt) == payload


@pytest.mark.parametrize("bad_index", [True, 0.0, "0"])
def test_receipt_index_rejects_json_type_coercion(bad_index):
    payload = deepcopy(_valid_payload())
    payload["index"] = bad_index
    with pytest.raises(ORCHORBITALError, match="index JSON type"):
        receipt_from_dict(payload)


@pytest.mark.parametrize("field", ["post_segment_leak", "switched_after_segment"])
def test_receipt_boolean_fields_reject_string_coercion(field):
    payload = deepcopy(_valid_payload())
    payload[field] = "false"
    with pytest.raises(ORCHORBITALError, match="JSON type must be boolean"):
        receipt_from_dict(payload)


def test_receipt_rejects_unknown_schema_key():
    payload = deepcopy(_valid_payload())
    payload["unexpected"] = "value"
    with pytest.raises(ORCHORBITALError, match="keys do not match schema"):
        receipt_from_dict(payload)


def test_receipt_rejects_missing_schema_key():
    payload = deepcopy(_valid_payload())
    del payload["winding_increment_hex"]
    with pytest.raises(ORCHORBITALError, match="keys do not match schema"):
        receipt_from_dict(payload)


def test_receipt_rejects_next_attractor_numeric_coercion():
    payload = deepcopy(_valid_payload())
    payload["next_attractor"] = 7
    with pytest.raises(ORCHORBITALError, match="next_attractor JSON type"):
        receipt_from_dict(payload)
