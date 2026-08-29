from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_madelung_onsager_gate_is_admitted_after_hosted_pass():
    graph = json.loads(GRAPH.read_text())
    nodes = {node["id"]: node for node in graph["nodes"]}
    status = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    for marker in [
        "CONTINUUM_MADELUNG_SCHRODINGER_ONSAGER_SPLIT_ACTIVE_NEXT_GATE",
        "CONTINUUM_MADELUNG_SCHRODINGER_ONSAGER_SPLIT_PASS",
        "EXACT_POLAR_DENSITY_PHASE_DECOMPOSITION_PASS",
        "COMPACT_PHASE_DENSITY_BALANCE_PASS",
        "CONSTANT_M_CURRENT_VELOCITY_BALANCE_PASS",
        "LINEARIZED_QUADRATIC_SCHRODINGER_DISPERSION_PASS",
        "POSITIVE_ONSAGER_LINEAR_MODE_NONPOSITIVE_GROWTH_PASS",
        "HOSTED_REFERENCE_SUITE_778_OF_778",
        "TEMPORAL_WAVE_LINEAR_MODE_AND_NOW_FRONTIER_COUPLING_ACTIVE_NEXT_GATE",
    ]:
        assert marker in status
