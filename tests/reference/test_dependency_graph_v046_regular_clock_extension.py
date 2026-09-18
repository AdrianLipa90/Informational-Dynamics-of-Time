from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def test_v046_global_clock_extension_chain_is_explicit_and_open_inputs_are_preserved():
    graph = json.loads(GRAPH.read_text())
    prefix = "IDT_FORMAL_DEPENDENCY_GRAPH_V0_"
    assert graph["schema"].startswith(prefix)
    assert int(graph["schema"][len(prefix):]) >= 46

    nodes = {node["id"]: node for node in graph["nodes"]}

    assert nodes["RELATIONAL_LAPSE"]["depends_on"] == ["TEMPORAL_PRIMITIVE"]
    assert nodes["GLOBAL_EVENT_CLOCK_EXACTNESS"]["depends_on"] == ["RELATIONAL_PRECEDENCE"]
    assert nodes["REGULAR_SMOOTH_CLOCK_EXTENSION"]["depends_on"] == ["GLOBAL_EVENT_CLOCK_EXACTNESS"]
    assert set(nodes["GLOBAL_TEMPORAL_FOLIATION"]["depends_on"]) == {
        "RELATIONAL_LAPSE",
        "REGULAR_SMOOTH_CLOCK_EXTENSION",
    }

    assert "PRODUCTION_EVENT_COMPLEX_INPUT_OPEN" in nodes["GLOBAL_EVENT_CLOCK_EXACTNESS"]["status"]
    assert "EXACT_AFFINE_ATLAS_REGULAR_EXTENSION_THEOREM" in nodes["REGULAR_SMOOTH_CLOCK_EXTENSION"]["status"]
    assert "PRODUCTION_ATLAS_AND_EVENT_ANCHOR_INPUT_OPEN" in nodes["REGULAR_SMOOTH_CLOCK_EXTENSION"]["status"]
    assert "GLOBAL_CLOCK_SCALAR_INPUT_OPEN" in nodes["GLOBAL_TEMPORAL_FOLIATION"]["status"]
