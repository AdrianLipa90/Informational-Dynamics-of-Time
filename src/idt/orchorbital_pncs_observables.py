from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Sequence

from .orchorbital_hierarchy import ORCHORBITALHierarchyError
from .orchorbital_pncs_hierarchy_binding import (
    PNCS_SOURCE_COMMIT,
    PNCS_SOURCE_REPOSITORY,
    PNCSHierarchyBindingSet,
    entity_binding_for_attractor,
)
from .orchorbital_residence_ledger import ORCHORBITALResidenceReceipt, verify_residence_receipts


PNCS_OBSERVABLE_SOURCE_FILE = "src/phasenav_natural_code/orch_orbital_core_v27.py"
PNCS_REDUCTION_SOURCE_FILE = "src/phasenav_natural_code/orch_orbital_reduction_v27.py"
PNCS_OBSERVABLE_CONTRACT = "PNCS_ORCHORBITAL_BINDING_V0_27"

_OBSERVABLE_ID_RE = re.compile(r"^pncs:orch-observables:sha256:[0-9a-f]{64}$")
_STATE_ID_RE = re.compile(r"^pncs:orch-state:sha256:[0-9a-f]{64}$")
_REDUCTION_ID_RE = re.compile(r"^pncs:orch-reduction:sha256:[0-9a-f]{64}$")
_KERNEL_ID_RE = re.compile(r"^pncs:orch-reduction-kernel:sha256:[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class PNCSTruthScalarBinding:
    observables_id: str
    truth_scalar: float | None
    source_repository: str = PNCS_SOURCE_REPOSITORY
    source_commit: str = PNCS_SOURCE_COMMIT
    source_file: str = PNCS_OBSERVABLE_SOURCE_FILE
    source_contract: str = PNCS_OBSERVABLE_CONTRACT

    def __post_init__(self) -> None:
        if type(self.observables_id) is not str or not _OBSERVABLE_ID_RE.fullmatch(self.observables_id):
            raise ORCHORBITALHierarchyError("observables_id must be a PNCS orch-observables SHA-256 ID")
        if self.truth_scalar is not None:
            if isinstance(self.truth_scalar, bool) or not isinstance(self.truth_scalar, (int, float)):
                raise ORCHORBITALHierarchyError("truth_scalar must be null or finite in [0,1]")
            value = float(self.truth_scalar)
            if not math.isfinite(value) or value < 0.0 or value > 1.0:
                raise ORCHORBITALHierarchyError("truth_scalar must be null or finite in [0,1]")
            object.__setattr__(self, "truth_scalar", value)
        if self.source_repository != PNCS_SOURCE_REPOSITORY or self.source_commit != PNCS_SOURCE_COMMIT:
            raise ORCHORBITALHierarchyError("truth scalar source differs from pinned PNCS snapshot")
        if self.source_file != PNCS_OBSERVABLE_SOURCE_FILE or self.source_contract != PNCS_OBSERVABLE_CONTRACT:
            raise ORCHORBITALHierarchyError("truth scalar source contract differs from pinned PNCS source")


@dataclass(frozen=True, slots=True)
class PNCSSemanticMassBinding:
    attractor_name: str
    source_projection_id: str
    semantic_mass: float
    mass_binding_id: str

    def __post_init__(self) -> None:
        if type(self.attractor_name) is not str or not self.attractor_name.strip():
            raise ORCHORBITALHierarchyError("semantic-mass attractor_name must be non-empty")
        if type(self.source_projection_id) is not str or not self.source_projection_id.startswith("pncs:entity-projection:sha256:"):
            raise ORCHORBITALHierarchyError("semantic mass requires PNCS entity-projection provenance")
        if len(self.source_projection_id) != len("pncs:entity-projection:sha256:") + 64:
            raise ORCHORBITALHierarchyError("semantic mass source_projection_id must carry 64 hex digits")
        suffix = self.source_projection_id.rsplit(":", 1)[-1]
        if any(ch not in "0123456789abcdef" for ch in suffix):
            raise ORCHORBITALHierarchyError("semantic mass source_projection_id must carry lowercase hex")
        if isinstance(self.semantic_mass, bool) or not isinstance(self.semantic_mass, (int, float)):
            raise ORCHORBITALHierarchyError("semantic_mass must be finite and non-negative")
        mass = float(self.semantic_mass)
        if not math.isfinite(mass) or mass < 0.0:
            raise ORCHORBITALHierarchyError("semantic_mass must be finite and non-negative")
        object.__setattr__(self, "semantic_mass", mass)
        if type(self.mass_binding_id) is not str or not self.mass_binding_id.startswith("pncs:mass-binding:sha256:"):
            raise ORCHORBITALHierarchyError("mass_binding_id must be a PNCS mass-binding SHA-256 ID")
        if len(self.mass_binding_id) != len("pncs:mass-binding:sha256:") + 64:
            raise ORCHORBITALHierarchyError("mass_binding_id must carry 64 hex digits")
        suffix = self.mass_binding_id.rsplit(":", 1)[-1]
        if any(ch not in "0123456789abcdef" for ch in suffix):
            raise ORCHORBITALHierarchyError("mass_binding_id must carry lowercase hex")


@dataclass(frozen=True, slots=True)
class PNCSReductionReadinessBinding:
    reduction_decision_id: str
    kernel_id: str
    state_id: str
    omega: float
    omega_crit: float
    reduce_ready: bool
    relation_alignment: float
    xi: float
    selected_orbital_index: int | None = None
    source_repository: str = PNCS_SOURCE_REPOSITORY
    source_commit: str = PNCS_SOURCE_COMMIT
    source_file: str = PNCS_REDUCTION_SOURCE_FILE

    def __post_init__(self) -> None:
        for label, value, pattern in (
            ("reduction_decision_id", self.reduction_decision_id, _REDUCTION_ID_RE),
            ("kernel_id", self.kernel_id, _KERNEL_ID_RE),
            ("state_id", self.state_id, _STATE_ID_RE),
        ):
            if type(value) is not str or not pattern.fullmatch(value):
                raise ORCHORBITALHierarchyError(f"{label} has invalid PNCS typed-ID domain")
        for label in ("omega", "omega_crit", "relation_alignment", "xi"):
            value = getattr(self, label)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ORCHORBITALHierarchyError(f"{label} must be finite")
            value = float(value)
            if not math.isfinite(value):
                raise ORCHORBITALHierarchyError(f"{label} must be finite")
            object.__setattr__(self, label, value)
        if type(self.reduce_ready) is not bool:
            raise ORCHORBITALHierarchyError("reduce_ready must be boolean")
        expected = self.omega >= self.omega_crit
        if self.reduce_ready != expected:
            raise ORCHORBITALHierarchyError("reduce_ready disagrees with omega threshold")
        if self.selected_orbital_index is not None:
            if type(self.selected_orbital_index) is not int or isinstance(self.selected_orbital_index, bool) or self.selected_orbital_index < 0:
                raise ORCHORBITALHierarchyError("selected_orbital_index must be null or a non-negative integer")
            if not self.reduce_ready:
                raise ORCHORBITALHierarchyError("selected orbital requires reduction-ready state")
        if self.source_repository != PNCS_SOURCE_REPOSITORY or self.source_commit != PNCS_SOURCE_COMMIT:
            raise ORCHORBITALHierarchyError("reduction source differs from pinned PNCS snapshot")
        if self.source_file != PNCS_REDUCTION_SOURCE_FILE:
            raise ORCHORBITALHierarchyError("reduction source file differs from pinned PNCS source")


@dataclass(frozen=True, slots=True)
class ORCHORBITALTypedObservableFrame:
    truth: PNCSTruthScalarBinding
    reduction: PNCSReductionReadinessBinding
    semantic_masses: tuple[PNCSSemanticMassBinding, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.truth, PNCSTruthScalarBinding):
            raise ORCHORBITALHierarchyError("truth must be PNCSTruthScalarBinding")
        if not isinstance(self.reduction, PNCSReductionReadinessBinding):
            raise ORCHORBITALHierarchyError("reduction must be PNCSReductionReadinessBinding")
        if any(not isinstance(item, PNCSSemanticMassBinding) for item in self.semantic_masses):
            raise ORCHORBITALHierarchyError("semantic_masses must contain PNCSSemanticMassBinding values")
        names = [item.attractor_name for item in self.semantic_masses]
        if len(set(names)) != len(names):
            raise ORCHORBITALHierarchyError("semantic mass attractor bindings must be unique")


def semantic_mass_bindings(
    binding_set: PNCSHierarchyBindingSet,
    *,
    require_complete: bool = True,
) -> tuple[PNCSSemanticMassBinding, ...]:
    if type(require_complete) is not bool:
        raise ORCHORBITALHierarchyError("require_complete must be boolean")
    out: list[PNCSSemanticMassBinding] = []
    missing: list[str] = []
    for entity in binding_set.entities:
        if entity.semantic_mass is None or entity.mass_binding_id is None:
            missing.append(entity.attractor_name)
            continue
        out.append(
            PNCSSemanticMassBinding(
                attractor_name=entity.attractor_name,
                source_projection_id=entity.source_projection_id,
                semantic_mass=entity.semantic_mass,
                mass_binding_id=entity.mass_binding_id,
            )
        )
    if require_complete and missing:
        raise ORCHORBITALHierarchyError(
            "complete semantic-mass binding required for attractors: " + ",".join(sorted(missing))
        )
    return tuple(out)


def residence_weighted_semantic_mass(
    receipts: Sequence[ORCHORBITALResidenceReceipt],
    masses: Sequence[PNCSSemanticMassBinding],
) -> float:
    verify_residence_receipts(receipts)
    mass_map = {item.attractor_name: item.semantic_mass for item in masses}
    if len(mass_map) != len(tuple(masses)):
        raise ORCHORBITALHierarchyError("semantic mass bindings must have unique attractor names")
    total_tau = 0.0
    weighted_mass = 0.0
    for receipt in receipts:
        if receipt.active_attractor not in mass_map:
            raise ORCHORBITALHierarchyError("residence lineage lacks semantic mass for active attractor")
        total_tau += receipt.delta_tau
        weighted_mass += receipt.delta_tau * mass_map[receipt.active_attractor]
    if not math.isfinite(total_tau) or total_tau <= 0.0:
        raise ORCHORBITALHierarchyError("residence lineage must carry positive finite dwell time")
    result = weighted_mass / total_tau
    if not math.isfinite(result) or result < 0.0:
        raise ORCHORBITALHierarchyError("residence-weighted semantic mass must be finite and non-negative")
    return float(result)
