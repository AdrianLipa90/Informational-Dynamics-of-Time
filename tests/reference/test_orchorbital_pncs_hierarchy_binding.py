import numpy as np
import pytest

from src.idt.orchorbital import AttractorEvaluation, AttractorFieldState
from src.idt.orchorbital_hierarchy import ORCHORBITALHierarchyError, hierarchy_field_state
from src.idt.orchorbital_pncs_hierarchy_binding import (
    PNCS_SOURCE_COMMIT,
    PNCS_SOURCE_CONTRACT,
    PNCS_SOURCE_REPOSITORY,
    PNCSEntityAttractorBinding,
    PNCSHierarchyBindingSet,
    PNCSSphereNode,
    attractor_path,
    hierarchy_nodes_from_pncs,
    ordered_entities_in_sphere,
    validate_exact_attractor_coverage,
)


def pid(kind, digit):
    return f"pncs:{kind}:sha256:{digit * 64}"


def entity(name, sphere, parent, orbit, phase, digit, **kwargs):
    return PNCSEntityAttractorBinding(
        attractor_name=name,
        source_projection_id=pid("entity-projection", digit),
        canonical_id=pid("result", digit),
        hierarchy_path_id=pid("hierarchy-lineage", digit),
        sphere_id=sphere,
        parent_sphere_id=parent,
        orbit_index=orbit,
        phase=phase,
        **kwargs,
    )


def binding_set():
    return PNCSHierarchyBindingSet(
        spheres=(
            PNCSSphereNode("ROOT", None),
            PNCSSphereNode("G1", "ROOT"),
            PNCSSphereNode("G2", "ROOT"),
        ),
        entities=(
            entity("A", "G1", "ROOT", 1, 0.4, "1"),
            entity("B", "G1", "ROOT", 0, 0.8, "2"),
            entity("C", "G2", "ROOT", 0, 0.2, "3"),
        ),
    )


def field():
    return AttractorFieldState(
        (
            AttractorEvaluation("A", 1.0, -1.0, 1.0, 0.50),
            AttractorEvaluation("B", 1.0, -0.5, 0.5, 0.25),
            AttractorEvaluation("C", 1.0, -0.5, 0.5, 0.25),
        ),
        "A",
        False,
        1.5,
        1.0 - 1.5 / np.log2(3.0),
    )


def test_binding_pins_exact_upstream_pncs_v029_source():
    data = binding_set()
    assert data.source_repository == PNCS_SOURCE_REPOSITORY == "AdrianLipa90/PhaseNav-Natural-Coding-System"
    assert data.source_commit == PNCS_SOURCE_COMMIT == "7a54596c1794be29e0b85f5c363213cc81eb87d7"
    assert data.source_contract == PNCS_SOURCE_CONTRACT == "PNCS_ORCHORBITAL_HARVEST_HARDENING_V0_29"


def test_pncs_binding_generates_existing_idt_hierarchy_without_second_semantics():
    data = binding_set()
    nodes = hierarchy_nodes_from_pncs(data)
    state = hierarchy_field_state(field(), nodes)
    assert state.active_path == ("ROOT", "G1", "A")
    weights = {item.name: item.weight for item in state.weights}
    assert weights["ROOT"] == pytest.approx(1.0)
    assert weights["G1"] == pytest.approx(0.75)
    assert weights["G2"] == pytest.approx(0.25)
    assert attractor_path(data, "A") == ("ROOT", "G1", "A")


def test_binding_requires_exact_dynamic_attractor_leaf_coverage():
    data = binding_set()
    validate_exact_attractor_coverage(["A", "B", "C"], data)
    with pytest.raises(ORCHORBITALHierarchyError, match="exactly cover"):
        validate_exact_attractor_coverage(["A", "B"], data)


def test_entity_parent_must_match_declared_sphere_parent():
    with pytest.raises(ORCHORBITALHierarchyError, match="disagrees"):
        PNCSHierarchyBindingSet(
            spheres=(PNCSSphereNode("ROOT"), PNCSSphereNode("G1", "ROOT")),
            entities=(entity("A", "G1", None, 0, 0.1, "1"),),
        )


def test_typed_pncs_identity_domains_fail_closed():
    with pytest.raises(ORCHORBITALHierarchyError, match="entity-projection"):
        PNCSEntityAttractorBinding(
            attractor_name="A",
            source_projection_id=pid("result", "1"),
            canonical_id=pid("result", "2"),
            hierarchy_path_id=pid("hierarchy-lineage", "3"),
            sphere_id="G1",
            parent_sphere_id="ROOT",
            orbit_index=0,
            phase=0.1,
        )
    with pytest.raises(ORCHORBITALHierarchyError, match="hierarchy-lineage"):
        PNCSEntityAttractorBinding(
            attractor_name="A",
            source_projection_id=pid("entity-projection", "1"),
            canonical_id=pid("result", "2"),
            hierarchy_path_id=pid("result", "3"),
            sphere_id="G1",
            parent_sphere_id="ROOT",
            orbit_index=0,
            phase=0.1,
        )


def test_semantic_mass_requires_exact_mass_binding_pair():
    with pytest.raises(ORCHORBITALHierarchyError, match="supplied together"):
        entity("A", "G1", "ROOT", 0, 0.1, "1", semantic_mass=0.25)
    value = entity(
        "A",
        "G1",
        "ROOT",
        0,
        0.1,
        "1",
        semantic_mass=0.25,
        mass_binding_id=pid("mass-binding", "9"),
    )
    assert value.semantic_mass == pytest.approx(0.25)
    assert value.mass_binding_id == pid("mass-binding", "9")


def test_orbit_index_is_unique_inside_each_sphere_and_order_is_replay_stable():
    data = binding_set()
    ordered = ordered_entities_in_sphere(data, "G1")
    assert [item.attractor_name for item in ordered] == ["B", "A"]

    with pytest.raises(ORCHORBITALHierarchyError, match="duplicate orbit_index"):
        PNCSHierarchyBindingSet(
            spheres=(PNCSSphereNode("ROOT"), PNCSSphereNode("G1", "ROOT")),
            entities=(
                entity("A", "G1", "ROOT", 0, 0.1, "1"),
                entity("B", "G1", "ROOT", 0, 0.2, "2"),
            ),
        )


def test_pinned_source_fields_are_fail_closed():
    data = binding_set()
    with pytest.raises(ORCHORBITALHierarchyError, match="source commit"):
        PNCSHierarchyBindingSet(data.spheres, data.entities, source_commit="0" * 40)
