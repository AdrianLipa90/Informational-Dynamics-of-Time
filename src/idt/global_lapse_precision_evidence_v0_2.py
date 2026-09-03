from __future__ import annotations

import hashlib, json
from dataclasses import asdict
from typing import Any, Mapping

from src.idt.global_lapse_precision_production_capture import (
    GlobalLapsePrecisionCaptureError,
    certify_precision_capture_dataset,
)

RECEIPT_SCHEMA="IDT_GLOBAL_LAPSE_PRECISION_EVIDENCE_RECEIPT_V0_2"

def _sha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def certify_precision_lapse_evidence_v02(data: Mapping[str,Any]) -> dict[str,Any]:
    cert=certify_precision_capture_dataset(data)
    rid=cert.realization_id
    if rid.startswith("pncs:realization36:"):
        raise GlobalLapsePrecisionCaptureError("IDT physical realization id must not alias a PNCS Phase36 realization id")
    payload={"schema":RECEIPT_SCHEMA,"authority":"SOURCE_CONTRACT","physical_production_claim":False,"physical_realization_id":rid,**asdict(cert)}
    payload["receipt_sha256"]=_sha(payload)
    return payload
