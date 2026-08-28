from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


class RelationalPrecedenceError(ValueError):
    pass


@dataclass(frozen=True)
class RelationalEdge:
    edge_id: str
    source: str
    target: str
    dtheta: float
    event_weight: float

    def __post_init__(self) -> None:
        if not self.edge_id:
            raise RelationalPrecedenceError("edge_id must be non-empty")
        if not self.source or not self.target:
            raise RelationalPrecedenceError("source and target must be non-empty")
        if not (self.dtheta > 0.0):
            raise RelationalPrecedenceError("dtheta must be strictly positive")
        if not (self.event_weight >= 0.0):
            raise RelationalPrecedenceError("event_weight must be non-negative")


@dataclass(frozen=True)
class Occurrence:
    prefix: tuple[str, ...]
    state: str
    theta: float
    terminal_edge_id: str | None
    terminal_event_weight: float | None

    @property
    def depth(self) -> int:
        return len(self.prefix)


def _is_prefix(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return len(left) <= len(right) and right[: len(left)] == left


def prefix_precedes(left: Occurrence, right: Occurrence, *, strict: bool = False) -> bool:
    if strict and left.prefix == right.prefix:
        return False
    return _is_prefix(left.prefix, right.prefix)


def unfold_serial_history(initial_state: str, edges: Sequence[RelationalEdge]) -> tuple[Occurrence, ...]:
    if not initial_state:
        raise RelationalPrecedenceError("initial_state must be non-empty")

    occurrences: list[Occurrence] = [
        Occurrence(
            prefix=(),
            state=initial_state,
            theta=0.0,
            terminal_edge_id=None,
            terminal_event_weight=None,
        )
    ]

    current_state = initial_state
    prefix: list[str] = []
    theta = 0.0

    for edge in edges:
        if edge.source != current_state:
            raise RelationalPrecedenceError(
                f"non-composable history: expected source {current_state!r}, got {edge.source!r}"
            )
        prefix.append(edge.edge_id)
        theta += edge.dtheta
        current_state = edge.target
        occurrences.append(
            Occurrence(
                prefix=tuple(prefix),
                state=current_state,
                theta=theta,
                terminal_edge_id=edge.edge_id,
                terminal_event_weight=edge.event_weight,
            )
        )

    return tuple(occurrences)


def serial_temporal_order_is_strict(occurrences: Sequence[Occurrence]) -> bool:
    for left, right in zip(occurrences, occurrences[1:]):
        if not prefix_precedes(left, right, strict=True):
            return False
        if not right.theta > left.theta:
            return False
    return True


def serial_now_frontier(occurrences: Sequence[Occurrence]) -> tuple[Occurrence, ...]:
    supported = [
        occ
        for occ in occurrences
        if occ.terminal_event_weight is not None and occ.terminal_event_weight > 0.0
    ]
    if not supported:
        return ()
    return (supported[-1],)


def maximal_frontier(
    node_ids: Iterable[str],
    precedence_pairs: Iterable[tuple[str, str]],
    supported_ids: Iterable[str],
) -> tuple[str, ...]:
    nodes = tuple(dict.fromkeys(node_ids))
    node_set = set(nodes)
    supported = set(supported_ids)
    if not supported <= node_set:
        raise RelationalPrecedenceError("supported_ids must be a subset of node_ids")

    relation = {(a, b) for a, b in precedence_pairs}
    for a, b in relation:
        if a not in node_set or b not in node_set:
            raise RelationalPrecedenceError("precedence pair references an unknown node")
        if a == b:
            raise RelationalPrecedenceError("strict precedence cannot contain self loops")

    adjacency = {node: set() for node in nodes}
    for a, b in relation:
        adjacency[a].add(b)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            raise RelationalPrecedenceError("strict precedence relation contains a cycle")
        visiting.add(node)
        for nxt in adjacency[node]:
            visit(nxt)
        visiting.remove(node)
        visited.add(node)

    for node in nodes:
        visit(node)

    reachability: dict[str, set[str]] = {node: set() for node in nodes}

    def descendants(node: str) -> set[str]:
        if reachability[node]:
            return reachability[node]
        out: set[str] = set()
        for nxt in adjacency[node]:
            out.add(nxt)
            out.update(descendants(nxt))
        reachability[node] = out
        return out

    for node in nodes:
        descendants(node)

    maximal = []
    for candidate in nodes:
        if candidate not in supported:
            continue
        if not (reachability[candidate] & supported):
            maximal.append(candidate)

    return tuple(maximal)
