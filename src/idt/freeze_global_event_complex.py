from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .global_event_complex_source_freeze import (
    EventComplexFreezeError,
    freeze_event_capture,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Freeze a source-owned realized event capture into the IDT GSC2 contract."
    )
    parser.add_argument("capture", type=Path)
    parser.add_argument("--dataset-out", type=Path, required=True)
    parser.add_argument("--certificate-out", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        raw = json.loads(args.capture.read_text(encoding="utf-8"))
        frozen = freeze_event_capture(raw)
    except (OSError, json.JSONDecodeError, EventComplexFreezeError, ValueError) as exc:
        result = {
            "schema": "IDT_GSC2_SOURCE_FREEZE_CLI_RESULT_V0_1",
            "status": "FAIL",
            "error": str(exc),
            "production_promoted": False,
            "promotion_authority": False,
        }
        args.certificate_out.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return 2

    args.dataset_out.write_text(
        json.dumps(frozen.dataset, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    result = {
        "schema": "IDT_GSC2_SOURCE_FREEZE_CLI_RESULT_V0_1",
        "status": "PASS",
        "capture_sha256": frozen.capture_sha256,
        "production_source_admitted": frozen.production_source_admitted,
        "clock_id": frozen.clock_id,
        "certificate": asdict(frozen.certificate),
        "production_promoted": False,
        "promotion_authority": False,
        "note": "promotion_eligible is an input-gate result; repository canon promotion is a separate action",
    }
    args.certificate_out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if frozen.certificate.exact_clock_certified else 3


if __name__ == "__main__":
    raise SystemExit(main())
