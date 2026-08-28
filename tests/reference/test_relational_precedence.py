import pytest

from idt.relational_precedence import (
    RelationalEdge,
    RelationalPrecedenceError,
    maximal_frontier,
    prefix_precedes,
    serial_now_frontier,
    serial_temporal_order_is_strict,
    unfold_serial_history,
)


def edge(edge_id, source, target, dtheta=1.0, q=1.0):
    return RelationalEdge(edge_id, source, target, dtheta, q)


def test_composable_word_generates_strict_prefix_and_theta_order():
    occ = unfold_serial_history(
        "A",
        [
            edge("e1", "A", "B", 0.4),
            edge("e2", "B", "C", 0.7),
            edge("e3", "C", "D", 0.2),
        ],
    )
    assert [o.theta for o in occ] == [0.0, 0.4, 1.1, 1.3]
    assert serial_temporal_order_is_strict(occ)
    assert prefix_precedes(occ[0], occ[3], strict=True)
    assert prefix_precedes(occ[1], occ[3], strict=True)


def test_state_recurrence_creates_new_occurrence_instead_of_order_cycle():
    occ = unfold_serial_history(
        "A",
        [
            edge("e1", "A", "B", 0.3),
            edge("e2", "B", "A", 0.5),
            edge("e3", "A", "B", 0.2),
        ],
    )
    assert occ[0].state == occ[2].state == "A"
    assert occ[1].state == occ[3].state == "B"
    assert occ[0].prefix != occ[2].prefix
    assert occ[1].prefix != occ[3].prefix
    assert occ[2].theta > occ[0].theta
    assert occ[3].theta > occ[1].theta
    assert serial_temporal_order_is_strict(occ)


def test_serial_now_is_latest_supported_occurrence():
    occ = unfold_serial_history(
        "A",
        [
            edge("e1", "A", "B", q=1.0),
            edge("e2", "B", "C", q=0.0),
            edge("e3", "C", "D", q=2.0),
        ],
    )
    now = serial_now_frontier(occ)
    assert len(now) == 1
    assert now[0].terminal_edge_id == "e3"
    assert now[0].state == "D"


def test_zero_signature_occurrence_does_not_replace_supported_now():
    occ = unfold_serial_history(
        "A",
        [
            edge("e1", "A", "B", q=1.0),
            edge("e2", "B", "C", q=0.0),
        ],
    )
    now = serial_now_frontier(occ)
    assert now[0].terminal_edge_id == "e1"


def test_empty_supported_history_has_empty_now_frontier():
    occ = unfold_serial_history(
        "A",
        [edge("e1", "A", "B", q=0.0)],
    )
    assert serial_now_frontier(occ) == ()


def test_concurrent_supported_maxima_form_now_antichain():
    nodes = ["root", "a", "b", "a2", "b2"]
    precedence = [
        ("root", "a"),
        ("root", "b"),
        ("a", "a2"),
        ("b", "b2"),
    ]
    now = maximal_frontier(nodes, precedence, {"root", "a", "b", "a2", "b2"})
    assert set(now) == {"a2", "b2"}


def test_maximal_frontier_uses_transitive_reachability():
    nodes = ["a", "b", "c"]
    precedence = [("a", "b"), ("b", "c")]
    now = maximal_frontier(nodes, precedence, {"a", "c"})
    assert now == ("c",)


def test_prefix_relation_is_antisymmetric_on_occurrences():
    occ = unfold_serial_history(
        "A",
        [edge("e1", "A", "B"), edge("e2", "B", "C")],
    )
    assert prefix_precedes(occ[0], occ[2])
    assert not prefix_precedes(occ[2], occ[0])
    assert prefix_precedes(occ[1], occ[1])
    assert not prefix_precedes(occ[1], occ[1], strict=True)


def test_invalid_noncomposable_word_fails_closed():
    with pytest.raises(RelationalPrecedenceError):
        unfold_serial_history(
            "A",
            [edge("e1", "A", "B"), edge("e2", "X", "C")],
        )


@pytest.mark.parametrize(
    "args",
    [
        ("e", "A", "B", 0.0, 1.0),
        ("e", "A", "B", -1.0, 1.0),
        ("e", "A", "B", 1.0, -0.1),
    ],
)
def test_invalid_edge_domain_fails_closed(args):
    with pytest.raises(RelationalPrecedenceError):
        RelationalEdge(*args)


def test_cyclic_declared_strict_precedence_fails_closed():
    with pytest.raises(RelationalPrecedenceError):
        maximal_frontier(
            ["a", "b", "c"],
            [("a", "b"), ("b", "c"), ("c", "a")],
            {"a", "b", "c"},
        )
