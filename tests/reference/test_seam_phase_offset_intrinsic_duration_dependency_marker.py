from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_seam_phase_offset_duration_gate_is_recorded_append_only():
    graph = json.loads(GRAPH.read_text())
    assert graph["schema"].startswith("IDT_FORMAL_DEPENDENCY_GRAPH_V0_")
    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]

    for historical in [
        "HOSTED_REFERENCE_SUITE_718_OF_718",
        "HOSTED_REFERENCE_SUITE_734_OF_734",
        "HOSTED_REFERENCE_SUITE_735_OF_735_FINAL_HEAD_CONFORMANCE_PASS",
    ]:
        assert historical in status

    for marker in [
        "SEAM_PHASE_OFFSET_INTRINSIC_DURATION_PASS",
        "REFERENCE_PHASE_CLOCK_NORMALIZATION_PASS",
        "GAUGE_INVARIANT_INTRINSIC_TEMPORAL_OFFSET_PASS",
        "INFORMATION_RATE_OFFSET_IDENTITY_PASS",
        "CLOCK_LAPSE_OFFSET_COMPOSITION_PASS",
        "INTEGER_CURVATURE_WINDING_REFERENCE_PERIOD_CONTROL_PASS",
        "HOSTED_REFERENCE_SUITE_753_OF_753",
        "MATERIAL_TEMPORAL_OFFSET_BINDING_ACTIVE_NEXT_GATE",
    ]:
        assert marker in status
