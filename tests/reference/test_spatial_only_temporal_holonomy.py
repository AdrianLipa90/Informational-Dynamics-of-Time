import math

import pytest

from idt.spatial_only_temporal_holonomy import (
    SpatialTemporalHolonomyError,
    exact_temporal_potential_offset,
    round_trip_temporal_offset,
    spatial_only_transport,
    temporal_holonomy,
)


def test_spatial_only_transport_preserves_foliation_time_at_arbitrary_distance():
    audit = spatial_only_transport([0.0, 0.0, 0.0], [4.2465, 0.0, 0.0], tau=12.0)
    assert math.isclose(audit.spatial_distance, 4.2465, rel_tol=0.0, abs_tol=1e-15)
    assert audit.tau_after_transport == audit.tau_before == 12.0
    assert audit.transport_temporal_offset == 0.0


def test_large_spatial_distance_does_not_create_minus_distance_over_c_offset():
    audit = spatial_only_transport([0.0], [1.0e12], tau=3.0)
    assert audit.spatial_distance == 1.0e12
    assert audit.transport_temporal_offset == 0.0


def test_zero_temporal_connection_gives_zero_holonomy_independent_of_path_length():
    h = temporal_holonomy([[1.0e9, 0.0], [0.0, -2.0e9]], [[0.0, 0.0], [0.0, 0.0]])
    assert h.temporal_offset == 0.0
    assert h.classification == "ZERO_TEMPORAL_OFFSET"


def test_temporal_holonomy_is_discrete_line_integral():
    h = temporal_holonomy([[2.0, 0.0], [0.0, 3.0]], [[0.5, 0.0], [0.0, -0.25]])
    assert math.isclose(h.temporal_offset, 0.25, rel_tol=0.0, abs_tol=1e-15)


def test_orientation_reversal_flips_line_integral_with_same_connection_samples():
    forward = temporal_holonomy([[2.0, 1.0], [-1.0, 4.0]], [[0.3, -0.2], [0.1, 0.5]])
    reverse = temporal_holonomy([[-2.0, -1.0], [1.0, -4.0]], [[0.3, -0.2], [0.1, 0.5]])
    assert math.isclose(reverse.temporal_offset, -forward.temporal_offset, rel_tol=0.0, abs_tol=1e-15)


def test_round_trip_can_have_negative_model_offset_only_from_connection_holonomy():
    audit = round_trip_temporal_offset(
        [[1.0, 0.0]],
        [[-0.75, 0.0]],
        [[-1.0, 0.0]],
        [[0.25, 0.0]],
    )
    assert math.isclose(audit.temporal_offset, -1.0, rel_tol=0.0, abs_tol=1e-15)
    assert audit.classification == "NEGATIVE_TEMPORAL_OFFSET_MODEL_COORDINATE"


def test_exact_temporal_potential_has_zero_closed_loop_offset():
    assert exact_temporal_potential_offset(2.5, 2.5) == 0.0
    assert math.isclose(exact_temporal_potential_offset(2.5, 4.0), 1.5, abs_tol=1e-15)


@pytest.mark.parametrize(
    "x_start,x_end,tau",
    [
        ([0.0], [0.0, 1.0], 0.0),
        ([float("nan")], [0.0], 0.0),
    ],
)
def test_spatial_transport_fails_closed(x_start, x_end, tau):
    with pytest.raises(SpatialTemporalHolonomyError):
        spatial_only_transport(x_start, x_end, tau)


def test_holonomy_fails_closed_on_shape_mismatch():
    with pytest.raises(SpatialTemporalHolonomyError):
        temporal_holonomy([[1.0, 0.0]], [[1.0]])
