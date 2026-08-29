from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_madelung_onsager_gate_waits_for_hosted_admission():
    graph = json.loads(GRAPH.read_text())
    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    assert "CONTINUUM_MADELUNG_SCHRODINGER_ONSAGER_SPLIT_PASS" not in status
    assert "CONTINUUM_MADELUNG_SCHRODINGER_ONSAGER_SPLIT_ACTIVE_NEXT_GATE" in status
