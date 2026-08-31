import math

import pytest

from idt.regular_smooth_clock_extension import (
    ClockOverlap,
    EventEmbedding,
    RegularClockPatch,
    SmoothClockExtensionError,
    certify_regular_smooth_clock_extension,
)


I4 = (
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0, 1.0),
)
ZERO4 = (0.0, 0.0, 0.0, 0.0)


def patch(name, intercept):
    return RegularClockPatch(name, (1.0, 0.0, 0.0, 0.0), intercept)


def overlap(source, target, dt):
    return ClockOverlap(source, target, I4, (dt, 0.0, 0.0, 0.0))


def base_two_patch_fixture(*, coverage=False):
    patches = [patch("p", 0.0), patch("q", -2.0)]
    overlaps = [overlap("p", "q", 2.0)]
    event_clock = {"e0": 10.0, "e1": 11.0}
    embeddings = [
        EventEmbedding("e0", "p", (0.0, 0.0, 0.0, 0.0)),
        EventEmbedding("e0", "q", (2.0, 0.0, 0.0, 0.0)),
        EventEmbedding("e1", "p", (1.0, 0.0, 0.0, 0.0)),
        EventEmbedding("e1", "q", (3.0, 0.0, 0.0, 0.0)),
    ]
    return certify_regular_smooth_clock_extension(
        patches,
        overlaps,
        event_clock,
        embeddings,
        domain_coverage_witness_supplied=coverage,
    )


def test_affine_two_patch_extension_matches_event_clock_up_to_global_offset():
    cert = base_two_patch_fixture()
    assert cert.compatible
    assert cert.regular_clock
    assert cert.smoothness_class == "C_INFINITY_AFFINE_CHART_WITNESS"
    assert cert.alignment_offset == pytest.approx(-10.0)
    assert cert.max_event_alignment_residual == pytest.approx(0.0)
    assert cert.max_overlap_scalar_residual == pytest.approx(0.0)
    assert cert.max_embedding_overlap_residual == pytest.approx(0.0)
    assert cert.production_input_status == "OPEN_INPUT"


def test_domain_wide_promotion_requires_explicit_coverage_witness():
    local = base_two_patch_fixture(coverage=False)
    global_cert = base_two_patch_fixture(coverage=True)
    assert not local.global_regular_extension
    assert not local.domain_coverage_witness_supplied
    assert global_cert.global_regular_extension
    assert global_cert.domain_coverage_witness_supplied


def test_nonzero_gradient_is_regular_everywhere_on_affine_patch():
    p = RegularClockPatch("p", (2.0, -1.0, 0.5, 0.25), 3.0)
    cert = certify_regular_smooth_clock_extension(
        [p],
        [],
        {"e": 7.0},
        [EventEmbedding("e", "p", (2.0, 0.0, 0.0, 0.0))],
        domain_coverage_witness_supplied=True,
    )
    assert cert.min_dt_norm > 0.0
    assert cert.global_regular_extension


def test_three_patch_affine_cocycle_passes():
    patches = [patch("p", 0.0), patch("q", -2.0), patch("r", -5.0)]
    overlaps = [
        overlap("p", "q", 2.0),
        overlap("q", "r", 3.0),
        overlap("p", "r", 5.0),
    ]
    cert = certify_regular_smooth_clock_extension(
        patches,
        overlaps,
        {"e": 4.0},
        [
            EventEmbedding("e", "p", (1.0, 0.0, 0.0, 0.0)),
            EventEmbedding("e", "q", (3.0, 0.0, 0.0, 0.0)),
            EventEmbedding("e", "r", (6.0, 0.0, 0.0, 0.0)),
        ],
        triangles=[("p", "q", "r")],
    )
    assert cert.triangle_count == 1
    assert cert.max_linear_cocycle_residual == pytest.approx(0.0)
    assert cert.max_translation_cocycle_residual == pytest.approx(0.0)


def test_event_clock_alignment_mismatch_fails_closed():
    with pytest.raises(SmoothClockExtensionError, match="global additive constant"):
        certify_regular_smooth_clock_extension(
            [patch("p", 0.0)],
            [],
            {"e0": 10.0, "e1": 12.0},
            [
                EventEmbedding("e0", "p", (0.0, 0.0, 0.0, 0.0)),
                EventEmbedding("e1", "p", (1.0, 0.0, 0.0, 0.0)),
            ],
        )


def test_overlap_scalar_mismatch_fails_closed():
    with pytest.raises(SmoothClockExtensionError, match="clock scalar mismatch"):
        certify_regular_smooth_clock_extension(
            [patch("p", 0.0), patch("q", -1.0)],
            [overlap("p", "q", 2.0)],
            {"e": 0.0},
            [EventEmbedding("e", "p", ZERO4)],
        )


def test_same_event_coordinates_must_transform_across_overlap():
    with pytest.raises(SmoothClockExtensionError, match="incompatible overlap coordinates"):
        certify_regular_smooth_clock_extension(
            [patch("p", 0.0), patch("q", -2.0)],
            [overlap("p", "q", 2.0)],
            {"e": 10.0},
            [
                EventEmbedding("e", "p", ZERO4),
                EventEmbedding("e", "q", (2.0, 0.1, 0.0, 0.0)),
            ],
        )


def test_missing_event_embedding_fails_closed():
    with pytest.raises(SmoothClockExtensionError, match="every 05H event must be embedded"):
        certify_regular_smooth_clock_extension(
            [patch("p", 0.0)],
            [],
            {"e0": 0.0, "e1": 1.0},
            [EventEmbedding("e0", "p", ZERO4)],
        )


def test_disconnected_clock_atlas_fails_closed():
    with pytest.raises(SmoothClockExtensionError, match="overlap graph must be connected"):
        certify_regular_smooth_clock_extension(
            [patch("p", 0.0), patch("q", 0.0)],
            [],
            {"e": 0.0},
            [EventEmbedding("e", "p", ZERO4)],
        )


def test_zero_clock_gradient_fails_closed():
    with pytest.raises(SmoothClockExtensionError, match="gradient must be nonzero"):
        RegularClockPatch("p", ZERO4, 0.0)


@pytest.mark.parametrize("bad", [math.inf, -math.inf, math.nan])
def test_nonfinite_clock_coefficients_fail_closed(bad):
    with pytest.raises(SmoothClockExtensionError):
        RegularClockPatch("p", (1.0, 0.0, 0.0, 0.0), bad)


def test_singular_overlap_map_fails_closed():
    singular = (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    )
    with pytest.raises(SmoothClockExtensionError, match="must be invertible"):
        ClockOverlap("p", "q", singular, ZERO4)


def test_translation_cocycle_mismatch_fails_closed():
    patches = [patch("p", 0.0), patch("q", -2.0), patch("r", -5.0)]
    with pytest.raises(SmoothClockExtensionError, match="translation chart cocycle"):
        certify_regular_smooth_clock_extension(
            patches,
            [
                overlap("p", "q", 2.0),
                overlap("q", "r", 3.0),
                ClockOverlap("p", "r", I4, (5.0, 1.0, 0.0, 0.0)),
            ],
            {"e": 4.0},
            [EventEmbedding("e", "p", (1.0, 0.0, 0.0, 0.0))],
            triangles=[("p", "q", "r")],
        )
