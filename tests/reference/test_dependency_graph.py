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
def test_memory_and_orchorbital_admission_markers_are_recorded():
    nodes=_nodes()
    for marker in ["REFERENCE_GATE_ADMITTED","HOSTED_FULL_SUITE_PASS"]: assert marker in nodes["MEMORY"]["status"]
    for marker in ["REFERENCE_GATE_ADMITTED","RESIDENCE_LEDGER_PASS","PNCS_HIERARCHY_PASS","TYPED_OBSERVABLES_PASS","HOSTED_FULL_SUITE_PASS"]: assert marker in nodes["ORCHORBITAL_ATTRACTORS"]["status"]
def test_downstream_frontier_markers_are_preserved():
    status=_nodes()["RETRODICTION"]["status"]
    for marker in ["SPATIAL_OFFSET_DIVERGENCE_WITNESS_FOUND","ADAPTIVE_SOD_SEPARATOR_TARGETED_PASS","EVENT_AWARE_RESIDENCE_CONDITIONING_PASS","RESIDENCE_LABEL_KNOWN_NULL_PERSISTENCE_PASS","PROVENANCE_FIREWALL_PASS","QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS","ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS","FIBER_LIFT_COMPOSITION_THEOREM_PASS","FINITE_DOMAIN_FIBER_LIFT_REFERENCE_PASS","STRATIFIED_GLOBAL_REDUCTION_PASS","CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_REFERENCE_PASS","PER_STRATUM_POSITION_DECODER_ACTIVE_NEXT_GATE","HOSTED_FULL_SUITE_PASS","GENERAL_GLOBAL_INJECTIVITY_OPEN","ORCHORBITAL_PARENT_ADMITTED_ON_PROMOTION_BRANCH"]: assert marker in status
