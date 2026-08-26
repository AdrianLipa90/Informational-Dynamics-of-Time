from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

from .orchorbital import AttractorFieldState, AttractorResidence


class ORCHORBITALHierarchyError(ValueError):
    pass


@dataclass(frozen=True)
class HierarchyNode:
    name: str
    parent: str | None


@dataclass(frozen=True)
class HierarchyWeight:
    name: str
    parent: str | None
    weight: float
    is_leaf: bool


@dataclass(frozen=True)
class HierarchyEntropyAudit:
    leaf_entropy_bits: float
    root_entropy_bits: float
    conditional_entropy_bits: float
    reconstructed_leaf_entropy_bits: float
    decomposition_error: float
    local_entropy_bits: tuple[tuple[str, float], ...]


@dataclass(frozen=True)
class HierarchyFieldState:
    weights: tuple[HierarchyWeight, ...]
    active_leaf: str | None
    active_path: tuple[str, ...]
    entropy: HierarchyEntropyAudit | None
    leak_mode: bool


@dataclass(frozen=True)
class HierarchyResidence:
    name: str
    dwell_tau: float
    winding: float
    leaf_segment_count: int


def _validated_nodes(nodes: Sequence[HierarchyNode], leaf_names: Sequence[str]) -> tuple[tuple[HierarchyNode, ...], dict[str, tuple[str, ...]], tuple[str, ...]]:
    if not nodes:
        raise ORCHORBITALHierarchyError("hierarchy nodes must be non-empty")
    names: list[str] = []
    parent: dict[str, str | None] = {}
    for raw in nodes:
        name = str(raw.name).strip()
        if not name:
            raise ORCHORBITALHierarchyError("hierarchy node names must be non-empty")
        if name in parent:
            raise ORCHORBITALHierarchyError("hierarchy node names must be unique")
        p = None if raw.parent is None else str(raw.parent).strip()
        if p == "":
            raise ORCHORBITALHierarchyError("parent names must be non-empty when supplied")
        if p == name:
            raise ORCHORBITALHierarchyError("a hierarchy node cannot parent itself")
        names.append(name)
        parent[name] = p

    for name, p in parent.items():
        if p is not None and p not in parent:
            raise ORCHORBITALHierarchyError(f"parent {p} of {name} is absent from hierarchy")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visited:
            return
        if name in visiting:
            raise ORCHORBITALHierarchyError("hierarchy contains a cycle")
        visiting.add(name)
        p = parent[name]
        if p is not None:
            visit(p)
        visiting.remove(name)
        visited.add(name)

    for name in names:
        visit(name)

    children_lists: dict[str, list[str]] = {name: [] for name in names}
    roots: list[str] = []
    for name in names:
        p = parent[name]
        if p is None:
            roots.append(name)
        else:
            children_lists[p].append(name)

    leaves = tuple(str(name).strip() for name in leaf_names)
    if not leaves or any(not name for name in leaves):
        raise ORCHORBITALHierarchyError("leaf_names must contain non-empty names")
    if len(set(leaves)) != len(leaves):
        raise ORCHORBITALHierarchyError("leaf_names must be unique")
    for leaf in leaves:
        if leaf not in parent:
            raise ORCHORBITALHierarchyError(f"leaf {leaf} is absent from hierarchy")
        if children_lists[leaf]:
            raise ORCHORBITALHierarchyError(f"dynamic attractor {leaf} must be a hierarchy leaf")

    hierarchy_leaves = {name for name in names if not children_lists[name]}
    if hierarchy_leaves != set(leaves):
        missing = sorted(hierarchy_leaves.difference(leaves))
        extra = sorted(set(leaves).difference(hierarchy_leaves))
        raise ORCHORBITALHierarchyError(
            f"leaf_names must equal hierarchy leaves; untyped={missing}, nonleaf={extra}"
        )

    children = {name: tuple(children_lists[name]) for name in names}
    return tuple(HierarchyNode(name, parent[name]) for name in names), children, tuple(roots)


def _leaf_weight_map(field: AttractorFieldState) -> dict[str, float]:
    weights: dict[str, float] = {}
    for item in field.evaluations:
        if item.name in weights:
            raise ORCHORBITALHierarchyError("attractor field contains duplicate names")
        weight = float(item.weight)
        if not math.isfinite(weight) or weight < 0.0:
            raise ORCHORBITALHierarchyError("attractor weights must be finite and non-negative")
        weights[item.name] = weight
    if not weights:
        raise ORCHORBITALHierarchyError("attractor field must contain evaluations")
    if field.leak_mode:
        if any(weight != 0.0 for weight in weights.values()):
            raise ORCHORBITALHierarchyError("LEAK_MODE field must have zero attractor weights")
        return weights
    total = sum(weights.values())
    if not math.isfinite(total) or abs(total - 1.0) > 1e-10:
        raise ORCHORBITALHierarchyError("bound attractor weights must sum to one")
    return weights


def _entropy(probabilities: Sequence[float]) -> float:
    return float(-sum(p * math.log2(p) for p in probabilities if p > 0.0))


def hierarchy_field_state(field: AttractorFieldState, nodes: Sequence[HierarchyNode]) -> HierarchyFieldState:
    leaf_weight = _leaf_weight_map(field)
    validated, children, roots = _validated_nodes(nodes, tuple(leaf_weight))
    parent = {node.name: node.parent for node in validated}

    if field.leak_mode:
        weights = tuple(
            HierarchyWeight(node.name, node.parent, 0.0, not children[node.name])
            for node in validated
        )
        return HierarchyFieldState(weights, None, tuple(), None, True)

    aggregate: dict[str, float] = {}

    def node_weight(name: str) -> float:
        if name in aggregate:
            return aggregate[name]
        if not children[name]:
            value = leaf_weight[name]
        else:
            value = float(sum(node_weight(child) for child in children[name]))
        aggregate[name] = value
        return value

    for root in roots:
        node_weight(root)

    root_weights = [aggregate[root] for root in roots]
    root_entropy = _entropy(root_weights)
    local_entropy: list[tuple[str, float]] = []
    conditional_total = 0.0
    for node in validated:
        child_names = children[node.name]
        node_w = aggregate[node.name]
        if child_names and node_w > 0.0:
            probabilities = [aggregate[child] / node_w for child in child_names]
            h_local = _entropy(probabilities)
            local_entropy.append((node.name, h_local))
            conditional_total += node_w * h_local

    leaf_entropy = _entropy(list(leaf_weight.values()))
    reconstructed = root_entropy + conditional_total
    entropy_audit = HierarchyEntropyAudit(
        leaf_entropy_bits=leaf_entropy,
        root_entropy_bits=root_entropy,
        conditional_entropy_bits=conditional_total,
        reconstructed_leaf_entropy_bits=reconstructed,
        decomposition_error=abs(leaf_entropy - reconstructed),
        local_entropy_bits=tuple(local_entropy),
    )

    active_leaf = field.active_attractor
    if active_leaf is None or active_leaf not in leaf_weight:
        raise ORCHORBITALHierarchyError("bound field must identify an active attractor leaf")
    path: list[str] = [active_leaf]
    cursor = active_leaf
    while parent[cursor] is not None:
        cursor = parent[cursor]  # type: ignore[assignment]
        path.append(cursor)
    path.reverse()

    weights = tuple(
        HierarchyWeight(node.name, node.parent, aggregate[node.name], not children[node.name])
        for node in validated
    )
    return HierarchyFieldState(weights, active_leaf, tuple(path), entropy_audit, False)


def hierarchy_residence_summary(
    residence: Sequence[AttractorResidence],
    nodes: Sequence[HierarchyNode],
) -> tuple[HierarchyResidence, ...]:
    if not residence:
        raise ORCHORBITALHierarchyError("residence must be non-empty")
    leaf_names = tuple(item.name for item in residence)
    validated, children, _ = _validated_nodes(nodes, leaf_names)
    dwell_leaf = {item.name: float(item.dwell_tau) for item in residence}
    winding_leaf = {item.name: float(item.winding) for item in residence}
    count_leaf = {item.name: int(item.segments) for item in residence}
    for item in residence:
        if not math.isfinite(item.dwell_tau) or item.dwell_tau < 0.0:
            raise ORCHORBITALHierarchyError("residence dwell time must be finite and non-negative")
        if not math.isfinite(item.winding):
            raise ORCHORBITALHierarchyError("residence winding must be finite")
        if isinstance(item.segments, bool) or item.segments < 0:
            raise ORCHORBITALHierarchyError("residence segment count must be non-negative")

    memo: dict[str, tuple[float, float, int]] = {}

    def aggregate(name: str) -> tuple[float, float, int]:
        if name in memo:
            return memo[name]
        if not children[name]:
            value = (dwell_leaf[name], winding_leaf[name], count_leaf[name])
        else:
            child_values = [aggregate(child) for child in children[name]]
            value = (
                float(sum(item[0] for item in child_values)),
                float(sum(item[1] for item in child_values)),
                int(sum(item[2] for item in child_values)),
            )
        memo[name] = value
        return value

    return tuple(
        HierarchyResidence(node.name, *aggregate(node.name))
        for node in validated
    )


def _descendant_leaves(name: str, children: Mapping[str, Sequence[str]]) -> set[str]:
    if not children[name]:
        return {name}
    out: set[str] = set()
    for child in children[name]:
        out.update(_descendant_leaves(child, children))
    return out


def coarse_grain_transition_counts(
    leaf_transition_counts: Mapping[tuple[str, str], int],
    nodes: Sequence[HierarchyNode],
    leaf_names: Sequence[str],
    cut_nodes: Sequence[str],
) -> dict[tuple[str, str], int]:
    validated, children, _ = _validated_nodes(nodes, leaf_names)
    names = {node.name for node in validated}
    cut = tuple(str(name).strip() for name in cut_nodes)
    if not cut or any(not name for name in cut):
        raise ORCHORBITALHierarchyError("cut_nodes must be non-empty")
    if len(set(cut)) != len(cut):
        raise ORCHORBITALHierarchyError("cut_nodes must be unique")
    if any(name not in names for name in cut):
        raise ORCHORBITALHierarchyError("cut_nodes must exist in hierarchy")

    leaf_set = set(leaf_names)
    owner: dict[str, str] = {}
    for cut_node in cut:
        covered = _descendant_leaves(cut_node, children)
        for leaf in covered:
            if leaf in owner:
                raise ORCHORBITALHierarchyError("cut_nodes overlap on hierarchy leaves")
            owner[leaf] = cut_node
    if set(owner) != leaf_set:
        raise ORCHORBITALHierarchyError("cut_nodes must partition all hierarchy leaves")

    out: dict[tuple[str, str], int] = {}
    for (source, target), raw_count in leaf_transition_counts.items():
        if source not in leaf_set or target not in leaf_set:
            raise ORCHORBITALHierarchyError("transition endpoints must be hierarchy leaves")
        if isinstance(raw_count, bool):
            raise ORCHORBITALHierarchyError("transition counts must be non-negative integers")
        count = int(raw_count)
        if count != raw_count or count < 0:
            raise ORCHORBITALHierarchyError("transition counts must be non-negative integers")
        coarse_source = owner[source]
        coarse_target = owner[target]
        if coarse_source == coarse_target or count == 0:
            continue
        edge = (coarse_source, coarse_target)
        out[edge] = out.get(edge, 0) + count
    return out
