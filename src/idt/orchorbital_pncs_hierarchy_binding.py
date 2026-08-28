from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Sequence

from .orchorbital_hierarchy import HierarchyNode, ORCHORBITALHierarchyError


PNCS_SOURCE_REPOSITORY = "AdrianLipa90/PhaseNav-Natural-Coding-System"
PNCS_SOURCE_COMMIT = "7a54596c1794be29e0b85f5c363213cc81eb87d7"
PNCS_SOURCE_CONTRACT = "PNCS_ORCHORBITAL_HARVEST_HARDENING_V0_29"
TAU = 2.0 * math.pi

_TYPED_ID_RE = re.compile(r"^pncs:[a-z0-9-]+:sha256:[0-9a-f]{64}$")
_PROJECTION_ID_RE = re.compile(r"^pncs:entity-projection:sha256:[0-9a-f]{64}$")
_HIERARCHY_ID_RE = re.compile(r"^pncs:hierarchy-lineage:sha256:[0-9a-f]{64}$")
_MASS_BINDING_ID_RE = re.compile(r"^pncs:mass-binding:sha256:[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class PNCSSphereNode:
    sphere_id: str
    parent_sphere_id: str | None = None

    def __post_init__(self) -> None:
        if type(self.sphere_id) is not str or not self.sphere_id.strip():
            raise ORCHORBITALHierarchyError("sphere_id must be a non-empty string")
        if self.parent_sphere_id is not None:
            if type(self.parent_sphere_id) is not str or not self.parent_sphere_id.strip():
                raise ORCHORBITALHierarchyError("parent_sphere_id must be null or a non-empty string")
            if self.parent_sphere_id == self.sphere_id:
                raise ORCHORBITALHierarchyError("sphere cannot parent itself")


@dataclass(frozen=True, slots=True)
class PNCSEntityAttractorBinding:
    attractor_name: str
    source_projection_id: str
    canonical_id: str
    hierarchy_path_id: str
    sphere_id: str
    parent_sphere_id: str | None
    orbit_index: int
    phase: float
    semantic_mass: float | None = None
    mass_binding_id: str | None = None

    def __post_init__(self) -> None:
        if type(self.attractor_name) is not str or not self.attractor_name.strip():
            raise ORCHORBITALHierarchyError("attractor_name must be a non-empty string")
        if type(self.source_projection_id) is not str or not _PROJECTION_ID_RE.fullmatch(self.source_projection_id):
            raise ORCHORBITALHierarchyError("source_projection_id must be a PNCS entity-projection SHA-256 ID")
        if type(self.canonical_id) is not str or not _TYPED_ID_RE.fullmatch(self.canonical_id):
            raise ORCHORBITALHierarchyError("canonical_id must be a typed PNCS SHA-256 ID")
        if type(self.hierarchy_path_id) is not str or not _HIERARCHY_ID_RE.fullmatch(self.hierarchy_path_id):
            raise ORCHORBITALHierarchyError("hierarchy_path_id must be a PNCS hierarchy-lineage SHA-256 ID")
        if type(self.sphere_id) is not str or not self.sphere_id.strip():
            raise ORCHORBITALHierarchyError("binding sphere_id must be a non-empty string")
        if self.parent_sphere_id is not None and (
            type(self.parent_sphere_id) is not str or not self.parent_sphere_id.strip()
        ):
            raise ORCHORBITALHierarchyError("binding parent_sphere_id must be null or a non-empty string")
        if type(self.orbit_index) is not int or isinstance(self.orbit_index, bool) or self.orbit_index < 0:
            raise ORCHORBITALHierarchyError("orbit_index must be a non-negative integer")
        if isinstance(self.phase, bool) or not isinstance(self.phase, (int, float)):
            raise ORCHORBITALHierarchyError("phase must be finite in [0, 2pi)")
        phase = float(self.phase)
        if not math.isfinite(phase) or phase < 0.0 or phase >= TAU:
            raise ORCHORBITALHierarchyError("phase must be finite in [0, 2pi)")
        object.__setattr__(self, "phase", phase)

        if (self.semantic_mass is None) != (self.mass_binding_id is None):
            raise ORCHORBITALHierarchyError("semantic_mass and mass_binding_id must be supplied together")
        if self.semantic_mass is not None:
            if isinstance(self.semantic_mass, bool) or not isinstance(self.semantic_mass, (int, float)):
                raise ORCHORBITALHierarchyError("semantic_mass must be finite and non-negative")
            mass = float(self.semantic_mass)
            if not math.isfinite(mass) or mass < 0.0:
                raise ORCHORBITALHierarchyError("semantic_mass must be finite and non-negative")
            object.__setattr__(self, "semantic_mass", mass)
            if type(self.mass_binding_id) is not str or not _MASS_BINDING_ID_RE.fullmatch(self.mass_binding_id):
                raise ORCHORBITALHierarchyError("mass_binding_id must be a PNCS mass-binding SHA-256 ID")


@dataclass(frozen=True, slots=True)
class PNCSHierarchyBindingSet:
    spheres: tuple[PNCSSphereNode, ...]
    entities: tuple[PNCSEntityAttractorBinding, ...]
    source_repository: str = PNCS_SOURCE_REPOSITORY
    source_commit: str = PNCS_SOURCE_COMMIT
    source_contract: str = PNCS_SOURCE_CONTRACT

    def __post_init__(self) -> None:
        if not self.spheres:
            raise ORCHORBITALHierarchyError("PNCS hierarchy binding requires at least one sphere")
        if not self.entities:
            raise ORCHORBITALHierarchyError("PNCS hierarchy binding requires at least one entity")
        if any(not isinstance(item, PNCSSphereNode) for item in self.spheres):
            raise ORCHORBITALHierarchyError("spheres must contain PNCSSphereNode values")
        if any(not isinstance(item, PNCSEntityAttractorBinding) for item in self.entities):
            raise ORCHORBITALHierarchyError("entities must contain PNCSEntityAttractorBinding values")
        if self.source_repository != PNCS_SOURCE_REPOSITORY:
            raise ORCHORBITALHierarchyError("source repository differs from pinned PNCS source")
        if self.source_commit != PNCS_SOURCE_COMMIT:
            raise ORCHORBITALHierarchyError("source commit differs from pinned PNCS source")
        if self.source_contract != PNCS_SOURCE_CONTRACT:
            raise ORCHORBITALHierarchyError("source contract differs from pinned PNCS source")
        _validate_binding_set(self.spheres, self.entities)


def _validate_binding_set(
    spheres: Sequence[PNCSSphereNode],
    entities: Sequence[PNCSEntityAttractorBinding],
) -> None:
    sphere_map: dict[str, PNCSSphereNode] = {}
    for sphere in spheres:
        if sphere.sphere_id in sphere_map:
            raise ORCHORBITALHierarchyError("duplicate sphere_id in PNCS hierarchy binding")
        sphere_map[sphere.sphere_id] = sphere

    roots = 0
    for sphere in spheres:
        if sphere.parent_sphere_id is None:
            roots += 1
        elif sphere.parent_sphere_id not in sphere_map:
            raise ORCHORBITALHierarchyError("PNCS hierarchy contains dangling parent_sphere_id")
    if roots < 1:
        raise ORCHORBITALHierarchyError("PNCS hierarchy requires at least one root sphere")

    for sphere_id in sphere_map:
        seen: set[str] = set()
        cursor: str | None = sphere_id
        while cursor is not None:
            if cursor in seen:
                raise ORCHORBITALHierarchyError("PNCS sphere hierarchy contains a cycle")
            seen.add(cursor)
            cursor = sphere_map[cursor].parent_sphere_id

    names: set[str] = set()
    projections: set[str] = set()
    canonical_ids: set[str] = set()
    orbit_slots: set[tuple[str, int]] = set()
    for entity in entities:
        if entity.attractor_name in names:
            raise ORCHORBITALHierarchyError("duplicate attractor_name in PNCS hierarchy binding")
        if entity.source_projection_id in projections:
            raise ORCHORBITALHierarchyError("duplicate source_projection_id in PNCS hierarchy binding")
        if entity.canonical_id in canonical_ids:
            raise ORCHORBITALHierarchyError("duplicate canonical_id in PNCS hierarchy binding")
        if entity.sphere_id not in sphere_map:
            raise ORCHORBITALHierarchyError("entity binding references unknown sphere_id")
        sphere = sphere_map[entity.sphere_id]
        if entity.parent_sphere_id != sphere.parent_sphere_id:
            raise ORCHORBITALHierarchyError("entity parent_sphere_id disagrees with sphere hierarchy")
        slot = (entity.sphere_id, entity.orbit_index)
        if slot in orbit_slots:
            raise ORCHORBITALHierarchyError("duplicate orbit_index inside one PNCS sphere")
        names.add(entity.attractor_name)
        projections.add(entity.source_projection_id)
        canonical_ids.add(entity.canonical_id)
        orbit_slots.add(slot)


def hierarchy_nodes_from_pncs(binding_set: PNCSHierarchyBindingSet) -> tuple[HierarchyNode, ...]:
    nodes: list[HierarchyNode] = [
        HierarchyNode(sphere.sphere_id, sphere.parent_sphere_id)
        for sphere in binding_set.spheres
    ]
    nodes.extend(
        HierarchyNode(entity.attractor_name, entity.sphere_id)
        for entity in binding_set.entities
    )
    return tuple(nodes)


def validate_exact_attractor_coverage(
    attractor_names: Sequence[str],
    binding_set: PNCSHierarchyBindingSet,
) -> None:
    names = tuple(attractor_names)
    if not names or any(type(name) is not str or not name.strip() for name in names):
        raise ORCHORBITALHierarchyError("attractor_names must contain non-empty strings")
    if len(set(names)) != len(names):
        raise ORCHORBITALHierarchyError("attractor_names must be unique")
    bound = {entity.attractor_name for entity in binding_set.entities}
    if set(names) != bound:
        raise ORCHORBITALHierarchyError("PNCS entity binding must exactly cover dynamic attractor leaves")


def entity_binding_for_attractor(
    binding_set: PNCSHierarchyBindingSet,
    attractor_name: str,
) -> PNCSEntityAttractorBinding:
    matches = [item for item in binding_set.entities if item.attractor_name == attractor_name]
    if len(matches) != 1:
        raise ORCHORBITALHierarchyError("attractor must resolve to exactly one PNCS entity binding")
    return matches[0]


def ordered_entities_in_sphere(
    binding_set: PNCSHierarchyBindingSet,
    sphere_id: str,
) -> tuple[PNCSEntityAttractorBinding, ...]:
    sphere_ids = {sphere.sphere_id for sphere in binding_set.spheres}
    if sphere_id not in sphere_ids:
        raise ORCHORBITALHierarchyError("unknown sphere_id")
    return tuple(
        sorted(
            (item for item in binding_set.entities if item.sphere_id == sphere_id),
            key=lambda item: (item.orbit_index, item.phase, item.canonical_id),
        )
    )


def sphere_path(
    binding_set: PNCSHierarchyBindingSet,
    sphere_id: str,
) -> tuple[str, ...]:
    sphere_map = {sphere.sphere_id: sphere for sphere in binding_set.spheres}
    if sphere_id not in sphere_map:
        raise ORCHORBITALHierarchyError("unknown sphere_id")
    path: list[str] = []
    cursor: str | None = sphere_id
    while cursor is not None:
        path.append(cursor)
        cursor = sphere_map[cursor].parent_sphere_id
    return tuple(reversed(path))


def attractor_path(
    binding_set: PNCSHierarchyBindingSet,
    attractor_name: str,
) -> tuple[str, ...]:
    entity = entity_binding_for_attractor(binding_set, attractor_name)
    return (*sphere_path(binding_set, entity.sphere_id), entity.attractor_name)
