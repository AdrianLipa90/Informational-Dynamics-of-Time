from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _graph():
    return json.loads(GRAPH.read_text())


def test_dependency_graph_records_tir_half_fiber_normalization_pass():
    graph = _graph()
    assert graph["schema"] == "IDT_FORMAL_DEPENDENCY_GRAPH_V0_35"
    nodes = {node["id"]: node for node in graph["nodes"]}

    primitive = nodes["TEMPORAL_PRIMITIVE"]["status"]
    for marker in (
        "TIR_HALF_FIBER_INTRINSIC_PHASE_RATE_NORMALIZATION_PASS",
        "TIR_COMMON_CYCLE_RELATIVE_RATE_RATIO_PASS",
        "TIR_ABSOLUTE_RATE_BOUNDARY_PRESERVED",
        "HOSTED_REFERENCE_SUITE_667_OF_667",
    ):
        assert marker in primitive

    half = nodes["HALF_FRAME_TEMPORAL_GLUING"]["status"]
    for marker in (
        "TIR_FIRST_DISTINCTION_HALF_SPLIT_TYPED_CROSSLINK_PASS",
        "TIR_HALF_FIBER_TEMPORAL_NORMALIZATION_PASS",
        "SPIN_HALF_4PI_PHYSICAL_BINDING_OPEN",
    ):
        assert marker in half
