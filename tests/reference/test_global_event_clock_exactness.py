import math

import pytest

from idt.global_event_clock_exactness import (
    EventEdge,
    TemporalExactnessError,
    certify_event_clock,
)


def edge(source: str, target: str, dtheta: float) -> EventEdge:
    return EventEdge(source, target, dtheta)


def test_serial_prefix_chain_reconstructs_exact_scalar_clock():
    cert = certify_event_clock(
        [
            edge("A", "B", 0.4),
            edge("B", "C", 0.7),
            edge("C", "D", 0.2),
        ]
    )
    assert cert.exact
    assert cert.component_count == 1
    assert cert.max_residual == pytest.approx(0.0, abs=1e-15)
    assert cert.potentials == pytest.approx({"A": 0.0, "B": 0.4, "C": 1.1, "D": 1.3})


def test_equal_diamond_paths_define_one_event_clock():
    cert = certify_event_clock(
        [
            edge("a", "b", 0.3),
            edge("b", "d", 0.8),
            edge("a", "c", 0.5),
            edge("c", "d", 0.6),
        ]
    )
    assert cert.potentials["d"] == pytest.approx(1.1)
    assert cert.max_residual == pytest.approx(0.0, abs=1e-15)


def test_unequal_diamond_paths_fail_as_temporal_holonomy():
    with pytest.raises(TemporalExactnessError, match="temporal holonomy defect"):
        certify_event_clock(
            [
                edge("a", "b", 0.3),
                edge("b", "d", 0.8),
                edge("a", "c", 0.5),
                edge("c", "d", 0.7),
            ]
        )


def test_positive_directed_cycle_fails_exactness():
    with pytest.raises(TemporalExactnessError, match="temporal holonomy defect"):
        certify_event_clock(
            [
                edge("a", "b", 0.2),
                edge("b", "c", 0.3),
                edge("c", "a", 0.4),
            ]
        )


def test_disconnected_input_fails_connected_domain_claim():
    with pytest.raises(TemporalExactnessError, match="connected-domain certificate"):
        certify_event_clock(
            [edge("a", "b", 0.2), edge("x", "y", 0.4)],
            require_connected=True,
        )


def test_disconnected_components_can_be_certified_when_explicitly_allowed():
    cert = certify_event_clock(
        [edge("a", "b", 0.2), edge("x", "y", 0.4)],
        require_connected=False,
    )
    assert cert.exact
    assert cert.component_count == 2
    assert cert.potentials["b"] - cert.potentials["a"] == pytest.approx(0.2)
    assert cert.potentials["y"] - cert.potentials["x"] == pytest.approx(0.4)


def test_isolated_vertex_is_detected_by_connectivity_gate():
    with pytest.raises(TemporalExactnessError, match="connected-domain certificate"):
        certify_event_clock(
            [edge("a", "b", 0.2)],
            vertices=["a", "b", "isolated"],
        )


@pytest.mark.parametrize("value", [0.0, -1.0, math.inf, -math.inf, math.nan])
def test_nonpositive_or_nonfinite_elapsed_weights_fail_closed(value):
    with pytest.raises(TemporalExactnessError):
        edge("a", "b", value)


def test_positive_self_loop_fails_closed():
    with pytest.raises(TemporalExactnessError, match="self-loop"):
        edge("a", "a", 0.1)


def test_exact_positive_edges_are_strictly_time_oriented():
    edges = [
        edge("r", "u", 0.25),
        edge("u", "v", 0.5),
        edge("r", "w", 0.4),
        edge("w", "v", 0.35),
    ]
    cert = certify_event_clock(edges)
    for item in edges:
        assert cert.potentials[item.target] > cert.potentials[item.source]
        assert cert.potentials[item.target] - cert.potentials[item.source] == pytest.approx(item.dtheta)


def test_single_vertex_has_trivial_exact_clock():
    cert = certify_event_clock([], vertices=["origin"])
    assert cert.exact
    assert cert.component_count == 1
    assert cert.potentials == {"origin": 0.0}
