from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_v041_temporal_density_current_markers_are_append_only():
    graph = json.loads(GRAPH.read_text())
    prefix = "IDT_FORMAL_DEPENDENCY_GRAPH_V0_"
    assert graph["schema"].startswith(prefix)
    assert int(graph["schema"][len(prefix):]) >= 41

    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]

    historical = [
        "HOSTED_REFERENCE_SUITE_640_OF_640",
        "HOSTED_REFERENCE_SUITE_667_OF_667",
        "HOSTED_REFERENCE_SUITE_668_OF_668",
        "HOSTED_REFERENCE_SUITE_686_OF_686",
        "HOSTED_REFERENCE_SUITE_706_OF_706",
        "HOSTED_REFERENCE_SUITE_718_OF_718",
        "HOSTED_REFERENCE_SUITE_730_OF_730",
        "HOSTED_REFERENCE_SUITE_741_OF_741",
    ]
    v041 = [
        "TEMPORAL_DENSITY_CURRENT_EXACT_CONTINUITY_PASS",
        "SEAM_COHERENCE_TRANSPORT_QUADRATURE_PASS",
        "GAUGE_INVARIANT_EDGE_CURRENT_PASS",
        "CONTINUUM_CURRENT_SECOND_ORDER_PASS",
        "ONSAGER_PHASE_ONLY_DENSITY_INVARIANCE_PASS",
        "HOSTED_REFERENCE_SUITE_752_OF_752",
        "CONTINUUM_PHASE_GRADIENT_ONSAGER_FLOW_ACTIVE_NEXT_GATE",
    ]
    for marker in historical + v041:
        assert marker in status
