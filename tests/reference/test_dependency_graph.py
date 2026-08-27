from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _nodes():
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    return {node["id"]: node for node in data["nodes"]}


def test_dependency_graph_is_acyclic():
    nodes = _nodes()
    visiting = set()
    visited = set()

    def visit(node_id):
        if node_id in visited:
            return
        assert node_id not in visiting
        visiting.add(node_id)
        for parent in nodes[node_id]["depends_on"]:
            assert parent in nodes
            visit(parent)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)


def test_declared_chain_matches_project_order():
    nodes = _nodes()
    expected = [
        "TIR",
        "TEMPORAL_PRIMITIVE",
        "TEMPORAL_WAVE",
        "NOW",
        "BIFURCATION",
        "TEMPORAL_TRANSPORT",
        "MEMORY",
        "ORCHORBITAL_ATTRACTORS",
        "RETRODICTION",
        "RETROCAUSAL_TESTS",
        "EINSTEIN_CLOSURE",
    ]
    assert list(nodes) == expected
    for parent, child in zip(expected, expected[1:]):
        assert nodes[child]["depends_on"] == [parent]


def test_wave_now_bifurcation_transport_frontier_is_typed_in_order():
    nodes = _nodes()
    assert nodes["TEMPORAL_WAVE"]["status"] == "TARGETED_DERIVATION_CONTINUUM_HOLONOMY_PASS_CANDIDATE"
    assert nodes["NOW"]["status"] == "STRUCTURAL_PASS_WAVE_ACTIVATION_TARGETED_PASS_CANDIDATE"
    assert nodes["BIFURCATION"]["status"] == "FORMAL_CONTRACT_PASS_NOW_BRIDGE_TARGETED_PASS_CANDIDATE"
    assert nodes["TEMPORAL_TRANSPORT"]["status"] == "STRUCTURAL_REFERENCE_GATE_PASS_WAVE_ENERGY_TARGETED_PASS_CANDIDATE"


def test_memory_orchorbital_retrodiction_order_is_explicit():
    nodes = _nodes()
    assert nodes["MEMORY"]["status"] == "INTEGRATION_PASS_TRANSPORT_BRIDGE_TARGETED_PASS_CANDIDATE"
    assert nodes["ORCHORBITAL_ATTRACTORS"]["status"] == "PROVISIONAL_MEMORY_EXTENSION_LINEAGE_BRIDGE_TARGETED_PASS_CANDIDATE"
    assert nodes["ORCHORBITAL_ATTRACTORS"]["depends_on"] == ["MEMORY"]
    assert nodes["RETRODICTION"]["depends_on"] == ["ORCHORBITAL_ATTRACTORS"]
    assert "GATED_PENDING_MEMORY_ORCHORBITAL_ADMISSION" in nodes["RETRODICTION"]["status"]
