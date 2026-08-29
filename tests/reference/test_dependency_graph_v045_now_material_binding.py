from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_now_material_binding_is_parallel_and_bifurcation_dependency_is_preserved():
    graph = json.loads(GRAPH.read_text())
    nodes = {node["id"]: node for node in graph["nodes"]}

    binding = nodes["NOW_MATERIAL_BINDING"]
    assert set(binding["depends_on"]) == {"TEMPORAL_DENSITY_FRONT", "NOW"}
    for marker in [
        "REALIZED_EVENT_TO_MATERIAL_FRONT_BINDING_ALGEBRAIC_REFERENCE_PASS",
        "EXCHANGE_INVOLUTION_UNIQUE_HALF_SELECTOR_PASS",
        "MIRROR_QUANTILE_EQUIVARIANCE_PASS",
        "STATE_RECURRENCE_OCCURRENCE_IDENTITY_PASS",
        "SERIAL_CONCURRENT_BINDING_PASS",
        "WAVE_EVENT_FACTORIZATION_PASS",
        "HOSTED_REFERENCE_SUITE_805_OF_805",
        "BOUND_NOW_BIFURCATION_CONSISTENCY_ACTIVE_NEXT_GATE",
    ]:
        assert marker in binding["status"]

    now_status = nodes["NOW"]["status"]
    for marker in [
        "MATERIAL_QUANTILE_BINDING_PASS",
        "EXCHANGE_SYMMETRIC_HALF_SELECTOR_PASS",
        "SERIAL_CONCURRENT_MATERIAL_BINDING_PASS",
        "HOSTED_REFERENCE_SUITE_805_OF_805",
    ]:
        assert marker in now_status

    assert nodes["BIFURCATION"]["depends_on"] == ["NOW"]
