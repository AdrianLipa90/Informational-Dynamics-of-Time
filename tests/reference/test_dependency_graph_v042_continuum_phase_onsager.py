from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _nodes():
    return {node["id"]: node for node in json.loads(GRAPH.read_text())["nodes"]}


def test_continuum_phase_onsager_gate_is_admitted_after_hosted_pass():
    nodes = _nodes()
    half_status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    for marker in [
        "HOSTED_REFERENCE_SUITE_752_OF_752",
        "HOSTED_REFERENCE_SUITE_753_OF_753",
        "CONTINUUM_PHASE_GRADIENT_ONSAGER_FLOW_PASS",
        "CONTINUUM_PHASE_ENERGY_LYAPUNOV_PASS",
        "GAUGE_COVARIANT_PHASE_GRADIENT_DIFFUSION_PASS",
        "PHASE_ONLY_POINTWISE_DENSITY_INVARIANCE_PASS",
        "HOSTED_REFERENCE_SUITE_764_OF_764",
        "CONTINUUM_MADELUNG_SCHRODINGER_ONSAGER_SPLIT_ACTIVE_NEXT_GATE",
    ]:
        assert marker in half_status
