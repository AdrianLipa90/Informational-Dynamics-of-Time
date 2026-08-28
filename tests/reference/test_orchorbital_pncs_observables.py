import math

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorFieldState, ORCHORBITALStep
from src.idt.orchorbital_hierarchy import ORCHORBITALHierarchyError
from src.idt.orchorbital_pncs_hierarchy_binding import (
    PNCS_SOURCE_COMMIT,
    PNCSEntityAttractorBinding,
    PNCSHierarchyBindingSet,
    PNCSSphereNode,
)
from src.idt.orchorbital_pncs_observables import (
    ORCHORBITALTypedObservableFrame,
    PNCSReductionReadinessBinding,
    PNCSSemanticMassBinding,
    PNCSTruthScalarBinding,
    residence_weighted_semantic_mass,
    semantic_mass_bindings,
)
from src.idt.orchorbital_residence_ledger import build_residence_receipts


def _pid(kind: str, digit: str) -> str:
    return f"pncs:{kind}:sha256:{digit * 64}"


def _entity(
    name: str,
    digit: str,
    orbit_index: int,
    *,
    semantic_mass: float | None,
) -> PNCSEntityAttractorBinding:
    return PNCSEntityAttractorBinding(
        attractor_name=name,
        source_projection_id=_pid("entity-projection", digit),
        canonical_id=_pid("entity", digit),
        hierarchy_path_id=_pid("hierarchy-lineage", digit),
        sphere_id="ROOT",
        parent_sphere_id=None,
        orbit_index=orbit_index,
        phase=0.1 * (orbit_index + 1),
        semantic_mass=semantic_mass,
        mass_binding_id=None if semantic_mass is None else _pid("mass-binding", digit),
    )


def _binding_set(*, complete: bool = True) -> PNCSHierarchyBindingSet:
    return PNCSHierarchyBindingSet(
        spheres=(PNCSSphereNode("ROOT"),),
        entities=(
            _entity("A", "a", 0, semantic_mass=1.0),
            _entity("B", "b", 1, semantic_mass=3.0 if complete else None),
        ),
    )


def _state(tau: float, x: float) -> MemoryPhaseState:
    return MemoryPhaseState(
        np.array([x, 0.0], dtype=float),
        np.array([0.0, 0.5], dtype=float),
        float(tau),
        0.0,
    )


def _residence_receipts():
    labels = ("A", "A", "B")
    delta_taus = (1.0, 1.0, 2.0)
    steps = []
    current = _state(0.0, 1.0)
    for index, (active, delta_tau) in enumerate(zip(labels, delta_taus)):
        next_active = labels[index + 1] if index + 1 < len(labels) else active
        after = _state(current.tau_internal + delta_tau, 1.01 + 0.01 * index)
        steps.append(
            ORCHORBITALStep(
                state_before=current,
                state_after=after,
                field_before=AttractorFieldState((), active, False, 0.0, 1.0),
                field_after=AttractorFieldState((), next_active, False, 0.0, 1.0),
                active_attractor=active,
                winding_increment=0.01 * (index + 1),
                switched_after_segment=(next_active != active),
            )
        )
        current = after
    return build_residence_receipts(steps)


@pytest.mark.parametrize("truth", [None, 0.0, 0.5, 1.0])
def test_truth_scalar_accepts_exact_pncs_domain_and_closed_unit_interval(truth):
    binding = PNCSTruthScalarBinding(_pid("orch-observables", "1"), truth)
    assert binding.truth_scalar is None if truth is None else binding.truth_scalar == float(truth)


@pytest.mark.parametrize("truth", [-0.01, 1.01, math.nan, math.inf, True])
def test_truth_scalar_rejects_out_of_domain_values(truth):
    with pytest.raises(ORCHORBITALHierarchyError, match="truth_scalar"):
        PNCSTruthScalarBinding(_pid("orch-observables", "1"), truth)


def test_truth_scalar_rejects_wrong_typed_id_and_wrong_source_pin():
    with pytest.raises(ORCHORBITALHierarchyError, match="observables_id"):
        PNCSTruthScalarBinding(_pid("orch-state", "1"), 0.5)
    with pytest.raises(ORCHORBITALHierarchyError, match="pinned PNCS snapshot"):
        PNCSTruthScalarBinding(
            _pid("orch-observables", "1"),
            0.5,
            source_commit="0" * 40,
        )


def test_semantic_mass_bindings_extract_complete_pncs_projection_mass_pairs():
    masses = semantic_mass_bindings(_binding_set())
    assert [(item.attractor_name, item.semantic_mass) for item in masses] == [("A", 1.0), ("B", 3.0)]
    assert all(item.source_projection_id.startswith("pncs:entity-projection:sha256:") for item in masses)
    assert all(item.mass_binding_id.startswith("pncs:mass-binding:sha256:") for item in masses)


def test_semantic_mass_binding_complete_mode_fails_loud_and_partial_mode_preserves_available_mass():
    binding_set = _binding_set(complete=False)
    with pytest.raises(ORCHORBITALHierarchyError, match="complete semantic-mass binding required"):
        semantic_mass_bindings(binding_set, require_complete=True)
    partial = semantic_mass_bindings(binding_set, require_complete=False)
    assert [(item.attractor_name, item.semantic_mass) for item in partial] == [("A", 1.0)]


def test_reduction_readiness_is_exactly_bound_to_omega_threshold():
    ready = PNCSReductionReadinessBinding(
        reduction_decision_id=_pid("orch-reduction", "2"),
        kernel_id=_pid("orch-reduction-kernel", "3"),
        state_id=_pid("orch-state", "4"),
        omega=0.75,
        omega_crit=0.75,
        reduce_ready=True,
        relation_alignment=0.4,
        xi=0.1,
        selected_orbital_index=7,
    )
    blocked = PNCSReductionReadinessBinding(
        reduction_decision_id=_pid("orch-reduction", "5"),
        kernel_id=_pid("orch-reduction-kernel", "6"),
        state_id=_pid("orch-state", "7"),
        omega=0.749,
        omega_crit=0.75,
        reduce_ready=False,
        relation_alignment=0.4,
        xi=0.1,
    )
    assert ready.reduce_ready and ready.selected_orbital_index == 7
    assert blocked.reduce_ready is False and blocked.selected_orbital_index is None


def test_reduction_binding_rejects_threshold_mismatch_selection_before_ready_and_wrong_id_domains():
    common = dict(
        reduction_decision_id=_pid("orch-reduction", "2"),
        kernel_id=_pid("orch-reduction-kernel", "3"),
        state_id=_pid("orch-state", "4"),
        omega=0.5,
        omega_crit=0.75,
        relation_alignment=0.4,
        xi=0.1,
    )
    with pytest.raises(ORCHORBITALHierarchyError, match="omega threshold"):
        PNCSReductionReadinessBinding(**common, reduce_ready=True)
    with pytest.raises(ORCHORBITALHierarchyError, match="requires reduction-ready"):
        PNCSReductionReadinessBinding(**common, reduce_ready=False, selected_orbital_index=0)
    with pytest.raises(ORCHORBITALHierarchyError, match="invalid PNCS typed-ID domain"):
        PNCSReductionReadinessBinding(
            **{**common, "reduction_decision_id": _pid("orch-state", "2")},
            reduce_ready=False,
        )


def test_typed_observable_frame_preserves_truth_reduction_and_mass_as_separate_carriers():
    truth = PNCSTruthScalarBinding(_pid("orch-observables", "1"), 0.8)
    reduction = PNCSReductionReadinessBinding(
        reduction_decision_id=_pid("orch-reduction", "2"),
        kernel_id=_pid("orch-reduction-kernel", "3"),
        state_id=_pid("orch-state", "4"),
        omega=0.9,
        omega_crit=0.8,
        reduce_ready=True,
        relation_alignment=0.6,
        xi=0.2,
        selected_orbital_index=3,
    )
    masses = semantic_mass_bindings(_binding_set())
    frame = ORCHORBITALTypedObservableFrame(truth, reduction, masses)
    assert frame.truth.truth_scalar == 0.8
    assert frame.reduction.omega == 0.9
    assert {item.attractor_name: item.semantic_mass for item in frame.semantic_masses} == {"A": 1.0, "B": 3.0}


def test_residence_weighted_semantic_mass_uses_exact_lineage_dwell_weights():
    masses = semantic_mass_bindings(_binding_set())
    value = residence_weighted_semantic_mass(_residence_receipts(), masses)
    assert value == pytest.approx(2.0, abs=1e-15)


def test_residence_weighted_semantic_mass_fails_when_active_attractor_mass_is_missing():
    masses = (PNCSSemanticMassBinding("A", _pid("entity-projection", "a"), 1.0, _pid("mass-binding", "a")),)
    with pytest.raises(ORCHORBITALHierarchyError, match="lacks semantic mass"):
        residence_weighted_semantic_mass(_residence_receipts(), masses)


def test_observable_source_pin_matches_hierarchy_source_commit():
    binding = PNCSTruthScalarBinding(_pid("orch-observables", "1"), 0.5)
    assert binding.source_commit == PNCS_SOURCE_COMMIT
