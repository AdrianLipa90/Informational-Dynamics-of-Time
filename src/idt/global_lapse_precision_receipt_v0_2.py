from __future__ import annotations

import hashlib, json
from dataclasses import asdict
from typing import Any

from src.idt.global_lapse_precision_production_capture import GlobalLapsePrecisionCertificate

RECEIPT_SCHEMA="IDT_GLOBAL_LAPSE_PRECISION_CERTIFICATE_V0_2"

def _sha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def precision_certificate_receipt(cert: GlobalLapsePrecisionCertificate) -> dict[str,Any]:
    if not isinstance(cert,GlobalLapsePrecisionCertificate):
        raise TypeError("GlobalLapsePrecisionCertificate required")
    payload={"schema":RECEIPT_SCHEMA,"authority":"SOURCE_CONTRACT","physical_production_claim":False,**asdict(cert)}
    payload["receipt_sha256"]=_sha(payload)
    return payload
