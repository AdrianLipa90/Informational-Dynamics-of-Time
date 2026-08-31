import math

import pytest

from idt.global_event_clock_exactness import EventEdge, certify_event_clock
from idt.regular_smooth_clock_extension import (
    AffineClockChart,
    AffineTransition,
    EventAnchor,
    RegularClockExtensionError,
    certify_regular_affine_clock_extension,
)


def chart(name, gradient, offset=0.0):
    return AffineClockChart(name, tuple(gradient), offset)


def transition(source, target, matrix, shift):
    return AffineTransition(
        source,
        target,
        tuple(tuple(row) for row in matrix),
        tuple(shift),
    )


def anchor(event_id, chart_name, point):
    return EventAnchor(event_id, chart_name, tuple(point))


def reference_witness():
    charts = [
        chart("A", [1.0, 0.0, 0.0, 0.0], 0.0),
        chart("B", [1.0, 0.0, 0.0, 0.0], -1.0),
    ]
    transitions = [
        transition(
            "A",
            "B",
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            [1.0, 0.0, 0.0, 0.0],
        )
    ]
    event_clock = certify_event_clock([EventEdge("e0", "e1", 2.0)])
    anchors = [
        anchor("e0", "A", [0.0, 0.0, 0.0, 0.0]),
        anchor("e1", "A", [2.0, 0.0, 0.0, 0.0]),
        anchor("e1", "B", [3.0, 0.0, 0.0, 0.0]),
    ]
    return charts, transitions, anchors, event_clock.potentials


def test_affine_overlap_and_05h_anchors_certify_regular_clock():
    charts, transitions, anchors, potentials = reference_witness()
    cert = certify_regular_affine_clock_extension(charts, transitions, anchors, potentials)
    assert cert.regular
    assert cert.dimension == 4
    assert cert.chart_count == 2
    assert cert.transition_count == 1
    assert cert.anchor_count == 3
    assert cert.connected
    assert cert.min_gradient_norm == pytest.approx(1.0)
    assert cert.min_transition_singular_value == pytest.approx(1.0)
    assert cert.max_overlap_linear_residual == pytest.approx(0.0, abs=1e-15)
    assert cert.max_overlap_offset_residual == pytest.approx(0.0, abs=1e-15)
    assert cert.max_anchor_residual == pytest.approx(0.0, abs=1e-15)
    assert cert.calibration_offset == pytest.approx(0.0, abs=1e-15)


def test_one_common_additive_calibration_is_allowed():
    charts, transitions, anchors, potentials = reference_witness()
    shifted = [
        chart("A", [1.0, 0.0, 0.0, 0.0], 7.5),
        chart("B", [1.0, 0.0, 0.0, 0.0], 6.5),
    ]
    cert = certify_regular_affine_clock_extension(shifted, transitions, anchors, potentials)
    assert cert.calibration_offset == pytest.approx(7.5)
    assert cert.max_anchor_residual == pytest.approx(0.0, abs=1e-15)


def test_zero_clock_differential_fails_closed():
    charts, transitions, anchors, potentials = reference_witness()
    bad = [chart("A", [0.0, 0.0, 0.0, 0.0]), charts[1]]
    with pytest.raises(RegularClockExtensionError, match="clock differential"):
        certify_regular_affine_clock_extension(bad, transitions, anchors, potentials)


def test_overlap_gradient_mismatch_fails_closed():
    charts, transitions, anchors, potentials = reference_witness()
    bad = [charts[0], chart("B", [2.0, 0.0, 0.0, 0.0], -1.0)]
    with pytest.raises(RegularClockExtensionError, match="gradient mismatch"):
        certify_regular_affine_clock_extension(bad, transitions, anchors, potentials)


def test_overlap_offset_mismatch_fails_closed():
    charts, transitions, anchors, potentials = reference_witness()
    bad = [charts[0], chart("B", [1.0, 0.0, 0.0, 0.0], -0.5)]
    with pytest.raises(RegularClockExtensionError, match="offset mismatch"):
        certify_regular_affine_clock_extension(bad, transitions, anchors, potentials)


def test_singular_chart_transition_fails_closed():
    charts, _, anchors, potentials = reference_witness()
    bad_transition = transition(
        "A",
        "B",
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
        ],
        [1.0, 0.0, 0.0, 0.0],
    )
    with pytest.raises(RegularClockExtensionError, match="singular"):
        certify_regular_affine_clock_extension(charts, [bad_transition], anchors, potentials)


def test_inconsistent_event_anchor_fails_closed():
    charts, transitions, anchors, potentials = reference_witness()
    bad_anchors = list(anchors)
    bad_anchors[-1] = anchor("e1", "B", [3.25, 0.0, 0.0, 0.0])
    with pytest.raises(RegularClockExtensionError, match="additive calibration"):
        certify_regular_affine_clock_extension(charts, transitions, bad_anchors, potentials)


def test_missing_event_anchor_fails_global_binding():
    charts, transitions, anchors, potentials = reference_witness()
    only_e0 = [item for item in anchors if item.event_id == "e0"]
    with pytest.raises(RegularClockExtensionError, match="events lack continuum anchors"):
        certify_regular_affine_clock_extension(charts, transitions, only_e0, potentials)


def test_disconnected_chart_atlas_fails_connected_domain_claim():
    charts = [
        chart("A", [1.0, 0.0]),
        chart("B", [1.0, 0.0]),
    ]
    anchors = [anchor("e0", "A", [0.0, 0.0])]
    with pytest.raises(RegularClockExtensionError, match="disconnected chart atlas"):
        certify_regular_affine_clock_extension(charts, [], anchors, {"e0": 0.0})


def test_single_chart_regular_clock_is_valid_without_transitions():
    charts = [chart("A", [1.0, 0.0, 0.0], 3.0)]
    anchors = [anchor("e0", "A", [2.0, 0.0, 0.0])]
    cert = certify_regular_affine_clock_extension(charts, [], anchors, {"e0": 2.0})
    assert cert.regular
    assert cert.connected
    assert cert.min_transition_singular_value == math.inf
    assert cert.calibration_offset == pytest.approx(3.0)


def test_nonfinite_inputs_fail_closed():
    with pytest.raises(RegularClockExtensionError):
        chart("A", [1.0, math.nan])
    with pytest.raises(RegularClockExtensionError):
        AffineClockChart("A", (1.0,), math.inf)
