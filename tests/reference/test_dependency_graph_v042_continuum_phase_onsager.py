from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _nodes():
    return {node["id"]: node for node in json.loads(GRAPH.read_text())["nodes"]}


def test_continuum_phase_onsager_gate_is_not_prematurely_promoted():
    nodes = _nodes()
    half_status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    # Before hosted admission, the new continuum Onsager gate remains receipt-local.
    assert "CONTINUUM_PHASE_GRADIENT_ONSAGER_FLOW_PASS" not in half_status
