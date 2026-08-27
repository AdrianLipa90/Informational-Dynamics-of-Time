from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
GRAPH=ROOT/"validation"/"dependency_graph.json"
def _nodes(): return {n["id"]:n for n in json.loads(GRAPH.read_text())["nodes"]}
def test_dependency_graph_is_acyclic():
    nodes=_nodes(); visiting=set(); visited=set()
    def visit(i):
        if i in visited:return
        assert i not in visiting; visiting.add(i)
        for p in nodes[i]["depends_on"]: assert p in nodes; visit(p)
        visiting.remove(i); visited.add(i)
    for i in nodes: visit(i)
def test_declared_chain_matches_project_order():
    nodes=_nodes(); expected=["TIR","TEMPORAL_PRIMITIVE","TEMPORAL_WAVE","NOW","BIFURCATION","TEMPORAL_TRANSPORT","MEMORY","ORCHORBITAL_ATTRACTORS","RETRODICTION","RETROCAUSAL_TESTS","EINSTEIN_CLOSURE"]
    assert list(nodes)==expected
    for p,c in zip(expected,expected[1:]): assert nodes[c]["depends_on"]==[p]
def test_temporal_primitive_records_upstream_forcing_chain():
    status=_nodes()["TEMPORAL_PRIMITIVE"]["status"]
    for marker in ["RELATIONAL_TENSOR_SCALAR_FORCING_TARGETED_PASS","PHASE_CONNECTION_HOLONOMY_TARGETED_PASS","SHANNON_RELATIVE_INFORMATION_MONOTONICITY_TARGETED_PASS","SHANNON_ONSAGER_RESPONSE_TARGETED_PASS_CANDIDATE"]: assert marker in status
def test_downstream_frontier_markers_are_preserved():
    status=_nodes()["RETRODICTION"]["status"]
    for marker in ["SPATIAL_OFFSET_DIVERGENCE_WITNESS_FOUND","ADAPTIVE_SOD_SEPARATOR_TARGETED_PASS","GENERAL_GLOBAL_INJECTIVITY_OPEN","GATED_PENDING_MEMORY_ORCHORBITAL_ADMISSION"]: assert marker in status
