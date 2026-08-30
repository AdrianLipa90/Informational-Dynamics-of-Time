import pytest

from src.idt.temporal_trace_uniqueness import (
    ROT_X_PI,
    ROT_Y_PI,
    TemporalTraceUniquenessError,
    add,
    certificate,
    invariance_constraints,
    linear_functional,
    positive_cone_admitted,
    rotate_spatial,
    trace_temporal_scalar,
)


def test_spatial_linear_coefficients_fail_rotation_invariance():
    for coefficients in (
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ):
        assert any(abs(d) > 0.0 for d in invariance_constraints(coefficients))


def test_scalar_coefficient_is_invariant_under_spatial_rotations():
    coefficients = (7.0, 0.0, 0.0, 0.0)
    x = (3.0, 0.5, -0.25, 1.0)
    assert linear_functional(coefficients, rotate_spatial(x, ROT_X_PI)) == linear_functional(coefficients, x)
    assert linear_functional(coefficients, rotate_spatial(x, ROT_Y_PI)) == linear_functional(coefficients, x)


def test_trace_temporal_scalar_is_additive():
    a = (2.0, 0.5, 0.0, 0.0)
    b = (3.0, -0.5, 0.25, 0.0)
    assert trace_temporal_scalar(add(a, b)) == trace_temporal_scalar(a) + trace_temporal_scalar(b)


def test_trace_temporal_scalar_is_spatial_rotation_invariant():
    x = (4.0, 1.0, 2.0, -1.0)
    assert trace_temporal_scalar(rotate_spatial(x, ROT_Y_PI)) == trace_temporal_scalar(x)


def test_trace_temporal_scalar_is_positive_on_admitted_positive_cone():
    examples = (
        (1.0, 0.0, 0.0, 0.0),
        (2.0, 1.0, 0.0, 0.0),
        (3.0, 1.0, 2.0, 1.0),
    )
    for x in examples:
        assert positive_cone_admitted(x)
        assert trace_temporal_scalar(x) > 0.0


def test_certificate_passes():
    cert = certificate()
    assert cert.vector_coefficients_zero
    assert cert.trace_additive
    assert cert.trace_rotation_invariant
    assert cert.trace_positive_on_positive_examples


def test_fail_closed_invalid_calibration_and_nonfinite_coordinates():
    with pytest.raises(TemporalTraceUniquenessError):
        trace_temporal_scalar((1.0, 0.0, 0.0, 0.0), calibration=0.0)
    with pytest.raises(TemporalTraceUniquenessError):
        trace_temporal_scalar((float("nan"), 0.0, 0.0, 0.0))
