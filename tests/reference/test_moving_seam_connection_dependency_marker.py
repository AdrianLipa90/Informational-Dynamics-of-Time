from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_moving_seam_connection_markers_are_append_only():
    graph = json.loads(GRAPH.read_text())
    assert graph["schema"] == "IDT_FORMAL_DEPENDENCY_GRAPH_V0_38"
    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]

    for historical in [
        "HOSTED_REFERENCE_SUITE_640_OF_640",
        "HOSTED_REFERENCE_SUITE_667_OF_667",
        "HOSTED_REFERENCE_SUITE_668_OF_668",
        "HOSTED_REFERENCE_SUITE_686_OF_686",
        "HOSTED_REFERENCE_SUITE_701_OF_701",
        "HOSTED_REFERENCE_SUITE_702_OF_702",
        "MOVING_SEAM_CONNECTION_WORK_ACTIVE_NEXT_GATE",
    ]:
        assert historical in status

    for admitted in [
        "MOVING_SEAM_CONNECTION_WORK_PASS",
        "CONNECTION_WORK_OPERATOR_IDENTITY_PASS",
        "TIME_DEPENDENT_GAUGE_GEOMETRIC_POWER_CLOSURE_PASS",
        "INTRINSIC_SEAM_PHASE_OFFSET_PASS",
        "HOSTED_REFERENCE_SUITE_717_OF_717",
        "TEMPORAL_SEAM_CURVATURE_RESPONSE_ACTIVE_NEXT_GATE",
    ]:
        assert admitted in status

    assert set(nodes["HALF_FRAME_TEMPORAL_GLUING"]["depends_on"]) == {
        "TEMPORAL_WAVE",
        "RELATIONAL_PRECEDENCE",
    }
    assert "HALF_FRAME_TEMPORAL_GLUING" not in nodes["NOW"]["depends_on"]
