from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _nodes():
    return {n["id"]: n for n in json.loads(GRAPH.read_text())["nodes"]}


def test_dependency_graph_is_acyclic():
    nodes = _nodes()
    visiting = set()
    visited = set()

    def visit(i):
        if i in visited:
            return
        assert i not in visiting
        visiting.add(i)
        for parent in nodes[i]["depends_on"]:
            assert parent in nodes
            visit(parent)
        visiting.remove(i)
        visited.add(i)

    for i in nodes:
        visit(i)


def test_declared_temporal_spine_preserves_project_order():
    nodes = _nodes()
    spine = [
        "TIR",
        "TEMPORAL_PRIMITIVE",
        "RELATIONAL_PRECEDENCE",
        "NOW",
        "BIFURCATION",
        "TEMPORAL_TRANSPORT",
        "MEMORY",
        "ORCHORBITAL_ATTRACTORS",
        "RETRODICTION",
        "RETROCAUSAL_TESTS",
        "EINSTEIN_CLOSURE",
    ]
    order = list(nodes)
    positions = [order.index(node) for node in spine]
    assert positions == sorted(positions)
    for parent, child in zip(spine, spine[1:]):
        assert parent in nodes[child]["depends_on"]

    assert nodes["TEMPORAL_WAVE"]["depends_on"] == ["TEMPORAL_PRIMITIVE"]
    assert "TEMPORAL_WAVE" in nodes["NOW"]["depends_on"]


def test_relativistic_bridge_is_an_explicit_parallel_einstein_prerequisite():
    nodes = _nodes()
    assert nodes["GAUGE_COVARIANT_NOETHER_SOURCE"]["depends_on"] == ["TEMPORAL_PRIMITIVE"]
    assert nodes["RELATIVISTIC_FIELD_BRIDGE"]["depends_on"] == ["GAUGE_COVARIANT_NOETHER_SOURCE"]
    assert "RELATIVISTIC_FIELD_BRIDGE" in nodes["EINSTEIN_CLOSURE"]["depends_on"]


def test_temporal_primitive_records_upstream_forcing_chain():
    status = _nodes()["TEMPORAL_PRIMITIVE"]["status"]
    for marker in [
        "ACTIVITY_DERIVED_INTRINSIC_TEMPORAL_MEASURE_ALGEBRAIC_REFERENCE_PASS",
        "EXTENSIVE_ORIENTATION_EVEN_DENSITY_UNIQUENESS_THEOREM_PASS",
        "REPARAMETERIZATION_INVARIANT_DURATION_PASS",
        "DURATION_ORIENTATION_SEPARATION_PASS",
        "RELATIONAL_LAPSE_ACTIVITY_RATIO_PASS",
        "HOSTED_REFERENCE_SUITE_576_OF_576",
        "RELATIONAL_TENSOR_SCALAR_FORCING_TARGETED_PASS",
        "PHASE_CONNECTION_HOLONOMY_TARGETED_PASS",
        "SHANNON_RELATIVE_INFORMATION_MONOTONICITY_TARGETED_PASS",
        "SHANNON_ONSAGER_RESPONSE_TARGETED_PASS_CANDIDATE",
    ]:
        assert marker in status


def test_relational_precedence_and_now_markers_are_recorded():
    nodes = _nodes()
    assert nodes["RELATIONAL_PRECEDENCE"]["depends_on"] == ["TEMPORAL_PRIMITIVE"]
    precedence_status = nodes["RELATIONAL_PRECEDENCE"]["status"]
    for marker in [
        "RELATIONAL_COMPOSITION_PREFIX_OCCURRENCE_ORDER_ALGEBRAIC_REFERENCE_PASS",
        "POSITIVE_THETA_ORDER_EMBEDDING_PASS",
        "STATE_RECURRENCE_WITHOUT_OCCURRENCE_ORDER_CYCLE_PASS",
        "SERIAL_NOW_UNIQUE_MAXIMUM_PASS",
        "CONCURRENT_NOW_MAXIMAL_ANTICHAIN_PASS",
        "TRANSITIVE_FRONTIER_PASS",
        "HOSTED_REFERENCE_SUITE_589_OF_589",
    ]:
        assert marker in precedence_status

    assert set(nodes["NOW"]["depends_on"]) == {"TEMPORAL_WAVE", "RELATIONAL_PRECEDENCE"}
    now_status = nodes["NOW"]["status"]
    assert "RELATIONAL_MAXIMAL_REALIZED_EVENT_FRONTIER_ALGEBRAIC_REFERENCE_PASS" in now_status
    assert "SERIAL_UNIQUE_CONCURRENT_ANTICHAIN_PASS" in now_status


def test_temporal_wave_records_zeta_collatz_frame_and_null_control_status():
    status = _nodes()["TEMPORAL_WAVE"]["status"]
    for marker in [
        "ZETA_COLLATZ_FRAME_ALGEBRAIC_REFERENCE_PASS",
        "ZETA_PRIME_LOG_GENERATOR_PASS",
        "SCHRODINGER_DERIVED_THETA_FUZZINESS_PASS",
        "FIRST_MERGE_LOCALITY_PASS",
        "SPARSE_ZETA_ORDERED_COLLATZ_PATH_PASS",
        "PRIME_PATH_LOW_MODE_HOMOGENIZATION_PASS",
        "COMPOSITE_PATH_HOMOGENIZATION_NULL_PASS",
        "RANDOMIZED_ORDER_NULL_PASS",
        "PRIME_SPECIFIC_CONTINUUM_DISCRIMINATOR_OPEN",
        "JOINT_ZETA_FREQUENCY_COLLATZ_DISCRIMINATOR_PASS",
        "LOW_PRIME_JOINT_ALIGNMENT_WITNESS_PASS",
        "MARGINAL_PRESERVING_PERMUTATION_CONTROL_PASS",
        "BULK_WINDOW_STABILITY_FAIL",
        "PRIME_BULK_ALIGNMENT_PROMOTION_OPEN",
        "FROZEN_ZETA_ZERO_FIXTURE_PASS",
        "EXACT_UNIT_MODULUS_PRIME_GAP_PHASE_PASS",
        "SYMMETRIC_LOCAL_OFF_ZERO_CONTROL_PASS",
        "BULK_ZETA_ZERO_PHASE_SPECIALITY_FAIL_TO_DISCRIMINATE",
        "EXACT_ZETA_VERTEX_GRADIENT_PASS",
        "CLOSED_GRADIENT_HOLONOMY_TRIVIAL_THEOREM_PASS",
        "EDGE_NATIVE_NONEXACT_ZETA_COLLATZ_CONNECTION_ACTIVE_NEXT_GATE",
        "HOSTED_REFERENCE_SUITE_621_OF_621",
    ]:
        assert marker in status


def test_memory_and_orchorbital_admission_markers_are_recorded():
    nodes = _nodes()
    for marker in ["REFERENCE_GATE_ADMITTED", "HOSTED_FULL_SUITE_PASS"]:
        assert marker in nodes["MEMORY"]["status"]
    for marker in [
        "REFERENCE_GATE_ADMITTED",
        "RESIDENCE_LEDGER_PASS",
        "PNCS_HIERARCHY_PASS",
        "TYPED_OBSERVABLES_PASS",
        "HOSTED_FULL_SUITE_PASS",
    ]:
        assert marker in nodes["ORCHORBITAL_ATTRACTORS"]["status"]


def test_downstream_frontier_markers_are_preserved():
    nodes = _nodes()
    status = nodes["RETRODICTION"]["status"]
    for marker in [
        "SPATIAL_OFFSET_DIVERGENCE_WITNESS_FOUND",
        "ADAPTIVE_SOD_SEPARATOR_TARGETED_PASS",
        "EVENT_AWARE_RESIDENCE_CONDITIONING_PASS",
        "RESIDENCE_LABEL_KNOWN_NULL_PERSISTENCE_PASS",
        "PROVENANCE_FIREWALL_PASS",
        "QUOTIENT_FIBER_FINITE_DOMAIN_GATE_PASS",
        "ORIENTED_WINDING_KNOWN_NULL_SEPARATOR_PASS",
        "FIBER_LIFT_COMPOSITION_THEOREM_PASS",
        "FINITE_DOMAIN_FIBER_LIFT_REFERENCE_PASS",
        "STRATIFIED_GLOBAL_REDUCTION_PASS",
        "CONSTRUCTIVE_FIXED_SEQUENCE_POSITION_LIFT_REFERENCE_PASS",
        "EXACT_PER_STRATUM_POSITION_DECODER_BASELINE_PASS",
        "FULL_POSITION_FIBER_PACKET_SUFFICIENCY_PASS",
        "07K_NDARRAY_CARRIER_INTERFACE_PASS",
        "POSITION_FIBER_COMPRESSION_PASS",
        "EXACT_WINDING_RADIUS_POSITION_DECODER_PASS",
        "POSITION_FIBER_NEW_SCALAR_BUDGET_HALVED",
        "CONDITIONAL_AUGMENTED_WINDING_RADIUS_RECONSTRUCTION_PASS",
        "RADIAL_PACKET_RESIDENCE_BINDING_PASS",
        "RESIDENCE_BOUND_WINDING_RADIUS_CARRIER_PASS",
        "AUGMENTED_GLOBAL_DOMAIN_COVERAGE_ACTIVE_NEXT_GATE",
        "HOSTED_FULL_SUITE_PASS",
        "GENERAL_GLOBAL_INJECTIVITY_OPEN",
        "ORCHORBITAL_PARENT_ADMITTED",
    ]:
        assert marker in status
    retro_status = nodes["RETROCAUSAL_TESTS"]["status"]
    assert "PREREGISTRATION_PREPARATION_ALLOWED" in retro_status
    assert "EXECUTION_AND_PHYSICAL_CLAIM_GATE_GATED" in retro_status
