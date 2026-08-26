import numpy as np
import pytest

from src.idt.orchorbital import AttractorEvaluation, AttractorFieldState, AttractorResidence
from src.idt.orchorbital_hierarchy import (
    HierarchyNode,
    ORCHORBITALHierarchyError,
    coarse_grain_transition_counts,
    hierarchy_field_state,
    hierarchy_residence_summary,
)


def _nodes():
    return [
        HierarchyNode("ROOT", None),
        HierarchyNode("G1", "ROOT"),
        HierarchyNode("G2", "ROOT"),
        HierarchyNode("A", "G1"),
        HierarchyNode("B", "G1"),
        HierarchyNode("C", "G2"),
    ]


def _field():
    evaluations = (
        AttractorEvaluation("A", 1.0, -1.0, 1.0, 0.50),
        AttractorEvaluation("B", 1.0, -0.5, 0.5, 0.25),
        AttractorEvaluation("C", 1.0, -0.5, 0.5, 0.25),
    )
    return AttractorFieldState(evaluations, "A", False, 1.5, 1.0 - 1.5 / np.log2(3.0))


def test_hierarchy_aggregates_leaf_weights_and_active_path():
    state = hierarchy_field_state(_field(), _nodes())
    weights = {item.name: item.weight for item in state.weights}
    assert not state.leak_mode
    assert weights["ROOT"] == pytest.approx(1.0)
    assert weights["G1"] == pytest.approx(0.75)
    assert weights["G2"] == pytest.approx(0.25)
    assert state.active_leaf == "A"
    assert state.active_path == ("ROOT", "G1", "A")


def test_hierarchy_shannon_chain_rule_reconstructs_leaf_entropy():
    state = hierarchy_field_state(_field(), _nodes())
    audit = state.entropy
    assert audit is not None
    assert audit.leaf_entropy_bits == pytest.approx(1.5, abs=1e-12)
    assert audit.root_entropy_bits == pytest.approx(0.0, abs=1e-12)
    assert audit.reconstructed_leaf_entropy_bits == pytest.approx(1.5, abs=1e-12)
    assert audit.decomposition_error < 1e-12
    local = dict(audit.local_entropy_bits)
    assert local["ROOT"] == pytest.approx(0.8112781244591328, abs=1e-12)
    assert local["G1"] == pytest.approx(0.9182958340544896, abs=1e-12)
    assert local["G2"] == pytest.approx(0.0, abs=1e-12)


def test_leak_mode_propagates_through_hierarchy_without_entropy():
    field = AttractorFieldState(
        (
            AttractorEvaluation("A", 1.0, 1.0, 0.0, 0.0),
            AttractorEvaluation("B", 1.0, 1.0, 0.0, 0.0),
            AttractorEvaluation("C", 1.0, 1.0, 0.0, 0.0),
        ),
        None,
        True,
        None,
        None,
    )
    state = hierarchy_field_state(field, _nodes())
    assert state.leak_mode
    assert state.entropy is None
    assert state.active_path == tuple()
    assert all(item.weight == 0.0 for item in state.weights)


def test_residence_coarse_grains_to_parent_and_root():
    residence = [
        AttractorResidence("A", 2, 0.10, 0.25),
        AttractorResidence("B", 3, 0.20, -0.05),
        AttractorResidence("C", 4, 0.30, 0.40),
    ]
    summary = {item.name: item for item in hierarchy_residence_summary(residence, _nodes())}
    assert summary["G1"].dwell_tau == pytest.approx(0.30)
    assert summary["G1"].winding == pytest.approx(0.20)
    assert summary["G1"].leaf_segment_count == 5
    assert summary["ROOT"].dwell_tau == pytest.approx(0.60)
    assert summary["ROOT"].winding == pytest.approx(0.60)
    assert summary["ROOT"].leaf_segment_count == 9


def test_transition_graph_coarse_grains_across_hierarchy_cut():
    leaf_counts = {
        ("A", "C"): 2,
        ("B", "C"): 1,
        ("C", "A"): 4,
        ("A", "B"): 5,
    }
    coarse = coarse_grain_transition_counts(leaf_counts, _nodes(), ["A", "B", "C"], ["G1", "G2"])
    assert coarse == {("G1", "G2"): 3, ("G2", "G1"): 4}


def test_overlapping_hierarchy_cut_fails_closed():
    with pytest.raises(ORCHORBITALHierarchyError, match="overlap"):
        coarse_grain_transition_counts({}, _nodes(), ["A", "B", "C"], ["ROOT", "G1"])


def test_incomplete_hierarchy_cut_fails_closed():
    with pytest.raises(ORCHORBITALHierarchyError, match="partition"):
        coarse_grain_transition_counts({}, _nodes(), ["A", "B", "C"], ["G1"])


def test_hierarchy_cycle_fails_closed():
    nodes = [
        HierarchyNode("A", "B"),
        HierarchyNode("B", "A"),
    ]
    field = AttractorFieldState(
        (
            AttractorEvaluation("A", 1.0, -1.0, 1.0, 0.5),
            AttractorEvaluation("B", 1.0, -1.0, 1.0, 0.5),
        ),
        "A",
        False,
        1.0,
        0.0,
    )
    with pytest.raises(ORCHORBITALHierarchyError, match="cycle"):
        hierarchy_field_state(field, nodes)
