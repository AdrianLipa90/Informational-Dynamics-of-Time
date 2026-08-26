from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _nodes():
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    return {node["id"]: node for node in data["nodes"]}


def test_dependency_graph_is_acyclic() -> None:
    nodes = _nodes()
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visited:
            return
        assert node_id not in visiting, f"cycle detected at {node_id}"
        visiting.add(node_id)
        for parent in nodes[node_id]["depends_on"]:
            assert parent in nodes
            visit(parent)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in nodes:
        visit(node_id)


def test_declared_chain_matches_project_order() -> None:
    nodes = _nodes()
    expected = [
        "TIR",
        "TEMPORAL_PRIMITIVE",
        "TEMPORAL_WAVE",
        "NOW",
        "BIFURCATION",
        "TEMPORAL_TRANSPORT",
        "MEMORY",
        "RETRODICTION",
        "RETROCAUSAL_TESTS",
        "EINSTEIN_CLOSURE",
    ]
    assert list(nodes) == expected
    for parent, child in zip(expected, expected[1:]):
        assert nodes[child]["depends_on"] == [parent]


def test_memory_is_not_admitted_before_transport() -> None:
    nodes = _nodes()
    assert nodes["TEMPORAL_TRANSPORT"]["status"] == "GATED"
    assert nodes["MEMORY"]["status"] == "PROVISIONAL_DOWNSTREAM_BRANCH"
