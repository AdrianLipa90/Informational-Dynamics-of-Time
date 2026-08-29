from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_temporal_seam_curvature_gate_is_recorded_append_only():
    graph = json.loads(GRAPH.read_text())
    assert graph["schema"].startswith("IDT_FORMAL_DEPENDENCY_GRAPH_V0_")
    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]

    for historical in [
        "HOSTED_REFERENCE_SUITE_640_OF_640",
        "HOSTED_REFERENCE_SUITE_667_OF_667",
        "HOSTED_REFERENCE_SUITE_668_OF_668",
        "HOSTED_REFERENCE_SUITE_686_OF_686",
        "HOSTED_REFERENCE_SUITE_701_OF_701",
        "HOSTED_REFERENCE_SUITE_702_OF_702",
        "HOSTED_REFERENCE_SUITE_717_OF_717",
        "HOSTED_REFERENCE_SUITE_718_OF_718",
    ]:
        assert historical in status

    for marker in [
        "TEMPORAL_SEAM_CURVATURE_GAUGE_INVARIANCE_PASS",
        "TEMPORAL_VERTEX_CONNECTION_COVARIANT_SPLIT_PASS",
        "GAUGE_NATIVE_MOVING_POWER_DECOMPOSITION_PASS",
        "POSITIVE_CURVATURE_RESPONSE_PASS",
        "CURVATURE_DISSIPATION_PASS",
        "GAUGE_INVARIANT_TEMPORAL_SEAM_OFFSET_PASS",
        "HOSTED_REFERENCE_SUITE_734_OF_734",
        "SEAM_PHASE_OFFSET_TO_INTRINSIC_DURATION_ACTIVE_NEXT_GATE",
    ]:
        assert marker in status
