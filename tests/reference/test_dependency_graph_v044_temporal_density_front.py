from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_temporal_density_front_is_admitted_as_parallel_material_coordinate():
    graph = json.loads(GRAPH.read_text())
    nodes = {node["id"]: node for node in graph["nodes"]}

    front = nodes["TEMPORAL_DENSITY_FRONT"]
    assert front["depends_on"] == ["HALF_FRAME_TEMPORAL_GLUING"]
    for marker in [
        "THRESHOLD_FREE_CUMULATIVE_MASS_FRONT_ALGEBRAIC_REFERENCE_PASS",
        "QUANTILE_LOCAL_VELOCITY_PASS",
        "HALF_MASS_TIR_SYMMETRIC_MARKER_PASS",
        "DISCRETE_CUMULATIVE_FLUX_TELESCOPING_PASS",
        "BARYCENTER_VARIANCE_KINEMATICS_PASS",
        "HOSTED_REFERENCE_SUITE_794_OF_794",
        "HOSTED_REFERENCE_SUITE_795_OF_795",
        "FINAL_HEAD_CONFORMANCE_PASS",
        "NOW_MATERIAL_REALIZATION_BINDING_ACTIVE_NEXT_GATE",
    ]:
        assert marker in front["status"]

    half_status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    for historical in [
        "HOSTED_REFERENCE_SUITE_764_OF_764",
        "HOSTED_REFERENCE_SUITE_778_OF_778",
        "HOSTED_REFERENCE_SUITE_794_OF_794",
        "HOSTED_REFERENCE_SUITE_795_OF_795",
    ]:
        assert historical in half_status

    now = nodes["NOW"]
    assert set(now["depends_on"]) == {"TEMPORAL_WAVE", "RELATIONAL_PRECEDENCE"}
    assert "MATERIAL_QUANTILE_BINDING_SEPARATELY_TYPED_ACTIVE_NEXT_GATE" in now["status"]
